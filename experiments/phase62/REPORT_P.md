# Phase 62P — H62-P1 prospective result

Status: **complete — prospective support for frozen A1 relative to tested N0/C0 baselines**.

This is the first result in the current model-family tournament whose target geometry was sealed before the exposed-score ranking was known.

## Chronology / audit trail

The ordering was preserved:

1. Phase62A froze H62-P1 before N0/C0/A1 tournament outcomes.
2. Phase62B/C produced exposed S1–S3 results.
3. Phase62D committed the exposed-score ranking `A1 > C0 > N0` while keeping the overall mechanism-family conclusion unresolved.
4. `IMPLEMENTATION_P.md`, the missing-bin rule, and `phase62p_h62p1.py` were committed before the first H62-P1 run.
5. Only then did PR #11 trigger the first prospective reveal.

First reveal:

- workflow run: `33314854583`
- head before result: `bdcf313198206ec7b2801dbd3c69f87ed5495a81`
- artifact ID: `9733130140`
- artifact ZIP SHA-256: `a54172cbb8ecbd783b3e2a5f323ded87b313de2afe3cab94ae52ec447ca56441`
- raw result JSON SHA-256: `0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264`

A second run used the unchanged scientific executable and required the raw result JSON to match that first-reveal SHA-256 exactly before persisting it in the repository. The digest check passed and the exact result is now `phase62p_h62p1_results.json`.

Pinned external inputs remained:

- ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- CREMMA commit `292525969ad98380b398e6606a9c2a36d51913ae`.

The result records the already-merged Phase62D decision blob `74441ebd1342f8eec944bd7df9d38d870b35eb60`.

## What H62-P1 tests

Within each eligible paragraph/item, near-family recurrence excess was measured in five preceding-token distance bins:

- B1: 1–2;
- B2: 3–5;
- B3: 6–10;
- B4: 11–20;
- B5: 21–40.

Each bin is corrected by a 100-replicate within-item token-order permutation null. The signed excess vector is L1-normalized.

Two primary diagnostics were frozen:

1. `D_profile` — L1 distance between candidate and held-out Voynich normalized five-bin profiles;
2. absolute difference in `C_short`, where `C_short` is signed excess concentration in B1–B3 (1–10 tokens).

Lower is better for both. No weighted combination was permitted.

Mechanistic relevance was frozen before reveal: A1 directly draws local-family variants from at most the preceding 10 generated tokens, so it predicts stronger 1–10 concentration than 11–40. It does not predict a literal zero after distance 10 because chained generation can transmit longer-range effects.

## Frozen prospective leader rule

A candidate could be called the prospective profile leader only if the same candidate simultaneously had:

- lowest mean `D_profile`;
- lowest median `D_profile`;
- unique `D_profile` win in at least 3/5 folds;
- lowest mean absolute `C_short` difference;
- unique `C_short` win in at least 3/5 folds.

No condition was added after the result.

## Result

| candidate | mean D_profile | median D_profile | D wins | mean |C_short diff| | C_short wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

Frozen verdict:

> **A1 is the H62-P1 prospective profile leader among the tested N0/C0/A1 candidates.**

This satisfies every preregistered prospective-leader condition.

## Fold-level result

| fold | Voynich C_short | N0 D | C0 D | A1 D | N0 |Cdiff| | C0 |Cdiff| | A1 |Cdiff| | both winners |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 0 | 0.73139 | 1.47481 | 1.81574 | **0.53607** | 0.76830 | 1.43845 | **0.26804** | A1 |
| 1 | 0.45802 | 1.78218 | 1.94667 | **0.56531** | 0.49493 | 1.16508 | **0.03659** | A1 |
| 2 | 0.46382 | 1.48697 | 1.94667 | **0.81061** | 0.50073 | 1.17088 | **0.01339** | A1 |
| 3 | 0.78823 | 1.47990 | 1.87201 | **0.88614** | 0.82514 | 1.49529 | **0.23130** | A1 |
| 4 | 0.56151 | 1.42527 | 1.71223 | **1.01480** | 0.59842 | 1.26856 | **0.03144** | A1 |

A1 uniquely wins **both** frozen diagnostics in every physical-leaf fold.

Neither N0 nor C0 beats A1 in a single fold on either metric.

## Profile geometry

### N0

Equal-manuscript excess vector:

`[+0.00730, -0.00372, -0.00426, -0.00079, +0.00247]`

Normalized profile:

`[+0.394, -0.201, -0.230, -0.042, +0.133]`

`C_short = -0.0369`

Thus the objective source-native medieval panel does not show the strong positive short-range concentration seen in Voynich.

### C0

Selected digraph-coding excess vector:

`[+0.00025, -0.00551, -0.00133, -0.00114, +0.00109]`

Normalized profile:

`[+0.0267, -0.5908, -0.1429, -0.1224, +0.1172]`

`C_short = -0.7071`

The C0 transform that improved the exposed S1–S3 joint error actually performs worse than N0 on this unseen recurrence-profile geometry. This is important evidence that its exposed-score improvement was not a general solution to Voynich locality.

### A1

Across the five held-out folds, A1 `C_short` is approximately:

- 0.463
- 0.495
- 0.477
- 0.557
- 0.530

Voynich held-out `C_short` is approximately:

- 0.731
- 0.458
- 0.464
- 0.788
- 0.562

A1 captures the **direction and concentration scale** of the short-range recurrence geometry far better than N0/C0.

It does not reproduce the full five-bin profile exactly. Its fold `D_profile` values remain `0.536–1.015`, not near zero. In particular, A1 generally produces negative B4/B5 excess, while some Voynich folds retain positive or mixed longer-range excess. The prospective result therefore supports the frozen local mechanism without establishing full structural equivalence.

## Scientific interpretation

This result materially changes the evidential status of A1.

Before H62-P1:

> A1 was the strongest fit on exposed statistics that had influenced model construction or evaluation design.

After H62-P1:

> **The frozen A1 mechanism predicts a previously sealed distance-dependent near-family recurrence geometry substantially better than the tested N0 and C0 baselines, with 5/5 fold wins on both preregistered diagnostics.**

This is genuine **prospective structural support** for the mechanism class represented by A1.

It is stronger than another exposed-statistic fit because:

- H62-P1 was frozen in Phase62A;
- Phase62D ranking and mechanistic prediction were committed before reveal;
- executable, aggregation, missing-bin handling and victory rule were committed before the first run;
- no A1 parameter was retuned;
- no C0 transform was reselected;
- no replacement holdout was used.

## What this does not establish

Do **not** infer:

- that the Voynich Manuscript is meaningless;
- that A1 is the historical production process;
- that its symbols have no semantic content;
- that meaningful text plus a more complex cipher/shorthand is falsified;
- that A1 reproduces the full line-position profile;
- that the empirical Voynich vocabulary supplied to A1 is an innocuous assumption.

A1 still pays substantial target-dependence cost:

- explicit paragraph-entry mechanism informed by Voynich structure;
- explicit local-family mechanism;
- maximum local memory of 10;
- parameters selected on Voynich training folds;
- empirical Voynich vocabulary of 8,295 token types;
- no independently meaningful plaintext or historically grounded generation process.

The training-vocabulary-only Phase61C sensitivity reduces one leakage concern, but H62-P1 has not yet been repeated under a training-only-vocabulary output constraint or an independent transcription lineage.

## Phase62 conclusion

The first fair tournament now has two layers of evidence:

### Exposed scorecard

`A1 > C0 > N0`

### Sealed prospective H62-P1

`A1` uniquely leads; N0/C0 record 0/5 wins on both prospective diagnostics.

Therefore A1 is promoted from:

> provisional leading exposed-score structural candidate

to:

> **leading tested structural mechanism with genuine prospective support**.

The overall manuscript-mechanism question remains below semantic/historical identification. The correct next step is not an A2 repair. It is to challenge whether A1's prospective advantage survives reductions in target dependence and independent representation/transcription replication.