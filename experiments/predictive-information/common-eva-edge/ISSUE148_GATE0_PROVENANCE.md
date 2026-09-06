# Issue #148 — common-EVA literal table transport Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

This document archives the first successful score-free Gate0 for Issue #148. It does not change the common representation, physical-leaf folds, clean-run semantics, transport object, smoothing, target population or future decision rule.

## Chronology

- Issue #148 plan commit: `2ac8a5e670373b32a77fda8bc4b19eecc6e95085`;
- score-free Gate0 executable commit: `e2d49b631fce05da19e6618a32bd264d9511a056`;
- workflow head: `b5958d2dbb640485973b80d7f58b49d8871c4f42`;
- no Issue #148 cross-table scientific scorer existed before this successful Gate run.

## First successful Gate authority

- Issue: #148
- PR: #149
- workflow: `Issue148 common-EVA table Gate0`
- run: `34062417674`
- workflow head: `b5958d2dbb640485973b80d7f58b49d8871c4f42`
- conclusion: `success`
- artifact ID: `9997888389`
- artifact name: `issue148-common-eva-table-gate0-b5958d2dbb640485973b80d7f58b49d8871c4f42`
- artifact ZIP digest: `sha256:ea29d75059869ed4a692a6aba0fe9d5b3c96a2139aae4b3152ac7c7277412238`
- result JSON SHA-256: `f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf`

Gate disposition:

> `PASS — PROCEED TO SEPARATELY COMMITTED CROSS-READING TABLE SCORER`

## Reproduced Issue #145 authority

- Issue #145 Gate result SHA-256 `563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48`;
- Issue #145 Gate script blob `80585066e746f42ac10554aaaeece793682a0b84`;
- Issue #145 Gate provenance blob `e98d2fffac1d2500623a7f8660343ead67218332`;
- Issue #145 scorer blob `ce8a167c607fbcf2807f567439ab6837471f4f07`;
- Issue #145 first-reveal provenance blob `1cbb43381c57726ecc3a5b5dc5e8efc0c7b732f6`;
- Issue #145 first-reveal result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`;
- physical-leaf fold identity SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

## Directional source-context support

### ZL3b → IT2a

| fold | source contexts | source pairs | target BODY | source-context supported | unsupported | coverage |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 23 | 213 | 4,031 | 4,031 | 0 | 1.000000 |
| 1 | 23 | 219 | 4,483 | 4,483 | 0 | 1.000000 |
| 2 | 23 | 211 | 5,220 | 5,218 | 2 | 0.999617 |
| 3 | 23 | 213 | 5,093 | 5,092 | 1 | 0.999804 |
| 4 | 21 | 216 | 4,649 | 4,646 | 3 | 0.999355 |

Minimum held-out previous-terminal context coverage: `0.99935469993547`.

### IT2a → ZL3b

| fold | source contexts | source pairs | target BODY | source-context supported | unsupported | coverage |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 22 | 251 | 3,122 | 3,121 | 1 | 0.999680 |
| 1 | 22 | 250 | 3,478 | 3,474 | 4 | 0.998850 |
| 2 | 21 | 248 | 4,073 | 4,071 | 2 | 0.999509 |
| 3 | 22 | 250 | 3,976 | 3,973 | 3 | 0.999245 |
| 4 | 22 | 245 | 3,605 | 3,604 | 1 | 0.999723 |

Minimum held-out previous-terminal context coverage: `0.9988499137435307`.

In every fold/direction, supported held-out BODY events exceed the preregistered minimum of 300 by more than an order of magnitude. Source-training and target-test physical leaves are disjoint in every comparison.

## Consequence for first reveal

The literal table transport experiment is not materially support-limited at the previous-terminal context level. At most four primary BODY events in any fold lack a source-trained context. Therefore a later directional failure cannot reasonably be attributed to broad context absence under the frozen common representation.

The exact frozen rule still applies to those rare unsupported contexts: empty exact-context additive smoothing (`1/32`), with no target-native fallback.

## Firewall status

The Gate artifact records:

- no cross-table target score;
- no target likelihood or bits/token;
- no `G_transport`;
- no retention ratio;
- no target-current-first-atom support selection;
- no outcome-driven support matching;
- no atom remapping;
- no strength/temperature/mixture tuning;
- no target-native edge fallback;
- no Currier/hand/section-conditioned transport;
- no latent-state fitting;
- no S1/S2/H62/R1 tuning.

The next allowed step is to merge this Gate authority, then commit the cross-reading scorer separately before its first target workflow exists.

Refs #88 #130 #145 #148 #149.
