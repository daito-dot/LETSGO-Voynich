# Phase 55 — Voynich internal structure map

Status: exploratory/internal-structure phase. Generator development is intentionally paused while the manuscript's own hierarchy is mapped.

## Scope

ZL3b P-coded prose was summarized at page-side/folio scale using token length/TTR, edit-1 family density, local near-family rate, paragraph-boundary gap, line-position MI, token-edge entropy and collapsed-unit frequencies. Both linear and nonlinear models were evaluated with grouped cross-validation.

## Metadata confounding

The metadata are strongly non-orthogonal. Normalized mutual information (normalized by the smaller label entropy):

- section × Currier: ~0.269
- section × hand: ~0.350
- Currier × hand: **~0.655**

Global Currier separability therefore cannot be interpreted as an isolated Currier mechanism.

## Linear vs nonlinear structure

Balanced accuracy on the common folio fingerprint:

| target | linear logistic | nonlinear ExtraTrees |
|---|---:|---:|
| section (classes n>=8) | 0.890 | 0.846 |
| Currier A/B | 0.974 | 0.973 |
| hand (classes n>=8) | 0.819 | 0.832 |

There is no large nonlinear advantage at this scale. Much of the large-scale separation is already visible in low-order combinations of the measured features.

## Conditional section contrasts

Holding major metadata fixed still leaves strong section structure:

- hand 1 / Currier A, Herbal vs Pharmaceutical: linear 0.874; nonlinear 0.895
- hand 2 / Currier B, Herbal vs Biological: **1.000 / 1.000**

By contrast, hand 2/3/5 prediction within Herbal B is much weaker (~0.625 linear; ~0.562 nonlinear).

## Strong local physical drift

Standardized fingerprint mean distance:

- same physical leaf, recto vs verso: **5.03**
- same section + same hand, different leaf: 6.81
- broadly unrelated: 7.44

Within the same section+hand, distance increases with leaf separation:

| leaf gap | mean distance |
|---|---:|
| same leaf | 5.02 |
| 1 | 5.72 |
| 2 | 6.12 |
| 3–5 | 6.17 |
| 6–10 | 6.31 |
| 11+ | 7.14 |

This supports a locally drifting physical/document state below broad section/hand labels.

## Linear unique-variance diagnostic

With section, Currier and hand entered jointly, unique section ΔR² is substantial for edit-1 density (~0.157), line-position MI (~0.262) and TTR (~0.310). Unique Currier ΔR² is near zero for these summaries after the shared section/hand variance is absorbed. This does **not** prove Currier has no effect; the crossed design is too confounded for that conclusion.

## Phase 53/54 audit correction

Phase53/54 accidentally collapsed recto and verso (`f1r`, `f1v`) to a common `f1` leaf identifier. The paragraph-boundary analysis was recomputed with full page-side IDs.

Corrected shifted-boundary gap across 206 eligible page-sides:

- shift -1: -0.0035
- **true boundary: +0.0899**
- shift +1: +0.0377
- shift +2: -0.0505

The recovery trajectory survives: continuity is 0.1348 at paragraph entry, 0.2184 one line later, 0.2818 two lines later, then ~0.29–0.30.

The earlier ~+0.115 leaf-collapsed headline is superseded.

## Paragraph entry is section-dependent

Corrected mean true-boundary gaps:

- Herbal: +0.0859 (128 sides)
- Biological: +0.1272 (19)
- Pharmaceutical: +0.1217 (16)
- starred/text section: +0.1371 (25)
- text-only miscellaneous: +0.1099 (6)
- Astronomical: -0.0502 (5; small n)
- Cosmological: -0.0968 (7; small/heterogeneous n)

The paragraph-entry effect is strong in several major prose-heavy sections but is **not manuscript-universal**.

## Current internal hierarchy

A better working description is:

`manuscript -> broad section/document role -> locally drifting leaf/page state -> paragraph-entry dynamics -> line-position grammar -> token morphology`

Hand and Currier labels cut across this hierarchy but are strongly confounded with section and each other.

## Decision

Do not resume generator tuning yet. Phase 56 should map paragraph- and line-level state geometry, physical-order drift/changepoints, recurring transformation directions across sections, and transition scales. Use both linear transition models and nonlinear/state-space/changepoint methods.
