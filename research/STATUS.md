# Current research status

For progress sequencing and the active decision gate, see `../ROADMAP.md`. Phase-specific plans/results control exact methods and numbers; this file controls the current accepted interpretation after later evidence.

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and a manuscript-wide paragraph-entry formal role. What is not established is whether these structures encode independently grounded semantic content, arise from cipher/shorthand mechanics, or can be reproduced by a hierarchical nonsemantic generator.

Structural equivalence is not cipher equivalence. Structural fit is not decipherment.

The current mechanism families remain open:

- **N** — meaningful structured natural/technical text;
- **C/B0** — meaningful structured text plus bounded cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms, deferred until simpler families have fixed failure patterns.

## Robust structural state through Phase 57

The audited structural hierarchy remains:

`broad document constraints`

`+ page-local token-family activation`

`+ paragraph-entry/body transition`

`+ line-position grammar`

`+ token morphology / edge-pattern / {k,t}-related dimensions`

Physical locality survives exact section+Currier+hand matching but is not one smooth drift. Matched-token variation is moderately low-dimensional. Phase57 promoted only the leading approximately two-dimensional residual subspace; higher residual axes remain representation/scale-sensitive.

## Phase 58 — content relation remains unestablished

Independently defined page-level visual properties in Biological/balneological and early Herbal-A domains did not associate significantly with the promoted 2D residual. A defensible paragraph-to-illustrated-subobject mapping was unavailable without post-hoc pairing.

Therefore current page-level visual semantic tests are negative, while strong localized semantic testing remains blocked rather than guessed.

## Phase 59 — medieval entry decomposition

Source-native medieval Latin item/section entries reproduce part of the Voynich paragraph-entry transition.

In the current development comparison, an external rank-2 medieval-entry basis learned without Voynich explains about 65% of Voynich transition energy. A Latin-orthogonal Voynich component remains and transfers positively across H/B/P/S/T.

Accepted interpretation:

`generic medieval entry/register grammar + Voynich-specific specialization`

The external control panel is still small and heterogeneous, so magnitude/dimensionality require broader manuscript and genre replication.

## Phase 60 — paragraph entry is real, transferable and short-lived

### 60A — genuine boundary specificity: SUPPORTED

Real paragraph line0→line2 transitions exceed internal pseudo-boundaries under physical-leaf cross-fitting.

### 60B — structural carriers: SUPPORTED

The transition is carried mainly by {k,t}-family behavior, near-family/edit1 activation, local previous-10 continuity, length/TTR and stable edge behavior across reasonable EVA representations.

### 60C — held-out-section transfer: SUPPORTED

A section-blind structural entry/body role transfers across held-out H/B/P/S/T and adds information beyond simple nuisance baselines.

### 60D/60D2/60E — persistent initialization: NOT SUPPORTED

The original recovery-vector result was mathematically coupled. Coupling-free prospective tests do not show useful line0 information for later absolute states once immediate prior state/metadata are known.

Retain:

> Voynich paragraph starts instantiate a manuscript-wide, transferable formal entry register. It is partly comparable to medieval structured-document entry grammar and partly Voynich-specific, but its detectable influence is short-lived rather than a persistent paragraph initializer.

Do not claim that line0 controls the later paragraph body.

The frozen Phase50 stationary/weak-context DSL also fails the entry-specific direction, showing that this generator family needs explicit boundary-conditioned machinery.

## Phase 61 — architecture discrimination

Phase61 tests whether explicit nonsemantic machinery can jointly reproduce several exposed structural constraints rather than one entry statistic.

### 61A — A0 narrow entry gate: SURVIVES

A0 adds one explicit short-lived paragraph-line0 entry mixture and no persistent paragraph state. Under physical-leaf cross-fitting it can reproduce/exceed the scalar held-out entry-direction projection.

Therefore paragraph-entry structure alone does not reject hierarchical nonsemantic generation once boundary awareness is granted.

### 61B — A0 joint scorecard: FAILS

A0 is not a sufficient joint model:

- edit1 type density is close only because it samples from the empirical Voynich vocabulary and is therefore non-independent;
- local-prev10 near-family activation is only about 6.7% of the Voynich level;
- mean line-position eta2 is about 3.3× the Voynich proxy;
- the multivariate entry/pseudo norm is about 2.8× the Voynich value at the fixed diagnostic strength.

### 61C — A1 first joint gate: SURVIVES

A1 was frozen before execution in `experiments/phase61/PLAN_C.md` and `IMPLEMENTATION_C.md`. Relative to A0 it adds exactly one mechanism: bounded local-family reuse/one-edit mutation from line1 onward. It adds no persistent paragraph state, section-specific grammar, or separate line-position rule.

The exact ZL3b input was verified by Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.

Before fresh evaluation, the reconstructed executable passed a Phase61B compatibility audit. The entry/pseudo norm reproduced essentially exactly: recorded 1.28505 versus recomputed 1.285053.

Five outer physical-leaf folds selected only the frozen parameter grid. Selected pairs were:

- folds 0, 1, 4: entry strength 0.5; local-family p=0.20;
- folds 2, 3: entry strength 0.5; local-family p=0.30.

Across-fold held-out means:

| target | Voynich | A1 | A1/Voynich |
|---|---:|---:|---:|
| entry projection | 1.18798 | 0.94667 | **0.797** |
| local-prev10 fraction | 0.09386 | 0.06729 | **0.717** |
| line-position eta2 mean | 0.04096 | 0.04572 | **1.116** |

The frozen broad-regime rule required all three ratios in `[0.5, 2.0]`; all three pass.

Accepted interpretation:

> A minimally extended boundary-aware nonsemantic generator can jointly reproduce the entry, local-family and line-position targets at broad-regime resolution once it pays for one additional local-family mechanism.

This is **not evidence that Voynich is meaningless**. A1 still uses the empirical Voynich token-type inventory, so high edit1 type density is not an independent prediction, and historical plausibility has not been established. The result only keeps G/A1 alive as a structural mechanism family.

Exact result: `experiments/phase61/phase61c_results.json`.

## Current frontier — first fair N/C/G tournament

A1 is now frozen. Do **not** create A2 merely to improve exposed statistics.

The immediate next problem is to compare A1 against meaningful structured-text competitors on the same scorecard:

1. **N0** — source-native structured medieval plaintext;
2. **B0/C0** — the same kind of plaintext under bounded, global, boundary-blind encoding;
3. **A1/G** — the frozen Phase61C generator.

Requirements:

- recover exact Phase59 external sources/provenance rather than reconstructing them approximately;
- use common metrics and physical/document holdouts where applicable;
- report complexity cost explicitly;
- do not give any family a statistic selected uniquely in its favor;
- freeze at least one genuinely new prospective holdout before claiming a model-family winner.

## Important corrections retained

- Phase3 plant-label result: NOT SUPPORTED after corrected permutation test.
- Phase53/54 recto/verso collapse corrected in Phase55; universal paragraph-reset claim withdrawn.
- Phase56 unmatched full-page PC1 was contaminated by token count; matched-token results supersede it.
- Phase60D recovery-vector prediction is not evidence for persistent initialization after coupling-free 60D2/60E.
- Phase61A narrow success did not imply a whole-manuscript generator; Phase61B rejected A0 jointly.
- Phase61C survival is structural only and does not independently predict edit1 density because the empirical Voynich vocabulary is supplied.

## Methodological rules

- Observation → Structure → Mechanism → Content relation → Decipherment.
- Preserve relevant known structure in nulls.
- Distinguish exploratory, model-selection, held-out, prospective and external-replication evidence.
- Page-side and physical leaf are distinct units.
- Search freedom belongs inside model-selection/null folds.
- Local state is a default confound.
- Negative results and audit corrections remain public.
- Do not rescue failed architectures silently; name and charge each extension.
- Exposed targets may train/diagnose models; genuinely new holdouts must be frozen before evaluation.
- Decipherment requires an executable fixed mapping/generation rule, substantial unseen prediction, interpretable fixed output, strong competitors/nulls, prospective/external replication and explicit accounting of failures/exceptions.
