# Phase 2A Amendment A — preserve local signal in the prefix control and calibrate randomized lag

Date: 2026-09-06
Status: **FROZEN BEFORE ANY PHASE-2A OUTER SCORE**
Applies to: `PLAN.md`

## Trigger

The preregistered PLAN contains only the plan document; no Phase-2A executable or workflow exists and no A0-A4 outer result has been computed.

A construct-validity audit identified two asymmetries that could make the original order attribution too favorable to `ORDERED128-FIXED`:

1. `PREFIX-BAG-CV` replaces the <=40 ordered-local predictor instead of adding order-free prefix inventory on top of it. It can therefore lose because it discards already-established local recency, even if long-prefix inventory contains genuine additional information.
2. `RANDOM-LAG-FIXED` inherits `pi=.30`, which was selected for the ordered model. If randomized lag association is weaker, forcing the ordered model's mixture strength can penalize the control through calibration rather than through loss of order information.

Neither issue is motivated by a Phase-2A outcome. This amendment strengthens the null/control side before reveal.

## A5 — `LOCAL_PLUS_PREFIX-CV`

Retain the frozen outer-fold `LOCAL40` predictor A0 exactly, including its Phase-1 parameters.

Let `P_LOCAL(t)` be A0's normalized probability at the current position and let `Q_bag(t)` be the A1 all-causal-prefix, order-free source distribution.

When a prefix-bag context exists:

`P_LP(t) = (1-rho) P_LOCAL(t) + rho Q_bag(t)`.

When no prefix-bag context exists:

`P_LP(t) = P_LOCAL(t)`.

Frozen grid:

`rho = 0.00, 0.01, ..., 0.30`.

Selection is by summed nested literal-surface likelihood inside the outer-training population only. Exact tie: smaller `rho`.

Primary conditional prefix-inventory contrast:

`G_prefix_cond = bits(A0 LOCAL40) - bits(A5 LOCAL_PLUS_PREFIX-CV)`.

This becomes the primary test that causal prefix inventory adds information beyond the already-established <=40 local effect. The original A1 replacement contrast remains required and is reported separately.

## A6 — `RANDOM-LAG-CV`

Reuse exactly the five frozen A4 randomizations and their source-weight permutations. No seed, history, tau or randomization rule changes.

Unlike A4, select the memory mixture strength separately for the randomized control:

`pi_random = 0.00, 0.01, ..., 0.30`.

For each candidate `pi_random`, compute each of the five randomized-model log likelihoods on every inner validation fold and select by the **arithmetic mean log likelihood across the five frozen randomizations**, summed across the four inner folds. Exact tie: smaller `pi_random`.

Outer score is the arithmetic mean bits/token across the same five fixed randomizations at the selected `pi_random`. Per-seed values are always retained.

Primary calibration-robust order contrast:

`G_order_random_cv = bits(A6 RANDOM-LAG-CV) - bits(A2 ORDERED128-FIXED)`.

A4 `G_order_random` remains the exact fixed-parameter intervention diagnostic. A6 is the stronger predictive control and cannot be rescued by choosing a favorable seed.

## Additional order contrast against the stronger prefix control

Define:

`G_order_hybrid = bits(A5 LOCAL_PLUS_PREFIX-CV) - bits(A2 ORDERED128-FIXED)`.

Positive means the actual ordered long-history model beats a model that retains the frozen local recency effect and separately receives all order-free causal-prefix inventory.

## Amended pass variables

Keep all original contrasts, but replace the primary attribution variables by:

- `PREFIX := G_prefix_cond` passes the frozen mean-positive + >=4/5 rule;
- `ORDER_RANDOM := G_order_random_cv` passes;
- `ORDER_HYBRID := G_order_hybrid` passes;
- `ORDER_FULL := ORDER_RANDOM && ORDER_HYBRID`.

Original `G_prefix`, `G_order_bag_fixed` and fixed-pi `G_order_random` remain required diagnostics and may not rescue a failure of the stronger controls.

## Amended classification

- `MIXED PREFIX + ORDER CONTRIBUTIONS` iff `PREFIX && ORDER_FULL`.
- `LONG-HISTORY GAIN PRIMARILY PREFIX-INVENTORY` iff `PREFIX` and both `ORDER_RANDOM` and `ORDER_HYBRID` are false.
- `ORDER-SENSITIVE LONG-HISTORY INFORMATION SURVIVES` iff `!PREFIX && ORDER_FULL`.
- `SOURCE ATTRIBUTION INCONCLUSIVE` for all other scientifically valid combinations, including disagreement between the two stronger order controls.
- `MODEL / SUPPORT INVALID` remains unchanged.

This is deliberately conservative: one favorable order control cannot license an order-sensitive interpretation.

## No other change

- A0/A2 Phase-1 reference parameters remain frozen.
- A1/A3/A4 remain in the experiment unchanged.
- history never extends beyond the causal prefix of the current physical leaf;
- no future token is allowed;
- no S1/S2/H62/R1 or semantic information is available;
- no grid or control may be extended after the first Phase-2A outer reveal.