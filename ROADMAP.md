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
5. independently grounded content prediction before any semantic promotion.

Families remain:

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
| Phases 53–57 | ✅ | audits corrected page/leaf/sample-size issues and narrowed a robust residual opportunity |
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
| **Phase 62P / H62-P1** | **✅ prospective A1 support** | frozen A1 wins both preregistered recurrence-profile diagnostics in **5/5 physical-leaf folds** |
| **Phase 63A** | **🟡 current** | remove the strongest remaining target convenience: re-test A1 with **training-leaf-only output vocabulary** and no retuning |
| Phase 63B | ⏭ | independent Voynich transcription-lineage replication of strongest Phase60–62 claims |
| Phase 64 | ⏭ | only after robustness: decide whether to invest in a more expressive C1, a more autonomous G model, or an independently grounded content lane |

## Completed Phase62 tournament

### N0 — meaningful structured medieval plaintext

Across-fold ratios to held-out Voynich:

- S1 entry specialization: **-0.980**
- S2 near-family locality excess: **0.133**
- S3 aggregate generic line-position eta2: **0.989**

N0 is not jointly competitive. Its S3 match shows that generic line-position structure is weak evidence by itself.

### C0 — bounded reversible boundary-blind recoding

All five folds selected non-overlapping digraph coding using training targets only.

C0/Voynich:

- S1 **-0.932**
- S2 **0.249**
- S3 **0.856**

C0 materially improves N0 under the frozen fold/manuscript-omission rule, but remains insufficient on S1/S2. The broader C family is not falsified; any stronger cipher/shorthand is a separately named and complexity-charged C1.

### A1 — frozen boundary-aware + local-family generator

No Phase62 retuning.

Common-score A1/Voynich ratio-of-means:

- S1 **0.623**
- S2 **1.512**
- S3 **0.587**

All pass the frozen exposed common-score gate. The independent Phase61 audit still limits the claim: aggregate S3 hides coordinate-level mismatch, and several individual fold/target ratios lie outside the broad interval.

### Phase62D — ranking frozen before prospective reveal

Before H62-P1 was computed, the repository committed:

> **Exposed scalar structural fit: A1 > C0 > N0.**

and separately:

> **Overall N/C/G mechanism-family conclusion: unresolved pending prospective validation.**

The same decision commit preregistered the directional A1 prediction: because A1 directly selects local-family variants from at most the preceding 10 tokens, near-family excess should be more concentrated in 1–10 than 11–40 tokens. This was explicitly not a prediction of literal zero after token 10.

## Completed H62-P1 — first sealed prospective discriminator

The five-bin statistic was frozen in Phase62A:

- B1 1–2 tokens
- B2 3–5
- B3 6–10
- B4 11–20
- B5 21–40

Within-item permutation nulls remove recurrence expected from the same item vocabulary/multiset. Two primary diagnostics were frozen: normalized profile L1 distance `D_profile` and absolute short-range concentration difference `|ΔC_short|`.

### Result

| candidate | mean D_profile | median D_profile | D wins | mean |ΔC_short| | C wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

A1 satisfies every frozen prospective-leader condition and uniquely wins both diagnostics in every held-out physical-leaf fold.

This is materially stronger evidence than another exposed-statistic fit because the target, interpretation, executable, aggregation, missing-bin rule and victory rule all existed in Git history before the first result.

See:

- `experiments/phase62/DECISION_D.md`
- `experiments/phase62/IMPLEMENTATION_P.md`
- `experiments/phase62/phase62p_h62p1.py`
- `experiments/phase62/phase62p_h62p1_results.json`
- `experiments/phase62/REPORT_P.md`

### What is promoted

Promote A1 from:

> provisional leading exposed-score structural candidate

to:

> **leading tested structural mechanism with genuine prospective support relative to N0/C0.**

### What is not promoted

Do not infer that:

- Voynich is meaningless;
- A1 is the historical production algorithm;
- semantics are absent;
- all meaningful-text/cipher families are rejected;
- A1 reproduces the full structural profile.

A1's five-bin profiles remain imperfect (`D_profile` about 0.54–1.01), and its longer-range B4/B5 behavior differs from Voynich in some folds.

## 🟡 Current gate — Phase63A: target-dependence reduction

The strongest remaining methodological objection to A1 is that it is supplied the empirical Voynich token vocabulary. Phase61C already showed that restricting the vocabulary to training leaves barely changes the exposed scalar gate, but **H62-P1 has not yet been challenged under that restriction**.

### Question

> Does A1's prospective H62-P1 advantage survive when every held-out fold can generate only token types observed on its training leaves?

### Intended frozen test

For each existing physical-leaf fold:

1. construct A1 vocabulary from training leaves only;
2. learn shape scores and edit1 neighbor graph from training-side information only;
3. retain the exact already-frozen A1 entry-strength/local-family-p pair — no retuning;
4. retain the exact held-out layout and deterministic seeds;
5. evaluate both:
   - Phase62 exposed S1/S2/S3;
   - the now-known H62-P1 five-bin profile;
6. report held-out token-type/occurrence coverage lost by the training-only vocabulary.

### Phase63A survival rule to freeze before execution

A1-R1 should count as robust only if, without parameter repair:

- S1/S2/S3 ratio-of-means still satisfy the historical `[0.5,2.0]` common-score gate;
- its H62-P1 mean profile distance remains lower than both N0 and C0;
- its mean absolute `C_short` difference remains lower than both N0 and C0;
- it beats both N0 and C0 in at least 3/5 folds on each H62-P1 metric.

No requirement that it beat the full-vocabulary A1 is imposed; degradation relative to full A1 is reported directly as target-dependence cost.

### Stop rule

If training-only vocabulary destroys the prospective advantage, record that before proposing a more autonomous G model. Do not silently restore full-vocabulary information or add an A2 mechanism.

## ⏭ Phase63B — independent transcription lineage

After Phase63A, replicate the strongest claims under an independently maintained Voynich transcription/segmentation lineage where technically defensible:

1. paragraph-entry boundary effect;
2. local near-family activation;
3. H62-P1 recurrence-distance geometry;
4. the frozen A1 robustness result.

Representation differences must be specified before comparing outcomes. Do not tune one transcription to mimic ZL3b.

## Other tracks

### C family

C0 is informative but weak. Do not build C1 merely because C0 lost. A historically motivated C1 becomes appropriate only after the current robustness challenge, with bounded rules and explicit complexity cost.

### G family

Do not build A2 to improve the known long-range/profile residual. If Phase63A passes, the next G question is **autonomy**: can the relevant token inventory/morphology itself be learned or generated without supplying the manuscript's empirical output vocabulary?

### Content lane

Page-level visual tests remain negative. Strong semantic promotion still requires externally grounded object/paragraph mapping and unseen content prediction.

### Reproducibility debt

Retain and eventually close:

- exact historical Phase60B eligibility/carrier replay;
- clean Phase60E executable replay;
- exact historical A0 provenance where recoverable.

These debts do not supersede the current prospective result but limit over-precise historical claims.

## Decision milestones

- **M1 Phase61 architecture gate:** ✅ A0 fails jointly; A1 survives narrow scalar gate.
- **M2 first fair exposed N/C/G tournament:** ✅ `A1 > C0 > N0` among tested implementations.
- **M3 prospective discriminator:** ✅ A1 wins H62-P1 5/5 on both frozen metrics.
- **M4 target-dependence robustness:** 🟡 Phase63A current.
- **M5 independent transcription/external robustness:** ⏭.
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

Execute **Phase63A**. Freeze its exact training-only-vocabulary implementation and survival rule before running it. Do not create A2/C1/M0 first.