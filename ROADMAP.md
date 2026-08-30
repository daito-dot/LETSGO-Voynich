# LETSGO-Voynich research roadmap

Last updated: 2026-08-30

This file tracks progress and decision points. Exact numerical authority remains with phase-specific plans/results; `research/STATUS.md` controls accepted interpretation; `research/hypothesis-ledger.md` controls hypothesis history.

## Progress legend

- ✅ complete / accepted as current evidence
- ❌ falsified / rejected in tested form
- 🟡 current executable frontier
- ⏭ planned after the current gate
- ⛔ blocked pending an external prerequisite
- 🔁 recurring robustness / replication track

## North star

The goal is not to accumulate unusual Voynich statistics. It is to discriminate among competing mechanism families by:

1. common held-out scorecards;
2. prospective prediction;
3. explicit complexity cost;
4. independent external controls/content where available.

Families kept open:

- **N** — meaningful structured natural/technical text;
- **C** — meaningful text plus bounded cipher, shorthand, or deliberate obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms, introduced only after simpler families have fixed failure patterns.

Structural fit alone is not decipherment.

## Current position

| Stage | Status | Main consequence |
|---|---|---|
| Phases 1–43 | ✅ | direct semantic cribs and weak periodic interpretations were repeatedly rejected; structural invariants accumulated |
| Phases 44–52 | ✅ | mechanism tests began; simple DSL/copy stories were challenged and document/genre confounding became explicit |
| Phases 53–57 | ✅ | structural audit corrected page/leaf/sample-size issues and narrowed the robust residual to a leading ~2D subspace |
| Phase 58 | ✅ negative / ⛔ localized content | tested page-level visual relations were negative; defensible paragraph/object localization unavailable |
| Phase 59 | ✅ | paragraph entry decomposes into a substantial generic-medieval component plus a transferable Voynich-specific remainder |
| Phase 60 | ✅ | paragraph entry is genuine, manuscript-wide and short-lived; persistent line0 initialization rejected |
| Phase 61A | ✅ narrow gate | a boundary-aware nonsemantic entry mixture can reproduce the scalar entry-direction target |
| Phase 61B | ❌ A0 | A0 fails the joint locality / line-position / entry scorecard |
| Phase 61C | ✅ A1 survives | adding exactly one bounded local-family body mechanism brings entry, locality and line-position into the frozen broad held-out regime |
| Phase 62A | 🟡 current | recover exact Phase59 structured medieval controls and freeze the first fair N0/B0/A1 tournament before evaluation |

## Completed decision gate — Phase 61C

A1 was frozen before execution:

- boundary-aware paragraph-line0 entry mixture;
- one local-family reuse / one-edit body mechanism;
- no persistent paragraph latent state;
- no section-specific grammar;
- no separate line-position rule.

Five physical-leaf folds selected parameters using training leaves only.

Held-out ratio of means:

| target | A1 / Voynich | frozen gate |
|---|---:|---:|
| entry projection | **0.797** | 0.5–2.0 |
| local-prev10 fraction | **0.717** | 0.5–2.0 |
| line-position eta2 mean | **1.116** | 0.5–2.0 |

All three pass. See `experiments/phase61/REPORT_C.md` and `phase61c_results.json`.

### Consequence

G/A1 remains a viable **structural** family. This does not establish semantic emptiness or historical plausibility. A1 uses the empirical Voynich token-type inventory, so edit1 density is non-independent and cannot count as an independent prediction.

**Anti-rescue rule:** A1 is now frozen. Do not build A2 merely to fit additional exposed Voynich statistics before N0/B0 are tested.

## 🟡 Current gate — Phase 62A: fair tournament freeze

### Question

How much of the joint Voynich fingerprint can be produced by meaningful structured medieval text before encoding, and how much can a bounded boundary-blind encoder add, relative to frozen A1?

### Immediate tasks

1. recover the **exact** Phase59 external manuscript/control inputs and provenance;
2. define **N0** from source-native structured medieval entries/items without target-aware recoding;
3. define **B0/C0** as bounded, global, boundary-blind transformations of the same source family;
4. put N0, B0/C0 and frozen A1 on the same scorecard;
5. define explicit complexity accounting before seeing tournament outcomes;
6. freeze the plan before numerical evaluation.

### Stop condition for Phase62A

Do not run the tournament until source identity, preprocessing, scorecard, transforms, split units and falsification rules are committed.

## Main track A — first model-family tournament

### G/A1 — frozen nonsemantic competitor

Status: ✅ frozen after Phase61C.

Complexity already paid:

- paragraph-boundary-conditioned entry mixture;
- one local-family mechanism;
- one fitted `local_family_p` scalar in addition to A0 entry strength;
- empirical Voynich output vocabulary supplied, therefore lexical/edit1 density is not independent.

No A2 before the tournament.

### N0 — structured medieval plaintext

Status: 🟡 preparation.

Goal: measure the joint scorecard **before any ciphering** using source-native boundaries.

Requirements:

- exact Phase59 source documents/provenance recovered;
- several manuscripts where possible rather than one canonical prose source;
- source-native entry/item boundaries retained;
- no target-aware mapping to Voynich;
- document/genre variation reported rather than averaged away.

### B0/C0 — structured plaintext + bounded global encoder

Status: 🟡 preparation after N0 source freeze.

Allowed families should be low-complexity and boundary-blind, for example:

- monoalphabetic substitution;
- fixed homophonic substitution;
- fixed token/codeword mapping;
- similarly explicit global recoding with bounded degrees of freedom.

Forbidden:

- inspecting paragraph position;
- inspecting Voynich section labels;
- selecting rules using held-out Voynich statistics;
- adding a special mechanism after each failed target without naming a new model and charging its cost.

### M0 — mixed mechanism

Status: ⏭ deferred.

M0 becomes legitimate only after A1, N0 and B0/C0 have stable failure/success profiles and a mixed architecture makes a distinct frozen prediction.

## Main track B — prospective holdout bank

Many Voynich features are already exposed and may be used for model construction/diagnosis. They are not enough for a final model-family claim.

Before declaring a tournament winner, freeze at least one new evaluation dimension that was not used to construct the candidates.

Candidate holdouts:

- rare-token placement and recurrence;
- distance-dependent token-family geometry;
- paragraph-length response;
- within-section transition geometry;
- line-length response conditional on line position;
- folio-to-folio transfer geometry;
- glyph-level conditional structure not used by the models;
- independently localized label/body/diagram relation.

Rules:

1. commit the metric and falsification rule first;
2. do not swap a failed holdout for a favorable one without recording the failure;
3. model-selection targets and final prospective targets remain distinct.

Status: ⏭ freeze after the first N0/B0/A1 scorecard is defined and before a winner is claimed.

## Main track C — medieval document/genre controls

Phase59 established that medieval document structure is a major confound and possible explanatory component.

Priority expansion:

- medical/treatment collections;
- recipe and pharmacological lists;
- herbals;
- astrological/astronomical practical texts;
- almanacs/calendars;
- scholastic/glossed texts;
- ecclesiastical/liturgical structured texts;
- inventories/ledgers/strongly itemized documents.

Goals:

- 🟡 recover exact Phase59 inputs;
- ⏭ add multiple manuscripts within genres;
- ⏭ repeat external entry-basis decomposition;
- ⏭ test stability of the Voynich-orthogonal remainder as the external basis grows;
- 🔁 preserve leave-one-document / leave-one-genre-out checks.

## Main track D — content anchors

Completed:

- ✅ Phase58 page-level Biological/balneological and early Herbal-A visual tests were negative in the tested representation;
- ✅ post-hoc paragraph/object pairing was refused when defensible localization was unavailable.

Next admissible semantic test requires an external mapping fixed without looking at target strings.

Status: ⛔ strong localized content test blocked pending better external annotation/localization.

A single prospective content prediction is more valuable than many additional structural anomalies.

## Main track E — transcription/representation robustness

Current main analyses use ZL3b/EVA.

Before mature claims:

- 🔁 continue reasonable EVA representation checks;
- ⏭ replicate strongest entry/local-family results on an independent transcription lineage where feasible;
- ⏭ identify dependence on spacing, uncertain glyph segmentation or editorial conventions.

Priority replication targets:

1. short-lived manuscript-wide paragraph-entry role;
2. generic-medieval + Voynich-specific entry decomposition;
3. local near-family activation;
4. line-position grammar;
5. Phase61C A1 tournament outcome after scorecard stabilization.

## Main track F — complexity accounting

The tournament should move from verbal rule counts toward quantitative cost.

Planned:

- 🟡 explicit parameter/mechanism count for Phase62;
- ⏭ predictive log loss / held-out likelihood where models permit it;
- ⏭ description length for codebooks, states, boundary conditions and section parameters;
- ⏭ Pareto comparison rather than one arbitrary weighted score.

A complex model does not win merely because it fits more exposed statistics.

## Decision milestones

### M1 — Phase61 architecture gate

✅ Complete.

A0 failed; A1 survived the frozen first joint gate and is now frozen.

### M2 — first fair model-family tournament

🟡 Current major milestone.

Complete when:

- N0, B0/C0 and A1 are compared on the same scorecard;
- source corpora and transforms are independently specified;
- complexity costs are reported;
- no family is judged by a uniquely favorable statistic.

### M3 — prospective discriminator

⏭ Planned.

Complete when a model-family ranking is frozen and challenged by at least one genuinely new preregistered holdout.

### M4 — external robustness

⏭ Planned / 🔁 recurring.

Requires broader medieval controls and, where feasible, an independent Voynich transcription lineage.

### M5 — content relation

⛔ Not established.

Requires a frozen representation/mechanism to predict independently grounded manuscript content on unseen material.

### M6 — decipherment threshold

⛔ Not reached.

Requires an executable fixed mapping/generation rule, substantial unseen prediction, interpretable fixed output, strong competitors/nulls, prospective/external replication and explicit accounting of failures/exceptions.

## Stop / pivot rules

Pause or pivot rather than endlessly repair when:

1. a candidate needs a new mechanism after every failed exposed statistic;
2. gains disappear on physical-leaf/section/document holdout;
3. results collapse under stronger document/genre controls;
4. a claim depends on one transcription convention without robustness;
5. semantic interpretation requires post-hoc relabeling/free exceptions;
6. a simpler competing architecture achieves comparable predictive fit at substantially lower complexity.

## What to do when asked simply to "continue"

1. read `RESUME.md`, this roadmap, `research/STATUS.md` and the exact current phase plan/result;
2. execute the current yellow gate rather than inventing a new local analysis;
3. record negative results as first-class outcomes;
4. update this roadmap when the active milestone/dependency changes;
5. update `research/STATUS.md` only when accepted scientific interpretation changes.
