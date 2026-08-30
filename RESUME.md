# RESUME — how to restart this research

This file is the deterministic entry point for a new researcher or AI/chat session.

## Read in this order

1. `README.md`
2. `ROADMAP.md`
3. `RESEARCH_PROTOCOL.md`
4. `research/STATUS.md`
5. `research/hypothesis-ledger.md`
6. `research/REPRODUCIBILITY_AUDIT.md`
7. `research/AUDIT_PHASE51_61C_20260830.md`
8. `experiments/phase61/PLAN_C.md`, `IMPLEMENTATION_C.md`, `REPORT_C.md`, `phase61c_results.json`
9. `experiments/phase62/PLAN.md`
10. `experiments/phase62/REPORT_B.md`, `phase62b_n0_results.json`
11. `experiments/phase62/REPORT_C.md`, `phase62c_c0_a1_results.json`
12. `experiments/phase62/DECISION_D.md`
13. `experiments/phase62/IMPLEMENTATION_P.md`, `IMPLEMENTATION_P_EDGE_CASES.md`
14. `experiments/phase62/REPORT_P.md`, `phase62p_h62p1_results.json`
15. `experiments/phase63/PLAN_A.md`
16. `experiments/phase63/DETERMINISM_AUDIT_A.md`
17. `experiments/phase63/REPORT_A.md`, `phase63a_training_vocab_results.json`
18. exact executable/source files before changing numerical interpretation

Do not reconstruct the project from old chat when the repository contains a newer state.

## Authority hierarchy

1. phase-specific frozen plan/result/report controls exact method and historical numerical result;
2. `research/STATUS.md` controls current accepted interpretation;
3. `research/hypothesis-ledger.md` controls hypothesis status/history;
4. reproducibility audits control what is exact-replay certified;
5. `ROADMAP.md` controls active sequencing;
6. frozen narrative/decision files preserve pre-result predictions;
7. old chat/memory is non-authoritative when repository evidence conflicts.

## Current accepted paragraph/mechanism state

Retain:

> Voynich paragraph starts instantiate a manuscript-wide, transferable formal entry register. It is partly comparable to medieval structured-document entry grammar and partly Voynich-specific, but its detectable influence is short-lived rather than a persistent paragraph initializer.

A1 is the current leading tested structural mechanism. It is a boundary-aware generator with one bounded local-family body process, no persistent paragraph latent state, no section-specific grammar and no separate line-position rule.

Phase61C narrow scalar gate:

- entry projection **0.797×**
- local-prev10 **0.717×**
- aggregate line-position eta2 **1.116×**

The Phase61 audit remains binding: A1 does not reproduce the full line-position coordinate profile.

## Phase62 exposed tournament

### N0

Source-native structured medieval text:

- S1 **-0.980×** Voynich
- S2 **0.133×**
- S3 **0.989×**

Fails joint gate; S3 match shows generic line-position structure alone is weak discrimination.

### C0

Best frozen reversible boundary-blind transform = non-overlapping digraph coding, selected independently in all five folds.

- S1 **-0.932×**
- S2 **0.249×**
- S3 **0.856×**

Materially improves N0 but remains insufficient on S1/S2.

### frozen A1

No Phase62 retuning:

- S1 **0.623×**
- S2 **1.512×**
- S3 **0.587×**

Passes exposed ratio-of-means gate, with fold/profile caveats retained.

## Phase62D pre-prospective freeze

Before H62-P1 was computed, the repository committed:

> exposed scalar structural ranking: **A1 > C0 > N0**

while keeping:

> overall N/C/G family conclusion: **unresolved pending prospective validation**.

It also committed A1's H62-P1 directional prediction: explicit maximum 10-token local-family memory should yield stronger near-family recurrence concentration in 1–10 relative to 11–40 tokens; not a literal zero-after-10 claim.

## Phase62P H62-P1 — genuine prospective A1 support

H62-P1 was frozen in Phase62A before tournament outcomes and implemented only after Phase62D.

| candidate | mean D | median D | D wins | mean |ΔC_short| | C wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

Accepted wording:

> **Frozen A1 predicts the previously sealed distance-dependent near-family recurrence geometry substantially better than tested N0/C0. A1 is the leading tested structural mechanism with genuine prospective support.**

This is not evidence that Voynich is meaningless or that A1 is historical truth.

First-reveal raw JSON SHA-256:

`0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264`

## Phase63A — training-only vocabulary robustness: PASS

Phase63A removes every token type not observed on a fold's training physical leaves, without parameter repair.

Intervention size:

- full vocabulary: 8,295 types;
- mean training vocabulary: **7,050.2**;
- mean held-out distinct-type coverage: **0.5083**;
- mean held-out occurrence coverage: **0.8016**.

Thus roughly half of held-out distinct token types are unavailable to generation.

A1-R1 / Voynich exposed ratio-of-means:

- S1 **0.65353**
- S2 **1.51061**
- S3 **0.58264**

All pass historical `[0.5,2.0]` gate.

H62-P1:

- mean D **0.76660**
- median D **0.80945**
- mean |ΔC_short| **0.11769**
- versus N0: 5/5 fold wins on both metrics
- versus C0: 5/5 fold wins on both metrics

All frozen R1/R2/R3 conditions pass. Degradation versus full-vocabulary A1 is negligible.

Accepted wording:

> **A1's exposed and prospective structural advantage does not depend on access to token types unique to the held-out physical leaves.**

This reduces one target-leakage concern. A1 still uses training-side Voynich morphology/vocabulary, Voynich-derived architecture, frozen Voynich-selected parameters, explicit paragraph boundaries/10-token memory and the true held-out layout/token counts.

### Phase63A replay note

First raw result SHA-256:

`bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7`

A clean replay differed bytewise only in 16 S1 floating-point fields, maximum absolute `2.22e-16`. S2/S3/H62-P1/discrete fields and verdicts were exactly identical. Canonical 14-decimal semantic SHA:

`cd53f47729c864badb5e8c747cfd9ad989de9c616ca54dd5bdcb83b075c33c74`

Read `experiments/phase63/DETERMINISM_AUDIT_A.md` before asserting raw-byte determinism.

## Current frontier — Phase63B independent transcription replication

When asked to continue:

1. find a genuinely independent Voynich transcription lineage with stable public provenance/version/hash;
2. document how glyph encoding, uncertain characters, spaces, lines and paragraph starts differ from ZL3b;
3. freeze a deterministic page/physical-leaf/line/paragraph mapping before computing results;
4. decide which Phase60–63 metrics are representation-comparable without adapting them to recreate the ZL3b outcome;
5. commit the source/design freeze;
6. only then run replication.

Priority targets:

1. paragraph-entry specialization vs internal pseudo-boundaries;
2. local edit1/near-family recurrence geometry;
3. H62-P1 five-bin profile;
4. A1-R1 advantage if a defensible independent-transcription generator can be defined;
5. aggregate S3 only as secondary because Phase62 shows it is weak alone.

If a result fails under the independent transcription, record the failure before changing token/glyph treatment.

## Research families

- **N:** simple N0 disfavored; broader meaningful-text families remain open.
- **C:** C0 limited/insufficient; stronger C1 only later as separately frozen model.
- **G:** A1 currently leads tested structural mechanisms prospectively and survives held-out-vocabulary restriction, but remains non-autonomous and historically/semantically ungrounded.
- **M:** deferred.

## Important retained corrections

- Phase3 plant-label semantic headline: NOT SUPPORTED.
- Phase53/54 recto/verso collapse corrected in Phase55.
- Phase56 unmatched PC1 sample-size contamination withdrawn.
- Phase60B exact historical eligibility/fine carrier magnitudes not replay-certified.
- Phase60D persistent-initialization evidence coupled; superseded by 60D2/60E; clean 60E replay remains debt.
- Phase61A is not prospective validation of preselected A0 strength.
- Phase61C aggregate eta2 does not establish full profile reproduction.
- Phase59 small semantic subsets are development evidence; Phase62 objective panel supersedes them for fair comparison.

## Before declaring decipherment

Require an executable fixed mapping/generation rule, substantial unseen prediction, fixed interpretable output, strong competitors/nulls, prospective/external replication, independently grounded content relation, and explicit accounting of failures/exceptions.