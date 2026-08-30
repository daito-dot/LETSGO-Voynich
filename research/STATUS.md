# Current research status

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and paragraph/line state dynamics. What is not yet established is whether the remaining variation preserves semantic information from a natural language or cipher, or can be generated without meaning by a sufficiently constrained formal process.

Structural equivalence is not cipher equivalence. A pattern is promoted toward decipherment only when it predicts independently grounded content or transfers under a constrained encoder/mapping.

## Current evidence frontier — through Phase 56

### Token and line structure

Strong token-internal positional constraints and line-position effects are reproducible. Removing within-slot token values can still preserve useful structural/document-role information in some tests. This supports a formal role/state interpretation but does not identify plaintext values.

### Local token families

Voynich tokens form unusually dense edit-distance-1 / near-neighbor families. Local activation of related token families occurs at short scales. Literal online copy-and-modify is weakened: edit geometry is largely inventory-driven and there is no clear earlier-source directional asymmetry.

### Audited multiscale hierarchy

Phase56 established a canonical substrate that keeps physical leaf, page-side, paragraph, line and token units distinct. It reproduces the overlapping Phase55 page fingerprints exactly under shared definitions.

The earlier simple hierarchy has been refined to:

`broad document constraints`

`+ page-local token-family activation state`

`+ transferable paragraph-entry transition`

`+ line-position grammar`

`+ token morphology / edge entropy / {k,t}-related dimensions`

Hand and Currier cut across this hierarchy but remain heavily confounded with section in parts of the manuscript.

### Physical locality: real but not one smooth drift

After exact matching on section + Currier + hand, structural fingerprint distance increases with physical separation. However, smooth-distance and explicit changepoint models do not yield a single adequate one-dimensional physical trajectory inside the largest continuous Herbal-A block.

H56-2 is therefore refined: physical locality is real, but the current description is broad state/block differences plus local similarity rather than one globally smooth drift or a few sharp regimes.

### Latent dimensionality: moderately low-dimensional

A critical Phase56C audit found that unmatched full-page PCA was contaminated by page token count (original PC1 r=-0.886 with n_tokens). The previous interpretation of that PC1 as a dominant section axis is withdrawn.

With matched-token windows, page-side variation is distributed over several structural dimensions:

- first 3 PCs: ~63.7%
- first 5 PCs: ~78.7%
- first 7 PCs: ~90.0%

The leading matched axis is primarily near-family activation / local continuity rather than section. Similar leading directions recur at paragraph scale. Linear PCA outperforms RBF kernel PCA in grouped held-out reconstruction; no nonlinear-manifold advantage is established for these matched fingerprints.

### Paragraph entry is a transferable multivariate state transition

The corrected paragraph-entry effect is not only a drop in one continuity statistic.

Using a 5D matched paragraph-trained latent basis and centering line states within page-side, the line0 -> line2 transition learned from other major sections transfers positively to every held-out H/B/P/S/T section. Held-out cosine similarity to the trained direction ranges from ~0.74 to ~0.97; page-bootstrap projection intervals remain above zero in all five sections.

Biological is weaker but still positive.

Thus a shared paragraph-entry/recovery dynamic is supported within the manuscript. This remains internal development evidence, not external replication.

### Structural residual target now exists

Phase56D constructed 635 matched paragraph fingerprints (>=20 body tokens). Independent resampling gives median split-half reliability ~0.964.

In physical-leaf-grouped cross-validation, section + Currier + hand + paragraph ordinal yields standardized MSE ~0.919. Adding leakage-safe page context from other paragraphs on the same page improves this to ~0.885.

Therefore known broad metadata and page-local context explain a real but minority share of stable paragraph variation. Substantial reliable paragraph-specific variation remains.

The leading cross-fitted residual axis has very little remaining association with broad labels (section eta2 ~0.005, Currier ~0.002, hand ~0.002). A modest page-local residual similarity remains, so the residual is not yet nuisance-free.

This residual is a **candidate future information-bearing target**, not evidence for semantics or cipher information.

### Paragraph-boundary audit correction retained

Phase53/54 accidentally collapsed recto and verso page-side IDs to common leaf IDs. Corrected analysis gives true-boundary gap ~+0.0899 across 206 eligible page-sides, with section dependence. The universal-reset interpretation remains withdrawn.

### Periodicity

Apparent fixed/drifting periodicities can be generated by token and boundary architecture. Stronger structure-preserving nulls remove the earlier periodic signal. Numerical/symbolic interpretations based on those recurrences are not supported.

### Semantic/content tests

Current pharmaceutical item-specific matching tests have not established a state-invariant mapping from structural token classes to item content. This is a negative result for the tested domain, not proof that the manuscript lacks meaning.

## Formal-generator branch status

The frozen simple DSL remains insufficient. Generator development remains paused until the new residual target passes robustness checks.

## Competing explanation families still open

1. meaningful natural-language text with unusual manuscript/genre structure
2. systematic information-preserving cipher
3. bounded deliberately deceptive/adversarial cipher
4. hierarchical formal generator with physical, paragraph and line state
5. mixed mechanisms

Deceptive-cipher explanations receive no credit merely because semantic tests fail. They must specify bounded nuisance mechanisms and outperform simpler alternatives after complexity charge.

## Immediate frontier: Phase 57 residual robustness gate

Before exposing Phase56 residuals to semantic/content/cipher hypotheses, test whether they survive reasonable analysis perturbations:

- alternative token-unit/collapse definitions
- matched-window length sensitivity
- richer but leakage-safe local structural predictors
- transcription/source sensitivity where feasible
- stability of residual axes and paragraph relationships across resampling

Only residual structure that survives this gate becomes the legitimate target for renewed content/cipher testing.

## Methodological rules

- Observation -> Structure -> Mechanism -> Content relation -> Decipherment.
- Preserve relevant known structure in nulls.
- Keep exploratory/model-selection/held-out/prospective/external-replication labels distinct.
- Audit unit definitions explicitly.
- Equalize or explicitly model estimator sample-size effects.
- Negative results and corrections remain recorded.
- Decipherment requires an executable mapping/generation rule, substantial unseen prediction, fixed interpretable output, strong competitors/nulls, and documented errors.
