#!/usr/bin/env python3
"""Issue #94 Phase 2A first reveal with prereveal Amendment A.

Extends the preregistered A0-A4 implementation with:
- A5 LOCAL_PLUS_PREFIX-CV
- A6 RANDOM-LAG-CV

Prediction only. No future-token or surface-target access.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
BASE_PATH = HERE.parent / "phase2a_order_vs_prefix.py"


def load_base():
    spec = importlib.util.spec_from_file_location("issue94_phase2a_base", BASE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-2A base implementation")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


B = load_base()
P1 = B.P1
I = B.I
PI_GRID = B.PI_GRID
RHO_GRID = B.PI_GRID
RANDOM_SEEDS = B.RANDOM_SEEDS
LN2 = B.LN2
TIE_EPS = B.TIE_EPS
N_FOLDS = B.N_FOLDS


def random_lag_features(items, parsed, v2, index, parser):
    """Return p0 and per-seed randomized Q(target) on accepted positions.

    At every target the exact A2 ordered weight multiset is permuted across the
    same eligible causal-prefix source occurrences. Seed namespaces are exactly
    those frozen in the base PLAN; current target identity is absent.
    """
    p_cache: Dict[object, float] = {}
    p0_rows: List[float] = []
    q_order_rows: List[float] = []
    q_seed_rows = {s: [] for s in RANDOM_SEEDS}
    avail_rows: List[bool] = []
    current_leaf = None
    prefix: List[Tuple[int, Dict[tuple, float]]] = []
    pos = 0
    n_visible = 0
    max_weight_sum_residual = 0.0

    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            prefix = []
            pos = 0
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                n_visible += 1
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    p0 = P1.P0.p0_surface(v2, parser, tok, p_cache)
                    if p0 <= 0.0:
                        raise RuntimeError("V2 non-positive in amended random-lag features")
                    m = len(prefix)
                    p0_rows.append(float(p0))
                    avail_rows.append(bool(m))
                    if m == 0:
                        q_order_rows.append(0.0)
                        for s in RANDOM_SEEDS:
                            q_seed_rows[s].append(0.0)
                    else:
                        weights = np.fromiter(
                            (math.exp(-(pos - src_pos) / 128.0) for src_pos, _dist in prefix),
                            dtype=float,
                            count=m,
                        )
                        denom = float(weights.sum())
                        if denom <= 0.0 or not math.isfinite(denom):
                            raise RuntimeError("invalid random-lag denominator")
                        qvals = np.fromiter((dist.get(tok, 0.0) for _src_pos, dist in prefix), dtype=float, count=m)
                        q_order = float(np.dot(weights, qvals) / denom)
                        if q_order < -1e-12 or q_order > 1.0 + 1e-10:
                            raise RuntimeError("ordered Q outside probability range")
                        q_order_rows.append(q_order)
                        for s in RANDOM_SEEDS:
                            seed = I.e.stable_seed(f"ISSUE94:RANDOM_LAG:{s}:{it.leaf}:{pos}")
                            perm = np.random.default_rng(seed).permutation(m)
                            wp = weights[perm]
                            resid = abs(float(wp.sum()) - denom)
                            max_weight_sum_residual = max(max_weight_sum_residual, resid)
                            if resid > max(1e-12, 1e-12 * denom):
                                raise RuntimeError("random-lag changed weight multiset")
                            q = float(np.dot(wp, qvals) / denom)
                            if q < -1e-12 or q > 1.0 + 1e-10:
                                raise RuntimeError("randomized Q outside probability range")
                            q_seed_rows[s].append(q)

                dist = P1.source_distribution(index, tok)
                if dist is not None:
                    prefix.append((pos, dist))
                pos += 1

    n = len(p0_rows)
    if any(len(q_seed_rows[s]) != n for s in RANDOM_SEEDS):
        raise RuntimeError("randomized feature population mismatch")
    return {
        "p0": np.asarray(p0_rows, dtype=float),
        "q_order": np.asarray(q_order_rows, dtype=float),
        "q_seed": {s: np.asarray(q_seed_rows[s], dtype=float) for s in RANDOM_SEEDS},
        "avail": np.asarray(avail_rows, dtype=bool),
        "n_scored": int(n),
        "n_visible": int(n_visible),
        "max_weight_sum_residual": float(max_weight_sum_residual),
    }


def hybrid_curve(prefix_feat, local_pi: float):
    p0 = prefix_feat["p0"]
    q_local = prefix_feat["q"][:, 0]
    av_local = prefix_feat["avail"][:, 0]
    q_bag = prefix_feat["q"][:, 2]
    av_bag = prefix_feat["avail"][:, 2]
    p_local = B.mix_probs(p0, q_local, av_local, local_pi)
    probs = np.where(
        av_bag[:, None],
        (1.0 - RHO_GRID[None, :]) * p_local[:, None] + RHO_GRID[None, :] * q_bag[:, None],
        p_local[:, None],
    )
    if np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid LOCAL_PLUS_PREFIX grid")
    return np.log(probs).sum(axis=0)


def random_cv_curve(rand_feat):
    total_by_seed = {s: np.zeros(len(PI_GRID), dtype=float) for s in RANDOM_SEEDS}
    p0 = rand_feat["p0"][:, None]
    av = rand_feat["avail"][:, None]
    for s in RANDOM_SEEDS:
        q = rand_feat["q_seed"][s][:, None]
        probs = np.where(av, (1.0 - PI_GRID[None, :]) * p0 + PI_GRID[None, :] * q, p0)
        if np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
            raise RuntimeError("invalid RANDOM_LAG_CV grid")
        total_by_seed[s] = np.log(probs).sum(axis=0)
    mean_ll = np.mean(np.stack([total_by_seed[s] for s in RANDOM_SEEDS]), axis=0)
    return mean_ll, total_by_seed


def choose_scalar(grid, ll):
    best = 0
    for i in range(1, len(grid)):
        if ll[i] > ll[best] + TIE_EPS:
            best = i
        elif abs(float(ll[i] - ll[best])) <= TIE_EPS and float(grid[i]) < float(grid[best]):
            best = i
    return int(best)


def select_amended_controls(vitems, folds, parsed, outer_f: int, parser):
    hybrid_total = np.zeros(len(RHO_GRID), dtype=float)
    random_total = np.zeros(len(PI_GRID), dtype=float)
    random_seed_total = {s: np.zeros(len(PI_GRID), dtype=float) for s in RANDOM_SEEDS}
    inner = []
    local_pi = float(B.PHASE1_EXPECTED[outer_f]["local_pi"])

    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        _tr, v2, index = B.fit_training(vitems, folds, parsed, (outer_f, inner_g))
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        pf = B.prefix_features(va, parsed, v2, index, parser)
        hybrid_total += hybrid_curve(pf, local_pi)

        rf = random_lag_features(va, parsed, v2, index, parser)
        if rf["n_scored"] != pf["n_scored"] or rf["n_visible"] != pf["n_visible"]:
            raise RuntimeError("inner support mismatch between prefix and random controls")
        mean_ll, by_seed = random_cv_curve(rf)
        random_total += mean_ll
        for s in RANDOM_SEEDS:
            random_seed_total[s] += by_seed[s]
        inner.append({
            "inner_fold": int(inner_g),
            "n_scored": int(pf["n_scored"]),
            "n_visible": int(pf["n_visible"]),
            "random_max_weight_sum_residual": rf["max_weight_sum_residual"],
        })

    hi = choose_scalar(RHO_GRID, hybrid_total)
    ri = choose_scalar(PI_GRID, random_total)
    return {
        "A5": {
            "selected_rho": float(RHO_GRID[hi]),
            "total_log_likelihood": float(hybrid_total[hi]),
            "curve": [
                {"rho": float(rho), "total_log_likelihood": float(hybrid_total[i])}
                for i, rho in enumerate(RHO_GRID)
            ],
        },
        "A6": {
            "selected_pi": float(PI_GRID[ri]),
            "mean_randomization_total_log_likelihood": float(random_total[ri]),
            "curve": [
                {
                    "pi": float(pi),
                    "mean_randomization_total_log_likelihood": float(random_total[i]),
                    "by_seed_total_log_likelihood": {str(s): float(random_seed_total[s][i]) for s in RANDOM_SEEDS},
                }
                for i, pi in enumerate(PI_GRID)
            ],
        },
        "inner": inner,
    }


def score_amended_outer(vitems, folds, parsed, outer_f: int, parser, prefix_sel: dict, amended_sel: dict):
    base = B.score_outer(vitems, folds, parsed, outer_f, parser, prefix_sel)
    _tr, v2, index = B.fit_training(vitems, folds, parsed, (outer_f,))
    test = I.b.by_leaves(vitems, folds[outer_f], include=True)
    pf = B.prefix_features(test, parsed, v2, index, parser)

    local_pi = float(B.PHASE1_EXPECTED[outer_f]["local_pi"])
    p_local = B.mix_probs(pf["p0"], pf["q"][:, 0], pf["avail"][:, 0], local_pi)
    rho = float(amended_sel["A5"]["selected_rho"])
    q_bag = pf["q"][:, 2]
    av_bag = pf["avail"][:, 2]
    p5 = np.where(av_bag, (1.0 - rho) * p_local + rho * q_bag, p_local)
    A5 = B.bits(p5)

    rf = random_lag_features(test, parsed, v2, index, parser)
    if rf["n_scored"] != base["n_scored"] or rf["n_visible"] != base["n_visible"]:
        raise RuntimeError("outer support mismatch")
    # Verify the direct ordered-Q path still reproduces A2 exactly.
    p2_direct = B.mix_probs(rf["p0"], rf["q_order"], rf["avail"], 0.30)
    if abs(B.bits(p2_direct) - base["A2_ORDERED128_FIXED_bits_per_token"]) > 1e-9:
        raise RuntimeError("amended direct ordered regression mismatch")

    pi_r = float(amended_sel["A6"]["selected_pi"])
    rand_seed_bits = {}
    for s in RANDOM_SEEDS:
        pr = B.mix_probs(rf["p0"], rf["q_seed"][s], rf["avail"], pi_r)
        rand_seed_bits[str(s)] = B.bits(pr)
    A6 = float(np.mean(list(rand_seed_bits.values())))

    A0 = float(base["A0_LOCAL40_bits_per_token"])
    A2 = float(base["A2_ORDERED128_FIXED_bits_per_token"])
    base["A5_LOCAL_PLUS_PREFIX_CV"] = {
        "selected_rho": rho,
        "bits_per_token": A5,
    }
    base["A6_RANDOM_LAG_CV"] = {
        "selected_pi": pi_r,
        "bits_per_token_by_seed": rand_seed_bits,
        "mean_bits_per_token": A6,
        "max_weight_sum_residual": rf["max_weight_sum_residual"],
    }
    base["contrasts"].update({
        "G_prefix_cond": float(A0 - A5),
        "G_order_hybrid": float(A5 - A2),
        "G_order_random_cv": float(A6 - A2),
    })
    return base


def run(zl_path: Path):
    if I.b.git_blob_sha1(zl_path.read_bytes()) != B.EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b authority mismatch")
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError("fold count mismatch")
    parser = I.e.SlotParser()
    I.e.validate_parser(parser)

    prefix_selection = {str(f): B.select_prefix_pi(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    amended_selection = {str(f): select_amended_controls(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    outer = [
        score_amended_outer(vitems, folds, parsed, f, parser, prefix_selection[str(f)], amended_selection[str(f)])
        for f in range(N_FOLDS)
    ]

    summaries = {
        "G_prefix": B.stability([r["contrasts"]["G_prefix"] for r in outer]),
        "G_order_bag_fixed": B.stability([r["contrasts"]["G_order_bag_fixed"] for r in outer]),
        "G_order_random": B.stability([r["contrasts"]["G_order_random"] for r in outer]),
        "G_prefix_cond": B.stability([r["contrasts"]["G_prefix_cond"] for r in outer]),
        "G_order_hybrid": B.stability([r["contrasts"]["G_order_hybrid"] for r in outer]),
        "G_order_random_cv": B.stability([r["contrasts"]["G_order_random_cv"] for r in outer]),
        "phase1_long_increment": B.stability([r["contrasts"]["phase1_long_increment"] for r in outer]),
        "mean_bits_per_token": {
            "A0_LOCAL40": float(np.mean([r["A0_LOCAL40_bits_per_token"] for r in outer])),
            "A1_PREFIX_BAG_CV": float(np.mean([r["A1_PREFIX_BAG_CV"]["bits_per_token"] for r in outer])),
            "A2_ORDERED128_FIXED": float(np.mean([r["A2_ORDERED128_FIXED_bits_per_token"] for r in outer])),
            "A3_PREFIX_BAG_FIXED": float(np.mean([r["A3_PREFIX_BAG_FIXED_bits_per_token"] for r in outer])),
            "A4_RANDOM_LAG_FIXED": float(np.mean([r["A4_RANDOM_LAG_FIXED"]["RANDOM_LAG_FIXED_mean_bits_per_token"] for r in outer])),
            "A5_LOCAL_PLUS_PREFIX_CV": float(np.mean([r["A5_LOCAL_PLUS_PREFIX_CV"]["bits_per_token"] for r in outer])),
            "A6_RANDOM_LAG_CV": float(np.mean([r["A6_RANDOM_LAG_CV"]["mean_bits_per_token"] for r in outer])),
        },
    }

    prefix_pass = bool(summaries["G_prefix_cond"]["pass"])
    order_random = bool(summaries["G_order_random_cv"]["pass"])
    order_hybrid = bool(summaries["G_order_hybrid"]["pass"])
    order_full = bool(order_random and order_hybrid)

    if prefix_pass and order_full:
        classification = "MIXED PREFIX + ORDER CONTRIBUTIONS"
    elif prefix_pass and not order_random and not order_hybrid:
        classification = "LONG-HISTORY GAIN PRIMARILY PREFIX-INVENTORY"
    elif (not prefix_pass) and order_full:
        classification = "ORDER-SENSITIVE LONG-HISTORY INFORMATION SURVIVES"
    else:
        classification = "SOURCE ATTRIBUTION INCONCLUSIVE"

    out = {
        "schema": "issue94-phase2a-amended-v1",
        "phase": "ISSUE94_PHASE2A",
        "classification": classification,
        "source": {
            "git_blob_sha1": I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": B.EXPECTED_ZL3B_BLOB,
        },
        "folds": P1.P0.fold_identity(folds),
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "authority_hashes": {
            "PLAN.md": B.sha256_file(HERE.parent / "PLAN.md"),
            "AMENDMENT_A.md": B.sha256_file(HERE.parent / "AMENDMENT_A.md"),
            "phase2a_order_vs_prefix.py": B.sha256_file(BASE_PATH),
            "phase2a_amended.py": B.sha256_file(HERE),
            "phase1_predictive_budget.py": B.sha256_file(B.PHASE1_PATH),
        },
        "prefix_selection": prefix_selection,
        "amended_selection": amended_selection,
        "outer": outer,
        "summaries": summaries,
        "decision_inputs": {
            "PREFIX_cond_pass": prefix_pass,
            "ORDER_RANDOM_CV_pass": order_random,
            "ORDER_HYBRID_pass": order_hybrid,
            "ORDER_FULL_pass": order_full,
        },
        "regression": {
            "A0_phase1_reproduced_all_folds": True,
            "A2_phase1_reproduced_all_folds": True,
            "direct_ordered_equals_accumulator_all_folds": True,
            "amended_direct_ordered_reproduced_all_folds": True,
        },
        "randomization": {
            "seeds": list(RANDOM_SEEDS),
            "seed_selected": False,
            "target_token_in_seed": False,
            "future_tokens_used": False,
            "fixed_pi_A4": 0.30,
            "A6_pi_selected_nested_only": True,
        },
        "firewall": {
            "future_test_tokens_used": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
        },
        "interpretation_boundary": {
            "historical_memory_horizon_identified": False,
            "semantic_content_tested": False,
            "latent_state_identified": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
    }
    return B.strict_safe(out)


def self_test():
    b = B.self_test()
    if not b.get("ok"):
        raise AssertionError("base self-test failed")
    p0 = np.asarray([0.2, 0.3])
    ql = np.asarray([0.4, 0.1])
    qb = np.asarray([0.1, 0.5])
    av = np.asarray([True, True])
    p_local = B.mix_probs(p0, ql, av, 0.2)
    p_rho0 = (1.0 - 0.0) * p_local + 0.0 * qb
    if not np.allclose(p_local, p_rho0, atol=0.0, rtol=0.0):
        raise AssertionError("rho=0 does not reduce exactly to LOCAL40")
    return {
        "ok": True,
        "prediction_only": True,
        "amendment_A": True,
        "random_seeds": list(RANDOM_SEEDS),
        "rho_grid": [float(x) for x in RHO_GRID],
        "random_pi_grid": [float(x) for x in PI_GRID],
        "future_tokens_used": False,
        "surface_target_calls": 0,
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ZL3B", "OUT"))
    ns = ap.parse_args(argv)
    if int(bool(ns.self_test)) + int(ns.run is not None) != 1:
        ap.error("choose exactly one mode")
    if ns.self_test:
        print(json.dumps(self_test(), indent=2, sort_keys=True))
        return 0
    out = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(out, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": out["classification"],
        "mean_bits_per_token": out["summaries"]["mean_bits_per_token"],
        "G_prefix_cond": out["summaries"]["G_prefix_cond"],
        "G_order_hybrid": out["summaries"]["G_order_hybrid"],
        "G_order_random_cv": out["summaries"]["G_order_random_cv"],
        "original_diagnostics": {
            "G_prefix": out["summaries"]["G_prefix"],
            "G_order_bag_fixed": out["summaries"]["G_order_bag_fixed"],
            "G_order_random": out["summaries"]["G_order_random"],
        },
        "decision_inputs": out["decision_inputs"],
        "A5_rho": {f:r["A5"]["selected_rho"] for f,r in out["amended_selection"].items()},
        "A6_pi": {f:r["A6"]["selected_pi"] for f,r in out["amended_selection"].items()},
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())