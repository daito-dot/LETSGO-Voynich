# Phase 66A-Color B result

Status: **SEALED BEFORE ANY PHASE66 IMAGE↔TEXT ASSOCIATION**

## Why B exists

Color A was a useful preflight failure: fixed HSV bins classified brown/yellow-ochre in all 24 crops, indicating substantial parchment/scan-color leakage. This was diagnosed before any text-side association. Per the research decision, ordinary imaging noise is therefore removed rather than preserved as if it were plant signal.

Color A is retained unchanged for audit. Color B is the scientific color measurement.

## Frozen correction

Color B estimates parchment from each crop's outer 12% border under fixed brightness/chroma criteria, maps that median Lab background to neutral bright Lab `(230,128,128)`, removes very dark ink and near-background pixels, and clusters the remaining chromatic pixels without pre-naming colors.

No Voynich text feature or morphology↔text result was available to this procedure.

## Data-driven cluster count

Pooled retained chromatic pixels: **823,956**.

Silhouette scores:

- k=2: 0.6080
- k=3: **0.6446**
- k=4: 0.4126
- k=5: 0.4229
- k=6: 0.3902

The frozen smallest-within-0.01-of-best rule therefore selected **k=3**.

Normalized Lab a/b centers, deterministically ordered:

- C1 = (-19.181, -0.540)
- C2 = (-7.001, +9.870)
- C3 = (-6.892, -17.502)

These are deliberately not assigned pigment names for scientific use.

## Binary presence

Using the frozen >=25 pixels and >=0.20% crop-area presence rule:

- C1: 17/24 present — **eligible**
- C2: 10/24 present — **eligible**
- C3: 3/24 present — **not eligible as binary primary feature**

C1 and C2 satisfy the predeclared page/row distribution firewall. C3 fails the minimum prevalence rule and remains descriptive only in binary form.

## Continuous area fraction

- C1: 20 nonzero objects; median 0.23668; p90 0.54296 — **eligible**
- C2: 23 nonzero objects; median 0.00159; p90 0.06085 — **eligible**
- C3: 8 nonzero objects; median 0; p90 0.00292 — **eligible under the frozen continuous rule**

The C3 continuous result is retained because the rule was frozen before measurement. Its sparsity must be considered when the statistical plan is frozen; it cannot be promoted simply because it later associates with text.

## Interpretation

The main improvement over Color A is conceptual: the analysis no longer asks whether hand-picked named colors are present. It measures deviations from each crop's estimated parchment baseline and lets the image population define the chromatic classes.

This is still scan-level colorimetry, not pigment chemistry. It cannot establish original pigment identity or botanical meaning.

## Next firewall

Image-side scientific candidates are now frozen before text association:

- morphology: the Phase66A characters that passed `ELIGIBILITY_REPORT_A.md`;
- color binary: C1, C2;
- color continuous area: C1, C2, C3.

No image↔text association has been computed at this point. The next step is to freeze the text feature family and `PLAN_B.md` statistical design before revealing any cross-modal result.
