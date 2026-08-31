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
M = e11e.M
N_NULLS = 200
REAL_CE = 3.6860993911494533
REAL_STABILITY = 0.6219935480654878
REAL_RECURRENCE = 1
REPLAY_TOL = 1e-12


def clone_with_segment_shuffle(records, null_index: int):
    out = []
    for r in records:
        seq = r["seq"].copy()
        seed = base.seed32(
            f"Issue26E11F:SegmentShuffle:v1:{null_index}:{r['source_line']}:{r['segment_index']}"
        )
        rng = np.random.default_rng(seed)
        rng.shuffle(seq)

        # Preserve the original token-length vector exactly for diagnostics.
        lens = [len(t) for t in r["tokens"]]
        toks = []
        pos = 0
        for ln in lens:
            toks.append(seq[pos:pos + ln].copy())
            pos += ln
        if pos != len(seq):
            raise RuntimeError("token-length repartition mismatch")

        q = dict(r)
        q["seq"] = seq
        q["tokens"] = toks
        out.append(q)
    return out


def evaluate_population(records, folds, fam_counts, latin_freq, lm):
    keys = []
    held_rows = []
    max_score_discrepancy = 0.0
    for f, held_leaves in enumerate(folds):
        train = [r["seq"] for r in records if r["leaf"] not in held_leaves]
        held = [r["seq"] for r in records if r["leaf"] in held_leaves]
        key, fit = e11e.fit_freq_hill(train, latin_freq, lm.cost)
        if fit["score_discrepancy"] > max_score_discrepancy:
            max_score_discrepancy = fit["score_discrepancy"]
        ce, n = e11e.score_key(key, held, lm.cost)
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
    rec = Counter(tuple(int(x) for x in k) for k in keys)
    exact_recurrence = max(rec.values())
    return {
        "pooled_cross_entropy": float(pooled_ce),
        "mean_pairwise_occurrence_weighted_key_stability": float(stability),
        "exact_full_key_recurrence": int(exact_recurrence),
        "max_score_discrepancy": float(max_score_discrepancy),
        "folds": held_rows,
    }


def quantile(xs, q):
    return float(np.quantile(np.asarray(xs, dtype=np.float64), q))


def main():
    if len(sys.argv) != 3:
        print(f"usage: {sys.argv[0]} ZL3b-STA1.txt CREMMA_ROOT", file=sys.stderr)
        return 2

    sta = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    records, folds, fam_counts, sta_meta = e11e.parse_sta(sta)
    latin_runs, _, latin_meta = base.load_latin(root)
    lm = base.LM4(latin_runs)
    latin_freq = Counter("".join(latin_runs))
    baseline = base.latin_self_baseline(latin_runs)

    real = evaluate_population(records, folds, fam_counts, latin_freq, lm)
    replay = {
        "pooled_ce_abs_diff": abs(real["pooled_cross_entropy"] - REAL_CE),
        "stability_abs_diff": abs(real["mean_pairwise_occurrence_weighted_key_stability"] - REAL_STABILITY),
        "recurrence_matches": real["exact_full_key_recurrence"] == REAL_RECURRENCE,
    }
    replay_ok = (
        replay["pooled_ce_abs_diff"] <= REPLAY_TOL
        and replay["stability_abs_diff"] <= REPLAY_TOL
        and replay["recurrence_matches"]
        and real["max_score_discrepancy"] <= 1e-10
    )

    if not replay_ok:
        out = {
            "experiment": "Issue26E11F fully refitted STA-family order-null audit",
            "classification": "E11F REPLAY FAILURE",
            "replay": replay,
            "real": real,
            "sta_population": sta_meta,
            "latin_population": latin_meta,
        }
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
        print()
        return 0

    nulls = []
    for n in range(N_NULLS):
        shuffled = clone_with_segment_shuffle(records, n)
        row = evaluate_population(shuffled, folds, fam_counts, latin_freq, lm)
        row["null_index"] = n
        nulls.append(row)
        if (n + 1) % 10 == 0:
            print(f"completed_nulls={n + 1}/{N_NULLS}", file=sys.stderr, flush=True)

    ces = [x["pooled_cross_entropy"] for x in nulls]
    stabs = [x["mean_pairwise_occurrence_weighted_key_stability"] for x in nulls]
    recs = [x["exact_full_key_recurrence"] for x in nulls]

    lower_count = sum(x <= real["pooled_cross_entropy"] for x in ces)
    upper_stab_count = sum(x >= real["mean_pairwise_occurrence_weighted_key_stability"] for x in stabs)
    ce_p = (1 + lower_count) / (N_NULLS + 1)
    stab_p = (1 + upper_stab_count) / (N_NULLS + 1)
    ce_median = float(statistics.median(ces))
    stab_median = float(statistics.median(stabs))
    ce_advantage = ce_median - real["pooled_cross_entropy"]

    ce_gate1 = ce_p <= .01
    ce_gate2 = ce_advantage >= .10
    stability_gate = real["mean_pairwise_occurrence_weighted_key_stability"] > stab_median
    absolute_diversity_gate = 0.7746166938 <= baseline["top5_char_fraction"] + .15

    if not (ce_gate1 and ce_gate2):
        classification = "LATIN-LIKE CE EXPLAINED BY REFITTED ORDER NULLS"
    elif not stability_gate:
        classification = "ORDER-SPECIFIC BUT KEY-UNSTABLE"
    elif absolute_diversity_gate:
        classification = "ORDER-SPECIFIC LATIN-LIKENESS RESIDUAL"
    else:
        # The frozen plan has no positive class for CE+stability passing while
        # the already-frozen absolute diversity requirement fails. Do not
        # manufacture a stronger interpretation post reveal.
        classification = "ORDER-SPECIFIC BUT ABSOLUTE READABILITY GATE FAILS"

    summary = {
        "null_count": N_NULLS,
        "ce_lower_tail_count": int(lower_count),
        "ce_lower_tail_p": float(ce_p),
        "null_ce_median": ce_median,
        "null_ce_q05": quantile(ces, .05),
        "null_ce_min": float(min(ces)),
        "real_minus_null_median_ce": float(real["pooled_cross_entropy"] - ce_median),
        "real_ce_advantage_vs_null_median": float(ce_advantage),
        "stability_upper_tail_count": int(upper_stab_count),
        "stability_upper_tail_p": float(stab_p),
        "null_stability_median": stab_median,
        "null_stability_q95": quantile(stabs, .95),
        "null_stability_max": float(max(stabs)),
        "recurrence_distribution": {str(k): int(v) for k, v in sorted(Counter(recs).items())},
        "gates": {
            "real_ce_p_le_0_01": bool(ce_gate1),
            "real_ce_at_least_0_10_below_null_median": bool(ce_gate2),
            "real_stability_above_null_median": bool(stability_gate),
            "e11e_absolute_top5_within_latin_plus_0_15": bool(absolute_diversity_gate),
        },
    }

    out = {
        "experiment": "Issue26E11F fully refitted STA-family order-null audit",
        "classification": classification,
        "replay": replay,
        "real": real,
        "summary": summary,
        "nulls": nulls,
        "sta_population": sta_meta,
        "latin_population": latin_meta,
        "latin_self_baseline": baseline,
        "seed_namespace": "Issue26E11F:SegmentShuffle:v1:<n>:<source_line>:<segment_index>",
    }
    json.dump(out, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
