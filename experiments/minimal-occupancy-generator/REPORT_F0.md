# Issue #75 Phase F0 — target-blind latent-frontier diagnostic result

Date: 2026-09-02  
Status: **COMPLETE / TRAINING-ONLY AUTHORITY FROZEN**

## Primary question

Phase E showed that two global hidden local-chain construction modes recover a large additional fraction of the replicated R1 topology but remain insufficient (`median T=0.7251534248`).

Phase F0 deliberately did **not** inspect target R1 residuals. It asked a narrower architecture-selection question using only physical-leaf held-out occupancy prediction:

> Is the next compact improvement better explained by (a) letting the probability of the two Phase-E construction modes depend on coarse token geometry K/R/S, or (b) adding a third geometry-independent global construction mode?

Frozen classification:

`F0_SELECT_KRS_GATED_TWO_MODE_CHAIN`

The result is strong: both richer families predict held-out occupancy better than M5 in all five physical folds, but the smaller K/R/S-gated two-mode model beats the global three-mode model in four of five folds and wins the prospectively frozen parsimony rule.

## Frozen authority

Normative plan:

- `PLAN_F0_TRAINING_LATENT_DIAGNOSTIC.md`
- plan commit `dc780cbe985e424dc3953003d05e682b8a492694`

Implementation clarification:

- commit `431ff0e328d1c3cd065bba53fa4438780490fa92`

First scientific executable:

- commit `201a4d3a1ff4ef374f1ab3b0c2f8adf7f886e394`

Attempt-1 numerical abort:

- run `33543350071`
- no accepted F0 authority or target result

Normalization-only repair:

- repair plan commit `021b8420dcefe06ddbba9f6c0f101ab18310806b`
- stable runner commit `2874f57a201fd36f8289e5375551a240ef5f02d4`
- repair freeze commit `d3622e70495bc256451a1b6dede027e96c78da57`

Authoritative complete serial execution:

- run `33545246568` — success
- execution head `9a9a66d85e74d02e804e435c9a15a007a7047aa2`
- artifact ID `9817348700`
- artifact digest `sha256:e56a2b4ab6e6741420c3ba3e430d16ec0c3a565abf4a40c7a917425da82cf7da`
- authority SHA-256 `999d9990449875708019ad71aa3a1d253afad19edada88cb45eb4204349887c6`
- permanent repository authority commit `fd1446d474208b9e2f17e3fd4df5249e133c2bd3`
- directory `experiments/minimal-occupancy-generator/stage-f0/`

The output records:

- `external_reference_measurements_accessed=false`;
- `reference_residual_vector_loaded=false`;
- `reference_correlation_computed=false`;
- `reference_sign_agreement_computed=false`;
- `random_restarts=false`;
- `rerolls=false`.

No R1 target correlation, target sign pattern, target edge residual, or T value was used to select the architecture.

## Families compared

### M5 baseline

`M5-KRS-2MIX-CHAIN`

- 2 global latent local-chain components;
- 43 free continuous parameters per outer fold;
- one geometry-independent global mixing probability `pi`.

### G2

`M6-KRS-GATED-2MIX-CHAIN`

The same two local-chain components, but the mode probability depends on standardized coarse token geometry:

`logit P(Z=1 | K,R,S) = a0 + aK*zK + aR*zR + aS*zS`.

- 42 local-chain component parameters;
- 4 gate parameters;
- total 46 free continuous parameters per outer fold;
- no explicit nonadjacent pair term;
- no generic distance term;
- no signature-specific term.

M5 is nested at `aK=aR=aS=0`.

### G3

`M6-GLOBAL-3MIX-CHAIN`

- 3 global M3 local-chain components;
- 2 global mixture logits;
- 65 free continuous parameters per outer fold;
- no K/R/S-dependent gate;
- no explicit nonadjacent pair term;
- no generic distance term;
- no signature-specific term.

## Evaluation

Each of the five physical leaves was held out in turn.

For each outer fold:

1. M5, G2, and G3 were fit only to the other four physical leaves;
2. model selection among deterministic starts used outer-training conditional likelihood only;
3. the held-out metric was exact conditional occupancy log likelihood `log P(x | K,R,S)` per token;
4. no Monte Carlo R1 measurement and no target graph was involved.

A richer family was prospectively defined as predictively supported over M5 only if:

- its held-out gain was positive in all five physical folds; and
- median gain was at least `0.01 nat/token`.

If both G2 and G3 were supported, G2 won by parsimony unless G3 beat G2 in at least 4/5 folds and by median direct gain at least `0.01 nat/token`.

## Result

### G2 versus M5

Held-out gain, nat/token:

| fold | G2 − M5 |
|---:|---:|
| 0 | `+0.0679060418` |
| 1 | `+0.0571128555` |
| 2 | `+0.0600306734` |
| 3 | `+0.0771395827` |
| 4 | `+0.0512153334` |

- positive folds: `5/5`;
- median gain: `+0.0600306734 nat/token`;
- support threshold: `+0.01 nat/token`;
- supported: **yes**.

### G3 versus M5

Held-out gain, nat/token:

| fold | G3 − M5 |
|---:|---:|
| 0 | `+0.0496963470` |
| 1 | `+0.0348642929` |
| 2 | `+0.1219960036` |
| 3 | `+0.0394097637` |
| 4 | `+0.0397234021` |

- positive folds: `5/5`;
- median gain: `+0.0397234021 nat/token`;
- supported: **yes**.

### G3 versus G2 directly

Held-out `H_G3-H_G2`, nat/token:

| fold | G3 − G2 |
|---:|---:|
| 0 | `-0.0182096948` |
| 1 | `-0.0222485626` |
| 2 | `+0.0619653302` |
| 3 | `-0.0377298190` |
| 4 | `-0.0114919313` |

- G3 wins: `1/5` folds;
- median direct gain: `-0.0182096948 nat/token`.

Therefore G3 does not satisfy the preregistered condition required to displace the smaller G2 family.

## Stable geometry gate

The G2 gate coefficients were estimated independently in each outer-training population after K/R/S standardization.

The three slopes `(aK,aR,aS)` were:

| fold | aK | aR | aS |
|---:|---:|---:|---:|
| 0 | `+0.7973` | `-2.1237` | `+1.2569` |
| 1 | `+0.8204` | `-2.3027` | `+1.4352` |
| 2 | `+0.8102` | `-2.1235` | `+1.1871` |
| 3 | `+0.5681` | `-2.0138` | `+2.0052` |
| 4 | `+0.5937` | `-2.0618` | `+2.0398` |

All three slope signs are identical across all five physical folds:

- occupied count `K`: positive;
- occupied-run count `R`: strongly negative;
- occupied span `S`: positive.

This is not a semantic labeling of either latent component. But, under the frozen component-label convention, one statistical construction regime becomes more probable for tokens that are, in standardized K/R/S terms, more occupied, broader in span, and less fragmented into separate occupied runs.

The fitted descriptor-level gate probabilities span roughly `0.019–0.033` at the low end and approach `0.99997–0.99999` at the high end. Thus geometry dependence is not a tiny correction to a 50:50 global mixture; for some coarse token shapes the latent regime is nearly determined.

## Mechanistic interpretation

Phase E established that hidden/common-cause construction variation is useful but that a single global A/B mixing proportion is too coarse.

F0 now identifies *where much of that missing structure sits*:

> **The hidden construction regime is coupled to the coarse geometry of the token itself.**

The data do not favor the picture

`choose A/B/C globally -> build token locally`

as strongly as the more economical picture

`coarse token geometry K/R/S -> changes probability of A/B construction regime -> local slot grammar -> completed occupancy signature`.

This matters because K/R/S were already conditioned on inside the local component distributions. The gain therefore is not merely that K/R/S predicts token shape. It says that **tokens with different coarse shapes use the two local construction grammars in systematically different proportions**.

A useful conceptual shorthand is:

`geometry is not only an output envelope; it also gates the construction regime.`

## Updated mechanistic ladder

The supported decomposition is now:

1. marginal occupancy/prevalence — insufficient;
2. occupancy count — insufficient;
3. K/R/S coarse geometry — real but limited;
4. position-specific local adjacency — large gain;
5. generic physical-distance coupling — small extra gain;
6. two global hidden local grammars — large extra gain;
7. **K/R/S-conditioned choice between those hidden grammars — strongest target-blind next mechanism**;
8. empirical complete signature inventory — sufficient positive control.

F0 does not yet say whether G2 reproduces the complete replicated 66-edge R1 topology. That is the next prospective target test.

## What F0 rules against

Within the tested compact alternatives, the Phase-E failure is not best explained by simply needing one more geometry-independent global token class.

A third global class does help held-out prediction, but it is larger (65 versus 46 parameters) and loses directly to G2 in four of five physical folds.

Thus the next target model should not be chosen by increasing latent-state count merely because Phase E used only two states.

## Boundaries

F0 does not establish:

- two semantic word classes;
- two languages;
- cipher states;
- meanings of slots or latent components;
- plaintext letters or words;
- a historical encoding procedure;
- natural-language morphology;
- decipherment.

It establishes a target-blind model-selection result: **coarse token geometry predictively gates the occupancy-construction regime**, and this compact 46-parameter mechanism is the prospectively selected next R1 generator test.
