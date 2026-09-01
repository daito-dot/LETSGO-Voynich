# Issue #72 V2 — Stage C1 aggregation implementation

Status: **FROZEN BEFORE FIRST C1 TARGET REVEAL**

Target-blind implementation preflight succeeded before this file was added:

- recovery preflight run: `33469256998`
- job: `99735460186`
- exact preflight head: `94403fc700adaa79bfa5e29343d0906e097163e8`
- artifact: `9785955003`
- artifact ZIP SHA-256: `aa99181070f56e335bcb9d655de500a6abb5e22ea70906372c91317bccb6924c`
- verified real-data reconstruction cases: `EL r0/r30`, `ES r0/r30`, `ET r0/r30`, `EG r0/r30`
- target loaded: false
- Q/residual-Z/target correlation computed: false

This file fixes mechanical aggregation details before any Stage C target result is seen.

## 1. Completeness before interpretation

The aggregate must contain exactly:

- 4 axes: EL, ES, ET, EG;
- 31 assignments per axis: r0..r30;
- 124 unique result JSON files total.

Duplicate `(axis,j)`, missing assignment, unexpected assignment or unexpected axis is fatal.

Every result must:

- have status `STAGE C1 ASSIGNMENT TARGET SCORED`;
- name the same exact first-reveal scientific head;
- carry exact C0 raw/gzip/manifest identities;
- carry the expected frozen target authority;
- state `hard_intervention_threshold_applied=false`;
- state `readings_averaged=false`;
- state `coverage_gate_applied=false`.

Aggregation may not omit a result based on its scientific value.

## 2. Quantile implementation

For each 31-value axis × reading `DELTA_R` vector, report:

- minimum;
- Q1 = NumPy `quantile(x, 0.25, method="linear")`;
- median = NumPy `quantile(x, 0.50, method="linear")`;
- Q3 = NumPy `quantile(x, 0.75, method="linear")`;
- maximum;
- arithmetic mean.

The quantile implementation is descriptive only. No quantile is a hard scientific threshold.

## 3. Sign counts

For exact floating results:

- negative: `DELTA_R < 0`;
- zero: `DELTA_R == 0`;
- positive: `DELTA_R > 0`.

Do not introduce an epsilon that turns small observed effects into zero after seeing results.

For each axis additionally report assignment-level reading agreement:

- `both_negative`: both ZL3b and IT2a delta < 0;
- `both_nonnegative`: both >= 0;
- `mixed`: all other combinations.

These three counts must sum to 31.

## 4. Rank evidence

For each axis × reading:

`nonloss_count = count(DELTA_R >= 0)`

`rank_nonloss = (1 + nonloss_count) / 32`

Report both exact count and fraction.

Per the preregistered scoring amendment, this is sampled-assignment rank evidence, not a classical exact permutation p-value and not a `.05` gate.

## 5. Representation/support context

For each axis aggregate from the already-carried C0 metadata:

- randomized full parser coverage min/median/max;
- common-support fraction min/median/max;
- common-support token count min/median/max.

These remain descriptive representation outcomes and may not rescue or negate the paired `DELTA_R` result.

## 6. Baseline and randomized topology context

For each axis × reading separately report distributions of:

- baseline common-support R;
- randomized common-support R.

Do not average ZL3b and IT2a.

## 7. Exact raw evidence

The aggregate artifact must preserve:

- all 124 individual JSON files;
- aggregate JSON;
- SHA-256 of every individual result and aggregate;
- workflow/run/head provenance.

No first-reveal report may be written before the aggregate validates the complete 124-result population.
