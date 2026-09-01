# Issue #75 Phase F0 — shard aggregate numerical repair

Date: 2026-09-02  
Status: **FROZEN AFTER AGGREGATE ATTEMPT-1 FAILURE / BEFORE ANY F0 CLASSIFICATION**

All ten scientific shards from run `33548214504` succeeded. Their candidate computations must not be rerun or altered for this repair.

The failed aggregator used an unrealistically strict `1e-10` tolerance on total M5 log likelihood across independently hosted runner jobs. The only observed discrepancy used to motivate this repair is the M5 baseline difference recorded in `F0_SHARD_AGGREGATE_ATTEMPT1_FAILURE.md`; no candidate support vector or classification has been inspected.

## Repaired cross-run M5 consistency audit

For the independently repeated M5 baseline in the G2 and G3 shard of the same physical fold, require:

- selected deterministic M5 start index: exact equality;
- training conditional log likelihood: absolute difference `<= 1e-3 nat` in total;
- held-out conditional log likelihood: absolute difference `<= 1e-3 nat` in total;
- held-out nat/token: absolute difference `<= 1e-7 nat/token`;
- global `pi`: absolute difference `<= 1e-4`.

The held-out score tolerance is at least 100,000 times smaller than the frozen `0.01 nat/token` predictive-support threshold and therefore cannot change a support decision except in a case already numerically unresolved at far below the preregistered practical-effect boundary.

## Candidate scoring remains unchanged

For each richer family, retain the held-out gain paired to the M5 refit from its own shard:

- G2 support uses `H_G2 - H_M5` from the G2 shard;
- G3 support uses `H_G3 - H_M5` from the G3 shard.

The direct G3-vs-G2 comparison remains the difference of their absolute held-out conditional nat/token values on the same physical leaf.

No averaging, cherry-picking, replacement fit, reroll, or favorable baseline selection is allowed.

## Scientific invariants

This repair changes only the *cross-run reproducibility audit* in the aggregator. It does not change:

- any of the ten already-completed shard computations;
- any candidate parameter, fit, deterministic start, or selected start;
- source/parser/fold populations;
- the normalization repair;
- support threshold `0.01 nat/token`;
- all-five-positive-fold requirement;
- G2/G3 parsimony/displacement law;
- target-topology firewall.

The aggregate-only retry must download the exact ten artifacts from run `33548214504` by artifact identity/pattern and must not execute G2 or G3 fitting again.
