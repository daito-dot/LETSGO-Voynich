# Issue #94 / Issue #88 Phase 2A — sequence order versus causal prefix inventory

Date frozen: 2026-09-06
Parent program: Issue #88
Implementation issue: #94
Status: **PREREGISTERED BEFORE PHASE-2A EXECUTABLE SCORING**

## 1. Scientific question

Issue #92 Phase 1 established that the <=40-token local recency mechanism does not saturate held-out prediction. Extending the same edit-1 family to all preceding tokens on the current physical leaf adds `~0.0469 bit/token` in 5/5 folds, and all five selectors choose `H=ALL, tau=128, pi=.30`.

That result does **not** distinguish genuine order-sensitive long memory from a simpler causal-prefix effect: as a leaf unfolds, its prefix reveals which token families are currently available or common.

The Phase-2A question is therefore:

> **How much of the Phase-1 long-history gain is explained by the order-free inventory of token families already observed in the causal prefix, and how much requires the actual association between source-token identity and recency/lag?**

No future token from the evaluated leaf is ever available to a predictor.

This is source attribution of an already-established predictive effect. It is not a new estimate of the total predictive budget and not a historical-memory claim.

## 2. Conditional-evidence status

Phase 2A is a prospective follow-up motivated by the Phase-1 `H=ALL,tau=128,pi=.30` result on the same five physical-leaf folds. Therefore:

- the interventions and decision rules below are frozen before their Phase-2A outer scores;
- the evidence is conditional on the already-observed Phase-1 family result;
- no claim of a second fully independent sample is made;
- exact matched interventions are preferred over opening a new large parameter search.

## 3. Frozen source / population / firewall

Reuse unchanged:

- ZL3b source hash and parser authority from Issues #90/#92;
- exact five physical-leaf outer folds;
- V2 literal-surface probability;
- training-vocabulary exact edit-distance-1 neighbour relation;
- outer-training token frequencies used inside each source occurrence's neighbour distribution;
- physical-leaf history reset convention;
- all visible prior surface tokens enter history, including parser-rejected tokens;
- only parser-accepted current token positions contribute primary code length.

No S1, S2, H62, R1, Issue #84 target range, image label, semantic hypothesis or proposed plaintext is available to the Phase-2A executable.

## 4. Common source-occurrence mechanism

For each past surface-token occurrence `i` in the causal prefix, define a normalized source-neighbour distribution `D_i(t)` exactly as in Phase 1:

- if source token `i` has no training-vocabulary exact edit-1 neighbour, it is ineligible;
- otherwise `D_i(t)` is proportional to outer-training token frequency over that source's edit-1 neighbours.

Every Phase-2A long-history control uses the **same eligible source occurrences and the same `D_i` distributions**. Only the weight assigned to source occurrence `i` changes.

For any normalized memory distribution `Q(t)`, literal prediction remains:

`P(t) = (1-pi) P_V2(t) + pi Q(t)`

when at least one eligible source exists, else exactly `P_V2(t)`.

## 5. Frozen models / interventions

### A0 — `LOCAL40`

Regression anchor: exact Phase-0/Phase-1 bounded local model selected per outer fold:

- previous <=40 surfaces;
- exponential source weighting;
- `tau=32`;
- `pi=.21,.21,.20,.21,.21` for outer folds 0..4.

Primary code length must reproduce the Phase-1 B1 values within `1e-9 bit/token`; otherwise stop and audit.

### A1 — `PREFIX-BAG-CV`

All eligible source occurrences in the **entire causal prefix of the current physical leaf** receive equal source weight.

This is exactly the `tau=INF, H=ALL` limit and is invariant to the order of source identities within the observed prefix.

Only `pi` is selected by nested literal-surface likelihood:

`pi = 0.00, 0.01, ..., 0.30`.

No larger mixture grid is opened if `.30` wins.

Scientific role: quantify predictive value of accumulated causal prefix token-family inventory beyond the <=40 local anchor without using future tokens.

### A2 — `ORDERED128-FIXED`

Matched reference intervention frozen directly from the Phase-1 result:

- all eligible source occurrences in causal prefix;
- actual lag `d` receives source weight `exp(-d/128)`;
- `pi=.30` in every fold.

No parameter is fitted in Phase 2A. This model must reproduce the Phase-1 B2 outer code length within `1e-9 bit/token`; otherwise stop and audit.

Scientific role: the observed ordered long-history reference to be causally decomposed, not a newly selected best model.

### A3 — `PREFIX-BAG-FIXED`

Use the same all-prefix source population as A2 but set every eligible source occurrence's weight to `1`, with `pi=.30` fixed.

A2 versus A3 changes only the mapping from source occurrence to source weight. It does not change:

- the causal prefix;
- edit-1 relation;
- neighbour distributions;
- V2 base;
- mixture strength.

Primary matched contrast:

`G_order_bag_fixed = bits(A3) - bits(A2)`.

### A4 — `RANDOM-LAG-FIXED`

For each parser-accepted target position, start from exactly the same eligible source occurrences and exact ordered-recency weight multiset that A2 would use:

`W = { exp(-d_i/128) }`.

Destroy the association between source identity and actual lag by a prospectively fixed permutation of `W` across those eligible source occurrences.

Frozen randomization family:

- 5 seeds: `0,1,2,3,4`;
- no seed selection or reroll;
- for seed `r`, target-independent stable seed namespace is `ISSUE94:RANDOM_LAG:r:<physical-leaf>:<target-visible-position>`;
- at each target position, `numpy.random.default_rng(stable_seed(namespace)).permutation(m)` assigns the existing ordered weight vector to the `m` eligible prior source occurrences;
- target token identity is never part of the random seed.

Each randomized source distribution is exactly normalized because the source-weight multiset and normalized `D_i` distributions are unchanged.

Mixture strength remains fixed `pi=.30`.

Primary RANDOM-LAG score per outer fold is the **arithmetic mean bits/token across all five fixed randomizations**. Per-seed scores are always reported.

Primary matched contrast:

`G_order_random = mean_bits(A4 seeds) - bits(A2)`.

A4 is not tuned by likelihood. It is an intervention/null control on the already-frozen A2 mechanism.

## 6. Primary attribution contrasts

All are paired outer held-out differences in bits/token.

### Prefix-inventory contribution

`G_prefix = bits(A0) - bits(A1)`.

Positive means an order-free all-prefix family predicts better than the <=40 local anchor.

### Actual order versus uniform-prefix weighting

`G_order_bag_fixed = bits(A3) - bits(A2)`.

Positive means the actual recency weighting beats an otherwise identical uniform-prefix intervention.

### Actual order versus randomized-lag association

`G_order_random = mean_bits(A4) - bits(A2)`.

Positive means the actual source-identity/lag association beats outcome-independent reassignments that preserve the same prefix and same recency-weight spectrum.

Each contrast is called reproducible only if:

- mean across the five outer folds is positive; and
- the fold-level contrast is positive in at least `4/5` folds.

This is a frozen stability rule, not a p-value.

## 7. Secondary diagnostics

Report without changing classification:

- A1 selected `pi` per fold and full inner likelihood curve;
- A1/A3/A2/A4 context-availability fractions;
- eligible source-occurrence counts by target and leaf;
- A2 ordered weighted effective source count

  `N_eff = (sum_i w_i)^2 / sum_i w_i^2`

  summarized across scored positions;
- A4 normalization residuals;
- per-seed A4 bits/token and variation;
- fraction of A2 improvement over A0 accounted for by A1:

  `share_prefix = (bits(A0)-bits(A1)) / (bits(A0)-bits(A2))`

  reported continuously only; no threshold uses this ratio;
- actual nested likelihood difference between A1 `pi=.30` and its selected `pi` if different.

## 8. Decision logic

Let:

- `PREFIX = G_prefix` passes the frozen stability rule;
- `ORDER_BAG = G_order_bag_fixed` passes;
- `ORDER_RANDOM = G_order_random` passes.

### `MIXED PREFIX + ORDER CONTRIBUTIONS`

If `PREFIX` passes and both `ORDER_BAG` and `ORDER_RANDOM` pass.

Interpretation: causal prefix inventory carries predictive information beyond local history, and the actual ordering/lag assignment carries additional information beyond that inventory.

### `LONG-HISTORY GAIN PRIMARILY PREFIX-INVENTORY`

If `PREFIX` passes but the conjunction `ORDER_BAG && ORDER_RANDOM` does not.

Interpretation: the tested evidence does not require actual long-range order once the accumulating causal prefix inventory is supplied.

### `ORDER-SENSITIVE LONG-HISTORY INFORMATION SURVIVES`

If `PREFIX` fails but both `ORDER_BAG` and `ORDER_RANDOM` pass.

Interpretation: the Phase-1 long-history gain is not reproduced by an order-free prefix bag, while actual lag association survives both matched controls.

### `SOURCE ATTRIBUTION INCONCLUSIVE`

All other pass/fail combinations or any normalization/support/regression failure.

Do not invent a weighted omnibus score to repair a mixed result.

## 9. What Phase 2A can and cannot license

If order-sensitive information survives, this licenses a later attempt to localize **which observable scale/state carries that ordered residual**. It does not by itself license semantic interpretation or a rich HMM.

If prefix inventory explains the gain, the historical interpretation shifts away from literal leaf-long memory toward evolving local inventory/register/topic availability. That still does not identify meaning.

Rich latent-state work remains blocked until the broader Phase-2 program has also tested observable document-state and support/vocabulary explanations.

## 10. Preflight / first reveal

Before the first outer Phase-2A result:

1. verify ZL3b hash and five-fold identity;
2. reproduce A0 Phase-1 B1 outer bits/token to `1e-9`;
3. reproduce A2 Phase-1 B2 outer bits/token to `1e-9`;
4. synthetic-normalization test A1/A3/A4;
5. verify A3 equals A1 formula at `pi=.30` on a synthetic fixed prefix;
6. verify A4 preserves the exact A2 source-weight multiset for every tested synthetic position;
7. verify A4 deterministic repeat under all five frozen seeds;
8. statically reject any S1/S2/H62/R1 target-scoring call in the executable.

The first complete outer-test run is the authoritative Phase-2A reveal. No architecture, seed or grid changes after that reveal are licensed.