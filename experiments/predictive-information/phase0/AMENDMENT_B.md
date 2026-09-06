# Phase 0 prereveal Amendment B — one-time decay-scale boundary extension

Date: 2026-09-06
Status: **FROZEN AFTER SCORE-FREE PREFLIGHT A AND BEFORE ANY DECAY40/TILT10 TARGET SCORE**
Applies to: `PLAN.md` candidate P1 / preflight selector

## Trigger

Score-free Preflight A (`PREFLIGHT_A_PROVENANCE.md`) selected DECAY40 with `tau=32` in all five outer folds. `tau=32` was the largest frozen decay scale, and best nested literal-surface likelihood improved monotonically from `tau=1` through `2,4,8,16,32` in every fold.

No S1, S2, H62, R1 or Issue #84 target score was computed before this amendment. The trigger is therefore target-blind and directly relevant to model-selection validity.

## Amendment

Keep the history window exactly frozen at the previous at most **40** surface tokens. Do not change the `pi` grid.

Extend the DECAY40 scale grid once to:

`tau in {1, 2, 4, 8, 16, 32, 64, 128, INF}`

where `INF` is the exact uniform weighting limit over eligible source occurrences within the same previous-40 window:

`weight(d | INF) = 1` for every eligible lag `d=1..40`.

This does **not** introduce a global cache and does not expand history beyond 40 tokens.

## Stopping rule

This is the only Phase-0 decay-scale extension.

- If a finite interior scale wins, use it.
- If `tau=128` wins, do not extend further.
- If `INF` wins, interpret Phase-0 likelihood as preferring no measurable distance decay inside the bounded 40-token window.

In either boundary case, do not expand the history window in Phase 0. Longer-history predictive structure belongs to Issue #88 Phase 1.

## Selection and tie rules

All original likelihood-only selection rules remain unchanged. For an exact likelihood tie within DECAY40 after `pi`:

- prefer the smaller finite `tau`;
- `INF` sorts after every finite scale.

The cross-family TILT10-vs-DECAY40 tie rule remains unchanged.

## No other change

- `pi = 0.00..0.30` step `.01` remains frozen;
- TILT10 beta grid remains frozen;
- target gates remain as amended by Amendment A;
- generation seeds / three realizations remain frozen;
- no X3 composition is licensed;
- target scoring remains prohibited until the amended score-free preflight is archived.