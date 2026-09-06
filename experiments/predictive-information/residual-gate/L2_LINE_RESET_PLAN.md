# Issue #123 — L2 source-line reset scope

Date: 2026-09-06
Status: **FROZEN BEFORE L2 FIRST REVEAL**
Parent: Issue #88 / Issue #118 / Issue #121

## Question

Does the fixed-k2 boundary-edge residual require context across source-line breaks, or is context carried only across visible spaces within the same source line sufficient?

## Authority

Reuse the exact source-order corrected B3 authority and the merged Issue #119 one-cell floating-point normalization. Before any L2 score is accepted, normalized corrected-core SHA-256 must equal:

`0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`

Reuse the original five physical-leaf folds and exact parser-accepted scoring support.

## Fixed experts

All byte experts use `k=2`, `alpha=.01` and literal visible-token UTF-8 bytes followed by `END_TOKEN`.

- `RESET2`: reset byte history before every visible token.
- `LINECONT2`: carry history across visible tokens inside one source line; reset at every source-line start.
- `LEAFCONT2`: carry history across visible tokens on one physical leaf; reset only on leaf change.

No byte hyperparameter or reset topology is selected in L2.

Each expert is mixed with corrected B3 using `w=0.00..1.00` in .01 increments, selected on pooled inner-fold accepted-token likelihood only; ties go to smaller `w`.

## Primary quantities

`G_line = bits(MIX_RESET2) - bits(MIX_LINECONT2)`

`G_beyond_line = bits(MIX_LINECONT2) - bits(MIX_LEAFCONT2)`

Each passes iff mean > 0 and positive in at least 4/5 outer folds.

## Frozen classes

1. `LINE-LOCAL CONTEXT CAPTURES RESIDUAL; NO ROBUST BEYOND-LINE GAIN` — `G_line` passes, `G_beyond_line` fails.
2. `ROBUST BEYOND-LINE CONTEXT REMAINS` — both pass.
3. `LINE-LOCAL CONTEXT FAILS TO REPRODUCE` — `G_line` fails regardless of `G_beyond_line`.
4. `INVALID CORE / SUPPORT REGRESSION` — authority/support failure before valid scoring.

No post-reveal class, effect-size threshold or equivalence margin may be added.

## Parent regression

The L2 implementation must reproduce the authoritative Issue #121 RESET2↔LEAFCONT2 outer-fold contrast before interpreting line scope:

- `+0.013939262960121823`
- `+0.00811504079524461`
- `+0.00930042233496664`
- `+0.010865786933976551`
- `+0.010940638641795175`

and inner-selected weights:

- RESET2 `.04` in all five folds;
- LEAFCONT2 `.08,.08,.09,.08,.09`.

Any parent regression mismatch invalidates L2.

## Diagnostics

Report without refitting:

- all three outer mixture weights;
- foldwise `G_line` and `G_beyond_line`;
- per-target RESET2→LINECONT2 and LINECONT2→LEAFCONT2 deltas by paragraph ENTRY/BODY and line FIRST/MIDDLE/FINAL/SINGLE.

Diagnostics do not alter the frozen class.

## Firewall

No latent state, segmentation change, Currier/hand/domain conditioning, semantic/image target, plaintext, language ID, cipher-family inference or historical mechanism interpretation is allowed in this reveal.
