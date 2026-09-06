# Issue #98 Phase 2C — amendment after source-order correction

Date: 2026-09-06
Status: **FROZEN AFTER ISSUE #100 C1-C3 AND BEFORE PHASE-2C PREDICTIVE SCORING**
Parent: Issue #88

## Gate-0 resolution

The original Gate 0 failed because lexical item/document sorting was not a valid causal-history authority. Issue #100 corrected the order prospectively and reran Phase 1, Phase 2A and Phase 2B.

All three qualitative conclusions are robust to correction. Corrected quantitative authorities now supersede legacy cross-token values.

The versioned order authority is:

`experiments/predictive-information/source_order_authority.py`

It defines:

- page/panel order from first occurrence of raw ZL3b page headers;
- paragraph order from numeric `:pN` within each document;
- unchanged line/token order;
- unchanged numeric physical-leaf reset and five outer folds.

Phase 2C may now proceed only under this corrected authority.

## Corrected frozen references

### LOCAL40

All five corrected Phase-1 folds reselected `H=40,tau=32`.

Per-fold pi:

`.21, .21, .21, .21, .22`.

Mean held-out code length: `9.5943670127 bits/token`.

### Long ordered reference

All five corrected Phase-1 folds reselected:

`H=ALL, tau=128, pi=.30`.

Mean held-out code length: `9.5461691796 bits/token`.

Phase 2C does not reopen H/tau/pi.

### Corrected Phase-2B previous-paragraph authority

`LOCAL + PREV_PARAS_BAG` mean: `9.5443610736 bits/token`.

Nested previous-paragraph bag alpha by fold:

`.23, .24, .22, .22, .24`.

Corrected cross-paragraph inventory contrast:

`+0.0414587108 bit/token`, positive 5/5.

Corrected previous-paragraph actual-lag advantage over matched random lag:

`+0.0043079025 bit/token`, positive 5/5.

Thus the finer decomposition must retain both inventory and order/lag diagnostics. Inventory remains the primary source because its effect is much larger.

## Primary inventory decomposition

The original Issue #98 two decompositions remain frozen:

### Temporal

- `PREV1`: all eligible source occurrences in exactly the immediately preceding parsed paragraph on the same numeric physical leaf;
- `OLDER`: all eligible source occurrences in earlier paragraphs on that leaf, excluding PREV1;
- `ALL_PREV = PREV1 union OLDER`.

### Page-side / panel

- `SAME_SIDE_PREV`: eligible source occurrences in earlier paragraphs with the same `document` as the target paragraph;
- `CROSS_SIDE_PREV`: eligible source occurrences in earlier causal paragraphs on the same numeric physical leaf but a different `document`;
- `ALL_PREV = SAME_SIDE_PREV union CROSS_SIDE_PREV`.

`document` is treated only as an observable transcription panel/page-side identity. No semantic interpretation is attached to r/v/foldout labels.

## One-pool inventory models

For each pool:

`P = (1-alpha) P_LOCAL + alpha Q_bag(pool)`

when the pool exists, else `P_LOCAL`.

Grid:

`alpha=0.00..0.30` step `.01`.

Selection: summed nested literal-surface log likelihood within outer training only; exact tie -> smaller alpha.

## Two-pool inventory models

For temporal and page-side decompositions separately:

`P = (1-a-b) P_LOCAL + a Q_1* + b Q_2*`

where `Q_i* = Q_i` when available and `P_LOCAL` otherwise.

Frozen grid:

- `a,b=0.00..0.30` step `.01`;
- require `a+b <= .30`;
- exact tie -> smaller `a+b`, then smaller `a`, then smaller `b`.

This is a predictive attribution model, not an additive causal-share model.

## Primary inventory contrasts and classification

Temporal joint model: `TEMP2 = PREV1 + OLDER`.

- `G_prev1_cond = bits(OLDER_ONLY) - bits(TEMP2)`;
- `G_older_cond = bits(PREV1_ONLY) - bits(TEMP2)`.

Page-side joint model: `SIDE2 = SAME_SIDE_PREV + CROSS_SIDE_PREV`.

- `G_same_side_cond = bits(CROSS_SIDE_ONLY) - bits(SIDE2)`;
- `G_cross_side_cond = bits(SAME_SIDE_ONLY) - bits(SIDE2)`.

A contrast passes iff mean > 0 and positive in >=4/5 outer folds.

Temporal classification:

- PREV1 passes, OLDER fails -> `IMMEDIATE-PREVIOUS DOMINANT`;
- OLDER passes, PREV1 fails -> `OLDER-INVENTORY DOMINANT`;
- both pass -> `TEMPORAL MULTISCALE`;
- otherwise -> `TEMPORAL INCONCLUSIVE`.

Page-side classification:

- same-side passes, cross-side fails -> `SAME-SIDE DOMINANT`;
- cross-side passes -> `CROSS-SIDE TRANSPORT SURVIVES`;
- otherwise -> `SIDE INCONCLUSIVE`.

## Added order/lag localization diagnostics

Issue #100 C3 strengthened the cross-paragraph actual-lag residual. Therefore, before any Phase-2C result, add matched order/random-lag diagnostics for each of the four atomic pools:

- PREV1;
- OLDER;
- SAME_SIDE_PREV;
- CROSS_SIDE_PREV.

For each pool:

- actual source weight is frozen `exp(-d/128)` using corrected causal token lag `d`;
- matched random-lag preserves the exact eligible source occurrences, source-to-neighbour distributions and recency-weight multiset at every target;
- use exactly five fixed randomizations `0..4`;
- seed namespace contains only phase/pool/randomization/leaf/target-position and never target surface;
- no rerolls.

Actual-order and random-lag models each use LOCAL40 as base and select their own scalar mixture `alpha=0.00..0.30` step `.01` by nested likelihood. Random-lag alpha is selected by arithmetic mean inner log likelihood over the five fixed randomizations; outer code length is the arithmetic mean over those same five randomizations.

Order diagnostic for pool X:

`G_order_X = bits(RANDOM_X) - bits(ORDERED_X)`.

Use the same mean-positive + >=4/5 stability rule. These order diagnostics do not alter the primary inventory topology classification; they identify where the already-established cross-paragraph order residual resides.

Also report ordered-vs-bag for each atomic pool as a required diagnostic.

## Corrected Phase-2B regression

Before interpreting Phase 2C, the implementation must reproduce under corrected order:

- LOCAL40 mean and per-fold support;
- ALL_PREV one-pool bag nested alpha `.23,.24,.22,.22,.24`;
- ALL_PREV mean code length `9.5443610736 bits/token` within `1e-9` from recomputed fold mean.

Failure blocks interpretation.

## Cross-side availability diagnostic

CROSS_SIDE_PREV is structurally unavailable on the first page/panel represented within a numeric physical leaf. Report:

- context availability by fold;
- whole-population code-length contrasts as the primary statistics;
- restricted-to-available positions mean bits saved as a diagnostic only.

Restricted diagnostics never alter selection or classification.

## Firewall

- corrected source order fixed before scoring;
- no S1/S2/H62/R1 target metric;
- no Issue #84 target;
- no Currier/section/scribe metadata;
- no page imagery, plaintext or semantics;
- no latent state;
- no future token;
- no H/tau/window search;
- no post-reveal pool/grid/randomization additions.

## Interpretation boundary

A PREV1 effect is not syntax; an OLDER effect is not topic; a same-side effect is not semantic page state; cross-side survival is not content transport. These labels only localize held-out predictive information under the current space-delimited production-unit representation.