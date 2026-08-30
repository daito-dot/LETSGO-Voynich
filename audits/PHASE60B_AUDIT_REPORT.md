# Phase 60B cross-fit audit report

Date: 2026-08-30

Status: audit-only; `main` experiment files are unchanged.

## Question

Does correcting the public Phase 60B reimplementation change the accepted scientific interpretation that the paragraph-entry transition survives physical-leaf held-out evaluation and is carried by a stable combination of token-length/TTR, near-family/local-continuity, and k/t-related structure?

## Exact input

The audit downloads `eva_zl3b.txt` from the public Aspect-Research transcription repository and verifies the Git blob SHA-1 before analysis:

`2a4533ab9bdfa85db9bad602d590978953055df1`

This is the same source identity documented by this project.

## Problems tested

The current public `phase60b_feature_attribution.py` has two reproducibility issues relevant here:

1. it constructs training-fold directions, but its final reported pooled projection replaces them with a direction estimated from all held-out deltas;
2. feature standard deviations are estimated once from all eligible lines rather than from the training leaves inside each fold.

The audit therefore compares:

- the current pooled-held-out-direction behavior;
- true fold-specific training direction with the existing global scaling;
- true fold-specific training direction with training-only scaling.

No accepted result file is overwritten.

## Primary corrected replay on the current public parser

The current parser yields 594 real-entry-eligible paragraphs and 431 paragraphs that also have at least one eligible internal pseudo-boundary. The latter exactly matches the Phase 60A paired sample size.

### Corrected cross-fit mean projection

| representation | accepted Phase60B reference | corrected, global scaling | corrected, training-only scaling |
|---|---:|---:|---:|
| raw EVA | 1.0072 | 0.9039 | 0.9017 |
| conservative composites | 0.9194 | 0.7534 | 0.7495 |
| Phase56 composites | 1.1182 | 0.9361 | 0.9326 |

Training-only scaling changes the corrected score only minimally relative to global scaling. The important correction is retaining the fold-specific training direction.

### Raw-EVA fold results under the stricter correction

`[0.6748, 1.5039, 0.4504, 0.4852, 1.4505]`

All five physical-leaf folds remain positive.

For comparison, the frozen Phase60A anti-circular raw-EVA fold results were approximately:

`[0.672, 1.491, 0.467, 0.485, 1.458]`

with weighted mean `0.904`.

The near identity is an important internal validation that the corrected fold implementation is reproducing the already-frozen Phase60A held-out calculation on the shared 431-paragraph sample.

The conservative and Phase56 representations also remain positive in all five folds under training-only scaling:

- conservative: `[0.5932, 1.3366, 0.3071, 0.2827, 1.2990]`
- Phase56: `[0.6344, 1.4784, 0.5931, 0.5913, 1.3895]`

## Historical Phase60B n=380 eligibility

The accepted Phase60B result reports `n=380`. The current public parser/eligibility rules do not reproduce that count.

A sensitivity search over simple combinations of line-first-token exclusion and minimum line token counts produced paired sample sizes:

- no first-token exclusion: 469, 431, 365, 289, 205 for minimum token counts 4..8;
- first-token excluded: 431, 365, 289, 205, 130 for minimum token counts 4..8.

None equals 380. Therefore the exact historical eligibility/parser detail used for accepted Phase60B remains unrecovered. The audit must not claim exact replay of the accepted Phase60B effect sizes.

The nearest simple scenario was 365 paired paragraphs (no first-token exclusion, minimum 6 tokens). Under the strict corrected cross-fit, mean projections were:

- raw EVA: `1.0446`
- conservative: `0.8947`
- Phase56: `1.0553`

Again every fold was positive in every representation. These values are close to the accepted Phase60B headline means despite the remaining eligibility mismatch.

## Carrier sensitivity

On the 365-paragraph sensitivity sample, signed standardized real-minus-pseudo effects with physical-leaf cluster bootstrap were stable in the same broad directions as the accepted Phase60B result.

### Raw EVA

- TTR: `-0.4381`, 95% `[-0.6523, -0.2172]`
- mean length: `-0.6744`, 95% `[-0.8356, -0.5038]`
- edit1 fraction: `+0.4218`, 95% `[+0.2359, +0.6005]`
- local previous-10 near-family: `+0.4128`, 95% `[+0.2186, +0.5992]`
- k/t mass: `+0.6140`, 95% `[+0.4309, +0.7992]`
- k share: `+0.2188`, 95% `[+0.0469, +0.4059]`
- last-unit entropy: `+0.2488`, 95% `[+0.0596, +0.4346]`

The same key signs survive conservative and Phase56 representations. Exact magnitudes and the fine ranking of secondary carriers differ from the frozen n=380 result, so those details remain provenance-sensitive.

## Scientific decision

**The high-level Phase60 interpretation does not reverse under the corrections tested.**

Supported after audit:

- the real paragraph-entry transition remains positive under genuine physical-leaf cross-fitting;
- it remains positive in every fold and across all three reasonable EVA representations tested;
- training-only feature scaling has negligible impact on the conclusion;
- near-family/edit1, local previous-10 continuity, k/t-related structure, lower TTR, and shorter tokens remain robust carriers in the sensitivity replay.

Not yet certified:

- the exact accepted Phase60B `n=380` sample;
- exact Phase60B effect sizes and carrier ranking;
- the current public script as an exact replay of `phase60b_results.json`.

The appropriate revised wording is:

> The paragraph-entry transition remains robustly cross-fitted and is consistently associated with lower TTR/shorter-token structure together with increased edit1/local-near-family and k/t-related structure. Exact contribution rankings and effect sizes remain dependent on recovery of the historical Phase60B eligibility implementation.

## Consequence for Phase61

This audit does not undermine the motivation for Phase61C. In particular, local near-family activation remains a robust component of the observed entry/body transition, so A0's severe local-family deficit remains scientifically relevant.

Before executing Phase61C, its implementation should contain one canonical parser/eligibility policy, one canonical definition for `local_prev10`, entry projection and line-position statistics, and training-only preprocessing/model selection. That implementation should be frozen together with the A0 baseline so that A1 differs by exactly the mechanism allowed in `PLAN_C.md`.

## Audit artifacts

Workflow run: `33311940729`

Audit scripts:

- `audits/phase60b_crossfit_audit.py`
- `audits/phase60b_eligibility_carrier_audit.py`

The workflow produced the machine-readable JSON outputs as the `phase60b-crossfit-audit` artifact.
