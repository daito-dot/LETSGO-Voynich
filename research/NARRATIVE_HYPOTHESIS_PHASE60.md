# Phase 60 narrative hypothesis — a structured practical manuscript with a specialized entry register

Status: **frozen narrative hypothesis before Phase60 falsification tests**.

This document is deliberately narrative. It is not a claim of decipherment and it is not allowed to absorb later anomalies by adding unconstrained exceptions.

## Narrative hypothesis N60

The Voynich Manuscript is best provisionally modeled as a **meaning-bearing practical/technical manuscript** whose text is generated through a constrained writing system with two superposed components:

1. a broad medieval manuscript entry/register grammar shared with other structured Latin manuscripts;
2. a Voynich-specific encoding or morphographic layer that reorganizes token families, line roles and local paragraph state more strongly than ordinary Latin prose.

Under this narrative, the writer is not generating each token independently and is not merely copying neighboring words. The writing process operates with a local state.

A new paragraph/item begins in an **entry state**. The first line preferentially uses a restricted subset of forms or formal roles that introduce, classify, label, index, or otherwise initialize the item. Over the next one to three lines, the text relaxes into a **body state** where token-family activity broadens and local continuity increases.

The same underlying writing system is used throughout the manuscript, but its local state varies with document role, physical neighborhood and section. This produces:

- strong token-internal grammar;
- line-position effects;
- paragraph-entry -> body transitions;
- local activation of near-form token families;
- section/document-role differences;
- physical/page-local similarity;
- a shared medieval entry component plus a Voynich-specific remainder.

The manuscript may encode natural language, a systematic cipher, a morphographic shorthand, or a mixed system. N60 does **not** choose among those subfamilies yet. Its distinctive claim is that the observed structure is produced by a meaningful structured-document workflow rather than by one stationary token generator or arbitrary pseudo-text.

## Why this narrative is currently economical

It jointly accommodates findings that previously looked separate:

- high near-family density is not itself evidence of literal copying;
- line-position grammar is easy to generate but remains strongly organized in the manuscript;
- simple paragraph-local topic/family models fail because they overproduce generic clustering;
- the paragraph-entry trajectory transfers across major Voynich sections;
- medieval Latin source-marker entries explain a substantial part (~65% of transition energy in the current development comparison) but not all of it;
- the Latin-orthogonal remainder remains positive across H/B/P/S/T;
- simple visual page content has not yet correlated with the robust paragraph residual.

The narrative therefore treats paragraph and line structure as part of the writing/encoding procedure, not as incidental formatting.

## Hard predictions

N60 is weakened or rejected if these predictions fail.

### P60-1 — entry-state restriction is local and directional

The Voynich-specific Latin-orthogonal entry component should be concentrated in first-line token architecture and should decay over the next one to three lines. It should not appear equally strongly at arbitrary internal line positions.

Falsification: matched pseudo-boundaries inside paragraphs reproduce the same orthogonal trajectory with comparable magnitude and direction.

### P60-2 — the entry signal should decompose into interpretable structural features

A small subset of audited token/line features should carry most of the Latin-orthogonal transition. The effect should not require dozens of unstable representation-specific statistics.

Falsification: the orthogonal component is diffuse, changes sign under reasonable token-unit definitions, or depends primarily on one estimator artifact.

### P60-3 — paragraph starts should preferentially recruit a restricted formal vocabulary/role inventory

After controlling section, page and token frequency, first lines should over-recruit particular token families / prefixes / suffixes / slot patterns and under-recruit others. These preferences should recur across H/B/P/S/T with section-specific modulation.

Falsification: entry/body classification collapses after frequency and length matching, or the predictive families are entirely section-specific with no transferable basis.

### P60-4 — body-state recovery should be predictable from the entry state

If entry lines initialize a structured item, the direction or magnitude of the following recovery should depend on the entry state's structural composition. Entry features should predict at least some held-out line2/body-state coordinates beyond section/page baseline.

Falsification: entry state has no prospective predictive relation to its own paragraph body once broad metadata is controlled.

### P60-5 — random formal generation should need explicit entry machinery

The frozen simple DSL and stationary generators should fail the Latin-orthogonal entry component unless they are given an explicit paragraph-entry state or equivalent mechanism.

Falsification: a stationary or weakly contextual formal generator reproduces the orthogonal component without explicit entry state and without degrading previously matched statistics.

### P60-6 — ordinary encryption should not automatically create the specialization

Applying bounded cipher transforms to meaningful medieval prose may alter generic entry geometry, but a simple substitution/transposition-like family should not consistently create the Voynich-specific orthogonal remainder.

Falsification: a broad but low-complexity cipher family repeatedly maps medieval prose into the same orthogonal transition while preserving the other Voynich structural constraints.

### P60-7 — content relation should emerge only after the structural layer is modeled correctly

The absence of page-level visual correlations is compatible with N60 because page illustrations may be too coarse. If the manuscript is meaning-bearing, a sufficiently localized independent content target should eventually correlate with some residual state or token-role pattern after structural nuisance removal.

Falsification is not immediate here: failure of one content test is insufficient. N60 is materially weakened if multiple independently annotated, properly localized content domains fail under pre-registered tests while formal generators increasingly explain the full structural fingerprint.

## Strong rival narratives

### R60-A — hierarchical meaningless formal generator

The manuscript is produced by a designed generator with paragraph-entry, line and local-family states but no encoded semantic content.

This rival currently explains much of the structural evidence and is the strongest non-semantic alternative. N60 must outperform it on independent content prediction, not aesthetic plausibility.

### R60-B — encrypted practical text

The underlying document is meaningful practical prose, but the Voynich-specific specialization is primarily a cipher-state artifact rather than a morphographic/document-role grammar.

This is a subfamily close to N60 and will require bounded encoder tests to separate.

### R60-C — elaborate scribal shorthand / morphographic notation

The manuscript is meaningful but its token system represents recurring functional/morphological units rather than ordinary alphabetic plaintext. Entry lines use special functional forms analogous to headings, labels, recipes or classificatory markers.

This is also close to N60 and may ultimately fit better than conventional cipher language.

### R60-D — adversarial/deceptive pseudo-text

The manuscript intentionally imitates structured technical writing while frustrating semantic recovery.

This rival is admissible only with a bounded generative rule. It receives no credit simply because semantic tests fail.

## Phase60 test order

1. **60A pseudo-boundary falsification** — compare real paragraph starts with matched internal pseudo-starts using the frozen Latin-orthogonal direction.
2. **60B feature attribution** — identify which stable token/line features carry the orthogonal component; repeat across token representations.
3. **60C transferable entry vocabulary/roles** — train on sections, predict entry vs body in held-out sections under length/frequency matching.
4. **60D prospective recovery** — predict line2/body state from entry-line state on held-out pages.
5. **60E generator/cipher challenge** — test frozen stationary/formal and bounded cipher controls against the same orthogonal target.

Only after 60A-60E should the narrative be revised.

## Decision rule

N60 gains support only if multiple hard predictions survive. One successful test is not enough.

If P60-1 through P60-4 fail, abandon the item-initialization narrative even if the paragraph-entry mean remains statistically unusual.

If P60-1 through P60-4 survive but P60-5/6 show that simple nonsemantic or cipher mechanisms reproduce the same joint fingerprint cheaply, prefer those simpler mechanisms.

If structural predictions survive and independent localized content prediction later succeeds, promote the meaning-bearing branch. Until then, N60 remains a falsifiable working narrative rather than a decipherment claim.
