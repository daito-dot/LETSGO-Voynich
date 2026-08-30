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
| Phase 63A | ✅ target-dependence robustness | training-leaf-only output vocabulary leaves exposed and H62-P1 advantages essentially unchanged |
| **Phase 63B** | **✅ strong external replication** | entry/recurrence effects survive GC v101 and IT EvaT; frozen A1-R1 transfers to IT without retuning and passes W1/W2 criteria |
| **Phase 64A** | **✅ mixed / strict autonomy fail** | synthetic-vocabulary A1 preserves core H62 geometry, but canonical ZL fails frozen S3 gate at `0.468×`; IT arm passes |
| **Phase 64B / C1** | **🟡 current fairness gate** | freeze a serious bounded meaningful-text + encoding/shorthand competitor before any family-level conclusion |

## Evidence staircase for the current A1 mechanism

The strongest current support is now sequential rather than a single fit result:

1. **Phase61C — held-out exposed regime:** A1 reaches broad scalar entry/locality/aggregate-position ranges but has known multivariate profile mismatch.
2. **Phase62C — fair exposed tournament:** among tested implementations, `A1 > C0 > N0` on the common scorecard.
3. **Phase62P — sealed prospective prediction:** A1 predicts previously unseen recurrence-distance geometry and wins both frozen diagnostics in 5/5 folds.
4. **Phase63A — held-out vocabulary restriction:** the advantage survives removal of token types unique to held-out leaves.
5. **Phase63B — independent transcription replication:** core entry/recurrence effects survive independent v101/EvaT transcriptions and frozen ZL-selected A1 parameters transfer to IT without retuning.

This is materially stronger evidence for a real formal generation layer. It still does not identify that layer as nonsemantic or historically identical to A1.

## Phase62 exposed tournament

- **N0:** S1 `-0.980×`, S2 `0.133×`, S3 `0.989×` Voynich. Not jointly competitive.
- **C0:** S1 `-0.932×`, S2 `0.249×`, S3 `0.856×`; digraph coding materially improves N0 but remains insufficient.
- **A1:** S1 `0.623×`, S2 `1.512×`, S3 `0.587×`; strongest exposed scalar fit, with known fold/profile heterogeneity and higher target dependence.

Before prospective reveal, Phase62D froze:

> **Exposed scalar fit: A1 > C0 > N0. Overall N/C/G mechanism-family conclusion unresolved.**

## Phase62P H62-P1 — sealed prospective test

| candidate | mean D_profile | median D_profile | D wins | mean |ΔC_short| | C wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

Accepted promotion:

> **A1 is the leading tested structural mechanism with genuine prospective support relative to N0/C0.**

## Phase63A — training-only vocabulary robustness

Across folds:

- full manuscript vocabulary: 8,295 types;
- mean training vocabulary: **7,050.2 types**;
- mean held-out distinct-type coverage by training vocabulary: **0.5083**;
- mean held-out token-occurrence coverage: **0.8016**.

A1-R1 / Voynich ratio-of-means:

- S1 **0.65353**
- S2 **1.51061**
- S3 **0.58264**

H62-P1:

- mean `D_profile` **0.76660**
- median **0.80945**
- mean `|ΔC_short|` **0.11769**
- beats N0 and C0 **5/5 folds on both metrics**.

Accepted:

> **A1's exposed and prospective structural advantage does not depend on access to token types unique to the held-out physical leaves.**

This does not make A1 autonomous: training-side empirical morphology/vocabulary remains supplied.

## Phase63B — independent-transcription replication: COMPLETE

### Independence design

- **GC2a / v101:** independent transcription/alphabet, analyzed natively with no v101→EVA mapping.
- **IT2a / EvaT:** independent reading/transcription, supporting full A1-R1 transfer without cross-alphabet invention.
- W1 primary + predeclared W2 sensitivity.
- exact source hashes, parser, populations, folds, metrics, seeds and pass/fail rules frozen before first scientific reveal.

### GC observational replication

GC-R1 entry specialization:

- W1 positive **5/5 folds**, mean projection **1.00905**;
- W2 mean **1.08374**, no sign reversal.

GC-R2 H62-P1:

- W1 positive `C_short` **5/5**, mean **0.58781**;
- W2 mean **0.59868**, no sign reversal.

**GC-R1/R2 pass.**

### IT observational replication

IT-R1:

- positive **5/5**, W1 mean projection **0.77003**.

IT-R2:

- positive `C_short` **5/5**;
- W1 mean **0.58501**;
- W2 mean **0.59326**.

**IT-R1/R2 pass.**

### IT-R3 full frozen A1-R1 transfer

W1 A1-R1 / IT exposed ratios:

- S1 **0.73723×**
- S2 **1.58617×**
- S3 **0.64696×**

All pass the frozen aggregate `[0.5,2]` gate.

H62-P1 W1:

| candidate | mean D_profile | mean |ΔC_short| |
|---|---:|---:|
| N0 | 1.47727 | 0.62192 |
| fixed C0-4 | 1.79735 | 1.29206 |
| **A1-R1** | **0.83028** | **0.07184** |

A1-R1 wins versus N0 `4/5` on D and `5/5` on C-short; versus C0 `5/5` on both. W2 also passes the frozen R3 criterion.

The one D-profile loss to N0 is fold2 and remains recorded. Individual exposed fold ratios are heterogeneous; the frozen gate was aggregate ratio-of-means, not universal per-fold matching.

Frozen classification:

> **STRONG REPLICATION — GC independent-alphabet observational effects and IT independent-reading observational/full A1-R1 transfer pass the frozen W1 criteria without W2 observational sign reversal.**

First reveal provenance:

- head `31746c4d318929b602b35c288e36e83001200509`
- run `33334225091`
- artifact `9738599590`
- ZIP SHA-256 `4b9448e655d539528357ee4b51de1ebdea70003730c593f49c96bdbb4a6d9324`
- raw JSON SHA-256 `77653133af22cd26141bc695a8ee6243cc3d924ba44a41a685cb148b9167db91`

See `experiments/phase63/REPORT_B.md` and `phase63b_science_results.json`.

## Phase64A — empirical-inventory autonomy: COMPLETE / MIXED

MG0 order 2 was selected by training-only CV in all ZL/IT folds. Synthetic vocabularies retained only ~20–23% training membership and ~12–13% held-out membership, with edit1 connectivity roughly halved.

ZL ratios: **0.847 / 0.920 / 0.468**. S3 alone fails the frozen `[0.5,2]` gate. ZL H62 remains `D=0.762`, `|ΔC_short|=0.120` and wins 5/5 against N0/C0 on both diagnostics.

IT ratios: **1.136 / 0.976 / 0.586**, all pass. IT H62 `D=0.832`, `|ΔC_short|=0.0749`; full arm passes.

Frozen classification: **INCONSISTENT / PRIMARY FAILURE**. Do not repair S3 after reveal. The important retained result is that explicit empirical inventory membership is not required for the core prospective recurrence geometry under tested MG0.

## 🟡 Phase64B — serious bounded C1 fairness gate

### Question

> Can a materially stronger, independently motivated meaningful-text + cipher/shorthand mechanism rival A1 on held-out entry/locality and H62 recurrence geometry without importing A1's previous-10 process or Voynich-specific boundary tuning?

### Why now

Phase64A makes A2 repair low-value and family fairness high-value. C0 was intentionally weak. A developed G candidate cannot support `G > C` at family level until C receives a serious, complexity-charged challenge.

### Freeze requirements

1. plaintext corpus/source rule fixed independently of Voynich outcomes;
2. historically or mathematically motivated encoding/shorthand operations;
3. no Voynich-specific paragraph/section rules unless explicitly charged;
4. nested training-only model selection;
5. explicit complexity/dependence ledger;
6. same held-out S1/S2/S3 and H62 scorecard;
7. at least one prospective discriminator frozen before C1 output is seen;
8. no copying of A1's explicit previous-10 local-family mechanism under a cipher label.

Content relation remains essential but mapping-prerequisite limited.

## Later model-family work

### G family

Do **not** add A2 merely to repair known B4/B5, fold2 or line-profile residuals. The next G challenge is autonomy, not better fit.

### C family

C0 is useful but insufficient. C1 is legitimate only as a separately frozen historically/mathematically motivated model with explicit complexity cost. It should receive enough model-development budget to make the N/C/G comparison scientifically fair.

### N/content lane

Simple N0 is disfavored, not all meaningful-text families. Strong semantic promotion still requires independently grounded object/paragraph mapping and unseen content prediction.

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
- **M5 independent transcription robustness:** ✅ Phase63B strong replication.
- **M6 mechanism autonomy:** ✅ Phase64A mixed — strict full autonomy not supported; core H62 survives inventory removal.
- **M7 fair strong C competitor:** 🟡 Phase64B/C1 current.
- **M8 content relation:** ⛔ not established.
- **M9 decipherment threshold:** ⛔ not reached.

## Stop / pivot rules

Pause or pivot rather than endlessly repair when:

1. a candidate needs a new mechanism after each failed frozen test;
2. gains disappear under training-only, independent-source or autonomy constraints;
3. results collapse under physical-leaf/manuscript/transcription holdout;
4. semantic interpretation requires post-hoc labels or free exceptions;
5. a simpler competing architecture obtains comparable prospective fit at materially lower target dependence/complexity;
6. family-level conclusions are being drawn against materially underdeveloped competitors.

## What to do when asked simply to "continue"

1. finish Phase64A replay/result integration if not yet on main;
2. freeze **Phase64B/C1** source family, operations, complexity ledger and falsification criteria before any C1 output is computed;
3. do not repair A1-R2 S3 or add A2;
4. give C1 materially more representational power than C0, but do not smuggle in Voynich-specific boundary/locality rules;
5. preserve the content bridge as the later semantic gate.
