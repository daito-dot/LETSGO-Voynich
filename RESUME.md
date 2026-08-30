# RESUME — how to restart this research

This file is the entry point for a new researcher or AI/chat session continuing the project.

## Read in this order

1. `README.md`
2. `ROADMAP.md`
3. `RESEARCH_PROTOCOL.md`
4. `research/STATUS.md`
5. `research/hypothesis-ledger.md`
6. `research/NARRATIVE_HYPOTHESIS_PHASE60.md` — frozen pre-test narrative; do not treat failed predictions as current truth
7. `research/NARRATIVE_REVISION_PHASE60.md` — post-60D2 revision
8. `experiments/phase59/` results for the medieval-entry decomposition
9. `experiments/phase60/` plans/results, especially 60A, 60B, 60C, 60D2 and 60E
10. `experiments/phase61/PLAN.md`, `phase61a_results.json`, `phase61b_results.json`, and `PLAN_C.md`
11. exact phase scripts/results before changing numerical interpretation

Do not reconstruct the project from chat history if the repository contains a newer state.

## Authority hierarchy

1. phase-specific result/report controls exact method/sample/statistic/numerical result;
2. `research/STATUS.md` controls current accepted interpretation;
3. `research/hypothesis-ledger.md` controls hypothesis history/status;
4. `ROADMAP.md` controls progress visibility, active gate and planned sequencing, but not exact scientific claims;
5. frozen narrative files record what was predicted before testing and must not be rewritten to hide failures;
6. checkpoint/handoff files are secondary summaries;
7. old chat/memory is non-authoritative when repository evidence conflicts.

## Current accepted state

The project has moved beyond direct pattern hunting into mechanism discrimination.

Accepted structural model:

`broad document constraints`

`+ page-local token-family activation`

`+ manuscript-wide short-lived paragraph-entry register`

`+ line-position grammar`

`+ token morphology / edge-pattern / k/t-family structure`

Phase57 promoted only a robust leading ~2D residual. Phase58 found no independently grounded page-level visual relation in the tested Biological and Herbal-A domains, and defensible paragraph-to-object localization remained unavailable.

Phase59 compared the paragraph-entry transition with source-native medieval Latin item/section entries. A generic medieval entry/register component explains a substantial part of the transition, while a Voynich-specific remainder survives and transfers across major sections.

## Phase 60 narrative test — current decisions

The pre-test narrative is preserved in `research/NARRATIVE_HYPOTHESIS_PHASE60.md`.

### P60-1 — genuine boundary specificity
SUPPORTED by Phase60A. Real paragraph boundaries exceed internal pseudo-boundaries under physical-leaf cross-fitting.

### P60-2 — stable structural carriers
SUPPORTED by Phase60B. k/t-family behavior, near-family/edit1 activation, local continuity, length/TTR and edge statistics carry the transition across reasonable EVA representations.

### P60-3 — transferable entry formal role
SUPPORTED by Phase60C. Entry/body structure learned outside a section transfers to held-out H/B/P/S/T and adds information beyond simple nuisance baselines.

### P60-4 — entry persistently initializes later body state
NOT SUPPORTED after Phase60D2 and Phase60E.

The initial Phase60D recovery-vector result was mathematically coupled because the target contained line0. Coupling-free prospective tests show no reliable useful line0 contribution to later absolute states once metadata/immediate prior state are known.

### P60-5 — stationary/weak-context generator without explicit entry mechanism
SUPPORTED AS A CONSTRAINT. The frozen Phase50 DSL fails to align with the Voynich entry-specific direction despite producing multivariate fluctuations of comparable raw magnitude. Explicit boundary-conditioned machinery is therefore required for that generator family.

### P60-6 — simple global cipher as discriminator from entry structure alone
NOT DISCRIMINATIVE. A boundary-blind simple cipher can inherit entry/register structure already present in meaningful structured plaintext. Ciphering becomes explanatory only if it also predicts Voynich-specific morphology/local-family/line-position structure beyond the plaintext.

## Current narrative after falsification

The strongest justified statement is:

> Voynich paragraph starts instantiate a manuscript-wide, transferable formal entry register. It is partly comparable to medieval structured-document entry grammar and partly Voynich-specific, but its detectable structural influence is short-lived rather than a persistent paragraph initializer.

This does not distinguish meaningful text, cipher/shorthand, hierarchical meaningless formal generation, or mixed mechanisms.

## Phase 61 — architecture discrimination

Phase61 compares mechanism families on joint constraints rather than one exposed statistic.

### Phase61A

A0 — a boundary-aware nonsemantic generator with a single short-lived entry mixture — **survived the narrow entry-direction gate**. This shows that the entry signature alone does not reject hierarchical meaningless generation once paragraph-boundary awareness is granted.

### Phase61B

The same frozen A0 **failed the joint scorecard**. It inherited global edit1 density from the empirical Voynich vocabulary but produced far too little local-prev10 near-family activation and overstated line-position and entry/pseudo effects. A0 is rejected as a sufficient joint model.

### Current frontier — Phase61C

`experiments/phase61/PLAN_C.md` is frozen before execution.

A1 adds exactly one repair to A0:

- local-family body activation: after line0, generation may reuse/mutate a recent token by one edit with a bounded probability.

No persistent paragraph latent state, section-specific grammar, or additional line-position rule is allowed.

**Immediate action when asked to continue:** execute Phase61C exactly as frozen.

If A1 fails, do not immediately invent A2. Freeze the failure and move first to fair comparison with N0/B0 meaningful structured-text competitors, as defined in `ROADMAP.md`.

## Research strategy after Phase61C

The main objective is a model-family tournament rather than endless local feature repair:

- **N** — meaningful structured natural/technical text;
- **C** — meaningful structured text plus bounded global cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms, introduced only after simpler families have fixed failure patterns.

Models should be compared on shared joint targets, explicit complexity cost, and prospectively frozen holdout dimensions not used to design the architecture.

Independent content tests remain a separate sparse track and require externally fixed content/localization rather than post-hoc word guessing.

## Important corrections retained

- Phase3 plant-label headline corrected: NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55.
- Phase56 unmatched full-page PC1 sample-size contamination withdrawn.
- Phase60D recovery-vector prediction is mathematically coupled and superseded for initialization claims by Phase60D2/60E.
- Passing one exposed structural statistic is not model-family validation; Phase61A -> 61B is the current explicit example.

## Frozen methodological constraints

- Observation -> Structure -> Mechanism -> Content relation -> Decipherment.
- Equalize or explicitly model sample-size effects.
- Page-side and physical leaf are distinct units.
- Search freedom belongs in null/model-selection folds.
- Local state is a default confound.
- Structural equivalence is not semantic/cipher equivalence.
- Deliberate deception is allowed only as a bounded, complexity-charged mechanism.
- Negative results and audit corrections remain public.
- Failed hard predictions narrow the narrative; they are not repaired with free exceptions.
- Exposed targets may train or diagnose models; genuinely new holdouts should be frozen before evaluation.

## Before declaring decipherment

Require an executable mapping/generation rule, substantial prediction of unseen material, fixed interpretable output, strong structure-preserving nulls/competitors, prospective or external replication, and explicit accounting of failures/exceptions.

## Session behavior

When asked simply to "continue", execute the current yellow gate in `ROADMAP.md` rather than only describing the next step or inventing a new local analysis. Update durable repository records when accepted interpretation or the active milestone changes. Stop only at a genuine decision point, external blocker, or result requiring materially different research branches.
