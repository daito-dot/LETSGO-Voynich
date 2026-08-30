# Phase 61C — implementation freeze

Status: frozen before any Phase61C held-out outcome is inspected.

This note resolves implementation details left open by `PLAN_C.md`. It does not change the allowed A1 architecture or parameter grids.

## Compatibility gate before fresh evaluation

The historical Phase61A/B executable was not preserved in the repository. Therefore the new Phase61C executable must first recompute the already-exposed Voynich-side Phase61B scorecard and remain in the same metric regime. If this compatibility gate fails, the script emits **no Phase61C scientific verdict**. Implementation corrections may then use only the already-exposed Phase61B diagnostics; held-out Phase61C results are not used for repair.

Reference Phase61B values:

- edit1 type density: 0.80374
- local-prev10 fraction: 0.09778
- line-position eta2 mean: 0.03115
- line-position eta2 max: 0.08810
- entry-vs-pseudo norm: 1.28505

The audit gate is intentionally tolerant because the exact historical diagnostic code is missing: relative error <=10% for edit1 density, <=30% for local-prev10, <=40% for line-position eta2 mean, and <=40% for entry/pseudo norm. The eta2 max is reported but is not an implementation gate.

## Parsing and split unit

- primary input: exact ZL3b/EVA v3b transcription, expected upstream Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`;
- P-coded prose only;
- explicit `<%>` markers define paragraph starts;
- outer split: five folds grouped by physical leaf number, so recto/verso stay together;
- no held-out leaf statistic is used for parameter selection.

## Frozen structural feature vector

Each eligible line is represented by the existing Phase60B-style 11-dimensional raw-EVA structural vector:

1. TTR;
2. mean token length;
3. token-length SD;
4. character inventory size;
5. character entropy;
6. first-character entropy;
7. last-character entropy;
8. within-line edit1-family fraction;
9. within-line previous-10 edit1 fraction;
10. k/t-containing token mass;
11. k share among k+t occurrences.

The real-entry-minus-internal-pseudo direction is learned on training leaves only. Line-position eta2 is measured over the same 11 features using paragraph line-index groups `0`, `1`, `2`, `3+`.

## A1 generator

The empirical Voynich prose token-type inventory is used as the shared output vocabulary. Consequently edit1 type density is explicitly **non-independent** and cannot count as a successful prediction.

### Body process

Ordinary body draws are uniform over the empirical token-type inventory. No section-specific grammar or explicit line-position mechanism is available.

### Entry mixture

On training leaves only, token shapes are defined as:

`(contains k or t, capped token length at 8, first character, last character)`.

A Laplace-smoothed entry-vs-body log-odds score is learned for each shape. Paragraph line0 draws from the same empirical type inventory with weights proportional to:

`exp(entry_strength * shape_log_odds)`.

Allowed `entry_strength`: `0.5, 1.0, 1.5, 2.0` only.

### Local-family body activation

From paragraph line1 onward, with probability `local_family_p`, the generator selects one of the previous ten generated tokens on the same physical leaf and emits a uniformly selected non-identical edit-distance-1 neighbor from the empirical inventory. If no such neighbor exists, it falls back to the ordinary body draw.

Allowed `local_family_p`: `0.05, 0.10, 0.20, 0.30` only.

The ten-token mechanism may transmit very short local dependence but introduces no persistent paragraph latent state.

## Model selection and stochastic replication

For each outer fold and each of the 16 frozen parameter pairs:

- run three deterministic stochastic replicates on training leaves;
- average the three primary targets;
- choose the pair minimizing mean squared relative error across:
  1. entry projection;
  2. local-prev10 fraction;
  3. line-position eta2 mean.

After selection, evaluate the chosen pair on held-out leaves with five deterministic replicates.

## Frozen broad-regime survival rule

A1 survives this first joint gate only if the across-fold mean generated/real ratio lies in `[0.5, 2.0]` for **all three** primary held-out targets:

- entry projection;
- local-prev10 fraction;
- line-position eta2 mean.

Otherwise A1 fails. Failure is frozen; do not create A2 before the N0/B0 comparison required by `ROADMAP.md`.

This is a structural generator test. Survival would not imply semantic emptiness or historical use of A1.