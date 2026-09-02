# Issue #75 Phase D — M4-KRS-CHAIN-DISTANCE implementation freeze

Date: 2026-09-01  
Status: **TARGET-BLIND AUTHORITATIVE IMPLEMENTATION FROZEN BEFORE VALID D0 EXECUTION**

## Chronology

- valid frozen Phase-C result commit: `9664e7cd1cf1eec8c2dacf37ceeb9c15c31a1f2a`;
- initial post-Phase-C `PLAN_D.md` commit: `1a56ef550af3ab65620ad32b2b4d6ba5aa7becc4` — superseded;
- obsolete distance-only draft executable: `1019378243dd145baa0a0da31a766558f312b0df` — non-authoritative;
- intermediate nested correction: `dcf652ef20418f230a1da9521ec036bb0c58e24c`;
- obsolete distance-only D0 run `33510176784` — failed at plan-diff gate before source checkout/generation and produced no target result;
- **final normative Phase-D preregistration:** `f9e60ed9e9261b30c3294c576cf7ea037cf2c2c7`;
- **first authoritative executable after final plan:** `ef8edcb94e287a3fd6c559308ff902dc7d1c41ee`;
- executable: `experiments/minimal-occupancy-generator/phase75d_generator_support.py`;
- corrected D0 launch run `33510519140` also failed at its chronology gate because it pinned the intermediate plan rather than the final plan; it stopped before source checkout, fitting, generation, Q/Z, or target access;
- no valid Phase-D D0 authority and no Phase-D target score exist at this freeze.

The scientific chronology that controls Phase D is therefore:

`frozen Phase-C failure -> final PLAN_D f9e60ed -> authoritative generator ef8edcb -> this implementation freeze -> valid D0`.

The stopped 20-parameter draft and both failed D0 launch attempts are provenance only and cannot be used as Phase-D evidence.

## Frozen model contract

Family: `M4-KRS-CHAIN-DISTANCE`.

Conditional on exact training-only `(K,R,S)`, the generator retains the Phase-C local grammar and adds only generic nonadjacent separation interactions:

- 11 free position-specific unary terms `h_1..h_11`, with `h_0=0`;
- 10 free position-specific adjacent terms `J_1..J_10`, with `J_0=0`;
- 8 free generic nonadjacent separation terms `B_3..B_10`;
- `B_2=0` fixes the nonadjacent common-offset gauge;
- `B_11=0` because `C_11=x_0*x_11=1[S=12]` is deterministic within fixed span;
- total **29 free continuous parameters per cross-fit training split**;
- zero named nonadjacent slot-pair parameters;
- zero complete-signature-specific parameters;
- zero latent-state parameters.

The executable must prove the complete-state within-`(K,R,S)` ranks:

- unary: `11`;
- unary + adjacent: `21`;
- all 33 reported features: `29`;
- selected 29-feature free basis: `29`.

## Training-moment contract

Report and reproduce all 33 training-only moments:

- 12 unary occupancies;
- 11 position-specific adjacent joint occupancies;
- 10 aggregate nonadjacent-distance occupancies for distances `2..11`.

Four exact descriptor identities are audited:

1. `sum U = K`;
2. `sum A = K-R`;
3. `sum C_2..C_11 = choose(K,2)-(K-R)`;
4. `C_11 = 1[S=12]`.

## Numerical contract

- exact 4095 non-empty state space;
- zero initialization;
- exact class-conditioned expectations/covariance;
- deterministic damped Newton updates;
- maximum absolute reported moment error `<=1e-10`;
- no Monte-Carlo fitting;
- no random fit initialization;
- no target-based tuning or regularization;
- failed fitting is failure, not reroll.

Target-blind numerical repair is permitted only for a demonstrable numerical implementation defect while the model family, sufficient statistics, gauges/fixed terms, target moments, tolerance, population, seed namespaces, and decision rule remain unchanged. Any repair must be documented before rerun.

## D0 population contract

- exactly 31 reps `0..30`;
- generation namespace `issue75:phaseD:M4-KRS-CHAIN-DISTANCE:rep{r}:fold{f}:generate`;
- frozen source/transcription and physical-fold authorities unchanged from Phase C;
- all target-access flags false;
- no Q/Z, target topology, correlation, sign agreement, or T in D0;
- no drops / no rerolls;
- exact occupancy SHA-256 for all 31 cases frozen before target access.

No Phase-D scorer or first-reveal target scoring is authorized until a valid D0 succeeds, is permanently fixed, exact replay passes, and the target-blind candidate-null smoke passes.
