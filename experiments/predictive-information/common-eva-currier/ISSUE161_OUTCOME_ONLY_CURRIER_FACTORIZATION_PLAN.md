# Issue #161 — outcome-only Currier factorization plan

Date: 2026-09-07
Status: **FROZEN BEFORE TARGET SCORING**
Parent: Issue #88
Issue: #161

## Question

Can the Currier A/B edge contrast be explained by a context-invariant Currier-specific bias over the next initial common-EVA atom, or does held-out information remain that requires a genuine previous-terminal × next-initial Currier interaction?

## Entry authority

Issue #158 is closed with frozen classification:

> **`CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`**

Frozen #158 authority:

- score-free Gate merge `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- Gate result SHA-256 `605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099`;
- Gate script blob `4dbc919f3e9ededa17d2e10f56de46c98456cdea`;
- corrected Gate provenance blob `07595bf7314cfb71763eba1a810bfd3aaa01a239`;
- scientific scorer blob `e7a70a10dd7b663f3482993b0adfa8f804816158`;
- first-reveal provenance blob `0f3c14d2f592dea020c180669670cafca5ba1b05`;
- first-reveal run `34076400927`;
- artifact `10002205049`;
- result JSON SHA-256 `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`;
- PR #160 merge `1741bed875a582594dc797ef18e30dd2ef3351ce`.

The current common-EVA Currier matched-table authority remains Issue #155 Gate0 and is reproduced through #158.

## Frozen representation, folds and target population

Reuse Issue #158 exactly:

- ZL3b and Takahashi/IT2a source authority;
- common Basic-EVA representation, 31 observed atoms plus END, `V=32`;
- maximal contiguous clean runs;
- Phase3A physical-leaf Currier A_ONLY/B_ONLY labels;
- the same five physical-leaf folds, SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- SlotParser primary targets unchanged;
- fixed `k=2`, `alpha=.01`;
- no context crosses an unclean segment;
- no target-native fallback.

## Frozen training tables

For each outer fold, reproduce the exact Issue #158 training-only rational tables:

- `C_A^MATCH(c,y)`;
- `C_B^MATCH(c,y)`;
- `C_POOL(c,y)=0.5*C_A^MATCH(c,y)+0.5*C_B^MATCH(c,y)`.

A/B/POOL have exactly equal effective mass separately inside every retained previous-terminal context `c`.

## Frozen outcome-only Currier gate

For each regime `R∈{A,B}` and fixed outcome `y` in the 32-outcome vocabulary, aggregate training-only matched counts across retained previous-terminal contexts:

`G_R(y)=Σ_c C_R^MATCH(c,y)`

`G_POOL(y)=Σ_c C_POOL(c,y)`.

Because context masses are equalized before aggregation, total aggregate A/B/POOL effective mass is exactly equal.

Use the same fixed additive constant `alpha=.01` to define:

`W_R(y)=(G_R(y)+alpha)/(G_POOL(y)+alpha)`.

For retained context `c`, define the already-frozen smoothed pooled conditional:

`P_POOL(y|c)=(C_POOL(c,y)+alpha)/(m(c)+alpha*V)`.

Then define:

`P_OUTCOME_R(y|c) ∝ P_POOL(y|c) * W_R(y)`

with exact normalization over the fixed 32 outcomes separately within each context.

This model contains a Currier×outcome main effect but **no Currier×previous-terminal×outcome interaction**. All multipliers are determined from training counts only. There is no target-likelihood fit, temperature, scalar, interpolation, mixture, outcome selection or context selection.

For unsupported exact contexts, retain the frozen empty additive distribution from #158; do not apply a Currier or target-native fallback.

## Frozen target models

For target reading `T` and Currier regime `R`:

### `EDGE_POOL_T,R`

Exact Issue #158 pooled edge model.

### `EDGE_OUTCOME_T,R`

Identical to `EDGE_POOL_T,R` except BODY first-atom probability uses `P_OUTCOME_R(y|c)`.

### `EDGE_REGIME_T,R`

Exact Issue #158 full target-regime matched table model.

All start, second-atom, k2 continuation and non-edge factors remain identical and target-reading/target-Currier native.

## Primary quantities

For each reading × regime × fold:

`G_outcome[T,R,f]=bits(EDGE_POOL_T,R)-bits(EDGE_OUTCOME_T,R)`

`G_interaction[T,R,f]=bits(EDGE_OUTCOME_T,R)-bits(EDGE_REGIME_T,R)`.

`G_outcome` is the held-out information captured by the context-invariant next-initial bias.

`G_interaction` is the residual held-out information requiring the full Currier-specific previous-terminal × next-initial mapping.

A reading×regime interaction residual passes iff:

- mean `G_interaction > 0`; and
- positive in at least `4/5` folds.

A regime is robustly context-specific only if that criterion passes independently in both ZL3b and IT2a.

`G_outcome` is reported prospectively but its positivity is not a prerequisite for recognizing a positive interaction residual.

## Frozen classifications

Exactly one:

1. **`CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN BOTH A AND B`**
2. **`CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN A ONLY`**
3. **`CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN B ONLY`**
4. **`NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`**
5. **`INVALID CURRIER EDGE FACTORIZATION`**

No equivalence margin, effect-size rescue threshold or post-reveal class change.

## Mandatory score-free Gate0

Before any real-target `EDGE_OUTCOME` probability or likelihood is computed:

1. reproduce exact merged #158 Gate/result/scorer/provenance authority;
2. reproduce all five #158 A/B/POOL rational table identities and physical-leaf folds;
3. construct `G_A`, `G_B`, `G_POOL` from training rational counts only;
4. prove aggregate A/B/POOL total mass equality exactly;
5. construct/archive all fixed `W_A(y)`, `W_B(y)` for all 32 outcomes using exact rational arithmetic;
6. prove finite normalized `P_OUTCOME_R(.|c)` for every retained context and both regimes without loading held-out target outcomes;
7. reproduce all #158 reading×regime×fold target support counts and zero held-out-leaf leakage;
8. run target-free synthetic tests: one pure global outcome shift and one context-specific contrast, verifying the factorization does not silently collapse the latter;
9. firewall every real-target outcome-only probability, likelihood, `G_outcome`, `G_interaction` and classification.

Gate0 must stop INVALID if authority, support, vocabulary coverage, mass equality or normalization fails. Do not change the factorization to rescue the Gate.

## Consequence fork

### Interaction residual in both A and B

Currier changes the conditional relation between previous-terminal and next-initial. The next compression target may be a separately preregistered low-rank interaction model.

### Interaction residual in only one regime

Retain an outcome-only gate for one regime and a context-specific correction for the other. Characterize only after freezing the primary result.

### No robust interaction residual

Promote the simpler responsibility:

> **one shared terminal→initial table + Currier-specific global next-initial bias.**

### Invalid

Stop without target interpretation.

## Firewall

This issue must not:

- inspect held-out target outcomes to select atoms or contexts;
- change Currier labels, common-EVA atomization, folds, support matching, pooled weights or target population;
- tune `alpha`, multiplier smoothing, temperature, interpolation, fallback or mixture;
- condition on hand/section/domain;
- fit latent states;
- tune S1/S2/H62/R1;
- infer words, plaintext, semantics, language/cipher family, authorship, historical direction/mechanism, artificiality/hoax or decipherment.

Refs #88 #134 #145 #151 #155 #158 #160 #161.
