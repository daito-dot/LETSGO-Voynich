# Issue #75 Phase D — compact distance-banded nonlocal occupancy grammar

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

The earlier `.github/workflows/issue75-phaseD-preregister-if-licensed.yml` was authored during the broken Phase-C automation chain. It is **non-authoritative**. Its generic distance-banded idea is retained because it is target-edge blind, but this `PLAN_D.md`, committed after the valid frozen Phase-C result and before any Phase-D executable, is the sole normative Phase-D plan.

No Phase-D target result exists at this point.

## 1. Scientific question

Phase A ruled out slot marginals and occupied-slot count alone. Phase B showed that coarse `(K,R,S)` token geometry recovers only a modest part of R1. Phase C added a first-order nearest-neighbor occupancy grammar and raised median `T` from about `0.287` to about `0.593`, but remained far below the empirical-signature positive-control ceiling near `0.965`.

The next deliberately narrow question is:

> **After exact K/R/S geometry is fixed, can generic nonlocal interaction determined only by separation distance — without selecting any particular revealed target edge — recover the replicated complete 66-edge topology?**

This phase tests the simplest nonlocal extension before considering a latent-state model.

## 2. Frozen representation and evaluation

Use the unchanged Issue #75 representation and complete-graph evaluation:

- parser-accepted token -> 12-bit occupancy vector;
- `SlotParser(min)` authority unchanged;
- 25,071 accepted ZL3b tokens on the frozen physical-leaf skeleton;
- five physical-leaf cross-fit folds unchanged;
- all `C(12,2)=66` unordered slot pairs retained;
- candidate-owned K_other-conditioned Jeffreys-smoothed MH/Yule-Q reference null;
- residual Z, residual energy E, existence p-value, physical-fold reliability W;
- ZL3b and IT2a target vectors evaluated separately;
- `T=min(R_ZL3b,R_IT2a)`;
- exact Phase-A paired M+ positive-control centers reused;
- q95 no-material-loss tolerance remains exactly `0.009768313008182594`.

No selected-edge score, subset correlation, or post-reveal topology repair is permitted.

## 3. M4-KRS-DISTANCE model

Retain the exact training-only empirical descriptor distribution

`q_d = P_train(K,R,S)`.

For a non-empty 12-bit occupancy vector `x`, define for separation distance `d=2..11`:

`C_d(x) = sum_{s=0}^{11-d} x_s x_{s+d}`.

Conditional on descriptor class `(K,R,S)`, define

`P(x | K,R,S) proportional to exp(sum_s h_s x_s + sum_{d=2}^{11} J_d C_d(x))`.

The model therefore contains:

- position-specific unary occupancy propensities `h_s`;
- one shared interaction coefficient for each nonadjacent separation distance;
- no coefficient for a particular named nonadjacent slot pair;
- no complete-signature-specific parameter;
- no latent state or mixture class.

Distance 1 is deliberately absent. Within fixed `(K,R,S)`, the number of occupied adjacent pairs is exactly `K-R`, so a shared distance-1 coefficient is constant within the descriptor class and cannot alter the conditional distribution.

## 4. Identification and complexity

Within fixed K, total unary occupancy is fixed. Set gauge:

`h_0 = 0`.

Within fixed K and R, total nonadjacent occupied-pair count is also fixed:

`sum_{d=2}^{11} C_d = choose(K,2) - (K-R)`.

Therefore a common offset across all nonadjacent distance coefficients cancels. Set gauge:

`J_2 = 0`.

Free continuous parameters per cross-fit training split:

- 11 unary parameters `h_1..h_11`;
- 9 distance parameters `J_3..J_11`;
- total: `20`.

Complexity assertions:

- explicit pair-specific nonadjacent parameters: `0`;
- empirical complete-signature-specific parameters: `0`;
- latent-state parameters: `0`.

## 5. Training-only sufficient statistics

Fit only from the four training folds to reproduce:

- all 12 slot occupancy means;
- all 10 aggregate nonadjacent distance occupancies `E[C_d]`, `d=2..11`.

The frozen `(K,R,S)` distribution imposes:

- one linear identity among the 12 unary moments;
- one linear identity among the 10 distance moments.

After gauges, this gives 20 independent moment degrees of freedom, matching the 20 free continuous parameters.

Both identities must be numerically verified before fitting. The target graph, target edge signs, target correlations, and IT2a outcomes must not be loaded or used during fitting.

## 6. Exact deterministic fitting

Use the exact 4095 non-empty 12-bit signature state space.

Required fitting procedure:

- zero initialization;
- exact expectations within every nonzero `(K,R,S)` class;
- exact covariance/Jacobian over the 20 free sufficient statistics;
- deterministic Newton or damped Newton moment matching;
- no Monte Carlo fitting;
- no random initialization;
- no target-based hyperparameter selection;
- maximum absolute error `<=1e-10` across all reported unary and distance moments;
- a failed fold fit is an experimental failure, not a reroll.

The solver may use deterministic numerical stabilization only if it does not change the model family, objective, target moments, or stopping tolerance.

## 7. Target-blind D0 population

Generate exactly 31 cross-fitted M4-KRS-DISTANCE corpora, reps `0..30`, on the frozen accepted-token/line skeleton.

Generation namespace:

`issue75:phaseD:M4-KRS-DISTANCE:rep{r}:fold{f}:generate`

Before any target access, freeze for all 31 cases:

- exact occupancy SHA-256;
- token count and fold counts;
- descriptor and moment-fit audit;
- distinct-signature diagnostics;
- all target-access flags false;
- no drops / no rerolls.

The D0 population must be permanently committed or otherwise immutable by exact SHA before target scoring is authorized.

## 8. Candidate-owned residual calibration

Reuse the exact unchanged R1 candidate-owned calibration contract:

- all 66 unordered pairs;
- K_other-conditioned Jeffreys-smoothed MH/Yule-Q;
- `N_ref=1000` candidate-owned line-local reference nulls;
- residual Z;
- five-fold reliability W;
- `N_test=1000` independent candidate-owned test nulls;
- E and `p_exist`.

Namespaces:

- `issue75:phaseD:M4-KRS-DISTANCE:rep{r}:reference`
- `issue75:phaseD:M4-KRS-DISTANCE:rep{r}:test`

First run exact target-blind replay preflight on reps `0` and `30`. Then run one target-blind rep0 candidate-null smoke. Neither may load Issue58C/Issue58D target vectors or compute target correlation/sign agreement/T.

## 9. Frozen first-reveal target comparison

Only after D0, boundary replay, candidate-null smoke, and a PRETARGET execution freeze succeed may target vectors be loaded.

For each rep `r=0..30`, report:

- E;
- `p_exist`;
- W;
- `R_ZL3b`;
- `R_IT2a`;
- sign agreement against each reading;
- `T[r]=min(R_ZL3b,R_IT2a)`.

Reuse the exact Phase-A paired positive-control center for the same rep:

`D_M4[r] = T_M4[r] - T_plus_center_PhaseA[r]`

and

`gap_M4 = median_r D_M4[r]`.

No case may be dropped, replaced, selected, or rerolled. ZL3b and IT2a may not be averaged.

## 10. Frozen decision rule

Primary threshold remains:

`delta_plus_q95 = 0.009768313008182594`.

If

`gap_M4 >= -0.009768313008182594`

classify:

`M4_KRS_DISTANCE_BANDED_NONLOCAL_GRAMMAR_SUFFICIENT`

and **stop the R1 model-complexity ladder**.

Otherwise classify:

`M4_KRS_DISTANCE_BANDED_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED`.

Only the latter outcome licenses a separately preregistered latent-state frontier. No latent architecture is selected or fitted in Phase D.

q90/q99 positive-control tolerances may be reported only as non-promoting sensitivity checks, exactly as in Phases A-C.

## 11. Falsifiable interpretation

### M4 succeeds

Generic dependence on structural separation distance is sufficient, once K/R/S geometry is fixed. This would identify a compact nonlocal occupancy law without naming specific slot pairs.

### M4 fails

Even generic distance-banded nonlocal coupling is insufficient. Combined with M3 failure, this would strongly motivate a latent configuration/state explanation rather than simply adding pair-specific interactions.

Failure does **not** license target-selected distant edges or an unrestricted pairwise model.

## 12. Interpretation boundary

Phase D concerns only the 12-slot occupancy representation. It cannot by itself establish:

- slot meanings;
- literal token spelling rules;
- plaintext letters or language;
- a cipher table;
- semantic absence;
- natural-language word boundaries;
- historical Naibbe use;
- decipherment.

Success would identify an occupancy-level distance law. Failure would establish only that such a law is insufficient under the tested hierarchy.

## 13. Completion criterion

Phase D is complete only after all of the following are frozen and successful:

1. this plan-before-code authority;
2. target-blind 31-case D0 generated-population authority;
3. exact replay preflight on reps 0 and 30;
4. target-blind rep0 candidate-owned-null smoke;
5. PRETARGET execution freeze;
6. complete 31/31 first reveal;
7. unchanged Phase-A paired M+ comparison;
8. permanent result freeze;
9. post-reveal report and hypothesis-ledger update;
10. classification under the decision rule above before any latent-state model is chosen.
