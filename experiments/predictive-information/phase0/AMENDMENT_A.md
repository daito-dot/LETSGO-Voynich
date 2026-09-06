# Phase 0 prereveal Amendment A — variance-neutral target gates

Date: 2026-09-06
Status: **FROZEN BEFORE EXECUTABLE PHASE-0 TARGET SCORING IMPLEMENTATION**
Applies to: `PLAN.md` sections 6–7

## Reason

The initial Phase-0 plan allowed each stochastic candidate to expand the S2 and raw-H62 target interval by its own three-realization Monte Carlo half-range.

That rule is rejected before any Phase-0 candidate target score exists because it creates a criterion-validity defect: a higher-variance candidate would receive a wider pass interval merely because it is noisier.

This amendment is methodological only. No DECAY40 or TILT10 S2/H62/R1 result has been computed or inspected before this change.

## Replacement rule

For both S2 and raw H62:

1. extract the five frozen held-out Voynich target values from the unchanged Phase62/64 fold contexts before candidate target generation;
2. define the immutable target interval as the literal `[min, max]` of those five values;
3. score the candidate by the **mean across its three fixed, no-reroll realizations**;
4. PASS only if that mean lies inside the immutable target interval;
5. report all three realization values, their range, standard deviation and half-range as diagnostics only;
6. candidate stochastic variation may never widen or move the target interval.

Thus:

- `S2_pass := target_S2_min <= mean_candidate_S2 <= target_S2_max`
- `H62_raw_pass := target_raw_min <= mean_candidate_abs_excess_sum <= target_raw_max`

No ratio band is substituted.

## Unchanged criteria

The following remain unchanged from `PLAN.md`:

- selection is nested literal-surface likelihood only;
- predictive gain must be positive in at least 4/5 outer folds and positive on the outer-fold mean;
- H62 profile must meet both frozen A1-R1 comparator means;
- R1 must pass all three fixed selected-model realizations;
- S1 is not a Phase-0 responsibility;
- no DECAY40+TILT10 or X3 composition is licensed in Phase 0;
- regardless of Phase-0 outcome, Issue #88 Phase 1 predictive-information budgeting remains the next program-level question.

## Authority precedence

Where `PLAN.md` mentions candidate-specific Monte Carlo expansion of an S2/raw-H62 target interval, this amendment supersedes that language. All other plan text remains authoritative.