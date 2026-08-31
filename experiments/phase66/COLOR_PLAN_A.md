# Phase 66A-Color — deterministic color preregistration

Status: **FROZEN BEFORE COLOR MEASUREMENT**

This lane is independent of the Phase66 morphology annotation and independent of all Voynich label features.

## Question

Measure whether the frozen Phase65 plant crops contain reproducible chromatic signals and where those signals occur spatially, without human color naming, organ identification, taxon identification, or pairwise visual judgment.

## Input firewall

Inputs are exactly the 24 frozen Phase65 crop PNGs whose SHA256 values were already verified against the Phase65 crop manifest.

No crop may be expanded, shifted, recolored, white-balanced per object, or selected based on label content.

The color executable receives pixels and object ID only. It does not receive transcription, morphology states, Phase65B statistics, or any text-side feature.

## Pixel representation

Decode PNG as sRGB and convert every pixel to OpenCV HSV (`H` 0..179, `S` 0..255, `V` 0..255).

A pixel is chromatic only if:

- `S >= 50`, and
- `V >= 35`.

This rejects most parchment background, near-gray ink, and very dark scan noise without using object-specific thresholds.

## Frozen color classes

Classes are mutually exclusive and evaluated in this order:

1. `brown`: `H in [5,25]`, `S >= 50`, `V <= 180`
2. `red`: (`H in [0,10]` or `H in [170,179]`), `S >= 65`, `V > 80`
3. `yellow_ochre`: `H in [11,34]` and not already brown
4. `green`: `H in [35,95]`
5. `blue`: `H in [96,135]`
6. `other_chromatic`: every remaining chromatic pixel

The class names are operational pixel bins, not pigment identifications.

## Noise rule

For each class, connected components are computed with 8-connectivity. Components smaller than both 25 pixels and 0.10% of crop area are discarded.

A class is `present=true` only if the retained class area is at least both:

- 25 pixels, and
- 0.20% of total crop area.

Presence is therefore deterministic and identical across objects.

## Frozen measurements per color class

For every crop and every class record:

- retained pixel count;
- fraction of total crop area;
- `present` boolean;
- normalized x centroid in `[0,1]` if present;
- normalized y centroid in `[0,1]` if present;
- fraction of retained class pixels in top, middle, and bottom thirds of the crop.

No anatomical label such as leaf/root/flower is assigned from color in this lane.

## Parchment / unpainted proxy

Record `low_chroma_bright_fraction` as the fraction of all pixels satisfying:

- `S < 50`, and
- `V >= 160`.

This is a crop-level imaging proxy only. It is not interpreted as literal unpainted plant area because parchment background is included.

## Pre-text eligibility firewall

Before any text association is computed, publish color prevalence and spatial coverage.

A binary color-presence feature may enter a Phase66 primary association family only if:

1. present in at least 4 of 24 objects;
2. absent in at least 4 of 24 objects;
3. both f102v2 and f100v contain at least one present observation;
4. no single physical row contains more than 80% of all present observations.

A continuous area-fraction feature may enter only if:

1. at least 8 objects have nonzero retained area;
2. both pages contain nonzero observations;
3. the 90th percentile is greater than the median by at least 0.002 of crop area, preventing numerically trivial variation from owning a claim.

Spatial centroid/third-distribution features are secondary unless a separate prospective statistic is frozen before association.

## Interpretation boundary

A later association would show only that deterministic color-bin measurements covary with predeclared label structure. It would not identify pigments, botanical taxa, semantic meanings, or writing-system values.

## Failure rule

If the script, thresholds, or class definitions are materially changed after measurement begins, the current color run is archived as invalid and a newly versioned preregistration is required. Thresholds may not be tuned after inspecting object-level color outputs.
