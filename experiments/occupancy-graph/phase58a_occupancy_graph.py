#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "issue26-music"))
import issue26e_core as e

ALPHA = 0.5
N_NULLS = 1000
N_SLOTS = 12
PAIRS = tuple(itertools.combinations(range(N_SLOTS), 2))
PAIR_I = np.asarray([x[0] for x in PAIRS], dtype=np.int64)
PAIR_J = np.asarray([x[1] for x in PAIRS], dtype=np.int64)
PAIR_OFF4 = (4 * np.arange(len(PAIRS), dtype=np.int64))[None, :]
PAIR_OFF44 = (44 * np.arange(len(PAIRS), dtype=np.int64))[None, :]
SELECTED = (3, 5)
SELECTED_INDEX = PAIRS.index(SELECTED)
assert len(PAIRS) == 66


def build_lines(items, folds, parser, policy):
    universe = set().union(*folds)
    leaf_to_fold = {int(leaf): f for f, leaves in enumerate(folds) for leaf in leaves}
    lines = []
    visible = parsed = 0
    slot_counts = np.zeros(N_SLOTS, dtype=np.int64)
    fold_tokens = np.zeros(5, dtype=np.int64)
    for it in items:
        leaf = it["leaf"]
        if leaf not in universe:
            continue
        fold = leaf_to_fold[int(leaf)]
        for li, toks in enumerate(it["lines"]):
            rows = []
            for tok in toks:
                visible += 1
                p = parser.pick(tok, policy)
                if p is None:
                    continue
                vals = p[1]
                b = np.fromiter((1 if vals[s] else 0 for s in range(N_SLOTS)), dtype=np.uint8, count=N_SLOTS)
                rows.append(b)
                slot_counts += b
                parsed += 1
                fold_tokens[fold] += 1
            if rows:
                lines.append({
                    "leaf": int(leaf),
                    "page": it["page"],
                    "paragraph": it["id"],
                    "line_index": int(li),
                    "fold": int(fold),
                    "occ": np.stack(rows),
                })
    lines.sort(key=lambda r: (r["leaf"], r["page"], r["paragraph"], r["line_index"]))
    return lines, {
        "visible_tokens": int(visible),
        "parsed_tokens": int(parsed),
        "parse_coverage": parsed / visible if visible else 0.0,
        "physical_lines_with_parsed_tokens": len(lines),
        "slot_occupancy_counts": slot_counts.astype(int).tolist(),
        "slot_occupancy_rates": (slot_counts / parsed).tolist() if parsed else [0.0] * N_SLOTS,
        "fold_parsed_tokens": fold_tokens.astype(int).tolist(),
    }


def flatten_lines(lines):
    X = np.concatenate([r["occ"] for r in lines], axis=0)
    folds = np.concatenate([np.full(len(r["occ"]), r["fold"], dtype=np.int64) for r in lines])
    lengths = np.asarray([len(r["occ"]) for r in lines], dtype=np.int64)
    maxlen = int(lengths.max())
    padded = np.zeros((len(lines), maxlen, N_SLOTS), dtype=np.uint8)
    mask = np.zeros((len(lines), maxlen), dtype=bool)
    for n, r in enumerate(lines):
        z = r["occ"]
        padded[n, :len(z)] = z
        mask[n, :len(z)] = True
    return X, folds, padded, mask


def fold_pair_counts(X, token_folds):
    codes = X[:, PAIR_I] * 2 + X[:, PAIR_J]
    idx = token_folds[:, None] * (len(PAIRS) * 4) + PAIR_OFF4 + codes
    C = np.bincount(idx.ravel(), minlength=5 * len(PAIRS) * 4)
    return C.reshape(5, len(PAIRS), 2, 2)


def fold_cond_counts(X, token_folds):
    total = X.sum(axis=1, dtype=np.int64)[:, None]
    bi = X[:, PAIR_I].astype(np.int64)
    bj = X[:, PAIR_J].astype(np.int64)
    k = total - bi - bj
    code = k * 4 + bi * 2 + bj
    idx = token_folds[:, None] * (len(PAIRS) * 44) + PAIR_OFF44 + code
    C = np.bincount(idx.ravel(), minlength=5 * len(PAIRS) * 44)
    return C.reshape(5, len(PAIRS), 11, 2, 2)


def held_gain_vec(train, held):
    T = train.astype(np.float64)
    H = held.astype(np.float64)
    n = H.sum(axis=(1, 2))
    row = T.sum(axis=2)
    col = T.sum(axis=1)
    nt = T.sum(axis=(1, 2))
    pi = (row + ALPHA) / (nt[:, None] + 2 * ALPHA)
    pj = (col + ALPHA) / (nt[:, None] + 2 * ALPHA)
    pjgi = (T + ALPHA) / (row[:, :, None] + 2 * ALPHA)
    pigj = (T + ALPHA) / (col[:, None, :] + 2 * ALPHA)
    cej = -(H * np.log2(pj[:, None, :])).sum(axis=(1, 2)) / n
    cejc = -(H * np.log2(pjgi)).sum(axis=(1, 2)) / n
    cei = -(H * np.log2(pi[:, :, None])).sum(axis=(1, 2)) / n
    ceic = -(H * np.log2(pigj)).sum(axis=(1, 2)) / n
    return ((cej - cejc) + (cei - ceic)) / 2.0


def crossfit_pair_counts(F):
    total = F.sum(axis=0)
    A = np.stack([held_gain_vec(total - F[f], F[f]) for f in range(5)])
    return {
        "fold_gains": A,
        "mean_gain": A.mean(axis=0),
        "all_five_positive": (A > 0).all(axis=0),
    }


def conditional_held_gain_vec(train, held):
    T = train.astype(np.float64)
    H = held.astype(np.float64)
    n = H.sum(axis=(1, 2, 3))
    nk = T.sum(axis=(2, 3))
    ci = T.sum(axis=3)
    cj = T.sum(axis=2)
    pjb = (cj + ALPHA) / (nk[:, :, None] + 2 * ALPHA)
    pib = (ci + ALPHA) / (nk[:, :, None] + 2 * ALPHA)
    pjfull = (T + ALPHA) / (ci[:, :, :, None] + 2 * ALPHA)
    pifull = (T + ALPHA) / (cj[:, :, None, :] + 2 * ALPHA)
    cejb = -(H * np.log2(pjb[:, :, None, :])).sum(axis=(1, 2, 3)) / n
    cejf = -(H * np.log2(pjfull)).sum(axis=(1, 2, 3)) / n
    ceib = -(H * np.log2(pib[:, :, :, None])).sum(axis=(1, 2, 3)) / n
    ceif = -(H * np.log2(pifull)).sum(axis=(1, 2, 3)) / n
    return ((cejb - cejf) + (ceib - ceif)) / 2.0


def crossfit_cond_counts(F):
    total = F.sum(axis=0)
    A = np.stack([conditional_held_gain_vec(total - F[f], F[f]) for f in range(5)])
    return {
        "fold_gains": A,
        "mean_gain": A.mean(axis=0),
        "all_five_positive": (A > 0).all(axis=0),
    }


def pooled_diagnostics(F):
    C = F.sum(axis=0).astype(np.float64)
    out = []
    for z in C:
        n00, n01, n10, n11 = z.ravel().tolist()
        n = n00 + n01 + n10 + n11
        r1 = n10 + n11
        r0 = n00 + n01
        c1 = n01 + n11
        c0 = n00 + n10
        den = math.sqrt(r1 * r0 * c1 * c0)
        phi = ((n11 * n00 - n10 * n01) / den) if den > 0 else 0.0
        obs = n11 / n if n else 0.0
        exp = (r1 / n) * (c1 / n) if n else 0.0
        ratio = obs / exp if exp > 0 else None
        out.append({
            "contingency": [[int(n00), int(n01)], [int(n10), int(n11)]],
            "phi": float(phi),
            "cooccupancy_rate": float(obs),
            "expected_cooccupancy_rate": float(exp),
            "cooccupancy_ratio": None if ratio is None else float(ratio),
        })
    return out


def shuffled_from_padded(padded, mask, null_index):
    rng = np.random.default_rng(e.stable_seed(f"Issue58A:LineSlotOccupancyShuffle:v2:{null_index}"))
    out = np.zeros_like(padded)
    invalid = ~mask
    for s in range(N_SLOTS):
        keys = rng.random(mask.shape)
        keys[invalid] = 2.0
        order = np.argsort(keys, axis=1, kind="stable")
        out[:, :, s] = np.take_along_axis(padded[:, :, s], order, axis=1)
    return out[mask]


def run_nulls(padded, mask, token_folds):
    null_max = np.empty(N_NULLS, dtype=np.float64)
    cond_null_max = np.empty(N_NULLS, dtype=np.float64)
    for n in range(N_NULLS):
        X = shuffled_from_padded(padded, mask, n)
        z = crossfit_pair_counts(fold_pair_counts(X, token_folds))
        q = crossfit_cond_counts(fold_cond_counts(X, token_folds))
        null_max[n] = float(z["mean_gain"].max())
        cond_null_max[n] = float(q["mean_gain"].max())
        if (n + 1) % 100 == 0:
            print(f"nulls={n+1}/{N_NULLS}", file=sys.stderr, flush=True)
    return null_max, cond_null_max


def maxt_p(real, null_max):
    return np.asarray([(1 + int((null_max >= x).sum())) / (N_NULLS + 1) for x in real], dtype=np.float64)


def parser_admissibility(parser):
    rows = []
    for i, j in PAIRS:
        representative = None
        for vi in e.SLOTS[i]:
            if representative is not None:
                break
            for vj in e.SLOTS[j]:
                token = vi + vj
                for _, vals in parser.parses(token):
                    if vals[i] != vi or vals[j] != vj:
                        continue
                    if all(vals[s] == "" for s in range(N_SLOTS) if s not in (i, j)):
                        representative = token
                        break
                if representative is not None:
                    break
        rows.append({
            "pair": [i, j],
            "cooccupancy_exact_parse_admitted": representative is not None,
            "representative_token": representative,
        })
    return {
        "tested_pairs": len(rows),
        "admitted_pairs": sum(r["cooccupancy_exact_parse_admitted"] for r in rows),
        "failures": [r for r in rows if not r["cooccupancy_exact_parse_admitted"]],
        "rows": rows,
    }


def edge_rows(real_cf, cond_cf, diag, pmax=None, cond_pmax=None):
    order = sorted(range(len(PAIRS)), key=lambda k: (-float(real_cf["mean_gain"][k]), PAIRS[k]))
    rank = {k: n + 1 for n, k in enumerate(order)}
    neg = [k for k in range(len(PAIRS)) if diag[k]["phi"] < 0]
    neg.sort(key=lambda k: (diag[k]["phi"], PAIRS[k]))
    exclusion_rank = {k: n + 1 for n, k in enumerate(neg)}
    rows = []
    for k, pair in enumerate(PAIRS):
        r = {
            "pair": list(pair),
            "rank_by_mean_gain": rank[k],
            "mean_gain": float(real_cf["mean_gain"][k]),
            "fold_gains": [float(x) for x in real_cf["fold_gains"][:, k]],
            "all_five_positive": bool(real_cf["all_five_positive"][k]),
            "conditional_mean_gain_k_other": float(cond_cf["mean_gain"][k]),
            "conditional_fold_gains_k_other": [float(x) for x in cond_cf["fold_gains"][:, k]],
            "conditional_all_five_positive": bool(cond_cf["all_five_positive"][k]),
            "exclusion_rank_by_negative_phi": exclusion_rank.get(k),
            **diag[k],
        }
        if pmax is not None:
            r["maxT_p"] = float(pmax[k])
        if cond_pmax is not None:
            r["conditional_maxT_p_k_other"] = float(cond_pmax[k])
        rows.append(r)
    return rows


def classify(rows):
    s = rows[SELECTED_INDEX]
    extreme = (
        s["rank_by_mean_gain"] <= 3
        and s["maxT_p"] <= 0.01
        and s["all_five_positive"]
        and s["phi"] < 0
    )
    qualifying = [r for r in rows if r["maxT_p"] <= 0.01 and r["all_five_positive"]]
    if extreme:
        label = "SELECTED SLOT3xSLOT5 EDGE IS GLOBALLY EXTREME"
    elif len(qualifying) >= 5:
        label = "BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE"
    elif len(qualifying) >= 1:
        label = "SPARSE OCCUPANCY DEPENDENCE; SLOT3xSLOT5 NOT GLOBALLY EXTREME"
    else:
        label = "NO FAMILY-WISE OCCUPANCY EDGE SURVIVES"
    complexity_sensitive = bool(
        extreme and (
            s["conditional_mean_gain_k_other"] <= 0
            or not s["conditional_all_five_positive"]
            or s["conditional_maxT_p_k_other"] > 0.01
        )
    )
    return label, {
        "selected_edge_extreme_gate": bool(extreme),
        "selected_edge_rank_le_3": bool(s["rank_by_mean_gain"] <= 3),
        "selected_edge_maxt_p_le_0_01": bool(s["maxT_p"] <= 0.01),
        "selected_edge_all_five_positive": bool(s["all_five_positive"]),
        "selected_edge_phi_negative": bool(s["phi"] < 0),
        "familywise_qualifying_edge_count": len(qualifying),
        "selected_edge_token_complexity_sensitive": complexity_sensitive,
        "selected_edge_conditional_maxt_p_le_0_01": bool(s["conditional_maxT_p_k_other"] <= 0.01),
        "selected_edge_conditional_all_five_positive": bool(s["conditional_all_five_positive"]),
    }


def real_policy(items, folds, parser, policy):
    lines, pop = build_lines(items, folds, parser, policy)
    X, token_folds, padded, mask = flatten_lines(lines)
    F = fold_pair_counts(X, token_folds)
    CF = fold_cond_counts(X, token_folds)
    real = crossfit_pair_counts(F)
    cond = crossfit_cond_counts(CF)
    diag = pooled_diagnostics(F)
    return pop, token_folds, padded, mask, real, cond, diag


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} ZL3b-n.txt", file=sys.stderr)
        return 2
    path = Path(sys.argv[1]).resolve()
    data = path.read_bytes()
    blob = e.git_blob_sha1(data)
    if blob != e.EXPECTED_ZL3B_BLOB:
        raise RuntimeError(f"ZL3b blob mismatch {blob}")

    items = e.parse_voynich(path)
    folds = e.physical_leaf_folds(items)
    if len(folds) != 5:
        raise RuntimeError("expected five physical-leaf folds")
    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    admiss = parser_admissibility(parser)

    pop, token_folds, padded, mask, real, cond, diag = real_policy(items, folds, parser, "min")
    null_max, cond_null_max = run_nulls(padded, mask, token_folds)
    pmax = maxt_p(real["mean_gain"], null_max)
    cpmax = maxt_p(cond["mean_gain"], cond_null_max)
    primary_rows = edge_rows(real, cond, diag, pmax, cpmax)
    classification, gates = classify(primary_rows)

    max_pop, _, _, _, max_real, max_cond, max_diag = real_policy(items, folds, parser, "max")
    max_rows = edge_rows(max_real, max_cond, max_diag)

    out = {
        "experiment": "Issue58A complete 12-slot occupancy-graph specificity audit",
        "classification": classification,
        "gates": gates,
        "selected_pair": list(SELECTED),
        "primary_min": {
            "population": pop,
            "edges": primary_rows,
            "selected_edge": primary_rows[SELECTED_INDEX],
            "familywise_qualifying_edges": [r["pair"] for r in primary_rows if r["maxT_p"] <= 0.01 and r["all_five_positive"]],
            "top10_by_mean_gain": [r for r in sorted(primary_rows, key=lambda r: (r["rank_by_mean_gain"], r["pair"]))[:10]],
            "null": {
                "count": N_NULLS,
                "maxT_mean_gain_min": float(null_max.min()),
                "maxT_mean_gain_median": float(np.median(null_max)),
                "maxT_mean_gain_q95": float(np.quantile(null_max, 0.95)),
                "maxT_mean_gain_max": float(null_max.max()),
                "conditional_maxT_min": float(cond_null_max.min()),
                "conditional_maxT_median": float(np.median(cond_null_max)),
                "conditional_maxT_q95": float(np.quantile(cond_null_max, 0.95)),
                "conditional_maxT_max": float(cond_null_max.max()),
            },
        },
        "max_sensitivity": {
            "population": max_pop,
            "edges": max_rows,
            "selected_edge": max_rows[SELECTED_INDEX],
            "top10_by_mean_gain": [r for r in sorted(max_rows, key=lambda r: (r["rank_by_mean_gain"], r["pair"]))[:10]],
        },
        "parser_admissibility": admiss,
        "parser_validation": validation,
        "pair_count": len(PAIRS),
        "smoothing_alpha": ALPHA,
        "null_count": N_NULLS,
        "source": {"zl3b_git_blob": blob},
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
