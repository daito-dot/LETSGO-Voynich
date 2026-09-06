#!/usr/bin/env python3
"""Issue #94 / Issue #88 Phase 2A source attribution.

Prediction-only matched interventions:
- LOCAL40 regression anchor
- PREFIX-BAG-CV causal prefix inventory
- ORDERED128-FIXED Phase-1 long-history reference
- PREFIX-BAG-FIXED matched uniform-weight intervention
- RANDOM-LAG-FIXED matched recency-weight reassignment controls

No future-token access and no surface-target scorer.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np

HERE = Path(__file__).resolve()
ROOT = HERE.parents[3]
PHASE1_PATH = ROOT / "experiments" / "predictive-information" / "phase1" / "phase1_predictive_budget.py"
EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
N_FOLDS = 5
LN2 = math.log(2.0)
PI_GRID = np.asarray([round(i / 100.0, 2) for i in range(31)], dtype=float)
RANDOM_SEEDS = (0, 1, 2, 3, 4)
TIE_EPS = 1e-12

PHASE1_EXPECTED = {
    0: {"A0": 9.74553213453277, "A2": 9.704993852780854, "local_pi": 0.21},
    1: {"A0": 9.654379389512654, "A2": 9.612149532173033, "local_pi": 0.21},
    2: {"A0": 9.44552408749662, "A2": 9.387814289841517, "local_pi": 0.20},
    3: {"A0": 9.478509701296273, "A2": 9.417253956137694, "local_pi": 0.21},
    4: {"A0": 9.656960288057821, "A2": 9.624058563568518, "local_pi": 0.21},
}


def load_phase1():
    spec = importlib.util.spec_from_file_location("issue92_phase1_authority", PHASE1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-1 authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


P1 = load_phase1()
I = P1.I


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(probs: np.ndarray) -> float:
    if len(probs) == 0 or np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid probability vector")
    return float(-np.log(probs).mean() / LN2)


def mix_probs(p0, q, avail, pi: float):
    out = np.where(avail, (1.0 - pi) * p0 + pi * q, p0)
    if np.any(out <= 0.0) or not np.all(np.isfinite(out)):
        raise RuntimeError("invalid mixture probability")
    return out


def fit_training(vitems, folds, parsed, excluded_folds: Sequence[int]):
    return P1.fit_training(vitems, folds, parsed, excluded_folds)


def prefix_features(items, parsed, v2, index, parser):
    candidates = [
        {"H": 40, "tau": 32.0},
        {"H": "ALL", "tau": 128.0},
        {"H": "ALL", "tau": math.inf},
    ]
    return P1.recency_feature_matrix(items, parsed, v2, index, parser, candidates=candidates)


def prefix_pi_curve(features, q_col=2):
    p0 = features["p0"][:, None]
    q = features["q"][:, q_col][:, None]
    av = features["avail"][:, q_col][:, None]
    pi = PI_GRID[None, :]
    probs = np.where(av, (1.0 - pi) * p0 + pi * q, p0)
    if np.any(probs <= 0.0):
        raise RuntimeError("non-positive prefix-CV probability")
    return np.log(probs).sum(axis=0)


def select_prefix_pi(vitems, folds, parsed, outer_f: int, parser):
    total = np.zeros(len(PI_GRID), dtype=float)
    inner = []
    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        _tr, v2, index = fit_training(vitems, folds, parsed, (outer_f, inner_g))
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        feat = prefix_features(va, parsed, v2, index, parser)
        total += prefix_pi_curve(feat)
        inner.append({"inner_fold": int(inner_g), "n_scored": int(feat["n_scored"]), "n_visible": int(feat["n_visible"])})
    best_i = 0
    for i in range(1, len(PI_GRID)):
        if total[i] > total[best_i] + TIE_EPS:
            best_i = i
        elif abs(total[i] - total[best_i]) <= TIE_EPS and PI_GRID[i] < PI_GRID[best_i]:
            best_i = i
    return {
        "selected_pi": float(PI_GRID[best_i]),
        "total_log_likelihood": float(total[best_i]),
        "curve": [{"pi": float(pi), "total_log_likelihood": float(total[i])} for i, pi in enumerate(PI_GRID)],
        "inner": inner,
    }


def eligible_history_random_scores(items, parsed, v2, index, parser, fold: int):
    """Score ORDERED128-FIXED and five matched RANDOM-LAG controls directly.

    Each RANDOM-LAG target position retains the exact eligible prefix source
    occurrences, their normalized neighbour distributions, and the ordered
    exp(-lag/128) weight multiset. Only the assignment of weights to source
    occurrences is permuted using a target-token-independent stable seed.
    """
    p_cache: Dict[object, float] = {}
    ordered_log = []
    random_log = {s: [] for s in RANDOM_SEEDS}
    neff = []
    eligible_counts = []
    context_n = 0
    visible_n = 0
    scored_n = 0
    max_q = 0.0
    current_leaf = None
    prefix: List[Tuple[int, Dict[tuple, float]]] = []
    pos = 0

    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            prefix = []
            pos = 0
        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                visible_n += 1
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    p0 = P1.P0.p0_surface(v2, parser, tok, p_cache)
                    if p0 <= 0.0:
                        raise RuntimeError("V2 non-positive in random-lag scorer")
                    scored_n += 1
                    m = len(prefix)
                    eligible_counts.append(m)
                    if m == 0:
                        ordered_log.append(math.log(p0))
                        for s in RANDOM_SEEDS:
                            random_log[s].append(math.log(p0))
                    else:
                        context_n += 1
                        weights = np.fromiter(
                            (math.exp(-(pos - src_pos) / 128.0) for src_pos, _dist in prefix),
                            dtype=float,
                            count=m,
                        )
                        denom = float(weights.sum())
                        if denom <= 0.0 or not math.isfinite(denom):
                            raise RuntimeError("invalid ordered recency denominator")
                        qvals = np.fromiter((dist.get(tok, 0.0) for _src_pos, dist in prefix), dtype=float, count=m)
                        q_ordered = float(np.dot(weights, qvals) / denom)
                        max_q = max(max_q, q_ordered)
                        if q_ordered < -1e-12 or q_ordered > 1.0 + 1e-10:
                            raise RuntimeError("ordered Q outside probability range")
                        p_ord = 0.70 * p0 + 0.30 * q_ordered
                        ordered_log.append(math.log(p_ord))
                        sw2 = float(np.dot(weights, weights))
                        neff.append(float(denom * denom / sw2))

                        # Stable target-position randomization; target token identity is absent from namespace.
                        for s in RANDOM_SEEDS:
                            seed = I.e.stable_seed(f"ISSUE94:RANDOM_LAG:{s}:{it.leaf}:{pos}")
                            perm = np.random.default_rng(seed).permutation(m)
                            wp = weights[perm]
                            # exact same multiset; numerical check is diagnostic/hard gate
                            if abs(float(wp.sum()) - denom) > max(1e-12, 1e-12 * denom):
                                raise RuntimeError("random-lag weight multiset sum changed")
                            q_rand = float(np.dot(wp, qvals) / denom)
                            max_q = max(max_q, q_rand)
                            if q_rand < -1e-12 or q_rand > 1.0 + 1e-10:
                                raise RuntimeError("random Q outside probability range")
                            p_rand = 0.70 * p0 + 0.30 * q_rand
                            random_log[s].append(math.log(p_rand))

                dist = P1.source_distribution(index, tok)
                if dist is not None:
                    prefix.append((pos, dist))
                pos += 1

    n = len(ordered_log)
    if n != scored_n or any(len(random_log[s]) != n for s in RANDOM_SEEDS):
        raise RuntimeError("random-lag scored-population mismatch")
    ord_bits = float(-np.mean(ordered_log) / LN2)
    rand_bits = {str(s): float(-np.mean(random_log[s]) / LN2) for s in RANDOM_SEEDS}
    return {
        "fold": int(fold),
        "ORDERED128_FIXED_bits_per_token": ord_bits,
        "RANDOM_LAG_FIXED_bits_per_token_by_seed": rand_bits,
        "RANDOM_LAG_FIXED_mean_bits_per_token": float(np.mean(list(rand_bits.values()))),
        "n_scored": int(scored_n),
        "n_visible": int(visible_n),
        "context_tokens": int(context_n),
        "context_fraction": float(context_n / scored_n) if scored_n else 0.0,
        "eligible_source_count": {
            "mean": float(np.mean(eligible_counts)) if eligible_counts else 0.0,
            "median": float(np.median(eligible_counts)) if eligible_counts else 0.0,
            "max": int(max(eligible_counts)) if eligible_counts else 0,
        },
        "ordered_effective_source_count": {
            "mean": float(np.mean(neff)) if neff else 0.0,
            "median": float(np.median(neff)) if neff else 0.0,
            "min": float(min(neff)) if neff else 0.0,
            "max": float(max(neff)) if neff else 0.0,
        },
        "max_observed_Q_target": float(max_q),
        "randomization": {
            "seeds": list(RANDOM_SEEDS),
            "target_token_in_seed": False,
            "future_tokens_used": False,
            "weight_multiset_preserved": True,
        },
    }


def stability(values):
    vals = [float(v) for v in values]
    return {
        "values": vals,
        "mean": float(np.mean(vals)),
        "positive_folds": int(sum(v > 0.0 for v in vals)),
        "pass": bool(float(np.mean(vals)) > 0.0 and sum(v > 0.0 for v in vals) >= 4),
    }


def score_outer(vitems, folds, parsed, outer_f: int, parser, prefix_selection: dict):
    _tr, v2, index = fit_training(vitems, folds, parsed, (outer_f,))
    test = I.b.by_leaves(vitems, folds[outer_f], include=True)
    feat = prefix_features(test, parsed, v2, index, parser)
    p0 = feat["p0"]
    q_local = feat["q"][:, 0]
    av_local = feat["avail"][:, 0]
    q_order = feat["q"][:, 1]
    av_order = feat["avail"][:, 1]
    q_bag = feat["q"][:, 2]
    av_bag = feat["avail"][:, 2]

    ex = PHASE1_EXPECTED[outer_f]
    A0 = bits(P1.mix_probs(p0, q_local, av_local, ex["local_pi"]))
    A1_pi = float(prefix_selection["selected_pi"])
    A1 = bits(P1.mix_probs(p0, q_bag, av_bag, A1_pi))
    A2 = bits(P1.mix_probs(p0, q_order, av_order, 0.30))
    A3 = bits(P1.mix_probs(p0, q_bag, av_bag, 0.30))

    if abs(A0 - ex["A0"]) > 1e-9:
        raise RuntimeError(f"fold{outer_f} A0 Phase-1 regression mismatch: {A0} != {ex['A0']}")
    if abs(A2 - ex["A2"]) > 1e-9:
        raise RuntimeError(f"fold{outer_f} A2 Phase-1 regression mismatch: {A2} != {ex['A2']}")

    random = eligible_history_random_scores(test, parsed, v2, index, parser, outer_f)
    if abs(random["ORDERED128_FIXED_bits_per_token"] - A2) > 1e-9:
        raise RuntimeError(f"fold{outer_f} direct ordered regression mismatch")

    return {
        "fold": int(outer_f),
        "n_scored": int(feat["n_scored"]),
        "n_visible": int(feat["n_visible"]),
        "A0_LOCAL40_bits_per_token": A0,
        "A1_PREFIX_BAG_CV": {
            "selected_pi": A1_pi,
            "bits_per_token": A1,
        },
        "A2_ORDERED128_FIXED_bits_per_token": A2,
        "A3_PREFIX_BAG_FIXED_bits_per_token": A3,
        "A4_RANDOM_LAG_FIXED": random,
        "contrasts": {
            "G_prefix": float(A0 - A1),
            "G_order_bag_fixed": float(A3 - A2),
            "G_order_random": float(random["RANDOM_LAG_FIXED_mean_bits_per_token"] - A2),
            "phase1_long_increment": float(A0 - A2),
            "share_prefix": float((A0 - A1) / (A0 - A2)) if abs(A0 - A2) > 1e-15 else None,
        },
    }


def strict_safe(obj):
    if isinstance(obj, dict):
        return {k: strict_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [strict_safe(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return "INF" if obj > 0 else "-INF"
    return obj


def run(zl_path: Path):
    if I.b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b authority mismatch")
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError("fold count mismatch")
    parser = I.e.SlotParser()
    I.e.validate_parser(parser)

    selections = {str(f): select_prefix_pi(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    outer = [score_outer(vitems, folds, parsed, f, parser, selections[str(f)]) for f in range(N_FOLDS)]

    g_prefix = stability([r["contrasts"]["G_prefix"] for r in outer])
    g_bag = stability([r["contrasts"]["G_order_bag_fixed"] for r in outer])
    g_rand = stability([r["contrasts"]["G_order_random"] for r in outer])
    prefix = bool(g_prefix["pass"])
    order_bag = bool(g_bag["pass"])
    order_rand = bool(g_rand["pass"])

    if prefix and order_bag and order_rand:
        classification = "MIXED PREFIX + ORDER CONTRIBUTIONS"
    elif prefix and not (order_bag and order_rand):
        classification = "LONG-HISTORY GAIN PRIMARILY PREFIX-INVENTORY"
    elif (not prefix) and order_bag and order_rand:
        classification = "ORDER-SENSITIVE LONG-HISTORY INFORMATION SURVIVES"
    else:
        classification = "SOURCE ATTRIBUTION INCONCLUSIVE"

    plan = HERE.parent / "PLAN.md"
    out = {
        "schema": "issue94-phase2a-order-vs-prefix-v1",
        "phase": "ISSUE94_PHASE2A",
        "classification": classification,
        "source": {
            "git_blob_sha1": I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": EXPECTED_ZL3B_BLOB,
        },
        "folds": P1.P0.fold_identity(folds),
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "authority_hashes": {
            "PLAN.md": sha256_file(plan),
            "phase2a_order_vs_prefix.py": sha256_file(HERE),
            "phase1_predictive_budget.py": sha256_file(PHASE1_PATH),
        },
        "frozen_random_seeds": list(RANDOM_SEEDS),
        "prefix_selection": selections,
        "outer": outer,
        "summaries": {
            "G_prefix": g_prefix,
            "G_order_bag_fixed": g_bag,
            "G_order_random": g_rand,
            "mean_bits_per_token": {
                "A0_LOCAL40": float(np.mean([r["A0_LOCAL40_bits_per_token"] for r in outer])),
                "A1_PREFIX_BAG_CV": float(np.mean([r["A1_PREFIX_BAG_CV"]["bits_per_token"] for r in outer])),
                "A2_ORDERED128_FIXED": float(np.mean([r["A2_ORDERED128_FIXED_bits_per_token"] for r in outer])),
                "A3_PREFIX_BAG_FIXED": float(np.mean([r["A3_PREFIX_BAG_FIXED_bits_per_token"] for r in outer])),
                "A4_RANDOM_LAG_FIXED": float(np.mean([r["A4_RANDOM_LAG_FIXED"]["RANDOM_LAG_FIXED_mean_bits_per_token"] for r in outer])),
            },
            "share_prefix_by_fold": [r["contrasts"]["share_prefix"] for r in outer],
            "mean_share_prefix": float(np.mean([r["contrasts"]["share_prefix"] for r in outer])),
        },
        "decision_inputs": {
            "PREFIX_pass": prefix,
            "ORDER_BAG_pass": order_bag,
            "ORDER_RANDOM_pass": order_rand,
        },
        "regression": {
            "A0_phase1_reproduced_all_folds": True,
            "A2_phase1_reproduced_all_folds": True,
            "direct_ordered_equals_accumulator_all_folds": True,
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
    return strict_safe(out)


def self_test():
    # Synthetic distributions each normalized over the same 3-token outcome support.
    dists = [
        {("a",): 0.7, ("b",): 0.3},
        {("a",): 0.2, ("c",): 0.8},
        {("b",): 0.4, ("c",): 0.6},
    ]
    weights = np.asarray([0.9, 0.5, 0.2], dtype=float)
    denom = float(weights.sum())
    support = [("a",), ("b",), ("c",)]
    q_order = {t: sum(weights[i] * dists[i].get(t, 0.0) for i in range(3)) / denom for t in support}
    if abs(sum(q_order.values()) - 1.0) > 1e-12:
        raise AssertionError("ordered synthetic Q not normalized")
    outputs = []
    for seed_id in RANDOM_SEEDS:
        seed = I.e.stable_seed(f"ISSUE94:RANDOM_LAG:{seed_id}:synthetic:3")
        perm = np.random.default_rng(seed).permutation(3)
        wp = weights[perm]
        if sorted(wp.tolist()) != sorted(weights.tolist()):
            raise AssertionError("random-lag weight multiset not preserved")
        q = {t: sum(wp[i] * dists[i].get(t, 0.0) for i in range(3)) / denom for t in support}
        if abs(sum(q.values()) - 1.0) > 1e-12:
            raise AssertionError("random synthetic Q not normalized")
        outputs.append((seed_id, perm.tolist(), q))
    # deterministic repeat
    outputs2 = []
    for seed_id in RANDOM_SEEDS:
        seed = I.e.stable_seed(f"ISSUE94:RANDOM_LAG:{seed_id}:synthetic:3")
        perm = np.random.default_rng(seed).permutation(3)
        outputs2.append((seed_id, perm.tolist()))
    if [(a,b) for a,b,_q in outputs] != outputs2:
        raise AssertionError("random-lag seed not deterministic")
    return {
        "ok": True,
        "prediction_only": True,
        "random_seeds": list(RANDOM_SEEDS),
        "random_lag_weight_multiset_preserved": True,
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
    result = run(Path(ns.run[0]))
    Path(ns.run[1]).write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "classification": result["classification"],
        "mean_bits_per_token": result["summaries"]["mean_bits_per_token"],
        "G_prefix": result["summaries"]["G_prefix"],
        "G_order_bag_fixed": result["summaries"]["G_order_bag_fixed"],
        "G_order_random": result["summaries"]["G_order_random"],
        "decision_inputs": result["decision_inputs"],
        "prefix_pi": {f:x["selected_pi"] for f,x in result["prefix_selection"].items()},
        "firewall": result["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
