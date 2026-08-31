# Phase 66C-D — direct illustrated image↔body control

Status: **BLOCKED BY SOURCE-IMAGE ACCESS; NOT A SCIENTIFIC NEGATIVE**

## Frozen test

`PLAN_D_IMAGE_BODY.md` preregistered an exact categorical agreement control using the same three Phase66 morphology characters:

- leaf composition
- leaf arrangement
- leaf margin

The paired prose side was then conservatively reduced to exact frozen states in `BODY_STATE_TABLE_D.json`, yielding exactly 12 non-U species×character cells before any image↔body comparison.

The frozen operational gate required at least 12 jointly observed cells, A >= 0.60, and one-sided Monte Carlo p <= 0.05.

## Source audit

The 1868 *Canadian wild flowers* source is verified in Wikimedia Commons, including the complete 113-page public-domain PDF and ten separately catalogued color plates. `Plate 2 Canadian wild flowers.jpg` is explicitly catalogued at 1530×2185 and is also indexed by PICRYL as a public-domain botanical plate from the work.

However, the current execution environment could not retrieve the actual Plate 2 pixels through a reproducible inspection path. The affected plate contains:

- Pyrola elliptica
- Moneses uniflora
- Rubus odoratus
- Veronica americana

Three of the twelve exact prose-side cells belong to those species:

- Pyrola elliptica — leaf margin
- Moneses uniflora — leaf arrangement
- Rubus odoratus — leaf margin

Therefore, even under perfect image observability for every other species, the maximum possible jointly observed coverage in this runtime is 9/12, below the frozen minimum of 12.

## Decision

No permutation test was run and no p-value was manufactured from the incomplete image population.

Classification:

> **BLOCKED_SOURCE_IMAGE_ACCESS**

This is not a failed positive control. It is an input-provenance/access block.

No state was filled from species knowledge or from the prose in order to repair the missing plate.

## What remains valid

The earlier Phase66C body-text calibration is unaffected:

- 14/24 fixed illustrated species have prose explicitly stating at least one of the three primary morphology categories;
- 24/24 have at least one explicit extended morphology/color statement;
- the literal Latin binomials directly state none of the three primary morphology categories under the frozen rule.

That result already demonstrates a key detector limitation:

> A known meaningful illustrated botanical work can carry depicted morphology in its body prose while the short plant-name string does not surface-encode those attributes.

Therefore Phase65B/66B remain valid negative tests of short-label surface coupling, but they are not generic tests for whether botanical morphology appears elsewhere in associated text.

## Next research frontier

Do not repair Phase66B with new short-label features.

The justified next prospective Voynich test is a **surrounding-body categorical encoding test**: freeze an objective text neighborhood around each fixed pharmaceutical plant fragment, build morphology-blind structural features from those longer text units, and test whether the sealed image morphology states predict systematic body-text differences under physically constrained permutation.

This is a new hypothesis and must be preregistered before any morphology↔surrounding-text association is inspected.
