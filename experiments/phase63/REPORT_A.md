# Phase 63A — training-only vocabulary robustness result

Status: **complete — A1-R1 survives every frozen robustness condition**.

Phase63A removes token types that occur only on held-out physical leaves from A1's output vocabulary. It introduces no new mechanism, does not retune parameters, and does not change H62-P1.

Exact result: `phase63a_training_vocab_results.json`.

## Frozen intervention

For each of the five physical-leaf folds:

- output vocabulary = token types observed on training leaves only;
- edit1 neighbor graph = training vocabulary only;
- entry shape scores = training paragraphs only;
- exact Phase61C fold parameter pair retained;
- exact Phase62C/62P held-out layout and five seeds retained;
- generated tokens are audited to belong to training vocabulary.

The held-out token strings are used only for coverage diagnostics and target evaluation, not as generation candidates.

## Frozen survival rule

A1-R1 survives only if all three conditions hold:

1. exposed Phase62 S1/S2/S3 ratio-of-means all remain in `[0.5,2.0]`;
2. H62-P1 mean profile distance and mean absolute `C_short` difference remain below both N0 and C0;
3. A1-R1 beats each baseline in at least 3/5 folds on each H62-P1 metric.

No degradation tolerance relative to full-vocabulary A1 was allowed after the result.

## Result — exposed common scorecard

A1-R1 / held-out Voynich ratio-of-means:

| target | full-vocabulary A1 | A1-R1 training-only vocabulary | frozen gate |
|---|---:|---:|---:|
| S1 entry projection | 0.62326 | **0.65353** | 0.5–2.0 |
| S2 locality excess | 1.51188 | **1.51061** | 0.5–2.0 |
| S3 aggregate line-position eta2 | 0.58738 | **0.58264** | 0.5–2.0 |

All three pass.

The difference from full-vocabulary A1 is negligible at the aggregate level:

- ΔS1 ratio: `+0.03027`;
- ΔS2 ratio: `-0.00127`;
- ΔS3 ratio: `-0.00474`.

As before, this is an across-fold aggregate gate, not a claim that every target passes in every individual fold. Fold heterogeneity remains visible and the Phase61 coordinate-profile mismatch remains binding.

## Result — H62-P1

A1-R1:

- mean `D_profile`: **0.76660**;
- median `D_profile`: **0.80945**;
- mean absolute `C_short` difference: **0.11769**.

Committed baselines from the sealed Phase62P result:

| candidate | mean D_profile | mean |ΔC_short| |
|---|---:|---:|
| N0 | 1.52982 | 0.63750 |
| C0 | 1.85866 | 1.30765 |
| full-vocabulary A1 | 0.76259 | 0.11615 |
| **A1-R1** | **0.76660** | **0.11769** |

A1-R1 beats:

- N0 on `D_profile`: **5/5 folds**;
- N0 on `|ΔC_short|`: **5/5 folds**;
- C0 on `D_profile`: **5/5 folds**;
- C0 on `|ΔC_short|`: **5/5 folds**.

All frozen R2/R3 conditions pass.

Relative to full-vocabulary A1, degradation is extremely small:

- mean `D_profile`: `+0.00401`;
- median `D_profile`: `-0.00116` (slightly better);
- mean `|ΔC_short|`: `+0.00153`.

Thus the H62-P1 advantage is essentially unchanged.

## How much held-out vocabulary was actually removed?

This was not a weak intervention.

Across folds:

- training vocabulary mean: **7,050.2 types** out of 8,295 full-manuscript types;
- mean held-out **type coverage** by training vocabulary: **0.5083**;
- mean held-out **token-occurrence coverage**: **0.8016**.

In other words, roughly **49% of distinct held-out token types** are unavailable to A1-R1, and about **20% of held-out token occurrences** use types absent from the training vocabulary in the real manuscript.

Every generated realization nevertheless contains **zero** token types outside the fold's training vocabulary by construction and audit.

## Frozen verdict

All three preregistered components pass:

- R1 exposed scalar retention: **PASS**;
- R2 H62-P1 mean superiority over N0/C0: **PASS**;
- R3 H62-P1 fold-majority superiority: **PASS**.

Therefore:

> **A1's exposed and prospective structural advantage does not depend on access to token types unique to the held-out physical leaves.**

This materially reduces one of the strongest target-leakage objections to the Phase62 result.

## Determinism audit

The first scientific run was deliberately retained as numerical authority:

- Actions run `33315453851`;
- job `99267937410`;
- artifact `9733309531`;
- artifact ZIP SHA-256 `d96a4362b16b77cafdf0addd031b9b5c1e293edbbe60d0aaedbd6f4a263ba60c`;
- raw result JSON SHA-256 `bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7`.

An attempted byte-identical clean replay triggered an audit because the raw SHA differed. A third unchanged scientific replay was structurally compared against the first.

Result of exact parsed-JSON diff:

- 16 differing scalar fields only;
- all are S1 floating-point projections or quantities directly derived from them;
- maximum absolute difference: `2.220446049250313e-16`;
- no string/integer/discrete differences;
- S2, S3, all H62-P1 values, all coverage/leakage fields and all pass/fail decisions are exactly identical.

After rounding floats to 14 decimal places and canonicalizing JSON key order, first and replay outputs share semantic SHA-256:

`cd53f47729c864badb5e8c747cfd9ad989de9c616ca54dd5bdcb83b075c33c74`

The apparent raw nondeterminism is therefore machine-precision cross-CPU floating reduction noise, not changed stochastic generation. See `DETERMINISM_AUDIT_A.md`.

The repository result file preserves the exact first-run artifact.

## What Phase63A changes scientifically

Before Phase63A, a major concern was:

> A1 may look successful because it is handed the manuscript-wide empirical token inventory, including types seen only on its held-out leaves.

After Phase63A:

> **That explanation is not supported. Removing held-out-only types — nearly half of held-out distinct types — leaves both the exposed scorecard and the previously prospective H62-P1 advantage essentially unchanged.**

This does **not** make A1 autonomous. It still receives:

- Voynich training-side vocabulary and morphology;
- an architecture derived from exposed Voynich phenomena;
- the frozen Voynich-selected entry-strength/local-family-p parameters;
- explicit paragraph-boundary knowledge;
- explicit 10-token local-family memory;
- the true held-out document layout/token counts.

It also still lacks independently meaningful plaintext and historical production evidence.

## Next question

Do not add A2 to improve the remaining profile mismatch.

The next high-value challenge is **independent transcription/segmentation replication**:

> Do the paragraph-entry, local-family recurrence geometry and A1 advantage survive when the target manuscript is represented by an independently maintained transcription lineage rather than ZL3b/EVA?

That test attacks a qualitatively different dependency and is more informative than another repair to the generator.