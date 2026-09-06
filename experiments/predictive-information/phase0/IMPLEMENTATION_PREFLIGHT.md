# Phase 0 score-free implementation note

Date: 2026-09-06
Status: **FROZEN BEFORE SCORE-FREE PREFLIGHT EXECUTION AND BEFORE TARGET-SCORING CODE EXISTS**

This note resolves implementation details left implicit by `PLAN.md` and `AMENDMENT_A.md`. None is chosen from DECAY40/TILT10 target outcomes.

## 1. Cross-family tie rule

Outer-fold model selection compares every legal DECAY40 and TILT10 setting by summed nested literal-surface log likelihood.

If two settings differ by at most `1e-12` total log likelihood:

1. prefer `TILT10` over `DECAY40` because it has one tuned scalar rather than two;
2. within TILT10, prefer smaller `beta`;
3. within DECAY40, prefer smaller `pi`, then smaller `tau`.

This tie rule is deterministic and target-blind.

## 2. TILT10 exact normalization

Let `p0(t)` be the frozen V2 literal-surface probability and let `a_t` be the number of recent source occurrences for which literal training-vocabulary token `t` is an exact edit-distance-1 neighbour.

Only finitely many tokens have `a_t > 0`. For `w_t = exp(beta * a_t)`, the declared model

`P_tilt(t|h) proportional to p0(t) * w_t`

has exact normalizer

`Z(h,beta) = 1 + sum_{t:a_t>0} p0(t) * (w_t - 1)`.

Therefore target-token scoring does not require enumeration of all V2 surfaces:

`P_tilt(y|h) = p0(y) * exp(beta*a_y) / Z`.

Exact generation also has a finite decomposition:

- with mass `1/Z`, draw from the unchanged V2 generator;
- for each activated surface `t`, add point mass `p0(t)*(w_t-1)/Z`.

The masses sum to one by construction. Tokens with zero V2 probability contribute zero extra mass and are ignored.

This decomposition is part of the frozen TILT10 architecture; it is not a later approximation.

## 3. History convention

Match Issue #81:

- history resets at physical-leaf boundaries, not at line boundaries;
- every observed/generated surface token enters history, including parser-rejected tokens;
- only parser-accepted observed tokens contribute literal-surface likelihood because V2 is the frozen emission support authority;
- DECAY40 retains at most 40 prior surfaces; TILT10 uses the most recent 10 from that same running history.

DECAY lag `d=1` is the immediately preceding surface token.

## 4. X2-HARD10 replay

The replay anchor is recomputed score-free during preflight using the unchanged Issue #81 nested selector and outer literal-surface likelihood. Its target S2/H62 values remain the archived Issue #81 authority until the later first-reveal stage.

The preflight does not call `output_metrics`, H62/S2 scorers, or R1 target scoring.

## 5. Preflight authority output

The score-free preflight JSON freezes:

- source git-blob SHA-1;
- plan/amendment/implementation hashes;
- five-fold identity hash;
- every nested likelihood curve/table;
- selected architecture/hyperparameters per outer fold;
- X0, X2-HARD10 and selected-model outer held-out bits/token;
- score-free generation hashes and support diagnostics for three fixed realizations;
- TILT decomposition-normalization residual diagnostics;
- deterministic repeat checks;
- explicit `target_score_calls = 0`.

After this preflight passes, its exact JSON/hash should be archived before target-scoring implementation is added.