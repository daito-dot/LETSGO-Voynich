# Issue #75 Phase D — nested distance-banded nonlocal occupancy grammar

Date: 2026-09-01  
Status: **PREREGISTERED AFTER FROZEN PHASE-C RESULT / BEFORE PHASE-D EXECUTABLE / NO PHASE-D TARGET RESULT**

## 0. Authority and chronology

Phase D is licensed only by the valid frozen Phase-C outcome:

- Phase-C first-reveal run: `33508975967` — success;
- scientific head: `8d02507355f428ffc80d590bbcfe256ce9fd0d95`;
- permanent result commit: `9664e7cd1cf1eec8c2dacf37ceeb9c15c31a1f2a`;
- aggregate SHA-256: `34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a`;
- classification: `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED`;
- `gap_M3=-0.37325753997796984`;
- frozen q95 allowed loss: `0.009768313008182594`.

The controlling decision file is:

`experiments/minimal-occupancy-generator/DECISION_C_NONLOCAL_OR_LATENT_REQUIRED.md`

The earlier `.github/workflows/issue75-phaseD-preregister-if-licensed.yml` was authored during the broken Phase-C automation chain and is non-authoritative. Commit `1a56ef550af3ab65620ad32b2b4d6ba5aa7becc4` then materialized a post-Phase-C distance-only plan. Before any Phase-D executable was committed, that plan was audited and corrected here for two reasons:

1. it discarded the position-specific adjacent interactions that Phase C had already shown to carry substantial topology signal, so it was not a nested extension of M3;
2. its stated 20-dimensional distance-only feature family missed an additional identifiability constraint induced by conditioning on span `S`.

This corrected file is the sole normative Phase-D plan. No Phase-D executable or target result predates it.

## 1. Scientific question

Phase A ruled out slot marginals and occupied-slot count alone. Phase B showed that coarse `(K,R,S)` token geometry recovers only a modest part of R1. Phase C retained exact training-only `(K,R,S)` geometry and added position-specific nearest-neighbor occupancy interactions, raising median `T` from about `0.287` to about `0.593`, while remaining far below the empirical-signature positive-control ceiling near `0.965`.

The next deliberately narrow question is:

> **If the successful M3 local transition grammar is retained, are generic nonadjacent interactions determined only by slot separation sufficient to recover the replicated complete 66-edge topology?**

This is a strict nested extension of M3. It adds no target-selected pair and no latent state.

## 2. Frozen representation and evaluation

Use the unchanged Issue #75 representation and complete-graph evaluation:

- parser-accepted token -> 12-bit occupancy vector;
- `SlotParser(min)` authority unchanged;
- 25,071 accepted ZL3b tokens on the frozen physical-leaf skeleton;
- five physical-leaf cross-fit folds unchanged;
- exact training-only empirical `(K,R,S)` descriptor distribution per cross-fit split;
- all `C(12,2)=66` unordered slot pairs retained;
- candidate-owned K_other-conditioned Jeffreys-smoothed MH/Yule-Q reference null;
- residual Z, residual energy E, existence p-value, physical-fold reliability W;
- ZL3b and IT2a target vectors evaluated separately;
- `T=min(R_ZL3b,R_IT2a)`;
- exact Phase-A paired M+ positive-control centers reused from aggregate SHA `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`;
- q95 no-material-loss tolerance remains exactly `0.009768313008182594`.

The frozen Phase-C result may be used only as prior-stage authority and as a descriptive paired comparator. No Phase-D feature, distance band, parameter, seed, or variant may be selected from the revealed 66 target edges, their signs, or their residual magnitudes.

## 3. M4-KRS-CHAIN-DISTANCE model

For non-empty occupancy vector `x in {0,1}^12`, retain

`D(x)=(K(x),R(x),S(x))`

and the exact training-only descriptor distribution

`q_d=P_train(D=d)`.

Within each descriptor class define:

- unary feature `U_s(x)=x_s`, for `s=0..11`;
- position-specific adjacent feature `A_s(x)=x_s*x_{s+1}`, for `s=0..10`;
- aggregate nonadjacent separation feature

`C_d(x)=sum_{s=0}^{11-d} x_s*x_{s+d}`, for `d=2..11`.

Conditional model:

`P(x | K,R,S) proportional to exp(sum_s h_s U_s(x) + sum_s J_s A_s(x) + sum_{d=2}^{11} B_d C_d(x))`.

This model contains M3 exactly when all identifiable `B_d` are zero. The only new information channel is generic nonadjacent separation distance.

It has:

- no named-pair-specific nonadjacent coefficient;
- no complete-signature-specific parameter;
- no latent state or mixture class;
- no target-derived feature selection.

## 4. Exact identification and complexity

Conditioning on `(K,R,S)` creates four parameter directions that cannot change `P(x|K,R,S)`.

### 4.1 Unary gauge

Within fixed `K`:

`sum_s U_s = K`.

A common unary offset cancels. Fix:

`h_0=0`.

This leaves 11 free unary parameters `h_1..h_11`.

### 4.2 Adjacent gauge

Within fixed `(K,R)`:

`sum_s A_s = K-R`.

A common adjacent offset cancels. Fix:

`J_0=0`.

This leaves 10 free position-specific adjacent parameters `J_1..J_10`, exactly as in M3.

### 4.3 Nonadjacent common-offset gauge

Within fixed `(K,R)`:

`sum_{d=2}^{11} C_d = choose(K,2)-(K-R)`.

A common offset across all nonadjacent-distance coefficients cancels. Fix:

`B_2=0`.

### 4.4 Span-induced distance-11 invariance

Because there are only 12 slots, `C_11=x_0*x_11`. Within a fixed span class:

- if `S=12`, both endpoints 0 and 11 are occupied and `C_11=1`;
- if `S<12`, the two endpoints cannot both be occupied and `C_11=0`.

Therefore `C_11` is a deterministic function of `S` and has zero within-descriptor variance. `B_11` is not identifiable and is omitted/fixed to zero.

The exact-state feature-rank audit must confirm:

- unary within-descriptor rank = `11`;
- unary + adjacent rank = `21`;
- unary + adjacent + all distance features rank = `29`.

Free continuous parameters per cross-fit training split:

- 11 unary parameters;
- 10 position-specific adjacent parameters;
- 8 nonadjacent distance parameters `B_3..B_10`;
- total: **29**.

Complexity assertions:

- explicit named-pair nonadjacent parameters: `0`;
- empirical complete-signature-specific parameters: `0`;
- latent-state parameters: `0`.

## 5. Training-only sufficient statistics

Fit only from the four training folds to reproduce the empirical moments of:

- all 12 unary occupancies `E[U_s]`;
- all 11 position-specific adjacent occupancies `E[A_s]`;
- all 10 aggregate nonadjacent-distance occupancies `E[C_d]`, `d=2..11`.

There are 33 reported moments but only 29 independent within-descriptor degrees of freedom because of the four exact identities in Section 4.

Before fitting, the executable must verify all four identities and the exact rank `29` over the complete 4095 non-empty state space partitioned by `(K,R,S)`.

No held-out-fold moment or target R1 quantity is part of training.

## 6. Exact deterministic fitting

Use the exact 4095 non-empty 12-bit signature state space.

Required procedure:

- zero initialization of all 29 free parameters;
- exact expectation and covariance within every nonzero `(K,R,S)` class;
- deterministic Newton / damped moment matching;
- no Monte-Carlo fitting;
- no random initialization;
- no target-derived regularization or feature pruning;
- maximum absolute error `<=1e-10` across all 33 reported moments after accounting for the exact identities;
- a failed fold fit is an experimental failure, not a reroll.

Deterministic numerical stabilization is allowed only if it does not alter the model family, sufficient statistics, target moments, or stopping tolerance.

## 7. Target-blind D0 population

Generate exactly 31 complete cross-fitted `M4-KRS-CHAIN-DISTANCE` corpora, reps `0..30`, on the frozen accepted-token/line skeleton.

For held-out fold `f`, fit only on the other four folds.

Generation namespace:

`issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:fold{f}:generate`

Each generated corpus must contain exactly 25,071 non-empty signatures on the unchanged skeleton.

Before any Phase-D target access, freeze for all 31 cases:

- exact occupancy SHA-256;
- token count and fold counts;
- exact training descriptor distribution;
- all 33 training and fitted moments;
- fitted parameter vector and max fit error;
- rank/identity audit;
- generated descriptor distribution and distinct-signature diagnostics;
- target-access flags all false;
- no drops / no rerolls.

The D0 population must be immutable by exact SHA before target scoring is authorized.

## 8. Required pretarget validation

Before first reveal:

1. exact-replay preflight for reps `0` and `30` must regenerate the frozen D0 occupancy SHA exactly;
2. one rep-0 candidate-null smoke must complete the full candidate-owned 1000-reference / 1000-test residual calculation while the ZL3b/IT2a target loader remains unused;
3. scorer and aggregator code must be frozen before the first target-scoring run;
4. all target-access guards must be explicit and machine-checked.

## 9. Candidate-owned R1 measurement

Reuse the exact unchanged Phase-A/B/C scoring contract:

- all 66 unordered pairs;
- K_other-conditioned Jeffreys-smoothed MH/Yule-Q;
- `N_ref=1000` line-local reference nulls;
- mid-rank normal residual Z;
- five-fold train/held reliability W;
- independent `N_test=1000` test nulls;
- residual energy E and `p_exist`.

Namespaces for rep `r`:

- reference: `issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:reference`;
- test: `issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:test`.

## 10. Frozen first-reveal target comparison

Only after exact D0 replay may the scorer load the unchanged frozen ZL3b and IT2a target vectors.

For each rep report:

- E;
- `p_exist`;
- W;
- complete-66 `R_ZL3b`;
- complete-66 `R_IT2a`;
- sign agreement for each reading;
- `T=min(R_ZL3b,R_IT2a)`.

Never average the two readings.

## 11. Primary sufficiency decision

Reuse the exact Phase-A paired positive-control centers `T_plus_center[r]` and frozen q95 tolerance.

For each rep:

`D_M4[r]=T_M4[r]-T_plus_center_PhaseA[r]`.

Define:

`gap_M4=median_r D_M4[r]`.

If

`gap_M4 >= -0.009768313008182594`

classify:

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_SUFFICIENT`

and stop the R1 model-complexity ladder.

Otherwise classify:

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED`.

Only this latter outcome licenses a separately preregistered latent-state frontier.

## 12. Secondary diagnostics

Without changing the primary decision, report:

- paired `T_M4-T_M3` using the permanently frozen Phase-C 31-case values;
- q90/q99 sensitivity using already-frozen Phase-A M+ tolerances;
- fit-error, rank, and four identity audits by fold;
- descriptor class count and entropy;
- generated vs training unary/adjacent/distance moments;
- distinct signature count;
- E/p/W distributions;
- per-reading R and sign-agreement distributions.

No diagnostic may be used to alter Phase D after target reveal.

## 13. Falsifiable interpretation

### M4 succeeds

The replicated R1 topology can be generated by a compact occupancy grammar consisting of:

`K/R/S geometry + position-specific local transitions + generic separation-dependent nonlocal coupling`.

This would localize the remaining structure to a low-dimensional nonlocal distance law.

### M4 fails

Even after retaining the successful M3 local grammar, generic distance-banded nonlocal coupling is insufficient. That outcome would license a separately preregistered latent-state/configuration model rather than target-selected distant edges or an unrestricted pairwise model.

## 14. Interpretation boundary

Phase D concerns only the 12-slot occupancy representation. It cannot by itself establish:

- slot meanings;
- literal token spelling rules;
- plaintext letters or language;
- a cipher table;
- semantic absence;
- natural-language word boundaries;
- historical Naibbe use;
- decipherment.

## 15. Completion criterion

Phase D is complete only after all of the following are frozen and successful:

1. this corrected plan-before-code authority;
2. target-blind 31-case D0 generated-population authority;
3. exact replay preflight on reps 0 and 30;
4. target-blind rep0 candidate-owned-null smoke;
5. PRETARGET execution freeze;
6. complete 31/31 first reveal;
7. unchanged Phase-A paired M+ comparison;
8. permanent result freeze;
9. post-reveal report and hypothesis-ledger update;
10. classification under the decision rule above before any latent-state model is chosen.
