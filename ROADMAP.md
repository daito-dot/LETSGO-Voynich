# LETSGO-Voynich research roadmap

Last updated: 2026-08-30

This file tracks progress and decision points. Exact numerical authority remains with phase-specific plans/results; `research/STATUS.md` controls accepted interpretation; `research/hypothesis-ledger.md` controls hypothesis history. Reproducibility caveats in `research/REPRODUCIBILITY_AUDIT.md` and `research/AUDIT_PHASE51_61C_20260830.md` remain binding.

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
| Phase 58 | ✅ negative / ⛔ localized content | page-level visual relations negative; defensible paragraph/object mapping unavailable |
| Phase 59 | ✅ | broad entry transition partly overlaps medieval structured-document entry grammar, with Voynich-specific remainder |
| Phase 60 | ✅ with audit caveats | paragraph entry genuine, manuscript-wide and short-lived; exact 60B carrier magnitudes and 60E replay retain provenance debt |
| Phase 61A | ✅ narrow | boundary-aware A0 family can reproduce scalar entry direction; not prospective validation of preselected strength |
| Phase 61B | ❌ A0 | A0 fails joint locality / line-position / entry scorecard; exact historical A0 replay remains provenance debt |
| Phase 61C | ✅ A1 survives narrow aggregate gate | one local-family mechanism brings frozen scalar targets into broad held-out regime; full line-position profile is **not** reproduced |
| Phase 62A | ✅ design/source freeze | objective N0 panel, common scorecard, C0 family, complexity ledger and H62-P1 frozen before scoring |
| Phase 62B | ❌ N0 joint gate | source-native structured Latin matches S3 but is opposite on S1 and reaches only ~13% of Voynich S2 locality excess |
| Phase 62C | ✅ | C0 digraph coding materially improves N0 but still fails S1/S2; frozen A1 passes all three exposed ratio-of-means gates |
| **Phase 62D** | **🟡 current** | freeze the exposed-score structural ranking / unresolved-set interpretation **before** H62-P1 reveal |
| Phase 62P/63 | 🔒 prospective | reveal the preregistered near-family recurrence-distance profile only after Phase62D is committed |

## Completed Phase62B — N0

Across-fold result:

| target | Voynich | N0 | N0/Voynich |
|---|---:|---:|---:|
| S1 entry projection | 0.87599 | -0.85872 | **-0.980** |
| S2 locality excess | 0.04388 | 0.00585 | **0.133** |
| S3 line-position eta2 mean | 0.02827 | 0.02797 | **0.989** |

Consequences:

- generic line-position S3 is weak discrimination by itself;
- objective source-native medieval text does not reproduce the stricter Voynich S1 specialization;
- Voynich near-family locality remains much stronger.

See `experiments/phase62/REPORT_B.md`.

## Completed Phase62C — C0 + frozen A1

### C0

All five outer folds selected **C0-4 non-overlapping digraph coding** using training targets only.

| target | C0/Voynich |
|---|---:|
| S1 | **-0.932** |
| S2 | **0.249** |
| S3 | **0.856** |

C0 reduces mean joint relative MSE from N0 `3.0388` to `2.8884`, improves held-out fit in 5/5 folds, and satisfies the frozen manuscript-omission stability rule. Therefore simple reversible boundary-blind recoding has **material but limited** explanatory value.

It does not solve the main residual problem: S1 remains opposite in sign and S2 remains only about one quarter of Voynich.

### Frozen A1

No retuning was performed. Across-fold ratio-of-means:

| target | A1/Voynich |
|---|---:|
| S1 | **0.623** |
| S2 | **1.512** |
| S3 | **0.587** |

All pass the frozen `[0.5,2.0]` common-score gate.

Interpretation constraint from the independent Phase61C audit remains binding: the S3 scalar average hides coordinate-level mismatch. A1 is therefore the strongest **exposed scalar structural fit**, not a demonstrated reproduction of the full multivariate line-position grammar.

A1 also pays materially higher target-dependence/complexity costs: explicit boundary mechanism, explicit local-family process with memory 10, Voynich-selected parameters, and supplied 8,295-type empirical Voynich vocabulary. It has no meaningful plaintext candidate.

See `experiments/phase62/REPORT_C.md` and `phase62c_c0_a1_results.json`.

## 🟡 Current gate — Phase62D ranking freeze

Phase62D computes no new Voynich statistic. Its purpose is to lock interpretation before the prospective reveal.

The decision must distinguish two questions:

1. **Exposed scalar structural fit:** which tested candidate is currently closest on frozen S1–S3?
2. **Overall mechanism-family support:** does exposed fit plus complexity/provenance justify a winner before prospective validation?

Expected admissible wording based on already-frozen results:

- N0 is not jointly competitive;
- C0 is better than N0 but insufficient on S1/S2;
- A1 is the **provisional leading exposed-score structural candidate** among N0/C0/A1;
- the overall N/C/G mechanism question remains unresolved because A1 has higher target dependence, profile mismatch, fold heterogeneity and no semantic/historical grounding, while C0 is only a bounded first cipher baseline rather than the whole C family.

Phase62D must freeze that ranking/unresolved set in the repository before any H62-P1 value is computed or revealed.

### Phase62D stop condition

Complete only when:

- the exposed-score ranking is explicit;
- complexity/target dependence is explicitly carried forward;
- Phase61C profile mismatch and Phase62C fold heterogeneity are recorded;
- no A2/C1/M0 repair is introduced;
- H62-P1 remains sealed in the Phase62D commit.

## 🔒 Next gate — H62-P1 prospective discriminator

Frozen in Phase62A before the tournament outcome:

near-family recurrence-distance bins:

- 1–2 tokens;
- 3–5;
- 6–10;
- 11–20;
- 21–40.

The metric compares observed recurrence to a layout-preserving permutation null and evaluates the normalized five-bin excess profile. It is especially discriminative for A1 because A1 contains an explicit maximum local-family memory of 10 tokens.

Rules:

1. do not compute/reveal the Voynich H62-P1 profile before Phase62D merge;
2. implement the exact frozen statistic and distance metric before seeing its result;
3. evaluate Voynich, N0, selected C0 and frozen A1 without retuning;
4. a failed H62-P1 cannot be swapped for a more favorable holdout;
5. no A2/C1/M0 repair until the prospective result is recorded.

## Main track C — external controls

After the frozen tournament/prospective gate:

- expand beyond CREMMA to independent medieval corpora;
- increase manuscripts within medical, recipe/pharmacological, herbal, astronomical/astrological, liturgical, scholastic and strongly itemized genres;
- preserve manuscript/genre holdout rather than pooling entries as independent documents.

## Main track D — content anchors

Page-level visual tests remain negative. Strong localized semantic testing remains ⛔ until an external paragraph/object mapping can be fixed without target-string inspection.

## Main track E — transcription / replay robustness

Priority debts after the prospective tournament gate:

- independent Voynich transcription-lineage replication;
- recover exact historical Phase60B eligibility if possible;
- exact clean Phase60E replay;
- historical A0 source provenance if recoverable;
- profile-aware replication of A1 rather than aggregate eta2 only.

## Main track F — complexity accounting

Use the frozen dependence vector / Pareto interpretation. Later MDL or held-out log-loss may sharpen comparison, but cannot retroactively erase target dependence.

## Decision milestones

- **M1 Phase61 architecture gate:** ✅ A0 fails jointly; A1 survives the frozen aggregate first gate.
- **M2 first fair N/C/G exposed tournament:** 🟡 results obtained; Phase62D interpretation freeze is current.
- **M3 prospective discriminator:** 🔒 H62-P1 already frozen; reveal next only after M2 interpretation freeze.
- **M4 external robustness:** ⏭ broader corpora + independent transcription.
- **M5 content relation:** ⛔ not established.
- **M6 decipherment threshold:** ⛔ not reached.

## Stop / pivot rules

Pause or pivot rather than endlessly repair when:

1. a candidate needs a new mechanism after every failed exposed statistic;
2. gains disappear on physical-leaf/manuscript holdout;
3. results collapse under stronger document/genre controls;
4. a claim depends on one transcription convention;
5. semantic interpretation requires post-hoc relabeling/free exceptions;
6. a simpler competing architecture obtains comparable prospective fit with materially lower target dependence/complexity.

## What to do when asked simply to "continue"

Execute **Phase62D** first. Commit the exposed-score ranking/unresolved-set interpretation while H62-P1 is still sealed. Only then implement and reveal H62-P1.