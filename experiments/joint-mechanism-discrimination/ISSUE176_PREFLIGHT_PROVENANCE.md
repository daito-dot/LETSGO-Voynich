# Issue #176 — accepted score-free recovery preflight provenance

Date: 2026-09-07
Status: **PASS — SCIENTIFIC WORKFLOW LICENSED**

This record is committed before any Issue #176 scientific recovery workflow is added.

## Scientific firewall

The accepted preflight payload records:

- `mode = preflight-only`
- `ok = true`
- `scientific_candidate_scores_computed = false`
- nested v1 `preflight.scientific_candidate_scores_computed = false`
- v1 `gate_pass = true`

No Issue #176 R1–R8 candidate performance score was computed or inspected in this phase.

## Frozen recovery code authority

- recovery base main: `54fb4f9a5122dfc64ae3fbf24633bb80380a5365`
- recovery-plan commit: `df7a6a60361ec8de9171c6c2648dbba50c80021f`
- recovery-plan blob: `6b05aa0dbe9dc57e55527b2123806c8d2d6582b9`
- initial wrapper commit: `4c67a5b047609b631cf6eb583f2c1dd253ada478`
- accepted wrapper commit: `bb00b88f4173dca5adf1596f1094bb7c0beeff74`
- accepted wrapper blob: `cd79047d12244350fccc6130379fa2e5726bab76`
- frozen Issue #172 v1 scorer blob: `f90f194396acdc50599cf9713dbbeb3ab5b4bed3`

The accepted wrapper differs from the initial wrapper only by containing the historical R1 self-test's human stdout inside the score-free audit object so machine JSON remains canonical. It does not alter scientific scoring.

## Aborted target-free wrapper run

The first Issue #176 preflight workflow run stopped before exact-source preflight because the historical R1 success message `self-test OK` contaminated wrapper JSON stdout.

- run ID: `34114017601`
- job ID: `101716510712`
- head: `509c1ce4fd0279eeb46d0baa50351d712eabaeb7`
- artifact ID: `10015517856`
- artifact digest: `sha256:39a0b0fb52effc1eff5d73ddb6f3cac4cbbae6a81d4170fadfb460320dc4d83e`
- archived self-test raw SHA-256: `1e4259a4e199c2cd335520bda618f9d777b0f085b3cb1d47f177cb9fe90b162f`
- exact-source preflight executed: **false**
- scientific candidate scores computed: **false**

The artifact itself showed that the return normalization worked: R1 was recorded as `ok=true`, `upstream_return=null`; the only failure was stdout transport purity.

## Accepted exact-source preflight

- workflow ID: `352220986`
- run ID: `34114228206`
- run attempt: `1`
- job ID: `101717194660`
- exact head: `34b0b751e3c4a8471b4ee814f09f688d1591d7c7`
- workflow blob: `0652e92bb25fea1297ffd003baa492892ba85b7d`
- artifact ID: `10015615648`
- artifact name: `issue176-runtime-recovery-preflight`
- artifact ZIP digest: `sha256:ef9c6b30b8c2a297e27fc049ed086e30f9005119f636b065347844e08348b0d0`
- raw preflight JSON SHA-256: `ef617c63e7ed48e709797bd1ba0f284832c880b69f3c00a082b0e75420d8e367`
- wrapper self-test JSON SHA-256: `da2226234a1307cdab1e1fb34745f59fd4f612c5f11522d11b23b23a8eb4ff49`
- provenance TXT SHA-256: `620fcb9bdabd8030500cb8a58e47f28dd64ba7039a37e924f2b85984a04cd6bf`
- preflight exit code: `0`
- workflow/job conclusion: `success`

The SHA-256 written inside the artifact for `issue176_recovery_preflight.json` was independently recomputed after download and matched exactly: `ef617c63e7ed48e709797bd1ba0f284832c880b69f3c00a082b0e75420d8e367`.

## Frozen external source authority

All source checks passed before preflight:

- cipher_benchmark commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- Naibbe commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`

## Score-free support audit

The preflight regenerated the immutable surfaces and found nonzero R1/R5 support in every fold for both historical anchors.

A1 fold event counts:

| fold | R1 boundary | R1 mid-token | R1 P2 | R5 same-line accepted BODY | R5 prior-line events |
|---:|---:|---:|---:|---:|---:|
| 0 | 5019 | 5401 | 4883 | 1956 | 235 |
| 1 | 5509 | 5921 | 5379 | 2040 | 238 |
| 2 | 6172 | 6573 | 6001 | 2446 | 296 |
| 3 | 6139 | 6467 | 5917 | 2509 | 305 |
| 4 | 5472 | 5866 | 5315 | 2100 | 275 |

Naibbe C1-E0 fold event counts:

| fold | R1 boundary | R1 mid-token | R1 P2 | R5 same-line accepted BODY | R5 prior-line events |
|---:|---:|---:|---:|---:|---:|
| 0 | 8251 | 7040 | 7309 | 7378 | 336 |
| 1 | 5537 | 4770 | 4980 | 4939 | 248 |
| 2 | 5034 | 4377 | 4510 | 4499 | 208 |
| 3 | 5851 | 5011 | 5189 | 5228 | 250 |
| 4 | 6843 | 5780 | 6094 | 6180 | 281 |

The causal-order audit also passed for both anchors:

- A1: 736 items, 99 causal groups, `acyclic=true`, `future_tokens_used=false`
- Naibbe: 241 items, 4 causal groups, `acyclic=true`, `future_tokens_used=false`

Naibbe R7 remains the preregistered structural disposition `FAIL_NO_CURRIER_COMPARABLE_CHANNEL`; this is not a newly fitted numerical score.

## Permission boundary

This PASS licenses exactly one next action: add the separately committed Issue #176 scientific recovery workflow that invokes the already-frozen wrapper `cd79047d...` and frozen v1 scorer `f90f1943...` on the exact same external sources.

It does not license any candidate, threshold, seed, representation, scoring-function, fold, source-population or access-policy change.

Refs #68 #88 #172 #175 #176.
