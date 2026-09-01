# Issue #75 Phase D — M4-KRS-DISTANCE implementation freeze

Date: 2026-09-01  
Status: **TARGET-BLIND IMPLEMENTATION FROZEN BEFORE D0 EXECUTION**

## Chronology

- normative Phase-D plan commit: `1a56ef550af3ab65620ad32b2b4d6ba5aa7becc4`
- first Phase-D executable commit: `1019378243dd145baa0a0da31a766558f312b0df`
- executable: `phase75d_generator_support.py`
- the generator commit is after the plan commit;
- no Phase-D target score exists at this freeze.

## Frozen model contract

Family: `M4-KRS-DISTANCE`.

Conditional on training-only `(K,R,S)`, the generator uses:

- 11 free position-specific unary terms `h_1..h_11`, gauge `h_0=0`;
- 9 free generic separation-distance terms `J_3..J_11`, gauge `J_2=0`;
- 20 free continuous parameters per cross-fit training split;
- zero named nonadjacent slot-pair parameters;
- zero complete-signature-specific parameters;
- zero latent-state parameters.

Target training moments are the 12 unary occupancies and 10 aggregate nonadjacent distance occupancies for distances `2..11`. The two descriptor-induced linear identities are explicitly audited.

## Numerical contract

- exact 4095 non-empty state space;
- zero initialization;
- exact class-conditioned expectations/covariance;
- deterministic damped Newton updates;
- maximum absolute reported moment error `<=1e-10`;
- no random fit initialization;
- no target-based tuning;
- failed fitting is failure, not reroll.

Target-blind numerical repair is permitted only if D0 fails for a demonstrable numerical reason while the model family, sufficient statistics, gauges, target moments, tolerance, population, and decision rule remain unchanged. Any such repair must be documented before rerun.

## D0 population contract

- exactly 31 reps `0..30`;
- generation namespace `issue75:phaseD:M4-KRS-DISTANCE:rep{r}:fold{f}:generate`;
- frozen source/transcription and physical-fold authorities unchanged from Phase C;
- all target-access flags false;
- no Q/Z, target topology, correlation, sign agreement, or T in D0;
- no drops / no rerolls;
- exact occupancy SHA-256 for all 31 cases must be frozen before target access.

No Phase-D scorer or first-reveal workflow is authorized until D0 succeeds and its exact authority is permanently fixed.
