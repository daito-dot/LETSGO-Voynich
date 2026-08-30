# Reproducibility audit

Last audited after Phase61C, including an independent post-61C code/provenance review.

This file distinguishes **accepted numerical authority** from **fully replayable code**. A result can remain accepted while its historical implementation is marked as reproducibility debt; the debt must not be silently hidden or reconstructed as if exact.

Detailed independent findings for Phase51–61C are recorded in `AUDIT_PHASE51_61C_20260830.md` and must be read before changing Phase60/61 numerical interpretation.

## Source data

The project does not redistribute the third-party ZL3b/EVA transcription. Reproduction requires the source described in `../data/README.md`. Public scripts should accept a local path rather than embedding transcription text.

Exact ZL3b/EVA Git blob SHA-1 used by the Phase60/61 audit:

`2a4533ab9bdfa85db9bad602d590978953055df1`

## Current replay status

| Phase | Result authority | Public executable status | Audit status |
|---|---|---|---|
| 51 | `phase51_frozen_dsl_falsification_results.json` | public entrypoint is parameter/provenance stub; recovered historical source archived under `experiments/phase51/archive/` | **historical implementation recovered**, but archive retains original workspace-specific path and is not yet normalized as a clean replay executable |
| 56A | `phase56a_audit_results.json` / state CSVs | `phase56_build_state_matrix.py` | replayable substrate builder |
| 56B | `phase56b_results.json` + `README.md` interpretation | `phase56b_drift_changepoint.py` | **historical implementation warning**: public script is an earlier KMeans/raw-MSE development implementation and should not be assumed to reproduce every final accepted diagnostic exactly |
| 56C | `phase56c_results.json` | exact final implementation not separately preserved | **reproducibility debt** |
| 56D | `phase56d_results.json` | exact final implementation not separately preserved | **reproducibility debt** |
| 57–59 | phase result/plan files | mixed; consult each phase directory | numerical result files remain authority; audit before exact replay claims |
| 60A | `phase60a_pseudoboundary_results.json` / `phase60a_results.json` | result preserved | parser/eligibility counts differ across neighboring historical phases; do not infer exact sample continuity without audit |
| 60B | `phase60b_results.json` | `phase60b_feature_attribution.py` | **public reimplementation is not an exact cross-fit replay**; pooled held-out direction is reused at final scoring; corrected audit keeps all five folds positive, but historical `n=380` eligibility remains unrecovered |
| 60C | `phase60c_results.json` | exact session implementation not yet promoted as standalone public script | reproducibility debt |
| 60D/D2 | result JSON + frozen plans | exact session implementation not yet promoted as standalone public script | reproducibility debt |
| 60E | `phase60e_results.json` | `phase60e_memory_horizon.py` is a provenance stub, not an executing replay | **reproducibility debt**; no audit evidence currently reverses the frozen short-memory interpretation |
| 61A | `phase61a_results.json` | historical generator executable not preserved | numerical authority retained; treat as a **narrow architecture/mechanism demonstration**, not prospective validation of preselected strength 1.5 |
| 61B | `phase61b_results.json` | historical A0 executable not preserved | **reproducibility debt**; accepted joint A0 rejection retained; Phase61C independently reproduces the Voynich-side metric regime |
| 61C | `phase61c_results.json` + `REPORT_C.md` | `phase61c_joint_model.py` | **replayable frozen implementation**; prospective freeze chronology verified; training-only preprocessing/model selection verified; additional vocabulary and eta2-profile sensitivities audited |

## Authority rule

For historical phases, if script output and frozen accepted result differ, **do not silently overwrite the result**. Record the discrepancy, identify whether it is parser, eligibility, feature standardization, CV grouping, null construction, model-selection leakage, or later correction, and only supersede accepted output after an explicit audit experiment.

A post-hoc diagnostic may narrow the interpretation of a frozen result but does not retroactively change a preregistered pass/fail rule.

## Phase51 recovered provenance

The full historical Phase51 DSL implementation was recovered from the preserved research workspace and archived verbatim at:

`../experiments/phase51/archive/phase51_frozen_dsl_falsification_historical.py`

It matches the recorded frozen architecture (64 roots, block 4, state-use 0.30, prefix 0.22, suffix 0.32, two variants/root) and the accepted result family. The archive intentionally retains its original `/mnt/data/eva_zl3b(1).txt` workspace path; changing that file would create a normalized reimplementation rather than preserve the historical source.

## Phase60B cross-fit correction

The current public `phase60b_feature_attribution.py` constructs fold-specific training directions but discards them for the final pooled score, recomputing a direction from all held-out deltas. It also estimates feature SD globally.

Independent audit on the exact ZL3b blob found that retaining the fold-specific training direction is the material correction; training-only versus global SD has negligible impact.

Corrected training-only-scaling mean projections on the current 431-paired-paragraph parser:

- raw EVA: `0.9017`;
- conservative: `0.7495`;
- Phase56: `0.9326`.

Raw-EVA fold means are:

`[0.6748, 1.5039, 0.4504, 0.4852, 1.4505]`

All five remain positive and almost reproduce the independently frozen Phase60A anti-circular fold values. Therefore the high-level paragraph-entry result survives the correction.

However, accepted Phase60B used `n=380`, and that historical eligibility rule remains unrecovered. Exact accepted effect sizes and carrier ranking are therefore not replay-certified. Use the broader signed carrier interpretation only; do not cite the current public script as an exact reproduction of `phase60b_results.json`.

Detailed numbers and carrier sensitivity: `AUDIT_PHASE51_61C_20260830.md`.

Audit workflow provenance: `33311940729`.

## Phase60E status

`phase60e_memory_horizon.py` currently prints provenance and points to the frozen result rather than executing the analysis. `phase60e_results.json` remains numerical authority. Exact clean replay is still required before describing the `.py` file as executable reproduction.

## Phase61A/B status

The historical Phase61A/B generator executable was not preserved. The audit therefore does not claim exact A0 replay.

61A should be described narrowly: the boundary-aware A0 architecture family contains a low-complexity entry mixture capable of reaching/exceeding the scalar entry target over the exposed strength grid. Because strength 1.5 was selected after the grid outcomes were visible and then used in 61B, 61A is not prospective validation of a preselected strength-1.5 model.

61B's accepted joint rejection remains scientifically relevant, especially its severe local-family deficit, but exact A0 numerical replay remains provenance debt.

## Phase61C independent audit

The Git history verifies prospective freeze order:

1. `PLAN_C.md` — `5744f37771c9dda471394c5c4f59fa5c825b3eb4`;
2. `IMPLEMENTATION_C.md` — `f24b9bbbc057f6f613a7e019bb75369de1867d7e`;
3. executable — `f081e0cd20048df2bcf86d16802761c91a0c5fd0`;
4. held-out result — `ca2184950497800a8cd2f18ec99fc279b029efdf`.

The executable correctly uses training leaves for feature scaling, entry-direction estimation, entry-shape learning and 16-pair parameter selection before held-out evaluation.

Frozen held-out A1/Voynich ratios remain:

- entry projection `0.7969`;
- local-prev10 `0.7169`;
- line-position eta2 mean `1.1163`.

All pass the frozen `[0.5,2.0]` first joint gate.

### Training-vocabulary-only sensitivity

Removing all held-out-only token types from the generator leaves the result essentially unchanged:

- entry `0.7947`;
- local-prev10 `0.7181`;
- line-position eta2 mean `1.0981`;

and leaves all five selected parameter pairs unchanged. Full-manuscript vocabulary sharing is not driving the frozen survival verdict.

Workflow: `33312218285`.

### Eta2 profile diagnostic

The line-position target is an average over 11 feature eta2 values. Exact replay of the selected models shows:

- all 11 ratio: `1.1163`;
- near-family coordinates only: `5.9840`;
- excluding near-family: `0.6391`;
- entry-shape-related coordinates: `0.7215`;
- excluding near-family and k/t: `0.6238`.

Thus A1 passes the **aggregate preregistered scalar** but substantially overproduces near-family line-position eta2 while underproducing several other coordinates. This does not retroactively fail Phase61C, but it means the result must not be paraphrased as reproducing the full multivariate Voynich line-position grammar.

Workflow: `33312993742`.

## Next repository-hardening work

1. Resolve the Phase60B historical `n=380` parser/eligibility provenance before certifying exact effect sizes/carrier rank.
2. Normalize the recovered Phase51 historical source into a separate clean replay script only if desired; preserve the archived original unchanged.
3. Add standalone exact/reimplemented scripts for 60C, 60D/D2 and 60E and regression-test against frozen outputs.
4. Reimplement Phase56C/D from frozen plans/results only if exact historical code cannot be recovered; label provenance honestly.
5. Add a machine-readable experiment manifest containing input identity, script, result, parser policy, CV grouping, exposure status and authority status.
6. Prefer profile-aware common scorecards/prospective discriminators in later model-family comparisons where scalar averaging can hide coordinate cancellation.

## Scientific principle

Reproducibility debt is not evidence against a result, but it lowers confidence in implementation-level auditability. The repository therefore exposes the debt instead of pretending that frozen numerical artifacts and available scripts are automatically identical.
