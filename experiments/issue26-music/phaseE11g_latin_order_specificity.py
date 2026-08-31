#!/usr/bin/env python3
from __future__ import annotations

import json
import statistics
import sys
from collections import Counter
from pathlib import Path

import numpy as np

import phaseE11e_leon_validated_reanalysis as e11e

base = e11e.base
ALPHABET = e11e.ALPHABET
A = len(ALPHABET)
M = e11e.M
ALPHA = 0.1
N_NULLS = 200
REAL_CE = 3.6860993911494533
PUBLISHED_REAL_SELF = 3.6903904874
REAL_CE_TOL = 1e-12
REAL_SELF_TOL = 1e-10
SEED_NAMESPACE = "Issue26E11G:LatinGlobalShuffle:v1:<null_index>"
assert A == 24 and M == 23


def quantile(xs, q):
    return float(np.quantile(np.asarray(xs, dtype=np.float64), q))


def evaluate_population(records, folds, fam_counts, latin_freq, lm_cost):
    keys = []
    held_rows = []
    max_score_discrepancy = 0.0
    for f, held_leaves in enumerate(folds):
        train = [r["seq"] for r in records if r["leaf"] not in held_leaves]
        held = [r["seq"] for r in records if r["leaf"] in held_leaves]
        key, fit = e11e.fit_freq_hill(train, latin_freq, lm_cost)
        max_score_discrepancy = max(max_score_discrepancy, fit["score_discrepancy"])
        ce, n = e11e.score_key(key, held, lm_cost)
        keys.append(key.copy())
        held_rows.append({
            "fold": f,
            "held_cross_entropy": float(ce),
            "held_scored_chars": int(n),
            "training_cross_entropy": float(fit["training_cross_entropy"]),
            "accepted_swaps": int(fit["accepted_swaps"]),
        })

    total_n = sum(x["held_scored_chars"] for x in held_rows)
    pooled_ce = sum(x["held_cross_entropy"] * x["held_scored_chars"] for x in held_rows) / total_n
    stability, _ = e11e.weighted_key_stability(keys, fam_counts)
    recurrence = Counter(tuple(int(x) for x in k) for k in keys)
    exact_recurrence = max(recurrence.values())
    return {
        "pooled_cross_entropy": float(pooled_ce),
        "mean_pairwise_occurrence_weighted_key_stability": float(stability),
        "exact_full_key_recurrence": int(exact_recurrence),
        "max_score_discrepancy": float(max_score_discrepancy),
        "folds": held_rows,
    }


def encode_latin_runs(runs):
    ai = {c: i for i, c in enumerate(ALPHABET)}
    encoded = [np.asarray([ai[c] for c in s], dtype=np.int16) for s in runs]
    lengths = np.asarray([len(x) for x in encoded], dtype=np.int64)
    flat = np.concatenate(encoded) if encoded else np.empty(0, dtype=np.int16)
    return encoded, lengths, flat


def c4_counts_for_runs(encoded_runs):
    by_fold = np.zeros((5, A ** 4), dtype=np.int64)
    for ri, xs in enumerate(encoded_runs):
        if len(xs) < 4:
            continue
        a = xs[:-3].astype(np.int64)
        b = xs[1:-2].astype(np.int64)
        c = xs[2:-1].astype(np.int64)
        d = xs[3:].astype(np.int64)
        q = (((a * A + b) * A + c) * A + d)
        by_fold[ri % 5] += np.bincount(q, minlength=A ** 4)
    return by_fold


def cost_from_c4(c4):
    c4m = np.asarray(c4, dtype=np.float64).reshape(A ** 3, A)
    c3 = c4m.sum(axis=1)
    den = c3[:, None] + ALPHA * A
    return (-np.log2((c4m + ALPHA) / den)).reshape(A ** 4)


def self_baseline_from_fold_c4(by_fold):
    total = by_fold.sum(axis=0)
    rows = []
    for f in range(5):
        held = by_fold[f]
        train = total - held
        cost = cost_from_c4(train)
        n = int(held.sum())
        ce = float(np.dot(held.astype(np.float64), cost) / n) if n else float("inf")
        rows.append({"fold": f, "cross_entropy": ce, "scored_chars": n})
    return {
        "mean_cross_entropy": float(statistics.fmean(r["cross_entropy"] for r in rows)),
        "folds": rows,
    }


def full_cost_and_self(encoded_runs):
    by_fold = c4_counts_for_runs(encoded_runs)
    total = by_fold.sum(axis=0)
    return cost_from_c4(total), self_baseline_from_fold_c4(by_fold)


def shuffled_runs(flat, lengths, null_index):
    seed = base.seed32(f"Issue26E11G:LatinGlobalShuffle:v1:{null_index}")
    rng = np.random.default_rng(seed)
    perm = flat.copy()
    rng.shuffle(perm)
    out = []
    pos = 0
    for ln in lengths:
        n = int(ln)
        out.append(perm[pos:pos + n].copy())
        pos += n
    if pos != len(perm):
        raise RuntimeError("run-length repartition mismatch")
    return out, perm


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-STA1.txt CREMMA_ROOT", file=sys.stderr)
        return 2

    sta = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()

    records, folds, fam_counts, sta_meta = e11e.parse_sta(sta)
    latin_runs, _, latin_meta = base.load_latin(root)
    latin_freq = Counter("".join(latin_runs))
    real_lm = base.LM4(latin_runs)
    real_self = base.latin_self_baseline(latin_runs)
    real = evaluate_population(records, folds, fam_counts, latin_freq, real_lm.cost)
    real_gap = real["pooled_cross_entropy"] - real_self["mean_cross_entropy"]

    replay = {
        "pooled_ce_abs_diff": abs(real["pooled_cross_entropy"] - REAL_CE),
        "self_baseline_abs_diff_from_published": abs(real_self["mean_cross_entropy"] - PUBLISHED_REAL_SELF),
        "max_score_discrepancy": real["max_score_discrepancy"],
    }
    replay_ok = (
        replay["pooled_ce_abs_diff"] <= REAL_CE_TOL
        and replay["self_baseline_abs_diff_from_published"] <= REAL_SELF_TOL
        and replay["max_score_discrepancy"] <= 1e-10
    )

    encoded_real, lengths, flat = encode_latin_runs(latin_runs)
    real_fast_cost, real_fast_self = full_cost_and_self(encoded_real)
    fast_replay = {
        "self_baseline_abs_diff_from_reference_implementation": abs(
            real_fast_self["mean_cross_entropy"] - real_self["mean_cross_entropy"]
        ),
        "full_cost_max_abs_diff": float(np.max(np.abs(real_fast_cost - real_lm.cost))),
    }
    replay_ok = replay_ok and fast_replay["self_baseline_abs_diff_from_reference_implementation"] <= 1e-12
    replay_ok = replay_ok and fast_replay["full_cost_max_abs_diff"] <= 1e-12

    if not replay_ok:
        out = {
            "experiment": "Issue26E11G Latin-order specificity audit",
            "classification": "E11G REPLAY FAILURE",
            "replay": replay,
            "fast_replay": fast_replay,
            "real": real,
            "real_self_baseline": real_self,
            "sta_population": sta_meta,
            "latin_population": latin_meta,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        print()
        return 0

    original_counts = np.bincount(flat.astype(np.int64), minlength=A)
    nulls = []
    for n in range(N_NULLS):
        runs, perm = shuffled_runs(flat, lengths, n)
        if not np.array_equal(np.bincount(perm.astype(np.int64), minlength=A), original_counts):
            raise RuntimeError(f"character multiset preservation failed for null {n}")
        if [len(x) for x in runs] != [int(x) for x in lengths]:
            raise RuntimeError(f"run-length preservation failed for null {n}")

        lm_cost, self_base = full_cost_and_self(runs)
        pop = evaluate_population(records, folds, fam_counts, latin_freq, lm_cost)
        gap = pop["pooled_cross_entropy"] - self_base["mean_cross_entropy"]
        nulls.append({
            "null_index": n,
            "pooled_cross_entropy": pop["pooled_cross_entropy"],
            "self_baseline_cross_entropy": self_base["mean_cross_entropy"],
            "normalized_gap": float(gap),
            "mean_pairwise_occurrence_weighted_key_stability": pop["mean_pairwise_occurrence_weighted_key_stability"],
            "exact_full_key_recurrence": pop["exact_full_key_recurrence"],
            "max_score_discrepancy": pop["max_score_discrepancy"],
        })
        if (n + 1) % 10 == 0:
            print(f"completed_nulls={n + 1}/{N_NULLS}", file=sys.stderr, flush=True)

    gaps = [x["normalized_gap"] for x in nulls]
    raw_ces = [x["pooled_cross_entropy"] for x in nulls]
    self_ces = [x["self_baseline_cross_entropy"] for x in nulls]
    stabs = [x["mean_pairwise_occurrence_weighted_key_stability"] for x in nulls]
    recs = [x["exact_full_key_recurrence"] for x in nulls]

    lower_count = sum(x <= real_gap for x in gaps)
    p = (1 + lower_count) / (N_NULLS + 1)
    gap_median = float(statistics.median(gaps))
    advantage = gap_median - real_gap
    gate_p = p <= .01
    gate_advantage = advantage >= .10
    classification = (
        "LATIN-ORDER-SPECIFIC NORMALIZED RESIDUAL"
        if gate_p and gate_advantage
        else "NO LATIN-ORDER SPECIFICITY UNDER FREQUENCY/RUN-LENGTH NULLS"
    )

    summary = {
        "null_count": N_NULLS,
        "real_normalized_gap": float(real_gap),
        "null_gap_lower_tail_count": int(lower_count),
        "null_gap_lower_tail_p": float(p),
        "null_gap_median": gap_median,
        "null_gap_q05": quantile(gaps, .05),
        "null_gap_q95": quantile(gaps, .95),
        "null_gap_min": float(min(gaps)),
        "null_gap_max": float(max(gaps)),
        "real_advantage_vs_null_gap_median": float(advantage),
        "null_raw_ce_median": float(statistics.median(raw_ces)),
        "null_raw_ce_q05": quantile(raw_ces, .05),
        "null_raw_ce_q95": quantile(raw_ces, .95),
        "null_self_ce_median": float(statistics.median(self_ces)),
        "null_self_ce_q05": quantile(self_ces, .05),
        "null_self_ce_q95": quantile(self_ces, .95),
        "null_stability_median": float(statistics.median(stabs)),
        "recurrence_distribution": {str(k): int(v) for k, v in sorted(Counter(recs).items())},
        "gates": {
            "lower_tail_p_le_0_01": bool(gate_p),
            "advantage_at_least_0_10_bits_per_char": bool(gate_advantage),
        },
    }

    out = {
        "experiment": "Issue26E11G Latin-order specificity audit",
        "classification": classification,
        "replay": replay,
        "fast_replay": fast_replay,
        "real": real,
        "real_self_baseline": real_self,
        "real_normalized_gap": float(real_gap),
        "summary": summary,
        "nulls": nulls,
        "sta_population": sta_meta,
        "latin_population": latin_meta,
        "preservation": {
            "character_multiset_exact": True,
            "ordered_run_length_vector_exact": True,
            "run_count": int(len(lengths)),
            "total_characters": int(len(flat)),
        },
        "seed_namespace": SEED_NAMESPACE,
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
