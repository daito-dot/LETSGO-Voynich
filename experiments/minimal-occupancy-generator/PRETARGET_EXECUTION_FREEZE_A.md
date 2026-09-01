# Issue #75 Phase A — pretarget execution freeze / first-reveal authorization

Date: 2026-09-01  
Status: **TARGET-BLIND EXECUTION VALIDATED; FIRST REVEAL AUTHORIZED**

Normative scientific plan:

- `PLAN_A.md`
- commit `8d984cfa61a5616bef61b45248c0a7a5d213fbf8`

Target-blind Stage A0 authority:

- 124/124 cross-fitted corpora permanently frozen
- authority commit `c703b2d01c941b6bfd17758f09868c71a200f212`
- authority SHA-256 `83e5808576a6416e4b03e302242805509c05d16928403d3a58e5636bdbf9ecd2`
- successful run `33501046064`
- no target vectors, Q, Z or target correlations computed during A0

Frozen scientific scorer / aggregation:

- original scorer freeze commit `21e7bbc176e593ef9fa025113fb17799ca500d8e`
- scorer replay-gate repair commit `11cbcab12e9c02e5002bc286a132b9a8a9f267aa`
- aggregation-law commit `d058a5dbe9571a7afa528e001d64d4a576f7c0ff`
- implementation freeze `IMPLEMENTATION_FREEZE_A.md`
- replay incident and repair addendum remain part of chronology

The replay repair changes no scientific model, random seed, generated corpus, candidate-null law, target vector, score or decision rule. Exact final occupancy SHA remains mandatory before target access.

## Successful exact-replay preflight

Workflow run `33501747280` completed `success` at head:

`698e7ee5503bc7e47d183deb7d8cc09d89502216`

Eight boundary cases all passed:

- M0 rep0 / rep30
- M1 rep0 / rep30
- MPLUS-A rep0 / rep30
- MPLUS-B rep0 / rep30

For every boundary case:

- deterministic source/parser/fold authority matched;
- training empirical statistics matched Stage A0;
- regenerated fit error remained `<=1e-10`;
- exact final occupancy SHA matched Stage A0;
- target access remained entirely false.

## Successful candidate-owned null smoke

Workflow run `33501857058` completed `success` at head:

`b4a723c204996764a64ac53121156cc194461c98`

One exact rep0 corpus from each family executed the full frozen candidate-owned measurement machinery:

- 66 pair-Q values;
- 1000 reference line-local nulls;
- residual Z;
- five-fold train/held reliability;
- 1000 independent test nulls;
- residual energy / `p_exist`.

All four jobs passed while deliberately never calling the target loader.

Smoke artifact authorities:

- M0 artifact `9798058669`, digest `sha256:29f5281ebc021d8f5ea488c3182e44e91e1336a3dc2b58334247333843b80b9b`
- M1 artifact `9798059454`, digest `sha256:3a77f5f8304c35d936848c3c93f19aadefe7b8dac151563e044061521eaaf82d`
- MPLUS-A artifact `9798059590`, digest `sha256:4c1c25d4fe62957a4229fe7ab4c87fc92cd61b4ca032efa6bc3c41c2dbc9a91a`
- MPLUS-B artifact `9798061185`, digest `sha256:7e1385e683838fe731f7b3511dc2e6d1ab5700b2298e76247f507463fae595f6`

The smoke results are implementation diagnostics only. Their E/p/W values are not used to alter the frozen model families, thresholds, nulls or first-reveal population.

## First-reveal authorization

The next licensed action is exactly one complete 124-case first reveal:

- M0 reps 0..30
- M1 reps 0..30
- MPLUS-A reps 0..30
- MPLUS-B reps 0..30

Every case must first regenerate and match its Stage A0 occupancy SHA, then compute candidate-owned residual calibration, and only then load the frozen ZL3b/IT2a target vectors.

After this point, no target-dependent change is licensed to:

- model definitions;
- fit criteria;
- cross-fit folds;
- generation seed namespaces;
- Stage A0 corpora;
- candidate reference/test null laws;
- N_ref/N_test;
- target loader or target vectors;
- T definition;
- M+ calibration floor;
- q95 positive-control tolerance law;
- ordered classification;
- complete no-drop 124-case population.

Execution/transport failures may be documented, but scientific commitments above may not be repaired after reveal begins.

At this freeze point there is still no Issue #75 target score, T distribution, positive-control target calibration, or Phase-A scientific classification.
