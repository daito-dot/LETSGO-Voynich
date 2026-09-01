# Issue #72 V2 — Stage C1 target implementation contract

Status: **FROZEN BEFORE C1 TARGET EXECUTION**

Authorities, in order:

1. `research/RESEARCH_PROTOCOL.md`
2. `STAGE_C_FIXED_PATH_RANDOMIZATION_PLAN.md`
3. `STAGE_C_SCORING_AMENDMENT_C1.md`
4. exact permanent C0 archive under `stage-c0/`

No Stage C intervention R1 target score existed when this contract was added.

## 1. Execution unit

One scoring job handles exactly one `(axis, assignment)` pair:

- axis ∈ `EL, ES, ET, EG`;
- assignment `r0..r30`.

The complete first reveal contains exactly 124 such jobs. No failed/scored assignment may be dropped or replaced.

## 2. C0 reconstruction gate before target access

Every job must first:

1. verify `stage-c0/stage_c0_support.json.gz` SHA-256 `946d8f8fa61d996a548a344f7e303f804283230ce8bef0d51add473d811e4ed3`;
2. decompress it and verify exact raw SHA-256 `da00a66b77a90eb36a158a9942927a27743e64aba7fac69337ff3a67424d695a` and byte count `206486933`;
3. verify `MANIFEST.json` SHA-256 `aba822be57bbac0c04a9fa785a0a835eafe192b406fead5cd7166051825f45ae`;
4. verify all 20 trace gzip files against the C0 trace manifest;
5. require the C0 target firewall to be entirely false.

No target reading may be loaded before these checks pass.

## 3. Surface reconstruction gate

Load pinned Naibbe `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`.

For the requested `(axis,j)`:

- reconstruct all rep0..rep4 baseline surfaces from exact C0 traces and the published map;
- reconstruct randomized surfaces from the exact C0 randomization law plus the documented unreachable-key invariant repair;
- verify each baseline rep pooled surface SHA against C0;
- verify the complete five-path randomized pooled surface SHA against C0;
- verify randomized parser support counts/coverage against C0;
- verify the exact stored common-support mask payload SHA.

Failure stops before target access.

## 4. Common-support dataset

For every frozen line mask, retain exactly positions with mask bit `1`.

Require:

- baseline and randomized tokens both parse under unchanged `SlotParser(min)`;
- baseline/randomized line support is identical;
- total retained count equals C0 `common_support_count`;
- fold counts equal C0 common-support counts summed across process reps within each manuscript.

Fold identity is manuscript-only:

- BIS193 → 0
- CLM13027 → 1
- Mazarine915 → 2
- UBL758 → 3

All five process reps remain inside the manuscript's fold.

## 5. R1 coordinate construction

Use all 66 unordered slot pairs and the unchanged K_other-conditional Jeffreys-smoothed MH Yule-Q implementation.

For each paired surface separately:

- calculate real full 66-edge Q on common support;
- generate 1,000 line-local reference nulls;
- residualize with the unchanged empirical mid-rank normal transform;
- retain full residual-Z, Q and residual energy.

C1 does not require an independent test-null population because it is not classifying residual-graph existence. The primary estimand is paired target-topology change.

Frozen deterministic namespaces:

- baseline: `issue72v2:C1:{axis}:r{j}:baseline-common:reference:v1`
- randomized: `issue72v2:C1:{axis}:r{j}:randomized-common:reference:v1`

Namespaces are independent across side/axis/assignment.

## 6. Target access

Only after §§2–5 complete may the job load the already frozen #58C ZL3b and #58D IT2a residual target vectors using the accepted Issue #68 loader.

For each reading report:

- baseline Pearson `R`;
- randomized Pearson `R`;
- `DELTA_R = R_randomized - R_baseline`;
- baseline sign agreement /66;
- randomized sign agreement /66.

Do not average readings.

## 7. Per-assignment output

Every result JSON must include:

- exact source/C0/code authority;
- axis and assignment;
- C0 surface/support identities;
- line/common token counts and four manuscript fold counts;
- both reference namespaces;
- baseline and randomized 66-edge Q vectors;
- baseline and randomized 66-edge residual-Z vectors;
- residual energies;
- both-reading topology metrics and `DELTA_R`;
- explicit statement that no hard intervention threshold was applied.

## 8. Aggregate output

After all 124 outputs exist, aggregate without selecting assignments.

For each axis × reading report:

- all 31 `DELTA_R` values;
- min/Q1/median/Q3/max/mean;
- counts `<0`, `=0`, `>0`;
- `rank_nonloss=(1+count[DELTA_R>=0])/32` and numerator;
- baseline/common and randomized/common R distributions;
- C0 coverage/common-support distributions.

Also report, per axis:

- assignments negative in both readings;
- assignments nonnegative in both readings;
- mixed-direction assignments.

No `.05` or other cutoff is used to manufacture a categorical claim.

## 9. Target-blind implementation preflight

Before the first-reveal workflow is added, the scorer must support a verify-only mode that executes §§2–4 and surface/support checks but does **not**:

- build R1 reference-null residuals;
- load ZL3b/IT2a target vectors;
- compute target correlations.

Run verify-only on at least one assignment from each axis. A failure may repair only implementation/transport semantics already frozen above; it may not modify the scientific randomization population after observing target data.

## 10. Claim boundary

C1 localizes association contribution conditional on frozen Naibbe process paths. It is not a historical-use test, plaintext identification, decoder validation, or decipherment.
