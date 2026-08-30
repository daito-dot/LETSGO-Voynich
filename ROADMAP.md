# LETSGO-Voynich research roadmap

Last updated: 2026-08-30

This file tracks progress and decision points. Exact numerical authority remains with phase-specific plans/results; `research/STATUS.md` controls accepted interpretation; `research/hypothesis-ledger.md` controls hypothesis history.

## Progress legend

- ✅ complete / accepted as current evidence
- ❌ falsified / rejected in tested form
- 🟡 current executable frontier
- ⏭ planned after current gate
- ⛔ blocked pending external prerequisite
- 🔒 frozen / sealed until a later gate
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
| Phase 59 | ✅ | broad entry transition partly overlaps medieval structured-document entry grammar, with Voynich-specific remainder |
| Phase 60 | ✅ | paragraph entry genuine, manuscript-wide and short-lived; persistent line0 initialization rejected |
| Phase 61A | ✅ narrow | boundary-aware A0 reproduces scalar entry direction |
| Phase 61B | ❌ A0 | A0 fails joint locality / line-position / entry scorecard |
| Phase 61C | ✅ A1 survives | one bounded local-family mechanism brings exposed Phase61 targets into broad held-out regime |
| Phase 62A | ✅ design/source freeze | objective N0 panel, common scorecard, C0 family, complexity ledger and H62-P1 frozen before scoring |
| Phase 62B | ❌ N0 joint gate | source-native structured Latin matches S3 but is opposite on S1 and reaches only ~13% of Voynich S2 locality excess |
| Phase 62C | 🟡 current | evaluate the five frozen C0 transforms and re-score frozen A1 on the same Phase62 S1–S3 scorecard |
| Phase 62D | ⏭ | freeze exposed-score N/C/G structural ranking or unresolved set |
| Phase 62P/63 | 🔒 prospective | reveal H62-P1 only after Phase62D is committed |

## Completed Phase61 gate

Frozen A1 held-out generated/Voynich ratios on the Phase61 scorecard:

- entry projection: **0.797**
- local-prev10: **0.717**
- line-position eta2 mean: **1.116**

A1 is frozen. No A2 before the fair N/C/G comparison is completed.

## Completed Phase62A source/design freeze

Pinned sources:

- CREMMA: `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`
- ZL3b mirror: `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

Historical Phase59 item membership was not fully recoverable for H318/CLM/BIS and was not reconstructed by fitting old Voynich results.

Voynich-blind corpus-wide primary N0 panel:

- BIS193
- CLM13027
- Mazarine915
- UBL758

Manuscripts receive equal primary weight. H318 is a predeclared small sensitivity; Arras861 has no eligible literal-pilcrow entries.

Frozen common scorecard:

- **S1** — fixed-five-token generic 8D entry-minus-pseudo projection;
- **S2** — full-line previous-10 near-family excess above document-vocabulary/line-layout preserving null;
- **S3** — fixed-five-token generic 8D line-position eta2 mean.

Frozen C0 transforms:

1. identity / monoalphabetic-equivalent;
2. token reversal;
3. 2-class positional allography;
4. 3-class positional allography;
5. non-overlapping digraph coding.

Frozen prospective holdout:

**H62-P1** near-family recurrence-distance profile over 1–2, 3–5, 6–10, 11–20, 21–40 token bins. Do not compute/reveal the Voynich profile before Phase62D is committed.

## Completed Phase62B — N0 baseline

Primary result:

| target | Voynich | N0 | N0/Voynich | result |
|---|---:|---:|---:|---|
| S1 entry projection | 0.87599 | -0.85872 | -0.980 | ❌ |
| S2 locality excess | 0.04388 | 0.00585 | 0.133 | ❌ |
| S3 line-position eta2 | 0.02827 | 0.02797 | 0.989 | ✅ |

Key consequences:

1. **Generic line-position grammar is not very discriminative by itself.** N0 essentially reproduces S3.
2. **The objective source-native medieval panel does not reproduce the common Voynich entry specialization.** S1 is negative in all four manuscripts and every outer fold.
3. **Voynich local near-family activation remains much stronger.** N0 reaches only ~13.3% of the S2 excess; leave-one-manuscript-out ratios remain ~0.116–0.160.
4. H318's tiny predeclared sensitivity can align strongly on S1 while failing S2 and grossly overshooting S3, demonstrating why favorable small semantic subsets are not promoted post hoc.

See `experiments/phase62/REPORT_B.md` and `phase62b_n0_results.json`.

## 🟡 Current gate — Phase62C C0 + frozen A1

Question:

> Can a low-complexity, reversible, boundary-blind recoding of meaningful structured text repair N0's S1/S2 failures, and how does that compare with frozen A1 when all are evaluated on the same Phase62 scorecard?

Execution rules already frozen in `experiments/phase62/PLAN.md`:

### C0

- evaluate only C0-0…C0-4;
- transform selection uses Voynich **training folds only**;
- no transform sees entry/paragraph position, line number, section or held-out target;
- no continuous transform parameter or Voynich-derived symbol/codebook;
- any more expressive transform becomes C1 later, never a hidden Phase62C repair.

### A1

- regenerate/re-score the exact frozen Phase61C architecture;
- use its already selected per-fold entry strength/local-family p;
- no retuning under the new common scorecard;
- retain explicit target-dependence cost from the supplied 8,295-type Voynich vocabulary.

### Firewall

- do not compute/reveal H62-P1;
- do not build A2, C1 or M0;
- after C0/A1 results, proceed to Phase62D and commit the exposed-score structural ranking/unresolved set first.

## Main track A — model-family tournament

### N0

Status: ❌ not jointly competitive on exposed S1–S3.

Important surviving contribution: natural structured documents explain much of generic line-position S3, so S3 alone is downgraded as evidence.

### C0

Status: 🟡 execute now.

Five fixed reversible boundary-blind transforms only.

### G/A1

Status: 🟡 common-score evaluation now; architecture itself remains ✅ frozen.

Complexity/dependence already paid:

- explicit paragraph-entry mechanism;
- local-family mechanism with memory 10;
- selected Phase61C parameters;
- empirical Voynich token vocabulary supplied.

### M0

Status: ⏭ deferred until N0/C0/A1 have fixed common-score profiles.

## Main track B — prospective holdout

H62-P1 is frozen and sealed. It directly tests the **shape** of near-family recurrence versus token distance, including the 10-token cutoff implied by A1.

Status: 🔒 reveal only after Phase62D.

A failed H62-P1 cannot be silently replaced with another favorable holdout.

## Main track C — external controls

Phase62A moved from small partly unrecoverable Phase59 semantic subsets to an objective corpus-wide source rule. Broader independent corpora remain desirable after the frozen tournament; they must not be used to change the Phase62 panel after seeing results.

## Main track D — content anchors

Page-level visual tests remain negative. Strong localized semantic testing remains ⛔ until an external mapping can be fixed without target-string inspection.

## Main track E — transcription robustness

Current primary transcription remains ZL3b/EVA. Independent transcription-lineage replication remains required for mature claims after the mechanism tournament.

## Main track F — complexity accounting

Use the frozen dependence vector / Pareto interpretation. Do not retroactively ignore A1's target-vocabulary dependence if its common-score fit is strong.

## Decision milestones

### M1 — Phase61 architecture gate

✅ A0 failed; A1 survived and is frozen.

### M2 — first fair N/C/G tournament

🟡 N0 complete; C0 and frozen-A1 common-score evaluation is current.

### M3 — prospective discriminator

🔒 H62-P1 already frozen; reveal only after Phase62D.

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

Execute Phase62C exactly as frozen. Do not reveal H62-P1 or introduce A2/C1/M0 before Phase62D.