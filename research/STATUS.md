# Current research status

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and a manuscript-wide paragraph-entry formal role. What is not established is whether these structures encode independently grounded semantic content, arise from cipher/shorthand mechanics, or can be reproduced by a hierarchical nonsemantic generator.

Structural equivalence is not cipher equivalence. A pattern is promoted toward decipherment only when it predicts independently grounded content or transfers under a constrained encoder/mapping.

For progress sequencing and the active decision gate, see `../ROADMAP.md`.

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

The external control panel remains small and heterogeneous, so the magnitude and dimensionality of this decomposition require broader manuscript/genre replication.

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

Repository result:

- line1-only MSE: 0.3721
- line0+line1 MSE: 0.3857
- relative change from adding line0: -3.64%
- page-cluster 95% interval for error reduction: [-0.0257, -0.0043]
- all H/B/P/S/T section-specific gains are negative.

The actual entry is only slightly better than a wrong entry when both are added, and both are worse than omitting line0 entirely.

Therefore the strong "entry initializes and controls later paragraph state" interpretation is withdrawn.

### 60E — memory horizon and mechanism challenge: COMPLETE

Coupling-free prospective tests across horizons line1-line4 show no reliable useful structural memory carried by line0 beyond metadata / immediately preceding state. The entry phenomenon is therefore better described as a short-lived position/register specialization than a persistent initializer.

The frozen Phase50 stationary/weak-context DSL also fails the entry-specific direction: its generated transitions can have comparable raw multivariate magnitude, but they are not concentrated at real paragraph entry and align poorly with the Voynich direction. This establishes a mechanism constraint: that generator family needs explicit boundary-conditioned machinery to reproduce the surviving entry signature.

Simple global boundary-blind ciphers are not rejected by paragraph-entry structure alone. Structured medieval plaintext can already contain entry/register differences that a position-independent cipher would inherit. Ciphering becomes explanatory only if it also accounts for Voynich-specific morphology, near-family/local continuity, line-position structure, or other independent constraints beyond what the plaintext already provides.

## Current accepted Phase 60 narrative

Retain:

> Voynich has a manuscript-wide, transferable, short-lived paragraph-entry register/formal role, partly homologous to medieval structured-document entry grammar and partly specialized in Voynichese.

Do not currently claim:

> the first line carries persistent information that initializes the later paragraph body.

This remains compatible with meaningful practical text, cipher/shorthand, hierarchical formal generation, and mixed mechanisms.

## Phase 61 — joint architecture discrimination

Phase61 moves from testing one entry statistic to comparing architectures against a joint target vector including entry specificity/direction, near-family density/local activation, line-position grammar, section modulation and short entry memory.

### 61A — A0 narrow entry gate: SURVIVES

A0 adds one explicit mechanism to a simple nonsemantic generator: paragraph line0 uses a separate entry-biased mixture, with no persistent paragraph state.

Under physical-leaf cross-fitting, this low-complexity boundary-aware mechanism can reproduce or exceed the scalar held-out Voynich entry-direction projection. Therefore the paragraph-entry signature by itself does not reject hierarchical meaningless generation once boundary awareness is granted.

### 61B — A0 joint scorecard: FAILS

The frozen A0 does not jointly reproduce the broader fingerprint.

Key diagnostic outcomes:

- global edit1 type density is close to Voynich only because the generator samples from an empirical Voynich vocabulary, so this is not an independent success;
- local-prev10 near-family activation is only about 6.7% of the Voynich level;
- mean line-position eta2 is about 3.3x the Voynich proxy;
- the multivariate entry-vs-pseudo norm is about 2.8x the Voynich value at the fixed diagnostic strength.

A0 is rejected as a sufficient joint model. A more complex nonsemantic model remains viable only if the added mechanism is frozen and charged explicitly.

### Current frontier — Phase 61C

`experiments/phase61/PLAN_C.md` is frozen before execution.

A1 adds exactly one new mechanism to A0: bounded local-family reuse / one-edit mutation in the body. It does not add persistent paragraph state, section-specific grammar, or a separate line-position mechanism.

The test asks whether entry projection, local near-family activation and line-position structure can be brought into the same broad held-out regime without another repair.

If A1 fails, the next action is not automatic A2 repair. The failure should be frozen and compared against N0/B0 meaningful structured-text competitors on a common scorecard before further generator elaboration.

## Strategic research direction

The next stage should discriminate model families rather than accumulate local anomalies:

- **N** — meaningful structured natural/technical text;
- **C** — meaningful structured text plus bounded cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms only after simpler families have fixed failure patterns.

Exposed Voynich features can be used for training/diagnosis, but model-family promotion should depend on jointly fitting them at explicit complexity cost and then predicting at least one prospectively frozen dimension not used to construct the model.

A separate sparse content track remains open, but semantic promotion requires independently grounded localization/content labels rather than post-hoc matching.

## Important corrections retained

- Phase3 plant-label result: 2 total 4-gram hits; exact permutation p=.725; binary pair-hit p=.667. NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55; universal paragraph-reset claim withdrawn.
- Phase56 unmatched full-page PC1 was contaminated by token count (r≈-.886); matched-token results supersede it.
- Phase60D recovery-vector prediction is not evidence for initialization after Phase60D2/60E removed mathematical coupling and tested future absolute state.
- Phase61A narrow success does not imply a successful whole-manuscript generator; Phase61B explicitly rejects A0 as a joint model.

## Methodological rules

- Observation -> Structure -> Mechanism -> Content relation -> Decipherment.
- Preserve relevant known structure in nulls.
- Keep exploratory/model-selection/held-out/prospective/external-replication labels distinct.
- Audit page-side vs physical leaf explicitly.
- Equalize or model estimator sample-size effects.
- Search freedom belongs inside null/model-selection folds.
- Negative results and corrections remain recorded.
- Do not preserve a narrative after its hard prediction fails; narrow it explicitly.
- Do not rescue a failed architecture by silently adding mechanisms; name and charge each extension.
- Decipherment requires executable mapping, substantial unseen prediction, fixed interpretable output, strong competitors/nulls, and prospective/external replication.
