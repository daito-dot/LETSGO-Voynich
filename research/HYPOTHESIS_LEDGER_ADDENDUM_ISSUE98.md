# Hypothesis Ledger Addendum — Issue #98 / Issue #88 Phase 2C

Date: 2026-09-06
Authority: `experiments/predictive-information/phase2c/REPORT.md`

## P98-1 — the dominant previous-paragraph inventory is mainly the immediately preceding paragraph

**State before Phase 2C:** LIVE.

**Result:** **REJECTED as the dominant explanation.**

Both temporal pools are conditionally predictive, but the magnitudes are strongly asymmetric:

- PREV1 conditional gain: `+0.0070407 bit/token`, positive 5/5;
- OLDER conditional gain: `+0.0367964 bit/token`, positive 5/5.

Formal temporal class: **TEMPORAL MULTISCALE**.

The immediately previous paragraph matters, but most of the slower inventory signal resides in accumulated older paragraphs.

## P98-2 — older paragraph inventory carries predictive information beyond PREV1

**State:** **SUPPORTED STRONGLY.**

OLDER remains predictive after PREV1 is separately available in the jointly nested model. The effect is stable 5/5 and substantially larger than the reciprocal PREV1 conditional effect.

This establishes predictive relevance of accumulated older paragraph inventory, not topic, semantics, or a literal historical memory store.

## P98-3 — the previous-paragraph inventory is confined to the same transcription page/panel

**State before Phase 2C:** LIVE.

**Result:** **REJECTED under the corrected structural control.**

Conditional inventory gains:

- SAME_SIDE_PREV given cross-panel history: `+0.0205711 bit/token`, positive 5/5;
- CROSS_SIDE_PREV given same-panel history: `+0.0237448 bit/token`, positive 5/5.

Formal side class: **CROSS-SIDE TRANSPORT SURVIVES**.

Cross-panel history exists for about 50.83% of scored positions and contributes independently. This is structural predictive transport across the transcription panel/page-side boundary within the same numeric physical leaf. It is not semantic/content transport.

## P98-4 — same-panel and cross-panel inventory are redundant descriptions of one homogeneous leaf-prefix pool

**State:** **WEAKENED.**

The jointly nested same+cross panel model reaches `9.5421029 bits/token`, versus `9.5443611` for the unsplit ALL_PREV bag, and allocates substantial weight to both components in every fold.

This suggests the panel split exposes real predictive heterogeneity rather than merely repartitioning a homogeneous pool. The improvement is modest, so it does not identify the underlying state.

## P98-5 — the corrected cross-paragraph order residual is concentrated in PREV1

**State:** **REJECTED.**

Matched random-lag contrasts:

- PREV1: `-0.0002645 bit/token`, positive 1/5, FAIL;
- OLDER: `+0.0057373`, positive 5/5, PASS.

The order-sensitive residual is associated with older paragraph history, not the immediately previous paragraph.

## P98-6 — cross-panel source/lag association contains no residual order information

**State:** **REJECTED WEAKLY / SUPPORTS SMALL RESIDUAL.**

- SAME_SIDE_PREV actual lag vs random lag: `+0.0001767`, positive 3/5, FAIL;
- CROSS_SIDE_PREV actual lag vs random lag: `+0.0022930`, positive 4/5, PASS.

Thus a small whole-population cross-panel order-sensitive residual survives the preregistered stability rule. Its restricted-to-cross-context diagnostic is slightly negative, so this should not be elevated into a strong historical mechanism claim.

## P98-7 — one fixed token-distance horizon is an adequate mechanistic description

**State:** **REJECTED as the main explanatory framing.**

The corrected hierarchy requires at least:

1. short local recency (`H=40,tau=32`);
2. a slower accumulated paragraph inventory dominated by OLDER;
3. independent same-panel and cross-panel inventory contributions;
4. a smaller order-sensitive component concentrated in OLDER / CROSS_SIDE.

A single distance kernel can predict some of this structure, but it conflates distinct observable document scales.

## P98-8 — rich latent-state fitting is now licensed

**State:** **REJECTED / still blocked.**

The next licensed step is transport across independently authoritative manuscript strata and explicit separation of support/vocabulary mismatch from mechanism mismatch.

Currier/section/scribe or equivalent observable metadata should be frozen independently before scoring. Only a reproducible residual that survives these observable-state and transport tests can license a richer latent-state model.

## Program consequence

The corrected working predictive hierarchy is now:

1. compact token-internal V2 construction;
2. stable short local edit-1 recency;
3. slower paragraph-scale token-family inventory;
4. within that slower inventory, accumulated OLDER paragraphs dominate over PREV1;
5. same-panel and cross-panel previous inventories both contribute;
6. smaller actual-lag information is concentrated in OLDER and weakly in CROSS_SIDE;
7. observable line/paragraph position contributes additional prediction.

Next: Phase 3 transport / independently authoritative manuscript-stratum attribution. No semantic or latent-state branch is licensed by Phase 2C alone.