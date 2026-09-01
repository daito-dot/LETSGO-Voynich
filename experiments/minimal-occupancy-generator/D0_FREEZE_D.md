# Issue #75 Phase D0 authority freeze

Date: 2026-09-01  
Status: **VALID TARGET-BLIND D0 AUTHORITY FROZEN**

## Authority

- family: `M4-KRS-CHAIN-DISTANCE`
- final normative plan commit: `f9e60ed9e9261b30c3294c576cf7ea037cf2c2c7`
- authoritative generator commit: `ef8edcb94e287a3fd6c559308ff902dc7d1c41ee`
- implementation freeze commit: `7a6f3d3257f9fdfaa43edefd63dec4cea4dbe5f2`
- D0 launch scientific head: `d1b4fbccc15cca3693c7f884783d9ece2590ab64`
- workflow run: `33510693677` — success
- artifact ID: `9801496506`
- artifact digest: `sha256:aa678ccb835059302058a9df2e1740fa5be30c440444db96edd4d736d097c409`
- D0 authority SHA-256: `5c31aaa5fdb959873d89d7762dfd78db42c1a773a091b71a9f0731e90fa269cb`
- permanent repository commit: `2e1e0545e73e857d595cd71bff05a910bfc10eee`
- permanent directory: `experiments/minimal-occupancy-generator/stage-d0/`

## Contract checks

- schema: `issue75-phaseD0-m4-krs-chain-distance-generator-authority-v1`
- status: `M4_KRS_CHAIN_DISTANCE_31_CORPORA_FROZEN_TARGET_BLIND`
- 31/31 reps `0..30`
- 25,071 tokens per corpus
- five frozen fold populations `4430 / 4810 / 5516 / 5447 / 4868`
- 31 distinct occupancy SHA-256 values
- no drops / no rerolls
- all target-access flags false

## Identifiability and fit

Exact complete-state within-`(K,R,S)` rank audit:

- unary rank: `11`
- unary + adjacent rank: `21`
- full 33 reported features rank: `29`
- selected free basis rank: `29`

Free parameters per fold: `29 = 11 unary + 10 adjacent + 8 nonadjacent distance`.

Maximum absolute reported training-moment fit error across all five cross-fit models:

`8.900935544176036e-13`

This is below the preregistered `1e-10` tolerance.

Descriptor class counts by held-out fold model:

`110 / 112 / 111 / 111 / 112`

Generated distinct-signature range across the 31 frozen corpora:

`1172 .. 1236`

## Firewall statement

D0 computed no candidate pair-Q, no residual Z, no ZL3b/IT2a target topology, no target correlation, no sign agreement, and no T.

Two prior Phase-D launch attempts (`33510176784`, `33510519140`) failed at pre-generation chronology/plan gates and are non-authoritative. Neither reached source checkout/fitting/generation or target access.

Next authorized actions are only:

1. exact D0 replay preflight on reps `0` and `30`;
2. target-blind candidate-owned-null smoke on rep `0`;
3. scorer/aggregator and PRETARGET execution freeze;
4. only then the complete 31-case first reveal.
