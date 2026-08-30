# Phase 56 — latent multiscale state map

The execution plan was frozen in `PLAN.md` before implementation.

## Phase 56A — canonical substrate: COMPLETE

`phase56_build_state_matrix.py` parses the actual ZL3b page-header metadata and preserves physical leaf and page-side separately.

Audited substrate:

- 226 page headers in source
- 4,087 included P-coded prose lines
- **206 page-sides**
- **99 physical leaves**
- **736 paragraphs**
- recto 104 / verso 102

The 197 page-sides overlapping the earlier Phase55 folio-feature map were regression-checked on TTR, token-unit length, edit-1 family coverage, previous-10 locality, line-position MI, and first/final entropy. Maximum absolute difference was **0.0** for every checked feature.

## Phase 56B — drift versus regimes: COMPLETE AS DEVELOPMENT DIAGNOSTIC

The initial global contiguous-block test suggested a smooth-neighbor advantage, but stronger follow-up tests changed the interpretation.

### Exact metadata-matched physical-distance gradient

Conditioning on identical **section + Currier + hand**, mean standardized fingerprint distance is:

- same physical leaf: **3.231** (106 pairs)
- leaf gap 1: **3.295** (233)
- gap 2: **3.534** (203)
- gap 3–5: **3.620** (530)
- gap 6–10: **3.637** (740)
- gap 11+: **4.340** (3219)

Therefore physical locality is not just a section/Currier/hand artifact.

### Largest exact stratum: Herbal / Currier A / hand 1

93 page-sides / 47 physical leaves. Interleaved leaf holdout:

- stratum mean MSE: **1.058**
- smooth distance predictor: **0.947**
- optimized dynamic-programming changepoint: **0.985**
- changepoint + smooth residual: **0.977**

Smooth interpolation is about 10.5% better than the stratum mean and beats explicit changepoints on average.

However, the changepoint model repeatedly places its main division around the large physical separation between the early Herbal-A block and its later reappearance. This may be block composition rather than a sharp within-block state transition.

### Main continuous Herbal-A block only

Restricting to Herbal / Currier A / hand 1 with physical leaf <=56 removes that separated recurrence. Interleaved holdout:

- global mean: **1.062**
- smooth: **1.065**
- changepoint: **1.062**
- mixed: **1.065**

The selected changepoint count collapses to one regime. Neither smooth drift nor discrete changepoints improve prediction inside this continuous block.

## Phase 56B decision

**H56-2: PARTIALLY SUPPORTED / REFINED.**

There is a real graded physical-locality signal after exact metadata matching. But it is not adequately described as one globally smooth physical trajectory, and simple sharp changepoints are also insufficient.

The current descriptive picture is:

> broad state/block differences or separated recurrences + physical locality, with weaker or non-predictive smooth variation inside at least the main continuous Herbal-A block.

This is precisely why the next step should be multivariate latent-state dimensionality rather than forcing physical order into a one-dimensional drift model.

## Phase 56C frontier — latent dimensionality

Next:

1. PCA / cross-validated low-rank reconstruction as the linear baseline;
2. held-out prediction versus number of latent dimensions;
3. nonlinear manifold sensitivity without treating visual separation as evidence;
4. determine whether a compact common basis exists and which axes track section, physical block, Currier/hand, paragraph/line structure;
5. use the result to define the structural component to be removed before residual content/cipher tests.
