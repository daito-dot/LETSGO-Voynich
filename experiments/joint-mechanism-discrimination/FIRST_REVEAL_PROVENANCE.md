# Issue #172 — historical-anchor calibration first-reveal provenance

Date: 2026-09-07
Status: **COMPLETE — FROZEN `INVALID / NON-COMPARABLE`**

## Frozen result

The Issue #172 historical-anchor first reveal did **not** produce interpretable A1 or Naibbe R1–R8 scores.

Frozen result:

> **`INVALID / NON-COMPARABLE`**

The scorer result records:

- `scored=false`
- error: `AttributeError: 'NoneType' object has no attribute 'get'`
- `post_failure_target_driven_repair_allowed=false`

Therefore this reveal supports no new scientific comparison between A1/A1-R1 and Naibbe C1-E0 under the post-#88 joint contract. Historical pre-Issue172 results remain historical authority only.

## Frozen scientific authority

- post-Stage0 base main: `53961dbe3a72ebb1c026079987d9a194ad0f0935`
- corrected target-plan head: `43f5e573d2ae0b621b1eba4495e29b3a4fb73bae`
- frozen target-plan blob: `e1caf3bf6b70fb85c00fc91c621d7e823f72f4d9`
- scorer-only commit: `dabcf1fe7ddd6df66d849c8e752e7e1245c9d52e`
- frozen scorer blob: `f90f194396acdc50599cf9713dbbeb3ab5b4bed3`

No scientific scorer code, threshold, candidate definition, seed, representation, or target-access rule was changed after the scorer-only commit.

## Pre-reveal wrapper abort

The first Actions run was:

- run ID: `34112911527`
- job ID: `101712997832`
- head: `ae27aa17e53bac83fd224cbc96e8e0858de396c2`
- artifact ID: `10015111916`
- artifact ZIP digest: `sha256:677f4fad04392145b86c7ebb4bd9c94472d6a41e6b6c21fdd857fe7b7f2b19de`

This run stopped in the target-free self-test wrapper. The frozen scorer self-test itself succeeded and reported `ok=true`, but the workflow incorrectly attempted to parse its human-prefixed stdout (`self-test OK` followed by JSON) as pure JSON. The actual `--run` target-scoring step was skipped. The uploaded artifact contained only the self-test output; no Issue #172 candidate target score was computed.

A workflow-only repair removed that wrapper parse. The repair did not modify the scorer or any scientific contract. Repair commit: `538f49dab521a8187525e747d378b540c10be950`.

The frozen target plan literally says that exactly one first target workflow is performed. There are two Actions workflow runs in the audit trail because of this pre-target wrapper abort. Only one run invoked the scientific `--run` path, but this provenance does **not** claim literal one-workflow chronology. The final scientific result is invalid independently, so no promotion or scientific conclusion is taken from the reveal.

## Scientific first-reveal execution

Workflow-only repair/final reveal head:

- exact head: `538f49dab521a8187525e747d378b540c10be950`
- workflow blob: `cc0b640c6cf563a3335ce9d5961f2ece020010b1`
- workflow ID: `352212115`
- run ID: `34113182808`
- run attempt: `1`
- job ID: `101713851142`
- workflow conclusion: `success` (transport/artifact preservation; the scorer step used `continue-on-error`)
- scorer exit code: `1`
- artifact ID: `10015252816`
- artifact name: `issue172-anchor-calibration-first-reveal`
- artifact ZIP digest: `sha256:6b7c084ac0e9254ff56940f2e4f49dd56df2ecad73cf1ed767d2f3fc01ddad0a`
- raw result JSON SHA-256: `045c4a3a50fda2057a889c9088e02c1c0db09153875cb060d7add526e9f16566`

The recorded SHA-256 in the artifact and an independent SHA-256 over the downloaded raw JSON bytes matched exactly.

Frozen external authority checks passed before the scorer run:

- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- Naibbe commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`

The target-free synthetic/self-test passed before `--run` in the scientific execution.

## Archived raw result

Repository copy: `FIRST_REVEAL_RESULT.json`.

The authoritative scientific payload is the artifact byte sequence identified by SHA-256 `045c4a3a50fda2057a889c9088e02c1c0db09153875cb060d7add526e9f16566`. The repository copy is intended to preserve the same canonical JSON payload.

## Interpretation firewall

Because the frozen result is `INVALID / NON-COMPARABLE` with `scored=false`:

- do not infer that A1 passes or fails any new Issue #172 R1–R8 responsibility;
- do not infer that Naibbe passes or fails any new Issue #172 R1–R8 responsibility;
- do not use the runtime error to alter a scientific threshold, candidate surface, seed, representation, codebook, or target-access rule;
- do not rerun this frozen reveal after modifying the scorer in place.

If the program continues with a corrected executable scorer, it must be a **new, explicitly preregistered phase/reveal** that preserves the scientific contract and documents why the implementation correction is non-scientific. It may not use any candidate target-performance vector from this failed reveal; none was produced.

## Consequence

Issue #172 has successfully frozen the post-#88 mechanism-discrimination contract and exposed an implementation failure in the first historical-anchor execution, but it has **not yet calibrated A1 or Naibbe against that contract**.

The next scientific step is therefore not to patch the strongest candidate. It is to create a clean, separately preregistered execution phase for the unchanged historical-anchor contract, with the runtime defect corrected before any new target-scoring execution.

Refs #68 #88 #172.
