#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import issue26e_core as e

IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
STRUCTURED_SHA256 = "3ded6745d58701d1a1c38a38f268c57396afffbbbf0a681ec9b16bb09f1e47bd"
EXACT_SHA256 = "652e23fa08701a87e0aaab961f4a267f2389ccc19769eb31ed05e651c2bedfaf"
FIXED_MAP = (0, 3, 4, 1, 2, 5)
FOLDS = [
    {1,6,11,17,22,27,32,37,42,47,52,57,68,77,82,87,94,101,106,113},
    {2,7,13,18,23,28,33,38,43,48,53,58,69,78,83,88,95,102,107,114},
    {3,8,14,19,24,29,34,39,44,49,54,65,70,79,84,89,96,103,108,115},
    {4,9,15,20,25,30,35,40,45,50,55,66,75,80,85,90,99,104,111,116},
    {5,10,16,21,26,31,36,41,46,51,56,67,76,81,86,93,100,105,112},
]
E2C_MEAN_A = 0.8337140490098738
E2C_COVERAGE = 0.8213154353321266
E2C_FOLD_A = [
    0.8355972832600879, 0.8021775235283263, 0.8705357142857143,
    0.8484604223762695, 0.8117993015989707,
]
EPS = 1e-12


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def masks_to_matrix(masks):
    if len(masks) != 20:
        raise RuntimeError(f"expected 20 row masks, got {len(masks)}")
    M = np.zeros((20, 6), dtype=np.int8)
    for r, mask in enumerate(masks):
        if not isinstance(mask, int) or mask <= 0 or mask >= 64:
            raise RuntimeError(f"bad row mask {mask}")
        for c in range(6):
            M[r, c] = 1 if mask & (1 << c) else 0
    return M


def pair_matrix(M):
    return (M.T @ M).astype(int)


def pair_hist(M):
    Q = pair_matrix(M)
    vals = [int(Q[a, b]) for a, b in itertools.combinations(range(6), 2)]
    return {str(k): vals.count(k) for k in sorted(set(vals))}


def matrix_masks(M):
    return sorted(sum((1 << c) for c in range(6) if M[r, c]) for r in range(20))


def validate_common(M):
    if sorted(M.sum(1).astype(int).tolist()) != [1] * 4 + [2] * 10 + [3] * 6:
        raise RuntimeError("row degree multiset mismatch")
    if M.sum(0).astype(int).tolist() != [7] * 6:
        raise RuntimeError("column degree mismatch")
    if int(M.sum()) != 42:
        raise RuntimeError("cell count mismatch")


def load_catalogs(here: Path):
    sp = here / "E3_STRUCTURED_NULLS.json"
    ep = here / "E3_EXACT_PAIR_ALTERNATIVES.json"
    if sha256_file(sp) != STRUCTURED_SHA256:
        raise RuntimeError("structured catalog SHA mismatch")
    if sha256_file(ep) != EXACT_SHA256:
        raise RuntimeError("exact catalog SHA mismatch")
    s = json.loads(sp.read_text())
    x = json.loads(ep.read_text())

    G = e.GUIDO.astype(np.int8)
    validate_common(G)
    gpair = pair_matrix(G)
    ghist = pair_hist(G)
    gmasks = matrix_masks(G)

    if len(s.get("row_masks", [])) != 100:
        raise RuntimeError("structured catalog must have 100 matrices")
    structured = []
    seen = set()
    for masks in s["row_masks"]:
        key = tuple(masks)
        if key in seen or list(masks) != sorted(masks):
            raise RuntimeError("duplicate/unsorted structured row multiset")
        seen.add(key)
        M = masks_to_matrix(masks); validate_common(M)
        if pair_hist(M) != ghist:
            raise RuntimeError("structured pair-overlap histogram mismatch")
        if np.array_equal(pair_matrix(M), gpair):
            raise RuntimeError("structured catalog contains exact Guidonian pair matrix")
        if list(masks) == gmasks:
            raise RuntimeError("structured catalog contains Guidonian rows")
        structured.append(M)

    sols = x.get("solutions", [])
    if len(sols) != 4 or sum(bool(z.get("is_guidonian")) for z in sols) != 1:
        raise RuntimeError("exact enumeration must contain four solutions with one Guidonian")
    exact_alts = []
    for z in sols:
        M = masks_to_matrix(z["row_masks"]); validate_common(M)
        if not np.array_equal(pair_matrix(M), gpair):
            raise RuntimeError("exact candidate pair matrix mismatch")
        isg = matrix_masks(M) == gmasks
        if isg != bool(z["is_guidonian"]):
            raise RuntimeError("exact candidate Guidonian flag mismatch")
        if not isg:
            exact_alts.append(M)
    if len(exact_alts) != 3:
        raise RuntimeError("expected exactly three non-Guidonian exact alternatives")
    return structured, exact_alts, {
        "guidonian_pair_matrix": gpair.tolist(),
        "guidonian_pair_histogram": ghist,
        "structured_count": len(structured),
        "exact_non_guidonian_count": len(exact_alts),
    }


def fit_types(items, train, parser):
    vectors = {}
    for it in items:
        if it["leaf"] not in train:
            continue
        for line in it["lines"]:
            for tok in line:
                p = parser.pick(tok, "max")
                if p is not None and tok not in vectors:
                    vectors[tok] = e.feature(p[1])
    return e.KMeans20().fit(vectors), len(vectors)


def fit_fixed(C, lattice):
    W = np.zeros((20, 20), dtype=np.int64)
    for s, v in enumerate(FIXED_MAP):
        W += C[:, s, None] * lattice[None, :, v]
    score, _ = e.assignment_score(W)
    rows = e.lex_assignment(W, score)
    return {"training_allowed": int(score), "state_to_vox": list(FIXED_MAP), "cluster_to_row": rows.tolist()}


def score_lattice(C, H, visible, parsed, M):
    mapping = fit_fixed(C, M)
    score = e.score_counts(H, visible, parsed, mapping, M)
    return score["accuracy"], mapping["training_allowed"]


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} IT2a-n.txt", file=sys.stderr); return 2
    it = Path(sys.argv[1]).resolve()
    if hashlib.sha256(it.read_bytes()).hexdigest() != IT_SHA256:
        raise RuntimeError("IT2a SHA mismatch")

    here = Path(__file__).resolve().parent
    structured, exact_alts, catalog_audit = load_catalogs(here)
    parser = e.SlotParser(); validation = e.validate_parser(parser)
    items = e.parse_voynich(it)
    universe = set().union(*FOLDS)

    folds = []
    g_acc = []
    exact_acc = [[] for _ in exact_alts]
    structured_acc = [[] for _ in structured]
    for f, held in enumerate(FOLDS):
        train = universe - held
        km, ntypes = fit_types(items, train, parser)
        C, tvis, tpar = e.count_matrix(items, train, parser, "max", km)
        H, hvis, hpar = e.count_matrix(items, held, parser, "max", km)
        ga, gtrain = score_lattice(C, H, hvis, hpar, e.GUIDO)
        g_acc.append(ga)
        eacc = []
        for j, M in enumerate(exact_alts):
            a, _ = score_lattice(C, H, hvis, hpar, M)
            exact_acc[j].append(a); eacc.append(a)
        sacc = []
        for j, M in enumerate(structured):
            a, _ = score_lattice(C, H, hvis, hpar, M)
            structured_acc[j].append(a); sacc.append(a)
        med = statistics.median(sacc)
        folds.append({
            "fold": f, "held_leaves": sorted(held),
            "training_unique_parsed_types": ntypes,
            "training_visible_occurrences": tvis, "training_parsed_occurrences": tpar,
            "heldout_visible_occurrences": hvis, "heldout_parsed_occurrences": hpar,
            "parse_coverage": hpar / hvis if hvis else 0.0,
            "guidonian_accuracy": ga, "guidonian_training_allowed": gtrain,
            "exact_alternative_accuracies": eacc,
            "structured_null_median": med,
            "structured_null_q95": e.quantile(sacc, .95),
            "guidonian_minus_structured_median": ga - med,
            "structured_p_fold": (1 + sum(x >= ga - EPS for x in sacc)) / 101,
        })

    mean_g = statistics.mean(g_acc)
    coverage = statistics.mean(x["parse_coverage"] for x in folds)
    if abs(mean_g - E2C_MEAN_A) > EPS or abs(coverage - E2C_COVERAGE) > EPS:
        raise RuntimeError(f"E2C replay mismatch meanA={mean_g} coverage={coverage}")
    if any(abs(a-b) > EPS for a,b in zip(g_acc, E2C_FOLD_A)):
        raise RuntimeError(f"E2C fold replay mismatch {g_acc}")

    exact_rows = []
    exact_pass = True
    for j, xs in enumerate(exact_acc):
        ma = statistics.mean(xs)
        wins = sum(g > a + EPS for g, a in zip(g_acc, xs))
        ties = sum(abs(g-a) <= EPS for g, a in zip(g_acc, xs))
        row = {"alternative": j, "mean_accuracy": ma, "guidonian_minus_alternative": mean_g-ma,
               "guidonian_strict_fold_wins": wins, "fold_ties": ties, "fold_accuracies": xs}
        exact_rows.append(row)
        if not (mean_g > ma + EPS and wins >= 3):
            exact_pass = False

    mean_null = [statistics.mean(xs) for xs in structured_acc]
    med_null = statistics.median(mean_null)
    p_global = (1 + sum(x >= mean_g - EPS for x in mean_null)) / 101
    b_wins = sum(x["guidonian_accuracy"] > x["structured_null_median"] + EPS for x in folds)
    structured_pass = p_global <= .05 and mean_g > med_null + EPS and b_wins >= 4

    if not exact_pass:
        verdict = "PAIR-GEOMETRY SUFFICIENT / GUIDONIAN NOT SPECIFIC"
    elif structured_pass:
        verdict = "GUIDONIAN-SPECIFIC BEYOND PAIR GEOMETRY"
    else:
        verdict = "STRUCTURED-NULL CHALLENGE NOT SURVIVED"

    out = {
        "experiment": "Issue26E3 structured-null specificity challenge", "issue": 26,
        "inputs": {
            "it_sha256": IT_SHA256,
            "plan_sha256": sha256_file(here / "PLAN_E3.md"),
            "core_sha256": sha256_file(here / "issue26e_core.py"),
            "structured_catalog_sha256": STRUCTURED_SHA256,
            "exact_catalog_sha256": EXACT_SHA256,
            "script_sha256": sha256_file(Path(__file__)),
            "fixed_state_to_vox": list(FIXED_MAP),
        },
        "slot_parser_validation": validation,
        "catalog_audit": catalog_audit,
        "e2c_replay": {"mean_parse_coverage": coverage, "mean_guidonian_accuracy": mean_g,
                        "fold_accuracies": g_acc},
        "folds": folds,
        "E3A_exact_pair_tournament": {"pass": exact_pass, "guidonian_mean": mean_g,
                                       "alternatives": exact_rows},
        "E3B_structured_null": {
            "pass": structured_pass, "guidonian_mean": mean_g,
            "null_mean_median": med_null, "null_mean_q95": e.quantile(mean_null, .95),
            "guidonian_advantage": mean_g-med_null, "p_global": p_global,
            "fold_median_wins": b_wins, "null_mean_min": min(mean_null), "null_mean_max": max(mean_null),
        },
        "frozen_classification": verdict,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True); print(); return 0

if __name__ == "__main__":
    raise SystemExit(main())
