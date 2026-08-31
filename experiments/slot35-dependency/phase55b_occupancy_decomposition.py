#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parents[1] / "issue26-music"))
import phase55a_slot35_dependency as a
import issue26e_core as e

ALPHA = 0.5
N_NULLS = 1000


def binary_counts(C):
    return np.asarray([
        [C[0, 0], C[0, 1:].sum()],
        [C[1:, 0].sum(), C[1:, 1:].sum()],
    ], dtype=np.int64)


def binary_held_gain(train, held):
    T = binary_counts(train).astype(np.float64)
    H = binary_counts(held).astype(np.float64)
    n = float(H.sum())
    row = T.sum(axis=1)
    col = T.sum(axis=0)
    total = float(T.sum())
    p3 = (row + ALPHA) / (total + 2 * ALPHA)
    p5 = (col + ALPHA) / (total + 2 * ALPHA)
    p5g3 = (T + ALPHA) / (row[:, None] + 2 * ALPHA)
    p3g5 = (T + ALPHA) / (col[None, :] + 2 * ALPHA)
    ce5 = -float((H * np.log2(p5[None, :])).sum() / n)
    ce5c = -float((H * np.log2(p5g3)).sum() / n)
    ce3 = -float((H * np.log2(p3[:, None])).sum() / n)
    ce3c = -float((H * np.log2(p3g5)).sum() / n)
    g5 = ce5 - ce5c
    g3 = ce3 - ce3c
    return {"held_tokens": int(n), "g5": g5, "g3": g3, "gsym": (g3 + g5) / 2.0}


def occupancy_conditionals(C):
    C = C.astype(np.float64)
    B = binary_counts(C).astype(np.float64)
    br = B.sum(axis=1)
    bc = B.sum(axis=0)
    pb5gb3 = (B + ALPHA) / (br[:, None] + 2 * ALPHA)
    pb3gb5 = (B + ALPHA) / (bc[None, :] + 2 * ALPHA)

    c5 = C[:, 1:].sum(axis=0)
    p5sub = (c5 + ALPHA) / (float(c5.sum()) + 4 * ALPHA)
    c3 = C[1:, :].sum(axis=1)
    p3sub = (c3 + ALPHA) / (float(c3.sum()) + 4 * ALPHA)

    q5g3 = np.zeros((5, 5), dtype=np.float64)
    for i in range(5):
        b3 = 0 if i == 0 else 1
        q5g3[i, 0] = pb5gb3[b3, 0]
        q5g3[i, 1:] = pb5gb3[b3, 1] * p5sub

    q3g5 = np.zeros((5, 5), dtype=np.float64)
    for j in range(5):
        b5 = 0 if j == 0 else 1
        q3g5[0, j] = pb3gb5[0, b5]
        q3g5[1:, j] = pb3gb5[1, b5] * p3sub

    if not np.allclose(q5g3.sum(axis=1), 1.0):
        raise RuntimeError("slot5 occupancy model normalization failure")
    if not np.allclose(q3g5.sum(axis=0), 1.0):
        raise RuntimeError("slot3 occupancy model normalization failure")
    return q5g3, q3g5


def residual_held(train, held):
    _, _, full5, full3 = a.probs_from_train(train)
    occ5, occ3 = occupancy_conditionals(train)
    H = held.astype(np.float64)
    n = float(H.sum())
    ce_full5 = -float((H * np.log2(full5)).sum() / n)
    ce_occ5 = -float((H * np.log2(occ5)).sum() / n)
    ce_full3 = -float((H * np.log2(full3)).sum() / n)
    ce_occ3 = -float((H * np.log2(occ3)).sum() / n)
    r5 = ce_occ5 - ce_full5
    r3 = ce_occ3 - ce_full3
    return {
        "held_tokens": int(n),
        "ce_full_slot5_given_slot3": ce_full5,
        "ce_occupancy_slot5_given_slot3": ce_occ5,
        "residual_gain_slot5": r5,
        "ce_full_slot3_given_slot5": ce_full3,
        "ce_occupancy_slot3_given_slot5": ce_occ3,
        "residual_gain_slot3": r3,
        "residual_symmetric_gain": (r3 + r5) / 2.0,
    }


def crossfit_decomposition(F):
    total = F.sum(axis=0)
    full_rows = []
    bin_rows = []
    resid_rows = []
    for f in range(5):
        train = total - F[f]
        held = F[f]
        full = a.held_gain(train, held)
        binary = binary_held_gain(train, held)
        resid = residual_held(train, held)
        full_rows.append({"fold": f, **full})
        bin_rows.append({"fold": f, **binary})
        resid_rows.append({"fold": f, **resid})
    full_mean = float(statistics.fmean(x["symmetric_gain"] for x in full_rows))
    bin_mean = float(statistics.fmean(x["gsym"] for x in bin_rows))
    resid_mean = float(statistics.fmean(x["residual_symmetric_gain"] for x in resid_rows))
    return {
        "full_fold_rows": full_rows,
        "binary_fold_rows": bin_rows,
        "residual_fold_rows": resid_rows,
        "mean_full_gain": full_mean,
        "mean_binary_gain": bin_mean,
        "occupancy_fraction_of_full_gain": float(bin_mean / full_mean) if full_mean != 0 else float("nan"),
        "mean_residual_symmetric_gain": resid_mean,
        "all_residual_folds_positive": all(x["residual_symmetric_gain"] > 0 for x in resid_rows),
    }


def subtype_shuffled_counts(lines, leaf_to_fold, null_index):
    out = np.zeros((5, 5, 5), dtype=np.int64)
    for r in lines:
        x3 = r["s3"].copy()
        x5 = r["s5"].copy()
        pos3 = np.flatnonzero(x3 > 0)
        pos5 = np.flatnonzero(x5 > 0)
        if len(pos3) >= 2:
            label = (
                f"Issue55B:Slot3SubtypeShuffle:v1:{null_index}:"
                f"{r['page']}:{r['paragraph']}:{r['line_index']}"
            )
            rng = np.random.default_rng(e.stable_seed(label))
            vals = x3[pos3].copy(); rng.shuffle(vals); x3[pos3] = vals
        if len(pos5) >= 2:
            label = (
                f"Issue55B:Slot5SubtypeShuffle:v1:{null_index}:"
                f"{r['page']}:{r['paragraph']}:{r['line_index']}"
            )
            rng = np.random.default_rng(e.stable_seed(label))
            vals = x5[pos5].copy(); rng.shuffle(vals); x5[pos5] = vals
        if not np.array_equal(x3 > 0, r["s3"] > 0) or not np.array_equal(x5 > 0, r["s5"] > 0):
            raise RuntimeError("occupancy preservation failure")
        a.add_pairs(out[leaf_to_fold[r["leaf"]]], x3, x5)
    return out


def null_audit(lines, leaf_to_fold, real_resid):
    vals = []
    posfold = []
    for n in range(N_NULLS):
        F = subtype_shuffled_counts(lines, leaf_to_fold, n)
        z = crossfit_decomposition(F)
        vals.append(z["mean_residual_symmetric_gain"])
        posfold.append(sum(x["residual_symmetric_gain"] > 0 for x in z["residual_fold_rows"]))
        if (n + 1) % 100 == 0:
            print(f"subtype_nulls={n+1}/{N_NULLS}", file=sys.stderr, flush=True)
    upper = sum(x >= real_resid for x in vals)
    med = float(statistics.median(vals))
    return {
        "null_count": N_NULLS,
        "upper_tail_count": int(upper),
        "upper_tail_p": float((1 + upper) / (N_NULLS + 1)),
        "median_residual_gain": med,
        "q05": float(np.quantile(vals, 0.05)),
        "q95": float(np.quantile(vals, 0.95)),
        "minimum": float(min(vals)),
        "maximum": float(max(vals)),
        "real_advantage_over_null_median": float(real_resid - med),
        "positive_residual_fold_count_distribution": {
            str(k): int(v) for k, v in sorted(__import__("collections").Counter(posfold).items())
        },
    }


def parser_admissibility(parser):
    rows = []
    failures = []
    for s3 in a.S3:
        for s5 in a.S5:
            if not s3 and not s5:
                continue
            token = s3 + s5
            exact = False
            parses = parser.parses(token)
            for _, vals in parses:
                if vals[3] != s3 or vals[5] != s5:
                    continue
                if all(vals[k] == "" for k in range(12) if k not in (3, 5)):
                    exact = True
                    break
            row = {"slot3": s3, "slot5": s5, "canonical_token": token, "exact_parse_admitted": exact, "parse_count": len(parses)}
            rows.append(row)
            if not exact:
                failures.append(row)
    return {"tested_nonempty_pairs": len(rows), "exact_pairs_admitted": len(rows) - len(failures), "failures": failures, "rows": rows}


def rare_cooccupancy(items, leaves, parser, policy):
    out = []
    for it in items:
        if it["leaf"] not in leaves:
            continue
        for li, toks in enumerate(it["lines"]):
            for ti, tok in enumerate(toks):
                p = parser.pick(tok, policy)
                if p is None:
                    continue
                vals = p[1]
                if vals[3] and vals[5]:
                    out.append({
                        "leaf": int(it["leaf"]), "page": it["page"], "paragraph": it["id"],
                        "line_index": int(li), "token_index": int(ti), "token": tok,
                        "slot3": vals[3], "slot5": vals[5],
                    })
    return out


def run_policy(items, folds, parser, policy):
    universe = set().union(*folds)
    leaf_to_fold = {int(leaf): f for f, leaves in enumerate(folds) for leaf in leaves}
    lines, pop = a.build_lines(items, universe, parser, policy)
    F = a.counts_by_fold(lines, leaf_to_fold)
    real = crossfit_decomposition(F)
    null = null_audit(lines, leaf_to_fold, real["mean_residual_symmetric_gain"])
    rare = rare_cooccupancy(items, universe, parser, policy)
    return {"policy": policy, "population": pop, "real": real, "subtype_null": null, "rare_cooccupancy": rare}


def classify(primary):
    z = primary["real"]
    n = primary["subtype_null"]
    focc = z["occupancy_fraction_of_full_gain"]
    resid = z["mean_residual_symmetric_gain"]
    if focc >= 0.95 and resid <= 0.005:
        c = "DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION"
    elif (
        (focc < 0.95 or resid > 0.005)
        and n["upper_tail_p"] <= 0.01
        and n["real_advantage_over_null_median"] >= 0.01
        and z["all_residual_folds_positive"]
    ):
        c = "SUBTYPE-LEVEL SLOT3xSLOT5 DEPENDENCE REMAINS"
    else:
        c = "OCCUPANCY-DOMINANT WITH SMALL OR UNSTABLE SUBTYPE RESIDUAL"
    return c, {
        "occupancy_fraction_ge_0_95": bool(focc >= 0.95),
        "real_mean_residual_le_0_005": bool(resid <= 0.005),
        "subtype_null_p_le_0_01": bool(n["upper_tail_p"] <= 0.01),
        "residual_advantage_ge_0_01": bool(n["real_advantage_over_null_median"] >= 0.01),
        "all_five_residual_folds_positive": bool(z["all_residual_folds_positive"]),
    }


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
    parser = e.SlotParser()
    validation = e.validate_parser(parser)
    admiss = parser_admissibility(parser)

    primary = run_policy(items, folds, parser, "min")
    classification, gates = classify(primary)
    sensitivity = run_policy(items, folds, parser, "max")

    out = {
        "experiment": "Issue55B slot3xslot5 occupancy-versus-subtype decomposition",
        "classification": classification,
        "gates": gates,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
        "parser_admissibility": admiss,
        "state_order": {"slot3": list(a.S3), "slot5": list(a.S5)},
        "smoothing_alpha": ALPHA,
        "null_count": N_NULLS,
        "parser_validation": validation,
        "source": {"zl3b_git_blob": blob},
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
