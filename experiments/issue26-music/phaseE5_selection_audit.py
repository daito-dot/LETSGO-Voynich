#!/usr/bin/env python3
from __future__ import annotations

import collections
import hashlib
import json
import statistics
import sys
from pathlib import Path

import numpy as np

import issue26e_core as e

IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
STRUCTURED_SHA256 = "3ded6745d58701d1a1c38a38f268c57396afffbbbf0a681ec9b16bb09f1e47bd"
EXACT_SHA256 = "652e23fa08701a87e0aaab961f4a267f2389ccc19769eb31ed05e651c2bedfaf"
EXPECTED_GUIDO_MAP = (0, 3, 4, 1, 2, 5)
EXPECTED_GUIDO_IT_MEAN = 0.8337140490098738
EXPECTED_GUIDO_IT_FOLDS = [
    0.8355972832600879,
    0.8021775235283263,
    0.8705357142857143,
    0.8484604223762695,
    0.8117993015989707,
]
N_DEGREE_NULL = 200
SWAP_ATTEMPTS = 5000
EPS = 1e-12

FOLDS = [
    {1,6,11,17,22,27,32,37,42,47,52,57,68,77,82,87,94,101,106,113},
    {2,7,13,18,23,28,33,38,43,48,53,58,69,78,83,88,95,102,107,114},
    {3,8,14,19,24,29,34,39,44,49,54,65,70,79,84,89,96,103,108,115},
    {4,9,15,20,25,30,35,40,45,50,55,66,75,80,85,90,99,104,111,116},
    {5,10,16,21,26,31,36,41,46,51,56,67,76,81,86,93,100,105,112},
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def masks_to_matrix(masks):
    if len(masks) != 20:
        raise RuntimeError(f"expected 20 rows, got {len(masks)}")
    M = np.zeros((20, 6), dtype=np.int8)
    for r, mask in enumerate(masks):
        if not isinstance(mask, int) or mask <= 0 or mask >= 64:
            raise RuntimeError(f"bad row mask {mask}")
        for c in range(6):
            M[r, c] = int(bool(mask & (1 << c)))
    return M


def validate_capacity(M):
    if M.shape != (20, 6):
        raise RuntimeError("shape mismatch")
    if sorted(M.sum(1).astype(int).tolist()) != [1] * 4 + [2] * 10 + [3] * 6:
        raise RuntimeError("row-degree multiset mismatch")
    if M.sum(0).astype(int).tolist() != [7] * 6:
        raise RuntimeError("column-degree mismatch")
    if int(M.sum()) != 42:
        raise RuntimeError("cell-count mismatch")


def load_previous_catalogs(here: Path):
    sp = here / "E3_STRUCTURED_NULLS.json"
    ep = here / "E3_EXACT_PAIR_ALTERNATIVES.json"
    if sha256_file(sp) != STRUCTURED_SHA256:
        raise RuntimeError("structured catalog hash mismatch")
    if sha256_file(ep) != EXACT_SHA256:
        raise RuntimeError("exact catalog hash mismatch")
    s = json.loads(sp.read_text())
    x = json.loads(ep.read_text())
    structured = [masks_to_matrix(z) for z in s["row_masks"]]
    if len(structured) != 100:
        raise RuntimeError("expected 100 structured nulls")
    for M in structured:
        validate_capacity(M)
    exact = []
    for z in x["solutions"]:
        if not z.get("is_guidonian"):
            M = masks_to_matrix(z["row_masks"])
            validate_capacity(M)
            exact.append(M)
    if len(exact) != 3:
        raise RuntimeError("expected three exact-pair alternatives")
    return structured, exact


def generate_degree_nulls():
    seen = set()
    out = []
    for j in range(N_DEGREE_NULL):
        M = e.swapped_lattice(f"Issue26E5:degree:null:{j}", seen, SWAP_ATTEMPTS)
        validate_capacity(M)
        out.append(M)
    return out


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


def precompute(items, parser):
    universe = set().union(*FOLDS)
    out = {}
    for policy in ("min", "max"):
        rows = []
        for f, held in enumerate(FOLDS):
            train = universe - held
            km, ntypes = fit_types(items, train, parser, policy)
            C, tvis, tpar = e.count_matrix(items, train, parser, policy, km)
            H, hvis, hpar = e.count_matrix(items, held, parser, policy, km)
            rows.append({
                "fold": f,
                "C": C,
                "H": H,
                "training_unique_parsed_types": ntypes,
                "training_visible_occurrences": tvis,
                "training_parsed_occurrences": tpar,
                "heldout_visible_occurrences": hvis,
                "heldout_parsed_occurrences": hpar,
                "parse_coverage": hpar / hvis if hvis else 0.0,
            })
        out[policy] = rows
    return out


def fit_fixed(C, lattice, perm):
    W = np.zeros((20, 20), dtype=np.int64)
    for s, v in enumerate(perm):
        W += C[:, s, None] * lattice[None, :, v]
    score, _ = e.assignment_score(W)
    rows = e.lex_assignment(W, score)
    return {
        "training_allowed": int(score),
        "state_to_vox": list(perm),
        "cluster_to_row": rows.tolist(),
    }


def score_fold(pre, lattice, mapping):
    return e.score_counts(
        pre["H"],
        pre["heldout_visible_occurrences"],
        pre["heldout_parsed_occurrences"],
        mapping,
        lattice,
    )["accuracy"]


def fixed_cv(pre_rows, lattice, perm):
    xs = []
    for z in pre_rows:
        m = fit_fixed(z["C"], lattice, perm)
        xs.append(score_fold(z, lattice, m))
    return statistics.mean(xs), xs


def select_on_zl(zl_pre, lattice):
    per_policy = {}
    for policy in ("min", "max"):
        free_maps = [e.fit_mapping(z["C"], lattice) for z in zl_pre[policy]]
        perms = [tuple(m["state_to_vox"]) for m in free_maps]
        counts = collections.Counter(perms)
        recurrence = max(counts.values())
        modes = sorted(q for q, n in counts.items() if n == recurrence)
        candidates = []
        for q in modes:
            mean_a, folds = fixed_cv(zl_pre[policy], lattice, q)
            candidates.append((mean_a, q, folds))
        best_mean = max(x[0] for x in candidates)
        tied = [x for x in candidates if abs(x[0] - best_mean) <= EPS]
        best_mean, best_q, best_folds = min(tied, key=lambda x: x[1])
        free_fold_a = [score_fold(z, lattice, m) for z, m in zip(zl_pre[policy], free_maps)]
        per_policy[policy] = {
            "recurrence": recurrence,
            "fitted_permutations": [list(q) for q in perms],
            "mode_count": len(modes),
            "mode_permutations": [list(q) for q in modes],
            "selected_map": list(best_q),
            "fixed_map_zl_mean_accuracy": best_mean,
            "fixed_map_zl_fold_accuracies": best_folds,
            "free_map_zl_mean_accuracy": statistics.mean(free_fold_a),
            "free_map_zl_fold_accuracies": free_fold_a,
        }

    def better(a, b):
        pa, xa = a
        pb, xb = b
        if xa["recurrence"] != xb["recurrence"]:
            return a if xa["recurrence"] > xb["recurrence"] else b
        if abs(xa["fixed_map_zl_mean_accuracy"] - xb["fixed_map_zl_mean_accuracy"]) > EPS:
            return a if xa["fixed_map_zl_mean_accuracy"] > xb["fixed_map_zl_mean_accuracy"] else b
        return a if pa < pb else b

    selected_policy, selected = better(("min", per_policy["min"]), ("max", per_policy["max"]))
    return selected_policy, tuple(selected["selected_map"]), per_policy


def transfer_to_it(it_pre, lattice, policy, perm):
    folds = []
    for z in it_pre[policy]:
        m = fit_fixed(z["C"], lattice, perm)
        folds.append(score_fold(z, lattice, m))
    return statistics.mean(folds), folds


def evaluate_candidate(zl_pre, it_pre, lattice, label, include_detail=False):
    policy, perm, per_policy = select_on_zl(zl_pre, lattice)
    mean_it, fold_it = transfer_to_it(it_pre, lattice, policy, perm)
    chosen = per_policy[policy]
    out = {
        "label": label,
        "selected_policy": policy,
        "selected_recurrence": chosen["recurrence"],
        "selected_map": list(perm),
        "selected_zl_fixed_mean_accuracy": chosen["fixed_map_zl_mean_accuracy"],
        "it_fixed_mean_accuracy": mean_it,
        "it_fixed_fold_accuracies": fold_it,
    }
    if include_detail:
        out["zl_policy_diagnostics"] = per_policy
    return out


def family_stats(rows, g):
    n = len(rows)
    ag = g["it_fixed_mean_accuracy"]
    rg = g["selected_recurrence"]
    transfer_exceed = sum(r["it_fixed_mean_accuracy"] >= ag - EPS for r in rows)
    joint_exceed = sum(
        r["selected_recurrence"] >= rg and r["it_fixed_mean_accuracy"] >= ag - EPS
        for r in rows
    )
    lex_exceed = sum(
        r["selected_recurrence"] > rg
        or (r["selected_recurrence"] == rg and r["it_fixed_mean_accuracy"] >= ag - EPS)
        for r in rows
    )
    acc = [r["it_fixed_mean_accuracy"] for r in rows]
    rec = collections.Counter(r["selected_recurrence"] for r in rows)
    return {
        "n": n,
        "p_transfer": (1 + transfer_exceed) / (n + 1),
        "p_joint": (1 + joint_exceed) / (n + 1),
        "p_lex": (1 + lex_exceed) / (n + 1),
        "transfer_exceedances": transfer_exceed,
        "joint_exceedances": joint_exceed,
        "lex_exceedances": lex_exceed,
        "it_accuracy_median": statistics.median(acc),
        "it_accuracy_q95": e.quantile(acc, .95),
        "it_accuracy_min": min(acc),
        "it_accuracy_max": max(acc),
        "recurrence_distribution": {str(k): rec[k] for k in sorted(rec)},
    }


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt", file=sys.stderr)
        return 2
    zl = Path(sys.argv[1]).resolve()
    it = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL blob mismatch")
    if hashlib.sha256(it.read_bytes()).hexdigest() != IT_SHA256:
        raise RuntimeError("IT2a hash mismatch")

    here = Path(__file__).resolve().parent
    structured, exact = load_previous_catalogs(here)
    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    zl_items = e.parse_voynich(zl)
    it_items = e.parse_voynich(it)
    zl_pre = precompute(zl_items, parser)
    it_pre = precompute(it_items, parser)

    guid = evaluate_candidate(zl_pre, it_pre, e.GUIDO, "GUIDONIAN", include_detail=True)
    if guid["selected_policy"] != "max":
        raise RuntimeError(f"Guidonian policy replay mismatch: {guid['selected_policy']}")
    if guid["selected_recurrence"] != 4:
        raise RuntimeError(f"Guidonian recurrence replay mismatch: {guid['selected_recurrence']}")
    if tuple(guid["selected_map"]) != EXPECTED_GUIDO_MAP:
        raise RuntimeError(f"Guidonian mapping replay mismatch: {guid['selected_map']}")
    if abs(guid["it_fixed_mean_accuracy"] - EXPECTED_GUIDO_IT_MEAN) > EPS:
        raise RuntimeError(f"Guidonian IT mean replay mismatch: {guid['it_fixed_mean_accuracy']}")
    if any(abs(a - b) > EPS for a, b in zip(guid["it_fixed_fold_accuracies"], EXPECTED_GUIDO_IT_FOLDS)):
        raise RuntimeError(f"Guidonian IT folds replay mismatch: {guid['it_fixed_fold_accuracies']}")

    degree_lattices = generate_degree_nulls()
    degree_rows = [
        evaluate_candidate(zl_pre, it_pre, M, f"degree_{j:03d}")
        for j, M in enumerate(degree_lattices)
    ]
    structured_rows = [
        evaluate_candidate(zl_pre, it_pre, M, f"structured_{j:03d}")
        for j, M in enumerate(structured)
    ]
    exact_rows = [
        evaluate_candidate(zl_pre, it_pre, M, f"exact_pair_alt_{j}", include_detail=True)
        for j, M in enumerate(exact)
    ]

    degree_stats = family_stats(degree_rows, guid)
    structured_stats = family_stats(structured_rows, guid)
    primary_pass = (
        degree_stats["p_transfer"] <= .05
        and degree_stats["p_joint"] <= .05
        and degree_stats["p_lex"] <= .05
    )
    exact_dominates = any(
        r["selected_recurrence"] >= guid["selected_recurrence"]
        and r["it_fixed_mean_accuracy"] >= guid["it_fixed_mean_accuracy"] - EPS
        for r in exact_rows
    )

    if not primary_pass:
        verdict = "SELECTION FREEDOM EXPLAINS THE APPARENT SURPRISE"
    elif structured_stats["p_joint"] > .05 or exact_dominates:
        verdict = "EXTERNAL FIT SURVIVES ORDINARY NULLS BUT NOT STRUCTURAL SPECIFICITY"
    else:
        verdict = "SELECTION-ADJUSTED EXTERNAL FIT REMAINS UNUSUAL"

    out = {
        "experiment": "Issue26E5 selection-adjusted external-structure surprise audit",
        "issue": 26,
        "inputs": {
            "zl_blob_sha1": e.EXPECTED_ZL3B_BLOB,
            "it_sha256": IT_SHA256,
            "plan_sha256": sha256_file(here / "PLAN_E5.md"),
            "core_sha256": sha256_file(here / "issue26e_core.py"),
            "structured_catalog_sha256": STRUCTURED_SHA256,
            "exact_catalog_sha256": EXACT_SHA256,
            "script_sha256": sha256_file(Path(__file__)),
            "n_degree_null": N_DEGREE_NULL,
        },
        "slot_parser_validation": validation,
        "guidonian_replay_and_selection": guid,
        "primary_degree_matched": {
            "stats": degree_stats,
            "rows": degree_rows,
        },
        "secondary_structured": {
            "stats": structured_stats,
            "rows": structured_rows,
        },
        "exact_pair_alternatives": exact_rows,
        "exact_pair_any_joint_dominance": exact_dominates,
        "primary_pass": primary_pass,
        "frozen_classification": verdict,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
