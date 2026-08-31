# Phase 66A-Color B — background-normalized, data-driven color measurement

Status: **FROZEN BEFORE COLOR-B MEASUREMENT**

This supersedes `COLOR_PLAN_A.md` for scientific use but does not delete or overwrite the initial preflight. The A run is retained as a diagnostic showing that fixed HSV bins confounded parchment/scan color with plant coloration.

## Goal

Measure chromatic structure in the 24 frozen Phase65 crops after deterministic parchment normalization, without pre-naming the colors and without using any Voynich text, morphology association, or object-level outcome.

## Input

Exactly the 24 frozen Phase65 crop PNGs. Their SHA256 values must match the Phase65 crop manifest before measurement.

No crop boundary may change.

## 1. Background reference extraction

For each crop independently:

1. Convert sRGB pixels to CIE Lab using OpenCV.
2. Define the border band as the outer 12% of image width/height.
3. From border-band pixels, retain candidate parchment pixels satisfying OpenCV-Lab `L >= 155` and chroma radius `sqrt((a-128)^2 + (b-128)^2) <= 35`.
4. If fewer than 500 candidate pixels exist, use all border pixels with `L >= 145`; if still fewer than 500, the crop is `BACKGROUND_FAIL` and Color B stops before any text-side analysis.
5. The crop background reference is the componentwise median Lab value of those candidates.

This is a deterministic imaging correction, not a semantic annotation.

## 2. White-balance / parchment neutralization

For each pixel in OpenCV Lab coordinates:

- keep L unchanged except for a global shift that maps the background median L to 230;
- shift a so the background median a maps to 128;
- shift b so the background median b maps to 128;
- clip each channel to 0..255.

No per-channel gain is fitted beyond these fixed additive shifts. This removes scan/parchment cast while preserving relative local chromatic deviations.

## 3. Ink and colored-pixel mask

On normalized Lab pixels define:

- `chroma = sqrt((a-128)^2 + (b-128)^2)`;
- `delta_bg = sqrt((L-230)^2 + (a-128)^2 + (b-128)^2)`.

A pixel enters the color-clustering pool iff:

- normalized `L >= 45` (exclude very dark ink),
- `chroma >= 12`, and
- `delta_bg >= 18`.

Connected components smaller than both 20 pixels and 0.08% of crop area are removed before pooling.

## 4. Data-driven color clusters

No red/green/blue/brown labels are used in the scientific measurement.

Pool all retained colored pixels from all 24 crops. Fit KMeans in the two-dimensional normalized `(a-128, b-128)` plane.

Candidate cluster counts: `k = 2,3,4,5,6`.

For computational stability, model selection uses a deterministic sample of at most 20,000 pooled pixels selected by fixed RNG seed `6602`.

For each k:

- KMeans `random_state=6602`, `n_init=20`;
- compute silhouette score on the same deterministic sample.

Choose the smallest k whose silhouette score is within 0.01 of the maximum candidate silhouette. This rule is frozen before measurement.

Refit that k to the full pooled color-pixel set with the same KMeans settings.

Cluster IDs are assigned deterministically after fitting by sorting cluster centers lexicographically by `(a_center, b_center)` and renumbering `C1..Ck`.

Human-readable color names may be added only as descriptive metadata after all scientific measurements are sealed. Primary statistics use only `C1..Ck`.

## 5. Per-object measurements

For each crop and each frozen cluster record:

- retained pixel count;
- fraction of total crop area;
- fraction of that crop's total colored pixels;
- present boolean;
- normalized x centroid;
- normalized y centroid;
- fractions of cluster pixels in top/middle/bottom thirds.

`present=true` requires both:

- at least 25 retained pixels;
- at least 0.20% of crop area.

Also record:

- total colored-pixel fraction;
- background Lab reference;
- applied Lab shift.

## 6. Eligibility before text reveal

A binary cluster-presence feature may enter the prospective Phase66 association family only if:

1. present in >=4/24 objects;
2. absent in >=4/24 objects;
3. both f102v2 and f100v have >=1 present object;
4. no single physical row contains >80% of present objects.

A cluster area-fraction feature may enter only if:

1. >=8 objects have nonzero retained area;
2. both pages contain nonzero observations;
3. 90th percentile area fraction exceeds median by >=0.002.

Spatial features remain secondary unless separately preregistered before any image-text association.

## 7. Diagnostics permitted before text reveal

Allowed:

- inspect normalized images and cluster-mask contact sheets for obvious background leakage;
- inspect per-cluster prevalence and cluster centers;
- declare Color B invalid if the algorithm demonstrably segments parchment/ink rather than coloration.

Not allowed:

- alter thresholds because a cluster does or does not look promising for text association;
- inspect Voynich label features while tuning Color B;
- select only visually attractive objects;
- alter k manually.

If a material defect is found, archive this run and create `COLOR_PLAN_C.md` before any rerun.

## 8. Interpretation boundary

Color B measures normalized chromatic classes in the scan. It does not by itself identify historical pigments, botanical organs, species, semantics, or glyph values.
