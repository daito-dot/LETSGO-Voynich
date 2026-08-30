# LETSGO-Voynich research roadmap

Last updated: 2026-08-30

This file tracks progress and decision points. Exact numerical authority remains with phase-specific plans/results; `research/STATUS.md` controls accepted interpretation; `research/hypothesis-ledger.md` controls hypothesis history.

## Progress legend

- ✅ complete / accepted as current evidence
- ❌ falsified / rejected in tested form
- 🟡 current executable frontier
- ⏭ planned after current gate
- ⛔ blocked pending external prerequisite
- 🔁 recurring robustness / replication track

## North star

Discriminate among competing mechanism families by common held-out scorecards, prospective prediction, explicit complexity/dependence cost, and independent controls. Do not optimize for the number of unusual Voynich statistics explained post hoc.

Families kept open:

- **N** — meaningful structured natural/technical text;
- **C** — meaningful text plus bounded cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms only after simpler families have fixed failure patterns.

Structural fit alone is not decipherment.

## Current position

| Stage | Status | Main consequence |
|---|---|---|
| Phases 1–43 | ✅ | direct semantic cribs and weak periodic interpretations repeatedly failed; structural invariants accumulated |
| Phases 44–52 | ✅ | mechanism tests and document/genre confounding became explicit |
| Phases 53–57 | ✅ | structural audit corrected page/leaf/sample-size issues and narrowed a robust residual opportunity |
| Phase 58 | ✅ negative / ⛔ localized content | tested page-level visual relations negative; defensible paragraph/object mapping unavailable |
| Phase 59 | ✅ | entry transition decomposes into generic-medieval component + transferable Voynich-specific remainder |
| Phase 60 | ✅ | paragraph entry genuine, manuscript-wide and short-lived; persistent line0 initialization rejected |
| Phase 61A | ✅ narrow | boundary-aware A0 reproduces scalar entry direction |
| Phase 61B | ❌ A0 | A0 fails joint locality / line-position / entry scorecard |
| Phase 61C | ✅ A1 survives | one bounded local-family mechanism brings exposed joint targets into broad held-out regime |
| Phase 62A | ✅ design/source freeze | external controls recovered/audited; objective N0 panel, common scorecard, C0 family, complexity ledger and prospective H62-P1 frozen before scoring |
| Phase 62B | 🟡 current | execute N0 structured-medieval baseline only; record manuscript heterogeneity without changing C0/A1 |
| Phase 62C | ⏭ | evaluate fixed C0 transform family and re-score frozen A1 under common scorecard |
| Phase 62D | ⏭ | freeze exposed-score N/C/G structural ranking or unresolved set |
| Phase 62P/63 | 🔒 prospective | reveal preregistered near-family distance profile only after Phase62D is committed |

## Completed Phase61 gate

Frozen A1 held-out generated/Voynich ratios of means:

- entry projection: **0.797**
- local-prev10: **0.717**
- line-position eta2 mean: **1.116**

All passed the Phase61C `[0.5,2.0]` broad-regime rule. A1 is now frozen. No A2 before fair N/C/G comparison.

## Completed Phase62A source/design freeze

### External corpus provenance

CREMMA control corpus is pinned to:

`HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`

Voynich reproducibility mirror is pinned to:

`matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`

with ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`.

### Recovery audit

Historical Phase59 item membership is not fully recoverable for H318/CLM/BIS, so no subset is reconstructed by matching old Voynich results. UBL758's old n=5 is effectively reconstructable.

A corpus-wide inclusion rule was frozen before counts were inspected: every CREMMA manuscript with >=5 eligible literal-pilcrow entries.

Primary N0 panel:

- BIS193 — 64 entries;
- CLM13027 — 39;
- Mazarine915 — 38;
- UBL758 — 5.

Manuscripts, not entries, receive equal primary weight.

Predeclared sensitivities:

- H318 — 4 eligible entries, Phase52-preexisting medical/recipe control;
- Arras861 — no literal pilcrow, non-entry document/line-position sensitivity only.

See `experiments/phase62/CONTROL_RECOVERY.md`.

### Common primary scorecard

Frozen in `experiments/phase62/PLAN.md`:

- **S1** — Voynich-training-derived entry-minus-pseudo projection on a sample-size-neutral 8D generic line representation using exactly five tokens per line;
- **S2** — full-line local previous-10 near-family excess above a document-vocabulary/line-layout preserving redistribution null;
- **S3** — mean line-position eta2 across the same generic fixed-five 8D representation.

Literal Voynich `{k,t}` features are excluded from the primary cross-language comparison.

### C0/B0 family

Exactly five predeclared reversible boundary-blind recodings:

1. identity / monoalphabetic-equivalent;
2. token reversal;
3. 2-class positional allography;
4. 3-class positional allography;
5. non-overlapping digraph coding.

Transform selection may use Voynich training folds only. No transform may inspect paragraph/entry position, section or held-out targets.

### Complexity/dependence

Interpret on a Pareto basis rather than one arbitrary penalty. In particular, A1's empirical Voynich token vocabulary (8,295 types) is supplied and therefore remains a major target-dependence cost even if structural fit is strong.

### Prospective discriminator already frozen

**H62-P1: near-family recurrence distance profile** over bins 1–2, 3–5, 6–10, 11–20, 21–40, with within-item permutation null.

The exact signed profile normalization, short-range concentration and L1 profile distance are defined in `experiments/phase62/PLAN.md`.

**Do not compute/reveal the Voynich H62-P1 profile before Phase62D ranking is committed.**

## 🟡 Current gate — Phase62B N0 baseline

Question:

> How close can source-native meaningful structured medieval text get to the common S1–S3 Voynich fingerprint before any recoding?

Execution rules:

1. use only the frozen four-manuscript primary panel;
2. use every eligible literal-pilcrow item in each manuscript;
3. equal-weight manuscripts;
4. run the frozen common scorecard against each Voynich physical-leaf fold;
5. record manuscript heterogeneity and leave-one-manuscript-out sensitivity;
6. do **not** change C0 transforms, A1, source panel or H62-P1 after seeing N0;
7. no semantic interpretation from N0 alone.

Stop after N0 result is durably recorded, then proceed to Phase62C as already specified.

## Main track A — model-family tournament

### N0

Status: 🟡 execute now.

No Voynich-tuned parameters. Meaningful source-native structured Latin is the baseline.

### C0/B0

Status: ⏭ frozen, not yet evaluated.

Boundary-blind reversible recoding only. More expressive ciphering becomes a separately named C1 after C0 result, never a hidden repair.

### G/A1

Status: ✅ frozen competitor.

Pays for:

- explicit paragraph-entry mechanism;
- local-family mechanism with memory 10;
- selected Phase61C parameters;
- empirical Voynich token vocabulary supplied.

### M0

Status: ⏭ deferred until N0/C0/A1 have fixed outcome profiles.

## Main track B — prospective holdout

H62-P1 is now frozen, not merely a candidate. It tests the **shape** of near-family recurrence versus token distance, particularly the 10-token cutoff directly implied by A1.

Status: 🔒 do not reveal Voynich result until Phase62D.

Other future holdouts remain available only after H62-P1 is resolved; do not swap a failed H62-P1 for a more favorable statistic.

## Main track C — external controls

Phase62A expanded the source audit from the old small Phase59 semantic subsets to objective corpus-wide entry availability. Future expansion beyond CREMMA should prioritize independent corpora and multiple manuscripts per genre, but must not delay the already frozen Phase62 tournament.

## Main track D — content anchors

Page-level visual tests remain negative. Strong localized semantic testing remains ⛔ until an external mapping can be fixed without looking at target strings.

## Main track E — transcription robustness

Current primary transcription remains ZL3b/EVA. Independent transcription-lineage replication remains required for mature claims after the current mechanism tournament.

## Main track F — complexity accounting

Phase62 now has a frozen qualitative/quantitative dependence vector. Later work may add predictive code length/MDL where mathematically coherent, but cannot retroactively ignore A1's supplied target vocabulary.

## Decision milestones

### M1 — Phase61 architecture gate

✅ A0 failed; A1 survived and is frozen.

### M2 — first fair N/C/G tournament

🟡 In execution. Phase62A design is complete; N0 is next.

### M3 — prospective discriminator

🔒 H62-P1 frozen now; reveal only after Phase62D.

### M4 — external robustness

⏭ broader corpora + independent Voynich transcription lineage.

### M5 — content relation

⛔ not established.

### M6 — decipherment threshold

⛔ not reached.

## Stop / pivot rules

Pause or pivot rather than endlessly repair when:

1. a candidate needs a new mechanism after every failed exposed statistic;
2. gains disappear on physical-leaf/manuscript holdout;
3. results collapse under stronger document/genre controls;
4. a claim depends on one transcription convention;
5. semantic interpretation requires post-hoc relabeling/free exceptions;
6. a simpler competing architecture obtains comparable fit with materially lower target dependence/complexity.

## What to do when asked simply to "continue"

Execute the current yellow gate in this roadmap. Record negative results as first-class outcomes and update durable state only at genuine decision points.
