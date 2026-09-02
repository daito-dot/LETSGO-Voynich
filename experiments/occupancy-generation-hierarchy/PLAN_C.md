# OGH-C — from token shape to token content: value-level successor grammar, per-token information budget, and the cross-token test

Status: **PREREGISTERED — NO OGH-C LIKELIHOOD OR R2/R3 RESULT REVEALED**

Parents: OGH-A/OGH-B (R1 generation lane closed: a second-order successor grammar over occupied slots is near-sufficient for R1). Frozen R2/R3 scorecards: Phase62B/62P/64B (`phase62b_n0.py`, `phase62p_h62p1.py`, `phase64b_naibbe.py`).

## 1. Questions

1. **Information budget.** How much information does one parsed Voynich token carry beyond its 12-slot shape, under the best compact memoryless token grammar? Report cross-fitted held-out bits per token for shape and for shape + values.
2. **Cross-token test.** Does a complete memoryless token generator (shape + values, no memory across tokens), placed into the manuscript's own paragraph/line skeleton, reproduce R2 (H62-P1 near-family recurrence profile) and R3 (signed S1 paragraph-entry specialization), and the easier S2/S3?

Expected under the program's current reading: (1) is a new number; (2) fails on R2 and R3, locating the content-bearing signal in cross-token structure. Either outcome is recorded.

## 2. Representation

A parsed token (`SlotParser(min)`, unchanged) is the ordered sequence of **units** `u_i = (slot_i, value_i)`, slots strictly increasing, values from the frozen `SLOTS` inventory (33 units in total). Tokens the parser rejects (≈23% of ZL3b visible tokens) are outside the grammar; their skeleton positions are still filled by the generator in stage C1 (the generator produces a complete surface, as A1 and Naibbe did).

Generated units are concatenated into an EVA string; downstream scoring treats that string exactly like a manuscript token (S1/S2/S3/H62 operate on character tuples; R1, if ever re-scored, would re-parse it).

## 3. Frozen model family (cross-fitted on the five physical-leaf folds, ZL3b)

| ID | model | free parameters (nominal) | role |
|---|---|---:|---|
| V0 | G7A shape grammar × independent values `P(v | slot)` (add-½) | 298 + 21 | shape + slot-marginal values baseline |
| V1 | first-order unit chain `P(u_{i+1} | u_i)` incl. `START`/`STOP`, later-slot constraint by construction (add-½) | ≤ 34 × 34 | compact content grammar |
| V2 | second-order unit chain `P(u_{i+1} | u_{i-1}, u_i)`, back-off to V1 with one pseudo-count | ≤ 34² × 34 contexts | richer content grammar |
| V+ | empirical parsed-token-type resampling from training folds | number of training types | memorized-vocabulary ceiling (non-promoting); held-out out-of-vocabulary rate reported |

Held-out likelihood is evaluated on parsed held-out tokens as `−log2 P(unit sequence)` per token; for V+ the covered-token likelihood and the OOV fraction are both reported. Shape-only bits are G7A's held-out cross-entropy (OGH-B stage B0) converted to bits.

Stage C0 (target-blind) reports these numbers and selects, by the OGH-B rule (positive gain over V1 in ≥ 4/5 folds, else V1), the **content grammar** `V*` ∈ {V1, V2} that enters stage C1. V0 and V+ enter stage C1 as anchors regardless.

## 4. Stage C1 — frozen cross-token scoring

For each of V0, V*, V+ and realizations `rep ∈ {0,1,2}`:

1. for each fold `f`, fit on training leaves and generate one token per visible token of every held-out paragraph line (`phase62b_n0.parse_voynich` items, layout only), seed `OGH-C:{model}:fold{f}:rep{rep}`;
2. assemble the five held-out generations into one complete synthetic manuscript of `b.Item`s;
3. score with the unchanged `phase64b_naibbe.output_metrics` (S1 per fold with the frozen Voynich training `sd`/direction, S2 excess, S3 mean η², H62-P1 profile) and aggregate the three realizations with `aggregate_realizations`;
4. evaluate with the unchanged `phase64b_naibbe.evaluate_aggregate` against the frozen Phase62C/63A held-out Voynich targets and the committed N0/C0/A1-R1 baselines.

Frozen readouts per model: S1/S2/S3 ratios to held-out Voynich (Phase62 exposed gate `[0.5, 2.0]`), H62 `mean D_profile` and `mean |ΔC_short|` with fold-wise wins against N0, C0 and A1-R1, and the Phase64B classification string (re-labelled `OGH-C` instead of `C1-E0`).

## 5. Frozen decision (stage C1, model V*)

- `MEMORYLESS TOKEN GRAMMAR REPRODUCES CROSS-TOKEN STRUCTURE` — exposed gate passes on S1, S2 and S3 **and** the Phase64B H62 viability gate passes (beats N0 and C0 on both H62 metrics in ≥ 3/5 folds and in the means).
- `MEMORYLESS TOKEN GRAMMAR PARTIAL` — exposed gate or H62 viability passes but not both.
- `MEMORYLESS TOKEN GRAMMAR FAILS CROSS-TOKEN STRUCTURE` — neither.

Reported without changing the class: the S1 sign (a wrong-sign S1 is the R3 failure mode), the S2 ratio, and whether V+ (memorized vocabulary) does better than V*, which would show that vocabulary identity rather than grammar carries the cross-token statistics.

## 6. Interpretation map

- Fails on R2 and R3 (expected): the content-bearing signal is in cross-token memory; the inverse program should concentrate there, with V* as the frozen memoryless null for token content. The bits-per-token number bounds what a per-token code can carry.
- Passes: cross-token constraints are largely by-products of token-internal grammar plus layout; A1's copy mechanism would be downgraded and R2/R3 lose discriminating power — a major revision, to be replicated on IT2a before acceptance.
- Partial: report which responsibility is reproduced; do not add memory terms inside this phase.

## 7. Prohibited

Any target statistic during model definition or selection; changing the frozen scorers; adding cross-token memory; selecting realizations; interpreting units as letters or meanings; calling any result decipherment.
