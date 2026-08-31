# Phase 66A-Color B result

Status: **SEALED BEFORE ANY PHASE66 IMAGE↔TEXT ASSOCIATION**

## Why B exists

Color A was a useful preflight failure: fixed HSV bins classified brown/yellow-ochre in all 24 crops, indicating substantial parchment/scan-color leakage. This was diagnosed before any text-side association. Color A remains archived; Color B is the scientific color measurement.

## Frozen correction

Color B estimates parchment from each crop's outer 12% border under fixed brightness/chroma criteria, maps that median Lab background to neutral bright Lab `(230,128,128)`, removes very dark ink and near-background pixels, and clusters the remaining chromatic pixels without pre-naming colors.

No Voynich text feature or image↔text result was used.

## Data-driven cluster count

Pooled retained chromatic pixels: **823,956**.

Silhouette scores: k=2 0.608025; k=3 0.644603; k=4 0.412643; k=5 0.422851; k=6 0.390209. The frozen smallest-within-0.01-of-best rule selected **k=3**.

Normalized Lab `(a-128,b-128)` centers:

- C1 = (-19.181, -0.540)
- C2 = (-7.001, +9.870)
- C3 = (-6.892, -17.502)

These remain operational cluster IDs rather than pigment names.

## Frozen eligibility outcome

Binary presence under the sealed result summary:

- C1: **16/24 — eligible**
- C2: **11/24 — eligible**
- C3: **3/24 — not eligible**

Present-row counts are C1: B=4, M=3, T=3, L2=4, L3=2; C2: B=1, M=3, T=1, L2=2, L3=4; C3: T=1, L2=1, L3=1.

Continuous area fractions satisfy the already frozen Color-B continuous eligibility rule for C1, C2, and C3. C3 is sparse: its binary feature fails prevalence. That fact is retained explicitly and cannot be repaired by changing the threshold after text association.

## Diagnostic inspection

A parchment-neutralized image sheet was inspected before any text-side association. The gross all-object brown/yellow contamination observed in Color A is no longer present. The normalized crops retain visibly localized chromatic plant regions rather than turning the entire parchment field into a single named-color signal.

This diagnostic inspection was permitted by `COLOR_PLAN_B.md`; no thresholds or k were manually changed from association behavior.

## Image-side Phase66 state

The image side is now sealed with two independent measurement families:

1. externally grounded botanical morphology characters that passed the morphology eligibility firewall;
2. deterministic background-normalized chromatic clusters that passed the Color-B firewall.

Color does not repair morphology, and morphology does not define the color clusters.

## Claim boundary

This is scan-level colorimetry, not pigment chemistry. It does not establish original pigment identity, botanical organ color, taxon identity, semantics, or glyph values.

The next step is to freeze the text-side feature family and Phase66B statistical design before the first image↔text association is computed.
