# Issue #75 Phase F0 — target-blind latent-frontier diagnostic plan

Date: 2026-09-02  
Status: **PREREGISTERED BEFORE F0 EXECUTABLE / TARGET-R1 FORBIDDEN**

## Why this diagnostic exists

Phase E permanently established:

`M5_KRS_TWO_LATENT_CHAIN_MODES_INSUFFICIENT_RICHER_LATENT_OR_CONFIGURATION_RULE_REQUIRED`

while also showing a large paired gain from introducing two hidden local-chain construction modes.

The next target model must not be selected by inspecting the revealed 66-edge target residuals. Phase F0 therefore performs **model discrimination using source occupancy observations and physical-leaf predictive likelihood only**.

F0 is not a target-reveal phase and cannot produce an R1 correlation, target sign agreement, or T score.

## Frozen scientific question

Which compact extension of the Phase-E latent mechanism is supported by cross-leaf predictive occupancy likelihood before another target-topology test?

The first two alternatives are deliberately minimal:

1. **G2 — geometry-conditioned two-mode gate**: keep exactly two M3 local-chain components, but allow mode prevalence to depend smoothly on coarse K/R/S geometry;
2. **G3 — three global local-chain modes**: keep a geometry-independent global mixture, but allow one additional latent component.

If neither produces reproducible held-out predictive gain, F0 will not add more global-mixture complexity; it will license a separately preregistered within-token hidden-state frontier instead.

## Firewall

The F0 executable must not import, open, derive, or score:

- ZL3b target R1 vectors;
- IT2a target R1 vectors;
- any Phase-E individual target residual vector;
- any 66-edge target residual or edge ranking;
- target correlations;
- target sign agreements;
- target T values for candidate selection.

The already-known Phase-E aggregate outcome only licenses this diagnostic. It is not an optimization objective.

The executable may read the frozen ZL3b transcription solely through the existing parser/dataset path used to fit prior generators, because the F0 outcome is exact held-out **occupancy likelihood**, not target topology.

## Physical-leaf outer evaluation

Reuse the exact frozen five physical folds.

For each outer fold `f`:

- fit each candidate on all tokens with `fold != f`;
- evaluate exact conditional log likelihood on observed tokens with `fold == f`;
- condition on each observed token's K/R/S descriptor;
- do not score q(K/R/S), because all candidate families retain the same empirical descriptor mechanism and F0 is discriminating the conditional configuration rule.

For family `m`, define:

`H_m[f] = heldout conditional log likelihood / N_heldout`

and relative to the refitted Phase-E family:

`Delta_m[f] = H_m[f] - H_M5[f]`.

Also report direct `H_G3-H_G2` per fold.

No Monte Carlo generation is required for F0.

## Baseline — M5 global two-mode local chain

Refit the exact Phase-E family on each outer training population:

- 2 latent components;
- each component = 21-parameter M3 local K/R/S-conditioned chain;
- one global mixing probability;
- 43 free continuous parameters;
- no explicit nonadjacent interactions;
- no distance interactions;
- no signature-specific parameters.

The implementation should reuse the frozen Phase-E exact conditional-likelihood machinery where possible.

## Candidate G2 — K/R/S-gated two-mode chain

Family name:

`M6-KRS-GATED-2MIX-CHAIN`

The two local-chain components are unchanged from M5.

Replace the single global mixture logit by:

`eta(d) = a0 + aK*zK(d) + aR*zR(d) + aS*zS(d)`

where `d=(K,R,S)` and `zK,zR,zS` are training-token weighted standardized descriptor coordinates computed separately inside each outer training population.

Then:

`P(Z=1 | d) = logistic(eta(d))`.

If a coordinate has zero training standard deviation, its standardized value is fixed to zero and its slope is fixed to zero; otherwise all three slopes are free.

Nominal free-parameter count:

- 42 component parameters;
- 4 gate parameters;
- total `46`.

M5 is nested by `aK=aR=aS=0`.

No slot-pair, distance, signature-specific, leaf, line, or target-dependent gate term is allowed.

## Candidate G3 — global three-mode local chain

Family name:

`M6-GLOBAL-3MIX-CHAIN`

Use exactly three M3 local-chain components, each with 21 free parameters, and a global three-category mixing distribution with two free logits.

Nominal free-parameter count:

- `3 × 21 = 63` component parameters;
- `2` global mixture parameters;
- total `65`.

The mixture prior cannot depend on K/R/S, slot, leaf, line, or target.

There are still:

- zero explicit nonadjacent interactions;
- zero generic-distance terms;
- zero named distant-pair terms;
- zero signature-specific terms.

M5 is nested by duplicating one component and splitting its weight.

## Deterministic fitting

All state probabilities and likelihoods are evaluated by exact enumeration over the 4095 non-empty 12-slot occupancy states within K/R/S descriptor classes.

No stochastic optimization or random restart is allowed.

### M5 baseline

Use the frozen Phase-E deterministic fitting implementation.

### G2 starts

Exactly 9 deterministic starts per outer fold:

- start 0: exact fitted M5 components and global logit, with all three gate slopes `0`;
- starts 1..8: deterministic SHA-derived symmetric perturbations of the two component vectors at amplitude `0.10`, plus deterministic SHA-derived gate-slope perturbations at amplitude `0.05`.

Select the valid start with greatest **outer-training conditional likelihood only**. Ties within `1e-10` go to smaller start index.

### G3 starts

Exactly 9 deterministic starts per outer fold:

- start 0: exact M5 distribution represented by duplicating component 0 and splitting its weight equally;
- starts 1..4: deterministic SHA-derived symmetric splits of M5 component 0 at amplitude `0.08`;
- starts 5..8: deterministic SHA-derived symmetric splits of M5 component 1 at amplitude `0.08`.

Initial weights preserve the corresponding M5 component's total weight under each split.

Select the valid start with greatest **outer-training conditional likelihood only**. Ties within `1e-10` go to smaller start index.

For all families:

- use deterministic exact objective/gradient evaluation;
- maximum optimizer iterations `2000`;
- reject non-finite fits;
- require all mixture weights > `1e-8`;
- no reroll or replacement start;
- no candidate may be repaired after held-out or target inspection.

## Frozen predictive-support rule

A richer family `m` is **predictively supported over M5** only if both are true:

1. `Delta_m[f] > 0` in all 5 physical held-out folds;
2. `median_f Delta_m[f] >= 0.01 nat/token`.

The `0.01 nat/token` threshold is frozen here as a minimum practically meaningful predictive gain before any F0 executable exists.

## Frozen architecture-selection rule

After all five held-out folds are scored:

1. If G2 is supported and G3 is not, select `M6-KRS-GATED-2MIX-CHAIN` for the next preregistered target phase.
2. If G3 is supported and G2 is not, select `M6-GLOBAL-3MIX-CHAIN`.
3. If both are supported, G2 wins by parsimony unless G3 beats G2 directly in at least 4/5 folds **and** `median(H_G3-H_G2) >= 0.01 nat/token`; only then may G3 displace G2.
4. If neither is supported, do not increase the number of global mixture states further. Classify the global-mixture frontier as insufficient for model selection and license a separately preregistered within-token hidden-state process.

F0 itself never opens target topology, regardless of which branch wins.

## Frozen F0 output

Produce one JSON authority containing:

- source/parser/fold provenance;
- family parameter counts and guardrails;
- per-fold training and held-out population sizes;
- selected deterministic start for every fitted family/fold;
- training conditional likelihoods;
- held-out conditional likelihoods and nat/token values;
- per-fold G2-M5, G3-M5, and G3-G2 differences;
- support flags under the exact rule above;
- one frozen selected next-frontier classification.

Expected classification vocabulary:

- `F0_SELECT_KRS_GATED_TWO_MODE_CHAIN`
- `F0_SELECT_GLOBAL_THREE_MODE_CHAIN`
- `F0_GLOBAL_MIXTURE_EXTENSIONS_NOT_PREDICTIVELY_SUPPORTED_WITHIN_TOKEN_STATE_FRONTIER_REQUIRED`

No R1, target correlation, sign agreement, target edge residual, or T field is permitted in the F0 output.

## What F0 can establish

F0 can tell us whether the two-mode Phase-E mechanism fails primarily because:

- the **probability of choosing a construction mode changes with coarse token geometry**, or
- the token inventory requires **at least one additional global construction regime**.

If neither is predictively supported, the stronger next hypothesis is that one fixed mode for the entire token is itself the wrong abstraction and hidden state must evolve during construction.

F0 cannot establish semantics, plaintext, cipher states, historical procedure, or decipherment.
