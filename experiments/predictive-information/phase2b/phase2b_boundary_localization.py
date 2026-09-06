#!/usr/bin/env python3
"""Issue #96 / Issue #88 Phase 2B boundary localization.

Prediction-only attribution of prefix inventory and actual lag/source association
across visible line and paragraph boundaries. No future-token or surface-target
access. All new scalar weights are selected by nested literal-surface likelihood.
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
PHASE2A_PATH = ROOT / "experiments" / "predictive-information" / "phase2a" / "phase2a_amended.py"
EXPECTED_ZL3B_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
N_FOLDS = 5
LN2 = math.log(2.0)
GRID = np.asarray([round(i / 100.0, 2) for i in range(31)], dtype=float)
RANDOM_SEEDS = (0, 1, 2, 3, 4)
TIE_EPS = 1e-12
TAU_ORDER = 128.0

EXPECTED = {
    0: {"A0": 9.74553213453277, "A2": 9.704993852780854, "A5": 9.709475084111618, "local_pi": .21, "leaf_rho": .20},
    1: {"A0": 9.654379389512654, "A2": 9.612149532173033, "A5": 9.615559783948873, "local_pi": .21, "leaf_rho": .21},
    2: {"A0": 9.44552408749662, "A2": 9.387814289841517, "A5": 9.383276385780013, "local_pi": .20, "leaf_rho": .20},
    3: {"A0": 9.478509701296273, "A2": 9.417253956137694, "A5": 9.422377790180956, "local_pi": .21, "leaf_rho": .20},
    4: {"A0": 9.656960288057821, "A2": 9.624058563568518, "A5": 9.62868695614544, "local_pi": .21, "leaf_rho": .21},
}

POOLS = ("LINE", "CURR_PARA", "PREV_PARAS", "LEAF_PREFIX")
ORDER_POOLS = ("CURR_PARA", "PREV_PARAS", "LEAF_PREFIX")
RANDOM_POOLS = ("CURR_PARA", "PREV_PARAS")


def load_phase2a():
    spec = importlib.util.spec_from_file_location("issue94_phase2a_authority", PHASE2A_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import Phase-2A authority")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    # Interface compatibility retained from the authoritative Phase-2A runner.
    mod.P1.mix_probs = mod.B.mix_probs
    return mod


A = load_phase2a()
B = A.B
P1 = A.P1
I = A.I


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bits(probs: np.ndarray) -> float:
    if len(probs) == 0 or np.any(probs <= 0.0) or not np.all(np.isfinite(probs)):
        raise RuntimeError("invalid probability vector")
    return float(-np.log(probs).mean() / LN2)


def mix(base: np.ndarray, q: np.ndarray, avail: np.ndarray, alpha: float) -> np.ndarray:
    out = np.where(avail, (1.0 - alpha) * base + alpha * q, base)
    if np.any(out <= 0.0) or not np.all(np.isfinite(out)):
        raise RuntimeError("invalid boundary mixture probability")
    return out


def choose(grid: np.ndarray, ll: np.ndarray) -> int:
    best = 0
    for i in range(1, len(grid)):
        if ll[i] > ll[best] + TIE_EPS:
            best = i
        elif abs(float(ll[i] - ll[best])) <= TIE_EPS and float(grid[i]) < float(grid[best]):
            best = i
    return int(best)


def state_line4(it, li: int) -> str:
    return P1.line4_state(it, li)


def source_stats(
    sources: Sequence[Tuple[int, Dict[tuple, float]]],
    target,
    pos: int,
    pool_name: str,
    leaf,
    randomize: bool,
):
    m = len(sources)
    if m == 0:
        return {
            "n": 0,
            "bag_num": 0.0,
            "order_num": 0.0,
            "order_den": 0.0,
            "q_bag": 0.0,
            "q_order": 0.0,
            "q_random": {s: 0.0 for s in RANDOM_SEEDS},
            "max_weight_sum_residual": 0.0,
        }
    qvals = np.fromiter((dist.get(target, 0.0) for _src_pos, dist in sources), dtype=float, count=m)
    weights = np.fromiter((math.exp(-(pos - src_pos) / TAU_ORDER) for src_pos, _dist in sources), dtype=float, count=m)
    den = float(weights.sum())
    if den <= 0.0 or not math.isfinite(den):
        raise RuntimeError("invalid ordered pool denominator")
    bag_num = float(qvals.sum())
    order_num = float(np.dot(weights, qvals))
    qbag = bag_num / m
    qorder = order_num / den
    qr = {s: 0.0 for s in RANDOM_SEEDS}
    max_resid = 0.0
    if randomize:
        for s in RANDOM_SEEDS:
            seed = I.e.stable_seed(f"ISSUE96:{pool_name}:RANDOM_LAG:{s}:{leaf}:{pos}")
            perm = np.random.default_rng(seed).permutation(m)
            wp = weights[perm]
            resid = abs(float(wp.sum()) - den)
            max_resid = max(max_resid, resid)
            if resid > max(1e-12, 1e-12 * den):
                raise RuntimeError("random-lag changed recency-weight multiset")
            qr[s] = float(np.dot(wp, qvals) / den)
    for q in [qbag, qorder, *qr.values()]:
        if q < -1e-12 or q > 1.0 + 1e-10 or not math.isfinite(q):
            raise RuntimeError("pool probability outside range")
    return {
        "n": int(m),
        "bag_num": bag_num,
        "order_num": order_num,
        "order_den": den,
        "q_bag": float(qbag),
        "q_order": float(qorder),
        "q_random": qr,
        "max_weight_sum_residual": float(max_resid),
    }


def combine_stats(a: dict, b: dict):
    n = int(a["n"] + b["n"])
    den = float(a["order_den"] + b["order_den"])
    return {
        "n": n,
        "q_bag": float((a["bag_num"] + b["bag_num"]) / n) if n else 0.0,
        "q_order": float((a["order_num"] + b["order_num"]) / den) if den > 0.0 else 0.0,
    }


def boundary_features(items, parsed, v2, index, parser):
    local = P1.RecencyAccumulator(40, 32.0)
    p_cache: Dict[object, float] = {}
    p0_rows: List[float] = []
    qlocal_rows: List[float] = []
    avlocal_rows: List[bool] = []
    qbag = {p: [] for p in POOLS}
    qorder = {p: [] for p in ORDER_POOLS}
    avail = {p: [] for p in POOLS}
    qrandom = {p: {s: [] for s in RANDOM_SEEDS} for p in RANDOM_POOLS}
    states_entry: List[str] = []
    states_line4: List[str] = []
    current_leaf = None
    prev_para_sources: List[Tuple[int, Dict[tuple, float]]] = []
    para_sources: List[Tuple[int, Dict[tuple, float]]] = []
    pos = 0
    visible = 0
    max_random_resid = 0.0

    for it in I.ordered(items):
        if it.leaf != current_leaf:
            current_leaf = it.leaf
            prev_para_sources = []
            para_sources = []
            pos = 0
            local.reset()
        else:
            # Ordered items on the same leaf are successive parser paragraphs.
            prev_para_sources.extend(para_sources)
            para_sources = []

        for li, line in enumerate(it.lines):
            line_sources: List[Tuple[int, Dict[tuple, float]]] = []
            for ti, tok in enumerate(line):
                visible += 1
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

                    st_line = source_stats(line_sources, tok, pos, "LINE", it.leaf, False)
                    st_para = source_stats(para_sources, tok, pos, "CURR_PARA", it.leaf, True)
                    st_prev = source_stats(prev_para_sources, tok, pos, "PREV_PARAS", it.leaf, True)
                    st_leaf = combine_stats(st_para, st_prev)
                    max_random_resid = max(
                        max_random_resid,
                        st_para["max_weight_sum_residual"],
                        st_prev["max_weight_sum_residual"],
                    )

                    qbag["LINE"].append(st_line["q_bag"])
                    qbag["CURR_PARA"].append(st_para["q_bag"])
                    qbag["PREV_PARAS"].append(st_prev["q_bag"])
                    qbag["LEAF_PREFIX"].append(st_leaf["q_bag"])
                    qorder["CURR_PARA"].append(st_para["q_order"])
                    qorder["PREV_PARAS"].append(st_prev["q_order"])
                    qorder["LEAF_PREFIX"].append(st_leaf["q_order"])
                    for p, st in (("CURR_PARA", st_para), ("PREV_PARAS", st_prev)):
                        for s in RANDOM_SEEDS:
                            qrandom[p][s].append(st["q_random"][s])
                    avail["LINE"].append(st_line["n"] > 0)
                    avail["CURR_PARA"].append(st_para["n"] > 0)
                    avail["PREV_PARAS"].append(st_prev["n"] > 0)
                    avail["LEAF_PREFIX"].append(st_leaf["n"] > 0)
                    states_entry.append("ENTRY" if li == 0 else "BODY")
                    states_line4.append(state_line4(it, li))

                dist = P1.source_distribution(index, tok)
                local.add(pos, dist)
                if dist is not None:
                    rec = (int(pos), dist)
                    line_sources.append(rec)
                    para_sources.append(rec)
                pos += 1

    n = len(p0_rows)
    for p in POOLS:
        if len(qbag[p]) != n or len(avail[p]) != n:
            raise RuntimeError("pool feature support mismatch")
    for p in ORDER_POOLS:
        if len(qorder[p]) != n:
            raise RuntimeError("ordered pool support mismatch")
    for p in RANDOM_POOLS:
        for s in RANDOM_SEEDS:
            if len(qrandom[p][s]) != n:
                raise RuntimeError("random pool support mismatch")
    return {
        "p0": np.asarray(p0_rows, dtype=float),
        "q_local": np.asarray(qlocal_rows, dtype=float),
        "av_local": np.asarray(avlocal_rows, dtype=bool),
        "q_bag": {p: np.asarray(qbag[p], dtype=float) for p in POOLS},
        "q_order": {p: np.asarray(qorder[p], dtype=float) for p in ORDER_POOLS},
        "q_random": {p: {s: np.asarray(qrandom[p][s], dtype=float) for s in RANDOM_SEEDS} for p in RANDOM_POOLS},
        "avail": {p: np.asarray(avail[p], dtype=bool) for p in POOLS},
        "entry_body": np.asarray(states_entry, dtype=object),
        "line4": np.asarray(states_line4, dtype=object),
        "n_scored": int(n),
        "n_visible": int(visible),
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
        raise RuntimeError("invalid scalar likelihood grid")
    return np.log(probs).sum(axis=0)


def random_curve(base: np.ndarray, feat: dict, pool: str):
    total_by_seed = {}
    av = feat["avail"][pool]
    for s in RANDOM_SEEDS:
        total_by_seed[s] = scalar_curve(base, feat["q_random"][pool][s], av)
    mean_ll = np.mean(np.stack([total_by_seed[s] for s in RANDOM_SEEDS]), axis=0)
    return mean_ll, total_by_seed


def select_outer_controls(vitems, folds, parsed, outer_f: int, parser):
    bag_total = {p: np.zeros(len(GRID), dtype=float) for p in POOLS}
    order_total = {p: np.zeros(len(GRID), dtype=float) for p in ORDER_POOLS}
    random_total = {p: np.zeros(len(GRID), dtype=float) for p in RANDOM_POOLS}
    random_seed_total = {p: {s: np.zeros(len(GRID), dtype=float) for s in RANDOM_SEEDS} for p in RANDOM_POOLS}
    local_pi = float(EXPECTED[outer_f]["local_pi"])
    inner = []

    for inner_g in range(N_FOLDS):
        if inner_g == outer_f:
            continue
        _tr, v2, index = B.fit_training(vitems, folds, parsed, (outer_f, inner_g))
        va = I.b.by_leaves(vitems, folds[inner_g], include=True)
        feat = boundary_features(va, parsed, v2, index, parser)
        plocal = local_probs(feat, local_pi)
        for p in POOLS:
            bag_total[p] += scalar_curve(plocal, feat["q_bag"][p], feat["avail"][p])
        for p in ORDER_POOLS:
            order_total[p] += scalar_curve(plocal, feat["q_order"][p], feat["avail"][p])
        for p in RANDOM_POOLS:
            mean_ll, by_seed = random_curve(plocal, feat, p)
            random_total[p] += mean_ll
            for s in RANDOM_SEEDS:
                random_seed_total[p][s] += by_seed[s]
        inner.append({
            "inner_fold": int(inner_g),
            "n_scored": feat["n_scored"],
            "n_visible": feat["n_visible"],
            "max_random_weight_sum_residual": feat["max_random_weight_sum_residual"],
        })

    def pack(curves: dict, kind: str):
        out = {}
        for p, ll in curves.items():
            bi = choose(GRID, ll)
            out[p] = {
                "selected_alpha": float(GRID[bi]),
                "total_log_likelihood": float(ll[bi]),
                "curve": [
                    {"alpha": float(a), "total_log_likelihood": float(ll[i])}
                    for i, a in enumerate(GRID)
                ],
            }
            if kind == "random":
                out[p]["by_seed_total_log_likelihood_at_selected"] = {
                    str(s): float(random_seed_total[p][s][bi]) for s in RANDOM_SEEDS
                }
        return out

    bag = pack(bag_total, "bag")
    order = pack(order_total, "order")
    random = pack(random_total, "random")
    expected_rho = float(EXPECTED[outer_f]["leaf_rho"])
    if abs(bag["LEAF_PREFIX"]["selected_alpha"] - expected_rho) > TIE_EPS:
        raise RuntimeError(
            f"Phase-2A A5 nested selection regression failed fold {outer_f}: "
            f"{bag['LEAF_PREFIX']['selected_alpha']} != {expected_rho}"
        )
    return {"bag": bag, "order": order, "random": random, "inner": inner}


def group_gain(probs_num: np.ndarray, probs_den: np.ndarray, labels: np.ndarray):
    """Bits saved by numerator model over denominator model, by observable state."""
    vals = np.log(probs_num / probs_den) / LN2
    out = {}
    for label in sorted(set(str(x) for x in labels)):
        m = labels == label
        out[label] = {
            "n": int(np.sum(m)),
            "mean_bits_saved": float(np.mean(vals[m])) if np.any(m) else None,
        }
    return out


def random_group_gain(order_probs: np.ndarray, random_probs: Dict[int, np.ndarray], labels: np.ndarray):
    vals = np.mean(
        np.stack([np.log(order_probs / random_probs[s]) / LN2 for s in RANDOM_SEEDS]),
        axis=0,
    )
    out = {}
    for label in sorted(set(str(x) for x in labels)):
        m = labels == label
        out[label] = {
            "n": int(np.sum(m)),
            "mean_bits_saved": float(np.mean(vals[m])) if np.any(m) else None,
        }
    return out


def score_outer(vitems, folds, parsed, outer_f: int, parser, sel: dict):
    _tr, v2, index = B.fit_training(vitems, folds, parsed, (outer_f,))
    test = I.b.by_leaves(vitems, folds[outer_f], include=True)
    feat = boundary_features(test, parsed, v2, index, parser)
    exp = EXPECTED[outer_f]
    plocal = local_probs(feat, float(exp["local_pi"]))
    a0 = bits(plocal)
    if abs(a0 - float(exp["A0"])) > 1e-9:
        raise RuntimeError(f"LOCAL40 regression failed fold {outer_f}: {a0} != {exp['A0']}")

    # Exact Phase-1 A2 standalone ordered reference.
    p_a2 = mix(feat["p0"], feat["q_order"]["LEAF_PREFIX"], feat["avail"]["LEAF_PREFIX"], .30)
    a2 = bits(p_a2)
    if abs(a2 - float(exp["A2"])) > 1e-9:
        raise RuntimeError(f"ORDERED128 regression failed fold {outer_f}: {a2} != {exp['A2']}")

    bag_probs = {}
    bag_bits = {}
    for p in POOLS:
        alpha = float(sel["bag"][p]["selected_alpha"])
        bag_probs[p] = mix(plocal, feat["q_bag"][p], feat["avail"][p], alpha)
        bag_bits[p] = bits(bag_probs[p])
    if abs(bag_bits["LEAF_PREFIX"] - float(exp["A5"])) > 1e-9:
        raise RuntimeError(
            f"Phase-2A A5 code-length regression failed fold {outer_f}: "
            f"{bag_bits['LEAF_PREFIX']} != {exp['A5']}"
        )

    order_probs = {}
    order_bits = {}
    for p in ORDER_POOLS:
        alpha = float(sel["order"][p]["selected_alpha"])
        order_probs[p] = mix(plocal, feat["q_order"][p], feat["avail"][p], alpha)
        order_bits[p] = bits(order_probs[p])

    random_probs = {p: {} for p in RANDOM_POOLS}
    random_bits = {p: {} for p in RANDOM_POOLS}
    random_mean_bits = {}
    for p in RANDOM_POOLS:
        alpha = float(sel["random"][p]["selected_alpha"])
        for s in RANDOM_SEEDS:
            pr = mix(plocal, feat["q_random"][p][s], feat["avail"][p], alpha)
            random_probs[p][s] = pr
            random_bits[p][str(s)] = bits(pr)
        random_mean_bits[p] = float(np.mean(list(random_bits[p].values())))

    contrasts = {
        "G_line_inventory": float(a0 - bag_bits["LINE"]),
        "G_within_para_inventory": float(a0 - bag_bits["CURR_PARA"]),
        "G_cross_para_inventory": float(bag_bits["CURR_PARA"] - bag_bits["LEAF_PREFIX"]),
        "G_prev_para_inventory": float(a0 - bag_bits["PREV_PARAS"]),
        "G_order_within_para": float(random_mean_bits["CURR_PARA"] - order_bits["CURR_PARA"]),
        "G_order_cross_para": float(random_mean_bits["PREV_PARAS"] - order_bits["PREV_PARAS"]),
        "G_order_vs_bag_within_para": float(bag_bits["CURR_PARA"] - order_bits["CURR_PARA"]),
        "G_order_vs_bag_prev_para": float(bag_bits["PREV_PARAS"] - order_bits["PREV_PARAS"]),
        "G_leaf_order_localbase_over_leaf_bag": float(bag_bits["LEAF_PREFIX"] - order_bits["LEAF_PREFIX"]),
    }

    diagnostics = {
        "ENTRY_BODY": {
            "within_para_inventory": group_gain(bag_probs["CURR_PARA"], plocal, feat["entry_body"]),
            "cross_para_inventory": group_gain(bag_probs["LEAF_PREFIX"], bag_probs["CURR_PARA"], feat["entry_body"]),
            "order_within_para": random_group_gain(order_probs["CURR_PARA"], random_probs["CURR_PARA"], feat["entry_body"]),
            "order_cross_para": random_group_gain(order_probs["PREV_PARAS"], random_probs["PREV_PARAS"], feat["entry_body"]),
        },
        "LINE4": {
            "within_para_inventory": group_gain(bag_probs["CURR_PARA"], plocal, feat["line4"]),
            "cross_para_inventory": group_gain(bag_probs["LEAF_PREFIX"], bag_probs["CURR_PARA"], feat["line4"]),
            "order_within_para": random_group_gain(order_probs["CURR_PARA"], random_probs["CURR_PARA"], feat["line4"]),
            "order_cross_para": random_group_gain(order_probs["PREV_PARAS"], random_probs["PREV_PARAS"], feat["line4"]),
        },
    }

    return {
        "fold": int(outer_f),
        "n_scored": feat["n_scored"],
        "n_visible": feat["n_visible"],
        "A0_LOCAL40_bits_per_token": a0,
        "A2_ORDERED128_STANDALONE_bits_per_token": a2,
        "bag_bits_per_token": bag_bits,
        "order_bits_per_token": order_bits,
        "random_bits_per_token": {
            p: {"by_seed": random_bits[p], "mean": random_mean_bits[p]} for p in RANDOM_POOLS
        },
        "selected": {
            "bag": {p: float(sel["bag"][p]["selected_alpha"]) for p in POOLS},
            "order": {p: float(sel["order"][p]["selected_alpha"]) for p in ORDER_POOLS},
            "random": {p: float(sel["random"][p]["selected_alpha"]) for p in RANDOM_POOLS},
        },
        "context_fraction": {p: float(np.mean(feat["avail"][p])) for p in POOLS},
        "max_random_weight_sum_residual": feat["max_random_weight_sum_residual"],
        "contrasts": contrasts,
        "state_diagnostics": diagnostics,
    }


def stability(vals: Sequence[float]):
    x = [float(v) for v in vals]
    return {
        "mean": float(np.mean(x)),
        "values": x,
        "positive_folds": int(sum(v > 0.0 for v in x)),
        "pass": bool(float(np.mean(x)) > 0.0 and sum(v > 0.0 for v in x) >= 4),
    }


def aggregate_state(outer: Sequence[dict], family: str, contrast: str):
    labels = sorted({label for row in outer for label in row["state_diagnostics"][family][contrast]})
    out = {}
    for label in labels:
        numer = denom = 0.0
        by_fold = []
        for row in outer:
            d = row["state_diagnostics"][family][contrast].get(label)
            if d is None or not d["n"]:
                continue
            n = int(d["n"])
            g = float(d["mean_bits_saved"])
            numer += n * g
            denom += n
            by_fold.append({"fold": row["fold"], "n": n, "mean_bits_saved": g})
        out[label] = {
            "n": int(denom),
            "mean_bits_saved": float(numer / denom) if denom else None,
            "by_fold": by_fold,
        }
    return out


def run(zl_path: Path):
    if I.b.git_blob_sha1(zl_path.read_bytes()) != EXPECTED_ZL3B_BLOB:
        raise RuntimeError("ZL3b authority mismatch")
    vitems, folds, parsed = I.C.load_corpus(zl_path)
    if len(folds) != N_FOLDS:
        raise RuntimeError("fold count mismatch")
    parser = I.e.SlotParser()
    I.e.validate_parser(parser)

    selection = {str(f): select_outer_controls(vitems, folds, parsed, f, parser) for f in range(N_FOLDS)}
    outer = [score_outer(vitems, folds, parsed, f, parser, selection[str(f)]) for f in range(N_FOLDS)]

    names = [
        "G_line_inventory",
        "G_within_para_inventory",
        "G_cross_para_inventory",
        "G_prev_para_inventory",
        "G_order_within_para",
        "G_order_cross_para",
        "G_order_vs_bag_within_para",
        "G_order_vs_bag_prev_para",
        "G_leaf_order_localbase_over_leaf_bag",
    ]
    contrasts = {name: stability([r["contrasts"][name] for r in outer]) for name in names}
    within_inventory = bool(contrasts["G_within_para_inventory"]["pass"])
    within_order = bool(contrasts["G_order_within_para"]["pass"])
    cross_inventory = bool(contrasts["G_cross_para_inventory"]["pass"])
    cross_order = bool(contrasts["G_order_cross_para"]["pass"])
    within = bool(within_inventory or within_order)
    cross = bool(cross_inventory or cross_order)
    if within and cross:
        classification = "MULTISCALE"
    elif cross:
        classification = "PREDICTIVE DEPENDENCE CROSSES PARAGRAPH BOUNDARIES"
    elif within:
        classification = "PREDICTIVE DEPENDENCE LOCALIZES WITHIN PARAGRAPH"
    else:
        classification = "BOUNDARY ATTRIBUTION INCONCLUSIVE"

    mean_bits = {
        "A0_LOCAL40": float(np.mean([r["A0_LOCAL40_bits_per_token"] for r in outer])),
        "A2_ORDERED128_STANDALONE": float(np.mean([r["A2_ORDERED128_STANDALONE_bits_per_token"] for r in outer])),
    }
    for p in POOLS:
        mean_bits[f"LOCAL_PLUS_{p}_BAG"] = float(np.mean([r["bag_bits_per_token"][p] for r in outer]))
    for p in ORDER_POOLS:
        mean_bits[f"LOCAL_PLUS_{p}_ORDERED128"] = float(np.mean([r["order_bits_per_token"][p] for r in outer]))
    for p in RANDOM_POOLS:
        mean_bits[f"LOCAL_PLUS_{p}_RANDOM_LAG"] = float(np.mean([r["random_bits_per_token"][p]["mean"] for r in outer]))

    state_summary = {}
    for family in ("ENTRY_BODY", "LINE4"):
        state_summary[family] = {}
        for contrast in ("within_para_inventory", "cross_para_inventory", "order_within_para", "order_cross_para"):
            state_summary[family][contrast] = aggregate_state(outer, family, contrast)

    out = {
        "schema": "issue96-phase2b-v1",
        "phase": "ISSUE96_PHASE2B",
        "classification": classification,
        "source": {
            "git_blob_sha1": I.b.git_blob_sha1(zl_path.read_bytes()),
            "expected_git_blob_sha1": EXPECTED_ZL3B_BLOB,
        },
        "fold_identity_sha256": P1.P0.fold_hash(folds),
        "authority_hashes": {
            "PLAN.md": sha256_file(HERE.parent / "PLAN.md"),
            "phase2b_boundary_localization.py": sha256_file(HERE),
            "phase2a_amended.py": sha256_file(PHASE2A_PATH),
        },
        "selection": selection,
        "outer": outer,
        "summary": {
            "mean_bits_per_token": mean_bits,
            "contrasts": contrasts,
            "decision_inputs": {
                "WITHIN_inventory": within_inventory,
                "WITHIN_order": within_order,
                "CROSS_inventory": cross_inventory,
                "CROSS_order": cross_order,
                "WITHIN": within,
                "CROSS": cross,
            },
            "state_diagnostics": state_summary,
        },
        "regression": {
            "LOCAL40_all_folds": True,
            "ORDERED128_standalone_all_folds": True,
            "Phase2A_A5_leaf_prefix_bag_selection_all_folds": True,
            "Phase2A_A5_leaf_prefix_bag_code_length_all_folds": True,
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
            "future_test_tokens_used": False,
            "surface_target_metrics_scored": False,
            "issue84_target_used": False,
            "currier_section_scribe_used": False,
            "semantic_or_image_context_used": False,
            "latent_state_fitted": False,
            "tau_or_window_reselected": False,
        },
        "interpretation_boundary": {
            "uniform_historical_memory_established": False,
            "paragraph_semantics_established": False,
            "latent_state_identified": False,
            "plaintext_recovered": False,
            "decipherment_established": False,
        },
    }
    return B.strict_safe(out)


def self_test():
    sources = [
        (0, {("a",): .75, ("b",): .25}),
        (3, {("a",): .20, ("b",): .80}),
        (7, {("a",): .50, ("b",): .50}),
    ]
    st = source_stats(sources, ("a",), 10, "TEST", 1, True)
    assert st["n"] == 3
    assert abs(st["q_bag"] - (0.75 + 0.20 + 0.50) / 3.0) < 1e-12
    assert 0.0 <= st["q_order"] <= 1.0
    assert st["max_weight_sum_residual"] < 1e-10
    p = np.asarray([.2, .4])
    q = np.asarray([.5, .1])
    av = np.asarray([True, False])
    assert np.allclose(mix(p, q, av, 0.0), p, atol=0.0, rtol=0.0)
    return {
        "ok": True,
        "prediction_only": True,
        "future_tokens_used": False,
        "surface_target_calls": 0,
        "tau_frozen": TAU_ORDER,
        "seeds": list(RANDOM_SEEDS),
        "grid": [float(x) for x in GRID],
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
        "primary_contrasts": {
            k: out["summary"]["contrasts"][k]
            for k in (
                "G_line_inventory",
                "G_within_para_inventory",
                "G_cross_para_inventory",
                "G_order_within_para",
                "G_order_cross_para",
            )
        },
        "decision_inputs": out["summary"]["decision_inputs"],
        "selected": {str(r["fold"]): r["selected"] for r in out["outer"]},
        "firewall": out["firewall"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
