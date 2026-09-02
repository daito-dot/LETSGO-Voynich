# Issue #75 Phase C — compact position-specific transition grammar

Status: **PREREGISTERED AFTER FROZEN M3 LICENSE / BEFORE PHASE-C EXECUTABLE / NO M3 TARGET RESULT**

Phase C is licensed only by the permanent Phase-B decision marker `DECISION_B_M3_LICENSED.md`.

## 1. Scientific question

Phase A showed that individual slot propensities and exact occupied-slot count K are insufficient, while empirical complete-signature resampling is sufficient.

Phase B then tested generic whole-pattern geometry `(K, occupied-run count R, occupied span S)` plus slot main effects.

The next deliberately narrow question is:

> **After coarse K/R/S geometry is fixed, are position-specific nearest-neighbor occupancy compatibilities sufficient to generate the replicated complete 66-edge residual topology?**

This phase tests one compact transition family only. It does not introduce arbitrary nonlocal pair terms, target-selected edges, a general latent HMM, or a 66-edge lookup table.

## 2. Frozen representation and authorities

Use the unchanged Issue #75 representation:

- parser-accepted token -> 12-bit occupied/empty vector;
- ZL3b source authority and physical-leaf five-fold split unchanged;
- 25,071 accepted tokens, fold counts `4430 / 4810 / 5516 / 5447 / 4868`;
- full 66-edge candidate-owned residual score unchanged;
- ZL3b and independent IT2a target vectors unchanged;
- Phase-A empirical-signature positive-control aggregate reused by exact SHA, not rerun or reselected.

Phase-C implementation must first verify the permanent Phase-B aggregate and its `M3 licensed` classification before generating any scientific corpus.

## 3. M3-KRS-CHAIN model

For non-empty occupancy vector `x in {0,1}^12`, retain the Phase-B generic descriptor

`D(x) = (K(x), R(x), S(x))`

where:

- `K` = occupied-slot count;
- `R` = number of contiguous occupied runs in frozen slot order `0..11`;
- `S` = occupied span from first to last occupied slot.

For each physical held-out fold, fit from the other four training folds only:

1. exact empirical training descriptor distribution `q_d=P_train(D=d)`;
2. conditional maximum-entropy distribution inside descriptor class `d`:

`P(x | D=d) ∝ exp(Σ_s h_s x_s + Σ_{s=0}^{10} J_s x_s x_{s+1})`.

The `h_s` are position-specific occupancy propensities. The `J_s` encode only adjacency in the already-frozen slot order.

No interaction between non-adjacent slots is permitted.

## 4. Identification / complexity

Conditional on fixed `(K,R,S)`:

- total occupied count `Σ_s x_s = K` is fixed, so a common offset across all `h_s` cancels;
- total number of occupied adjacent pairs is `K-R`, so a common offset across all `J_s` cancels.

Fix gauges:

- `h_0 = 0`;
- `J_0 = 0`.

Free parameters per cross-fit training split:

- 11 unary position parameters `h_1..h_11`;
- 10 adjacent interaction parameters `J_1..J_10`;
- total 21 continuous parameters;
- plus the already-licensed empirical K/R/S descriptor distribution inherited from Phase B.

Explicit non-adjacent pair interaction parameters: `0`.

Empirical complete-signature-specific parameters: `0`.

Report descriptor-distribution complexity separately from the 21 continuous transition parameters.

## 5. Training moments

Fit the 21 free parameters to exact training-only moments:

- the 12 slot occupancies `E[x_s]`;
- the 11 adjacent joint occupancies `E[x_s x_{s+1}]`.

Because q(K,R,S) fixes one linear sum among the unary moments and one linear sum among the adjacent-pair moments, only 21 moment degrees of freedom are independent, matching the two frozen gauges.

The executable must verify those implied identities before fitting.

No complete-66 target edge, held-out-fold moment, target R1 value, or target topology is used in training or model selection.

## 6. Deterministic exact-state fitting

Use the same exact 4095 non-empty signature state space as Phases A/B.

Required fit method:

- zero initialization of all 21 free parameters;
- exact expectation and covariance over all valid states in every nonzero descriptor class;
- deterministic Newton / damped moment matching;
- no Monte-Carlo fitting;
- no random initialization;
- frozen maximum absolute error `<=1e-10` over all 23 reported unary+adjacent moments, with the two dependent identities explicitly audited;
- a failed fit is a failed case, not manually repaired or rerolled.

Hardware-level bit identity of intermediate floating parameters is not required across runners. Exact training empirical moments, fit tolerance, model code/seed namespace, and exact final generated occupancy SHA are the replay authorities.

## 7. Cross-fitted generated population

Generate exactly 31 complete M3-KRS-CHAIN corpora, reps `0..30`.

For held-out fold `f`, sample only from the model fit on the other four folds.

Generation namespace:

`issue75:phaseC:M3-KRS-CHAIN:rep{r}:fold{f}:generate`

Every corpus must contain exactly 25,071 non-empty signatures on the frozen accepted-token/line skeleton.

No drops. No rerolls.

## 8. Mandatory target-blind Stage C0 authority

Before any M3 target scoring:

1. fit all five cross-fit M3 models;
2. record exact training K/R/S distributions;
3. record exact unary and adjacent training moments;
4. record all fitted parameters and fit errors;
5. generate all 31 corpora;
6. freeze exact occupancy SHA-256 for each corpus;
7. record generated slot marginals, adjacent occupancies, K/R/S distribution and distinct signature counts;
8. explicitly assert target vectors, pair Q, residual Z, target correlations and Phase-C classification were not computed.

The later scorer must regenerate a requested corpus and require exact C0 occupancy SHA before target access.

## 9. Candidate-owned residual calibration

Reuse the exact unchanged Phase-A/B R1 scoring machinery:

- all 66 unordered slot pairs;
- K_other-conditioned Jeffreys-smoothed MH/Yule-Q association;
- `N_ref=1000` line-local reference nulls;
- mid-rank normal residual Z;
- five-fold train/held reliability W;
- independent `N_test=1000` test nulls;
- residual energy E and `p_exist`.

Namespaces for rep r:

- reference: `issue75:phaseC:M3-KRS-CHAIN:rep{r}:reference`
- test: `issue75:phaseC:M3-KRS-CHAIN:rep{r}:test`

## 10. Frozen target comparison

Only after exact C0 replay may the scorer load the unchanged frozen ZL3b and IT2a target vectors.

Report for each rep:

- E;
- `p_exist`;
- W;
- complete-66 `R_ZL3b`;
- complete-66 `R_IT2a`;
- sign agreement for each reading;
- `T=min(R_ZL3b,R_IT2a)`.

Never average the two readings.

## 11. Frozen positive-control authority / primary decision

Reuse the exact permanent Phase-A positive control:

- aggregate SHA-256 `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`;
- 31 frozen paired `T_plus_center[r]` values;
- already-passed M+ calibration;
- q95 `delta_plus = 0.009768313008182594`.

For each rep:

`D_M3[r] = T_M3[r] - T_plus_center_PhaseA[r]`.

Define:

`gap_M3 = median_r D_M3[r]`.

If

`gap_M3 >= -0.009768313008182594`

classify:

`M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_SUFFICIENT`

and **stop the R1 model-complexity ladder**. Do not add a richer R1 model merely to increase fit.

Otherwise classify:

`M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED`.

A failure licenses only a new separately preregistered frontier. It does not identify which nonlocal or latent architecture is correct.

## 12. Required diagnostics

Report without changing the primary q95 decision:

- fit error and moment identities by fold;
- descriptor class counts/entropy;
- generated vs training unary/adjacent moments;
- generated K/R/S distributions;
- distinct signature count;
- E/p/W distributions;
- per-reading R/sign distributions;
- q90/q99 sensitivity using the already-frozen Phase-A M+ self-difference tolerances;
- comparison with permanently frozen M1 and M2 results as descriptive context only.

## 13. Interpretation boundary

M3 success would establish a compact **occupancy-level nearest-neighbor compatibility grammar** as sufficient for R1 under this representation.

It would not establish:

- meanings for slots;
- literal Voynich token spellings;
- plaintext letters;
- a cipher table;
- natural-language word boundaries;
- historical Naibbe use;
- decipherment.

## 14. Completion criterion

Phase C is complete only after:

1. this plan is committed before all Phase-C executable code;
2. 31 M3 corpora are target-blind frozen with exact SHA authority;
3. exact replay preflight succeeds;
4. candidate-owned null smoke succeeds without target access;
5. all 31 first-reveal scores complete with no drops/rerolls;
6. comparison uses the unchanged Phase-A positive-control authority and q95 rule;
7. first-reveal evidence is permanently archived;
8. the frozen result determines whether the R1 complexity ladder stops or a new frontier must be preregistered.
