# Phase 63A — A1 training-only-vocabulary robustness challenge

Status: **frozen before execution**.

Phase62P gave the frozen A1 mechanism genuine prospective support on H62-P1. Phase63A does not add a new mechanism and does not seek another favorable statistic. It removes one major target-derived convenience: access to token types seen only on the held-out physical leaves.

## Scientific question

> Does A1 retain both its exposed Phase62 structural gate and its H62-P1 advantage when each held-out fold can generate only token types observed on its training leaves?

This is a **target-dependence robustness test**, not a new prospective holdout. H62-P1 is already known; the freedom being frozen here is the intervention and its success criterion.

## Frozen candidate — A1-R1

For each of the existing five physical-leaf folds:

1. training paragraphs = all paragraphs outside the held-out physical leaves;
2. output vocabulary = unique token types in training paragraphs only;
3. edit-distance-1 neighbor graph = constructed from that training-only vocabulary only;
4. entry shape scores = learned from training paragraphs only and evaluated only over training vocabulary;
5. held-out layout = exact original held-out paragraph/line/token-count layout, with no held-out token identity used by generation;
6. Phase61C parameter pair is unchanged:
   - fold0 `.5 / .20`
   - fold1 `.5 / .20`
   - fold2 `.5 / .30`
   - fold3 `.5 / .30`
   - fold4 `.5 / .20`;
7. five held-out seeds are exactly the Phase62C/62P seeds;
8. no parameter, vocabulary rule, shape rule, memory horizon or generation rule is reselected.

The only intended scientific difference from full-vocabulary A1 is removal of token types absent from the fold's training leaves.

## Leakage audit

The executable must explicitly verify that every generated token belongs to the fold's training vocabulary.

For each held-out fold report:

- training vocabulary type count;
- held-out observed type count;
- number/fraction of held-out observed types absent from training vocabulary;
- number/fraction of held-out token occurrences whose type is absent from training vocabulary;
- full-manuscript vocabulary count for reference only.

These coverage statistics are diagnostics, not tuning inputs.

## Exposed common-score replay

Use the exact Phase62 S1/S2/S3 implementation and the same held-out Voynich targets.

For every A1-R1 realization:

- S1 uses the Phase62 fold training SD and direction;
- S2 uses the exact Phase62B null algorithm with a neighbor map built from the training-only generator vocabulary; because all generated tokens belong to that vocabulary, no held-out token relation can enter the generator score;
- S3 uses the exact generic fixed-five 8D line-position eta2 implementation.

Average the same five deterministic realizations within each fold, then compute across-fold ratio-of-means against held-out Voynich exactly as Phase62C did.

No new exposed metric is added.

## H62-P1 robustness replay

Use the exact committed H62-P1 implementation from Phase62P:

- bins `1–2 / 3–5 / 6–10 / 11–20 / 21–40`;
- within-item 100-replicate permutation null;
- signed excess vector;
- normalize after averaging A1 replicate excess vectors;
- `D_profile` and absolute `C_short` difference remain the two diagnostics.

For A1-R1 replicate `r` in fold `f`, use the **same H62-P1 null entity label** `A1:fold{f}:rep{r}` used for full-vocabulary A1. This pairs permutation RNG streams/layout across the full-vocabulary and training-only variants and reduces Monte Carlo noise without changing either statistic.

Held-out Voynich profiles, N0 and selected C0 profiles are read from the committed exact Phase62P result. They are not recomputed or reselected.

## Frozen robustness survival rule

A1-R1 counts as **robust to held-out vocabulary removal** only if all of the following hold without retuning.

### R1 — exposed scalar retention

Across-fold ratio-of-means for all three Phase62 common targets remains in the historical interval `[0.5, 2.0]`:

- S1;
- S2;
- S3.

### R2 — H62-P1 mean superiority

A1-R1 has:

- lower mean `D_profile` than N0 **and** C0;
- lower mean absolute `C_short` difference than N0 **and** C0.

### R3 — H62-P1 fold-majority superiority

Against each baseline separately, A1-R1 wins at least 3/5 folds on:

- `D_profile`;
- absolute `C_short` difference.

All R1–R3 conditions must pass.

## Full-vocabulary A1 is a benchmark, not a gate

Report degradation/improvement relative to the committed full-vocabulary A1:

- change in S1/S2/S3 ratios;
- change in mean/median H62-P1 `D_profile`;
- change in mean absolute `C_short` difference;
- per-fold H62-P1 distance changes.

A1-R1 is **not required to beat full-vocabulary A1**. The scientific question is whether the prior advantage over N0/C0 survives when held-out-only token types are unavailable.

No post-result tolerance or degradation allowance may be added.

## Interpretation

### If A1-R1 survives

Promote:

> A1's exposed and prospective structural advantage does not depend on access to token types unique to the held-out physical leaves.

This reduces, but does not eliminate, target dependence. The generator still uses Voynich training-side token inventory/morphology, a Voynich-derived architecture and Voynich-selected parameters.

### If A1-R1 fails

Record:

> A1's current prospective advantage depends materially on manuscript-wide empirical vocabulary access.

Do not repair it in this phase. Any model that generates or learns missing morphology is a separately named more autonomous G model.

## Firewall

Phase63A forbids:

- A2 or any new generation mechanism;
- parameter re-selection;
- changing the 10-token memory;
- changing H62-P1 bins/null/normalization;
- C1 or C0 re-selection;
- dropping a bad fold;
- restoring held-out-only types after inspecting failure;
- replacing the robustness criterion.

## Next decision

After Phase63A is recorded:

- if robust, prioritize independent transcription-lineage replication;
- if not robust, record target-dependence failure before considering a more autonomous G architecture;
- either way, do not infer semantics or decipherment from this structural test.