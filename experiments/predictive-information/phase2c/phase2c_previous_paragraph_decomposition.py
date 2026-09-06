#!/usr/bin/env python3
"""Issue #98 Phase 2C: corrected-order previous-paragraph decomposition.

Prediction-only localization of the corrected Phase-2B PREV_PARAS signal into:
- immediate previous paragraph vs older paragraphs;
- same transcription page/panel vs cross-panel previous paragraphs;
with matched actual-lag vs randomized-lag diagnostics for each atomic pool.
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
PRED = ROOT / "experiments" / "predictive-information"
PHASE2B_PATH = PRED / "phase2b" / "phase2b_boundary_localization.py"
if str(PRED) not in sys.path:
    sys.path.insert(0, str(PRED))

import source_order_authority as OA  # noqa: E402

EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
N_FOLDS = 5
LN2 = math.log(2.0)
GRID = np.asarray([round(i / 100.0, 2) for i in range(31)], dtype=float)
TIE_EPS = 1e-12
TAU_ORDER = 128.0
RANDOM_SEEDS = (0, 1, 2, 3, 4)

ATOMIC = ("PREV1", "OLDER", "SAME_SIDE_PREV", "CROSS_SIDE_PREV")
ALL_POOL = "ALL_PREV"

CORRECTED = {
    0: {"local_pi": .21, "all_prev_alpha": .23},
    1: {"local_pi": .21, "all_prev_alpha": .24},
    2: {"local_pi": .21, "all_prev_alpha": .22},
    3: {"local_pi": .21, "all_prev_alpha": .22},
    4: {"local_pi": .22, "all_prev_alpha": .24},
}
CORRECTED_LOCAL_MEAN = 9.594367012730386
CORRECTED_ALL_PREV_MEAN = 9.54436107360304


def load_phase2b():
    spec = importlib.util.spec_from_file_location("issue98_phase2b_corrected_base", PHASE2B_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-2B authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


P2B = load_phase2b()
I = P2B.I
P1 = P2B.P1
B = P2B.B


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(probs: np.ndarray) -> float:
    if len(probs) == 0 or np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid probability vector")
    return float(-np.log(probs).mean() / LN2)


def mix(base: np.ndarray, q: np.ndarray, avail: np.ndarray, alpha: float) -> np.ndarray:
    out = np.where(avail, (1.0 - alpha) * base + alpha * q, base)
    if np.any(out <= 0.0) or not np.all(np.isfinite(out)):
        raise RuntimeError("invalid one-pool probability")
    return out


def joint_mix(base: np.ndarray, q1: np.ndarray, av1: np.ndarray, q2: np.ndarray, av2: np.ndarray, a: float, b: float) -> np.ndarray:
    q1s = np.where(av1, q1, base)
    q2s = np.where(av2, q2, base)
    out = (1.0 - a - b) * base + a * q1s + b * q2s
    if np.any(out <= 0.0) or not np.all(np.isfinite(out)):
        raise RuntimeError("invalid two-pool probability")
    return out


def choose_scalar(ll: np.ndarray) -> int:
    best = 0
    for i in range(1, len(GRID)):
        if ll[i] > ll[best] + TIE_EPS:
            best = i
        elif abs(float(ll[i] - ll[best])) <= TIE_EPS and float(GRID[i]) < float(GRID[best]):
            best = i
    return int(best)


JOINT_GRID = tuple(
    (float(a), float(b))
    for a in GRID
    for b in GRID
    if float(a + b) <= .30 + 1e-12
)


def choose_joint(ll: np.ndarray) -> int:
    best = 0
    for i in range(1, len(JOINT_GRID)):
        if ll[i] > ll[best] + TIE_EPS:
            best = i
            continue
        if abs(float(ll[i] - ll[best])) > TIE_EPS:
            continue
        a, b = JOINT_GRID[i]
        ba, bb = JOINT_GRID[best]
        key = (a + b, a, b)
        bkey = (ba + bb, ba, bb)
        if key < bkey:
            best = i
    return int(best)


def source_stats(sources: Sequence[Tuple[int, Dict[tuple, float]]], target, pos: int, pool: str, leaf) -> dict:
    m = len(sources)
    if not m:
        return {
            "n": 0,
            "q_bag": 0.0,
            "q_order": 0.0,
            "q_random": {s: 0.0 for s in RANDOM_SEEDS},
            "max_weight_sum_residual": 0.0,
        }
    qvals = np.fromiter((dist.get(target, 0.0) for _p, dist in sources), dtype=float, count=m)
    weights = np.fromiter((math.exp(-(pos - src_pos) / TAU_ORDER) for src_pos, _dist in sources), dtype=float, count=m)
    den = float(weights.sum())
    if den <= 0.0 or not math.isfinite(den):
        raise RuntimeError("invalid ordered denominator")
    qbag = float(qvals.mean())
    qorder = float(np.dot(weights, qvals) / den)
    qr = {}
    max_resid = 0.0
    for s in RANDOM_SEEDS:
        seed = I.e.stable_seed(f"ISSUE98:PHASE2C:{pool}:RANDOM_LAG:{s}:{leaf}:{pos}")
        perm = np.random.default_rng(seed).permutation(m)
        wp = weights[perm]
        resid = abs(float(wp.sum()) - den)
        max_resid = max(max_resid, resid)
        if resid > max(1e-12, 1e-12 * den):
            raise RuntimeError("random-lag changed weight multiset")
        qr[s] = float(np.dot(wp, qvals) / den)
    for q in [qbag, qorder, *qr.values()]:
        if q < -1e-12 or q > 1.0 + 1e-10 or not math.isfinite(q):
            raise RuntimeError("pool Q outside probability range")
    return {
        "n": int(m),
        "q_bag": qbag,
        "q_order": qorder,
        "q_random": qr,
        "max_weight_sum_residual": float(max_resid),
    }


def flatten(records: Sequence[dict]) -> List[Tuple[int, Dict[tuple, float]]]:
    return [src for rec in records for src in rec["sources"]]


def features(items, parsed, v2, index, parser):
    local = P1.RecencyAccumulator(40, 32.0)
    p_cache: Dict[object, float] = {}
    p0_rows: List[float] = []
    qlocal_rows: List[float] = []
    avlocal_rows: List[bool] = []
    qbag = {p: [] for p in (*ATOMIC, ALL_POOL)}
    qorder = {p: [] for p in ATOMIC}
    qrandom = {p: {s: [] for s in RANDOM_SEEDS} for p in ATOMIC}
    avail = {p: [] for p in (*ATOMIC, ALL_POOL)}
    current_leaf = None
    previous_paragraphs: List[dict] = []
    pos = 0
    n_visible = 0
    max_random_resid = 0.0

    for it in OA.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            previous_paragraphs = []
            pos = 0
            local.reset()

        prev1_records = previous_paragraphs[-1:] if previous_paragraphs else []
        older_records = previous_paragraphs[:-1] if previous_paragraphs else []
        same_records = [r for r in previous_paragraphs if r["document"] == it.document]
        cross_records = [r for r in previous_paragraphs if r["document"] != it.document]
        pool_sources = {
            "PREV1": flatten(prev1_records),
            "OLDER": flatten(older_records),
            "SAME_SIDE_PREV": flatten(same_records),
            "CROSS_SIDE_PREV": flatten(cross_records),
            "ALL_PREV": flatten(previous_paragraphs),
        }
        current_sources: List[Tuple[int, Dict[tuple, float]]] = []

        for li, line in enumerate(it.lines):
            for ti, tok in enumerate(line):
                n_visible += 1
                local.prune(pos)
                seq = parsed[it.item_id][li][ti]
                if seq is not None:
                    p0 = P1.P0.p0_surface(v2, parser, tok, p_cache)
                    if p0 <= 0.0:
                        raise RuntimeError("V2 assigned non-positive literal probability")
                    ql, avl = local.q(tok)
                    p0_rows.append(float(p0))
                    qlocal_rows.append(float(ql))
                    avlocal_rows.append(bool(avl))
                    for pool in (*ATOMIC, ALL_POOL):
                        st = source_stats(pool_sources[pool], tok, pos, pool, it.leaf)
                        qbag[pool].append(st["q_bag"])
                        avail[pool].append(st["n"] > 0)
                        max_random_resid = max(max_random_resid, st["max_weight_sum_residual"])
                        if pool in ATOMIC:
                            qorder[pool].append(st["q_order"])
                            for s in RANDOM_SEEDS:
                                qrandom[pool][s].append(st["q_random"][s])

                dist = P1.source_distribution(index, tok)
                local.add(pos, dist)
                if dist is not None:
                    current_sources.append((int(pos), dist))
                pos += 1

        previous_paragraphs.append({
            "item_id": it.item_id,
            "document": it.document,
            "sources": current_sources,
        })

    n = len(p0_rows)
    for p in (*ATOMIC, ALL_POOL):
        if len(qbag[p]) != n or len(avail[p]) != n:
            raise RuntimeError(f"bag support mismatch for {p}")
    for p in ATOMIC:
        if len(qorder[p]) != n:
            raise RuntimeError(f"order support mismatch for {p}")
        for s in RANDOM_SEEDS:
            if len(qrandom[p][s]) != n:
                raise RuntimeError(f"random support mismatch for {p}/{s}")
    return {
        "p0": np.asarray(p0_rows, dtype=float),
        "q_local": np.asarray(qlocal_rows, dtype=float),
        "av_local": np.asarray(avlocal_rows, dtype=bool),
        "q_bag": {p: np.asarray(qbag[p], dtype=float) for p in (*ATOMIC, ALL_POOL)},
        "q_order": {p: np.asarray(qorder[p], dtype=float) for p in ATOMIC},
        "q_random": {p: {s: np.asarray(qrandom[p][s], dtype=float) for s in RANDOM_SEEDS} for p in ATOMIC},
        "avail": {p: np.asarray(avail[p], dtype=bool) for p in (*ATOMIC, ALL_POOL)},
        "n_scored": int(n),
        "n_visible": int(n_visible),
        "max_random_weight_sum_residual": float(max_random_resid),
    }


def local_probs(feat: dict, local_pi: float) -> np.ndarray:
    return mix(feat["p0"], feat["q_local"], feat["av_local"], local_pi)


def scalar_curve(base: np.ndarray, q: np.ndarray, av: np.ndarray) -> np.ndarray:
    probs = np.where(
        av[:, None],
        (1.0 - GRID[None, :]) * base[:, None] + GRID[None, :] * q[:, None],
        base[:, None],
    )
    if np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid scalar grid")
    return np.log(probs).sum(axis=0)


def joint_curve(base: np.ndarray, q1: np.ndarray, av1: np.ndarray, q2: np.ndarray, av2: np.ndarray) -> np.ndarray:
    q1s = np.where(av1, q1, base)
    q2s = np.where(av2, q2, base)
    out = np.empty(len(JOINT_GRID), dtype=float)
    for i, (a, b) in enumerate(JOINT_GRID):
        probs = (1.0 - a - b) * base + a * q1s + b * q2s
        if np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
            raise RuntimeError("invalid joint grid")
        out[i] = float(np.log(probs).sum())
    return out


def random_curve(base: np.ndarray, feat: dict, pool: str):
    by_seed = {}
    for s in RANDOM_SEEDS:
        by_seed[s] = scalar_curve(base, feat["q_random"][pool][s], feat["avail"][pool])
    return np.mean(np.stack([by_seed[s] for s in RANDOM_SEEDS]), axis=0), by_seed


def select_outer(vitems, folds, parsed, outer_f: int, parser):
    bag_total = {p: np.zeros(len(GRID), dtype=float) for p in (*ATOMIC, ALL_POOL)}
    order_total = {p: np.zeros(len(GRID), dtype=float) for p in ATOMIC}
    random_total = {p: np.zeros(len(GRID), dtype=float) for p in ATOMIC}
    random_seed_total = {p: {s: np.zeros(len(GRID), dtype=float) for s in RANDOM_SEEDS} for p in ATOMIC}
    temp_total = np.zeros(len(JOINT_GRID), dtype=float)
    side_total = np.zeros(len(JOINT_GRID), dtype=float)
    local_pi = float(CORRECTED[outer_f]["local_pi"])
    inner = []

    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        _tr, v2, index = B.fit_training(vitems, folds, parsed, (outer_f, inner_g))
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        feat = features(va, parsed, v2, index, parser)
        plocal = local_probs(feat, local_pi)
        for pool in (*ATOMIC, ALL_POOL):
            bag_total[pool] += scalar_curve(plocal, feat["q_bag"][pool], feat["avail"][pool])
        for pool in ATOMIC:
            order_total[pool] += scalar_curve(plocal, feat["q_order"][pool], feat["avail"][pool])
            mean_ll, by_seed = random_curve(plocal, feat, pool)
            random_total[pool] += mean_ll
            for s in RANDOM_SEEDS:
                random_seed_total[pool][s] += by_seed[s]
        temp_total += joint_curve(
            plocal, feat["q_bag"]["PREV1"], feat["avail"]["PREV1"],
            feat["q_bag"]["OLDER"], feat["avail"]["OLDER"],
        )
        side_total += joint_curve(
            plocal, feat["q_bag"]["SAME_SIDE_PREV"], feat["avail"]["SAME_SIDE_PREV"],
            feat["q_bag"]["CROSS_SIDE_PREV"], feat["avail"]["CROSS_SIDE_PREV"],
        )
        inner.append({
            "inner_fold": int(inner_g),
            "n_scored": feat["n_scored"],
            "n_visible": feat["n_visible"],
            "context_fraction": {p: float(np.mean(feat["avail"][p])) for p in (*ATOMIC, ALL_POOL)},
            "max_random_weight_sum_residual": feat["max_random_weight_sum_residual"],
        })

    bag_sel = {}
    order_sel = {}
    random_sel = {}
    for pool in (*ATOMIC, ALL_POOL):
        bi = choose_scalar(bag_total[pool])
        bag_sel[pool] = {
            "selected_alpha": float(GRID[bi]),
            "total_log_likelihood": float(bag_total[pool][bi]),
            "curve": [{"alpha": float(a), "total_log_likelihood": float(bag_total[pool][i])} for i, a in enumerate(GRID)],
        }
    for pool in ATOMIC:
        oi = choose_scalar(order_total[pool])
        ri = choose_scalar(random_total[pool])
        order_sel[pool] = {
            "selected_alpha": float(GRID[oi]),
            "total_log_likelihood": float(order_total[pool][oi]),
            "curve": [{"alpha": float(a), "total_log_likelihood": float(order_total[pool][i])} for i, a in enumerate(GRID)],
        }
        random_sel[pool] = {
            "selected_alpha": float(GRID[ri]),
            "mean_randomization_total_log_likelihood": float(random_total[pool][ri]),
            "by_seed_total_log_likelihood_at_selected": {str(s): float(random_seed_total[pool][s][ri]) for s in RANDOM_SEEDS},
            "curve": [
                {
                    "alpha": float(a),
                    "mean_randomization_total_log_likelihood": float(random_total[pool][i]),
                    "by_seed_total_log_likelihood": {str(s): float(random_seed_total[pool][s][i]) for s in RANDOM_SEEDS},
                }
                for i, a in enumerate(GRID)
            ],
        }

    ti = choose_joint(temp_total)
    si = choose_joint(side_total)
    ta, tb = JOINT_GRID[ti]
    sa, sb = JOINT_GRID[si]
    joint_sel = {
        "TEMP2": {
            "PREV1_weight": ta,
            "OLDER_weight": tb,
            "total_log_likelihood": float(temp_total[ti]),
            "grid": [
                {"PREV1_weight": a, "OLDER_weight": b, "total_log_likelihood": float(temp_total[i])}
                for i, (a, b) in enumerate(JOINT_GRID)
            ],
        },
        "SIDE2": {
            "SAME_SIDE_weight": sa,
            "CROSS_SIDE_weight": sb,
            "total_log_likelihood": float(side_total[si]),
            "grid": [
                {"SAME_SIDE_weight": a, "CROSS_SIDE_weight": b, "total_log_likelihood": float(side_total[i])}
                for i, (a, b) in enumerate(JOINT_GRID)
            ],
        },
    }

    expected_all = float(CORRECTED[outer_f]["all_prev_alpha"])
    if abs(bag_sel[ALL_POOL]["selected_alpha"] - expected_all) > TIE_EPS:
        raise RuntimeError(
            f"corrected Phase-2B ALL_PREV selection regression failed fold {outer_f}: "
            f"{bag_sel[ALL_POOL]['selected_alpha']} != {expected_all}"
        )
    return {"bag": bag_sel, "order": order_sel, "random": random_sel, "joint": joint_sel, "inner": inner}


def restricted_gain(p_num: np.ndarray, p_den: np.ndarray, mask: np.ndarray) -> dict:
    if not np.any(mask):
        return {"n": 0, "mean_bits_saved": None}
    vals = np.log(p_num[mask] / p_den[mask]) / LN2
    return {"n": int(np.sum(mask)), "mean_bits_saved": float(np.mean(vals))}


def score_outer(vitems, folds, parsed, outer_f: int, parser, sel: dict):
    _tr, v2, index = B.fit_training(vitems, folds, parsed, (outer_f,))
    test = I.b.by_leaves(vitems, folds[outer_f], include=True)
    feat = features(test, parsed, v2, index, parser)
    plocal = local_probs(feat, float(CORRECTED[outer_f]["local_pi"]))
    local_bits = bits(plocal)

    bag_probs = {}
    bag_bits = {}
    for pool in (*ATOMIC, ALL_POOL):
        alpha = float(sel["bag"][pool]["selected_alpha"])
        bag_probs[pool] = mix(plocal, feat["q_bag"][pool], feat["avail"][pool], alpha)
        bag_bits[pool] = bits(bag_probs[pool])

    ta = float(sel["joint"]["TEMP2"]["PREV1_weight"])
    tb = float(sel["joint"]["TEMP2"]["OLDER_weight"])
    p_temp = joint_mix(
        plocal, feat["q_bag"]["PREV1"], feat["avail"]["PREV1"],
        feat["q_bag"]["OLDER"], feat["avail"]["OLDER"], ta, tb,
    )
    sa = float(sel["joint"]["SIDE2"]["SAME_SIDE_weight"])
    sb = float(sel["joint"]["SIDE2"]["CROSS_SIDE_weight"])
    p_side = joint_mix(
        plocal, feat["q_bag"]["SAME_SIDE_PREV"], feat["avail"]["SAME_SIDE_PREV"],
        feat["q_bag"]["CROSS_SIDE_PREV"], feat["avail"]["CROSS_SIDE_PREV"], sa, sb,
    )
    temp_bits = bits(p_temp)
    side_bits = bits(p_side)

    order_probs = {}
    order_bits = {}
    random_probs = {p: {} for p in ATOMIC}
    random_bits = {p: {} for p in ATOMIC}
    random_mean = {}
    for pool in ATOMIC:
        oa = float(sel["order"][pool]["selected_alpha"])
        order_probs[pool] = mix(plocal, feat["q_order"][pool], feat["avail"][pool], oa)
        order_bits[pool] = bits(order_probs[pool])
        ra = float(sel["random"][pool]["selected_alpha"])
        for s in RANDOM_SEEDS:
            pr = mix(plocal, feat["q_random"][pool][s], feat["avail"][pool], ra)
            random_probs[pool][s] = pr
            random_bits[pool][str(s)] = bits(pr)
        random_mean[pool] = float(np.mean(list(random_bits[pool].values())))

    contrasts = {
        "G_prev1_cond": float(bag_bits["OLDER"] - temp_bits),
        "G_older_cond": float(bag_bits["PREV1"] - temp_bits),
        "G_same_side_cond": float(bag_bits["CROSS_SIDE_PREV"] - side_bits),
        "G_cross_side_cond": float(bag_bits["SAME_SIDE_PREV"] - side_bits),
    }
    for pool in ATOMIC:
        contrasts[f"G_order_{pool}"] = float(random_mean[pool] - order_bits[pool])
        contrasts[f"G_order_vs_bag_{pool}"] = float(bag_bits[pool] - order_bits[pool])

    cross_mask = feat["avail"]["CROSS_SIDE_PREV"]
    diagnostics = {
        "cross_side_available_fraction": float(np.mean(cross_mask)),
        "cross_side_joint_gain_restricted": restricted_gain(p_side, bag_probs["SAME_SIDE_PREV"], cross_mask),
        "cross_side_order_gain_restricted": restricted_gain(
            order_probs["CROSS_SIDE_PREV"],
            np.mean(np.stack([random_probs["CROSS_SIDE_PREV"][s] for s in RANDOM_SEEDS]), axis=0),
            cross_mask,
        ),
    }

    return {
        "fold": int(outer_f),
        "n_scored": feat["n_scored"],
        "n_visible": feat["n_visible"],
        "LOCAL40_bits_per_token": local_bits,
        "bag_bits_per_token": bag_bits,
        "TEMP2_bits_per_token": temp_bits,
        "SIDE2_bits_per_token": side_bits,
        "order_bits_per_token": order_bits,
        "random_bits_per_token": {p: {"by_seed": random_bits[p], "mean": random_mean[p]} for p in ATOMIC},
        "selected": {
            "bag": {p: float(sel["bag"][p]["selected_alpha"]) for p in (*ATOMIC, ALL_POOL)},
            "order": {p: float(sel["order"][p]["selected_alpha"]) for p in ATOMIC},
            "random": {p: float(sel["random"][p]["selected_alpha"]) for p in ATOMIC},
            "TEMP2": {"PREV1_weight": ta, "OLDER_weight": tb},
            "SIDE2": {"SAME_SIDE_weight": sa, "CROSS_SIDE_weight": sb},
        },
        "context_fraction": {p: float(np.mean(feat["avail"][p])) for p in (*ATOMIC, ALL_POOL)},
        "max_random_weight_sum_residual": feat["max_random_weight_sum_residual"],
        "contrasts": contrasts,
        "diagnostics": diagnostics,
    }


def stability(vals: Sequence[float]) -> dict:
    x = [float(v) for v in vals]
    return {
        "mean": float(np.mean(x)),
        "values": x,
        "positive_folds": int(sum(v > 0.0 for v in x)),
        "pass": bool(float(np.mean(x)) > 0.0 and sum(v > 0.0 for v in x) >= 4),
    }


def run(zl_path: Path):
    if I.b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b authority mismatch")
    order_config = OA.configure(zl_path)
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    order_verify = OA.verify(vitems)
    I.ordered = OA.ordered
    P2B.I.ordered = OA.ordered
    P1.I.ordered = OA.ordered
    B.I.ordered = OA.ordered

    if len(folds) != N_FOLDS:
        raise RuntimeError("fold count mismatch")
    parser = I.e.SlotParser()
    I.e.validate_parser(parser)

    selection = {str(f): select_outer(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    outer = [score_outer(vitems, folds, parsed, f, parser, selection[str(f)]) for f in range(N_FOLDS)]

    all_prev_mean = float(np.mean([r["bag_bits_per_token"][ALL_POOL] for r in outer]))
    local_mean = float(np.mean([r["LOCAL40_bits_per_token"] for r in outer]))
    if abs(all_prev_mean - CORRECTED_ALL_PREV_MEAN) > 1e-9:
        raise RuntimeError(f"corrected ALL_PREV mean regression failed: {all_prev_mean} != {CORRECTED_ALL_PREV_MEAN}")
    if abs(local_mean - CORRECTED_LOCAL_MEAN) > 1e-9:
        raise RuntimeError(f"corrected LOCAL mean regression failed: {local_mean} != {CORRECTED_LOCAL_MEAN}")

    primary_names = ("G_prev1_cond", "G_older_cond", "G_same_side_cond", "G_cross_side_cond")
    order_names = tuple(f"G_order_{p}" for p in ATOMIC)
    bag_order_names = tuple(f"G_order_vs_bag_{p}" for p in ATOMIC)
    summaries = {
        name: stability([r["contrasts"][name] for r in outer])
        for name in (*primary_names, *order_names, *bag_order_names)
    }

    prev1_pass = bool(summaries["G_prev1_cond"]["pass"])
    older_pass = bool(summaries["G_older_cond"]["pass"])
    same_pass = bool(summaries["G_same_side_cond"]["pass"])
    cross_pass = bool(summaries["G_cross_side_cond"]["pass"])
    if prev1_pass and older_pass:
        temporal = "TEMPORAL MULTISCALE"
    elif prev1_pass:
        temporal = "IMMEDIATE-PREVIOUS DOMINANT"
    elif older_pass:
        temporal = "OLDER-INVENTORY DOMINANT"
    else:
        temporal = "TEMPORAL INCONCLUSIVE"
    if cross_pass:
        side = "CROSS-SIDE TRANSPORT SURVIVES"
    elif same_pass:
        side = "SAME-SIDE DOMINANT"
    else:
        side = "SIDE INCONCLUSIVE"

    mean_bits = {
        "LOCAL40": local_mean,
        "TEMP2": float(np.mean([r["TEMP2_bits_per_token"] for r in outer])),
        "SIDE2": float(np.mean([r["SIDE2_bits_per_token"] for r in outer])),
    }
    for p in (*ATOMIC, ALL_POOL):
        mean_bits[f"BAG_{p}"] = float(np.mean([r["bag_bits_per_token"][p] for r in outer]))
    for p in ATOMIC:
        mean_bits[f"ORDERED_{p}"] = float(np.mean([r["order_bits_per_token"][p] for r in outer]))
        mean_bits[f"RANDOM_{p}"] = float(np.mean([r["random_bits_per_token"][p]["mean"] for r in outer]))

    restricted = {
        "cross_side_available_fraction_mean": float(np.mean([r["diagnostics"]["cross_side_available_fraction"] for r in outer])),
        "joint_gain_on_cross_available": {
            "weighted_n": int(sum(r["diagnostics"]["cross_side_joint_gain_restricted"]["n"] for r in outer)),
            "weighted_mean_bits_saved": None,
        },
        "order_gain_on_cross_available": {
            "weighted_n": int(sum(r["diagnostics"]["cross_side_order_gain_restricted"]["n"] for r in outer)),
            "weighted_mean_bits_saved": None,
        },
    }
    for key, src in (
        ("joint_gain_on_cross_available", "cross_side_joint_gain_restricted"),
        ("order_gain_on_cross_available", "cross_side_order_gain_restricted"),
    ):
        den = sum(r["diagnostics"][src]["n"] for r in outer)
        if den:
            restricted[key]["weighted_mean_bits_saved"] = float(
                sum(r["diagnostics"][src]["n"] * r["diagnostics"][src]["mean_bits_saved"] for r in outer) / den
            )

    out = {
        "schema": "issue98-phase2c-corrected-v1",
        "phase": "ISSUE98_PHASE2C",
        "classification": {"temporal": temporal, "page_side": side},
        "source": {
            "git_blob_sha1": I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": EXPECTED_ZL3B_BLOB,
        },
        "order_authority": {**order_config, **order_verify},
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "authority_hashes": {
            "AMENDMENT_AFTER_ORDER_CORRECTION.md": sha256_file(HERE.parent / "AMENDMENT_AFTER_ORDER_CORRECTION.md"),
            "phase2c_previous_paragraph_decomposition.py": sha256_file(HERE),
            "source_order_authority.py": sha256_file(PRED / "source_order_authority.py"),
            "phase2b_boundary_localization.py": sha256_file(PHASE2B_PATH),
        },
        "selection": selection,
        "outer": outer,
        "summary": {
            "mean_bits_per_token": mean_bits,
            "contrasts": summaries,
            "decision_inputs": {
                "PREV1_cond_pass": prev1_pass,
                "OLDER_cond_pass": older_pass,
                "SAME_SIDE_cond_pass": same_pass,
                "CROSS_SIDE_cond_pass": cross_pass,
            },
            "restricted_cross_side_diagnostics": restricted,
        },
        "regression": {
            "corrected_LOCAL40_mean": True,
            "corrected_ALL_PREV_alpha_all_folds": True,
            "corrected_ALL_PREV_mean": True,
            "fold_membership_changed": False,
        },
        "randomization": {
            "seeds": list(RANDOM_SEEDS),
            "seed_selected": False,
            "target_token_in_seed": False,
            "future_tokens_used": False,
            "tau": TAU_ORDER,
            "alpha_selected_nested_mean_ll": True,
        },
        "firewall": {
            "corrected_source_order_used": True,
            "future_test_tokens_used": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "currier_section_scribe_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
            "H_tau_window_reselected": False,
            "post_reveal_pool_or_grid_added": False,
        },
        "interpretation_boundary": {
            "syntax_established": False,
            "topic_established": False,
            "semantic_page_state_established": False,
            "content_transport_established": False,
            "latent_state_identified": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
    }
    return B.strict_safe(out)


def self_test():
    if len(JOINT_GRID) != 496:
        raise AssertionError(f"unexpected joint grid size {len(JOINT_GRID)}")
    p = np.asarray([.2, .4])
    q1 = np.asarray([.5, .1])
    q2 = np.asarray([.3, .7])
    av1 = np.asarray([True, False])
    av2 = np.asarray([False, True])
    if not np.allclose(joint_mix(p, q1, av1, q2, av2, 0.0, 0.0), p, atol=0.0, rtol=0.0):
        raise AssertionError("zero joint weights do not reduce to local")
    sources = [(1, {("x",): .8}), (4, {("x",): .2}), (7, {("x",): .5})]
    st = source_stats(sources, ("x",), 10, "TEST", 1)
    if abs(st["q_bag"] - .5) > 1e-12:
        raise AssertionError("bag probability mismatch")
    if st["max_weight_sum_residual"] > 1e-10:
        raise AssertionError("randomization did not preserve weights")
    return {
        "ok": True,
        "prediction_only": True,
        "corrected_source_order_required": True,
        "joint_grid_size": len(JOINT_GRID),
        "random_seeds": list(RANDOM_SEEDS),
        "tau_frozen": TAU_ORDER,
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
        "mean_bits_per_token": out["summary"]["mean_bits_per_token"],
        "primary_contrasts": {k: out["summary"]["contrasts"][k] for k in (
            "G_prev1_cond", "G_older_cond", "G_same_side_cond", "G_cross_side_cond")},
        "order_diagnostics": {k: out["summary"]["contrasts"][k] for k in (
            "G_order_PREV1", "G_order_OLDER", "G_order_SAME_SIDE_PREV", "G_order_CROSS_SIDE_PREV")},
        "decision_inputs": out["summary"]["decision_inputs"],
        "selected": {str(r["fold"]): r["selected"] for r in out["outer"]},
        "cross_side_diagnostics": out["summary"]["restricted_cross_side_diagnostics"],
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
