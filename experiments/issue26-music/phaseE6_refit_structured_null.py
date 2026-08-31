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
FOLDS = [
    {1,6,11,17,22,27,32,37,42,47,52,57,68,77,82,87,94,101,106,113},
    {2,7,13,18,23,28,33,38,43,48,53,58,69,78,83,88,95,102,107,114},
    {3,8,14,19,24,29,34,39,44,49,54,65,70,79,84,89,96,103,108,115},
    {4,9,15,20,25,30,35,40,45,50,55,66,75,80,85,90,99,104,111,116},
    {5,10,16,21,26,31,36,41,46,51,56,67,76,81,86,93,100,105,112},
]
EXPECTED = {
    ("ZL", "min"): 0.8509664380470466,
    ("ZL", "max"): 0.8439032769036159,
    ("IT", "min"): 0.8512154779726009,
    ("IT", "max"): 0.8404723923113318,
}
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

    structured = []
    seen = set()
    for masks in s.get("row_masks", []):
        key = tuple(masks)
        if key in seen or list(masks) != sorted(masks):
            raise RuntimeError("duplicate/unsorted structured row multiset")
        seen.add(key)
        M = masks_to_matrix(masks)
        validate_common(M)
        if pair_hist(M) != ghist:
            raise RuntimeError("structured pair-overlap histogram mismatch")
        if np.array_equal(pair_matrix(M), gpair):
            raise RuntimeError("structured catalog contains exact Guidonian pair matrix")
        if matrix_masks(M) == gmasks:
            raise RuntimeError("structured catalog contains Guidonian rows")
        structured.append(M)
    if len(structured) != 100:
        raise RuntimeError(f"expected 100 structured nulls, got {len(structured)}")

    sols = x.get("solutions", [])
    if len(sols) != 4 or sum(bool(z.get("is_guidonian")) for z in sols) != 1:
        raise RuntimeError("exact enumeration must contain four solutions with one Guidonian")
    exact_alts = []
    for z in sols:
        M = masks_to_matrix(z["row_masks"])
        validate_common(M)
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
        "structured_count": len(structured),
        "exact_non_guidonian_count": len(exact_alts),
        "guidonian_pair_histogram": ghist,
        "guidonian_pair_matrix": gpair.tolist(),
    }


def fit_types(items, train, parser, policy):
    vectors = {}
    for it in items:
        if it["leaf"] not in train:
            continue
        for line in it["lines"]:
            for tok in line:
                p = parser.pick(tok, policy)
                if p is not None and tok not in vectors:
                    vectors[tok] = e.feature(p[1])
    return e.KMeans20().fit(vectors), len(vectors)


def score_candidate(C, H, visible, parsed, lattice):
    mapping = e.fit_mapping(C, lattice)
    score = e.score_counts(H, visible, parsed, mapping, lattice)
    return score["accuracy"], mapping


def evaluate(items, parser, dataset, policy, structured, exact_alts):
    universe = set().union(*FOLDS)
    folds = []
    g_acc = []
    s_acc = [[] for _ in structured]
    x_acc = [[] for _ in exact_alts]

    for f, held in enumerate(FOLDS):
        train = universe - held
        km, ntypes = fit_types(items, train, parser, policy)
        C, tvis, tpar = e.count_matrix(items, train, parser, policy, km)
        H, hvis, hpar = e.count_matrix(items, held, parser, policy, km)

        ga, gm = score_candidate(C, H, hvis, hpar, e.GUIDO)
        g_acc.append(ga)

        sfold = []
        for j, M in enumerate(structured):
            a, _ = score_candidate(C, H, hvis, hpar, M)
            s_acc[j].append(a)
            sfold.append(a)

        xfold = []
        for j, M in enumerate(exact_alts):
            a, xm = score_candidate(C, H, hvis, hpar, M)
            x_acc[j].append(a)
            xfold.append({"alternative": j, "accuracy": a, "mapping": xm})

        folds.append({
            "fold": f,
            "held_leaves": sorted(held),
            "training_unique_parsed_types": ntypes,
            "training_visible_occurrences": tvis,
            "training_parsed_occurrences": tpar,
            "heldout_visible_occurrences": hvis,
            "heldout_parsed_occurrences": hpar,
            "parse_coverage": hpar / hvis if hvis else 0.0,
            "guidonian_accuracy": ga,
            "guidonian_mapping": gm,
            "structured_fold_median": statistics.median(sfold),
            "structured_fold_q95": e.quantile(sfold, .95),
            "exact_alternatives": xfold,
        })

    mean_g = statistics.mean(g_acc)
    expected = EXPECTED[(dataset, policy)]
    if abs(mean_g - expected) > EPS:
        raise RuntimeError(
            f"{dataset}/{policy} Guidonian replay mismatch: {mean_g} != {expected}"
        )

    s_means = [statistics.mean(xs) for xs in s_acc]
    s_med = statistics.median(s_means)
    p_s = (1 + sum(x >= mean_g - EPS for x in s_means)) / (len(s_means) + 1)
    structured_pass = p_s <= .05 and mean_g > s_med + EPS

    exact_rows = []
    exact_pass = True
    for j, xs in enumerate(x_acc):
        ma = statistics.mean(xs)
        wins = sum(g > a + EPS for g, a in zip(g_acc, xs))
        ties = sum(abs(g - a) <= EPS for g, a in zip(g_acc, xs))
        row = {
            "alternative": j,
            "mean_accuracy": ma,
            "guidonian_minus_alternative": mean_g - ma,
            "guidonian_strict_fold_wins": wins,
            "fold_ties": ties,
            "fold_accuracies": xs,
        }
        exact_rows.append(row)
        if not (mean_g > ma + EPS):
            exact_pass = False

    return {
        "dataset": dataset,
        "policy": policy,
        "mean_parse_coverage": statistics.mean(x["parse_coverage"] for x in folds),
        "guidonian_mean_accuracy": mean_g,
        "guidonian_fold_accuracies": g_acc,
        "replay_expected": expected,
        "replay_pass": True,
        "structured": {
            "pass": structured_pass,
            "n": len(s_means),
            "mean_median": s_med,
            "mean_q95": e.quantile(s_means, .95),
            "mean_min": min(s_means),
            "mean_max": max(s_means),
            "guidonian_advantage_over_median": mean_g - s_med,
            "exceedances": sum(x >= mean_g - EPS for x in s_means),
            "p_global": p_s,
            "mean_accuracies": s_means,
        },
        "exact_pair": {
            "pass": exact_pass,
            "alternatives": exact_rows,
        },
        "folds": folds,
    }


def classify(zl, it):
    exact_ok = zl["exact_pair"]["pass"] and it["exact_pair"]["pass"]
    structured_ok = zl["structured"]["pass"] and it["structured"]["pass"]
    if not exact_ok:
        return "PAIR GEOMETRY / GENERIC STRUCTURE SUFFICIENT UNDER FULL REFIT"
    if structured_ok:
        return "GUIDONIAN SPECIFICITY SURVIVES FULL REFIT"
    return "STRUCTURED NULLS EXPLAIN ARCHITECTURE EFFECT"


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    it = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")
    if hashlib.sha256(it.read_bytes()).hexdigest() != IT_SHA256:
        raise RuntimeError("IT2a SHA mismatch")

    here = Path(__file__).resolve().parent
    structured, exact_alts, catalog_audit = load_catalogs(here)
    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    zl_items = e.parse_voynich(zl)
    it_items = e.parse_voynich(it)

    zl_min = evaluate(zl_items, parser, "ZL", "min", structured, exact_alts)
    it_min = evaluate(it_items, parser, "IT", "min", structured, exact_alts)
    primary = classify(zl_min, it_min)

    zl_max = evaluate(zl_items, parser, "ZL", "max", structured, exact_alts)
    it_max = evaluate(it_items, parser, "IT", "max", structured, exact_alts)
    sensitivity = classify(zl_max, it_max)

    out = {
        "experiment": "Issue26E6 fully-refitted structured-null architecture audit",
        "issue": 26,
        "inputs": {
            "zl_blob_sha1": e.EXPECTED_ZL3B_BLOB,
            "it_sha256": IT_SHA256,
            "plan_sha256": sha256_file(here / "PLAN_E6.md"),
            "core_sha256": sha256_file(here / "issue26e_core.py"),
            "structured_catalog_sha256": STRUCTURED_SHA256,
            "exact_catalog_sha256": EXACT_SHA256,
            "script_sha256": sha256_file(Path(__file__)),
        },
        "slot_parser_validation": validation,
        "catalog_audit": catalog_audit,
        "primary_min": {"ZL": zl_min, "IT": it_min},
        "sensitivity_max": {"ZL": zl_max, "IT": it_max},
        "frozen_classification": primary,
        "max_sensitivity_classification": sensitivity,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
