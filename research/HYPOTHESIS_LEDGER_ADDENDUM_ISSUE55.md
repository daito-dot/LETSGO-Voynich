# Hypothesis ledger addendum — Issue #55

Date: 2026-08-31

This file records the hypothesis-neutral follow-up to the failed E10 Sloane 351 music-cipher interpretation. Exact methods and provenance remain controlled by the issue-specific plans and reports.

## #55A — native slot3×slot5 dependence transfers across physical leaves

Origin:

- E10 selected the same complete slot3×slot5 fitted key in 4/5 folds but produced unreadable, collapse-dominated plaintext.
- #55A removed Sloane, music, Latin likelihood, plaintext decoding and all historical ordering.

Prediction:

- a slot3↔slot5 relation learned on four physical-leaf folds should improve prediction on the untouched fifth beyond line-local marginal composition.

Result:

- mean symmetric held-out gain: `0.04417745 bits/token`;
- all five folds positive;
- within-line pair-destruction null p `0.000999001`;
- advantage over null median `0.04113104 bits/token`;
- cyclic-misalignment sensitivity also p `0.000999001`.

Status: **SUPPORTED STRUCTURE — `CROSS-LEAF SLOT3xSLOT5 DEPENDENCE`**.

Permitted interpretation:

- a stable manuscript-native relation exists between the two factors.

Prohibited inference:

- 25-symbol cipher, Sloane plaintext, music, semantic meaning or direct causation.

Disposition:

- decompose occupancy versus subtype before any interpretation.

## #55B — the dependence contains subtype information beyond occupancy

Prediction:

- if the 5×5 relation is richer than EMPTY/nonEMPTY exclusion, full subtype identity should add held-out predictive information beyond a frozen occupancy-only interaction model.

Result:

- full five-state gain: `0.0441774454`;
- binary occupancy gain: `0.0442150445`;
- occupancy fraction of full gain: `1.0008510918`;
- mean residual subtype gain: `-0.0000374707`;
- residual folds positive: 2/5;
- occupancy-preserving subtype-null p: `0.2697302697`;
- residual advantage over null median: `0.0000586212 bits/token`;
- parser admits 24/24 nonempty canonical slot3×slot5 combinations;
- only three observed parsed tokens have both slots nonempty.

Status: **NOT SUPPORTED AS SUBTYPE CODE — `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`**.

Permitted interpretation:

- #55A remains a real cross-leaf morphotactic constraint;
- slot3 and slot5 behave as almost mutually exclusive token-construction channels;
- the exclusion is not forced by simple parser inadmissibility.

Prohibited inference:

- rich 5×5 paired-state code;
- subtype correspondence between `t/k/p/f` and `cth/ckh/cph/cfh`;
- Sloane/music/plaintext evidence;
- semantic labels for the slots.

Disposition:

- treat slot3×slot5 as a previously selected pair and test its specificity against the complete 12-slot occupancy graph before constructing any transform interpretation.
