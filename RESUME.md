# RESUME — how to restart this research

This file is the deterministic entry point for a new researcher or AI/chat session.

## Read in this order

1. `README.md`
2. `ROADMAP.md`
3. `RESEARCH_PROTOCOL.md`
4. `research/STATUS.md`
5. `research/hypothesis-ledger.md`
6. `experiments/phase59/` — medieval-entry development comparison
7. `experiments/phase60/` — especially 60A/60B/60C/60D2/60E
8. `experiments/phase61/PLAN_C.md`, `IMPLEMENTATION_C.md`, `REPORT_C.md`, `phase61c_results.json`
9. `experiments/phase62/CONTROL_RECOVERY.md`
10. `experiments/phase62/PLAN.md`
11. `experiments/phase62/IMPLEMENTATION_B.md`
12. `experiments/phase62/REPORT_B.md` and `phase62b_n0_results.json`
13. exact scripts/results before changing numerical interpretation

Do not reconstruct the project from chat history when the repository contains a newer state.

## Authority hierarchy

1. phase-specific frozen plan/result/report controls exact method and numerical result;
2. `research/STATUS.md` controls current accepted scientific interpretation;
3. `research/hypothesis-ledger.md` controls hypothesis history/status;
4. `ROADMAP.md` controls active gate and sequencing;
5. frozen narrative/design files record pre-test decisions and are not rewritten to hide failures;
6. old chat/memory is non-authoritative when repository evidence conflicts.

## Current accepted structural state

Voynichese currently requires explanation of at least:

`broad document constraints`

`+ page-local token-family activation`

`+ manuscript-wide short-lived paragraph-entry register`

`+ line-position grammar`

`+ token morphology / edge-pattern / {k,t}-related structure`

Phase59 showed that broad medieval entry grammar overlaps part of the Voynich transition while a Voynich-specific remainder survives.

Phase60 established that the entry role is genuine and transferable but short-lived rather than a persistent paragraph initializer.

Current page-level visual/content tests remain negative; strong localized semantic testing is blocked pending defensible external paragraph/object mapping.

## Phase61 decisions

### A0

- 61A: boundary-aware entry mixture survives a narrow scalar entry gate.
- 61B: A0 fails jointly because locality is far too weak and positional/entry effects are mis-scaled.

### A1

61C adds exactly one bounded local-family mechanism to A0 and no persistent paragraph state/section grammar/additional line rule.

Held-out A1/Voynich Phase61 ratios:

- entry: **0.797**
- local-prev10: **0.717**
- line-position eta2: **1.116**

A1 survives that exposed structural gate but uses the empirical Voynich token inventory and is now frozen.

Do not create A2 before the current tournament and prospective test are resolved.

## Phase62A — source/design freeze: COMPLETE

Pinned Voynich:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`

Pinned medieval controls:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`

Historical Phase59 H318/CLM/BIS subsets were not fully recoverable and were not rebuilt by fitting old Voynich results.

Primary objective N0 panel:

- BIS193
- CLM13027
- Mazarine915
- UBL758

Equal-weight manuscripts. H318 is sensitivity only.

Frozen common scorecard:

- **S1** — generic 8D fixed-five-token entry-minus-pseudo projection;
- **S2** — full-line previous-10 near-family excess above a vocabulary/line-layout preserving null;
- **S3** — generic fixed-five-token line-position eta2 mean.

Frozen C0 family:

1. identity / monoalphabetic-equivalent;
2. token reversal;
3. 2-class positional allography;
4. 3-class positional allography;
5. non-overlapping digraph coding.

Frozen prospective H62-P1 is a five-bin near-family recurrence-distance profile. **Do not compute/reveal Voynich H62-P1 until after Phase62D is committed.**

## Phase62B — N0 baseline: COMPLETE / FAILS JOINT GATE

Source-native meaningful structured medieval text was evaluated before C0/A1 common-score results.

Across-fold means:

| target | Voynich | N0 | ratio |
|---|---:|---:|---:|
| S1 | 0.87599 | -0.85872 | -0.980 |
| S2 | 0.04388 | 0.00585 | 0.133 |
| S3 | 0.02827 | 0.02797 | 0.989 |

Interpretation:

- **S1 fails:** every primary manuscript is negative on the Voynich-training-derived common entry direction; every leave-one-manuscript-out aggregate remains negative.
- **S2 fails:** ordinary structured Latin reaches only ~13.3% of the Voynich locality excess; LOMO remains ~11.6–16.0%.
- **S3 passes:** generic line-position grammar is readily reproduced and is weak evidence when cited alone.

H318's tiny predeclared sensitivity aligns positively on S1 but fails/overshoots the other dimensions and remains outside the primary result.

Exact result/report:

- `experiments/phase62/phase62b_n0_results.json`
- `experiments/phase62/REPORT_B.md`

Do not interpret N0 failure as proof of G/A1. The common-score C0/A1 comparison has not yet been run.

## Current frontier — Phase62C

When asked to continue, execute the already-frozen Phase62C comparison.

### C0

- evaluate only C0-0…C0-4 from `experiments/phase62/PLAN.md`;
- select transform on Voynich training folds only using frozen S1–S3 error;
- evaluate selected transform on held-out Voynich folds;
- no boundary-aware transform, target codebook, continuous tuning or post-result repair;
- if more expressive ciphering is later justified, name it C1 after Phase62C is frozen.

### Frozen A1

- regenerate/re-score the Phase61C model under the common Phase62 S1–S3 scorecard;
- use its already selected fold-specific entry strength/local-family p;
- do not retune A1;
- retain explicit complexity/target-vocabulary cost.

### Firewall

- do not compute/reveal H62-P1;
- do not create A2, C1 or M0 inside Phase62C;
- after Phase62C, Phase62D must commit the exposed-score structural ranking/unresolved set before H62-P1 reveal.

## Research families

- **N** — meaningful structured natural/technical text;
- **C** — meaningful structured text + bounded cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms only after simpler families have fixed failure patterns.

## Important corrections retained

- Phase3 plant-label semantic headline: NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55.
- Phase56 unmatched full-page PC1 sample-size contamination withdrawn.
- Phase60D persistent-initialization evidence was mathematically coupled and rejected by 60D2/60E.
- Phase61A narrow success did not validate A0; Phase61B rejected it jointly.
- Phase61C survival is structural only and carries target-vocabulary dependence.
- Phase59 small semantic subsets remain historical development evidence; Phase62 uses an independently reproducible objective source panel.

## Frozen methodological constraints

- Observation → Structure → Mechanism → Content relation → Decipherment.
- Preserve relevant known structure in nulls.
- Page-side and physical leaf are distinct units.
- Search freedom belongs in model-selection/null folds.
- Local state is a default confound.
- Structural equivalence is not semantic/cipher equivalence.
- Deliberate deception is allowed only as a bounded, complexity-charged mechanism.
- Negative results and audit corrections remain public.
- Failed hard predictions narrow the narrative; no free repair.
- Exposed targets may train/diagnose models; sealed prospective targets remain untouched until their preregistered reveal gate.

## Before declaring decipherment

Require an executable fixed mapping/generation rule, substantial prediction of unseen material, fixed interpretable output, strong competitors/nulls, prospective/external replication, and explicit accounting of failures/exceptions.

## Session behavior

When asked simply to "continue", execute Phase62C exactly as frozen. Do not skip ahead to H62-P1 or create A2/C1/M0 before Phase62D.