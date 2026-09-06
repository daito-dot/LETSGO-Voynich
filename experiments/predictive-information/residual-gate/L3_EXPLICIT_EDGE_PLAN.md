# Issue #125 — L3 explicit terminal-to-initial edge identity

Date: 2026-09-06
Status: **FROZEN BEFORE L3 FIRST REVEAL**
Parent: Issue #88 / Issue #118 / Issue #121 / Issue #123

## Question

Issue #123 confirmed that the useful fixed-k2 byte context is line-local. L3 asks whether that line-local gain is genuinely token-to-token identity information or can be explained by a simpler observable fact: source-line-start tokens and source-line-interior tokens have different onset distributions.

## Authority

Reuse the exact corrected source-order B3 authority, original five physical-leaf folds, literal visible-token bytes, parser-accepted scientific support and merged Issue #119 one-cell floating-point normalization.

Before L3 scoring, normalized corrected-core SHA-256 must equal:

`0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`.

All onset/edge experts use fixed `k=2`, additive `alpha=.01`, byte vocabulary size `257` and `END_TOKEN=256`.

## Explicit decomposition

For a source-line-start token, k2 line-continuous history begins from BOS.

For a source-line-interior token, the first emitted symbol sees `(previous_token_final_byte, END_TOKEN)`, the next emitted symbol sees `(END_TOKEN, current_first_byte)`, and from the third emitted symbol onward both history symbols are inside the current token.

L3 therefore defines three explicit experts.

### RESET2

The existing token-reset k2 expert from Issue #123.

### POS2

Line-position onset model with no previous-token identity:

- first symbol at line start: distribution learned from source-line-start tokens;
- first symbol in line body: one distribution pooled over all source-line-interior tokens, ignoring the previous token;
- next symbol conditional on current first symbol, separately for line-start and line-body tokens; this outcome may be a raw byte or `END_TOKEN`;
- third and later emitted symbols use the ordinary shared within-token k2 transition table.

### EDGE2

Exactly POS2 except for the first symbol of a line-body token:

- condition on the previous visible token's final raw byte.

All other probability factors are identical to POS2.

## Required equivalence to Issue #123 LINECONT2

EDGE2 is intended as an explicit factorization of the already-frozen LINECONT2 expert, not a new flexible family.

For every inner and outer training/evaluation split, before L3 interpretation:

- train the Issue #123 LINECONT2 byte model;
- score the exact same accepted targets;
- require `max_abs(EDGE2_token_logp - LINECONT2_token_logp) <= 1e-12`;
- require equal visible and accepted support.

The resulting EDGE2 mixed outer model must also reproduce the frozen Issue #123 LINECONT2 weights and RESET2→LINECONT2 `G_line` values:

`G_line = [0.03339038902518254, 0.02093212050888482, 0.03017008407788957, 0.02839973265948892, 0.03291474485290813]`

LINECONT2/EDGE2 weights:

`[.15, .16, .15, .15, .15]`

RESET2 weights:

`[.04, .04, .04, .04, .04]`

Any mismatch is `INVALID EDGE DECOMPOSITION / SUPPORT REGRESSION` and blocks L3.

## Mixture protocol

For RESET2, POS2 and EDGE2 separately:

`p_mix = (1-w) p_B3 + w p_expert`

with `w=0.00,0.01,...,1.00`.

Select `w` by pooled inner accepted-token likelihood only; ties go to smaller `w`. Score the untouched outer fold once.

## Primary quantities

`G_position = bits(MIX_RESET2) - bits(MIX_POS2)`

`G_identity = bits(MIX_POS2) - bits(MIX_EDGE2)`

Each passes iff mean > 0 and positive in at least `4/5` outer folds.

Foldwise identity must satisfy the arithmetic decomposition:

`G_position + G_identity = frozen Issue123 G_line`

within `1e-12`.

## Frozen classes

1. `TERMINAL→INITIAL IDENTITY ADDS ROBUST LINE-LOCAL INFORMATION` — `G_identity` passes.
2. `LINE-POSITION ONSET EXPLAINS LINECONT2 ADVANTAGE` — `G_identity` fails and `G_position` passes.
3. `NEITHER COMPACT ONSET COMPONENT ROBUSTLY EXPLAINS L2` — both fail despite valid EDGE2 equivalence.
4. `INVALID EDGE DECOMPOSITION / SUPPORT REGRESSION` — any pre-interpretation authority/equivalence/support failure.

No post-reveal class or effect-size threshold may be added.

## Diagnostics

Report without affecting the class:

- outer weights and raw/mixed bits for RESET2/POS2/EDGE2;
- foldwise `G_position`, `G_identity` and their sum;
- max EDGE2↔LINECONT2 log-probability difference for every split;
- training support counts: line-start tokens, line-body tokens, unique previous-terminal bytes, first-symbol outcome counts, onset second-symbol context counts and shared within-token k2 contexts;
- held-out contributions for RESET2→POS2 and POS2→EDGE2 grouped by paragraph ENTRY/BODY and line FIRST/MIDDLE/FINAL/SINGLE.

## Firewall

No latent-state fit, segmentation change, Currier/hand/domain conditioning, target scorecard, semantic/image target, plaintext/language/cipher inference or historical production-mechanism claim is allowed in this reveal.

If terminal identity survives, the next licensed step is transport/observable-regime testing of this compact edge and then a residual-after-edge capacity test before latent-state interpretation.
