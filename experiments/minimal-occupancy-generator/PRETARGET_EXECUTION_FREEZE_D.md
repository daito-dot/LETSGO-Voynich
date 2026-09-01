# Issue #75 Phase D — PRETARGET execution freeze

Date: 2026-09-01  
Status: **AUTHORIZED FOR ONE COMPLETE 31-CASE FIRST REVEAL**

No valid Phase-D target score exists at this freeze.

## Frozen scientific chain

1. Frozen Phase-C insufficiency authority:
   - aggregate SHA-256 `34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a`
   - classification `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED`
2. Final Phase-D preregistration:
   - commit `f9e60ed9e9261b30c3294c576cf7ea037cf2c2c7`
3. Authoritative nested M4 generator:
   - commit `ef8edcb94e287a3fd6c559308ff902dc7d1c41ee`
4. Final D0 target-blind authority:
   - generation head `d1b4fbccc15cca3693c7f884783d9ece2590ab64`
   - run `33510693677` success
   - permanent commit `2e1e0545e73e857d595cd71bff05a910bfc10eee`
   - authority SHA-256 `5c31aaa5fdb959873d89d7762dfd78db42c1a773a091b71a9f0731e90fa269cb`
5. D0 freeze metadata:
   - commit `60afe3147de208a3b23035fd0602a1d1ce88415c`
6. Frozen scorer:
   - commit `5449d31480d783f5bb335958be557e6ad8cbadb6`
7. Candidate-null smoke with target-loader hard block:
   - final commit `16ca05a186d3936d81f7fbe8c7527b0637a8406a`
8. Frozen aggregate decision law:
   - final commit `44c7955b834e51932bd9c9946d38d66da489d001`

## Pretarget replay/null authority

Workflow:

- run `33511195719` — success
- execution head `99d656321dc041da0435b8ac34b44aefdb5446f6`
- permanent evidence commit `af187ab80af1bb4868756b2625eefd866b69ee99`
- directory `experiments/minimal-occupancy-generator/stage-d-pretarget/`
- artifact ID `9801731480`
- artifact digest `sha256:0aa265c67a0e8ea2e2166be2ff9e90cb5b1be9fa590278eec53587b87708d182`

Exact replay:

- rep 0 occupancy SHA `6831ee24022f34eb66e9e5db5ab16f553d370063f36b1e8e38cd7d206c08fd2d`
- rep 30 occupancy SHA `724b79a6e0d826555de6b0365f97aa6a29ba6e27714e0813f474640ffb05dc40`
- both exactly equal their frozen D0 corpus authorities
- all target-access fields false

Candidate-owned-null smoke, rep 0:

- output SHA-256 `60613a2763a830e50a2b342ace218088968df9db4ed016c94028b07f0f84ab83`
- `N_ref=1000`, `N_test=1000`
- complete residual vector length `66`
- residual energy `E=3.0662698685620127`
- `p_exist=0.000999000999000999`
- reliability `W=0.9496019313081269`
- target loader monkeypatched to hard-fail if called
- ZL3b target loaded: false
- IT2a target loaded: false
- target correlation: false
- target sign agreement: false
- T: false

Pretarget file SHA-256 values:

- candidate smoke JSON `60613a2763a830e50a2b342ace218088968df9db4ed016c94028b07f0f84ab83`
- rep0 replay JSON `b802ed805c604572d58f0888c48fad1a45f067e4aac11dd260c87f7b77b11244`
- rep30 replay JSON `923aa39259d73632ec352bf7a3663914b50cc9de521c953ab3ce8d15058ec1ca`

## First-reveal contract

Exactly one complete Phase-D first-reveal population is authorized:

- family `M4-KRS-CHAIN-DISTANCE` only;
- reps `0..30`, all 31 required;
- exact regeneration of each frozen D0 occupancy SHA before target access;
- unchanged candidate-owned 1000-reference / 1000-test null;
- complete 66-edge residual vector;
- frozen ZL3b and IT2a target references loaded only after candidate measurement;
- ZL3b and IT2a reported separately;
- `T=min(R_ZL3b,R_IT2a)`;
- no case selection;
- no drops;
- no rerolls;
- no target-selected pair, distance, hyperparameter, architecture, seed, or repair.

## Frozen primary decision

Reuse exact Phase-A aggregate SHA:

`fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

and exact q95 tolerance:

`delta_plus=0.009768313008182594`.

For each rep:

`D_M4[r] = T_M4[r] - T_plus_center_PhaseA[r]`

and

`gap_M4 = median_r D_M4[r]`.

If:

`gap_M4 >= -0.009768313008182594`

classify:

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_SUFFICIENT`

and **STOP** the R1 model-complexity ladder.

Otherwise classify:

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED`.

Only the latter outcome licenses a separately preregistered latent-state/configuration frontier.

The paired `T_M4-T_M3` distribution and q90/q99 tolerance checks are diagnostic only and cannot promote or alter the primary decision.

## Target-history firewall

At this freeze:

- Phase-D D0 target access = zero;
- replay target access = zero;
- candidate-null smoke target access = zero;
- valid Phase-D first-reveal target scores = zero;
- no Phase-D target residual, target correlation, sign pattern, or T has been observed;
- no latent-state architecture has been selected.

The two stopped pre-D0 runs `33510176784` and `33510519140` remain non-authoritative pretarget failures and do not contain Phase-D target results.
