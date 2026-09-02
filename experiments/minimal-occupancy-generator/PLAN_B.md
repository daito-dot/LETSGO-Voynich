# Issue #75 Phase B — generic occupancy-shape sufficiency

Status: **PREREGISTERED BEFORE PHASE-B EXECUTABLE / NO M2 TARGET RESULT**

Parent authority:

- Phase A plan `8d984cfa61a5616bef61b45248c0a7a5d213fbf8`;
- Phase A frozen classification `LOW_ORDER_MODELS_INSUFFICIENT_EMPIRICAL_PATTERN_STRUCTURE_REQUIRED`;
- Phase A aggregate SHA-256 `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`;
- Phase A permanent authority commit `5059eaf60d5725e65895c8c0fac8dfe859151cf7`.

## 1. Why Phase B is licensed

Phase A established prospectively that:

- M0 individual slot marginals fail strongly;
- M1 slot marginals + occupied-slot count `K` fail strongly;
- two independent cross-fitted empirical-signature resampling controls succeed strongly (`T≈0.965`).

M1 is especially diagnostic: it produces residual energy around the empirical control (`E≈3.25`) but the complete 66-edge topology is mildly anticorrelated with both frozen readings.

Therefore the missing information concerns **which subsets of the 12 slots are selected together**, beyond how many slots are selected.

Phase B tests exactly one generic shape family before any latent/state generator is licensed.

## 2. Primary question

> **Can generic geometry of a 12-bit occupancy pattern — occupied-slot count, number of contiguous occupied runs, and occupied span — together with slot main effects explain the replicated 66-edge residual topology without empirical signature memorization or pair-specific parameters?**

This phase does not implement M3 or any latent/state model.

## 3. Frozen source / cross-fitting / targets

Use exactly the Phase-A source and representation:

- `matthewdgreen/cipher_benchmark` commit `315f0cad4de3d021bd4185765c037cf2a28d341c`;
- ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- `SlotParser(min)`;
- physical-leaf five-fold split from #58B/#58C;
- 25,071 accepted tokens;
- fold counts `4430 / 4810 / 5516 / 5447 / 4868`.

All Phase-B model parameters are fit separately for each held-out fold using only the other four folds.

Target vectors remain frozen Issue58C/Issue58D authorities and may not be loaded until the generated M2 population is target-blind frozen and exact-replay preflight succeeds.

## 4. Generic shape descriptors

For one non-empty occupancy signature `x in {0,1}^12`, define:

### K — occupied-slot count

`K(x) = sum_s x_s`, range `1..12`.

### R — occupied-run count

Read slots in frozen order `0..11`.

`R(x)` is the number of maximal contiguous runs of occupied slots.

Examples:

- `001110000000` -> `R=1`;
- `001010010000` -> `R=3`.

### S — occupied span

Let `first(x)` and `last(x)` be the first and last occupied slot.

`S(x) = last(x) - first(x) + 1`, range `1..12`.

For any one-slot pattern, `K=R=S=1`.

These descriptors are generic geometry of a binary pattern. They are not chosen from the observed 66 target edges.

## 5. M2-KRS model

Scientific role:

> test whether coarse pattern geometry plus slot location propensity is sufficient.

For each cross-fit training split, estimate the exact empirical training-only joint descriptor distribution:

`q_d = P_train(D=d)`, where `D=(K,R,S)`.

Then generate a descriptor class `d` from `q_d`.

Conditional on `D=d`, sample a complete occupancy signature from the maximum-entropy main-effect model

`P(x | D=d) ∝ exp(sum_s lambda_s x_s)`

restricted to the non-empty state-space signatures satisfying exactly

`(K(x), R(x), S(x)) = d`.

Because every descriptor class fixes K, adding a common constant to all `lambda_s` cancels. Freeze `lambda_0=0` and fit the remaining 11 slot main-effect parameters so that the model's unconditional 12 slot occupancies match the training-only empirical slot marginals.

No slot-pair interaction, selected edge, target residual value, target correlation, empirical complete-signature probability or latent state is permitted.

## 6. Complexity accounting

For every cross-fit fold report:

- number of nonzero `(K,R,S)` descriptor classes;
- descriptor-distribution entropy;
- at most `n_classes - 1` independent descriptor probabilities;
- 11 free slot main-effect parameters;
- 0 explicit pair-interaction parameters;
- 0 empirical signature-specific parameters.

Also report the number of possible 12-bit signatures covered by each descriptor class and the training number of distinct complete signatures.

The purpose is to make clear how far M2 remains from empirical-signature resampling.

## 7. Deterministic fitting

Use the exact 4095 non-empty signature state space in ascending integer-mask order.

Fit the 11 main effects deterministically:

- zero initialization;
- exact state-space expectations/covariances;
- deterministic Newton/damped moment matching;
- same scientific fit tolerance as Phase A: maximum absolute slot-marginal error `<=1e-10`;
- no random initialization;
- no target loss.

A descriptor class with zero training probability is not generated.

All nonzero training descriptor classes must contain at least one valid 12-bit state by definition. No class may be silently merged or dropped.

## 8. Frozen M2 population

Generate exactly 31 complete cross-fitted M2-KRS corpora, reps `0..30`.

For held-out fold `f`, generation namespace:

`issue75:phaseB:M2-KRS:rep{r}:fold{f}:generate`

No rerolls.

Each realization contains exactly the Phase-A accepted-token/line skeleton:

- total 25,071 signatures;
- exact fold counts `4430 / 4810 / 5516 / 5447 / 4868`;
- no all-zero signature.

## 9. Mandatory Stage B0 target-blind authority

Before target access:

1. fit all five cross-fit M2 models;
2. freeze descriptor distributions, complexity diagnostics and fit parameters;
3. generate all 31 corpora;
4. record exact occupancy SHA-256 for every corpus;
5. record generated slot marginals and `(K,R,S)` distributions;
6. record distinct signature counts;
7. explicitly assert no Q, residual Z, target load, correlation or classification.

The later scorer must regenerate the requested corpus and require exact frozen occupancy SHA before target loading.

As in Phase A, hardware-level last-bit equality of intermediate floating Newton parameters is not itself a scientific authority. Exact training empirical statistics, fit tolerance and final generated occupancy SHA are the replay authorities.

## 10. Candidate-owned residual calibration

Reuse the exact Phase-A scoring construct without modification:

- all 66 unordered pairs;
- `K_other`-conditional Jeffreys-smoothed MH/Yule-Q association;
- `N_ref=1000` candidate-owned line-local reference nulls;
- mid-rank normal residual Z;
- five-fold reliability W;
- independent `N_test=1000` candidate-owned test nulls;
- residual energy E and `p_exist`.

Namespaces for rep `r`:

- reference: `issue75:phaseB:M2-KRS:rep{r}:reference`
- test: `issue75:phaseB:M2-KRS:rep{r}:test`

## 11. Frozen target comparison

Only after exact B0 corpus replay may the scorer load the unchanged frozen target vectors.

For each rep report:

- E;
- `p_exist`;
- W;
- complete-66 `R_ZL3b`;
- complete-66 `R_IT2a`;
- sign agreement against each reading;
- `T=min(R_ZL3b,R_IT2a)`.

Do not average the two readings.

## 12. Reuse of frozen Phase-A positive control

Phase B does not rerun empirical-signature positive controls.

Use the permanently frozen Phase-A M+ paired values exactly as calibration authority:

- aggregate SHA-256 `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`;
- MPLUS-A median T `0.9643123238628766`;
- MPLUS-B median T `0.9655940679816023`;
- both already passed `T_control_floor=0.9447148364`;
- frozen paired `T_plus_center[r]`, `r=0..30`;
- frozen q95 bank self-difference `delta_plus=0.009768313008182594`.

These values predate all Phase-B target results and must be loaded directly from the permanent Phase-A aggregate, not recomputed from a selected subset.

## 13. Frozen primary decision

For each rep `r`:

`D_M2[r] = T_M2[r] - T_plus_center_PhaseA[r]`.

Define:

`gap_M2 = median_r D_M2[r]`.

### M2 sufficient

If

`gap_M2 >= -0.009768313008182594`

classify:

`M2_GENERIC_KRS_SHAPE_DESCRIPTORS_SUFFICIENT`

Interpretation:

> generic token geometry `(K,R,S)` plus slot main effects is sufficient within previously frozen empirical-inventory stochastic variation.

Do not proceed to M3 merely because it could fit better.

### M2 insufficient

If

`gap_M2 < -0.009768313008182594`

classify:

`M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED`

This outcome licenses a separately preregistered M3 compact state/transition generator.

The continuous gap and all reading-specific values are primary evidence regardless of category.

## 14. Non-promoting diagnostics

After the frozen primary classification report:

- q90/q99 Phase-A M+ tolerance sensitivity using the already frozen Phase-A paired values;
- descriptor class counts / entropy;
- generated vs training K/R/S distributions;
- generated vs training slot marginals;
- distinct complete-signature count;
- E/p/W distributions;
- reading-specific R/sign distributions;
- per-fold fit diagnostics.

These may not redefine the q95 result.

## 15. Criterion Validity Table

| Claim | Construct | Metric | Threshold | Source | Failure meaning |
|---|---|---|---|---|---|
| M2 fit is scientifically identical to frozen model | training K/R/S distribution + slot marginals | exact empirical stats; max moment error | exact stats; error `<=1e-10` | T1 plan | implementation invalid; stop before target |
| generated case is exactly preregistered | complete cross-fitted occupancy corpus | SHA-256 | exact B0 SHA | T1 B0 | no target access; no reroll |
| candidate creates residual object | complete 66-edge candidate residual | E/p/W | descriptive, same as Phase A | T2/T3 context | report; cannot rescue topology class |
| generic KRS shape is sufficient | topology relative to frozen empirical-signature control | `gap_M2` | `>= -0.009768313008182594` | T2 Phase-A M+ self variation | K/R/S geometry lacks required configuration information |

## 16. Interpretation boundaries

M2 success would identify a sufficient **occupancy-shape statistic**, not:

- meanings for slots;
- literal token spelling;
- natural-language word morphology;
- plaintext;
- cipher table;
- historical mechanism;
- decipherment.

M2 failure would show only that `(K,R,S)+slot main effects` is insufficient. It would not prove a particular M3 state architecture.

## 17. Completion criterion

Phase B is complete only after:

1. this plan predates all Phase-B executable code;
2. 31 M2 corpora are target-blind frozen with exact SHA authority;
3. exact replay preflight succeeds;
4. no cases are dropped/rerolled;
5. all 31 target scores complete under the unchanged candidate-null/target machinery;
6. the frozen Phase-A M+ calibration is used unchanged;
7. the exact q95 decision above is computed;
8. first-reveal evidence is permanently frozen and reported before any M3 design is implemented.
