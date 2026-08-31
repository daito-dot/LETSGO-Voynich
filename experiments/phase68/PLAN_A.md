# Phase 68A — image morphology -> formal-residual lexical/family selection

Status: **FROZEN BEFORE FIRST PHASE68 IMAGE↔LEXICAL ASSOCIATION**

Date: 2026-08-31

## 1. Why this changes representational level

Phase66B and Phase67A–C all tested relatively direct image-morphology ↔ text-surface relations and were null:

- short attached-label structure;
- raw following-paragraph character n-grams;
- following-paragraph character n-grams after masking tokens compatible with the established paragraph-entry / short-range edit1 formal channels.

Those negatives do not imply that nearby text lacks content. A text can discuss different objects by selecting different lexical items while preserving very similar character-level statistics. This matters especially in Voynichese because Phase61–64 independently established a strong formal layer that can shape token realization and local recurrence.

Phase68A therefore moves one level upward:

> After the same A1-compatible formal mask, does sealed image morphology predict **which retained token identities or edit1-neighborhood lexical families are selected** in the paired body paragraph?

This is not a retry with a new leaf trait or a new character n-gram. It tests lexical selection rather than surface composition.

Because the hypothesis is chosen after the Phase67 nulls, any positive result is **candidate evidence only** until independently replicated on a separately frozen pharmaceutical population.

## 2. Frozen population and inputs

Reuse without modification from Phase67:

- `experiments/phase67/BLOCK_MANIFEST_A.json` — 14 Quire 19 illustration→paragraph blocks;
- `experiments/phase67/TEXT_TABLE_A.json` — sealed ZL3b body paragraphs;
- `experiments/phase67/IMAGE_ANNOTATION_A.json` — sealed leaf states;
- `experiments/phase67/ROOT_ANNOTATION_B.json` — sealed root architecture states.

No image annotation, block boundary, paragraph boundary, or transcription choice may change in Phase68A.

## 3. Formal mask

Reuse the Phase67C mask exactly.

Process paragraphs in manuscript order within folio, with a FIFO history of the previous ten conservatively cleaned tokens.

For each token:

1. any token on paragraph line 0 -> `ENTRY_MASKED`;
2. otherwise, if Levenshtein distance exactly 1 from any previous-ten token -> `LOCAL_EDIT1_MASKED`;
3. otherwise -> `INNOVATION_RETAINED`;
4. every cleaned token is appended to history, masked or retained.

The `lev1` relation is exactly the Phase61C implementation:

- equality is not edit1;
- one insertion, deletion, or substitution is edit1;
- length difference >1 is not edit1.

The mask is a compatibility filter, not a claim that A1 historically generated each masked token.

## 4. Conservative text cleaning

Reuse Phase67C exactly:

- `.`, `,`, whitespace, and `<->` are separators;
- paragraph markers are removed;
- only complete lowercase alphabetic tokens matching `^[a-z]+$` are retained;
- tokens containing uncertainty/editorial markup are discarded rather than resolved.

## 5. Two morphology-blind lexical lanes

Both lexical feature spaces are built from `INNOVATION_RETAINED` tokens only. No image state is consulted when defining either vocabulary.

### L1 — exact retained-token identity

Define document frequency for each retained token type as the number of the 14 frozen paragraphs containing that exact type.

Vocabulary:

`V = all retained token types with paragraph document frequency >= 2`.

For each paragraph:

- count occurrences of each token in V;
- normalize counts to relative frequency over V-counted occurrences;
- apply Hellinger transform `sqrt(p)`.

A paragraph with no V-counted token receives the zero vector; it is not silently removed.

### L2 — edit1-anchor lexical-family neighborhood

Use the same V as a fixed anchor vocabulary.

For every retained token `t` and every anchor `v in V`, count one hit for anchor v if:

`t == v OR lev1(t, v)`.

Thus each anchor defines a deterministic exact-or-one-edit neighborhood. A token may contribute to more than one anchor; this is intentional and no graph clustering/community algorithm is introduced.

For each paragraph:

- sum anchor hits;
- normalize the anchor-hit vector to relative frequency when its sum is nonzero;
- apply Hellinger transform.

This lane asks whether morphology predicts selection of recurrent lexical neighborhoods even when their surface realization differs by one edit, using the same edit relation already established before Phase68.

## 6. Text-only feasibility firewall

Before any image↔lexical statistic is interpreted, both lanes must satisfy all of:

1. `|V| >= 5`;
2. at least 10/14 paragraphs have a nonzero L1 vector;
3. at least 10/14 paragraphs have a nonzero L2 vector.

These checks use text only. If any fails, Phase68A is `BLOCKED / LEXICAL REPRESENTATION TOO SPARSE`; do not alter the DF threshold after seeing image association.

Report:

- retained token total;
- retained distinct types;
- `|V|`;
- L1/L2 nonzero paragraph counts;
- per-block retained token count and vocabulary-hit coverage.

## 7. Frozen image predictor family

Use exactly the four already sealed characters:

1. `leaf_composition`
2. `leaf_arrangement`
3. `leaf_margin`
4. `root_subterranean_architecture`

For each character separately:

- exclude object-level `U`;
- compute block proportions over the character's non-U states;
- Hellinger-transform those proportions;
- a block with no observed state for that character is unusable for that character.

No new visual trait is allowed in Phase68A.

## 8. Folio-state control

For each image character and lexical lane:

- retain blocks usable for that image character;
- only folios with at least two usable blocks contribute;
- subtract the within-folio mean from image and lexical vectors separately.

This keeps the previously established folio-local state from creating a false content relation.

## 9. Primary statistic and multiplicity

For each of 4 image characters × 2 lexical lanes, compute normalized RV:

`RV = ||X^T Y||_F^2 / sqrt(||X^T X||_F^2 * ||Y^T Y||_F^2)`.

There are exactly eight preregistered cells.

Primary statistic:

`T = max(all 8 RV values)`.

The eight-way maximum is frozen before first association and provides family-wise correction under the exact permutation null.

## 10. Exact null

Hold image annotations and lexical paragraph representations fixed. Permute complete paragraph representations **within folio only**.

Exact space:

`4! * 3! * 2! * 1! * 2! * 2! = 1,152`.

Enumerate all 1,152 assignments, identity included. Recompute all eight RVs and their maximum.

Exact one-sided p-value:

`p = count(T_perm >= T_obs) / 1152`.

## 11. Operational image-coverage gate

A candidate relation requires:

1. eight-way global exact `p <= 0.05`;
2. the winning image character has at least 8 centered usable blocks;
3. those blocks span at least 3 contributing folios.

If p passes but image coverage fails: `UNDERPOWERED / IMAGE-COVERAGE LIMITED`.

## 12. Formal-mask retention nuisance

Reuse the Phase67C paragraph retained fraction:

`innovation_retained / cleaned_tokens`.

For each of the eight image×lexical cells:

- within matching usable blocks, center retained fraction within folio;
- compute image↔retention RV as a nuisance diagnostic;
- residualize the centered lexical matrix on centered retained fraction, no intercept;
- recompute the same eight-way exact maxT test after residualization.

If the primary p<=0.05 and the winning image character has retention-only p<=0.05, require the residualized eight-way global p<=0.05. Otherwise classify `TEXT-RETENTION CONFOUNDED`.

The residual analysis cannot rescue a failed primary test.

## 13. Sequential classification

Because Phase68A is adaptive after Phase67, even a clean gate-passing result is classified only:

`CANDIDATE FORMAL-RESIDUAL LEXICAL IMAGE↔BODY ASSOCIATION — INDEPENDENT REPLICATION REQUIRED`

A failed primary is `NOT SUPPORTED`.

## 14. What a null would mean

If Phase68A is null, the project should **not** keep cycling through nearby image traits or text tokenizations on these same 14 blocks.

The combined Phase66–68 evidence would then disfavor direct object-local coupling at three representational levels:

- label/surface;
- local body character structure;
- formal-residual lexical/family selection.

The next content frontier would move to a qualitatively different model: page/recipe-level organization, nonlocal reference, or an explicit cipher/shorthand/obfuscation family with prospective predictions.

## 15. Claim boundary

A positive Phase68A result would not identify plaintext, token meanings, plant names, language, or a cipher key. It would establish only that sealed image morphology contains prospective information about retained lexical/family selection after folio state and two strong formal channels are controlled.
