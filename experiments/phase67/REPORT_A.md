# Phase 67A — pharmaceutical leaf morphology -> local body paragraph

Status: **CLOSED — NOT SUPPORTED**

## Question

Do differences in the depicted leaf morphology of pharmaceutical illustration blocks predict differences in the immediately following running text, after folio-local writing state is removed?

This was the direct follow-up to Phase66B. Phase66B found no simple leaf-attribute relation in short attached labels; Phase67A moved the response from the short labels to the longer body paragraph while keeping the image-side morphology vocabulary frozen.

## Frozen design

- 14 objectively delimited pharmaceutical illustration→paragraph blocks from f99r, f99v, f100r, f100v, f102v2, f102v1.
- Image characters: `leaf_composition`, `leaf_arrangement`, `leaf_margin` from the pre-existing Phase66A schema.
- Paragraph representation: ZL3b body text only, within-token character 1/2/3-gram relative frequencies after conservative uncertainty filtering and Hellinger transform.
- Both image and text vectors centered within folio.
- Three character-specific normalized RV coefficients; primary family statistic = their maximum.
- Exact paragraph reassignment only within folio.
- Full assignment space: **1,152**. (`PLAN_A.md` printed 2,304 despite writing the correct factorial expression; `ARITHMETIC_CORRECTION_A.md` documents this clerical error. The executable exhausted the correct 1,152 assignments.)
- Detection gate required global maxT p<=0.05 and at least 8 usable centered blocks across at least 3 folios.

## Primary result

All three image characters passed the frozen coverage gate with 9 centered usable blocks across four folios: f99r, f100r, f102v2, f102v1.

| Character | RV | uncorrected exact p |
|---|---:|---:|
| leaf composition | 0.3669 | 0.7500 |
| leaf arrangement | 0.6481 | 0.1771 |
| leaf margin | **0.6511** | **0.1667** |

The family-corrected primary statistic was:

- winner: `leaf_margin`
- maxT = **0.6511**
- global exact p = **0.1979** (228 / 1,152 assignments at least as large)

This does not pass the frozen `p <= 0.05` gate.

The null distribution itself was not far below the observed value:

- null mean maxT = 0.6064
- null 95th percentile = 0.6896
- null maximum = 0.7254

So the observed leaf/body alignment is not an isolated near-miss; this amount of multivariate similarity is common under correct folio-preserving reassignment.

## Observability control

The image population is uneven: f99r/f99v are heavily root/storage-fragment dominated, so leaf characters are often `U`. The pre-frozen coverage control did not itself reach p<=0.05 for the primary winner (`leaf_margin` coverage p=0.1198), but the stronger residual diagnostic was also null:

- coverage-residualized maxT = 0.5466
- residual winner = `leaf_margin`
- residual global exact p = **0.5313**

Thus removing variation associated with leaf observability does not uncover a hidden signal.

## Frozen secondary sensitivity

The predeclared 1/2-gram-only text representation was also null:

- winner: `leaf_arrangement`
- maxT = 0.6628
- global exact p = **0.1563**
- coverage-residualized global p = **0.4115**

It does not rescue the primary result.

## Decision

Phase67A is classified:

> **NOT SUPPORTED**

Within these frozen Quire 19 pharmaceutical blocks, the depicted distributions of leaf composition, leaf arrangement, and leaf margin do not measurably determine the surface character-ngram structure of the immediately following running paragraph once folio state is respected.

This result is narrower than "the pictures and text are unrelated." It leaves several distinct possibilities open:

1. the nearby paragraph can be semantically related without literally encoding these three leaf properties;
2. the salient pharmaceutical attribute may be root/subterranean architecture rather than leaves, especially on root-dominated f99r/f99v;
3. the relation may use a representation above raw character n-grams (units, syntax, transformations, or nonlocal paragraph structure);
4. illustration rows and paragraphs may share a page/recipe-level relation without one-to-one attribute coding.

Any root-architecture or higher-level representation test is a new hypothesis. It must be frozen separately and cannot be used to reinterpret Phase67A as positive.

## Provenance

Successful exact run:

- GitHub Actions run: `33382775064`
- scientific head: `1c1f4bd69ac0d994130c5991dbd4a3390a86fefa`
- artifact: `phase67a-results`, ID `9754391675`
- artifact SHA-256: `8fa56e61402300abfdde89c019360c9717c1f5895664a775dfcfe011fae11451`

The preceding workflow attempt failed before producing a scientific result because NumPy 2.5 rejected conversion of a 1x1 array directly with `float(...)`. The one-line `.item()` compatibility fix changed no data, statistic, or scientific rule.