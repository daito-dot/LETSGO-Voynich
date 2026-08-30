# Phase 65A plan — independently grounded localized content-anchor audit

Status: **PREREGISTERED / NO NEW VOYNICHESE CONTENT METRIC MAY BE COMPUTED IN THIS PHASE.**

Parent decision: `DECISION_65.md`.

## Objective

Determine whether at least one externally grounded, physically localized anchor population is strong enough to justify a separate frozen Phase65B content-relation test.

Phase65A evaluates the **quality of the mapping**, not whether Voynichese predicts the mapped content.

## Separation rule

During candidate admission/rejection:

- manuscript images/layout and external sources may be inspected;
- exact folio/object/text-unit identifiers may be recorded;
- prior published repository results may be read only to avoid duplicating already-failed tests;
- **no new feature, distance, clustering, classification, stem overlap or semantic score may be computed from the Voynichese strings of candidate units**;
- candidate selection may not depend on how promising the strings look.

## Hard admission gates

A candidate population must pass **all** gates A1–A6. There is no compensating aggregate score.

### A1 — source independence

The content-side identity/descriptor must be determined without using Voynichese textual similarity.

PASS examples:

- physical image morphology annotated from a text-blinded crop;
- a diagram identity evident from iconography and independently documented;
- a named identification supported by independent catalog/scholarly evidence not derived from the candidate Voynichese label.

FAIL examples:

- selecting an object because its label resembles a proposed word;
- selecting a scholarly identification whose main evidence is the proposed Voynichese reading;
- choosing candidate classes after inspecting new text-derived separability.

### A2 — physical localization

The content object and associated text unit must be localizable below broad page/section class by physical layout alone.

PASS requires an auditable rule such as adjacency, enclosure, leader/association geometry, or an externally documented object-label relation.

A whole Herbal/Pharma/Zodiac page class by itself is insufficient.

### A3 — mapping ambiguity

The object↔text assignment must be effectively one-to-one or have an explicit layout-only ambiguity set fixed before text analysis.

Primary admission requires either:

- unique mapping; or
- ambiguity set size <=2 with the ambiguity represented in the later null/test rather than resolved from the string.

### A4 — content specificity

The external target must vary at a resolution capable of producing a falsifiable prediction. Generic labels such as `plant`, `human`, `star`, `jar` alone do not pass.

Permitted targets include:

- blinded quantitative/ordinal visual morphology;
- independently fixed object identity/category more specific than broad section type;
- independently fixed relationships among localized objects.

### A5 — prospective population

The candidate must support a meaningful held-out or unseen-item design.

Primary pass requires one of:

1. >=20 localized units with a continuous/multivariate external target and a preregisterable item-level holdout;
2. >=3 externally fixed content classes with >=4 physically distinct localized units per class;
3. a repeated-identity design with >=6 physically distinct repetitions in total and an exact permutation/randomization test whose minimum attainable two-sided p-value is <=0.05.

Smaller scientifically interesting mappings may be recorded as secondary evidence but do not open Phase65B.

### A6 — contamination control

The proposed Phase65B target/test must not be a relabeling of an already inspected candidate-text relationship.

Prior negative results do not ban the same physical objects if the new target is independently defined and genuinely different. However the audit must state the prior exposure and why the new test is not outcome-selected from candidate strings.

## Candidate-family audit order

Audit in this order and stop only after all feasible families have been classified:

### V1 — localized image-object pairs

Look for exact object↔label/paragraph pairings where the image can supply text-blinded visual descriptors. Pharmaceutical/herbal small-object layouts are eligible only if physical attachment is auditable.

Important: species-name guessing is not required and is not the primary V1 route.

### V2 — independently identifiable diagrams

Audit zodiac/astronomical/cosmological or other diagram units whose depicted identity is externally clear. A diagram is admissible only if its associated text is physically localizable and the population satisfies A5; merely recognizing a zodiac sign is insufficient if the attached text relation or repetition structure is not testable.

### V3 — independently named objects

Audit specific botanical/astronomical/other identifications from catalog or scholarship. Because this lane is vulnerable to circular decipherment claims, primary admission requires at least two genuinely independent supporting sources or one authoritative catalog/source plus direct unambiguous iconographic identity, and still must pass A1–A6.

## Evidence record for each candidate

For every serious candidate family, record:

- candidate ID and object type;
- folio/object population definition;
- exact physical mapping rule;
- external source(s) and what they establish;
- whether the source used Voynichese reading as evidence;
- prior repository exposure relevant to contamination;
- A1–A6 PASS/FAIL individually;
- decisive rejection reason if any;
- whether a Phase65B preregistration is executable without inspecting candidate-string outcomes.

Negative candidates remain in the audit.

## Phase65A classification

Exactly one of:

### `M8-ANCHOR READY`

At least one candidate passes A1–A6 and can support a frozen Phase65B unseen-item content-relation test.

Required output before any Phase65B science:

- exact anchor population and source provenance;
- exact content-side target construction;
- exact text-side representation chosen from pre-existing repository machinery or otherwise independently motivated;
- holdout/null/permutation design;
- primary metric and pass/fail threshold;
- contamination statement.

### `M8-EXTERNALLY BLOCKED`

No audited candidate passes A1–A6.

Interpretation:

> Current external/localized mapping quality is insufficient for a clean content-relation test under the frozen standard.

This is not evidence of semantic absence.

## Prohibited Phase65A moves

- no plant/species name inference from Voynichese;
- no translation attempt;
- no choosing visual features because they correlate with candidate strings;
- no changing A5 after seeing sample sizes;
- no broad page-level visual classification already covered by Phase58;
- no post-hoc Naibbe/A1 repair;
- no promotion from structural mechanism evidence to semantic conclusion.

## Deliverables

- `ANCHOR_AUDIT_A.md` — complete positive/negative external audit;
- source/provenance table with stable URLs/identifiers where possible;
- if READY: a separate frozen Phase65B plan before any content score;
- if BLOCKED: update `research/STATUS.md`, `research/hypothesis-ledger.md` and `ROADMAP.md`, then move to the predeclared residual-C fallback.
