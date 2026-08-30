# Current research status

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and paragraph/line state dynamics. What is not yet established is whether the remaining robust variation preserves independently grounded content information.

Structural equivalence is not cipher equivalence. A pattern is promoted toward decipherment only when it predicts independently grounded content or transfers under a constrained encoder/mapping.

## Structural state established through Phase 56

The audited hierarchy is currently:

`broad document constraints`

`+ page-local token-family activation state`

`+ transferable paragraph-entry transition`

`+ line-position grammar`

`+ token morphology / edge entropy / {k,t}-related dimensions`

Physical locality remains after exact section+Currier+hand matching, but is not one simple smooth drift. Matched-token structural variation is moderately low-dimensional: ~64% in 3 PCs and ~79% in 5. Similar leading directions recur across page and paragraph scales. Linear PCA currently beats nonlinear kernel compression.

The paragraph-entry/recovery transition is multivariate and transfers positively to held-out H/B/P/S/T sections when learned from the others. This is internal manuscript evidence, not external replication.

## Phase 57 residual robustness gate — PASS WITH NARROW TARGET

Phase56D's paragraph residual was stress-tested before semantic use.

The result is deliberately narrow: **only the leading approximately two-dimensional consensus residual is promoted**.

- reasonable EVA unit-definition changes rotate the residual somewhat, but retain a moderately aligned leading space;
- on a fixed eligible paragraph set, the top-2 residual subspace is stable across 15–40 token windows, while PC3+ is more scale-sensitive;
- richer leakage-safe same-page/opposite-side/adjacent-leaf context does not explain the residual away in the tested models;
- explicit cross-fitted section/Currier/hand removal leaves only small broad-label association in residual PC1/PC2 (eta² roughly .01–.03);
- physical-leaf bootstrap gives stable top-2 subspace orientation.

Higher residual axes are **not eligible** for post-hoc semantic rescue.

## Phase 58A nuisance transfer control — COMPLETE

Before content testing, the promoted 2D residual was tested against document/physical labels not explicitly removed.

Using physical-leaf-grouped CV and matched permutations within section|Currier|hand:

- recto/verso balanced accuracy **.445**, matched-null mean ~.498, upper-tail p=.978;
- coarse physical leaf bin balanced accuracy **.180**, matched-null mean ~.186, upper-tail p=.597;
- quire prediction is near nominal inverse-class-count performance but is high-cardinality and poorly supported across grouped folds, so it is descriptive only.

Thus there is no evidence that the promoted 2D residual is mainly a recto/verso or coarse physical-order nuisance code. This clears the tested nuisance gate but is **not positive semantic evidence**.

## Current semantic/content evidence

Earlier pharmaceutical item-specific/state-invariant mapping tests were negative. They predate the new robust residual and cannot be reinterpreted as tests of it.

The next content test must use labels defined independently of Voynichese and frozen before comparison. Same-state/matched permutation controls remain mandatory.

## Competing explanation families still open

1. meaningful natural-language text with unusual manuscript/genre structure
2. systematic information-preserving cipher
3. bounded deliberately deceptive/adversarial cipher
4. hierarchical formal generator with physical, paragraph and line state
5. mixed mechanisms

Deceptive-cipher explanations receive no credit from failed semantic tests alone. A deception mechanism must be bounded and complexity-charged.

## Immediate frontier: Phase 58B independently grounded content relation

The eligible predictor is fixed: the Phase57-promoted leading ~2D paragraph residual.

Before comparing it with content:

- define visual/content labels without reading Voynichese;
- document the annotation/data-selection rule;
- freeze labels before residual comparison;
- prefer within-page or same section+hand+Currier matching;
- compare against structure-only baselines and matched label permutations;
- do not reinterpret residual axis orientation after seeing labels.

A positive Phase58B result would establish an information-bearing relation only. It would not identify plaintext or constitute decipherment.

## Important corrections retained

- Phase3 plant-label result: 2 total 4-gram hits; exact permutation p=.725; binary pair-hit p=.667. NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55; universal paragraph-reset claim withdrawn.
- Phase56 unmatched full-page PC1 was contaminated by token count (r≈-.886); matched-token results supersede it.

## Methodological rules

- Observation -> Structure -> Mechanism -> Content relation -> Decipherment.
- Preserve relevant known structure in nulls.
- Keep exploratory/model-selection/held-out/prospective/external-replication labels distinct.
- Audit page-side vs physical leaf explicitly.
- Equalize or model estimator sample-size effects.
- Search freedom belongs inside null/model-selection folds.
- Negative results and corrections remain recorded.
- Decipherment requires executable mapping, substantial unseen prediction, fixed interpretable output, strong competitors/nulls, and prospective/external replication.
