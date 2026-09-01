# Hypothesis ledger addendum — Issue #75 Phase A

Status: **PHASE A COMPLETE / LOW-ORDER MODELS FALSIFIED**

## H75-M0 — independent slot marginals are sufficient for the replicated R1 occupancy topology

### Prediction

A cross-fitted non-empty maximum-entropy generator using only training-fold occupancy probability for each of the 12 slots should reproduce the complete 66-edge residual topology within the stochastic variation of empirical-signature resampling if R1 is fundamentally a slot-prevalence effect.

### Result

**REFUTED.**

31/31 frozen M0 realizations:

- median `T=min(R_ZL3b,R_IT2a) = -0.1100912028`
- median ZL3b Pearson `-0.1061945351`
- median IT2a Pearson `-0.1065375742`
- median residual energy `1.1951700876`
- median fold reliability `W=0.0113522046`

Positive-control center is near `T≈0.965` and the frozen q95 positive-control self-variation is only `0.0097683130`.

Paired median gap:

`gap_M0 = -1.0779969902`

Thus individual slot frequencies plus the non-empty-token constraint do not explain the replicated topology.

## H75-M1 — slot marginals plus occupied-slot count K are sufficient

### Prediction

If the residual topology is principally induced by regulating how many slots a token occupies, then a generator supplied with the training-only exact `P(K)` plus slot main effects, but no pair interactions or empirical signature inventory, should recover the target topology.

### Result

**REFUTED.**

31/31 frozen M1 realizations:

- median `T=-0.1674116607`
- median ZL3b Pearson `-0.1674116607`
- median IT2a Pearson `-0.1552698274`
- median residual energy `3.2511860424`
- median fold reliability `W=0.3238465130`
- median/constant sign agreement approximately `38/66` ZL3b and `37/66` IT2a
- `p_exist=0.000999` in all 31 realizations

Paired median gap:

`gap_M1 = -1.1307973706`

This result is especially informative: occupancy-count regulation produces a strong, non-null residual graph of roughly the correct total energy, but its geometry is wrong and mildly anticorrelated with Voynich.

Therefore:

> **The presence of strong within-token dependence is not sufficient. The identity of which structural slots are selected together matters.**

## H75-MPLUS — the empirical occupancy-signature inventory is sufficient under cross-fitting

### Prediction

Sampling complete 12-bit signatures from the other four physical folds should regenerate the held-out/full replicated topology if the occupancy-pattern inventory itself is the R1-relevant sufficient information identified by #72 FI.

### Result

**SUPPORTED AS POSITIVE CONTROL.**

Independent bank A:

- median T `0.9643123239`
- median ZL3b R `0.9670395573`
- median IT2a R `0.9643123239`
- median W `0.9867897938`

Independent bank B:

- median T `0.9655940680`
- median ZL3b R `0.9684856054`
- median IT2a R `0.9655940680`
- median W `0.9857565429`

Both exceed the preregistered positive-control floor `0.9447148364`.

The q95 paired bank-to-bank T variation is only `0.0097683130`.

This validates the Phase-A evaluation interface and confirms that the cross-fold empirical signature inventory retains the independently replicated R1 core.

## Frozen Phase-A classification

`LOW_ORDER_MODELS_INSUFFICIENT_EMPIRICAL_PATTERN_STRUCTURE_REQUIRED`

Authority:

- first-reveal scientific head `785bd9f04afceadf4072ea576812649554ad6c6e`
- run `33502168755` — success
- 124/124 complete population
- aggregate SHA-256 `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`
- permanent authority commit `5059eaf60d5725e65895c8c0fac8dfe859151cf7`

## Scientific revision

The R1 construction constraint can now be localized more narrowly than after #72.

Not sufficient:

1. individual slot occupancy rates;
2. individual slot occupancy rates plus the number of occupied slots per token.

Sufficient positive control:

3. the cross-fitted empirical inventory of complete 12-bit occupancy configurations.

The missing mechanism must therefore encode information about **which subsets of positions are compatible/preferred together**.

Conceptually:

`slot propensities`

`      +`

`token occupancy count K`

`      ↓`

`strong generic dependence, but wrong graph`

`      +`

`within-token configuration-selection rule   <-- unresolved required layer`

`      ↓`

`Voynich-like 66-edge residual topology`

This does not require literal empirical signature memorization as a historical mechanism. M+ only shows a sufficiency ceiling. The next question is whether a small generic rule can replace that empirical inventory.

## Licensed next frontier

The preregistered Phase-A outcome explicitly licenses a richer phase because:

- M0 failed materially;
- M1 failed materially;
- both M+ banks passed calibration.

Next hypothesis:

> A compact, target-blind within-token configuration grammar based on generic shape structure or a small latent/state process can reproduce the empirical-signature positive-control topology without storing the empirical 12-bit inventory.

The next phase must remain ordered from simpler generic pattern descriptions to a small state generator. It must not directly optimize the frozen 66 target edges.

## Interpretation boundary

No Phase-A result identifies:

- meanings for slots;
- literal Voynich glyph/token rules;
- plaintext;
- a cipher mechanism;
- word boundaries;
- historical Naibbe use;
- decipherment.

The result concerns the minimum information currently known to be required for the replicated 12-slot occupancy topology.
