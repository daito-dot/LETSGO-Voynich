# Issue #151 — shared common-EVA edge consolidation plan

Status: **FROZEN BEFORE SHARED-TABLE TARGET SCORING**
Date: 2026-09-07
Parent: Issue #88
Entry result: closed Issue #148 / merged PR #150

## Entry authority

Issue #148 frozen classification:

> **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**

Authority:

- Issue #145 common-EVA scorer blob `ce8a167c607fbcf2807f567439ab6837471f4f07`;
- Issue #145 first-reveal result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`;
- Issue #148 Gate script blob `a8029aac50ccc6e09ec975b7b86a1bde44415f9f`;
- Issue #148 Gate provenance blob `7f97b9731a6e72e2456ede436e837a3735f265fd`;
- Issue #148 Gate result SHA-256 `f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf`;
- Issue #148 first-reveal scorer blob `7847c0fea1dcfc4ace5752d0188d70e3739679d3`;
- Issue #148 authoritative run `34073660425`;
- Issue #148 artifact `10001309613`, ZIP digest `sha256:cfefd670b00ebb3eae3020a4b5308115ec9172b793ed1fe4b598928718f5c622`;
- Issue #148 result SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`;
- Issue #148 merge `b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131`;
- physical-leaf fold identity SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

## Question

Does either reading retain reproducible held-out predictive information beyond one fixed reading-balanced common-EVA previous-terminal→next-initial table?

## Frozen representation / population

Reuse Issue #145/#148 exactly:

- exact ZL3b / Takahashi-IT2a authorities;
- Phase4A/4B target-blind common Basic-EVA representation;
- 25 single atoms + 6 composites, `END_TOKEN`, `V=32`;
- literal IVTFF `.` certain-space segmentation;
- maximal contiguous clean runs;
- reset at line start and after every unclean segment;
- unchanged five physical-leaf folds;
- fixed `k=2`, `alpha=0.01`;
- unchanged SlotParser primary target;
- previous clean unit need not be SlotParser accepted;
- no context crosses an unclean segment.

No representation or population repair is allowed after reveal.

## Frozen models

For target reading `T` and outer fold `f`, all edge counts use physical leaves outside `f` only.

### POS2_TARGET

Issue #145 target-native generic onset model.

### EDGE2_NATIVE_T

Issue #145 target-native edge model.

### EDGE2_SHARED

All non-edge factors are target-native. Only BODY first-atom counts conditional on previous terminal are shared:

`C_SHARED(ctx,outcome) = 0.5*C_ZL3b(ctx,outcome) + 0.5*C_IT2a(ctx,outcome)`.

The weights are fixed and untuned. They preserve approximately one-reading count scale instead of doubling effective sharpness merely because the same physical manuscript has two transcriptions.

Missing cells contribute zero. Missing exact contexts use the same empty exact-context additive rule under `alpha=0.01`; no target-native fallback, pooled fallback, scalar, temperature, calibration, interpolation or mixture is allowed.

## Primary quantities — future scorer only

`G_shared[T,f] = bits(POS2_TARGET) - bits(EDGE2_SHARED)`

`G_specific[T,f] = bits(EDGE2_SHARED) - bits(EDGE2_NATIVE_T)`

A reading-specific residual is robust iff mean `G_specific > 0` and `G_specific > 0` in at least 4/5 untouched folds.

A valid shared-table consolidation also requires mean `G_shared > 0` and positive 4/5 in **both** readings.

## Frozen classes

Exactly one:

1. `ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`
2. `ZL3B RETAINS READING-SPECIFIC EDGE INFORMATION`
3. `IT2A RETAINS READING-SPECIFIC EDGE INFORMATION`
4. `BOTH READINGS RETAIN READING-SPECIFIC EDGE INFORMATION`
5. `INVALID SHARED EDGE CONSOLIDATION`

No equivalence margin and no post-reveal rescue class.

## Mandatory Gate0

Before any real `EDGE2_SHARED` target likelihood is computed, the Gate must:

1. re-run and hash-check the score-free Issue #148 Gate;
2. pin Issue #145/#148 scientific file blobs and declared result authorities;
3. reproduce physical-leaf folds and exact target support;
4. prove held-out fold leaves are absent from **both** readings' consensus training counts;
5. audit per-reading training clean/BODY counts;
6. archive each reading's training edge-cell support by previous-terminal context and current first atom;
7. construct the exact fractional `0.5/0.5` training-only consensus and archive its support;
8. audit held-out primary BODY events for previous-terminal context presence only, without outcome-based selection;
9. require at least 300 primary BODY targets and at least 300 consensus-context-supported BODY targets per reading/fold;
10. perform a target-free synthetic fractional-count arithmetic/smoothing self-test;
11. record that no real shared-table target probability, likelihood, bits/token, `G_shared`, `G_specific`, retention or scientific classification was computed.

If any authority or support check fails, stop INVALID. Do not repair after target scoring.

## Non-promoting diagnostics allowed after reveal

Prospectively allowed only after the primary quantities are frozen:

- shared/native retention ratio;
- shared vs opposite-source table gain;
- training-only per-context Jensen-Shannon divergence;
- training count imbalance;
- equal-context/count-weighted descriptive summaries;
- directional asymmetry.

None can change the frozen class.

## Firewall

This issue must not:

- change atomization, uncertainty handling, segmentation, folds or target population;
- align readings by held-out current first-atom outcomes;
- tune consensus weights;
- tune `k`, `alpha`, smoothing, fallback, scalar, temperature or mixture;
- include held-out physical leaves from either reading in consensus counts;
- fit Currier/hand/section-specific shared tables;
- fit latent states;
- tune S1/S2/H62/R1;
- infer words, plaintext, semantics, language/cipher family, authorship, historical direction, artificiality/hoax or decipherment.

Refs #88 #125 #130 #134 #139 #145 #148 #150 #151.