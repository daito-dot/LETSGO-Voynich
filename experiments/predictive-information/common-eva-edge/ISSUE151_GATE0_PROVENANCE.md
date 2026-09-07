# Issue #151 — shared common-EVA edge consolidation Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

This document archives the first successful score-free Gate0 for Issue #151. No real-target `EDGE2_SHARED` probability, likelihood, bits/token, `G_shared`, `G_specific`, retention ratio or scientific classification was computed.

## Chronology

- Issue #151 opened after Issue #148 closed with `COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`;
- frozen plan commit `286cbb50b2f4801e42b1f89c4b3b62badaaea76c`, plan blob `e903bfbdd3742e578f784dc9c358f98f44ad42d2`;
- score-free Gate executable commit `99c2247125d7e917e903fdbc417d971ad5dfb4e0`, Gate blob `d5e3bd22501f8caebabc7c2728bc7f8d5cb59018`;
- workflow commit/head `d6a728c3f0b0508bad6586ace96373d9db06956e`;
- PR #153 was opened only after the plan, Gate and workflow were committed;
- no Issue #151 scientific shared-table scorer existed before this successful Gate run.

## First successful Gate authority

- Issue: #151
- PR: #153
- workflow: `Issue151 shared common-EVA edge Gate0`
- run: `34074227552`
- workflow head: `d6a728c3f0b0508bad6586ace96373d9db06956e`
- conclusion: `success`
- artifact ID: `10001496031`
- artifact name: `issue151-shared-edge-gate0-d6a728c3f0b0508bad6586ace96373d9db06956e`
- artifact ZIP digest: `sha256:5dc5e53921278db7e2cf1ce355aed408a45c6900c032be16fac850bda09b0390`
- result JSON SHA-256: `bcc6c6bd5600ef9f74484807b51ef1db454613bae2bbd351d90f089c8693eea2`

Gate disposition:

> `PASS — PROCEED TO SEPARATELY COMMITTED SHARED-EDGE SCORER`

## Reproduced entry authority

The successful Gate re-ran the frozen Issue #148 score-free Gate and reproduced:

- Issue #148 Gate result SHA-256 `f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf`;
- Issue #148 Gate script blob `a8029aac50ccc6e09ec975b7b86a1bde44415f9f`;
- Issue #148 Gate provenance blob `7f97b9731a6e72e2456ede436e837a3735f265fd`;
- Issue #148 scorer blob `7847c0fea1dcfc4ace5752d0188d70e3739679d3`;
- declared Issue #148 first-reveal result SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`;
- declared Issue #148 artifact `10001309613`, ZIP digest `sha256:cfefd670b00ebb3eae3020a4b5308115ec9172b793ed1fe4b598928718f5c622`;
- Issue #148 merge `b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131`;
- Issue #145 scorer blob `ce8a167c607fbcf2807f567439ab6837471f4f07`;
- declared Issue #145 first-reveal result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`;
- physical-leaf fold identity SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

Frozen sources were also re-verified:

- ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- Takahashi/IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`, git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`.

## Frozen consensus construction

For every outer fold, training counts from both readings exclude the same held-out physical-leaf fold and are combined exactly as:

`C_SHARED(ctx,outcome) = 0.5*C_ZL3b(ctx,outcome) + 0.5*C_IT2a(ctx,outcome)`.

The weights are fixed, not tuned. Future smoothing remains `alpha=0.01`, `V=32`. No target-native fallback, scalar, temperature, calibration, interpolation or mixture is licensed.

The Gate archived the exact training-only sparse fractional counts and SHA-256 identities of the corresponding dense 31×31 observed-atom matrices. END is part of the future model vocabulary but is not an observed edge-count matrix cell.

## Foldwise score-free support

| fold | ZL3b train BODY | IT2a train BODY | shared mass | shared contexts | positive pairs | ZL3b target BODY supported/total | IT2a target BODY supported/total |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 18,155 | 23,365 | 20,760.0 | 25 | 263 | 3,122 / 3,122 | 4,031 / 4,031 |
| 1 | 17,670 | 22,760 | 20,215.0 | 25 | 262 | 3,478 / 3,478 | 4,483 / 4,483 |
| 2 | 17,068 | 22,054 | 19,561.0 | 24 | 259 | 4,073 / 4,073 | 5,218 / 5,220 |
| 3 | 17,177 | 22,133 | 19,655.0 | 25 | 260 | 3,976 / 3,976 | 5,093 / 5,093 |
| 4 | 17,654 | 22,688 | 20,171.0 | 25 | 256 | 3,605 / 3,605 | 4,649 / 4,649 |

Consensus previous-terminal context coverage:

- ZL3b: `1.0` in all five folds;
- IT2a: `[1.0, 1.0, 0.9996168582375479, 1.0, 1.0]`;
- only two IT2a primary BODY events in fold 2 have a previous-terminal context absent from the consensus training table.

Every reading/fold exceeds the preregistered minimum of 300 total and consensus-context-supported primary BODY events by more than an order of magnitude.

## Physical-leaf leakage firewall

For every outer fold, all three checked overlaps are exactly empty:

- ZL3b training leaves ∩ held-out physical leaves;
- IT2a training leaves ∩ held-out physical leaves;
- union of both consensus-training leaf sets ∩ held-out physical leaves.

Thus the same manuscript leaf cannot enter the shared table through the other transcription lineage.

## Synthetic fractional-count check

Before real-target Gate execution, the target-free synthetic self-test verified:

- exact `0.5/0.5` fractional arithmetic;
- finite additive-smoothed probability for a seen synthetic outcome;
- finite additive-smoothed probability for END under `alpha=0.01`, `V=32`;
- no real target source loaded.

## Firewall status

The successful Gate artifact records all of the following as false:

- real-target shared-table probability computed;
- real-target shared-table likelihood computed;
- `bits_EDGE2_SHARED` computed;
- `G_shared` computed;
- `G_specific` computed;
- retention ratio computed;
- scientific classification computed;
- held-out current first atom used for support selection;
- target-selected support matching;
- target-selected atom mapping;
- consensus weights tuned;
- `k`/`alpha`/smoothing/fallback tuned;
- Currier/hand/section-conditioned shared table;
- latent-state fitting;
- S1/S2/H62/R1 tuning.

## Consequence

Support and leakage are sufficient to proceed without repair. The next allowed step is:

1. merge this Gate authority;
2. create a fresh post-merge branch;
3. commit the Issue #151 scientific scorer separately, pinned to this exact Gate result and merged Gate blobs;
4. only then create the first target-scoring workflow.

No Issue #151 scientific target result has been revealed by this Gate.

Refs #88 #145 #148 #150 #151 #153.