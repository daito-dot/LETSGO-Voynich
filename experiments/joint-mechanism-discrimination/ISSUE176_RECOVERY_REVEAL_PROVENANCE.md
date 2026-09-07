# Issue #176 — historical-anchor recovery reveal provenance

Date: 2026-09-07
Status: **COMPLETE — INTERPRETABLE RECOVERY REVEAL**

## Frozen execution authority

- recovery base main: `54fb4f9a5122dfc64ae3fbf24633bb80380a5365`
- recovery plan blob: `6b05aa0dbe9dc57e55527b2123806c8d2d6582b9`
- accepted preflight authority blob: `cb8f4e7a743711288dd97a3d39955147612a1332`
- accepted preflight raw JSON SHA-256: `ef617c63e7ed48e709797bd1ba0f284832c880b69f3c00a082b0e75420d8e367`
- recovery wrapper blob: `cd79047d12244350fccc6130379fa2e5726bab76`
- frozen Issue #172 v1 scorer blob: `f90f194396acdc50599cf9713dbbeb3ab5b4bed3`
- scientific workflow head: `34bd6e0cba08441a61d79515a2bc6b36e93655d3`
- scientific workflow blob: `4a1cd0ae7c13b6ca4ef49a9b1edd5bf5cfe271cf`
- workflow ID: `352224359`
- run ID: `34114462636`
- run attempt: `1`
- job ID: `101717935665`
- workflow/job conclusion: `success`
- scorer exit code: `0`
- artifact ID: `10015772712`
- artifact name: `issue176-historical-anchor-recovery-reveal`
- artifact ZIP digest: `sha256:9b2007d583379901c103f828d42d01d071f2c599811d1dd7ef7c3612b086b2f9`
- raw result JSON SHA-256: `d6149607aa90530b02d440899d7abb23c28e44a51ff270205e919a3f00d17b35`

The SHA-256 recorded inside the workflow artifact and an independent SHA-256 over the downloaded raw JSON bytes matched exactly before interpretation.

External authorities were rechecked immediately before scoring:

- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- Naibbe commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`

No candidate, surface, seed, representation, threshold, fold, source population, codebook, target-access rule, or scientific scoring function changed after the accepted score-free preflight.

## Frozen outcome

Both historical anchors are classified as:

> **`PARTIAL STRUCTURAL MODEL`**

Neither is `JOINT-STRUCTURAL COMPETITIVE`.

### A1 / A1-R1 — surface generator

| Responsibility | Outcome | Main evidence |
|---|---|---|
| R1 production-boundary asymmetry | PASS | pooled `D_RESET=5.9006`; shift-left `-5.9531`; shift-right `-3.6763` |
| R2 complete66 residual geometry | FAIL | representation coverage `12650/32570 = 0.3884 < 0.60` |
| R3 cross-token/profile package | PASS | `S2 ratio=1.5666`; raw H62 ratio `5.0164`; mean D-profile `0.7551`; mean short-C diff `0.10987` |
| R4 paragraph-entry S1 | PASS | candidate mean `0.54781`; target mean `0.87599`; ratio `0.62536` |
| R5 common-EVA previous-terminal edge | FAIL | same-line gain mean `-0.02366`, positive folds `0/5`; beyond-line continuation is instead robust positive `5/5` |
| R6 reading-invariant edge table | FAIL | no per-reading tuning, but R5 responsibility itself fails |
| R7 Currier-conditioned edge structure | FAIL | Currier A mean `-0.04495`, B mean `-0.00720`, both `0/5` positive; no sufficient K through 16 |
| R8 prior-paragraph inventory beyond LOCAL40 | FAIL | previous-paragraph gain `0.01739`, below target band lower bound `0.02072935`; same-line inventory is also robust positive (`5/5`, mean `0.02658`) when it should not be |
| R9 decoder closure | N/A | surface-generator role |
| R10 complexity / target access | PASS | Issue #172 trainable scalars `0`; no post-reveal selection or candidate-specific repair |

A1 therefore reproduces the **within-token/boundary and paragraph-entry/profile layer** but not the required common-EVA edge, Currier-conditioned, or clean longer-range inventory layer.

### Naibbe C1-E0 — reversible transform / decoder candidate

| Responsibility | Outcome | Main evidence |
|---|---|---|
| R1 production-boundary asymmetry | PASS | pooled `D_RESET=9.7905`; shift-left `-9.0418`; shift-right `-5.9654` |
| R2 complete66 residual geometry | PASS | coverage `29759/33574 = 0.8864`; ZL3b Pearson `0.8830`, sign `60/66`; IT2a Pearson `0.9001`, sign `61/66`; all maxT p `≈0.000999` |
| R3 cross-token/profile package | FAIL | `S2 ratio=0.02259`; raw H62 ratio `0.2273`; mean D-profile `1.2013`; mean short-C diff `0.4690` |
| R4 paragraph-entry S1 | FAIL | candidate mean `-0.04976` versus positive target mean `0.87599` |
| R5 common-EVA previous-terminal edge | FAIL | same-line gain mean `-0.00554`, positive folds `0/5`; beyond-line continuation robust positive `5/5` |
| R6 reading-invariant edge table | FAIL | no per-reading tuning, but R5 responsibility itself fails |
| R7 Currier-conditioned edge structure | FAIL | frozen `FAIL_NO_CURRIER_COMPARABLE_CHANNEL`; no numerical target score computed |
| R8 prior-paragraph inventory beyond LOCAL40 | PASS | previous-paragraph gain mean `0.02940`, positive `5/5`, inside target band; same-line inventory exactly `0` in all folds; no future leakage |
| R9 decoder closure | FAIL | unique exact recovery `1167/1778 = 0.65636`, required `1.0` |
| R10 complexity / target access | PASS | Issue #172 trainable scalars `0`; public fixed target-aware codebook charged, no post-reveal fitting |

Naibbe therefore reproduces the **production-boundary, complete66 residual geometry, and clean longer-range prior-inventory layer**, but not the cross-token/profile package, paragraph-entry effect, common-EVA edge/Currier layer, or exact decoder closure.

## Mechanism-discrimination consequence

The historical anchors split the post-#88 contract rather than one dominating the other:

- shared success: **R1**;
- A1-only success among the scored structural responsibilities: **R3, R4**;
- Naibbe-only success: **R2, R8**;
- shared failures: **R5, R6**;
- R7: A1 numerically fails; Naibbe has no comparable Currier channel;
- decoder-specific R9: Naibbe fails exact closure;
- both satisfy R10 under the frozen historical-anchor accounting.

This is the useful calibration result: the current evidence is not pointing to either old anchor as a complete mechanism. It says the next mechanism search must explain **at least four structural layers that the historical anchors split across**: local production/boundary formation, complete66 residual geometry, paragraph/profile organization, and longer-range inventory memory, while also solving the common-EVA edge/Currier responsibilities that neither historical anchor captures.

The result does **not** license combining A1 and Naibbe ad hoc. Any composite or new mechanism must be specified independently before scoring and must pay its full R10 complexity/target-access cost.

## Interpretation boundary

This calibration says nothing by itself about plaintext semantics, natural-language wordhood, language family, cipher family, authorship, historical provenance, artificiality/hoax, or decipherment. It is a structural mechanism-discrimination result only.

Refs #68 #88 #172 #175 #176.
