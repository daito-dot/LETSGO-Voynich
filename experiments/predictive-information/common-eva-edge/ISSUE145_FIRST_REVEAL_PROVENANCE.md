# Issue #145 — common-EVA dual terminal→initial edge first-reveal provenance

Date: 2026-09-07
Status: **COMMON-EVA EDGE ROBUST IN BOTH READINGS**

This document archives the first target-scoring run under the prospectively frozen Issue #145 contract. It adds provenance only; it does not change source handling, common-EVA representation, clean-run reset semantics, folds, primary population, smoothing, model family, pass rule or interpretation boundary.

## Chronology

### Merged score-free authority

Issue #145 Gate0 was merged before the scientific scorer existed:

- Gate0 PR: #146
- Gate0 merge: `692b141ac8457f4026ae482a4a8ae79a4f0fef50`
- Gate0 run: `34062035436`
- Gate0 artifact: `9997776831`
- Gate0 result JSON SHA-256: `563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48`
- Gate0 disposition: `PASS — PROCEED TO SEPARATELY COMMITTED COMMON-EVA DUAL EDGE SCORER`

### Scorer freeze before target reveal

The scientific scorer was committed separately after Gate0 merge and before any target workflow existed:

- scorer commit: `0343bf89a13ad8cefaba6de243a5789519a624bf`
- scorer file: `experiments/predictive-information/common-eva-edge/issue145_common_eva_first_reveal.py`
- scorer Git blob SHA-1: `ce8a167c607fbcf2807f567439ab6837471f4f07`

The subsequent commit added only the PR-triggered workflow:

- workflow commit / scientific head: `1a14f7d61c312829b1852b5cd7bf8c61c551de81`

No Issue #145 target score was run or inspected before that chronology was fixed.

## Authoritative first target reveal

- PR: #147
- workflow: `Issue145 common-EVA edge first reveal`
- run: `34062199123`
- scientific/workflow head: `1a14f7d61c312829b1852b5cd7bf8c61c551de81`
- run conclusion: `success`
- artifact ID: `9997826217`
- artifact name: `issue145-common-eva-edge-first-reveal-1a14f7d61c312829b1852b5cd7bf8c61c551de81`
- artifact ZIP digest: `sha256:d5d4aca2c8620e98753899b7ff675daba9739c19a0e818998fdc8c5da5acc5b8`
- result JSON: `issue145_common_eva_edge_first_reveal.json`
- result JSON SHA-256: `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`

Before scoring, the workflow re-established:

- exact Gate0 result SHA-256 `563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48`;
- exact Gate0 script blob `80585066e746f42ac10554aaaeece793682a0b84`;
- exact Gate0 provenance blob `e98d2fffac1d2500623a7f8660343ead67218332`;
- exact frozen scorer blob `ce8a167c607fbcf2807f567439ab6837471f4f07`;
- exact Phase4A/4B representation blobs;
- exact SlotParser blob;
- exact ZL3b and IT2a source hashes;
- exact physical-leaf fold authority.

## Frozen primary result

For each reading and fold:

`G_common = bits(POS2_COMMON) - bits(EDGE2_COMMON)`

A reading passed iff mean `G_common > 0` and `G_common > 0` in at least 4/5 untouched folds.

### ZL3b under common Basic-EVA

| fold | targets | run-body targets | POS2_COMMON | EDGE2_COMMON | G_common |
|---:|---:|---:|---:|---:|---:|
| 0 | 4,038 | 3,122 | 9.9590351040 | 9.8188493328 | +0.1401857712 |
| 1 | 4,392 | 3,478 | 9.9229183506 | 9.8122103146 | +0.1107080360 |
| 2 | 5,129 | 4,073 | 9.7256051381 | 9.5873823599 | +0.1382227782 |
| 3 | 4,993 | 3,976 | 9.7107278200 | 9.5625818766 | +0.1481459434 |
| 4 | 4,537 | 3,605 | 9.9096856829 | 9.7788317341 | +0.1308539488 |

Aggregate:

- mean POS2_COMMON: `9.845594419122616 bits/token`;
- mean EDGE2_COMMON: `9.711971123595143 bits/token`;
- mean `G_common`: `+0.1336232955274749 bit/token`;
- positive folds: `5/5`;
- reading PASS.

### Takahashi/IT2a under the same common Basic-EVA

| fold | targets | run-body targets | POS2_COMMON | EDGE2_COMMON | G_common |
|---:|---:|---:|---:|---:|---:|
| 0 | 4,729 | 4,031 | 9.9959523906 | 9.8274556265 | +0.1684967641 |
| 1 | 5,171 | 4,483 | 9.9027481407 | 9.7632985650 | +0.1394495757 |
| 2 | 6,020 | 5,220 | 9.6936720428 | 9.5279836717 | +0.1656883711 |
| 3 | 5,896 | 5,093 | 9.7842617523 | 9.6039178120 | +0.1803439403 |
| 4 | 5,296 | 4,649 | 9.9177229675 | 9.7624517017 | +0.1552712657 |

Aggregate:

- mean POS2_COMMON: `9.858871458784403 bits/token`;
- mean EDGE2_COMMON: `9.697021475389315 bits/token`;
- mean `G_common`: `+0.16184998339508744 bit/token`;
- positive folds: `5/5`;
- reading PASS.

## Frozen joint classification

Both readings satisfy the preregistered stability rule.

> **`COMMON-EVA EDGE ROBUST IN BOTH READINGS`**

## Implementation-equivalence and support checks

- `EDGE2_COMMON_full_run_k2_max_abs_token_logp = 0.0` in all ten reading×fold evaluations;
- unseen previous-terminal identity contexts among scored run-body targets: `0` in all ten evaluations;
- target counts reproduced Gate0 exactly;
- run-body target counts reproduced Gate0 exactly;
- no support repair or fallback addition occurred.

Thus the explicit previous-terminal→next-initial factor remains exactly the factor that distinguishes the compact observable EDGE2 representation from the generic onset model under the common atomization.

## Frozen non-promoting magnitude diagnostics

Common-representation foldwise IT2a minus ZL3b gain:

`[+0.0283109929, +0.0287415397, +0.0274655930, +0.0321979968, +0.0244173169] bit/token`

Aggregate:

- mean difference: `+0.028226687867612538 bit/token`;
- common-representation mean-gain ratio IT2a/ZL3b: `1.2112407702278882`.

For context only, the native-representation authorities had reported approximately `+0.02026956 bit/token` for the ZL3b identity increment in Issue #125 versus `+0.15211188542908544 bit/token` for IT2a in Issue #139. Those native numbers are not directly effect-size comparable because their representations/populations differ. Under the frozen common representation, the edge remains strong in both and the magnitude gap becomes much smaller.

The warranted conclusion is not that the native difference has been mathematically decomposed, but that **the architecture and a substantial effect survive a common target-blind representation in both reading lineages**. This substantially weakens an explanation based solely on one transcription's glyph encoding or exceptional-notation conventions.

## Interpretation boundary

Accepted responsibility can now be promoted to:

> a compact same-clean-run observable edge linking the previous visible unit's terminal common-EVA atom to the next visible unit's initial common-EVA atom is robustly predictive in both ZL3b and independent Takahashi/IT2a under one frozen representation and one held-out rule.

This makes a subsequent literal conditional-table / strength-transport test across transcription lineages scientifically well-posed.

It does **not** establish literal table equality, natural-language wordhood, semantics, plaintext, language, cipher family, authorship, historical direction, production mechanism, hoax/artificial origin or decipherment.

Refs #88 #112 #115 #125 #139 #145 #146 #147.
