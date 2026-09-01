# Issue #75 Phase F0 decision — select K/R/S-gated two-mode chain

Date: 2026-09-02  
Status: **FROZEN TRAINING-ONLY ARCHITECTURE DECISION**

## Frozen authority

Phase-F0 authority:

- run `33545246568` — success
- execution head `9a9a66d85e74d02e804e435c9a15a007a7047aa2`
- artifact ID `9817348700`
- artifact digest `sha256:e56a2b4ab6e6741420c3ba3e430d16ec0c3a565abf4a40c7a917425da82cf7da`
- authority SHA-256 `999d9990449875708019ad71aa3a1d253afad19edada88cb45eb4204349887c6`
- permanent evidence commit `fd1446d474208b9e2f17e3fd4df5249e133c2bd3`

The authority contains no target R1 correlation, target residual vector, target sign agreement, or target T score.

## Frozen selection result

G2:

`M6-KRS-GATED-2MIX-CHAIN`

- 46 free continuous parameters/fold;
- held-out gain over M5 positive in `5/5` physical folds;
- median gain `+0.06003067340698798 nat/token`;
- predictively supported.

G3:

`M6-GLOBAL-3MIX-CHAIN`

- 65 free continuous parameters/fold;
- held-out gain over M5 positive in `5/5` physical folds;
- median gain `+0.03972340211067871 nat/token`;
- predictively supported.

Direct G3 versus G2:

- G3 wins only `1/5` physical folds;
- median `H_G3-H_G2 = -0.018209694780489283 nat/token`.

Frozen classification:

`F0_SELECT_KRS_GATED_TWO_MODE_CHAIN`

## Decision

The next target-topology generator must be G2, not G3.

The next target family is therefore:

`M6-KRS-GATED-2MIX-CHAIN`

Its mechanism is:

1. draw training-only empirical K/R/S geometry;
2. compute a training-fitted geometry-dependent probability of the two latent construction regimes;
3. draw the latent regime;
4. generate the complete 12-slot occupancy signature from that regime's position-specific nearest-neighbour local chain.

There are still:

- zero explicit nonadjacent pair parameters;
- zero generic-distance parameters;
- zero named distant-pair parameters;
- zero complete-signature-specific parameters.

## Why this is the selected next mechanism

Phase E showed that hidden construction modes materially improve R1, but a global mode prior is insufficient.

F0 shows that allowing the prior to depend on K/R/S is a larger and more reproducible held-out predictive improvement than simply adding a third global mode, despite using 19 fewer free parameters per fold.

The stable gate-slope signs across all five outer folds further support the interpretation that coarse token geometry and latent construction regime are systematically coupled.

## Next target-test firewall

Before any G2 target measurement:

- freeze a prospective Phase-F target plan;
- use the already-frozen F0 parameters or an exactly specified training-only reconstruction;
- generate exactly 31 target-blind candidate corpora with fixed deterministic seeds;
- freeze exact generated occupancy SHA-256 identities;
- replay at least reps 0 and 30;
- perform candidate-owned-null smoke with target loaders blocked;
- freeze scorer and aggregate decision law;
- then perform exactly one complete 31-case first reveal.

The target evaluation must retain:

- the same 12-slot parser;
- the same physical folds and token populations;
- the complete 66-edge residual topology;
- ZL3b and IT2a as separate target readings;
- `T=min(R_ZL3b,R_IT2a)`;
- the frozen Phase-A M+ paired q95 equivalence tolerance `0.009768313008182594`;
- no drops;
- no rerolls;
- no target-selected repair.

## Prequalified fallback

G3 is a legitimate training-supported but **non-selected** alternative.

To prevent future target-driven architecture selection, the ordering is frozen now:

1. test G2 first because it won the F0 rule by predictive performance plus parsimony;
2. if G2 reaches the frozen M+ equivalence criterion, stop the R1 complexity ladder and do not target-test G3;
3. if G2 is insufficient, G3 may be tested only as a separately frozen secondary target phase using the already-defined `M6-GLOBAL-3MIX-CHAIN` family, without changing its architecture in response to the G2 target residuals;
4. G2 target residual edges may not be used to modify G3 or to introduce selected distant-pair terms.

This fallback sequence is fixed before any G2 target reveal.

## Boundaries

The selected latent regimes remain statistical occupancy-construction states. The decision does not assign semantics, plaintext, language, cipher state, or historical meaning to them.
