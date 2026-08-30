# Phase 54 — paragraph-boundary specificity

Status: development diagnostic. Paragraph boundaries and all relevant targets are exposed.

## Why this phase

Phase 53 showed that simple paragraph-local topic/family concentration can increase the paragraph reset, but only by over-producing generic short-range clustering. Phase 54 asks what temporal shape a successful mechanism actually has to reproduce.

## Shifted-boundary test

The same adjacent-line edit-distance-1 family continuity statistic was recomputed after shifting every paragraph-start label by -6 through +6 lines within each folio.

Mean within-minus-boundary gap:

- shift -1: -0.0145
- **true boundary 0: +0.1153**
- shift +1: +0.0332
- shift +2: -0.0535

All other shifts are near zero relative to the true boundary. At the true boundary, 88/99 eligible folios have a positive gap.

This is much sharper than a generic paragraph-level stationary topic effect.

## Recovery after paragraph start

Mean adjacent-line near-family continuity by current line's distance from the paragraph start:

- first paragraph line (0): **0.1326**
- line 1: 0.2172
- line 2: 0.2876
- line 3: 0.2885
- line 4: 0.2919
- line 5: 0.2822
- line 6: 0.2660

The discontinuity is therefore concentrated at paragraph entry, followed by rapid recovery over roughly the next two lines.

## Interpretation

The generator target is now more precise:

> a boundary-triggered transient reconfiguration followed by rapid relaxation into an ordinary within-paragraph regime.

This is different from assigning each paragraph a stationary restricted vocabulary or topic distribution. Those mechanisms naturally raise within-paragraph local clustering, which Phase 53 showed is too strong relative to Voynich.

The shape is compatible with several mechanism families and does not decide among them:

- discourse/entry morphology at paragraph openings;
- a cipher/key/state initialization that relaxes or mixes after entry;
- a formal generator with a paragraph-entry state followed by transition to a shared steady regime;
- mixed mechanisms.

## Falsifiable next mechanism

A minimal next generator should add **one transient paragraph-entry state** with a predeclared decay schedule, rather than a stationary paragraph-local root pool. It succeeds only if it raises the true-boundary gap while preserving the observed modest generic local excess and the Phase 50 density target.

Because this mechanism is directly motivated by Phase 54, its fit to these dimensions is model development, not validation. New dimensions must be reserved before any later validation claim.
