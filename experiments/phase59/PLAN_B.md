# Phase 59B plan — medieval Latin medical/recipe entry-state comparison

Status: pre-execution plan. Frozen before running the medical controls.

## Question

Is the Voynich paragraph-entry -> recovery trajectory unusual even relative to medieval Latin medical, diagnostic, and recipe-style texts with heavy scribal abbreviation and practical item structure?

## Primary corpora

Use CREMMA-Medieval-LAT graphematic transcriptions where available, prioritizing:

- H318 (medical miscellany; includes De urinis, recipes, Liber de coitu, Practica and related material)
- CLM13027 (medical)
- Latin16195 (medical)
- Egerton821 (medical)

Dante remains the continuous-prose baseline from Phase59A.

## Representation

Prefer source-native graphematic transcription rather than normalized/expanded Latin. Preserve abbreviation/special grapheme tokens when the corpus representation permits. Record any normalization required by the generic feature extractor.

## Structural boundary classes

Do not label every break a paragraph. Analyze separately where the source supports it:

1. ordinary prose/medical-discussion paragraph or section entry;
2. diagnostic/classificatory item entry (e.g. urine/prognostic category);
3. recipe/remedy/prescription item entry;
4. page/region boundary only, as a nuisance control.

If the source files do not encode a reliable semantic item boundary, do not infer one from the Latin wording after looking at the Voynich result. Such material may still be used for line/page controls but not for the item-entry test.

## Frozen statistic

Use the same generic 11-dimensional feature family used in Phase59A:

- type-token ratio
- mean token/unit length
- token/unit length SD
- unit inventory size
- unit entropy
- first-unit entropy
- last-unit entropy
- edit-distance-1 type-family coverage
- local previous-10 near-family continuity
- k/t-mass analogue only where representation has literal k/t; otherwise retain as zero/non-comparable and report this limitation
- within-k/t balance analogue only where defined

Primary entry statistic: standardized multivariate line0 -> line2 transition norm, with paired sign-flip null within source entries. Report the full mean transition vector, not only the norm.

## Matching / sensitivity

- Use source-native manuscript lines when available.
- Also run Voynich-line-length synthetic wrapping as a sensitivity analysis where source lines are unsuitable or absent.
- Require >=3 lines and >=5 usable tokens in entry line and line2 for the primary trajectory statistic.
- Bootstrap/permutation units are source entries or manuscript pages, never individual tokens.

## Frozen hypotheses

### H59B-1 — practical-medical entry explanation
Medieval Latin medical/recipe item entries reproduce a Voynich-like sharp multivariate entry -> line2 trajectory.

Support requires a significant entry transition with magnitude/direction materially closer to Voynich than Dante, not merely any line-position difference.

### H59B-2 — Voynich remains unusual within medical controls
Medical/recipe controls behave closer to ordinary Latin prose than to Voynich, or their transitions point in substantially different feature-space directions.

### H59B-3 — mixed result
Some practical medical genres reproduce part of the trajectory but not its full magnitude/direction. In that case, the Voynich effect should be reframed as an amplification/specialization of a practical-document entry grammar rather than manuscript-unique structure.

## Promotion rule

This phase can only discriminate mechanism/document-genre explanations. It cannot establish language identity, content identity, cipher, or decipherment.
