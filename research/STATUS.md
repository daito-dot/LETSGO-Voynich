# Current research status

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and a manuscript-wide paragraph-entry formal role. What is not established is whether these structures encode independently grounded semantic content, arise from cipher/shorthand mechanics, or can be reproduced by a hierarchical nonsemantic generator.

Structural equivalence is not cipher equivalence. A pattern is promoted toward decipherment only when it predicts independently grounded content or transfers under a constrained encoder/mapping.

## Structural state through Phase 57

The audited hierarchy remains:

`broad document constraints`

`+ page-local token-family activation`

`+ paragraph-entry / body-state transition`

`+ line-position grammar`

`+ token morphology / edge-pattern / {k,t}-related dimensions`

Physical locality survives exact section+Currier+hand matching but is not one simple smooth drift. Matched-token structural variation is moderately low-dimensional. Phase57 promoted only the leading approximately two-dimensional residual subspace; higher residual axes remain too representation/scale-sensitive for semantic rescue.

## Phase 58 — content tests

### 58A nuisance transfer

The promoted 2D residual does not predict recto/verso or coarse physical-position bins above matched nulls. It is not obviously a leftover simple manuscript-location code.

### 58B visual/content pilots

Independently defined page-level visual properties failed in two narrow matched domains:

- Biological/balneological: blue pool/water p=.921; green pool/water p=.155; animal/special animal p=.649.
- early Herbal-A: veined leaves p=.327; multiple flowers p=.982; flat-topped root p=.311; broad reproductive structure p=.220.

No relation is supported. Page-level visual semantics therefore remain negative at the promoted residual representation.

### 58C localization

A defensible paragraph-to-illustrated-subobject mapping was not available from the current external annotations without post-hoc pairing. Localized semantic testing remains blocked rather than guessed.

## Phase 59 — medieval entry grammar comparison

Dante continuous prose does not reproduce the Voynich multivariate paragraph-entry trajectory. However, source-native medieval Latin item/section markers in medical and other structured manuscripts do produce partially similar entry transitions.

In the current development comparison, an external rank-2 medieval-entry basis learned without Voynich explains about 65% of Voynich transition energy. A substantial Latin-orthogonal Voynich component remains and transfers positively across H/B/P/S/T.

The accepted interpretation is therefore:

`generic medieval entry/register grammar + Voynich-specific specialization`

rather than either "Voynich-unique state machine" or "ordinary Latin paragraphing explains everything".

## Phase 60 — falsification of a narrative model

A frozen narrative proposed that Voynich is a structured practical/technical manuscript with a specialized paragraph-entry register. The stronger version also proposed that entry state initializes later paragraph body state.

### 60A — pseudo-boundary falsification: PASS

Real paragraph line0->line2 transitions strongly exceed internal pseudo-boundaries within the same paragraphs. In physical-leaf cross-fitting, real > pseudo in all five folds. The paragraph boundary is therefore a genuine special structural position rather than an arbitrary two-line fluctuation.

### 60B — feature attribution: PASS WITH SPECIFIC CARRIERS

Across raw EVA, conservative composites and Phase56 composites, the entry/body transition is carried mainly by:

- k/t-family usage and balance;
- edit1 / near-family activation;
- local previous-10 near-family continuity;
- token/unit length and TTR;
- stable first/last-edge changes.

The effect is not mainly total entropy or inventory-size noise.

### 60C — held-out-section transfer: PASS

A section-blind structural entry/body role transfers to every held-out H/B/P/S/T section. Broader structural models add paired entry-vs-body discrimination beyond length/frequency nuisance baselines in every section, with page-bootstrap intervals above zero.

Several EVA edge-pattern coefficient directions remain invariant across all five outer held-out-section fits. This establishes a manuscript-wide formal paragraph-entry role, not its semantic meaning.

### 60D — recovery-vector prediction: NOT ACCEPTED AS INITIALIZATION EVIDENCE

A strong prediction of line2-line0 recovery from line0 was observed, but the target algebraically contains line0. This creates mathematical coupling/regression-to-the-mean risk.

### 60D2 — prospective absolute future-state test: FAILS P60-4

The coupling-free test asks whether line0 improves prediction of absolute line3 after line1 and metadata are known. It does not.

Current repository result:

- line1-only MSE: 0.3721
- line0+line1 MSE: 0.3857
- relative change from adding line0: -3.64%
- page-cluster 95% interval for error reduction: [-0.0257, -0.0043]
- all H/B/P/S/T section-specific gains are negative.

The actual entry is only slightly better than a wrong entry when both are added, and both are worse than omitting line0 entirely.

Therefore the strong "entry initializes and controls later paragraph state" interpretation is withdrawn.

## Current accepted Phase 60 narrative

Retain:

> Voynich has a manuscript-wide, transferable, short-lived paragraph-entry register/formal role, partly homologous to medieval structured-document entry grammar and partly specialized in Voynichese.

Do not currently claim:

> the first line carries persistent information that initializes the later paragraph body.

The special entry state appears to be largely absorbed by the next line at the level of the tested structural fingerprints.

This remains compatible with meaningful practical text, cipher/shorthand, hierarchical formal generation, and mixed mechanisms.

## Immediate frontier — Phase 60E / memory-horizon mechanism challenge

The next mechanism comparison must target the narrower surviving phenomenon, not the falsified persistent-initialization story.

Priority tests:

1. estimate the true short memory horizon using coupling-free prospective tests (line0 contribution to line1, line2, line3... absolute states while conditioning appropriately);
2. challenge stationary/simple formal generators: can they reproduce the transferable entry-vs-body signature without an explicit entry mechanism while retaining prior matched constraints?;
3. challenge bounded cipher transforms of structured medieval prose against the same entry signature;
4. only if a structural/cipher mechanism fails and independent localized content evidence becomes available, return to semantic promotion.

## Important corrections retained

- Phase3 plant-label result: 2 total 4-gram hits; exact permutation p=.725; binary pair-hit p=.667. NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55; universal paragraph-reset claim withdrawn.
- Phase56 unmatched full-page PC1 was contaminated by token count (r≈-.886); matched-token results supersede it.
- Phase60D recovery-vector prediction is not evidence for initialization after Phase60D2 removed mathematical coupling.

## Methodological rules

- Observation -> Structure -> Mechanism -> Content relation -> Decipherment.
- Preserve relevant known structure in nulls.
- Keep exploratory/model-selection/held-out/prospective/external-replication labels distinct.
- Audit page-side vs physical leaf explicitly.
- Equalize or model estimator sample-size effects.
- Search freedom belongs inside null/model-selection folds.
- Negative results and corrections remain recorded.
- Do not preserve a narrative after its hard prediction fails; narrow it explicitly.
- Decipherment requires executable mapping, substantial unseen prediction, fixed interpretable output, strong competitors/nulls, and prospective/external replication.
