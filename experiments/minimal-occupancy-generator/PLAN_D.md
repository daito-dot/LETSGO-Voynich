# Issue #75 Phase D — nested distance-banded nonlocal occupancy grammar

Date: 2026-09-01  
Status: **FINAL PREREGISTRATION / BEFORE AUTHORITATIVE PHASE-D EXECUTABLE / NO PHASE-D GENERATED POPULATION OR TARGET RESULT**

## 0. Authority and chronology

Phase D is licensed only by the valid frozen Phase-C outcome:

- Phase-C first-reveal run: `33508975967` — success;
- scientific head: `8d02507355f428ffc80d590bbcfe256ce9fd0d95`;
- permanent result commit: `9664e7cd1cf1eec8c2dacf37ceeb9c15c31a1f2a`;
- aggregate SHA-256: `34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a`;
- classification: `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED`;
- `gap_M3=-0.37325753997796984`;
- frozen q95 allowed loss: `0.009768313008182594`.

The controlling decision file is `DECISION_C_NONLOCAL_OR_LATENT_REQUIRED.md`.

### Phase-D preregistration repair

The historical `.github/workflows/issue75-phaseD-preregister-if-licensed.yml` belonged to the broken pre-recovery Phase-C automation chain and is non-authoritative.

After the valid Phase-C result, commit `1a56ef550af3ab65620ad32b2b4d6ba5aa7becc4` created an initial distance-only plan and commit `1019378243dd145baa0a0da31a766558f312b0df` created a corresponding draft generator. Before that draft generator was scientifically executed, the plan was audited and two target-independent design defects were found:

1. the distance-only model discarded the position-specific adjacent interactions that Phase C had already shown to carry substantial topology signal, so it was not a nested extension of M3;
2. conditioning on span `S` makes distance-11 occupancy deterministic, adding an identifiability constraint omitted by the 20-parameter draft.

Commit `dcf652ef20418f230a1da9521ec036bb0c58e24c` corrected the scientific design to a nested 29-parameter model. The first attempted D0 run, `33510176784`, stopped at its chronology gate before source checkout, fitting, corpus generation, Q/Z computation, or target access because it correctly detected that the plan had changed.

Therefore:

- draft executable `101937...` is non-authoritative and must not be executed or scored;
- no Phase-D corpus has been generated under scientific authority;
- no Phase-D Q, Z, target correlation, sign agreement, or T exists;
- this file is the **final normative Phase-D plan**;
- the authoritative Phase-D executable must be committed only after this final plan commit.

## 1. Scientific question

Phase A ruled out slot marginals and occupied-slot count alone. Phase B showed that coarse `(K,R,S)` geometry recovers only a modest part of R1. Phase C retained `(K,R,S)` and added position-specific nearest-neighbor occupancy interactions, raising median `T` from about `0.287` to about `0.593`, while remaining far below the empirical-signature positive-control ceiling near `0.965`.

The next deliberately narrow question is:

> **If the successful M3 local transition grammar is retained, are generic nonadjacent interactions determined only by slot separation sufficient to recover the replicated complete 66-edge topology?**

This is a strict nested extension of M3. It adds no target-selected pair and no latent state.

## 2. Frozen representation and evaluation

Use the unchanged Issue #75 representation and evaluation:

- parser-accepted token -> 12-bit occupancy vector;
- `SlotParser(min)` authority unchanged;
- 25,071 accepted ZL3b tokens on the frozen physical-leaf skeleton;
- five physical-leaf cross-fit folds unchanged;
- exact training-only empirical `(K,R,S)` descriptor distribution per split;
- all 66 unordered slot pairs retained;
- candidate-owned K_other-conditioned Jeffreys-smoothed MH/Yule-Q reference null;
- mid-rank normal residual Z, E, `p_exist`, and physical-fold reliability W;
- ZL3b and IT2a evaluated separately;
- `T=min(R_ZL3b,R_IT2a)`;
- exact Phase-A paired M+ centers from SHA `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`;
- q95 no-material-loss tolerance `0.009768313008182594`.

The Phase-C result may be used only as prior-stage authority and a descriptive paired comparator. No Phase-D feature, band, parameter, seed, or variant may be chosen from revealed target-edge values, signs, or residual magnitudes.

## 3. M4-KRS-CHAIN-DISTANCE model

For non-empty `x in {0,1}^12`, retain descriptor

`D(x)=(K(x),R(x),S(x))`

with exact training-only distribution `q_d=P_train(D=d)`.

Within each descriptor class define:

- unary `U_s(x)=x_s`, `s=0..11`;
- position-specific adjacent feature `A_s(x)=x_s*x_{s+1}`, `s=0..10`;
- aggregate nonadjacent separation feature `C_d(x)=sum_{s=0}^{11-d} x_s*x_{s+d}`, `d=2..11`.

Conditional model:

`P(x|K,R,S) proportional to exp(sum_s h_s U_s + sum_s J_s A_s + sum_{d=2}^{11} B_d C_d)`.

M3 is recovered exactly when all identifiable `B_d` are zero. The only new information channel is generic nonadjacent separation distance.

Forbidden in M4:

- named-pair-specific nonadjacent coefficients;
- empirical complete-signature parameters;
- latent states or mixture classes;
- target-derived feature selection.

## 4. Exact identification and complexity

Conditioning on `(K,R,S)` creates four invariant parameter directions.

1. `sum_s U_s=K` -> gauge `h_0=0`; 11 free unary terms.
2. `sum_s A_s=K-R` -> gauge `J_0=0`; 10 free adjacent terms `J_1..J_10`.
3. `sum_{d=2}^{11} C_d=choose(K,2)-(K-R)` -> common nonadjacent-distance offset cancels; gauge `B_2=0`.
4. `C_11=x_0*x_11` is deterministic from span: `C_11=1` iff `S=12`, otherwise `0`; therefore `B_11=0` and is omitted.

Free parameters per training split:

- 11 unary;
- 10 position-specific adjacent;
- 8 generic nonadjacent distance terms `B_3..B_10`;
- total **29**.

The executable must perform an exact within-descriptor feature-rank audit over the full 4095-state space and confirm:

- unary rank `11`;
- unary + adjacent rank `21`;
- unary + adjacent + identifiable distance rank `29`.

## 5. Training-only moments and identities

Fit only the four training folds to reproduce all reported empirical moments:

- 12 unary occupancies `E[U_s]`;
- 11 position-specific adjacent occupancies `E[A_s]`;
- 10 aggregate nonadjacent-distance occupancies `E[C_d]`, `d=2..11`.

Report all 33 moments. The executable must verify four exact descriptor-induced identities:

- unary sum equals `E_q[K]`;
- adjacent sum equals `E_q[K-R]`;
- distance sum equals `E_q[choose(K,2)-(K-R)]`;
- distance-11 moment equals `P_q(S=12)`.

Only the 29 identifiable coordinates are parameterized. No held-out-fold or target R1 quantity enters fitting.

## 6. Exact deterministic fitting

Use the complete 4095 non-empty signature state space.

Required procedure:

- zero initialization of all 29 free parameters;
- exact expectation and covariance within every nonzero `(K,R,S)` class;
- deterministic Newton / damped moment matching;
- no Monte-Carlo fitting;
- no random initialization;
- no target-derived regularization or feature pruning;
- maximum absolute error `<=1e-10` across all 33 reported moments;
- failed fold fit is failure, not reroll.

Deterministic numerical stabilization is allowed only if it leaves the model family, sufficient statistics, target moments, gauges, tolerance, population, and decision rule unchanged.

## 7. Target-blind D0 population

Generate exactly 31 complete cross-fitted `M4-KRS-CHAIN-DISTANCE` corpora, reps `0..30`, on the unchanged accepted-token/line skeleton. Held-out fold `f` is generated from a model fitted only on the other four folds.

Namespace:

`issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:fold{f}:generate`.

Each corpus must contain exactly 25,071 non-empty signatures. Before any target access freeze:

- occupancy SHA-256 for every rep;
- token/fold counts;
- training descriptor distribution;
- all 33 training and fitted moments;
- fitted parameters and max fit error;
- rank/identity audit;
- generated descriptor and distinct-signature diagnostics;
- all target-access flags false;
- no drops / no rerolls.

## 8. Required pretarget validation

Before first reveal:

1. reps `0` and `30` must regenerate exact D0 occupancy SHAs;
2. rep0 candidate-null smoke must complete 1000 reference + 1000 test nulls while target vectors remain unloaded;
3. scorer and aggregator must be frozen;
4. a PRETARGET execution freeze must pin all exact authorities;
5. all target-access guards must pass.

## 9. Candidate-owned R1 measurement

Reuse the unchanged Phase-A/B/C scoring contract:

- all 66 pairs;
- K_other-conditioned Jeffreys-smoothed MH/Yule-Q;
- `N_ref=1000` reference nulls;
- mid-rank normal residual Z;
- five-fold train/held reliability W;
- `N_test=1000` independent test nulls;
- E and `p_exist`.

Namespaces:

- `issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:reference`;
- `issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:test`.

## 10. Frozen first-reveal comparison

Only after exact D0 replay and PRETARGET authorization may unchanged ZL3b and IT2a target vectors be loaded.

For every rep report E, `p_exist`, W, complete-66 R for each reading, sign agreement for each reading, and `T=min(R_ZL3b,R_IT2a)`. Never average readings.

Reuse exact Phase-A paired positive-control centers:

`D_M4[r]=T_M4[r]-T_plus_center_PhaseA[r]`

`gap_M4=median_r D_M4[r]`.

No case may be selected, dropped, replaced, or rerolled.

## 11. Frozen primary decision

If

`gap_M4 >= -0.009768313008182594`

classify

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_SUFFICIENT`

and stop the R1 model-complexity ladder.

Otherwise classify

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED`.

Only the latter licenses a separately preregistered latent-state frontier. No latent architecture is selected or fitted in Phase D.

## 12. Secondary diagnostics

Non-promoting diagnostics only:

- paired `T_M4-T_M3` using frozen Phase-C 31-case values;
- q90/q99 frozen M+ tolerance sensitivity;
- fit, rank, and four identity audits;
- descriptor class count/entropy;
- generated vs training unary/adjacent/distance moments;
- distinct-signature count;
- E/p/W distributions;
- per-reading R/sign distributions.

No diagnostic may alter Phase D after target reveal.

## 13. Falsifiable interpretation

If M4 succeeds, the replicated R1 topology is explainable by

`K/R/S geometry + position-specific local transitions + generic separation-dependent nonlocal coupling`.

If M4 fails, even this nested generic nonlocal extension is insufficient, licensing a separately preregistered latent-state/configuration model rather than target-selected distant edges or an unrestricted pairwise model.

## 14. Boundary

Phase D concerns only 12-slot occupancy. It does not establish slot meanings, literal spelling, plaintext, language, cipher table, semantic absence, word boundaries, historical Naibbe use, or decipherment.

## 15. Completion criterion

Phase D requires, in order:

1. this final plan-before-authoritative-code freeze;
2. target-blind 31-case D0 authority;
3. exact replay preflight reps 0/30;
4. target-blind rep0 candidate-null smoke;
5. PRETARGET freeze;
6. complete 31/31 first reveal;
7. unchanged Phase-A paired M+ comparison;
8. permanent result freeze;
9. report and hypothesis-ledger update;
10. frozen classification before any latent-state model is chosen.
