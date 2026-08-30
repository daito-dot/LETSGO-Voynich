# Next research frontier after the meta-analysis

Decision point after Phase55 and `META_ANALYSIS.md`.

## What should not happen next

Do not immediately resume generator tuning.

Do not search for another isolated correlation or visual reading.

Do not treat Currier, hand, section, folio and paragraph as independent labels without accounting for their observational confounding.

Do not optimize another model against the already exposed paragraph-reset / line-position targets and then call the fit validation.

## Frontier: latent multiscale state map

The next research block should determine the smallest useful state representation of the manuscript itself.

Working descriptive hierarchy:

`section/document role -> physical page/leaf drift -> paragraph dynamics -> line state -> token morphology`

The central question is not yet what historical mechanism produced those states. It is whether these apparent layers are genuinely distinct, how many latent dimensions they require, and which observed labels become redundant once physical and textual context are modeled.

## Phase 56A — structural state matrix

Construct one audited feature matrix at several observation scales:

- page-side
- paragraph
- line

Feature families should include morphology, token-family topology, line-position composition, local recurrence/continuity, token length, slot occupancy, and selected previously established structural equivalence features.

Every row must retain explicit metadata:

- full page-side id
- physical leaf id/order
- recto/verso
- section
- Currier
- hand
- paragraph id
- line index / paragraph-relative position

The purpose is to create one canonical analysis substrate and prevent unit-definition drift between phases.

## Phase 56B — smooth drift versus changepoints

Within comparable section/hand/Currier strata, test whether physical-order variation is better described as:

- smooth local drift;
- discrete changepoints;
- a mixture of stable regimes plus drift.

Use both linear/state-space descriptions and nonlinear/change-point methods. Compare predictive performance on held-out neighboring and non-neighboring page-sides.

## Phase 56C — latent dimensionality

Estimate how many latent coordinates are needed to reconstruct/predict the structural fingerprint.

Use complementary methods rather than trusting one embedding:

- PCA/factor-style linear compression;
- nonlinear manifold representation as exploratory sensitivity;
- cross-validated low-rank prediction;
- clustering/state models only where supported by stability tests.

The important statistic is held-out predictive adequacy versus dimensionality, not visual attractiveness of an embedding.

## Phase 56D — transfer and residualization

Test whether a latent representation learned in one part of the manuscript predicts structural features in another:

- within section across physical distance;
- across sections with same Currier/hand where possible;
- across hand with same section/Currier where possible.

Then residualize known structural variation. Preserve those residuals as the future target for content/cipher tests.

## Falsifiable hypotheses

### H56-1: low-dimensional state hypothesis

A small latent state (roughly a few dimensions rather than dozens of independent factors) predicts a substantial fraction of held-out structural variation.

Falsified if predictive performance continues to improve broadly with many unrelated dimensions and no stable compact representation emerges.

### H56-2: smooth physical drift hypothesis

After controlling broad section/document role, nearby physical leaves/page-sides remain more predictable from one another than distant ones, with a graded distance relationship.

Falsified if the Phase55 distance gradient disappears under audited matched strata or is explained entirely by discrete metadata/changepoints.

### H56-3: shared grammar plus local state

A substantial common structural basis transfers across sections while a smaller number of coordinates account for section/local differences.

Falsified if models require essentially separate high-dimensional grammars for each major section and cross-section transfer collapses.

### H56-4: meaningful residual opportunity

After structural state is modeled, nontrivial stable residual variation remains that can be tested against independent content/illustration/label evidence.

This hypothesis is not supported merely because residual variance exists. Residuals must be stable under transcription/control sensitivity and predict independent evidence.

## Stop condition for this block

Do not return to decipherment/generator selection until there is an audited answer to:

1. what the main structural scales are;
2. whether physical variation is drift or regimes;
3. approximate latent dimensionality;
4. which labels remain independently predictive after conditioning;
5. what residual target remains after structural prediction.

That residual target becomes the next legitimate search space for semantic or cipher information.
