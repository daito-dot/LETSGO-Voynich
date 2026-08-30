# RESUME — how to restart this research

This file is the deterministic entry point for a new researcher or AI/chat session.

## Read in this order

1. `README.md`
2. `ROADMAP.md`
3. `RESEARCH_PROTOCOL.md`
4. `research/STATUS.md`
5. `research/hypothesis-ledger.md`
6. `research/NARRATIVE_HYPOTHESIS_PHASE60.md`
7. `research/NARRATIVE_REVISION_PHASE60.md`
8. `experiments/phase59/` — medieval-entry development comparison
9. `experiments/phase60/` — especially 60A/60B/60C/60D2/60E
10. `experiments/phase61/PLAN_C.md`, `IMPLEMENTATION_C.md`, `REPORT_C.md`, `phase61c_results.json`
11. `experiments/phase62/CONTROL_RECOVERY.md`
12. `experiments/phase62/PLAN.md`
13. exact scripts/results before changing numerical interpretation

Do not reconstruct the project from chat history when the repository contains a newer state.

## Authority hierarchy

1. phase-specific frozen plan/result/report controls exact method and numerical result;
2. `research/STATUS.md` controls current accepted scientific interpretation;
3. `research/hypothesis-ledger.md` controls hypothesis history/status;
4. `ROADMAP.md` controls active gate and sequencing, not scientific numbers;
5. frozen narrative/design files record pre-test decisions and are not rewritten to hide failures;
6. checkpoint/handoff files are secondary summaries;
7. old chat/memory is non-authoritative when repository evidence conflicts.

## Current accepted structural state

Voynichese currently requires explanation of at least:

`broad document constraints`

`+ page-local token-family activation`

`+ manuscript-wide short-lived paragraph-entry register`

`+ line-position grammar`

`+ token morphology / edge-pattern / {k,t}-related structure`

Phase59 supports a decomposition of paragraph entry into a substantial generic medieval entry/register component plus a transferable Voynich-specific remainder.

Phase60 established that the entry role is genuine and transferable but does **not** behave like a persistent line0 initializer of later paragraph body state.

Current page-level visual/content tests remain negative; strong localized semantic testing is blocked pending defensible external paragraph/object mapping.

## Phase61 decisions

### 61A — A0 narrow entry gate

SUPPORTED NARROWLY. A boundary-aware nonsemantic paragraph-line0 mixture can reproduce the held-out scalar entry direction without persistent paragraph state.

### 61B — A0 joint model

FALSIFIED AS SUFFICIENT. A0 produces far too little local-prev10 near-family activation and strongly overstates line-position / entry-pseudo effects. High edit1 density is non-independent because the empirical Voynich vocabulary is supplied.

### 61C — A1 first joint gate

SUPPORTED AS A STRUCTURAL GENERATOR GATE.

A1 adds exactly one mechanism to A0: bounded local-family reuse / one-edit mutation from line1 onward. No persistent paragraph state, section-specific grammar or extra line-position rule was allowed.

Held-out A1/Voynich ratios across five physical-leaf folds:

- entry projection: **0.797**
- local-prev10: **0.717**
- line-position eta2 mean: **1.116**

All pass the frozen `[0.5,2.0]` broad-regime gate.

Interpretation:

> A minimally extended boundary-aware nonsemantic generator remains structurally viable once it pays for one additional local-family mechanism.

This is not evidence that the manuscript is meaningless. A1 uses the empirical Voynich token inventory and is now frozen.

## Phase62A — source/design freeze: COMPLETE

Phase62A was deliberately completed **without computing N0/C0 tournament scores**.

### External provenance

Voynich reproducibility mirror:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- `ZL3b-n.txt` expected Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`

Medieval controls:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`

### Control-recovery correction

The exact old Phase59 H318/CLM/BIS semantic item subsets are not fully reconstructable from the current repository. Do **not** recreate them by choosing entries that match old Voynich results.

A new corpus-wide rule was fixed before counts were inspected: include manuscripts with >=5 eligible literal-pilcrow entries. Primary N0 panel:

- BIS193 — 64;
- CLM13027 — 39;
- Mazarine915 — 38;
- UBL758 — 5.

Manuscript is the equal-weight replication unit.

Predeclared sensitivities:

- H318 — 4 eligible, Phase52-preexisting medical/recipe control;
- Arras861 — no literal-pilcrow entry, non-entry sensitivity only.

See `experiments/phase62/CONTROL_RECOVERY.md`.

### Frozen common scorecard

Primary:

- **S1** — generic 8D fixed-five-token entry-minus-pseudo projection;
- **S2** — full-line previous-10 near-family excess over a document-vocabulary/line-layout preserving redistribution null;
- **S3** — generic fixed-five-token line-position eta2 mean.

Voynich-specific literal `{k,t}` dimensions are excluded from the primary cross-language tournament.

### Frozen C0 family

Exactly five boundary-blind reversible transforms:

1. identity/monoalphabetic-equivalent;
2. token reversal;
3. two-class positional allography;
4. three-class positional allography;
5. non-overlapping digraph coding.

No C0 transform can inspect entry position, line, section or held-out Voynich target.

### Frozen prospective holdout H62-P1

A five-bin near-family recurrence distance profile is preregistered over distances:

- 1–2;
- 3–5;
- 6–10;
- 11–20;
- 21–40 tokens.

This is mechanistically relevant because A1 has an explicit maximum local-family memory of 10 tokens.

**Do not compute/reveal the Voynich H62-P1 profile until Phase62D's exposed-score structural ranking/unresolved set is committed.**

Exact definitions are in `experiments/phase62/PLAN.md`.

## Current frontier — Phase62B N0 baseline

When asked to continue, execute **N0 only** under the frozen plan.

1. reproduce the pinned Voynich and CREMMA inputs;
2. implement the common S1–S3 extractor exactly as frozen;
3. run the four primary manuscripts with all eligible entries;
4. equal-weight manuscripts;
5. report per-manuscript and leave-one-manuscript-out heterogeneity;
6. record the N0 result durably;
7. do not change C0, A1, source membership, or H62-P1 after seeing N0;
8. stop at the Phase62B decision record, then proceed to already-frozen Phase62C.

## Research families

- **N** — meaningful structured natural/technical text;
- **C** — meaningful structured text + bounded cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms only after simpler families have fixed failure patterns.

The project now compares predictive efficiency and target dependence, not how many observed peculiarities a story can explain after the fact.

## Important corrections retained

- Phase3 plant-label semantic headline: NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55.
- Phase56 unmatched full-page PC1 sample-size contamination withdrawn.
- Phase60D recovery-vector result mathematically coupled; persistent-initialization claim rejected by 60D2/60E.
- Phase61A narrow success did not validate A0; Phase61B rejected A0 jointly.
- Phase61C survival is structural only and carries target-vocabulary dependence.
- Phase59 small semantic control subsets remain historical development evidence, not the prospective Phase62 source panel.

## Frozen methodological constraints

- Observation → Structure → Mechanism → Content relation → Decipherment.
- Equalize/model sample-size effects.
- Page-side and physical leaf are distinct units.
- Search freedom belongs in model-selection/null folds.
- Local state is a default confound.
- Structural equivalence is not semantic/cipher equivalence.
- Deliberate deception is allowed only as a bounded, complexity-charged mechanism.
- Negative results and audit corrections remain public.
- Failed hard predictions narrow the narrative; no free repair.
- Exposed targets may train/diagnose models; preregistered holdouts remain sealed until their reveal gate.

## Before declaring decipherment

Require an executable fixed mapping/generation rule, substantial prediction of unseen material, fixed interpretable output, strong competitors/nulls, prospective/external replication, and explicit accounting of failures/exceptions.

## Session behavior

When asked simply to "continue", execute the current yellow gate in `ROADMAP.md`. Update durable records at genuine decision points. Do not skip ahead to H62-P1 or create A2/C1 before their frozen gate.
