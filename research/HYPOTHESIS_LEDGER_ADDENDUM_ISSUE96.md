# Hypothesis Ledger Addendum — Issue #96 / Issue #88 Phase 2B

Date: 2026-09-06
Authority: `experiments/predictive-information/phase2b/REPORT.md`

## P96-1 — the dominant nonlocal predictive effect is approximately uniform in token distance across a physical leaf

**State before Phase 2B:** LIVE / unresolved.

**Result:** **REJECTED as the main description under the tested boundary controls.**

After LOCAL40, same-line bag adds `0`, current-paragraph bag adds only `+0.000708 bit/token`, while allowing previous-paragraph inventory adds `+0.043598 bit/token` beyond the current-paragraph model, positive 5/5 folds.

A single distance-only horizon therefore conflates strongly different observable document regimes.

## P96-2 — additional current-paragraph inventory is a material source beyond LOCAL40

**State:** **FORMALLY SUPPORTED BUT EFFECT-SMALL.**

`+0.000708 bit/token`, positive 4/5 folds; one fold reverses and nested mixture weight is only `.01-.02`.

This satisfies the preregistered stability rule but should not be treated as a major explanatory component.

## P96-3 — previous-paragraph token-family inventory is a major predictive source

**State:** **SUPPORTED STRONGLY.**

Cross-paragraph inventory contrast:

- mean `+0.043598 bit/token`;
- positive 5/5 folds.

Previous-paragraph-only bag reaches `9.543951 bits/token`, better under this conditional model than the full leaf-prefix bag (`9.551875`) and the Phase-1 standalone ORDERED128 reference (`9.549254`).

This establishes predictive relevance of the earlier-paragraph inventory, not its semantic or historical identity.

## P96-4 — precise current-paragraph lag/order carries residual information beyond the local model

**State:** **REJECTED under the tested matched control.**

Actual current-paragraph lag assignment loses slightly to matched random lag in all five folds (`-0.0000877 bit/token` mean).

## P96-5 — precise previous-paragraph lag/order carries some residual information

**State:** **SUPPORTED WEAKLY.**

Actual lag/source association beats matched random lag by `+0.000607 bit/token`, positive 4/5 folds. One fold reverses and the effect is tiny relative to the inventory effect.

The main previous-paragraph source is therefore inventory-like, with only a small surviving order-sensitive residual.

## P96-6 — rich latent-state fitting is now licensed

**State:** **REJECTED / still blocked.**

The dominant previous-paragraph signal has not yet been localized into:

- immediately previous versus older paragraphs;
- same page-side versus recto/verso carryover within the numeric physical leaf;
- paragraph index / observable transition effects;
- Currier/section/scribe strata and transport.

These observable source-attribution tests precede latent-state modeling.

## Program consequence

The predictive hierarchy is now better described as:

1. compact token-internal V2 construction;
2. short local edit-1 recency;
3. a dominant slower inventory associated with earlier paragraphs on the same physical leaf;
4. a tiny cross-paragraph order/lag residual;
5. separately established line/paragraph position information.

The next experiment should decompose item 3 structurally before introducing external manuscript metadata.