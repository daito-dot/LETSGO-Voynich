# Issue #109 Phase 3C — pure-Herbal matched-domain Gate 0

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE RESULT**
Parent: Issue #88

## Result

> **PASS — PROCEED TO MATCHED HERBAL TRANSPORT**

The conservative whole-leaf restriction leaves enough Currier A and B Herbal data in every original physical-leaf fold to run the preregistered transport test without deleting tokens inside leaves or changing fold assignments.

## Matched populations

### Currier A / Herbal

- 46 leaves
- 177 items
- 7,387 visible tokens
- 5,462 parser-accepted tokens
- fold accepted counts: `1376, 851, 1328, 1070, 837`

### Currier B / Herbal

- 15 leaves
- 63 items
- 3,153 visible tokens
- 2,382 parser-accepted tokens
- fold accepted counts: `179, 753, 417, 466, 567`

All ten A/B-by-fold cells are nonzero.

## Why the whole-leaf restriction matters

Phase 3C does not remove non-Herbal tokens from otherwise mixed leaves. Such filtering would shorten LOCAL40 distances and alter previous-paragraph causal histories. Instead, a leaf is either entirely retained or entirely excluded according to metadata fixed before prediction.

This reduces the raw Phase-3B Herbal support slightly—from A 5,520/B 2,449 accepted tokens to A 5,462/B 2,382—but preserves the meaning of the existing mechanism family.

## Next experiment

The next predictive scorer may now repeat the exact Phase-3A target-support mechanism transport on these pure-Herbal leaves:

- target-side V2 emission/support;
- LOCAL40 fixed `H=40,tau=32`, scalar `pi`;
- order-free PREV_PARAS, scalar `alpha`;
- grids `0.00..0.30` step `.01`;
- original five folds;
- source-only parameter selection and target-only nested oracle.

The primary question is whether the all-domain Phase-3A PREV classification (`A->B ONLY`) becomes bidirectional after matching domain, remains one-directional, or disappears.

No hand-conditioned or latent-state model is licensed by this Gate.

## Provenance

Authoritative run `34022201125`; artifact `9985870190`; result JSON SHA-256 `ec8c1dcb14f4450fe6e9f42d80ad00a60872719553c5ee46c153287723f705d8`.

See `PURE_HERBAL_GATE0_PROVENANCE.md`.