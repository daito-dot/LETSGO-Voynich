# Current research status

For progress sequencing and the active decision gate, see `../ROADMAP.md`. Phase-specific plans/results control exact methods and numbers; this file controls current accepted interpretation.

For implementation/replay caveats through Phase61C, also read `REPRODUCIBILITY_AUDIT.md` and `AUDIT_PHASE51_61C_20260830.md` before changing any Phase60/61 numerical interpretation.

## Accepted high-level state

Voynichese has strong internal grammar, positional structure, document-role effects, page-local token-family organization, and a manuscript-wide paragraph-entry formal role. What is not established is whether these structures encode independently grounded semantic content, arise from cipher/shorthand mechanics, or can be reproduced most efficiently by a hierarchical nonsemantic generator.

Structural equivalence is not cipher equivalence. Structural fit is not decipherment.

Current mechanism families remain open:

- **N** — meaningful structured natural/technical text;
- **C** — meaningful structured text plus bounded cipher/shorthand/obscuration;
- **G** — constrained nonsemantic/formal generation;
- **M** — mixed mechanisms, deferred until simpler families have fixed failure patterns.

## Robust structural state through Phase 57

The audited hierarchy remains:

`broad document constraints`

`+ page-local token-family activation`

`+ paragraph-entry/body transition`

`+ line-position grammar`

`+ token morphology / edge-pattern / {k,t}-related dimensions`

Physical locality survives exact section+Currier+hand matching but is not one smooth drift. Matched-token variation is moderately low-dimensional. Phase57 promoted only the leading approximately two-dimensional residual subspace; higher residual axes remain representation/scale-sensitive.

## Phase 58 — content relation remains unestablished

Independently defined page-level visual properties in Biological/balneological and early Herbal-A domains did not associate significantly with the promoted 2D residual. A defensible paragraph-to-illustrated-subobject mapping was unavailable without post-hoc pairing.

Current page-level visual semantic tests are therefore negative; strong localized semantic testing remains blocked rather than guessed.

## Phase 59 — medieval entry decomposition

Source-native medieval Latin item/section entries reproduce part of the broader Voynich paragraph-entry transition. In the Phase59 development representation, an external rank-2 medieval-entry basis learned without Voynich explained about 65% of Voynich transition energy, while a Latin-orthogonal Voynich component remained positive across H/B/P/S/T.

Retain:

`generic medieval entry/register grammar + Voynich-specific specialization`

Phase62 later shows that this broad overlap does **not** mean objective source-native structured Latin reproduces the stricter common held-out Voynich entry direction.

## Phase 60 — paragraph entry is real, transferable and short-lived

- **60A:** real paragraph boundaries exceed internal pseudo-boundaries under physical-leaf cross-fitting.
- **60B:** the transition is consistently associated with lower TTR/shorter-token structure together with increased edit1/local-near-family and k/t-related structure. An independent audit found the current public reimplementation's final pooled-direction calculation is not a true cross-fit replay; corrected fold-specific training directions leave all five folds positive, but the historical accepted `n=380` eligibility rule is still unrecovered. Therefore exact Phase60B contribution magnitudes and fine carrier ranking are not replay-certified.
- **60C:** a section-blind structural entry/body role transfers across held-out H/B/P/S/T.
- **60D/60D2/60E:** persistent line0 initialization is not supported after coupling-free prospective testing. The current public 60E `.py` file is only a provenance stub; frozen JSON remains numerical authority pending exact clean replay.

Strongest retained statement:

> Voynich paragraph starts instantiate a manuscript-wide, transferable formal entry register. It is partly comparable to medieval structured-document entry grammar and partly Voynich-specific, but its detectable influence is short-lived rather than a persistent paragraph initializer.

The frozen Phase50 stationary/weak-context DSL also fails the entry-specific direction; explicit boundary-conditioned machinery is needed for that generator family. The original full Phase51 historical generator source has now been recovered and archived as provenance, while the public Phase51 entrypoint remains a normalized parameter/provenance stub.

## Phase 61 — nonsemantic architecture discrimination

### 61A — A0 narrow entry gate: SURVIVES

A boundary-aware short-lived paragraph-line0 mixture can reproduce the scalar held-out entry-direction target without persistent paragraph state.

Interpret this as a **narrow architecture/mechanism demonstration**. The exposed strength grid was evaluated before strength 1.5 was fixed for the first 61B joint diagnostic, so 61A is not prospective validation of a preselected strength-1.5 model.

### 61B — A0 joint scorecard: FAILS

A0 produces far too little local-prev10 near-family activation while overproducing line-position and entry/pseudo effects. Its high edit1 density is non-independent because the empirical Voynich vocabulary is supplied.

The exact historical A0 executable was not preserved, so `phase61b_results.json` remains accepted numerical authority rather than a fully replay-certified generator run. Phase61C independently reproduces the Voynich-side metric regime closely; this supports metric continuity but does not reconstruct the missing A0 run.

### 61C — A1 first joint gate: SURVIVES

A1 adds exactly one bounded local-family reuse/one-edit mechanism from line1 onward. No persistent paragraph state, section-specific grammar or extra line-position rule was allowed.

Held-out A1/Voynich ratios on the **frozen aggregate Phase61 scorecard**:

| target | ratio |
|---|---:|
| entry projection | **0.797** |
| local-prev10 | **0.717** |
| line-position eta2 mean | **1.116** |

All pass the frozen `[0.5,2.0]` broad-regime gate. Independent review verifies the plan → implementation freeze → executable → held-out result chronology and confirms training-only feature scaling, direction learning and parameter selection.

A stricter sensitivity that removed every held-out-only token type from the generator produced essentially unchanged ratios (`0.795`, `0.718`, `1.098`) and exactly the same selected parameter pairs. Full-manuscript vocabulary sharing is therefore not driving the first-gate survival decision.

However, a post-hoc held-out decomposition shows the aggregate line-position eta2 mean hides substantial coordinate mismatch: near-family eta2 coordinates are overproduced by about 6x while the aggregate excluding those coordinates is about 0.64x Voynich. This diagnostic was not preregistered and does not retroactively fail 61C, but it constrains the claim.

Retain:

> A minimally extended boundary-aware nonsemantic generator remains structurally viable after paying for one additional local-family mechanism: it reaches the broad held-out regime for the frozen scalar entry projection, global local-prev10 level, and aggregate line-position eta2 mean.

Do **not** strengthen that to:

> A1 reproduces the full Voynich multivariate line-position grammar/profile.

This is not evidence that Voynich is meaningless. A1 remains historically/semantically ungrounded and pays explicit target-derived vocabulary/architecture costs.

## Phase 62 — first fair N/C/G tournament

Phase62 freezes a cross-representation common scorecard, objective medieval source panel, bounded reversible C0 family, complexity/dependence ledger, and a sealed genuinely prospective discriminator before comparing model families.

Primary common exposed scorecard:

- **S1** — sample-size-neutral generic 8D entry-minus-pseudo projection learned from Voynich training leaves;
- **S2** — full-line previous-10 near-family locality excess above a document-vocabulary/line-layout preserving null;
- **S3** — generic fixed-five-token line-position eta2 mean.

Literal Voynich `{k,t}` dimensions are excluded from this primary cross-language comparison.

The Phase61C eta2 decomposition is a warning against overinterpreting scalar averages. Phase62 family ranking should preserve the frozen scorecard but carry coordinate/profile mismatch forward as a diagnostic and rely on the already-sealed prospective discriminator before claiming a winner.

### 62A — source/design freeze: COMPLETE

Pinned sources:

- Voynich mirror `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`, exact ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- CREMMA `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`.

Historical Phase59 H318/CLM/BIS item subsets were not fully recoverable and were not reconstructed by matching Voynich. A Voynich-blind corpus-wide inclusion rule selected the primary N0 panel:

- BIS193;
- CLM13027;
- Mazarine915;
- UBL758.

Manuscripts receive equal primary weight. H318 is a predeclared small sensitivity only.

The future H62-P1 five-bin near-family recurrence-distance profile was frozen and remains sealed until after Phase62D.

### 62B — N0 source-native meaningful structured text: FAILS JOINT GATE

N0 was evaluated before any C0/A1 common-score result was inspected.

Across five Voynich physical-leaf folds:

| target | held-out Voynich | N0 equal-manuscript | N0/Voynich |
|---|---:|---:|---:|
| **S1 entry-specific projection** | 0.87599 | **-0.85872** | **-0.980** |
| **S2 near-family locality excess** | 0.04388 | **0.00585** | **0.133** |
| **S3 line-position eta2 mean** | 0.02827 | **0.02797** | **0.989** |

Frozen broad-regime gate: **S1 fail, S2 fail, S3 pass**.

#### S1 interpretation

All four primary manuscripts have negative mean S1 projections under the Voynich-training-derived common 8D direction:

- BIS193: -1.389
- CLM13027: -1.420
- Mazarine915: -0.362
- UBL758: -0.264

The N0 aggregate remains negative in every Voynich outer fold and under every leave-one-manuscript-out aggregate.

Thus source-native medieval entry structure exists but does not reproduce the stricter sample-size-neutral Voynich entry specialization in the current objective panel.

#### S2 interpretation

N0 locality excess is only about **13.3%** of the held-out Voynich level. Leave-one-manuscript-out ratios remain about 0.116–0.160.

Thus ordinary meaningful structured medieval text produces some local near-family clustering, but not the Voynich magnitude after controlling each document's own vocabulary and line layout.

#### S3 interpretation

N0 essentially matches generic line-position eta2. This sharply downgrades line-position structure **alone** as Voynich-specific evidence at this resolution.

The small predeclared H318 sensitivity behaves very differently (strong positive S1, negative S2, very large S3) but has only two S1-eligible items and remains excluded from the primary result. It illustrates why favorable small semantic subsets must not be promoted post hoc.

Exact compact result: `experiments/phase62/phase62b_n0_results.json`; report: `experiments/phase62/REPORT_B.md`.

## Current frontier — Phase62C

Do not reinterpret the N0 failure as evidence for G yet.

Execute the already-frozen comparison:

1. evaluate C0-0…C0-4, the five reversible global boundary-blind transforms, with transform choice on Voynich training folds only;
2. re-score frozen Phase61C A1 on the same Phase62 common S1–S3 scorecard without retuning;
3. compare both against the recorded N0 baseline;
4. keep H62-P1 sealed;
5. do not introduce C1, A2 or M0 inside Phase62C.

After Phase62C, Phase62D must commit the exposed-score structural ranking or unresolved set **before** H62-P1 is revealed.

## Important corrections retained

- Phase3 plant-label semantic result: NOT SUPPORTED after corrected permutation test.
- Phase53/54 recto/verso collapse corrected in Phase55; universal paragraph-reset claim withdrawn.
- Phase56 unmatched full-page PC1 was contaminated by token count.
- Phase60B public reimplementation is not an exact cross-fit replay; corrected training-direction audit preserves the high-level entry effect but exact historical `n=380` effect sizes/carrier rank remain uncertified.
- Phase60D recovery-vector evidence for persistent initialization was mathematically coupled and superseded by 60D2/60E; the public 60E executable remains a provenance stub pending exact replay.
- Phase61A narrow success did not validate a preselected A0 strength; Phase61B rejected A0 jointly, while exact historical A0 numerical replay remains provenance debt.
- Phase61C survival is structural only. It is robust to training-vocabulary-only sensitivity, but its aggregate eta2 pass does not establish a full multivariate line-position profile match.
- Phase59 small semantic source subsets remain historical development evidence; Phase62 uses an independently reproducible objective source panel.

## Methodological rules

- Observation → Structure → Mechanism → Content relation → Decipherment.
- Preserve relevant known structure in nulls.
- Distinguish exploratory, model-selection, held-out, prospective and external-replication evidence.
- Page-side and physical leaf are distinct units.
- Search freedom belongs inside model-selection/null folds.
- Local state is a default confound.
- Negative results and audit corrections remain public.
- Do not rescue failed architectures silently; name and charge each extension.
- Exposed targets may train/diagnose models; sealed prospective targets remain untouched until their preregistered reveal gate.
- Decipherment requires an executable fixed mapping/generation rule, substantial unseen prediction, interpretable fixed output, strong competitors/nulls, prospective/external replication and explicit accounting of failures/exceptions.
