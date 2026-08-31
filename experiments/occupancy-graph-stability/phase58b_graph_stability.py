#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

HERE = Path(__file__).resolve()
EXPERIMENTS = HERE.parents[1]
sys.path.insert(0, str(EXPERIMENTS / "issue26-music"))
sys.path.insert(0, str(HERE.parent))
import issue26e_core as e
import source_audit as sa

ALPHA = 0.5
N_NULLS = 1000
N_SLOTS = 12
PAIRS = tuple(itertools.combinations(range(N_SLOTS), 2))
PAIR_I = np.asarray([p[0] for p in PAIRS], dtype=np.int64)
PAIR_J = np.asarray([p[1] for p in PAIRS], dtype=np.int64)
PAIR_OFF44 = 44 * np.arange(len(PAIRS), dtype=np.int64)[None, :]
PAIR_OFF4 = 4 * np.arange(len(PAIRS), dtype=np.int64)[None, :]
EXPECTED_SOURCE_BLOB = "2a4533ab9bdfa85db9bad602d590978953055df1"
EXPECTED_VISIBLE = 32570
EXPECTED_PARSED = 25071

META_GROUPS = ("AH", "BH", "BB", "BS")
META_INDEX = {name: i for i, name in enumerate(META_GROUPS)}
POSITION_GROUPS = ("initial", "interior", "final")
POSITION_INDEX = {name: i for i, name in enumerate(POSITION_GROUPS)}
CONTRASTS = (
    ("CURRIER_H_A_vs_B", "AH", "BH", "register_section"),
    ("SECTION_B_vs_H", "BB", "BH", "register_section"),
    ("SECTION_B_vs_S", "BB", "BS", "register_section"),
    ("SECTION_H_vs_S", "BH", "BS", "register_section"),
    ("POSITION_initial_vs_interior", "initial", "interior", "position"),
    ("POSITION_initial_vs_final", "initial", "final", "position"),
    ("POSITION_interior_vs_final", "interior", "final", "position"),
)
EXPECTED_GROUP_FOLDS = {
    "AH": [1434, 851, 1328, 1070, 837],
    "BH": [179, 753, 417, 533, 567],
    "BB": [999, 941, 1116, 1191, 689],
    "BS": [1269, 1270, 2135, 1917, 1157],
    "initial": [536, 547, 653, 616, 563],
    "interior": [3398, 3765, 4303, 4290, 3800],
    "final": [492, 497, 552, 540, 504],
}


def corr(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if len(a) != len(b) or len(a) < 2 or np.std(a) <= 1e-15 or np.std(b) <= 1e-15:
        return None
    z = float(np.corrcoef(a, b)[0, 1])
    return z if math.isfinite(z) else None


def spearman(a, b):
    return corr(rankdata(np.asarray(a, float), method="average"), rankdata(np.asarray(b, float), method="average"))


def cosine(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    den = float(np.linalg.norm(a) * np.linalg.norm(b))
    if den <= 1e-15:
        return None
    z = float(np.dot(a, b) / den)
    return z if math.isfinite(z) else None


def med(xs, minimum=4):
    vals = [float(x) for x in xs if x is not None and math.isfinite(float(x))]
    return None if len(vals) < minimum else float(np.median(vals))


def meta_group(lval, ival):
    if (lval, ival) == ("A", "H"):
        return "AH"
    if (lval, ival) == ("B", "H"):
        return "BH"
    if (lval, ival) == ("B", "B"):
        return "BB"
    if (lval, ival) == ("B", "S"):
        return "BS"
    return None


def build_dataset(path, parser, policy):
    path = Path(path)
    raw = path.read_bytes()
    blob = e.git_blob_sha1(raw)
    if blob != EXPECTED_SOURCE_BLOB:
        raise RuntimeError(f"source blob mismatch: {blob}")
    pages, _ = sa.parse_page_metadata(raw.decode("utf-8", errors="ignore"))
    items = e.parse_voynich(path)
    folds = e.physical_leaf_folds(items)
    universe = set().union(*folds)
    leaf_to_fold = {int(leaf): f for f, leaves in enumerate(folds) for leaf in leaves}

    visible = parsed = 0
    lines = []
    for item in items:
        if item["leaf"] not in universe:
            continue
        leaf = int(item["leaf"])
        fold = int(leaf_to_fold[leaf])
        page = item["page"]
        pm = pages.get(page, {})
        lval = pm.get("L", sa.MISSING)
        ival = pm.get("I", sa.MISSING)
        mg = meta_group(lval, ival)
        for line_index, toks in enumerate(item["lines"]):
            n_visible = len(toks)
            visible += n_visible
            rows, positions = [], []
            for idx, tok in enumerate(toks):
                picked = parser.pick(tok, policy)
                if picked is None:
                    continue
                vals = picked[1]
                rows.append(np.fromiter((bool(vals[s]) for s in range(N_SLOTS)), dtype=np.uint8, count=N_SLOTS))
                positions.append(sa.position_category(idx, n_visible))
                parsed += 1
            if rows:
                lines.append({
                    "leaf": leaf,
                    "fold": fold,
                    "page": page,
                    "paragraph": item["id"],
                    "line_index": int(line_index),
                    "meta_group": mg,
                    "occ": np.stack(rows),
                    "positions": tuple(positions),
                })

    lines.sort(key=lambda x: (x["leaf"], x["page"], x["paragraph"], x["line_index"]))
    if (visible, parsed) != (EXPECTED_VISIBLE, EXPECTED_PARSED):
        raise RuntimeError(f"population mismatch: {(visible, parsed)}")

    X = np.concatenate([x["occ"] for x in lines], axis=0)
    token_folds = np.concatenate([np.full(len(x["occ"]), x["fold"], np.int8) for x in lines])
    meta_id = np.concatenate([np.full(len(x["occ"]), META_INDEX.get(x["meta_group"], -1), np.int8) for x in lines])
    pos_id = np.concatenate([
        np.asarray([POSITION_INDEX.get(p, -1) for p in x["positions"]], dtype=np.int8) for x in lines
    ])

    maxlen = max(len(x["occ"]) for x in lines)
    padded = np.zeros((len(lines), maxlen, N_SLOTS), dtype=np.uint8)
    line_mask = np.zeros((len(lines), maxlen), dtype=bool)
    for n, x in enumerate(lines):
        z = x["occ"]
        padded[n, : len(z)] = z
        line_mask[n, : len(z)] = True
    if not np.array_equal(padded[line_mask], X):
        raise RuntimeError("padded/flat ordering mismatch")

    return {
        "source_blob": blob,
        "folds": [sorted(map(int, f)) for f in folds],
        "visible": visible,
        "parsed": parsed,
        "X": X,
        "token_folds": token_folds,
        "meta_id": meta_id,
        "pos_id": pos_id,
        "padded": padded,
        "line_mask": line_mask,
    }


def validate_support(d):
    got = {}
    for name, idx in META_INDEX.items():
        got[name] = [int(np.sum((d["meta_id"] == idx) & (d["token_folds"] == f))) for f in range(5)]
    for name, idx in POSITION_INDEX.items():
        got[name] = [int(np.sum((d["pos_id"] == idx) & (d["token_folds"] == f))) for f in range(5)]
    for name, expected in EXPECTED_GROUP_FOLDS.items():
        if got[name] != expected:
            raise RuntimeError(f"support mismatch {name}: {got[name]} != {expected}")
    return {name: {"parsed_tokens": int(sum(v)), "fold_parsed_tokens": v} for name, v in got.items()}


def pair_codes(X):
    total = X.sum(axis=1, dtype=np.int64)[:, None]
    bi = X[:, PAIR_I].astype(np.int64)
    bj = X[:, PAIR_J].astype(np.int64)
    return (total - bi - bj) * 4 + bi * 2 + bj


def partition_counts(code, ids, n_groups, conditional):
    valid = ids >= 0
    c = code[valid]
    g = ids[valid].astype(np.int64)
    if conditional:
        idx = g[:, None] * (len(PAIRS) * 44) + PAIR_OFF44 + c
        return np.bincount(idx.ravel(), minlength=n_groups * len(PAIRS) * 44).reshape(n_groups, len(PAIRS), 11, 2, 2)
    idx = g[:, None] * (len(PAIRS) * 4) + PAIR_OFF4 + (c % 4)
    return np.bincount(idx.ravel(), minlength=n_groups * len(PAIRS) * 4).reshape(n_groups, len(PAIRS), 2, 2)


def q_cond(C):
    C = np.asarray(C, np.float64)
    n = C.sum(axis=(-1, -2))
    active = n > 0
    n00, n01, n10, n11 = C[..., 0, 0], C[..., 0, 1], C[..., 1, 0], C[..., 1, 1]
    nk = n + 4 * ALPHA
    numerator = ((((n11 + ALPHA) * (n00 + ALPHA)) / nk) * active).sum(axis=-1)
    denominator = ((((n10 + ALPHA) * (n01 + ALPHA)) / nk) * active).sum(axis=-1)
    odds = numerator / denominator
    return (odds - 1.0) / (odds + 1.0)


def q_raw(C):
    C = np.asarray(C, np.float64)
    n00, n01, n10, n11 = C[..., 0, 0] + ALPHA, C[..., 0, 1] + ALPHA, C[..., 1, 0] + ALPHA, C[..., 1, 1] + ALPHA
    odds = (n11 * n00) / (n10 * n01)
    return (odds - 1.0) / (odds + 1.0)


def graphs_partitioned(X, meta_id, pos_id, conditional=True):
    code = pair_codes(X)
    if conditional:
        mg = q_cond(partition_counts(code, meta_id, len(META_GROUPS), True))
        pg = q_cond(partition_counts(code, pos_id, len(POSITION_GROUPS), True))
    else:
        mg = q_raw(partition_counts(code, meta_id, len(META_GROUPS), False))
        pg = q_raw(partition_counts(code, pos_id, len(POSITION_GROUPS), False))
    out = {name: mg[idx] for name, idx in META_INDEX.items()}
    out.update({name: pg[idx] for name, idx in POSITION_INDEX.items()})
    return out


def graph_mask(X, mask, conditional=True):
    Z = X[mask]
    ids = np.zeros(len(Z), dtype=np.int8)
    code = pair_codes(Z)
    if conditional:
        return q_cond(partition_counts(code, ids, 1, True))[0]
    return q_raw(partition_counts(code, ids, 1, False))[0]


def observed(d, conditional=True):
    masks = {name: d["meta_id"] == idx for name, idx in META_INDEX.items()}
    masks.update({name: d["pos_id"] == idx for name, idx in POSITION_INDEX.items()})
    full = {name: graph_mask(d["X"], m, conditional) for name, m in masks.items()}
    train, held = defaultdict(dict), defaultdict(dict)
    within = {}
    for name, mask in masks.items():
        vals = []
        for f in range(5):
            gt = graph_mask(d["X"], mask & (d["token_folds"] != f), conditional)
            gh = graph_mask(d["X"], mask & (d["token_folds"] == f), conditional)
            train[name][f], held[name][f] = gt, gh
            vals.append(corr(gt, gh))
        within[name] = {"fold_correlations": vals, "median": med(vals)}

    contrasts = {}
    for label, s, t, family in CONTRASTS:
        st = [corr(train[s][f], held[t][f]) for f in range(5)]
        ts = [corr(train[t][f], held[s][f]) for f in range(5)]
        contrasts[label] = {
            "source": s,
            "target": t,
            "family": family,
            "pearson_full": corr(full[s], full[t]),
            "spearman_full": spearman(full[s], full[t]),
            "cosine_full": cosine(full[s], full[t]),
            "source_to_target_fold": st,
            "source_to_target_median": med(st),
            "target_to_source_fold": ts,
            "target_to_source_median": med(ts),
        }
    return {
        "group_graphs": {k: v.tolist() for k, v in full.items()},
        "within_reliability": within,
        "contrasts": contrasts,
    }


def shuffled_flat(d, null_index):
    rng = np.random.default_rng(e.stable_seed(f"Issue58B:GraphStability:LineSlotOccupancyShuffle:v1:{null_index}"))
    keys = rng.random(d["padded"].shape)
    keys[~d["line_mask"]] = 2.0
    order = np.argsort(keys, axis=1, kind="stable")
    shuffled = np.take_along_axis(d["padded"], order, axis=1)
    shuffled[~d["line_mask"]] = 0
    if null_index == 0 and not np.array_equal(d["padded"].sum(axis=1), shuffled.sum(axis=1)):
        raise RuntimeError("null failed line x slot marginal preservation")
    return shuffled[d["line_mask"]]


def run_nulls(d):
    real_graphs = graphs_partitioned(d["X"], d["meta_id"], d["pos_id"], True)
    real_r = {label: corr(real_graphs[s], real_graphs[t]) for label, s, t, _ in CONTRASTS}
    if any(x is None for x in real_r.values()):
        raise RuntimeError(f"zero-variance real graph: {real_r}")
    maxima = np.empty(N_NULLS, dtype=float)
    for n in range(N_NULLS):
        Y = shuffled_flat(d, n)
        g = graphs_partitioned(Y, d["meta_id"], d["pos_id"], True)
        rs = []
        for _, s, t, _ in CONTRASTS:
            z = corr(g[s], g[t])
            rs.append(0.0 if z is None else z)
        maxima[n] = max(rs)
        if (n + 1) % 100 == 0:
            print(f"Issue58B null {n+1}/{N_NULLS}", file=sys.stderr, flush=True)
    p = {label: float((1 + int(np.sum(maxima >= r))) / (N_NULLS + 1)) for label, r in real_r.items()}
    return {
        "real_full_pearson": real_r,
        "p_maxT": p,
        "maxT_values": maxima.tolist(),
        "maxT_summary": {
            "min": float(np.min(maxima)),
            "median": float(np.median(maxima)),
            "q95": float(np.quantile(maxima, 0.95)),
            "max": float(np.max(maxima)),
        },
    }


def classify(m, within, pmax):
    s, t = m["source"], m["target"]
    ws, wt = within[s]["median"], within[t]["median"]
    r, st, ts = m["pearson_full"], m["source_to_target_median"], m["target_to_source_median"]
    reliable = ws is not None and wt is not None and ws >= 0.50 and wt >= 0.50
    valid = all(x is not None for x in (r, st, ts))
    stable = reliable and valid and pmax <= 0.01 and r >= 0.70 and st >= max(0.60, wt - 0.15) and ts >= max(0.60, ws - 0.15)
    if stable:
        label = "STABLE"
    elif reliable and valid and (r < 0.40 or st < 0.30 or ts < 0.30):
        label = "DIFFERENT_OR_MIXTURE"
    elif reliable and valid and pmax <= 0.01 and r >= 0.40 and st >= 0.30 and ts >= 0.30:
        label = "RELATED_BUT_MODULATED"
    else:
        label = "INCONCLUSIVE"
    return {
        "classification": label,
        "reliable": bool(reliable),
        "within_source": ws,
        "within_target": wt,
        "pearson_full": r,
        "p_maxT": pmax,
        "source_to_target": st,
        "target_to_source": ts,
        "stable_required_source_to_target": None if wt is None else max(0.60, wt - 0.15),
        "stable_required_target_to_source": None if ws is None else max(0.60, ws - 0.15),
    }


def global_labels(classes):
    primary = [n for n, _, _, f in CONTRASTS if f == "register_section"]
    position = [n for n, _, _, f in CONTRASTS if f == "position"]
    a = [classes[n]["classification"] for n in primary]
    b = [classes[n]["classification"] for n in position]
    if all(x == "STABLE" for x in a):
        reg = "SHARED CORE SIGNED OCCUPANCY GRAPH ACROSS CURRIER AND SECTION"
    elif any(x == "DIFFERENT_OR_MIXTURE" for x in a):
        reg = "REGISTER/SECTION MIXTURE MATERIALLY CHANGES OCCUPANCY GRAPH"
    elif any(x == "INCONCLUSIVE" for x in a):
        reg = "CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE"
    else:
        reg = "SHARED CORE WITH CURRIER/SECTION MODULATION"

    if all(x == "STABLE" for x in b):
        pos = "LINE-POSITION STABLE SIGNED GRAPH"
    elif any(x == "DIFFERENT_OR_MIXTURE" for x in b):
        pos = "LINE-POSITION MATERIALLY MODULATES GRAPH"
    elif any(x == "INCONCLUSIVE" for x in b):
        pos = "LINE-POSITION GRAPH STABILITY INCONCLUSIVE"
    else:
        pos = "LINE-POSITION RELATED BUT MODULATED"
    return reg, pos


def self_test():
    C = np.zeros((3, 66, 11, 2, 2), dtype=np.int64)
    C[0, :, 3] = np.asarray([[50, 1], [1, 50]])
    C[1, :, 3] = np.asarray([[1, 50], [50, 1]])
    C[2, :, 3] = np.asarray([[25, 25], [25, 25]])
    q = q_cond(C)
    if not (np.all(q[0] > 0.8) and np.all(q[1] < -0.8) and np.all(np.abs(q[2]) < 1e-12)):
        raise RuntimeError("conditional Q synthetic test failed")
    x = np.arange(66, dtype=float)
    if abs(corr(x, x) - 1.0) > 1e-12 or abs(spearman(x, x[::-1]) + 1.0) > 1e-12:
        raise RuntimeError("correlation synthetic test failed")
    padded = np.zeros((2, 3, N_SLOTS), dtype=np.uint8)
    line_mask = np.asarray([[1, 1, 1], [1, 1, 0]], dtype=bool)
    padded[0, :3, 0] = [1, 0, 1]
    padded[0, :3, 1] = [0, 1, 0]
    padded[1, :2, 0] = [1, 0]
    padded[1, :2, 2] = [0, 1]
    shuffled_flat({"padded": padded, "line_mask": line_mask}, 0)


def main(path):
    self_test()
    parser = e.SlotParser()
    parser_validation = e.validate_parser(parser)

    d = build_dataset(path, parser, "min")
    support = validate_support(d)
    obs = observed(d, True)
    raw_obs = observed(d, False)
    nulls = run_nulls(d)
    classes = {label: classify(obs["contrasts"][label], obs["within_reliability"], nulls["p_maxT"][label]) for label, _, _, _ in CONTRASTS}
    register_section, position = global_labels(classes)

    dmax = build_dataset(path, parser, "max")
    max_support = validate_support(dmax)
    if support != max_support:
        raise RuntimeError("min/max support mismatch")

    out = {
        "phase": "Issue58B-A",
        "target_reveal": True,
        "source": {"git_blob": d["source_blob"], "expected_git_blob": EXPECTED_SOURCE_BLOB},
        "parser": {"primary_policy": "min", "sensitivity_policy": "max", "validation": parser_validation},
        "population": {"visible_tokens": d["visible"], "parsed_tokens": d["parsed"], "group_support": support, "physical_leaf_folds": d["folds"]},
        "pairs": [list(x) for x in PAIRS],
        "primary_min": {
            "graph_definition": "K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule Q",
            "observed": obs,
            "null": nulls,
            "contrast_classifications": classes,
            "register_section_classification": register_section,
            "position_classification": position,
        },
        "sensitivities": {
            "raw_unconditional_min": raw_obs,
            "max_parser_observed_only": {"conditional": observed(dmax, True), "raw_unconditional": observed(dmax, False)},
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--self-test":
        self_test()
        print("Issue58B synthetic self-test: OK")
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        raise SystemExit("usage: phase58b_graph_stability.py --self-test | ZL3b-n.txt")
