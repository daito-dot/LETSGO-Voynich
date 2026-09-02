# Issue #75 Phase E — PRETARGET execution freeze

Date: 2026-09-01  
Status: **AUTHORIZED FOR ONE COMPLETE 31-CASE M5 FIRST REVEAL**

At this freeze there are zero valid Phase-E target scores.

## Frozen scientific chain

1. Permanent Phase-D insufficiency authority:
   - aggregate SHA-256 `c15ffb92030220596cacef9db9cb3bdb26c92607f675c24ff0fa607e16764489`
   - classification `M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED`
2. Final Phase-E preregistration:
   - commit `b2ef72d19111445f164d68ded813f1f81e297af6`
3. Phase-E generator:
   - commit `e6eb4fd32a7428a152b6370562f29eb453e4f049`
4. Target-blind E0 authority:
   - run `33512983928` — success
   - generation head `3e1eb27b18cdc087808658763745ca185580d65d`
   - permanent E0 commit `e89023ba6508822f77b49d2bc46a02e35b7a0f15`
   - E0 authority SHA-256 `4c406e60872f8fcfd27901cc41901db04c1aa192fa9ee91a14c01ea3dbe46a89`
5. E0 freeze metadata:
   - commit `09929843dfe280490c037b1d520f0833011b40e8`
6. Frozen scorer:
   - commit `98392e084a94e55f723dff9d0c94994385ac61f7`
7. Frozen aggregate decision code:
   - commit `46637f293c6d20c831614d4277767e6454790137`
8. Target-blocked candidate-null smoke:
   - commit `9cb0a473a33cafbfa873b282a78180671c6e9287`

## Pretarget replay/null authority

Workflow:

- run `33513586351` — success
- execution head `c26353ca1288fd41ed15086d3a83ba5da81e350e`
- permanent evidence commit `9fea627e74e0cde136877b059c867d954d8a838e`
- directory `experiments/minimal-occupancy-generator/stage-e-pretarget/`
- artifact ID `9802706196`
- artifact digest `sha256:d9c799c2be566f4a3eb81922468e2605697e2072723006253d52203aab051c42`

Exact replay:

- rep 0 occupancy SHA `1a651c319a4dbc52c357fbae9671a1d3ea421f5ff67c8e6a5544c6b42250f21c`
- rep 30 occupancy SHA `4eda55f6b9582784264e5c48f4f3c85b198b0ac6cfe81287d0c34473f1020959`
- both exactly equal frozen E0 authorities
- rep0 replay JSON SHA-256 `0be44eaad00617645a627942f9011ad11375824ccf60efec0c5e690366246b85`
- rep30 replay JSON SHA-256 `a325cdb6e9978099c7a1fe24ee8216da245dcb19ae2e30e0e877d1dd49bb9ec5`
- all replay target-access flags false

Candidate-owned-null smoke, rep 0:

- JSON SHA-256 `3e4e4d356b1e79845e40bcbd483d225fb48fc0a2281d12c987bd481e2f43044c`
- `N_ref=1000`, `N_test=1000`
- complete residual vector length `66`
- residual energy `E=3.117192571696727`
- `p_exist=0.000999000999000999`
- reliability `W=0.9687471374075881`
- target loader monkeypatched to hard-fail if called
- ZL3b target loaded: false
- IT2a target loaded: false
- target correlation: false
- target sign agreement: false
- T: false

## Training-only M5 facts frozen before reveal

Across five cross-fit training splits:

- selected deterministic starts: `2 / 3 / 2 / 2 / 3`;
- canonicalized global `pi`: `0.5051 / 0.5007 / 0.4848 / 0.4893 / 0.4890`;
- M5 conditional training log-likelihood gain over nested M3: `+8764.61 / +8526.69 / +8118.01 / +8258.54 / +8502.17` total log units;
- approximately `+0.415 .. +0.425` nat per training token;
- generated E0 distinct-signature range `859..904`.

This training-only evidence shows a stable two-regime occupancy structure but is not itself evidence that M5 reproduces R1 target topology.

## First-reveal contract

Exactly one complete first-reveal population is authorized:

- family `M5-KRS-2MIX-CHAIN` only;
- reps `0..30`, all 31 required;
- use the frozen E0 parameters, not refitting or reselecting starts;
- exact regeneration of each E0 occupancy SHA before target access;
- unchanged candidate-owned `1000` reference / `1000` test null;
- complete 66-edge residual vector;
- frozen ZL3b and IT2a target references loaded only after candidate measurement;
- readings reported separately;
- `T=min(R_ZL3b,R_IT2a)`;
- no case selection;
- no drops;
- no rerolls;
- no target-selected component, start, pair, hyperparameter, or repair.

## Frozen primary decision

Reuse exact Phase-A aggregate SHA:

`fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

and q95 tolerance:

`delta_plus=0.009768313008182594`.

For each rep:

`D_M5[r]=T_M5[r]-T_plus_center_PhaseA[r]`

and:

`gap_M5=median_r D_M5[r]`.

If:

`gap_M5 >= -0.009768313008182594`

classify:

`M5_KRS_TWO_LATENT_CHAIN_MODES_SUFFICIENT`

and **STOP** the R1 model-complexity ladder.

Otherwise classify:

`M5_KRS_TWO_LATENT_CHAIN_MODES_INSUFFICIENT_RICHER_LATENT_OR_CONFIGURATION_RULE_REQUIRED`.

Only the latter licenses a separately preregistered richer latent frontier.

Paired M5-M3, M5-M4, q90/q99, mixture weights, and training likelihood gains are secondary diagnostics only and cannot alter the primary decision.

## Target-history firewall

At this freeze:

- E0 target access = zero;
- exact replay target access = zero;
- candidate-null smoke target access = zero;
- valid Phase-E target scores = zero;
- no Phase-E target correlation, sign pattern, or T has been observed;
- no richer Phase-F latent architecture has been selected.