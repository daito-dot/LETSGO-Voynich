# Issue26E16 pre-reveal performance amendment

Status: **FROZEN WHILE FIRST E16 RUN WAS STILL IN PROGRESS, BEFORE ANY E16 RESULT/JSON/SUMMARY WAS EMITTED**

Parent plan: `PLAN_E16.md` at `397d6393164b37436c7dab24726884d5edc591d9`.

The first executable/workflow used the frozen scientific design literally but recomputed 200 × 90 candidate-key null fits through deeply nested Python run/key loops. During that still-running workflow, before any E16 output had been emitted, this was recognized as an avoidable computational implementation cost.

This amendment changes **performance only**.

Unchanged scientific authority:

- same five candidate slots `1,2,4,7,8`;
- same raw state orders;
- same 3! state→duration permutations;
- same phases `0,1,2`;
- same 90-key complete search;
- same five physical-leaf folds;
- same training objective and tie order;
- same invalid codes `220/221/222`;
- same CREMMA model;
- same 200 nulls;
- same within-run ternary-state shuffle;
- same seed namespace `Issue26E16:TernaryShuffle:v1:<null>:<slot>:<paragraph_id>:<run_index>`;
- same full independent refit for every null/fold;
- same statistics, gates, thresholds, and classifications.

## Vectorized implementation

The optimized runner may batch the 200 null realizations for each run and compute the six state permutations simultaneously. It may aggregate per-leaf sufficient statistics before performing the identical five-fold 90-key selection.

This is algebraically equivalent to calling the original `stats_one` / `fit_population` loop independently for every null.

## Mandatory equivalence gate

Before the vectorized null tournament is accepted, null index `0` must also be generated and fitted through the original slow code path.

The optimized and original null-0 outputs must agree on:

- pooled held-out CE within `1e-12`;
- pooled valid-group fraction within `1e-12`;
- exact-key recurrence exactly;
- each fold's selected `(slot, phase, permutation)` exactly;
- each fold's held group count, invalid count, scored-character count exactly;
- each fold's held NLL within `1e-10`.

If any equivalence check fails, classification is **`E16 OPTIMIZATION EQUIVALENCE FAILURE`** and the vectorized null results have no scientific authority.

No target result, selected key, null statistic, or decoded text was available when this amendment was frozen.
