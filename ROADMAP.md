# LETSGO-Voynich research roadmap

Last updated: 2026-08-30

This file tracks research progress and decision points. It is not the authority for exact numerical results; phase-specific reports control exact methods and values, `research/STATUS.md` controls accepted interpretation, and `research/hypothesis-ledger.md` controls hypothesis history.

## Progress legend

- ✅ complete / accepted as current evidence
- ❌ falsified / rejected in the tested form
- 🟡 current executable frontier
- ⏭ planned after the current gate
- ⛔ blocked pending an external prerequisite
- 🔁 recurring robustness / replication track

## North star

The research goal is not to accumulate unusual Voynich statistics. It is to discriminate among competing mechanism families by prospective prediction, joint constraint satisfaction, and explicit complexity cost.

Current families kept open:

- **N — meaningful natural or technical text**
- **C — meaningful text plus cipher, shorthand, or deliberately deceptive encoding**
- **G — constrained nonsemantic / formal generation**
- **M — mixed mechanisms**

A mechanism advances only when it predicts held-out or prospectively frozen evidence better than plausible competitors. Structural fit alone is not decipherment.

## Current position

### Completed research arc

| Stage | Status | Main consequence |
|---|---|---|
| Phases 1–43 | ✅ historical foundation | many direct semantic cribs and weak periodic interpretations were rejected; structural invariants accumulated |
| Phases 44–52 | ✅ mechanism groundwork | simple copy/locality stories and a tuned finite-state DSL were challenged; document/genre confounding became explicit |
| Phases 53–57 | ✅ structural audit | page/leaf and sample-size corrections narrowed the robust latent residual to a leading ~2D subspace |
| Phase 58 | ✅ negative / blocked content tests | tested page-level visual relations were negative; defensible localized object mapping remained unavailable |
| Phase 59 | ✅ medieval-entry decomposition | Voynich paragraph entry contains a substantial generic medieval entry component plus a transferable Voynich-specific remainder |
| Phase 60 | ✅ narrative falsification | paragraph entry is genuine, manuscript-wide and short-lived; persistent line0 initialization of later body state was rejected |
| Phase 61A | ✅ narrow A0 gate survived | one explicit paragraph-entry mixture can reproduce the scalar entry-direction target |
| Phase 61B | ❌ A0 rejected as joint model | A0 fails joint locality / line-position / entry constraints despite passing the narrow entry gate |
| Phase 61C | 🟡 frozen, not yet executed | test A1 = entry mixture + one local-family body mechanism; no further repair is allowed inside A1 |

## Immediate decision gate — Phase 61C

**Question:** can a minimally repaired nonsemantic generator jointly reproduce the surviving entry signature, local near-family activation, and line-position structure on held-out physical leaves?

A1 is already frozen in `experiments/phase61/PLAN_C.md`.

Allowed additions relative to A0:

1. paragraph-line0 boundary-aware entry mixture;
2. one local-family reuse / one-edit body mechanism.

Not allowed inside A1:

- persistent paragraph latent state;
- section-specific grammar;
- a new line-position mechanism;
- post-hoc parameter expansion after held-out results are seen.

### Gate rule

- **If A1 survives:** retain G as a viable structural family, record its explicit complexity cost, then compare it directly with meaningful-text competitors.
- **If A1 fails:** do **not** immediately invent A2. Freeze the failure and move first to the B0/N0 comparison so the project does not become an endless generator-repair exercise.

## Main track A — mechanism-family tournament

### A1. Boundary-aware nonsemantic generator

- 🟡 Execute Phase 61C exactly as frozen.
- ⏭ Record held-out joint scorecard and complexity increment.
- ⏭ Freeze A1 before any further architecture change.

### B0. Structured medieval plaintext + global encoding

Goal: determine whether meaningful structured text can inherit medieval entry grammar and also reproduce Voynich-specific morphology/local-family/line-position constraints under a bounded, boundary-blind encoder.

Required properties:

- source-native medieval item/paragraph boundaries;
- global transform cannot inspect Voynich paragraph position or section;
- bounded monoalphabetic / homophonic / token-codebook or similarly explicit recoding families;
- same frozen scorecard used for G competitors;
- codebook and state complexity counted explicitly.

Current status: ⏭ planned. Exact Phase59 external source inputs should be recovered before direct numerical cipher simulation rather than reconstructed approximately.

### N0. Unencoded structured medieval controls

Goal: measure how much of the joint fingerprint arises before any ciphering.

- ⏭ Run the same scorecard on source-native structured controls.
- ⏭ Separate document/genre effects from encoding effects.
- ⏭ Prefer several manuscripts per genre rather than one canonical prose source.

### M0. Mixed mechanism

Status: ⏭ deferred.

Do not introduce a mixed model merely because N/C/G each miss different targets. M0 becomes legitimate only after N0, B0 and A1 have fixed failure patterns and a mixed architecture makes a distinct frozen prediction with an explicit complexity increment.

## Main track B — prospective holdout bank

The project has already inspected many features. Those features may be used to fit or diagnose models, but success on them alone is no longer strong validation.

Before a model-family winner is claimed, freeze a set of **new evaluation dimensions not used to construct the candidate architecture**.

Candidate future holdouts include:

- rare-token placement and recurrence;
- distance-dependent token-family geometry;
- paragraph-length response;
- within-section local transition geometry;
- line-length response conditional on line position;
- folio-to-folio transfer patterns;
- glyph-level conditional structure not used by the model;
- label/body/diagram relations with independently fixed localization.

Rules:

1. select the next holdout before testing the candidate model on it;
2. commit the metric and falsification rule first;
3. do not replace a failed holdout with a more favorable one without recording the failure;
4. model selection targets and final prospective targets remain distinct.

Status: ⏭ formal holdout bank to be frozen after Phase 61C and before broad tournament claims.

## Main track C — medieval document and genre controls

Phase59 showed that a large portion of the paragraph-entry transition is not safely described as uniquely Voynich.

Next control expansion should separate:

`individual manuscript -> document genre -> language`

Priority source families:

- medical / treatment collections;
- recipe and pharmacological lists;
- herbals;
- astrological / astronomical practical texts;
- almanacs and calendars;
- scholastic / glossed texts;
- ecclesiastical / liturgical structured texts;
- inventories, ledgers and other strongly itemized documents.

Progress goals:

- ⏭ recover exact Phase59 control inputs and provenance;
- ⏭ expand to multiple manuscripts within the same genre;
- ⏭ repeat the external entry-basis decomposition;
- ⏭ test whether the Voynich-orthogonal remainder remains stable as the external basis grows;
- 🔁 preserve leave-one-document / leave-one-genre-out checks.

## Main track D — content anchors

This track is deliberately sparse. The goal is not unconstrained word guessing.

Completed:

- ✅ Phase58 page-level Biological/balneological and early Herbal-A visual tests were negative in the tested representation.
- ✅ the project refused post-hoc paragraph-to-object pairing when defensible localization was unavailable.

Next admissible content test requires an external mapping fixed without looking at the target text, for example a defensible paragraph/object association or another independently grounded content label.

Status: ⛔ blocked for strong localized tests until better external annotation or mapping becomes available.

A single strong prospective content prediction is more valuable than many additional structural curiosities.

## Main track E — transcription and representation robustness

Current main analyses use the ZL3b / EVA-derived working transcription.

Before treating a major structural result as mature:

- 🔁 verify reasonable EVA unit representations;
- ⏭ replicate the strongest paragraph-entry and local-family results on an independent transcription lineage where feasible;
- ⏭ identify results that depend materially on spacing, uncertain glyph segmentation, or editorial conventions;
- ⏭ distinguish manuscript evidence from transcription artefact.

Priority replication targets:

1. manuscript-wide short-lived paragraph-entry register;
2. generic-medieval + Voynich-specific entry decomposition;
3. local near-family activation;
4. line-position grammar.

## Main track F — complexity and model accounting

Narrative statements such as "one extra mechanism" should become quantitative model costs where practical.

Planned evaluation:

- ⏭ predictive log loss / held-out likelihood where model families permit it;
- ⏭ description length for codebooks, states, section parameters and boundary conditions;
- ⏭ explicit parameter and rule count as a minimum fallback;
- ⏭ Pareto comparison rather than one arbitrary weighted score.

A complex generator does not win merely by reproducing more exposed Voynich statistics.

## Decision milestones

### Milestone M1 — Phase 61 architecture gate

Complete when:

- A1 has an executed held-out joint scorecard;
- its failure/survival is frozen;
- no post-hoc A2 rescue is folded into the same hypothesis.

Current: 🟡 in progress.

### Milestone M2 — first fair model-family tournament

Complete when:

- N0, B0 and A1 are compared on the same structural scorecard;
- input corpora and transforms are independently specified;
- complexity costs are reported;
- no family is judged by a statistic selected uniquely in its favor.

Current: ⏭ next major milestone.

### Milestone M3 — prospective discriminator

Complete when:

- a model-family ranking is frozen;
- at least one genuinely new holdout dimension is committed before evaluation;
- the ranking survives or is revised by that prospective result.

Current: ⏭ planned.

### Milestone M4 — external robustness

Complete when the major surviving mechanism result is stable across a materially broader medieval control panel and, where feasible, an independent Voynich transcription lineage.

Current: ⏭ planned / recurring.

### Milestone M5 — content relation

Complete only when a frozen structural or mechanism representation predicts independently grounded manuscript content on unseen material.

Current: ⛔ not established.

### Milestone M6 — decipherment threshold

Not reached unless there is:

- an executable fixed mapping / generation rule;
- substantial prediction of unseen material;
- interpretable fixed output;
- strong structure-preserving nulls and competing mechanisms;
- prospective or external replication;
- explicit accounting of failures and exceptions.

Current: ⛔ not reached.

## Stop / pivot rules

Pause the current branch of research rather than endlessly repairing it when any of the following occurs:

1. a candidate needs a new mechanism after every failed exposed statistic;
2. performance gains disappear on physical-leaf or section holdout;
3. a result collapses under stronger document/genre controls;
4. a claim depends on one transcription convention without robustness;
5. semantic interpretation requires post-hoc relabeling or free exceptions;
6. a simpler competing architecture attains comparable predictive fit at substantially lower complexity.

## What to do when asked simply to "continue"

1. read `RESUME.md`, this roadmap, `research/STATUS.md`, and the exact current phase plan/result;
2. execute the current yellow gate rather than inventing a new local analysis;
3. record negative results as first-class outcomes;
4. update this roadmap only when a milestone, dependency, or current frontier changes;
5. update `research/STATUS.md` only when accepted scientific interpretation changes.
