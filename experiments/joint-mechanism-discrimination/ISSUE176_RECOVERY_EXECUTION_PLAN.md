# Issue #176 — runtime-recovery execution plan

Date: 2026-09-07
Status: **FROZEN RECOVERY DESIGN — NO NEW CANDIDATE TARGET SCORE MAY BE COMPUTED FROM THIS COMMIT**

Parent: #172. Recovery issue: #176.
Base authority: post-PR #175 main `54fb4f9a5122dfc64ae3fbf24633bb80380a5365`.
Frozen Issue #172 v1 scorer blob: `f90f194396acdc50599cf9713dbbeb3ab5b4bed3`.
Frozen Issue #172 invalid-result SHA-256: `045c4a3a50fda2057a889c9088e02c1c0db09153875cb060d7add526e9f16566`.
Frozen target-plan blob: `e1caf3bf6b70fb85c00fc91c621d7e823f72f4d9`.

## 1. Purpose

Issue #172 first reveal is permanently frozen as `INVALID / NON-COMPARABLE` with `scored=false`. No A1 or Naibbe R1–R8 candidate performance vector was produced. Issue #176 exists only to correct the target-free runtime interface defect while preserving every scientific choice of the frozen Issue #172 historical-anchor contract.

This is not an A1 repair, Naibbe repair, representation rescue, threshold change, or candidate-family redesign.

## 2. Frozen defect diagnosis

The v1 scorer imports the historical Phase4A production-boundary self-test as `R1A.self_test()`.

The historical R1 self-test is success-by-no-exception and returns `None`. The already-frozen Issue #172 target-free self-test artifact records `historical_synthetic.R1 = null` before any Issue #172 candidate scoring.

The v1 runtime preflight later constructs a dictionary containing `R1A.self_test()` and applies `.get("ok")` to every value. Therefore a successful historical R1 self-test is dereferenced as if it were a mapping, producing the frozen error:

`AttributeError: 'NoneType' object has no attribute 'get'`

The correction is therefore fixed before any new scientific reveal: normalize only this historical self-test return contract.

## 3. Scientific contract remains byte-anchored

The following are immutable in this recovery phase:

- Issue #172 candidate roster and primary roles;
- A1/A1-R1 mechanism, primary seeds and canonical surfaces;
- Naibbe C1-E0 public commit, codebook, primary view, seeds and canonical surfaces;
- ZL3b, IT2a and CREMMA source authorities;
- R1–R10 scientific definitions, thresholds and outcome logic;
- fold assignments, source populations and causal ordering;
- historical R2 and R9 carry-forward authority;
- common-EVA cleaning and R5/R6 edge definitions;
- Currier R7 definitions and K ladder;
- R8 LOCAL40 / prior-inventory definitions;
- R10 access and complexity accounting;
- no per-reading candidate tuning;
- no post-reveal candidate/seed/view/representation/threshold selection.

The frozen v1 scorer file itself is retained unchanged at git blob `f90f194396acdc50599cf9713dbbeb3ab5b4bed3`.

## 4. Recovery wrapper

A new wrapper will be added at:

`experiments/joint-mechanism-discrimination/issue176_recovery_wrapper.py`

It must import the frozen v1 scorer and verify its git blob before doing any work. It must not copy or rewrite the scientific scoring functions.

The only runtime normalization licensed is:

1. capture the original `R1A.self_test` function before patching;
2. call that original exactly once each time the normalized test is invoked;
3. if it raises, propagate failure;
4. if it returns `None`, normalize to `{ "ok": true, "upstream_return": null }`;
5. if it returns a mapping, reject only an explicit `ok == false`, otherwise preserve the mapping as `upstream_return` and normalize `ok=true`;
6. any other return type is a runtime-contract failure;
7. assign only the normalized adapter to `v1.R1A.self_test`.

No `R1A.score_*` function, atomization rule, event population, fold, target, candidate surface or threshold may change.

## 5. Required wrapper modes

### `--self-test`

Target-free wrapper contract test. It must verify:

- v1 scorer blob identity;
- normalized R1 self-test behavior;
- v1 joint classification helper on synthetic structures;
- no external target source is loaded;
- no real Issue #176 candidate score is computed.

### `--preflight-only ZL3B IT2A CREMMA_ROOT NAIBBE_ROOT OUT_JSON`

This mode may call the frozen v1 `preflight(...)` after installing only the R1 self-test normalization. It may regenerate immutable A1/Naibbe primary surfaces and score-free support/authority audits required by the frozen contract.

It must stop before `score_all(...)` and record:

- `mode = "preflight-only"`;
- `scientific_candidate_scores_computed = false`;
- exact wrapper and v1 identities;
- the v1 preflight payload or an explicit invalid preflight error.

A failure here licenses no scientific workflow.

### `--run ZL3B IT2A CREMMA_ROOT NAIBBE_ROOT OUT_JSON`

This mode is not executed until the preflight-only phase has passed and been archived. It installs the identical R1 self-test normalization and then delegates the full scientific calculation to frozen v1 `score_all(...)` without changing its inputs or output classification logic.

## 6. External authority

The preflight and scientific workflows must use the exact historical sources:

- cipher_benchmark commit `315f0cad4de3d021bd4185765c037cf2a28d341c`;
- ZL3b git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`;
- IT2a git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`;
- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- CREMMA commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- Naibbe commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`;
- Naibbe `naibbe_v2.py` blob `b566ad82e4b6ff0782ecdddebf77718dac44f292`;
- Naibbe `references/naibbe_tables.csv` blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`.

## 7. Chronology firewall

The required order is:

1. commit this recovery execution plan alone;
2. commit the recovery wrapper alone and freeze its blob;
3. add a preflight-only workflow in a later commit;
4. execute the preflight-only workflow;
5. archive preflight raw bytes, SHA-256, exact head, run/job/artifact IDs, v1 blob, wrapper blob and workflow blob before any scientific workflow is added;
6. only after an accepted preflight, add the scientific recovery workflow in a later commit;
7. perform one scientific recovery reveal;
8. archive result raw bytes, SHA-256, exact head, run/job/artifact IDs and code/workflow blobs before interpretation;
9. no scientific repair after reveal inside Issue #176.

A workflow transport failure before the scientific `--run` step must be archived explicitly. It is not permission to alter scientific code.

## 8. Interpretation boundary

A valid Issue #176 result remains only a historical-anchor structural calibration under the unchanged Issue #172 contract. It cannot by itself establish plaintext, semantics, natural-language wordhood, language/cipher family, authorship, historical mechanism, artificiality/hoax or decipherment.

Refs #68 #88 #172 #175 #176.
