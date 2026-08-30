# Current research status

For sequencing and the active gate, see `../ROADMAP.md`. Phase-specific plans/results control exact methods and historical numerical results; this file controls current accepted interpretation.

Before changing Phase60/61 claims, read:

- `REPRODUCIBILITY_AUDIT.md`
- `AUDIT_PHASE51_61C_20260830.md`

A later audit may narrow interpretation without rewriting a frozen historical result. Missing historical source or exact replay is reproducibility debt, not evidence that a result is false.

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and a manuscript-wide short-lived paragraph-entry formal role.

The Phase62/63 mechanism tournament now provides two stronger layers beyond exploratory fit:

1. **sealed prospective support** for the frozen A1 local-family mechanism on previously unseen recurrence-distance geometry;
2. **target-dependence robustness** showing that this advantage survives removal of token types unique to held-out physical leaves.

Current family state:

- **N:** simple source-native structured medieval N0 is disfavored on joint exposed and prospective recurrence geometry; broader meaningful-text families remain open.
- **C:** simple reversible boundary-blind C0 materially improves N0 on exposed structure but is insufficient on S1/S2 and poor on H62-P1; broader cipher/shorthand families remain open only as separately specified, complexity-charged models.
- **G:** A1 is the **leading tested structural mechanism with genuine prospective support**, and Phase63A shows that support is not explained by access to held-out-only token types. A1 remains training-manuscript-dependent, historically/semantically ungrounded and structurally imperfect.
- **M:** deferred pending simpler-family robustness.

Structural fit is not decipherment.

## Robust structural state through Phase60

Retain:

> Voynich paragraph starts instantiate a manuscript-wide, transferable formal entry register. It is partly comparable to medieval structured-document entry grammar and partly Voynich-specific, but its detectable influence is short-lived rather than a persistent paragraph initializer.

Audit qualifications:

- Phase60A genuine boundary effect survives physical-leaf cross-fitting.
- Phase60B high-level signed carrier associations survive audit, but exact historical `n=380` eligibility/fine contribution magnitudes are not replay-certified.
- Phase60C section-blind entry/body role transfers across H/B/P/S/T.
- Persistent line0 initialization is not supported by 60D2/60E; clean public 60E replay remains debt.

Current page-level content tests remain negative; independently localized semantic testing remains blocked pending defensible external mapping.

## Phase61 — A1 architecture state

A0 demonstrates that boundary-conditioned generation can hit the scalar entry direction but fails jointly. A1 adds one bounded local-family reuse/one-edit mechanism from line1 onward.

Frozen Phase61C held-out ratios:

- entry projection **0.797**
- local-prev10 **0.717**
- aggregate line-position eta2 **1.116**

A training-vocabulary-only sensitivity gives approximately `0.795 / 0.718 / 1.098` with unchanged parameters.

However, aggregate line-position eta2 masks coordinate-level mismatch: near-family eta2 coordinates are about 6× Voynich while the aggregate excluding them is about 0.64×.

Retain only:

> A1 reaches the broad held-out regime for the frozen scalar entry projection, global local-prev10 and aggregate line-position eta2 mean.

Do not claim A1 reproduces the full multivariate line-position profile.

## Phase62 — first fair N/C/G tournament

### N0

Objective equal-weight medieval panel (BIS193, CLM13027, Mazarine915, UBL758):

- S1 **-0.980×** Voynich
- S2 **0.133×**
- S3 **0.989×**

N0 fails the joint gate. Its S3 match shows that generic aggregate line-position structure is weak discrimination by itself.

### C0

Five frozen reversible boundary-blind transforms; all five folds select non-overlapping digraph coding using training targets only.

- S1 **-0.932×**
- S2 **0.249×**
- S3 **0.856×**

C0 materially improves N0 under the frozen rule but remains insufficient on S1/S2.

### Frozen A1 on common exposed scorecard

Without retuning:

- S1 **0.623×**
- S2 **1.512×**
- S3 **0.587×**

All pass the frozen ratio-of-means interval, with fold heterogeneity and the Phase61 profile mismatch retained.

### Phase62D pre-prospective freeze

Before H62-P1 was computed, the repository committed:

> **Exposed scalar structural ranking among tested implementations: A1 > C0 > N0.**

and separately:

> **Overall N/C/G mechanism-family conclusion: unresolved pending prospective validation.**

The same decision committed A1's directional prediction: its explicit maximum 10-token direct local-family memory should produce stronger near-family recurrence concentration in 1–10 than 11–40 tokens, without requiring a literal zero after 10.

## Phase62P — H62-P1: GENUINE PROSPECTIVE SUPPORT FOR A1

H62-P1 was frozen in Phase62A before tournament outcomes and implemented only after Phase62D was merged.

Five preceding-token distance bins:

- 1–2
- 3–5
- 6–10
- 11–20
- 21–40

Within-item token-order permutation nulls yield signed recurrence-excess profiles. Frozen diagnostics:

1. `D_profile` — L1 distance to held-out Voynich normalized five-bin profile;
2. absolute `C_short` difference — mismatch in signed 1–10 concentration.

| candidate | mean D_profile | median D_profile | D wins | mean |ΔC_short| | C wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

A1 satisfies every preregistered prospective-leader condition and uniquely wins both metrics in all five physical-leaf folds.

Accepted promotion:

> **The frozen A1 mechanism predicts a previously sealed distance-dependent near-family recurrence geometry substantially better than tested N0/C0. A1 is the leading tested structural mechanism with genuine prospective support.**

Limits remain: A1 is not the historical generator, not evidence of semantic emptiness, and does not exactly reproduce the full five-bin/profile or line-position geometry.

## Phase63A — training-only vocabulary robustness: PASSES

Phase63A removes all token types absent from each fold's training leaves. It does not add a mechanism or retune A1.

### Intervention strength

Across folds:

- full vocabulary: 8,295 types;
- mean training vocabulary: **7,050.2**;
- mean held-out distinct-type coverage by training vocabulary: **0.5083**;
- mean held-out token-occurrence coverage: **0.8016**.

Thus nearly half of held-out distinct types and about one fifth of held-out token occurrences correspond to types unavailable to A1-R1.

Generation audit confirms zero generated types outside the training vocabulary.

### Exposed score retention

A1-R1 / Voynich ratio-of-means:

- S1 **0.65353**
- S2 **1.51061**
- S3 **0.58264**

All retain the historical `[0.5,2.0]` aggregate gate.

### H62-P1 retention

A1-R1:

- mean `D_profile` **0.76660**
- median `D_profile` **0.80945**
- mean `|ΔC_short|` **0.11769**

It beats N0 and C0 **5/5 folds on both metrics**.

Relative to full-vocabulary A1:

- mean `D_profile` changes only `+0.00401`;
- median `D_profile` `-0.00116`;
- mean `|ΔC_short|` `+0.00153`.

All frozen R1/R2/R3 conditions pass.

Accepted interpretation:

> **A1's exposed and prospective structural advantage does not depend on access to token types unique to the held-out physical leaves.**

This materially reduces the manuscript-wide empirical-vocabulary leakage objection. It does not eliminate target dependence: A1 still uses Voynich training-side vocabulary/morphology, exposed-Voynich-derived architecture, frozen Voynich-selected parameters, explicit boundaries/memory and true held-out layout/token counts.

### Replay audit

First scientific run:

- Actions run `33315453851`
- artifact `9733309531`
- raw JSON SHA-256 `bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7`

A raw-byte replay mismatch was investigated before acceptance. First vs clean replay parsed JSON differ only in 16 S1 floating scalars at maximum absolute `2.22e-16`; all S2/S3/H62-P1/discrete fields and all verdicts are identical. Canonical 14-decimal semantic SHA:

`cd53f47729c864badb5e8c747cfd9ad989de9c616ca54dd5bdcb83b075c33c74`

Therefore the scientific verdict is replay-stable to machine precision; raw cross-CPU JSON bytes are not guaranteed identical. See `experiments/phase63/DETERMINISM_AUDIT_A.md`.

## Current frontier — Phase63B independent transcription replication

The highest-value remaining robustness question is now **transcription/segmentation dependence**.

Before computing any replication result:

1. identify a genuinely independent Voynich transcription lineage with stable provenance/version/hash;
2. document glyph/token/space/paragraph conventions relative to ZL3b;
3. freeze a deterministic page/leaf/line/paragraph mapping without tuning against prior results;
4. freeze which metrics remain representation-comparable;
5. freeze any normalization/character treatment before seeing outcomes.

Priority replication targets:

1. genuine paragraph-entry specialization versus internal pseudo-boundaries;
2. local near-family recurrence geometry;
3. H62-P1 short-vs-long profile shape;
4. A1-R1 advantage if the independent representation permits a defensible generator/neighbor construction;
5. aggregate line-position eta2 only as secondary evidence.

If a result depends materially on ZL3b conventions, record that before adapting the metric.

## Current interpretation limits

Do **not** infer:

- Voynich is meaningless;
- semantic information is absent;
- A1 is the historical production algorithm;
- all meaningful/cipher models are rejected;
- the manuscript is deciphered.

The mechanism evidence is now strong enough to demand harder independence tests, not stronger semantic language.

## Methodological rules

- Observation → Structure → Mechanism → Content relation → Decipherment.
- Preserve relevant known structure in nulls.
- Distinguish exploratory, model-selection, held-out, prospective and external-replication evidence.
- Search freedom belongs inside training/model-selection folds.
- Negative results and audit corrections remain public.
- Do not rescue failed architectures silently; name and charge each extension.
- Reduce target dependence before adding mechanisms when a candidate gains support.
- Prefer profile-aware checks when scalar averages can hide cancellation.
- Decipherment requires an executable fixed mapping/generation rule, substantial unseen prediction, interpretable output, strong competitors/nulls, prospective/external replication, independently grounded content relation and explicit accounting of failures/exceptions.