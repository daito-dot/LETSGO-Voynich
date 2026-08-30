# Phase 56 plan — latent multiscale state map

Status: **pre-execution plan**. This file freezes the order of work and evaluation logic before Phase56 implementation begins.

## Objective

Build an audited structural state representation of the Voynich Manuscript before returning to generator or decipherment hypotheses.

The goal is to separate predictable document/manuscript structure from residual variation that might later carry semantic or cipher information.

## Canonical hierarchy

All analyses must preserve explicit identifiers for:

`manuscript -> section/document role -> physical leaf -> page-side -> paragraph -> line -> token`

Cross-cutting metadata retained separately:

- Currier language label
- hand/scribe label
- recto/verso
- physical order
- source line type / paragraph-start markers

No analysis may silently collapse page-side to leaf.

## Phase 56A — canonical structural state matrix

Create audited tables at three scales:

1. page-side
2. paragraph
3. line

Feature families:

- token count / type count / type-token ratio
- token-length moments and quantiles
- collapsed-unit length moments
- edit-distance-1 family coverage
- local previous-N near-family continuity/excess
- first/middle/last line-position composition
- prefix/suffix/medial unit frequencies
- slot-occupancy / token-shape features already established in earlier phases
- selected structural-equivalence indicators such as `{k,t}` balance where defined
- paragraph-relative line position and paragraph-entry indicators

Every matrix row must carry explicit unit provenance and row-generation version.

Deliverables:

- `phase56_build_state_matrix.py`
- compact schema/summary JSON
- CSV/JSONL matrices when repository size permits
- audit counts by section, Currier, hand and physical unit

## Phase 56B — smooth drift versus changepoints

Within comparable strata, compare three descriptions of physical-order variation:

- smooth local drift
- discrete changepoints / regimes
- mixed regimes plus within-regime drift

Linear/state-space methods and nonlinear/changepoint methods are both allowed.

Evaluation must be predictive: hold out page-sides or blocks and compare reconstruction/prediction error. Visual embeddings alone are not evidence.

## Phase 56C — latent dimensionality

Estimate the smallest useful latent state dimensionality.

Required complementary views:

- PCA / linear low-rank model
- cross-validated low-rank prediction
- nonlinear embedding/manifold sensitivity analysis
- clustering/state-model stability where justified

Primary decision statistic: held-out predictive adequacy as a function of latent dimension.

## Phase 56D — transfer and residualization

Test whether learned latent coordinates transfer:

- within section across physical distance
- across sections under matched Currier/hand where possible
- across hands within matched section/Currier where possible

Then predict known structural features from the accepted latent state and save residuals.

Residuals become the future target for semantic/cipher/content tests only if they are:

- stable to transcription/preprocessing sensitivity
- reproducible across held-out units
- not explained by known metadata or physical order

## Frozen hypotheses

### H56-1 — compact latent state
A small number of latent dimensions predicts a substantial fraction of held-out structural variation.

Reject/weaken if prediction improves diffusely across many unrelated dimensions with no stable compact representation.

### H56-2 — physical drift
After broad section/document-role control, nearby physical leaves/page-sides remain more mutually predictive than distant ones with a graded distance relationship.

Reject/weaken if the Phase55 distance gradient disappears after matched-stratum auditing or is explained fully by discrete metadata/changepoints.

### H56-3 — shared grammar plus local state
A common structural basis transfers across sections while a smaller local-state component explains section/physical differences.

Reject/weaken if major sections require essentially separate high-dimensional grammars and cross-section transfer collapses.

### H56-4 — stable residual opportunity
After structural prediction, stable nontrivial residual variation remains that can be tested against independent content evidence.

Residual variance alone is not support. It must survive preprocessing/transcription controls and predict independent evidence.

## Evaluation discipline

- Phase55/earlier statistics are exposed development information.
- Any feature selected after examining Phase56 results is development-only.
- Physical leaf, page-side, paragraph and line are distinct units in all resampling/CV.
- Bootstrap/CV units follow the causal/document hierarchy rather than individual tokens.
- Section, Currier and hand are treated as confounded observational labels unless a crossed comparison makes an independent effect identifiable.
- Linear and nonlinear methods are compared on the same held-out splits.

## Stop condition

Do not return to generator tuning or decipherment tests until Phase56 provides audited answers to:

1. what structural scales are independently required;
2. smooth drift versus discrete regimes;
3. approximate latent dimensionality;
4. which metadata labels retain independent predictive value;
5. what stable residual target remains.
