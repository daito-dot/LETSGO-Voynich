# Issue #75 Phase A — implementation freeze before target access

Date: 2026-09-01  
Status: **SCORER / AGGREGATION IMPLEMENTED; NO PHASE-A TARGET SCORE YET**

Normative scientific plan:

- `PLAN_A.md`
- plan commit `8d984cfa61a5616bef61b45248c0a7a5d213fbf8`

Target-blind Stage A0 authority:

- successful generation run `33501046064`
- generation head `edae4cbe9811128dc839bf63c77efe0f48c78da4`
- permanent authority commit `c703b2d01c941b6bfd17758f09868c71a200f212`
- `generator_authority.json` SHA-256 `83e5808576a6416e4b03e302242805509c05d16928403d3a58e5636bdbf9ecd2`
- artifact ID `9797702407`
- artifact digest `sha256:4dbf35ea95983a1b0f61ba7641954d8e1cadd8eedb5b1417c32928f9292723c6`
- 124/124 corpora frozen
- no target vectors loaded
- no pair Q / residual Z / target topology computed
- no drops / no rerolls

Pretarget numerical incident:

- failed run `33500769086`
- incident record `STAGE_A0_IMPLEMENTATION_INCIDENT_20260901.md`
- repair changed only deterministic M1 Newton damping; scientific M1 family unchanged
- successful fitted maximum marginal error after repair `1.2705114738054135e-14`, well inside the frozen `1e-10` requirement

Frozen scorer:

- file `phase75a_score.py`
- commit `21e7bbc176e593ef9fa025113fb17799ca500d8e`

The scorer must:

1. re-read the exact Stage A0 authority SHA;
2. deterministically refit M0/M1 and regenerate the requested family/rep corpus;
3. require exact occupancy SHA equality with Stage A0;
4. in `--verify-only`, stop before pair Q, residual Z or target loading;
5. in scoring mode, compute candidate-owned 1000-reference / 1000-test line-local null calibration;
6. only after candidate residual construction call the already-audited `target68.load_target_references()`;
7. retain both ZL3b and IT2a separately and set only `T=min(R_ZL3b,R_IT2a)` as the conservative joint scalar.

Frozen aggregation:

- file `phase75a_aggregate.py`
- commit `d058a5dbe9571a7afa528e001d64d4a576f7c0ff`

The primary positive-control tolerance uses the plan's empirical q95 rule. The implementation freezes “empirical q95” as the conventional higher empirical order statistic:

`sorted_x[ceil(q*n)-1]`

with `n=31` paired MPLUS-A/B differences.

This is frozen before any Phase-A target score exists. The same definition is used for non-promoting q90/q99 sensitivity.

The exact ordered classification remains:

1. validate both M+ bank median T values against `0.9447148364`;
2. if either fails, `POSITIVE_CONTROL_CALIBRATION_FAILED_STOP`;
3. otherwise compute `delta_plus=q95(|T_A-T_B|)`;
4. compute paired median gaps of M0 and M1 against `(T_A+T_B)/2`;
5. if M0 gap `>= -delta_plus`, classify `M0_INDEPENDENT_SLOT_MARGINALS_SUFFICIENT`;
6. else if M1 gap `>= -delta_plus`, classify `M1_MARGINALS_PLUS_OCCUPANCY_COUNT_SUFFICIENT`;
7. else `LOW_ORDER_MODELS_INSUFFICIENT_EMPIRICAL_PATTERN_STRUCTURE_REQUIRED`.

No target edge is selected or optimized, no reading is averaged, no round R threshold is introduced, and M2/M3 remain unlicensed in this first reveal.

The next licensed action is target-blind scorer preflight only.
