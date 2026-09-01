# Issue #75 Phase B — implementation freeze before target access

Date: 2026-09-01  
Status: **M2 SCORER / AGGREGATION FROZEN; NO PHASE-B TARGET SCORE YET**

Normative Phase-B plan:

- `PLAN_B.md`
- commit `f09ba414de015eabd1eef03f275be68b82752d7f`

Target-blind Phase B0:

- successful run `33503712565`
- generation/workflow head `9f01b5e964946a1a53a8ad9adb00eeaf1579252b`
- permanent authority commit `591accc7105e96ddd2b172c8d8c0f54fc0b7f4c1`
- `generator_authority.json` SHA-256 `9c180c7026e4f9464954dd029b71973cc1890f25223af6152959649dde57e834`
- 31/31 M2-KRS corpora frozen
- target access false
- drops `0`, rerolls `0`

Target-blind model-complexity diagnostics:

- nonzero `(K,R,S)` descriptor classes by training split: `110 / 112 / 111 / 111 / 112`;
- training distinct complete signatures: `611 / 601 / 595 / 602 / 610`;
- generated distinct signatures across reps: `1873..1946`;
- maximum slot-marginal fit error `6.106226635438361e-16`.

Thus M2 uses a coarse generic descriptor distribution substantially smaller than the empirical signature inventory and generates many signatures not literally observed in training. It is not an empirical-signature resampling model.

Frozen scorer:

- `phase75b_score.py`
- commit `6b09b2870b7693a9f098f51803363d75ae9674ef`

The scorer must verify:

1. exact B0 authority SHA;
2. exact source/parser/folds;
3. exact training slot marginals;
4. exact training K/R/S descriptor support/counts/probabilities;
5. refit error `<=1e-10`;
6. exact final generated occupancy SHA for the requested rep;
7. only then candidate-owned Q/Z/null calibration and target loading.

`--verify-only` stops before Q/Z and target access.

Frozen aggregation:

- `phase75b_aggregate.py`
- commit `3bb949c926b9cef90fd56c9c7027ddb28c44db18`

The aggregation does not rerun or select a new positive control. It loads the permanent Phase-A aggregate by exact SHA:

`fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

and reuses:

- all 31 frozen Phase-A `T_plus_center[r]` values;
- q95 `delta_plus = 0.009768313008182594`;
- already-passed M+ calibration.

Primary Phase-B decision remains:

`gap_M2 = median(T_M2[r] - T_plus_center_PhaseA[r])`

- if `gap_M2 >= -0.009768313008182594`: `M2_GENERIC_KRS_SHAPE_DESCRIPTORS_SUFFICIENT`;
- otherwise: `M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED`.

No target-edge optimization, selected edge, reading average, M+ reselection, or M3 implementation has occurred.

Next licensed action: target-blind exact-replay preflight for M2 rep0/rep30. A full candidate-null smoke may follow while target access remains false. Only after both execution layers are validated may the 31-case first reveal begin.
