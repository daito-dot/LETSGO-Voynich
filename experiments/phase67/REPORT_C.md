# Phase 67C — image morphology -> A1-formal-residual body text

Status: **CLOSED — NOT SUPPORTED**

## Question

Phase67A/B found no direct relation between sealed leaf/root morphology and the raw character-ngram structure of the immediately following pharmaceutical paragraph. Phase67C tested whether that failure was caused by the strongest known formal processes dominating the text surface.

Before association, the text was filtered using two mechanisms already established by the structural program:

1. paragraph line-0 tokens were masked as entry-register compatible;
2. outside line 0, tokens at Levenshtein distance exactly 1 from any of the preceding ten cleaned tokens on the folio were masked as compatible with the short-range local-family process.

The question was then:

> Does image morphology predict the character structure of the tokens left after those formal-compatible tokens are removed?

The edit-distance-1 relation is exactly the historical Phase61C implementation relation; it was not invented from the Phase67 outcome.

## Mask strength

Across the 14 frozen Quire 19 blocks:

- cleaned body tokens: **685**
- paragraph-entry masked: **107**
- local edit1 masked: **155**
- retained innovations: **423**
- retained fraction: **61.75%**

The intervention therefore removed about 38% of the cleaned body tokens before the image↔text comparison.

## Primary n=1,2,3 result

The four-way image family was fixed as:

- leaf composition
- leaf arrangement
- leaf margin
- root/subterranean architecture

Observed RV values:

| Image character | RV |
|---|---:|
| leaf composition | 0.3627 |
| leaf arrangement | 0.5741 |
| leaf margin | **0.5777** |
| root/subterranean architecture | 0.4957 |

Family result:

- winner: `leaf_margin`
- maxT: **0.57770**
- exact within-folio p: **0.65712** (757 / 1,152 assignments at least as large)
- frozen coverage gate: pass

This is not a near-threshold result. Under the exact null, maxT had:

- mean: **0.59923**
- 95th percentile: **0.69568**
- maximum: **0.75106**

The observed value is below the null mean.

## Retention-fraction control

Different paragraphs retain different fractions after the formal mask, so retention fraction was frozen as a nuisance control.

For the primary winner, retention-only p was **0.16667**. After residualizing the retained-text vectors on paragraph retention fraction:

- winner became `root_subterranean_architecture`
- residual maxT: **0.42757**
- four-way exact p: **0.95573**

Removing retention variation makes the apparent image relation weaker, not stronger.

## Frozen n=1,2 sensitivity

The predeclared 1/2-gram-only analysis was also null:

- winner: `leaf_arrangement`
- maxT: **0.54701**
- global exact p: **0.75434**
- retention-residualized winner: root architecture
- retention-residualized global p: **0.98264**

## Decision

Phase67C is classified:

> **NOT SUPPORTED**

The result closes a fairly broad version of the simplest local content route tested so far. In these objectively paired pharmaceutical blocks, image morphology does not predict:

1. attached short-label surface structure (Phase66B);
2. raw local body-paragraph character structure (Phase67A/B);
3. body-paragraph character structure after masking tokens directly compatible with the established paragraph-entry and previous-10 edit1 formal channels (Phase67C).

This does **not** imply that the illustrations and text are unrelated. The remaining live models are qualitatively different. In particular, semantics may be carried by **which lexical/token family is selected**, while the character realization of that family is strongly shaped by the formal process already detected. A recipe/page-level relation, nonlocal organization, shorthand/cipher transform, or an intentionally obfuscating system also remains open.

The next content test should therefore not keep changing leaf/root traits or character n-grams. It should move one representational level upward and prospectively test lexical/token-family selection after the formal layer is controlled.

## Provenance

- GitHub Actions run: `33383613195`
- job: `99461202330`
- scientific head: `27123ff8e4e567dc39827fc91d4fb5eafd1aa086`
- artifact ID: `9754699347`
- artifact SHA-256: `34620cf4108cc2796cc1bd609360871083c629ddab2b7205bee2b5208a4603a4`
- primary raw result SHA-256: `c7c8e5f4ee1db8e4c59d2c1069dc9a9f52e925e518bf6a308a27e918d631a04c`
- n=1,2 raw result SHA-256: `a1c68d19829b07824d7f41699a86982e942acc4c0e20f6ef52bb72f9d96d101f`
