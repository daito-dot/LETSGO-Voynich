# Current research status

For sequencing and the active gate, see `../ROADMAP.md`. Phase-specific plans/results control exact methods and historical numerical results; this file controls current accepted interpretation.

Before changing Phase60/61 claims, read:

- `REPRODUCIBILITY_AUDIT.md`
- `AUDIT_PHASE51_61C_20260830.md`

A later audit may narrow interpretation without rewriting a frozen historical result. Missing historical source or exact replay is reproducibility debt, not evidence that a result is false.

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and a manuscript-wide short-lived paragraph-entry formal role.

The first N/C/G mechanism-family tournament has now produced **genuine prospective structural evidence** for the frozen A1 generator mechanism relative to the tested N0/C0 baselines. This does not establish semantic emptiness, historical production method, or decipherment.

Current family state:

- **N:** simple source-native structured medieval N0 is disfavored on the joint exposed scorecard and on H62-P1; broader meaningful-text families remain open.
- **C:** simple reversible boundary-blind C0 materially improves N0 on exposed structure but performs poorly on H62-P1; broader cipher/shorthand families remain open only as separately specified, complexity-charged models.
- **G:** frozen A1 is the **leading tested structural mechanism and now has prospective support**, but remains strongly target-dependent and historically/semantically ungrounded.
- **M:** deferred; no mixed mechanism is justified before simpler-family robustness tests are completed.

Structural fit is not decipherment.

## Robust structural state

The audited hierarchy remains:

`broad document constraints`

`+ page-local token-family activation`

`+ manuscript-wide short-lived paragraph-entry register`

`+ line-position grammar`

`+ token morphology / edge-pattern / {k,t}-related dimensions`

Phase60 establishes that paragraph entry is genuine and transferable but not a persistent line0 initializer of later body state. Phase59 development evidence supports broad overlap with medieval entry/register grammar plus a Voynich-specific specialization.

Current page-level content tests remain negative; independently localized semantic testing remains blocked pending defensible external mapping.

## Reproducibility guardrails through Phase61

### Phase60

- **60A:** real paragraph boundaries exceed internal pseudo-boundaries under physical-leaf cross-fitting.
- **60B:** high-level signed association survives audit, but the exact historical `n=380` eligibility and fine carrier contribution magnitudes are not replay-certified. The public reimplementation is not the exact old cross-fit procedure.
- **60C:** a section-blind structural entry/body role transfers across held-out H/B/P/S/T.
- **60D2/60E:** persistent initialization is not supported. Public Phase60E code remains provenance debt; frozen result JSON controls the historical numerical conclusion.

Strongest retained entry statement:

> Voynich paragraph starts instantiate a manuscript-wide, transferable formal entry register. It is partly comparable to medieval structured-document entry grammar and partly Voynich-specific, but its detectable influence is short-lived rather than a persistent paragraph initializer.

### Phase61A/B

A0 demonstrates that explicit boundary awareness can reproduce the scalar entry direction, but its strength search was exposed. A0 fails the joint scorecard because locality is far too weak and positional/entry effects are mis-scaled. Exact historical A0 executable provenance remains incomplete.

### Phase61C — A1 narrow scalar gate

A1 adds one bounded local-family reuse/one-edit mechanism from line1 onward. Frozen held-out ratios:

- entry projection **0.797**
- local-prev10 **0.717**
- aggregate line-position eta2 mean **1.116**

All pass the preregistered `[0.5,2.0]` gate. A training-vocabulary-only sensitivity gives approximately `0.795 / 0.718 / 1.098`, with unchanged selected parameters.

But the independent audit shows aggregate line-position eta2 masks coordinate-level mismatch: near-family eta2 coordinates are about 6× Voynich while the aggregate excluding them is about 0.64×.

Retain:

> A1 reaches the broad held-out regime for the frozen scalar entry projection, global local-prev10 and aggregate line-position eta2 mean.

Do not claim:

> A1 reproduces the full Voynich multivariate line-position grammar/profile.

## Phase62 — first fair N/C/G tournament

### Phase62A — pre-result freeze

Pinned inputs:

- ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1` via `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`;
- CREMMA `292525969ad98380b398e6606a9c2a36d51913ae`.

Objective equal-weight N0 panel:

- BIS193
- CLM13027
- Mazarine915
- UBL758

Common exposed scorecard:

- **S1** generic fixed-five 8D entry-minus-pseudo projection;
- **S2** full-line previous-10 near-family excess above a vocabulary/layout-preserving null;
- **S3** generic fixed-five 8D line-position eta2 mean.

The bounded C0 family and H62-P1 prospective recurrence-distance profile were frozen before outcomes.

### Phase62B — N0 fails joint gate

N0/Voynich:

- S1 **-0.980**
- S2 **0.133**
- S3 **0.989**

All primary manuscripts are negative on S1. S2 failure survives manuscript omissions. S3 essentially matches, downgrading generic aggregate line-position structure as standalone evidence.

### Phase62C — C0 improves N0 but remains insufficient

All five folds select non-overlapping digraph coding using training targets only.

C0/Voynich:

- S1 **-0.932**
- S2 **0.249**
- S3 **0.856**

C0 improves held-out joint MSE in 5/5 folds and passes the frozen manuscript-omission stability rule. Therefore simple reversible boundary-blind recoding has material explanatory value, but it does not solve the key S1/S2 residual.

### Phase62C — frozen A1 leads exposed scalar fit

Without retuning, A1/Voynich common-score ratio-of-means:

- S1 **0.623**
- S2 **1.512**
- S3 **0.587**

All pass the frozen exposed gate. This is an aggregate pass with fold heterogeneity, and the Phase61 coordinate-profile mismatch remains binding.

### Phase62D — ranking frozen before prospective reveal

Before H62-P1 was computed, `experiments/phase62/DECISION_D.md` committed:

> **Exposed scalar structural ranking among tested implementations: A1 > C0 > N0.**

but kept:

> **Overall N/C/G mechanism-family conclusion: unresolved pending prospective validation.**

The same pre-result decision recorded A1's mechanistic H62-P1 prediction: its direct 10-token local-family memory should produce stronger near-family recurrence concentration in distances 1–10 relative to 11–40, without requiring a literal cutoff to zero after 10.

## Phase62P — H62-P1: PROSPECTIVE SUPPORT FOR A1

H62-P1 was frozen before the tournament result and implemented only after Phase62D was merged.

Five distance bins:

- 1–2
- 3–5
- 6–10
- 11–20
- 21–40 tokens

Within-item token-order permutation nulls yield a signed recurrence-excess vector. Frozen diagnostics:

1. `D_profile`: L1 distance to the held-out Voynich normalized five-bin profile;
2. absolute `C_short` difference for signed excess concentration in the first three bins (1–10 tokens).

### Prospective result

| candidate | mean D_profile | median D_profile | D wins | mean |ΔC_short| | C wins |
|---|---:|---:|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0/5 | 0.63750 | 0/5 |
| C0 | 1.85866 | 1.87201 | 0/5 | 1.30765 | 0/5 |
| **A1** | **0.76259** | **0.81061** | **5/5** | **0.11615** | **5/5** |

A1 satisfies every preregistered prospective-leader condition and uniquely wins both diagnostics in every held-out physical-leaf fold.

The first prospective raw JSON was produced by GitHub Actions run `33314854583`, artifact `9733130140`; raw JSON SHA-256:

`0e1b687ab73efbc494834f49398ed474230f47bcde4cf4dbcaa46631efd75264`

A second unchanged scientific run required exact digest equality before persisting `phase62p_h62p1_results.json`; the check passed.

Accepted promotion:

> **The frozen A1 mechanism predicts a previously sealed distance-dependent near-family recurrence geometry substantially better than the tested N0 and C0 baselines, with 5/5 fold wins on both preregistered diagnostics. A1 is therefore the leading tested structural mechanism with genuine prospective support.**

This is the strongest mechanism evidence in the project so far.

### Limits that remain binding

Do not infer that:

- Voynich is meaningless;
- A1 is the historical production algorithm;
- semantic information is absent;
- every meaningful-text/cipher model is rejected;
- A1 reproduces the exact five-bin profile or full line-position grammar.

A1 `D_profile` remains about `0.54–1.01` across folds, so the fit is materially imperfect. Longer-range B4/B5 behavior differs in some folds.

Most importantly, A1 still receives substantial Voynich-derived assistance:

- explicit paragraph-entry mechanism;
- explicit local-family mechanism;
- maximum direct local memory of 10 tokens;
- parameters selected on Voynich training folds;
- empirical Voynich vocabulary of 8,295 token types;
- no independently meaningful plaintext or historical construction model.

## Current frontier — Phase63A target-dependence robustness

The next question is not how to repair A1's remaining mismatch. It is whether the existing prospective advantage survives **less access to the target manuscript**.

Primary robustness challenge:

> regenerate each held-out fold using only token types observed on that fold's training leaves, with the exact existing A1 parameters/seeds and no retuning, then re-evaluate both S1–S3 and H62-P1.

A1-R1 should be called robust only if:

- S1/S2/S3 ratio-of-means still pass the historical `[0.5,2.0]` gate;
- H62-P1 mean `D_profile` remains below N0 and C0;
- mean absolute `C_short` difference remains below N0 and C0;
- A1-R1 beats both baselines on both H62-P1 metrics in at least 3/5 folds.

Degradation relative to full-vocabulary A1 is reported directly, not tuned away.

After Phase63A, the highest-priority external replication is an independent Voynich transcription lineage.

No A2, C1 or M0 should be introduced before this robustness challenge is recorded.

## Important corrections retained

- Phase3 plant-label semantic result: not supported.
- Phase53/54 recto/verso collapse corrected in Phase55.
- Phase56 unmatched full-page PC1 sample-size contamination withdrawn.
- Phase60B exact historical eligibility/carrier magnitudes not replay-certified.
- Phase60D persistent-initialization evidence was coupled and superseded by 60D2/60E; clean 60E replay remains debt.
- Phase61A is not prospective validation of a preselected A0 strength.
- Phase61C aggregate S3 does not establish full profile reproduction.
- Phase59 small semantic subsets are development evidence; Phase62 uses an objective reproducible control panel.

## Methodological rules

- Observation → Structure → Mechanism → Content relation → Decipherment.
- Preserve known structure in nulls.
- Distinguish exploratory, exposed/model-selection, held-out, prospective and external-replication evidence.
- Page-side and physical leaf are distinct units.
- Search freedom belongs inside training/model-selection folds.
- Local state is a default confound.
- Negative results and audit corrections remain public.
- Do not rescue failed architectures silently; name and charge each extension.
- Reduce target dependence before adding mechanisms when a candidate gains support.
- Prefer profile-aware checks when scalar averages can hide cancellation.
- Decipherment requires an executable fixed mapping/generation rule, substantial unseen prediction, interpretable fixed output, strong competitors/nulls, prospective/external replication and explicit accounting of failures/exceptions.