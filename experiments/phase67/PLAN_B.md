# Phase 67B — pharmaceutical root architecture -> local body paragraph

Status: **FROZEN BEFORE ROOT-STATE ANNOTATION AND ROOT↔TEXT ASSOCIATION**

Date: 2026-08-31

## Why this is a new test

Phase67A tested three leaf characters and was null. Its image audit also established, before this plan, that many pharmaceutical blocks — especially f99r/f99v — are dominated by roots, storage organs, or subterranean-looking fragments and therefore have little usable leaf geometry.

Phase67B does **not** alter or rescue Phase67A. It asks a new, prospectively fixed question using a morphology character that already existed in the Phase66 annotation schema before Phase67A:

> Does the distribution of depicted root/subterranean architecture in a pharmaceutical illustration block predict the immediately following body-paragraph character structure after folio-local state is removed?

Because this hypothesis was selected after observing the Phase67A null and the image-side leaf missingness, a positive Phase67B result is classified only as a **candidate** until it reproduces on an independent pharmaceutical population.

## Population and text side

Reuse without change:

- `BLOCK_MANIFEST_A.json` — the same 14 objectively delimited blocks;
- `TEXT_TABLE_A.json` — the same sealed ZL3b paragraph strings;
- the primary text representation and cleaning from `PLAN_A.md`;
- the same within-folio centering.

No paragraph boundary or text token may be changed for Phase67B.

## Frozen image character

Use exactly the pre-existing Phase66A `root_subterranean_architecture` states:

- `single_primary_root_like`
- `branched_root_system`
- `fibrous_tufted_roots`
- `swollen_tuberous_or_storage_like`
- `bulb_corm_or_compact_storage_body_like`
- `rhizome_or_horizontal_axis_like`
- `mixed`
- `U`

Each fixed plant-fragment object in `BLOCK_MANIFEST_A.json` receives exactly one state.

Rules:

- use only directly visible root/subterranean geometry;
- `U` when no subterranean/root-like organ is visible or the architecture cannot be resolved;
- do not infer from plant identity, label spelling, body text, or resemblance to an external species;
- where the same object already has a sealed Phase66 root architecture state, reuse that state verbatim;
- do not change states after the Phase67B association statistic is opened.

## Block vector

Within each block:

- exclude `U` from the architecture distribution;
- calculate proportions over the seven non-U states;
- Hellinger-transform each proportion with `sqrt(p)`;
- a block with zero non-U root observations is unusable.

Also record block root observability as `non-U object count / fixed object count` for a nuisance control.

## Primary text representation

Exactly Phase67A primary text features:

- conservative complete-token cleaning;
- within-token character n-grams n=1,2,3;
- vocabulary defined by occurrence in at least two of the 14 frozen paragraphs;
- relative frequency within n;
- Hellinger transform;
- equal `1/sqrt(3)` scaling of n=1,2,3 feature blocks.

## Folio-state control

Retain root-usable blocks only. Within each folio with at least two root-usable blocks, center both the root architecture vectors and text vectors by subtracting that folio's mean.

Folios with fewer than two root-usable blocks contribute no centered information.

## Primary statistic

Compute one normalized RV coefficient between centered root architecture matrix `X` and centered text matrix `Y`:

`RV = ||X^T Y||_F^2 / sqrt(||X^T X||_F^2 * ||Y^T Y||_F^2)`.

There is one frozen morphology character, so there is no within-Phase67B character maxT search.

## Exact null

Use exactly the same within-folio paragraph reassignment space as Phase67A.

The corrected full population has:

`4! * 3! * 2! * 1! * 2! * 2! = 1,152`

assignments. Enumerate all 1,152, identity included.

Exact one-sided p-value:

`p = count(RV_perm >= RV_obs) / 1152`.

## Coverage / observability control

Use the same procedure fixed before Phase67A reveal:

1. within-folio-center scalar root observability coverage `C`;
2. compute coverage-only RV against centered text;
3. residualize centered root architecture columns on centered coverage with no intercept;
4. recompute root↔text RV from the residualized root matrix;
5. run the same 1,152 exact permutations for both diagnostics.

If primary p<=0.05 but coverage-only p<=0.05, require the residualized root RV to have p<=0.05 before retaining a candidate association.

## Operational gate

The root result can be called a candidate association only if:

1. primary exact p<=0.05;
2. at least 8 centered root-usable blocks remain;
3. those blocks span at least 3 contributing folios (each contributing folio has at least two usable blocks by construction);
4. the observability rule above is satisfied.

## Frozen secondary sensitivity

Repeat with text n=1,2 only. It cannot rescue a failed primary n=1,2,3 test.

## Sequential-research classification

Because the root hypothesis was chosen after the leaf test failed, even a gate-passing result is labeled:

`CANDIDATE ROOT↔BODY ASSOCIATION — REPLICATION REQUIRED`

It becomes a supported structure only after a separately frozen independent replication on earlier pharmaceutical folios not used in Phase67A/B.

A primary p>0.05 is `NOT SUPPORTED`.