# LETSGO-Voynich research roadmap

Last updated: 2026-08-30

This file tracks progress and decision points. Exact numerical authority remains with phase-specific plans/results; `research/STATUS.md` controls accepted interpretation; `research/hypothesis-ledger.md` controls hypothesis history. Reproducibility caveats in `research/REPRODUCIBILITY_AUDIT.md` and `research/AUDIT_PHASE51_61C_20260830.md` remain binding.

## Progress legend

- ✅ complete / accepted as current evidence
- ❌ falsified / rejected in tested form
- 🟡 current executable frontier
- ⏭ planned after current gate
- ⛔ blocked pending external prerequisite
- 🔒 frozen / sealed
- 🔁 robustness / replication track

## North star

Discriminate among competing mechanism families by:

1. common held-out scorecards;
2. genuinely prospective prediction;
3. explicit target-dependence / complexity cost;
4. independent transcription and external controls;
5. independently grounded content prediction before semantic promotion.

Families remain open:

- **N** — meaningful structured natural/technical text;
- **C** — meaningful text plus cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms only after simpler families have fixed failure profiles.

Structural fit is not decipherment.

## Current position

| Stage | Status | Main consequence |
|---|---|---|
| Phases 1–43 | ✅ | direct semantic cribs and weak periodic interpretations repeatedly failed; structural invariants accumulated |
| Phases 44–52 | ✅ | mechanism tests and document/genre confounding became explicit |
| Phases 53–57 | ✅ | audits corrected page/leaf/sample-size issues and narrowed robust residual opportunities |
| Phase 58 | ✅ negative / ⛔ localized content | page-level visual relations negative; defensible object/paragraph mapping unavailable |
| Phase 59 | ✅ development | broad entry transition partly overlaps medieval structured-document entry grammar, with Voynich-specific remainder |
| Phase 60 | ✅ with audit caveats | paragraph entry genuine, transferable and short-lived; exact 60B/60E replay debts remain |
| Phase 61A | ✅ narrow | boundary-aware A0 can reproduce scalar entry direction |
| Phase 61B | ❌ A0 | A0 fails joint locality/position/entry scorecard |
| Phase 61C | ✅ narrow | A1 survives frozen aggregate scalar gate; full line-position coordinate profile still mismatched |
| Phase 62A | ✅ freeze | objective N0 panel, common scorecard, bounded C0, complexity ledger and H62-P1 frozen |
| Phase 62B | ❌ N0 | source-native structured Latin matches generic S3 but fails S1/S2 |
| Phase 62C | ✅ | C0 materially improves N0 but remains insufficient; frozen A1 leads exposed scalar fit |
| Phase 62D | ✅ pre-prospective freeze | exposed ranking fixed as `A1 > C0 > N0`; overall family conclusion kept unresolved |
| Phase 62P / H62-P1 | ✅ prospective A1 support | A1 uniquely wins both preregistered recurrence-profile diagnostics in 5/5 physical-leaf folds |
| **Phase 63A** | **✅ target-dependence robustness** | training-leaf-only output vocabulary leaves exposed and H62-P1 advantages essentially unchanged |
| **Phase 63B** | **🟡 current** | freeze and execute an independent Voynich transcription/segmentation-lineage replication |
| Phase 64 | ⏭ | after independent replication, decide whether next highest-value challenge is autonomous morphology, bounded C1, or externally grounded content |

## Strongest current mechanism evidence

### Phase62 exposed tournament

- **N0:** S1 `-0.980×`, S2 `0.133×`, S3 `0.989×` Voynich. Not jointly competitive.
- **C0:** S1 `-0.932×`, S2 `0.249×`, S3 `0.856×`; digraph coding materially improves N0 but remains insufficient.
- **A1:** S1 `0.623×`, S2 `1.512×`, S3 `0.587×`; strongest exposed scalar fit, with known fold/profile heterogeneity and higher target dependence.

Before prospective reveal, Phase62D froze:

> **Exposed scalar fit: A1 > C0 > N0. Overall N/C/G mechanism-family conclusion unresolved.**

### Phase62P H62-P1 — sealed prospective test

H62-P1 was frozen in Phase62A before tournament outcomes. It measures near-family recurrence excess in distance bins `1–2 / 3–5 / 6–10 / 11–20 / 21–40` and compares normalized profile shape plus short-range concentration.

| candidate | mean D_profile | median D_profile | D wins | mean |ΔC_short| | C wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

A1 satisfies every preregistered prospective-leader condition.

Accepted promotion:

> **A1 is the leading tested structural mechanism with genuine prospective support relative to N0/C0.**

This is not a claim of meaninglessness, historical production identity or decipherment.

## Completed Phase63A — training-only vocabulary robustness

Phase63A removes token types that occur only on each held-out physical-leaf fold. No new mechanism or retuning is allowed.

### How strong was the intervention?

Across folds:

- full manuscript vocabulary: 8,295 types;
- mean training vocabulary: **7,050.2 types**;
- mean held-out distinct-type coverage by training vocabulary: **0.5083**;
- mean held-out token-occurrence coverage: **0.8016**.

Thus roughly **49% of held-out distinct token types** and **20% of held-out token occurrences** correspond to types unavailable to the generator.

All generated tokens are audited to belong to the training vocabulary.

### Exposed score retention

A1-R1 / Voynich ratio-of-means:

- S1 **0.65353**
- S2 **1.51061**
- S3 **0.58264**

All remain in the frozen historical `[0.5,2.0]` gate.

### H62-P1 retention

A1-R1:

- mean `D_profile` **0.76660**
- median `D_profile` **0.80945**
- mean `|ΔC_short|` **0.11769**

It beats N0 and C0 in **5/5 folds on both metrics**.

Relative to full-vocabulary A1, degradation is negligible:

- mean `D_profile` `+0.00401`;
- median `D_profile` `-0.00116`;
- mean `|ΔC_short|` `+0.00153`.

All frozen Phase63A R1/R2/R3 survival conditions pass.

Accepted interpretation:

> **A1's exposed and prospective structural advantage does not depend on access to token types unique to the held-out physical leaves.**

This reduces one major target-leakage concern but does not make A1 autonomous. It still uses Voynich training-side morphology/vocabulary, Voynich-derived architecture and frozen Voynich-selected parameters.

### Replay audit

First raw scientific result:

- Actions run `33315453851`
- artifact `9733309531`
- raw JSON SHA-256 `bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7`

A cross-run raw SHA mismatch was audited before acceptance. First and clean replay parsed JSON differ in only 16 S1 floating-point scalars, maximum absolute difference `2.22e-16`; all S2/S3/H62-P1/discrete fields and verdicts are identical. Canonical 14-decimal semantic SHA is identical:

`cd53f47729c864badb5e8c747cfd9ad989de9c616ca54dd5bdcb83b075c33c74`

See `experiments/phase63/DETERMINISM_AUDIT_A.md` and `REPORT_A.md`.

## 🟡 Current gate — Phase63B independent transcription replication

The next highest-value objection is no longer held-out vocabulary leakage. It is **representation/transcription dependence**.

### Question

> Do the strongest Phase60–63 findings survive an independently maintained Voynich transcription/segmentation lineage rather than ZL3b/EVA?

### Phase63B source/design freeze requirements

Before calculating replication outcomes:

1. identify at least one genuinely independent transcription lineage with stable provenance/version/hash;
2. document how its glyph/token/space conventions differ from ZL3b;
3. define a deterministic paragraph/line/physical-leaf mapping without tuning against ZL3b results;
4. freeze which metrics are technically comparable under that representation;
5. freeze any unavoidable cross-transcription normalization before outcomes;
6. preserve the original ZL3b result as discovery/primary evidence rather than rewriting it.

### Priority replication targets

In order:

1. genuine paragraph-boundary entry specialization versus internal pseudo-boundaries;
2. local near-family activation / recurrence-distance geometry;
3. H62-P1 short-vs-long profile shape;
4. A1-R1 structural advantage if the independent representation supports a defensible generator vocabulary/neighbor definition;
5. aggregate line-position structure only as a secondary check because Phase62 shows S3 alone is weak discrimination.

### Stop rule

If a claimed invariant depends strongly on ZL3b segmentation/glyph conventions, record the failure before adapting the metric. Do not tune the independent transcription until it recreates the ZL3b answer.

## Later model-family work

### G family

Do **not** add A2 merely to repair known B4/B5 or line-profile residuals. If independent replication survives, the next G challenge is autonomy: generate/learn morphology without supplying the empirical Voynich token inventory.

### C family

C0 is useful but insufficient. A stronger C1 is legitimate only as a separately frozen historically/mathematically motivated model with explicit complexity cost after current replication.

### N/content lane

Simple N0 is disfavored, not all meaningful-text families. Strong semantic promotion still requires externally grounded object/paragraph mapping and unseen content prediction.

## Reproducibility debt

Retain and eventually close:

- exact historical Phase60B eligibility/carrier replay;
- clean Phase60E executable replay;
- exact historical A0 provenance where recoverable.

These debts limit fine historical claims but do not erase the newer prospectively frozen Phase62/63 results.

## Decision milestones

- **M1 Phase61 architecture gate:** ✅ A0 fails jointly; A1 survives narrow scalar gate.
- **M2 exposed N/C/G tournament:** ✅ `A1 > C0 > N0` among tested implementations.
- **M3 prospective discriminator:** ✅ A1 wins H62-P1 5/5 on both frozen metrics.
- **M4 target-dependence robustness:** ✅ Phase63A survives training-only vocabulary restriction.
- **M5 independent transcription robustness:** 🟡 Phase63B current.
- **M6 content relation:** ⛔ not established.
- **M7 decipherment threshold:** ⛔ not reached.

## Stop / pivot rules

Pause or pivot rather than endlessly repair when:

1. a candidate needs a new mechanism after each failed frozen test;
2. gains disappear under training-only or independent-source constraints;
3. results collapse under physical-leaf/manuscript/transcription holdout;
4. semantic interpretation requires post-hoc labels or free exceptions;
5. a simpler competing architecture obtains comparable prospective fit at materially lower target dependence/complexity.

## What to do when asked simply to "continue"

Execute **Phase63B source recovery/design freeze first**. Do not calculate an independent-transcription replication result until source identity, segmentation mapping, comparable metrics and falsification rules are committed.