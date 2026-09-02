# Issue #75 Phase B — pretarget execution freeze / M2 first-reveal authorization

Date: 2026-09-01  
Status: **TARGET-BLIND EXECUTION VALIDATED; 31-CASE M2 FIRST REVEAL AUTHORIZED**

## Frozen scientific design

- Phase-B plan: `PLAN_B.md`
- plan commit: `f09ba414de015eabd1eef03f275be68b82752d7f`
- M2-KRS target-blind generator commit: `1c88e05f17cebad5c8fbbe8102d22439ab3724e3`
- Phase-B scorer commit: `6b09b2870b7693a9f098f51803363d75ae9674ef`
- Phase-B aggregator commit: `3bb949c926b9cef90fd56c9c7027ddb28c44db18`
- implementation freeze commit: `61dd252fa7e07c0de34b7f319dfe38e9ec6efb0d`

## Target-blind B0 authority

- successful run: `33503712565`
- permanent authority commit: `591accc7105e96ddd2b172c8d8c0f54fc0b7f4c1`
- authority SHA-256: `9c180c7026e4f9464954dd029b71973cc1890f25223af6152959649dde57e834`
- 31/31 M2-KRS corpora frozen before target access
- no drops / no rerolls

## Exact-replay preflight

Workflow run `33503957561` completed `success` at head:

`a0efaa67b91cf39d75d7da02fef8c23f9a35c6de`

Both preregistered boundary cases passed:

- M2-KRS rep0
- M2-KRS rep30

For both cases:

- source/parser/fold authority matched;
- training slot marginals matched B0;
- K/R/S descriptor support/counts/probabilities matched B0;
- refit error remained `<=1e-10`;
- exact generated occupancy SHA matched B0;
- target access remained entirely false.

## Candidate-owned null execution smoke

Wrapper commit:

`d2c85c05b337fa8f6cd86bdd9f62d81a1ac6c403`

Workflow run `33504179109` completed `success` at head:

`97f56cac6d3be7cb5d3254d46e0c79d9eda848d3`

For exact rep0, the frozen M2 measurement machinery completed:

- all 66 candidate pair-Q values;
- 1000 candidate-owned reference line-local nulls;
- residual Z;
- five-fold residual reliability;
- 1000 independent candidate-owned test nulls;
- residual energy and `p_exist`.

It deliberately never called the target loader.

Smoke artifact:

- ID `9798963232`
- digest `sha256:141a2083b849c881dbcbba1c0965614217823f00ad8f4c0ef74de428c6661aa2`

Smoke E/p/W are implementation diagnostics only and are not used to alter the frozen model, tolerance or first-reveal population.

## Frozen Phase-A comparison authority

Phase B reuses the permanent Phase-A positive-control aggregate without rerunning/reselecting it:

- aggregate SHA-256 `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`
- M+ calibration already valid
- 31 frozen paired `T_plus_center` values
- q95 `delta_plus = 0.009768313008182594`

Primary Phase-B decision remains:

`gap_M2 = median(T_M2[r] - T_plus_center_PhaseA[r])`

- `gap_M2 >= -0.009768313008182594` -> `M2_GENERIC_KRS_SHAPE_DESCRIPTORS_SUFFICIENT`
- otherwise -> `M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED`

## First-reveal authorization

The next licensed action is exactly one complete 31-case M2-KRS first reveal, reps `0..30`.

Every case must:

1. regenerate and match its exact Phase-B0 occupancy SHA;
2. execute the frozen candidate-owned 1000-reference/1000-test calibration;
3. only then load the unchanged frozen ZL3b and IT2a target vectors;
4. score both readings separately and set `T=min(R_ZL3b,R_IT2a)`;
5. be retained regardless of result.

After first reveal starts, no target-dependent change is licensed to the M2 model, descriptor set, fit rule, seed namespaces, B0 corpus identities, null laws, targets, Phase-A positive-control authority, q95 tolerance or decision mapping.

M3 remains unimplemented and unlicensed until the frozen M2 result is permanently archived and classified.
