# Phase 61C inductive-vocabulary sensitivity audit

Date: 2026-08-30

Status: audit-only; no accepted Phase61C file on `main` is modified.

## Question

The frozen Phase61C implementation performs training-only feature scaling, direction estimation and parameter selection, but shares the empirical full-manuscript token-type vocabulary across outer folds. Does A1 still survive if the generator in each fold may use **only token types observed on training physical leaves**?

This is a stricter inductive sensitivity test, not a rewrite of the frozen preregistration.

## Method

For each of the same five physical-leaf folds:

- reconstruct the token vocabulary from training leaves only;
- reconstruct the edit-distance-1 neighbor graph from that training vocabulary only;
- learn entry-shape scores from training leaves only;
- perform the same 16-pair parameter grid search using training data only;
- evaluate the selected pair on the held-out leaf layout using five deterministic replicates;
- retain the frozen `[0.5, 2.0]` broad-regime gate on entry projection, local-prev10, and line-position eta2 mean.

Input Git blob SHA-1:

`2a4533ab9bdfa85db9bad602d590978953055df1`

## Result

A1 **survives** the stricter inductive-vocabulary sensitivity.

### Ratio of generated held-out mean to real held-out mean

| primary target | frozen Phase61C | training-vocabulary-only audit |
|---|---:|---:|
| entry projection | 0.7969 | 0.7947 |
| local-prev10 fraction | 0.7169 | 0.7181 |
| line-position eta2 mean | 1.1163 | 1.0981 |

All three remain inside the frozen `[0.5, 2.0]` survival regime.

The selected parameter pair is unchanged in every fold:

- fold 0: entry strength 0.5, local-family p 0.2
- fold 1: entry strength 0.5, local-family p 0.2
- fold 2: entry strength 0.5, local-family p 0.3
- fold 3: entry strength 0.5, local-family p 0.3
- fold 4: entry strength 0.5, local-family p 0.2

### Held-out vocabulary novelty

The stricter condition is nontrivial. Roughly 48–50% of held-out token **types** are absent from the corresponding training vocabulary, representing roughly 19–21% of held-out token **occurrences**. Despite removing all of those held-out-only types from the generator's available vocabulary, the primary gate ratios are almost unchanged.

Per-fold unseen type fractions:

`[0.4791, 0.4984, 0.4910, 0.5034, 0.4866]`

Per-fold unseen token fractions:

`[0.2056, 0.2055, 0.1907, 0.1929, 0.1974]`

## Decision

The full-manuscript vocabulary sharing in the frozen Phase61C implementation is **not driving the Phase61C survival decision** on the three primary targets.

The stricter result supports the same limited conclusion:

> A1 remains a viable structural generator after paying for one local-family activation mechanism. This is not evidence that the manuscript is meaningless and does not establish A1 as a historical generator.

The result also strengthens the case for freezing A1 and proceeding to the fair N0/B0/G comparison rather than introducing A2.

## Audit provenance

Workflow run: `33312218285`

Artifact: `phase61c-inductive-vocab-audit`

Audit executable: `audits/phase61c_inductive_vocab_audit.py`
