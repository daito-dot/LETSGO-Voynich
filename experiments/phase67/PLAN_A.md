# Phase 67A — pharmaceutical image morphology -> body-paragraph structure

Status: **FROZEN BEFORE IMAGE-BLOCK ANNOTATION AND MORPHOLOGY↔TEXT ASSOCIATION**

Date: 2026-08-31

## Pre-annotation population correction

The first freeze draft counted a fourth f99v block. Before any Phase67 image annotation or morphology↔text association was inspected, the ZL3b sequence was re-audited and showed that `f99v.36` (`@Lc`) is followed by the body paragraph `f99v.37-43`, while the only associated `@Lf` locus `f99v.44` occurs **after** that paragraph. This breaks the prospective rule that a visual label/fragment group must objectively precede its paired paragraph. The ambiguous tail is therefore excluded now, before science.

The corrected population below is final: **14 blocks**, with an exact within-folio permutation space of **2,304** assignments.

## Question

Phase 66B found no detectable relation between the frozen visual plant attributes and the short attached `Lf` label strings. That result does not test whether the longer running text associated with the same pharmaceutical illustration block carries morphology-related information.

Phase 67A asks a narrower new question:

> Within pharmaceutical folios, do illustration blocks with different frozen leaf-morphology state distributions have systematically different following body-paragraph text structure?

This is not a translation test. A positive result would show a reproducible image↔body association after folio state is held fixed. A null result would reject this particular surface/structural body-text detector, not all possible semantic encodings.

## Independence from earlier label tests

The predictor is image morphology only. `Lf`/`Lc` label strings are used only to delimit visual/text blocks where ZL3b and the page layout provide an objective boundary. Label spelling is not a predictor or response.

Phase 41's earlier `Lf label -> correct body row` test is therefore not reused as evidence for or against this test; it tested label-form relations and was null.

## Frozen population

Use exactly the 14 blocks in `BLOCK_MANIFEST_A.json` from Quire 19:

- f99r: 4 blocks
- f99v: 3 blocks
- f100r: 2 blocks
- f100v: 1 block
- f102v2: 2 blocks
- f102v1: 2 blocks

These pages were selected because the page layout and ZL3b sequence define the visual block and its body paragraph without choosing among nearby paragraphs after inspecting morphology↔text results.

Excluded prospectively:

- f99v tail (`f99v.36`, paragraph `37-43`, `Lf` at `44`): the plant-fragment label occurs after the paragraph, so the visual-block boundary is not objective under the frozen rule;
- f101r: no labels and multiple paragraphs occupy the same inter-row zone;
- f101v: multiple paragraphs are at the bottom of a foldout and the row↔paragraph mapping is not unique;
- f102r1: multiple paragraphs lie between illustration groups;
- f102r2: lower labels/containers and two paragraphs do not yield a unique row↔paragraph mapping.

No block may be added or removed after the image annotation or primary statistic is opened.

## Image-side authority

Use manuscript pixels only. The visual state vocabulary is exactly the already frozen Phase 66A `ANNOTATION_SCHEMA_A.json`:

### `leaf_composition`

- `simple`
- `compound_pinnate`
- `compound_palmate`
- `deeply_divided_uncertain_leaflet_status`
- `U`

### `leaf_arrangement`

- `alternate`
- `opposite`
- `whorled_3plus`
- `basal_or_rosette`
- `single_or_insufficient_nodes`
- `U`

### `leaf_margin`

- `entire_or_nearly_entire`
- `serrate_or_dentate`
- `crenate_or_rounded_teeth`
- `lobed_or_incised`
- `spiny_or_aculeate_margin`
- `mixed`
- `U`

Rules:

- code each fixed plant fragment independently;
- use `U` when the relevant leaf geometry is not actually visible;
- do not infer from a proposed species identity, historical analogue, nearby label, or body text;
- do not change a state after the morphology↔text statistic is opened.

## Block-level visual vector

For each morphology character separately, convert the fragment states in a block to a distribution over the non-`U` states of that character.

- `U` is excluded from the state distribution;
- the distribution is conditional on observed states only;
- apply the Hellinger transform (`sqrt(proportion)`) to the state vector;
- a block with zero non-`U` observations for that character is not usable for that character.

No ordinal score is assigned to the categories.

## Text-side authority

Use ZL3b, version 3b dated 2025-05-13, and exactly the P0 locus ranges in `BLOCK_MANIFEST_A.json`.

Text cleaning is frozen as follows:

1. treat `.`, `,`, whitespace, and `<->` as separators;
2. remove paragraph/line markers such as `<%>` and `<$>`;
3. retain only complete lowercase alphabetic tokens matching `^[a-z]+$`;
4. discard any token containing transcription/editorial uncertainty markup (`?`, `[`, `]`, `{`, `}`, `@`, `:`, `<`, `>`) rather than resolving the uncertainty;
5. do not use `Lf` or `Lc` tokens in the text vector.

For each body paragraph, count within-token character n-grams for n=1, 2, and 3.

For each n independently:

- vocabulary = grams occurring in at least 2 of the 14 frozen body paragraphs;
- convert counts to relative frequencies within that n;
- apply the Hellinger transform;
- concatenate the n=1,2,3 vectors, scaling each n-order block by `1/sqrt(3)`.

The vocabulary rule uses no image information.

## Folio-state control

The primary analysis removes folio-level state before testing association.

For each morphology character:

- retain only blocks with at least one non-`U` image observation for that character;
- within each folio represented by at least two retained blocks, subtract the folio mean from both the visual vectors and the text vectors;
- folios with fewer than two retained blocks contribute no centered information for that character.

This directly addresses the strong same-folio state already established in earlier phases.

## Primary statistic

For each morphology character `c`, compute the normalized RV coefficient between the within-folio-centered visual matrix `X_c` and text matrix `Y_c`:

`RV_c = ||X_c^T Y_c||_F^2 / sqrt(||X_c^T X_c||_F^2 * ||Y_c^T Y_c||_F^2)`.

The global statistic is:

`T = max(RV_leaf_composition, RV_leaf_arrangement, RV_leaf_margin)`.

This max statistic is frozen before image annotation so the three morphology characters are corrected as one family.

## Exact null

Hold all image annotations and paragraph texts fixed. Permute complete text paragraphs among the frozen blocks **within each folio only**.

The full assignment space is exactly:

`4! * 3! * 2! * 1! * 2! * 2! = 2,304`.

Enumerate all 2,304 assignments; do not Monte Carlo sample them. Recompute the full three-character max statistic for every assignment.

Exact one-sided p-value:

`p = count(T_perm >= T_obs) / 2304`.

The identity assignment is part of the exhaustive null.

## Operational gates

A morphology↔body result is called detected only if both are true:

1. global exact maxT `p <= 0.05`;
2. the winning morphology character has at least 8 usable blocks spanning at least 3 folios, with at least 2 usable blocks in each contributing folio.

If the p-value passes but the coverage gate fails, classify the result as `UNDERPOWERED / COVERAGE-LIMITED`, not positive.

## Missingness control

For each character, separately compute a block-level coverage scalar: fraction of fixed fragments in the block that are non-`U` for that character.

Run the same within-folio exact-permutation association against the text vector using coverage alone. This is a nuisance/control analysis. If the primary morphology test is positive but the corresponding coverage-only test is also positive at `p <= 0.05`, downgrade interpretation to `MORPHOLOGY / OBSERVABILITY CONFOUNDED` unless the morphology statistic remains significant after residualizing the visual state proportions on coverage within folio.

## Secondary sensitivity

Repeat the primary workflow using only text n=1,2 grams. This is secondary and cannot rescue a failed primary n=1,2,3 result.

## Falsification rule

The hypothesis is not supported if the frozen primary maxT test has `p > 0.05`, or if the operational coverage gate fails.

Do not change block boundaries, image states, text cleaning, n-gram order, or permutation strata after the primary result is opened.