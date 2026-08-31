#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1] / "issue26-music"))
import issue26e_core as e

S3 = ("", "t", "k", "p", "f")
S5 = ("", "cth", "ckh", "cph", "cfh")
I3 = {v: i for i, v in enumerate(S3)}
I5 = {v: i for i, v in enumerate(S5)}
ALPHA = 0.5
N_NULLS = 1000
EFFECT_GATE = 0.02
assert len(S3) == len(S5) == 5


def build_lines(items, leaves, parser, policy):
    lines = []
    visible = parsed = 0
    for it in items:
        if it["leaf"] not in leaves:
            continue
        for li, toks in enumerate(it["lines"]):
            a = []
            b = []
            for tok in toks:
                visible += 1
                p = parser.pick(tok, policy)
                if p is None:
                    continue
                vals = p[1]
                try:
                    a.append(I3[vals[3]])
                    b.append(I5[vals[5]])
                except KeyError as ex:
                    raise RuntimeError(f"unexpected slot3/slot5 state in {tok!r}: {ex}") from ex
                parsed += 1
            if a:
                lines.append({
                    "leaf": int(it["leaf"]),
                    "page": it["page"],
                    "paragraph": it["id"],
                    "line_index": int(li),
                    "s3": np.asarray(a, dtype=np.uint8),
                    "s5": np.asarray(b, dtype=np.uint8),
                })
    return lines, {
        "visible_tokens": int(visible),
        "parsed_tokens": int(parsed),
        "parse_coverage": parsed / visible if visible else 0.0,
        "physical_lines_with_parsed_tokens": len(lines),
        "singleton_parsed_lines": int(sum(len(x["s3"]) == 1 for x in lines)),
        "movable_lines": int(sum(len(x["s3"]) >= 2 for x in lines)),
        "movable_tokens": int(sum(len(x["s3"]) for x in lines if len(x["s3"]) >= 2)),
    }


def add_pairs(C, s3, s5):
    idx = s3.astype(np.int64) * 5 + s5.astype(np.int64)
    C += np.bincount(idx, minlength=25).reshape(5, 5)


def counts_by_fold(lines, leaf_to_fold):
    out = np.zeros((5, 5, 5), dtype=np.int64)
    for r in lines:
        f = leaf_to_fold[r["leaf"]]
        add_pairs(out[f], r["s3"], r["s5"])
    return out


def probs_from_train(C):
    C = C.astype(np.float64)
    n = float(C.sum())
    row = C.sum(axis=1)
    col = C.sum(axis=0)
    p3 = (row + ALPHA) / (n + 5 * ALPHA)
    p5 = (col + ALPHA) / (n + 5 * ALPHA)
    p5g3 = (C + ALPHA) / (row[:, None] + 5 * ALPHA)
    p3g5 = (C + ALPHA) / (col[None, :] + 5 * ALPHA)
    return p3, p5, p5g3, p3g5


def held_gain(train, held):
    p3, p5, p5g3, p3g5 = probs_from_train(train)
    H = held.astype(np.float64)
    n = float(H.sum())
    if n <= 0:
        raise RuntimeError("empty held contingency")
    ce5 = -float((H * np.log2(p5[None, :])).sum() / n)
    ce5c = -float((H * np.log2(p5g3)).sum() / n)
    ce3 = -float((H * np.log2(p3[:, None])).sum() / n)
    ce3c = -float((H * np.log2(p3g5)).sum() / n)
    g5 = ce5 - ce5c
    g3 = ce3 - ce3c
    return {
        "held_tokens": int(n),
        "ce_slot5_marginal": ce5,
        "ce_slot5_given_slot3": ce5c,
        "gain_slot5_from_slot3": g5,
        "ce_slot3_marginal": ce3,
        "ce_slot3_given_slot5": ce3c,
        "gain_slot3_from_slot5": g3,
        "symmetric_gain": (g3 + g5) / 2.0,
    }


def crossfit_from_fold_counts(F):
    total = F.sum(axis=0)
    rows = []
    for f in range(5):
        rows.append({"fold": f, **held_gain(total - F[f], F[f])})
    mean = float(statistics.fmean(x["symmetric_gain"] for x in rows))
    n = sum(x["held_tokens"] for x in rows)
    pooled = sum(x["symmetric_gain"] * x["held_tokens"] for x in rows) / n
    return {
        "folds": rows,
        "equal_weight_mean_symmetric_gain": mean,
        "occurrence_weighted_symmetric_gain": float(pooled),
        "all_five_positive": all(x["symmetric_gain"] > 0 for x in rows),
    }


def empirical_stats(C):
    C = C.astype(np.float64)
    n = float(C.sum())
    p = C / n
    pr = p.sum(axis=1)
    pc = p.sum(axis=0)
    mi = 0.0
    for i in range(5):
        for j in range(5):
            if p[i, j] > 0 and pr[i] > 0 and pc[j] > 0:
                mi += float(p[i, j] * math.log2(p[i, j] / (pr[i] * pc[j])))
    expected = np.outer(C.sum(axis=1), C.sum(axis=0)) / n
    chi2 = float(np.where(expected > 0, (C - expected) ** 2 / expected, 0.0).sum())
    v = math.sqrt(chi2 / (n * 4.0))
    p5g3 = np.divide(C, C.sum(axis=1)[:, None], out=np.zeros_like(C), where=C.sum(axis=1)[:, None] > 0)
    p3g5 = np.divide(C, C.sum(axis=0)[None, :], out=np.zeros_like(C), where=C.sum(axis=0)[None, :] > 0)
    return {
        "contingency": C.astype(np.int64).tolist(),
        "slot3_marginal": C.sum(axis=1).astype(np.int64).tolist(),
        "slot5_marginal": C.sum(axis=0).astype(np.int64).tolist(),
        "empirical_mutual_information_bits": float(mi),
        "cramers_v": float(v),
        "p_slot5_given_slot3": p5g3.tolist(),
        "p_slot3_given_slot5": p3g5.tolist(),
    }


def shuffled_fold_counts(lines, leaf_to_fold, null_index, mode):
    out = np.zeros((5, 5, 5), dtype=np.int64)
    for r in lines:
        s3 = r["s3"]
        s5 = r["s5"]
        n = len(s5)
        if n <= 1:
            z = s5
        elif mode == "shuffle":
            label = (
                f"Issue55A:WithinLineSlot5Shuffle:v1:{null_index}:"
                f"{r['page']}:{r['paragraph']}:{r['line_index']}"
            )
            rng = np.random.default_rng(e.stable_seed(label))
            z = s5.copy()
            rng.shuffle(z)
            if not np.array_equal(np.bincount(z, minlength=5), np.bincount(s5, minlength=5)):
                raise RuntimeError("within-line shuffle failed to preserve slot5 multiset")
        elif mode == "rotate":
            label = (
                f"Issue55A:WithinLineSlot5Rotate:v1:{null_index}:"
                f"{r['page']}:{r['paragraph']}:{r['line_index']}"
            )
            off = int(e.stable_seed(label) % (n - 1)) + 1
            z = np.roll(s5, off)
            if not np.array_equal(np.bincount(z, minlength=5), np.bincount(s5, minlength=5)):
                raise RuntimeError("within-line rotate failed to preserve slot5 multiset")
        else:
            raise ValueError(mode)
        add_pairs(out[leaf_to_fold[r["leaf"]]], s3, z)
    return out


def quantile(xs, q):
    return float(np.quantile(np.asarray(xs, dtype=np.float64), q))


def null_audit(lines, leaf_to_fold, real_mean, mode):
    vals = []
    positive_fold_counts = []
    for n in range(N_NULLS):
        F = shuffled_fold_counts(lines, leaf_to_fold, n, mode)
        cf = crossfit_from_fold_counts(F)
        vals.append(cf["equal_weight_mean_symmetric_gain"])
        positive_fold_counts.append(sum(x["symmetric_gain"] > 0 for x in cf["folds"]))
        if (n + 1) % 100 == 0:
            print(f"{mode}_nulls={n+1}/{N_NULLS}", file=sys.stderr, flush=True)
    upper = sum(x >= real_mean for x in vals)
    p = (1 + upper) / (N_NULLS + 1)
    med = float(statistics.median(vals))
    return {
        "null_count": N_NULLS,
        "upper_tail_count": int(upper),
        "upper_tail_p": float(p),
        "median_mean_symmetric_gain": med,
        "q05": quantile(vals, 0.05),
        "q95": quantile(vals, 0.95),
        "minimum": float(min(vals)),
        "maximum": float(max(vals)),
        "real_advantage_over_null_median": float(real_mean - med),
        "positive_fold_count_distribution": {
            str(k): int(v) for k, v in sorted(Counter(positive_fold_counts).items())
        },
    }


def run_policy(items, folds, parser, policy):
    universe = set().union(*folds)
    leaf_to_fold = {}
    for f, leaves in enumerate(folds):
        for leaf in leaves:
            leaf_to_fold[int(leaf)] = f
    lines, pop = build_lines(items, universe, parser, policy)
    realF = counts_by_fold(lines, leaf_to_fold)
    real = crossfit_from_fold_counts(realF)
    desc = empirical_stats(realF.sum(axis=0))
    primary = null_audit(lines, leaf_to_fold, real["equal_weight_mean_symmetric_gain"], "shuffle")
    rotate = null_audit(lines, leaf_to_fold, real["equal_weight_mean_symmetric_gain"], "rotate")
    return {
        "policy": policy,
        "population": pop,
        "real": real,
        "descriptive": desc,
        "within_line_shuffle_null": primary,
        "within_line_cyclic_shift_sensitivity": rotate,
    }


def classify(primary):
    real = primary["real"]
    null = primary["within_line_shuffle_null"]
    p_pass = null["upper_tail_p"] <= 0.01
    effect_pass = null["real_advantage_over_null_median"] >= EFFECT_GATE
    folds_pass = real["all_five_positive"]
    if folds_pass and p_pass and effect_pass:
        c = "CROSS-LEAF SLOT3xSLOT5 DEPENDENCE"
    elif p_pass and not effect_pass:
        c = "STATISTICALLY DETECTABLE BUT SMALL SLOT3xSLOT5 DEPENDENCE"
    else:
        c = "NO CROSS-LEAF SLOT3xSLOT5 DEPENDENCE BEYOND LINE MARGINALS"
    return c, {
        "all_five_held_folds_positive": bool(folds_pass),
        "within_line_shuffle_p_le_0_01": bool(p_pass),
        "real_advantage_over_null_median_ge_0_02_bits": bool(effect_pass),
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
    if len(folds) != 5:
        raise RuntimeError("expected five physical-leaf folds")
    parser = e.SlotParser()
    validation = e.validate_parser(parser)

    primary = run_policy(items, folds, parser, "min")
    classification, gates = classify(primary)
    sensitivity = run_policy(items, folds, parser, "max")

    out = {
        "experiment": "Issue55A hypothesis-neutral slot3xslot5 dependency audit",
        "classification": classification,
        "gates": gates,
        "primary_min": primary,
        "max_sensitivity": sensitivity,
        "state_order": {"slot3": list(S3), "slot5": list(S5)},
        "smoothing_alpha": ALPHA,
        "null_count_per_family": N_NULLS,
        "effect_gate_bits_per_token": EFFECT_GATE,
        "parser_validation": validation,
        "source": {"zl3b_git_blob": blob},
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
