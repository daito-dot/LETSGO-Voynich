#!/usr/bin/env python3
from __future__ import annotations

import collections
import hashlib
import itertools
import json
import statistics
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp

import issue26e_core as e

ZL_BLOB_SHA1 = "2a4533ab9bdfa85db9bad602d590978953055df1"
IT_SHA256 = "7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5"
EXACT_SHA256 = "652e23fa08701a87e0aaab961f4a267f2389ccc19769eb31ed05e651c2bedfaf"
FIXED_MAP = (0, 3, 4, 1, 2, 5)  # raw EMPTY,d,l,r,m,n -> ut,re,mi,fa,sol,la columns
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
    0.8355972832600879,
    0.8021775235283263,
    0.8705357142857143,
    0.8484604223762695,
    0.8117993015989707,
]
EPS = 1e-12
DEGREES = (1, 2, 3)
DEGREE_COUNTS = (4, 10, 6)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fit_types(items, leaves, parser):
    vectors = {}
    for it in items:
        if it["leaf"] not in leaves:
            continue
        for line in it["lines"]:
            for tok in line:
                p = parser.pick(tok, "max")
                if p is not None and tok not in vectors:
                    vectors[tok] = e.feature(p[1])
    return e.KMeans20().fit(vectors), len(vectors)


def matrix_masks(M):
    return sorted(
        sum((1 << s) for s in range(6) if int(M[r, s]))
        for r in range(20)
    )


def masks_to_matrix(masks):
    M = np.zeros((20, 6), dtype=np.int8)
    for r, mask in enumerate(masks):
        for s in range(6):
            M[r, s] = 1 if int(mask) & (1 << s) else 0
    return M


def validate_capacity(M):
    if M.shape != (20, 6):
        raise RuntimeError(f"bad topology shape {M.shape}")
    if sorted(M.sum(1).astype(int).tolist()) != [1] * 4 + [2] * 10 + [3] * 6:
        raise RuntimeError("row-degree multiset mismatch")
    if M.sum(0).astype(int).tolist() != [7] * 6:
        raise RuntimeError("column-degree mismatch")
    if int(M.sum()) != 42:
        raise RuntimeError("cell-count mismatch")


def pair_matrix(M):
    return (M.T @ M).astype(int)


def pair_hist(M):
    Q = pair_matrix(M)
    vals = [int(Q[a, b]) for a, b in itertools.combinations(range(6), 2)]
    return {str(k): vals.count(k) for k in sorted(set(vals))}


def pair_l1_upper(A, B):
    return int(sum(abs(int(A[a, b]) - int(B[a, b])) for a, b in itertools.combinations(range(6), 2)))


def raw_guidonian():
    G = np.zeros((20, 6), dtype=np.int8)
    for s, v in enumerate(FIXED_MAP):
        G[:, s] = e.GUIDO[:, v]
    validate_capacity(G)
    return G


def build_milp_constraints(C, primary_score=None):
    nx = 20 * 6
    ny = 20 * 3
    n = nx + ny
    rows = []
    rhs = []

    def xi(c, s):
        return c * 6 + s

    def yi(c, k):
        return nx + c * 3 + k

    for c in range(20):
        row = np.zeros(n, dtype=float)
        for k in range(3):
            row[yi(c, k)] = 1.0
        rows.append(row); rhs.append(1.0)

    for c in range(20):
        row = np.zeros(n, dtype=float)
        for s in range(6):
            row[xi(c, s)] = 1.0
        for k, d in enumerate(DEGREES):
            row[yi(c, k)] = -float(d)
        rows.append(row); rhs.append(0.0)

    for k, need in enumerate(DEGREE_COUNTS):
        row = np.zeros(n, dtype=float)
        for c in range(20):
            row[yi(c, k)] = 1.0
        rows.append(row); rhs.append(float(need))

    for s in range(6):
        row = np.zeros(n, dtype=float)
        for c in range(20):
            row[xi(c, s)] = 1.0
        rows.append(row); rhs.append(7.0)

    if primary_score is not None:
        row = np.zeros(n, dtype=float)
        row[:nx] = C.astype(float).reshape(-1)
        rows.append(row); rhs.append(float(primary_score))

    A = np.stack(rows)
    b = np.asarray(rhs, dtype=float)
    return LinearConstraint(A, b, b)


def rounded_binary_solution(res, n):
    if not res.success or res.x is None:
        raise RuntimeError(f"MILP failed: status={res.status} message={res.message}")
    z = np.rint(res.x).astype(np.int8)
    if np.max(np.abs(res.x - z)) > 1e-6:
        raise RuntimeError("MILP returned non-integral solution beyond tolerance")
    if len(z) != n:
        raise RuntimeError("MILP solution length mismatch")
    return z


def learn_nonmusic_topology(C):
    C = np.asarray(C, dtype=np.int64)
    if C.shape != (20, 6):
        raise RuntimeError("ZL count matrix shape mismatch")
    nx = 120
    n = 180
    integrality = np.ones(n, dtype=np.int8)
    bounds = Bounds(np.zeros(n), np.ones(n))

    c1 = np.zeros(n, dtype=float)
    c1[:nx] = -C.reshape(-1).astype(float)
    res1 = milp(
        c=c1,
        integrality=integrality,
        bounds=bounds,
        constraints=build_milp_constraints(C),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    z1 = rounded_binary_solution(res1, n)
    X1 = z1[:nx].reshape(20, 6)
    primary = int((C * X1).sum())
    validate_capacity(X1)

    # SHA256-derived deterministic ranking of the 120 cell variables.  The
    # maximum possible total secondary objective is 9.438e-5 (< 1e-4).
    keyed = []
    for i in range(nx):
        h = hashlib.sha256(f"Issue26E4:secondary:{i}".encode()).digest()
        keyed.append((h, i))
    ordered = [i for _, i in sorted(keyed)]
    rank = np.empty(nx, dtype=int)
    for r, i in enumerate(ordered, start=1):
        rank[i] = r
    unit = 1.3e-8
    weights = rank.astype(float) * unit
    if float(weights.sum()) >= 1e-4:
        raise RuntimeError("secondary objective range invariant failed")

    c2 = np.zeros(n, dtype=float)
    c2[:nx] = -weights
    res2 = milp(
        c=c2,
        integrality=integrality,
        bounds=bounds,
        constraints=build_milp_constraints(C, primary_score=primary),
        options={"presolve": True, "mip_rel_gap": 0.0},
    )
    z2 = rounded_binary_solution(res2, n)
    X2 = z2[:nx].reshape(20, 6)
    validate_capacity(X2)
    primary2 = int((C * X2).sum())
    if primary2 != primary:
        raise RuntimeError(f"secondary solve changed primary score {primary2} != {primary}")

    masks = matrix_masks(X2)
    T = masks_to_matrix(masks)
    validate_capacity(T)
    return T, {
        "primary_optimum_allowed_occurrences": primary,
        "secondary_objective_value": float((weights * X2.reshape(-1)).sum()),
        "secondary_total_weight_range": float(weights.sum()),
        "cluster_specific_row_masks_before_identity_discard": [
            sum((1 << s) for s in range(6) if int(X2[c, s])) for c in range(20)
        ],
        "transferable_sorted_row_masks": masks,
    }


def fit_raw(C, M):
    W = np.zeros((20, 20), dtype=np.int64)
    for s in range(6):
        W += C[:, s, None] * M[None, :, s]
    score, _ = e.assignment_score(W)
    rows = e.lex_assignment(W, score)
    return {"training_allowed": int(score), "cluster_to_row": rows.tolist()}


def score_raw(H, parsed, mapping, M):
    allowed = 0
    for c in range(20):
        r = mapping["cluster_to_row"][c]
        for s in range(6):
            allowed += int(H[c, s]) * int(M[r, s])
    return {
        "parsed_occurrences": int(parsed),
        "allowed_occurrences": int(allowed),
        "accuracy": allowed / parsed if parsed else 0.0,
    }


def load_e3_alternatives(here):
    p = here / "E3_EXACT_PAIR_ALTERNATIVES.json"
    if sha256_file(p) != EXACT_SHA256:
        raise RuntimeError("E3 exact-pair catalog SHA mismatch")
    data = json.loads(p.read_text())
    out = []
    for z in data.get("solutions", []):
        if z.get("is_guidonian"):
            continue
        Mv = masks_to_matrix(z["row_masks"])
        Mr = np.zeros((20, 6), dtype=np.int8)
        for s, v in enumerate(FIXED_MAP):
            Mr[:, s] = Mv[:, v]
        validate_capacity(Mr)
        out.append(Mr)
    if len(out) != 3:
        raise RuntimeError("expected three E3 exact-pair alternatives")
    return out


def topology_diagnostics(T, G, e3_alts):
    tq = pair_matrix(T); gq = pair_matrix(G)
    tm = matrix_masks(T); gm = matrix_masks(G)
    alt_rows = []
    for j, M in enumerate(e3_alts):
        mq = pair_matrix(M)
        alt_rows.append({
            "alternative": j,
            "exact_row_multiset_match": matrix_masks(M) == tm,
            "pair_matrix_l1_upper": pair_l1_upper(tq, mq),
        })
    return {
        "raw_state_order": list(e.SLOT10_STATES),
        "generic_pair_matrix": tq.tolist(),
        "guidonian_raw_pair_matrix": gq.tolist(),
        "pair_matrix_exact_equal": bool(np.array_equal(tq, gq)),
        "pair_matrix_l1_upper": pair_l1_upper(tq, gq),
        "generic_pair_histogram": pair_hist(T),
        "guidonian_pair_histogram": pair_hist(G),
        "generic_row_mask_counts": {str(k): v for k, v in sorted(collections.Counter(tm).items())},
        "guidonian_row_mask_counts": {str(k): v for k, v in sorted(collections.Counter(gm).items())},
        "e3_exact_pair_alternative_comparison": alt_rows,
    }


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt IT2a-n.txt", file=sys.stderr)
        return 2

    zl = Path(sys.argv[1]).resolve()
    it = Path(sys.argv[2]).resolve()
    if e.git_blob_sha1(zl.read_bytes()) != ZL_BLOB_SHA1:
        raise RuntimeError("ZL3b Git blob SHA mismatch")
    if hashlib.sha256(it.read_bytes()).hexdigest() != IT_SHA256:
        raise RuntimeError("IT2a SHA-256 mismatch")

    here = Path(__file__).resolve().parent
    parser = e.SlotParser()
    validation = e.validate_parser(parser)

    # Discovery: use only ZL, on the exact admitted-leaf population clarified
    # in POPULATION_AMENDMENT_E4A.md.
    zl_items = e.parse_voynich(zl)
    zl_folds = e.physical_leaf_folds(zl_items)
    zl_universe = set().union(*zl_folds)
    zl_km, zl_types = fit_types(zl_items, zl_universe, parser)
    C_ZL, zl_visible, zl_parsed = e.count_matrix(zl_items, zl_universe, parser, "max", zl_km)
    T, learn_audit = learn_nonmusic_topology(C_ZL)

    # Frozen comparator in the same raw-state coordinates.
    G = raw_guidonian()
    e3_alts = load_e3_alternatives(here)
    diag = topology_diagnostics(T, G, e3_alts)

    # Prospective IT evaluation.  Reproduce E3/E2-C first, then compare T.
    it_items = e.parse_voynich(it)
    universe = set().union(*FOLDS)
    folds = []
    ga = []
    ma = []
    cover = []
    for f, held in enumerate(FOLDS):
        train = universe - held
        km, ntypes = fit_types(it_items, train, parser)
        C, tvis, tpar = e.count_matrix(it_items, train, parser, "max", km)
        H, hvis, hpar = e.count_matrix(it_items, held, parser, "max", km)

        gm = fit_raw(C, G)
        mm = fit_raw(C, T)
        gs = score_raw(H, hpar, gm, G)
        ms = score_raw(H, hpar, mm, T)
        coverage = hpar / hvis if hvis else 0.0
        ga.append(gs["accuracy"]); ma.append(ms["accuracy"]); cover.append(coverage)
        folds.append({
            "fold": f,
            "held_leaves": sorted(held),
            "training_unique_parsed_types": ntypes,
            "training_visible_occurrences": int(tvis),
            "training_parsed_occurrences": int(tpar),
            "heldout_visible_occurrences": int(hvis),
            "heldout_parsed_occurrences": int(hpar),
            "parse_coverage": coverage,
            "guidonian_accuracy": gs["accuracy"],
            "nonmusic_accuracy": ms["accuracy"],
            "guidonian_minus_nonmusic": gs["accuracy"] - ms["accuracy"],
            "guidonian_training_allowed": gm["training_allowed"],
            "nonmusic_training_allowed": mm["training_allowed"],
        })

    mean_g = statistics.mean(ga)
    mean_m = statistics.mean(ma)
    mean_cov = statistics.mean(cover)
    if abs(mean_g - E2C_MEAN_A) > EPS:
        raise RuntimeError(f"E2-C mean replay mismatch {mean_g} != {E2C_MEAN_A}")
    if abs(mean_cov - E2C_COVERAGE) > EPS:
        raise RuntimeError(f"E2-C coverage replay mismatch {mean_cov} != {E2C_COVERAGE}")
    if any(abs(a - b) > EPS for a, b in zip(ga, E2C_FOLD_A)):
        raise RuntimeError(f"E2-C fold replay mismatch {ga}")

    m_ge_g = sum(m >= g - EPS for g, m in zip(ga, ma))
    g_gt_m = sum(g > m + EPS for g, m in zip(ga, ma))
    nonmusic_pass = mean_m >= mean_g - EPS and m_ge_g >= 3
    near_match = mean_m >= mean_g - 0.005
    verdict = (
        "NON-MUSICAL SLOT TOPOLOGY MATCHES/BEATS GUIDONIAN"
        if nonmusic_pass
        else "GUIDONIAN PAIR GEOMETRY RETAINS ADVANTAGE AGAINST E4 GENERIC MODEL"
    )

    out = {
        "experiment": "Issue26E4 non-musical slot-mechanism audit",
        "issue": 26,
        "inputs": {
            "zl_blob_sha1": ZL_BLOB_SHA1,
            "it_sha256": IT_SHA256,
            "plan_sha256": sha256_file(here / "PLAN_E4.md"),
            "population_amendment_sha256": sha256_file(here / "POPULATION_AMENDMENT_E4A.md"),
            "core_sha256": sha256_file(here / "issue26e_core.py"),
            "e3_exact_catalog_sha256": EXACT_SHA256,
            "script_sha256": sha256_file(Path(__file__)),
            "parser_policy": "max",
            "fixed_state_to_vox": list(FIXED_MAP),
        },
        "slot_parser_validation": validation,
        "zl_discovery": {
            "admitted_leaf_count": len(zl_universe),
            "admitted_leaves": sorted(zl_universe),
            "unique_parsed_types": zl_types,
            "visible_occurrences": int(zl_visible),
            "parsed_occurrences": int(zl_parsed),
            "parse_coverage": zl_parsed / zl_visible if zl_visible else 0.0,
            "cluster_by_raw_state_counts": C_ZL.astype(int).tolist(),
            "learner_audit": learn_audit,
        },
        "topology_diagnostics": diag,
        "e2c_replay": {
            "mean_parse_coverage": mean_cov,
            "mean_guidonian_accuracy": mean_g,
            "fold_accuracies": ga,
        },
        "folds": folds,
        "primary": {
            "mean_guidonian_accuracy": mean_g,
            "mean_nonmusic_accuracy": mean_m,
            "guidonian_minus_nonmusic_mean": mean_g - mean_m,
            "nonmusic_ge_guidonian_folds": m_ge_g,
            "guidonian_gt_nonmusic_folds": g_gt_m,
            "near_match_within_0_005": near_match,
        },
        "frozen_classification": verdict,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
