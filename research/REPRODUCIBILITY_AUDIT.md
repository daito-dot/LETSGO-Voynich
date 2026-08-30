# Reproducibility audit

Last audited after Phase60D2.

This file distinguishes **accepted numerical authority** from **fully replayable code**. A result can remain accepted while its historical implementation is marked as reproducibility debt; the debt must not be silently hidden or reconstructed as if exact.

## Source data

The project does not redistribute the third-party ZL3b/EVA transcription. Reproduction requires the source described in `data/README.md`. Public scripts should accept a local path rather than embedding transcription text.

## Current replay status

| Phase | Result authority | Public executable status | Audit status |
|---|---|---|---|
| 56A | `phase56a_audit_results.json` / state CSVs | `phase56_build_state_matrix.py` | replayable substrate builder |
| 56B | `phase56b_results.json` + `README.md` interpretation | `phase56b_drift_changepoint.py` | **historical implementation warning**: public script is an earlier KMeans/raw-MSE development implementation and should not be assumed to reproduce every final accepted diagnostic exactly |
| 56C | `phase56c_results.json` | exact final implementation not separately preserved | **reproducibility debt** |
| 56D | `phase56d_results.json` | exact final implementation not separately preserved | **reproducibility debt** |
| 57–59 | phase result/plan files | mixed; consult each phase directory | numerical result files remain authority; audit before exact replay claims |
| 60A | `phase60a_pseudoboundary_results.json` / `phase60a_results.json` | result preserved | parser/eligibility counts differ across neighboring historical phases; do not infer exact sample continuity without audit |
| 60B | `phase60b_results.json` | `phase60b_feature_attribution.py` | executable restored after audit; requires local transcription |
| 60C | `phase60c_results.json` | exact session implementation not yet promoted as standalone public script | reproducibility debt |
| 60D/D2 | result JSON + frozen plans | exact session implementation not yet promoted as standalone public script | reproducibility debt |

## Authority rule

For historical phases, if script output and frozen accepted result differ, **do not silently overwrite the result**. Record the discrepancy, identify whether it is parser, eligibility, feature standardization, CV grouping, null construction, or later correction, and only supersede accepted output after an explicit audit experiment.

## Known Phase56 issue

`phase56b_drift_changepoint.py` currently contains the earlier KMeans/raw-MSE regime comparison. Later accepted Phase56 interpretation incorporated corrected matched-token / standardized diagnostics and rejected a sample-size-contaminated unmatched PCA interpretation. Therefore the current public 56B script is useful provenance but is not sufficient evidence that a clean clone exactly regenerates every accepted 56B headline.

Exact final Phase56C/D code was not durably preserved as a separate executable. Reconstructing it from prose would create a new implementation, not recover historical code. If reconstructed, it must be labeled `reimplementation` and regression-tested against frozen JSON before promotion.

## Phase60B repair

The placeholder reproducibility note at `experiments/phase60/phase60b_feature_attribution.py` has been replaced by an executable implementation accepting a local transcription path. Frozen `phase60b_results.json` remains numerical authority until an explicit clean-environment regression confirms exact reproduction.

## Next repository-hardening work

1. Add standalone exact/reimplemented scripts for 60C, 60D and 60D2 and regression-test against frozen outputs.
2. Reimplement Phase56C/D from frozen plans/results only if exact historical code cannot be recovered; label provenance honestly.
3. Add a machine-readable experiment manifest containing input identity, script, result, parser policy, unit of CV grouping and authority status.
4. Add lightweight regression checks that compare key headline statistics rather than requiring redistribution of transcription data.
5. Resolve the Phase59A/60A/56D paragraph eligibility-count differences before claiming exact cross-phase sample continuity.

## Scientific principle

Reproducibility debt is not evidence against a result, but it lowers confidence in implementation-level auditability. The repository therefore exposes the debt instead of pretending that frozen numerical artifacts and available scripts are automatically identical.
