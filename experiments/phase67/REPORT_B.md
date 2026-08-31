# Phase 67B — pharmaceutical root architecture -> local body paragraph

Status: **CLOSED — NOT SUPPORTED**

## Question

Phase67A found no detectable relation between three leaf-morphology distributions and the immediately following pharmaceutical body paragraph after folio-local state was removed. Because much of the pharmaceutical imagery is root/storage-organ dominated, Phase67B prospectively froze a new test using the pre-existing Phase66 `root_subterranean_architecture` character.

The question was:

> Do differences in depicted root/subterranean architecture predict differences in the immediately following body-paragraph surface structure within the same folio?

## Frozen design

- Same 14 objective illustration→paragraph blocks as Phase67A.
- Same sealed ZL3b body paragraphs and the same conservative text cleaning.
- Root states were frozen before the root↔text association was opened:
  - single primary root-like
  - branched root system
  - fibrous/tufted roots
  - swollen/tuberous/storage-like
  - bulb/corm/compact storage-body-like
  - rhizome/horizontal-axis-like
  - mixed
  - U
- Block state proportions were Hellinger transformed.
- Both image and text matrices were centered within folio.
- Primary text representation used within-token character n=1,2,3 grams.
- Exact null: all 1,152 within-folio paragraph assignments, identity included.
- Frozen coverage gate: at least 8 centered usable blocks across at least 3 folios.
- Frozen observability control: root-state coverage alone and coverage-residualized root architecture.
- Predeclared secondary sensitivity: n=1,2 grams only.

Because the root hypothesis was selected after the Phase67A leaf null, even a positive result would have been classified only as a replication-required candidate.

## Primary result

The coverage gate was comfortably met:

- centered usable blocks: **13 / 14**
- contributing folios: **5** — f99r, f99v, f100r, f102v2, f102v1

Observed association:

- root/body RV = **0.61288**
- exact p = **0.41840** (482 / 1,152 assignments at least as large)

The result is not close to the frozen `p <= 0.05` threshold.

Observability diagnostics were also null:

- coverage-only p = **1.00000**
- coverage-residualized root/body p = **0.47135**

Thus the null is not explained by the fact that some blocks expose more classifiable root geometry than others.

## Frozen secondary sensitivity

Using only character 1/2-grams:

- RV = **0.61742**
- exact p = **0.30556** (352 / 1,152)
- coverage-only p = **1.00000**
- coverage-residualized p = **0.31163**

The predeclared sensitivity is also null.

## Decision

Phase67B is classified:

> **NOT SUPPORTED**

Within these objectively paired Quire 19 pharmaceutical blocks, the depicted root/subterranean architecture does not predict the surface character-ngram structure of the immediately following paragraph once folio-local state is respected.

Together with Phase67A, this closes the simplest image-morphology→local-body-surface route for the current detector:

- leaf composition / arrangement / margin: null;
- root/subterranean architecture: null;
- short attached label surface form was already null in Phase66B.

This still does not establish that the illustrations and running text are semantically unrelated. The current negatives are all tests of relatively direct morphology-to-surface-form coupling. A relation could instead be carried by a higher-level formal representation, for example token-family innovations after the already-established short-range A1-like recurrence process is factored out.

## Provenance

Successful exact run:

- GitHub Actions run: `33383282015`
- job: `99460176681`
- scientific head: `5c0af4d23c5b92615ebad73cb39f22c967f53b9a`
- artifact: `phase67b-results`, ID `9754575208`
- artifact SHA-256: `20ec3b78b96425cf406251f223e699ca0ae32417d9866d478c7d636a85e03ea4`
