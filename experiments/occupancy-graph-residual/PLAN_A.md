# Issue #58C / #64 — preregistered null-residual token-construction graph

Status: **PREREGISTERED — NO #58C TARGET RESIDUAL SCORE REVEALED**

Parent: Issue #64 under umbrella Issue #58.

Base main at phase creation:

`a60603de9991582bef2bbbf0eecb401c27a3750e`

This plan must predate any #58C executable that calculates a real residual graph score.

## 1. Program-level object

Read `research/TOKEN_CONSTRUCTION_PROGRAM.md` first.

This phase studies the internal construction of **one space-delimited Voynich token** under the frozen 12-slot representation.

It is **not** sentence-level syntax, and visible spaces are not assumed to be proven natural-language word boundaries.

The decipherment-relevant architectural question is:

> **Does the manuscript contain one non-trivial token-internal construction system that a later inverse model can treat as shared, or must that inverse problem be hierarchical / multi-generator?**

## 2. Why this is a new hypothesis

Issue #58A established a broad signed 66-edge occupancy graph.

Issue #58B then asked whether the complete raw conditional graph transfers across Currier/section/line-position strata. The observed graphs were reliable and numerically similar, but the exact line-local marginal-preserving null itself generated complete-graph correlations near the same range.

Frozen #58B classifications:

- `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`
- `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

#58B first-reveal raw result SHA-256:

`45024fd1d15b2d2484ffc26657ccc8007fd6a04dc3ed1b53b243f77ba455f8a0`

The scientific blocker was therefore not low observed similarity. It was that **raw whole-graph similarity is insufficiently discriminating against lower-order line-local slot prevalence / occupancy architecture**.

#58C is generated after seeing that failure mode. It is not a repaired #58B confirmatory test.

## 3. Selection accounting

All #58A/#58B edge identities, signs, ranks and strengths are already observed.

Therefore:

- retain all `C(12,2)=66` unordered slot pairs in the primary residual graph;
- do not privilege `(3,5)`, `(8,10)`, `(8,11)`, `(10,11)` or any other historical leader;
- individual edge residuals may be emitted descriptively only after frozen graph-level classification;
- no edge subset may promote or rescue a failed primary gate.

## 4. Frozen source, parser, fold universe and strata

Reuse without alteration from #58B:

- source repository: `matthewdgreen/cipher_benchmark`;
- source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`;
- source file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`;
- required source Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`;
- parser: `experiments/issue26-music/issue26e_core.py`;
- slot grammar: same frozen 12 slots used by #55/#58A/#58B;
- primary parser ambiguity policy: `min`;
- representation sensitivity: `max`, non-promoting;
- folds: same deterministic five physical-leaf folds.

The implementation must reproduce before target scoring:

- visible tokens: `32,570`;
- parsed tokens under `min`: `25,071`;
- target group fold counts exactly as #58B.

Target groups:

- `ALL`: all successfully parsed tokens in the frozen physical-leaf universe;
- `AH`: Currier A within Herbal;
- `BH`: Currier B within Herbal;
- `BB`: section B within Currier B;
- `BS`: section S within Currier B;
- `initial`;
- `interior`;
- `final`.

The seven planned cross-stratum contrasts remain:

1. `CURRIER_H_A_vs_B`: AH vs BH;
2. `SECTION_B_vs_H`: BB vs BH;
3. `SECTION_B_vs_S`: BB vs BS;
4. `SECTION_H_vs_S`: BH vs BS;
5. `POSITION_initial_vs_interior`;
6. `POSITION_initial_vs_final`;
7. `POSITION_interior_vs_final`.

No new target stratum may be added after target reveal.

## 5. Base edge statistic

For every successfully parsed token construct the same binary occupancy vector

`B in {0,1}^12`.

For every unordered pair `(i,j)`, define

`K_other = sum(B) - B_i - B_j`.

The base edge statistic remains the #58B primary statistic:

1. within every observed `K_other=k`, form the `2 x 2` occupancy table for `(B_i,B_j)`;
2. add Jeffreys `alpha=0.5` to the four cells of each observed k table;
3. compute the Mantel-Haenszel common odds ratio;
4. map to Yule Q:

`Q = (OR_MH - 1) / (OR_MH + 1)`.

Thus every group/view has a 66-edge base vector `q` in `[-1,1]^66`.

No #58C result may switch to raw-unconditional Q as primary. Raw Q may be emitted only as a non-promoting sensitivity if prospectively implemented.

## 6. Views required for residual calibration

For each group `S` the phase requires:

- `FULL(S)`: all tokens in S;
- for each physical-leaf fold `f=0..4`, `TRAIN(S,f)`: S excluding fold f;
- for each fold f, `HELD(S,f)`: S restricted to fold f.

Reference-null calibration must be estimated separately for every:

`group x view x edge`.

This is necessary because the sampling distribution of Q changes with group support and train/held sample size.

## 7. Null generator

Reuse the exact structural null principle that exposed the #58B problem.

For each physical line and each of the 12 slots independently, relocate occupied states among the parsed-token rows of that same line, preserving:

- the exact physical lines;
- parsed-token row count per line;
- exact line x slot occupied count;
- page / Currier / section metadata attached to rows;
- physical-leaf fold;
- token-position label attached to each parsed row.

Different slots are relocated independently, destroying same-token cross-slot pairing while retaining line-local slot prevalence.

The implementation must explicitly verify line x slot marginal preservation on deterministic test draws.

## 8. Independent reference and test null ensembles

Use **2,000 null populations total**, split prospectively into two independent deterministic namespaces.

### 8.1 Reference-null ensemble

Exactly `N_ref=1,000` populations.

Seed namespace:

`Issue58C:ResidualGraph:Reference:LineSlotOccupancyShuffle:v1:<index>`

for `<index>=0..999`.

These populations are used **only to define the residual calibration** for every group/view/edge.

They do not enter confirmatory p-value numerators/denominators.

### 8.2 Test-null ensemble

Exactly `N_test=1,000` independent populations.

Seed namespace:

`Issue58C:ResidualGraph:Test:LineSlotOccupancyShuffle:v1:<index>`

for `<index>=0..999`.

These populations are transformed using the already fixed reference-null calibration and provide the confirmatory null distributions.

This split prevents the same simulated populations from both defining and validating the residual representation.

## 9. Frozen residual transform — reference empirical normal score

For one fixed group/view/edge, let the `N_ref=1000` reference-null Q values be

`r_1, ..., r_1000`.

For any candidate Q value `q` — real or test-null — define:

- `n_lt(q) = #{m: r_m < q}`;
- `n_eq(q) = #{m: r_m = q}`.

Define the reference mid-rank probability

`u(q) = [0.5 + n_lt(q) + 0.5*n_eq(q)] / (N_ref + 1)`.

Then define the residual normal score

`Z(q) = Phi^{-1}(u(q))`,

where `Phi^{-1}` is the standard-normal quantile function.

Properties / reasons for freezing this transform:

- every edge is calibrated against its own null distribution;
- no post-reveal choice of mean vs median or SD vs MAD is required;
- discrete ties are handled by the frozen mid-rank rule;
- the transform is bounded by the finite reference ensemble and cannot diverge from a tiny estimated scale;
- test-null dependence across edges is preserved and handled empirically at graph level.

No clipping, winsorization, alternative z-score, edge-specific scale floor or post-reveal normalization may replace this transform in #58C-A.

Each real group/view yields a 66-edge residual vector `z`.

Each independent test-null population yields matching transformed residual vectors using the same fixed reference ensemble.

## 10. Primary residual-existence statistic

The primary question is whether a non-null residual graph exists **before** asking whether it transfers.

For any FULL residual vector `z` define residual energy

`E(z) = sqrt(mean_e z_e^2)`

over all 66 edges.

The primary pooled statistic is

`E_ALL = E(z_FULL(ALL))`.

For each independent test-null population n compute the matching

`E_ALL_null,n`.

Primary one-sided empirical p-value:

`p_exist_ALL = [1 + #{n: E_ALL_null,n >= E_ALL_real}] / 1001`.

### 10.1 Pooled residual reliability

Using separately calibrated TRAIN/HELD residual vectors, define for each fold:

`W_ALL,f = corr(z_TRAIN(ALL,f), z_HELD(ALL,f))`.

Frozen summary:

`W_ALL = median_f W_ALL,f`, requiring at least 4 valid fold correlations.

### 10.2 Primary existence gate

Classify the pooled residual graph as **established** iff both:

1. `p_exist_ALL <= .01`;
2. `W_ALL >= .50`.

If `p_exist_ALL > .01`, the confirmatory global result is immediately:

> `NO DETECTABLE RESIDUAL GRAPH BEYOND LOWER-ORDER OCCUPANCY ARCHITECTURE`

and cross-stratum residual similarity is **not interpreted confirmatorily**.

If `p_exist_ALL <= .01` but `W_ALL < .50` or fewer than 4 fold correlations are valid, the global result is:

> `RESIDUAL TOKEN-CONSTRUCTION RESULT INCONCLUSIVE`

and cross-stratum residual similarity is not promoted.

The `.01` significance threshold and `.50` reliability threshold are frozen before reveal; `.50` intentionally reuses the #58B reliability standard rather than tuning a new threshold to #58C outcomes.

## 11. Stratum-level residual-existence eligibility

Only if the pooled existence gate passes, evaluate the seven non-ALL groups:

`AH, BH, BB, BS, initial, interior, final`.

For each group S compute real `E_S` and residual reliability `W_S` exactly as above.

For each test-null population compute all seven group residual energies and define:

`M_E,null = max_S E_S,null`.

Family-wise group existence p-value:

`p_E,maxT(S) = [1 + #{null: M_E,null >= E_S,real}] / 1001`.

A stratum has **supported residual existence** iff:

- `p_E,maxT(S) <= .01`; and
- `W_S >= .50` with at least 4 valid fold correlations.

A contrast cannot be classified as stable/modulated/different if either member lacks supported residual existence. Such a contrast is `INCONCLUSIVE_RESIDUAL_BASIS`.

Failure of one stratum-level existence gate is not evidence that the two strata are different.

## 12. Residual graph similarity

Only after the pooled existence gate passes, for every planned contrast `(S,T)` compute:

`R_Z(S,T) = corr(z_FULL(S), z_FULL(T))`

over all 66 residual edges.

Pearson is primary, matching #58B's topology-preservation target.

For every independent test-null population compute the same seven residual correlations after reference calibration, and define:

`M_R,null = max_c R_Z,null,c`.

Family-wise similarity p-value:

`p_R,maxT(c) = [1 + #{null: M_R,null >= R_Z,real,c}] / 1001`.

If a null or real residual vector has zero variance, its correlation is invalid. Invalid required real summaries make the relevant contrast inconclusive.

Spearman and cosine similarities may be emitted as non-promoting sensitivities if implemented before reveal.

## 13. Residual within-stratum reliability and directional transfer

For every group S and fold f use the separately calibrated residual vectors:

- `z_S,-f = z_TRAIN(S,f)`;
- `z_S,f = z_HELD(S,f)`.

Within-stratum residual reliability:

`W_S,f = corr(z_S,-f, z_S,f)`

and

`W_S = median_f W_S,f`.

For ordered transfer `S -> T`:

`X_Z,S->T,f = corr(z_TRAIN(S,f), z_HELD(T,f))`

and

`X_Z,S->T = median_f X_Z,S->T,f`.

Require at least 4 valid fold correlations for every required median.

The source training graph never sees physical leaves assigned to the held-out fold.

## 14. Frozen per-contrast classification gates

These practical thresholds intentionally reuse #58B's preregistered geometry rather than choosing new values after #58C reveal.

A contrast is first **eligible** only if both groups have supported stratum-level residual existence.

### 14.1 `STABLE_RESIDUAL`

iff all are true:

1. both group residual-existence gates pass;
2. `R_Z >= .70`;
3. `p_R,maxT <= .01`;
4. `X_Z,S->T >= max(.60, W_T - .15)`;
5. `X_Z,T->S >= max(.60, W_S - .15)`.

### 14.2 `RELATED_RESIDUAL_BUT_MODULATED`

If stable fails, classify this iff all are true:

1. both group residual-existence gates pass;
2. `R_Z >= .40`;
3. `p_R,maxT <= .01`;
4. both directional transfers are `>= .30`.

### 14.3 `DIFFERENT_RESIDUAL_OR_MIXTURE`

Classify this iff:

1. both group residual-existence gates pass; and
2. at least one is true:
   - `R_Z < .40`;
   - `X_Z,S->T < .30`;
   - `X_Z,T->S < .30`.

A lack of similarity significance by itself does not prove difference.

### 14.4 `INCONCLUSIVE_RESIDUAL_BASIS`

If either group fails residual-existence eligibility, use this class.

### 14.5 `INCONCLUSIVE_RESIDUAL_STABILITY`

Any otherwise eligible contrast satisfying none of the stable/related/different gates receives this class.

## 15. Frozen family and global classifications

These classifications are reached only if the pooled residual-existence gate passes.

### 15.1 Register/section family

Four contrasts:

- Currier A vs B within Herbal;
- B vs H within Currier B;
- B vs S within Currier B;
- H vs S within Currier B.

Family classification:

- `REGISTER/SECTION SHARED RESIDUAL GRAPH` iff all four are `STABLE_RESIDUAL`;
- `REGISTER/SECTION RESIDUAL MODULATION` iff none is different/inconclusive and at least one is `RELATED_RESIDUAL_BUT_MODULATED`;
- `REGISTER/SECTION MULTIPLE/HIERARCHICAL RESIDUAL GRAMMARS` iff any is `DIFFERENT_RESIDUAL_OR_MIXTURE`;
- otherwise `REGISTER/SECTION RESIDUAL STABILITY INCONCLUSIVE`.

### 15.2 Line-position family

Three contrasts.

- `LINE-POSITION STABLE RESIDUAL GRAPH` iff all three are `STABLE_RESIDUAL`;
- `LINE-POSITION RESIDUAL MODULATION` iff none is different/inconclusive and at least one is `RELATED_RESIDUAL_BUT_MODULATED`;
- `LINE-POSITION MATERIALLY CHANGES RESIDUAL GRAPH` iff any is `DIFFERENT_RESIDUAL_OR_MIXTURE`;
- otherwise `LINE-POSITION RESIDUAL STABILITY INCONCLUSIVE`.

### 15.3 Overall #58C classification

Apply in this order:

1. if `p_exist_ALL > .01` -> `NO DETECTABLE RESIDUAL GRAPH BEYOND LOWER-ORDER OCCUPANCY ARCHITECTURE`;
2. else if pooled residual reliability gate fails -> `RESIDUAL TOKEN-CONSTRUCTION RESULT INCONCLUSIVE`;
3. else if register/section family is multiple/hierarchical **or** line-position materially changes residual graph -> `MULTIPLE/HIERARCHICAL RESIDUAL TOKEN GRAMMARS`;
4. else if register/section family is shared **and** line-position family is stable -> `SHARED RESIDUAL TOKEN-CONSTRUCTION GRAPH`;
5. else if neither family is inconclusive and at least one family is modulation -> `RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`;
6. otherwise -> `RESIDUAL TOKEN-CONSTRUCTION RESULT INCONCLUSIVE`.

This ordering prevents an attractive cross-stratum pattern from rescuing failure of the primary existence gate.

## 16. Parser `max` sensitivity

Repeat **real-data calculations only** under parser ambiguity policy `max` using the same frozen reference calibration concept, but `max` cannot alter the primary `min` classification.

Because the residual transform requires a null reference distribution, a valid `max` sensitivity must generate its own prospectively fixed `N_ref=1000` reference-null ensemble under a distinct namespace:

`Issue58C:ResidualGraph:MaxSensitivityReference:v1:<index>`.

No independent test-null p-values are required for `max` in #58C-A.

Emit descriptively:

- pooled real residual energy under its `max` reference calibration;
- real residual group energies;
- real residual graph correlations/reliabilities/transfers.

Agreement may strengthen representation robustness descriptively; disagreement may weaken generality; neither can promote the primary result.

If runtime or implementation complexity makes this sensitivity unsafe, it may be omitted only **before target reveal**, with the omission recorded in preflight. It may not be dropped because the observed sensitivity is unfavorable.

## 17. Implementation efficiency rule

The statistical definition above is normative; implementation may optimize algebra without changing it.

In particular, for each null population it is permitted and preferred to compute conditional occupancy counts once by `group x physical-leaf fold x edge x K_other x 2 x 2`, then derive FULL/TRAIN/HELD Q vectors by summing fold counts before applying the frozen Q formula.

This avoids rescanning tokens for every view and does not change the statistic.

## 18. Preflight and first-reveal authorization

Before target scoring, preflight must verify without emitting any real residual target statistic:

1. this plan predates the target executable;
2. exact external source commit/blob;
3. parser import and frozen parser examples;
4. visible/parsed population counts;
5. exact group/fold support counts;
6. all 66 pair labels and expected dimensions;
7. reference/test seed namespaces are disjoint;
8. null line x slot marginal preservation on synthetic or designated null data;
9. empirical-normal-score implementation on synthetic tied and untied examples;
10. reference and test null paths cannot alias the same stored/drawn null index.

Pushes to the research branch may run preflight only.

The first target reveal is authorized only by opening a PR to `main` (or an explicit workflow dispatch after an audit records why PR execution is unavailable). This preserves a visible plan-before-reveal event.

## 19. Exact target outputs required

The raw result JSON must include:

1. phase/version and target-reveal flag;
2. source/blob/parser/fold verification;
3. exact population and group/fold counts;
4. all 66 pair labels;
5. reference/test null seed namespaces and counts;
6. primary real `Q` and residual `Z` vectors for ALL and all target groups;
7. real TRAIN/HELD residual vectors or sufficient exact summaries to reproduce W/X;
8. primary pooled residual energy, null distribution summary and `p_exist_ALL`;
9. group residual energies, `p_E,maxT`, reliabilities and eligibility flags;
10. all seven real residual correlations, `p_R,maxT`, directional fold transfers and medians;
11. every per-contrast frozen classification;
12. register/section family classification;
13. line-position family classification;
14. overall #58C classification;
15. test-null pooled energy values and maxT vectors sufficient to reproduce all empirical p-values;
16. non-promoting sensitivities actually executed;
17. complete deterministic runtime/configuration metadata needed for exact replay.

The raw result must be archived permanently immediately after first reveal with SHA-256 and provenance.

## 20. Stop rules after reveal

Do not after target reveal:

- change the 66-edge set;
- change the base conditional Q statistic;
- change the empirical-normal-score transform;
- reuse test nulls as reference nulls or vice versa;
- change `N_ref=1000` or `N_test=1000`;
- change seed namespaces;
- change the primary `E=sqrt(mean(z^2))` statistic;
- change `.01/.50/.70/.40/.60/.30/.15` gates;
- switch Pearson to Spearman/cosine because it looks better;
- add or merge strata;
- privilege observed individual residual edges;
- interpret residual similarity if the pooled existence gate fails;
- infer slot semantics, plaintext, a cipher table, music, or decipherment.

Any material change is a new separately preregistered phase.

## 21. Consequence branches

### If `SHARED RESIDUAL TOKEN-CONSTRUCTION GRAPH`

Promote the residual graph — not the raw #58A graph — as a stronger manuscript-wide token-internal surface constraint. Next prioritize representation/transcription invariance. Only after that use the stable residual constraints prospectively to restrict reversible generative/inverse models.

### If `RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`

Model a shared residual core plus prospectively documented register/section/position modulation before any inverse claim.

### If `MULTIPLE/HIERARCHICAL RESIDUAL TOKEN GRAMMARS`

Stop assuming one token generator across the manuscript. Move to a hierarchical or multiple-generator inverse architecture.

### If `NO DETECTABLE RESIDUAL GRAPH BEYOND LOWER-ORDER OCCUPANCY ARCHITECTURE`

Downgrade the raw 66-edge graph from a deep-grammar candidate under this representation. Do not continue mining individual occupancy edges. Move to another independently motivated structural representation or inverse constraint.

### If `RESIDUAL TOKEN-CONSTRUCTION RESULT INCONCLUSIVE`

Record the limitation. Do not tune this phase after reveal. Diagnose power/representation limits only in a new plan-first phase if the expected information gain justifies it.

## 22. Interpretation boundary

Even a positive shared residual result does not establish:

- that visible spaces are linguistic words;
- sentence grammar;
- semantic meanings for slots;
- a plaintext alphabet or cipher table;
- one particular historical generator;
- semantic presence or absence;
- decipherment.

Its role is architectural: establish whether a non-trivial token-internal construction layer survives lower-order occupancy controls strongly enough to constrain the later inverse problem.