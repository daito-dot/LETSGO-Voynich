# Phase 54 — paragraph-boundary specificity

Status: development diagnostic. Paragraph boundaries and all relevant targets are exposed.

## Audit note added in Phase 55

The original Phase53 parser collapsed `f1r` and `f1v` to the common leaf id `f1` via `re.match(r'f\d+', loc)`. Phase54 inherited that parser. The original headline therefore mixed recto/verso page-sides inside a leaf-level sequence.

Phase55 recomputed this test preserving full page-side identifiers (`f1r`, `f1v`, etc.). The qualitative transient survives, but the corrected headline gap is smaller and the effect is not uniform across manuscript sections. The corrected values below supersede the original Phase54 headline for interpretation.

## Corrected shifted-boundary test

Mean within-minus-boundary gap across 206 eligible page-sides:

- shift -1: **-0.0035**
- **true boundary 0: +0.0899**
- shift +1: +0.0377
- shift +2: -0.0505

At the true boundary, 161/206 eligible page-sides have a positive gap.

The original leaf-collapsed values (`+0.1153`, 88/99 leaves) are retained only as historical audit evidence and should not be used as the current headline.

## Corrected recovery after paragraph start

Mean adjacent-line near-family continuity by current line's distance from paragraph start:

- first paragraph line (0): **0.1348**
- line 1: 0.2184
- line 2: 0.2818
- line 3: 0.2905
- line 4: 0.3012
- line 5: 0.2845
- line 6: 0.2670

The rapid recovery over roughly two lines therefore survives the page-side audit.

## Section dependence discovered in Phase 55

Corrected mean true-boundary gaps:

- Herbal: +0.0859 (128 sides)
- Biological: +0.1272 (19)
- Pharmaceutical: +0.1217 (16)
- starred/text section: +0.1371 (25)
- text-only miscellaneous: +0.1099 (6)
- Astronomical: -0.0502 (5; small n)
- Cosmological: -0.0968 (7; small/heterogeneous n)

Therefore the paragraph-entry effect is strong in major prose-heavy sections but must **not** be described as manuscript-universal.

## Interpretation

The surviving target is:

> in several major prose-heavy Voynich sections, paragraph entry is associated with a boundary-specific reconfiguration followed by rapid recovery toward the ordinary within-paragraph regime.

This remains different from a simple stationary paragraph-local topic model. It is compatible with discourse/entry morphology, cipher/key/state initialization, a formal entry-state mechanism, or mixed mechanisms.

Because the target was discovered and audited on the same corpus, it is a development target, not prospective validation.
