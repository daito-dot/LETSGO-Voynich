# Phase 67D — image morphology -> formal-residual lexical-family selection

Status: **CLOSED — NOT SUPPORTED**

## Question

Phase67C showed that image morphology does not predict the character-ngram structure of body tokens left after masking two established formal channels. Phase67D moved the text representation one level upward:

> Does image morphology predict **which lexical/edit1 token families** are selected among those retained innovation tokens?

The primary representation used the 279 retained token types as an overlapping closed edit1-family vocabulary. For each vocabulary type `v`, a paragraph counted retained tokens equal to `v` or at Levenshtein distance exactly 1 from `v`, then converted the family-count vector to Hellinger proportions.

No connected-component clustering or fitted edit-distance weight was introduced.

## Frozen design

- same 14 Quire 19 illustration→paragraph blocks;
- same Phase67C formal mask;
- same sealed leaf and root image states;
- same within-folio centering;
- four image characters corrected as one family by a maxT statistic;
- all 1,152 within-folio paragraph assignments enumerated exactly;
- retention-fraction nuisance control frozen in advance;
- exact retained token identity predeclared as a stricter secondary representation.

## Primary closed-edit1-family result

Observed RV values:

| Image character | RV | uncorrected exact p |
|---|---:|---:|
| leaf composition | 0.4274 | 0.7500 |
| leaf arrangement | **0.5784** | **0.0521** |
| leaf margin | 0.5523 | 0.6146 |
| root architecture | 0.5282 | 0.9948 |

The low-looking uncorrected leaf-arrangement value is exactly why the image-character family was frozen before reveal. After the required four-way correction:

- winner: `leaf_arrangement`
- maxT = **0.57841**
- global exact p = **0.73611** (848 / 1,152 assignments at least as large)

So this is not evidence for a leaf-arrangement content channel. The selected leaf-arrangement statistic is ordinary once the predeclared search over four image characters is included in the null.

Retention diagnostics also do not rescue it:

- winner retention-only p = **0.13542**
- retention-residualized winner: `root_subterranean_architecture`
- residual maxT = **0.49621**
- residual global exact p = **0.86285**

## Frozen exact-token sensitivity

Using exact retained token types instead of edit1-expanded families:

- winner: `root_subterranean_architecture`
- maxT = **0.58388**
- global exact p = **0.67622**
- retention-residualized global p = **0.66319**

This representation is also null.

## Decision

Phase67D is classified:

> **NOT SUPPORTED**

The Quire 19 pharmaceutical result is now broader than a single failed morphology feature. Under objective illustration→paragraph boundaries and exact within-folio controls, the tested leaf/root image morphology does not predict:

1. local body character n-grams;
2. those character n-grams after masking entry-register and previous-10 edit1-compatible tokens;
3. closed edit1 lexical-family selection among the retained innovation tokens;
4. exact retained token-type selection.

Combined with Phase66B, the same image traits also failed to predict the attached short-label surface form.

The repeated nulls make another variation of leaf/root feature engineering on these same 14 blocks a poor next experiment. A useful next step needs a different content anchor or a different structural question rather than another representation of the same morphology hypothesis.

## Provenance

- GitHub Actions run: `33383847456`
- job: `99461919730`
- scientific head: `ca084d3be1e1a9c39b508a970be66ba88e5671ea`
- artifact ID: `9754792280`
- artifact SHA-256: `f5ac49b42602c38bf69f69b8bf89a87de069e6712653d2c26bf51559783e2331`
