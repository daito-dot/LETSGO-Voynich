# Issue #75 Phase F0 — execution-sharding implementation freeze

Date: 2026-09-02  
Status: **FROZEN OFF LIVE BRANCH / MAY BE PROMOTED ONLY IF REPAIR-1 SERIAL AUTHORITY FAILS**

Normative execution-sharding plan:

- commit `f9a452f8f865a12dfa6c1a946677d35a955b5f33`
- file `experiments/minimal-occupancy-generator/F0_EXECUTION_SHARDING_PLAN.md`

Exact fold-family runner:

- commit `a96ca018fccac26298d6cc02a98032637a476036`
- file `experiments/minimal-occupancy-generator/phase75f0_shard_runner.py`
- Git blob SHA-1 `2a2034facf3365ecd4eb0a273c9dd502dc8a6f13`

Exact ten-shard aggregator:

- commit `e540cca7e698cb16d6fdc18b82912af6ab50e4e9`
- file `experiments/minimal-occupancy-generator/phase75f0_shard_aggregate.py`
- Git blob SHA-1 `c9c6590c7938e55a031864ce5423e142dd0967b9`

## Equivalence contract

The shard runner imports the already-frozen normalization-repaired F0 implementation. It does not redefine any candidate objective, start, gradient, optimizer policy, support rule, or target firewall.

Each `(fold,family)` shard reconstructs the same source dataset, refits the same M5 baseline, and calls the same `fit_g2` or `fit_g3` function that the serial repaired executable calls.

The aggregator refuses to proceed unless exactly ten shards exist and the independently repeated G2/G3 M5 baselines agree within `1e-10` on:

- selected deterministic M5 start;
- training conditional likelihood;
- held-out conditional likelihood;
- held-out nat/token;
- global M5 `pi`.

It then applies the same frozen Phase-F0 predictive-support and architecture-selection law.

No partial shard output may become a scientific authority.

## Authority precedence

The live repair-1 serial run `33545246568` remains preferred if it completes through validation and authority commit. This sharding implementation exists only as a mechanically equivalent timeout fallback and is intentionally developed on `issue75-f0-sharded-prep` so it cannot interfere with the live branch or its running push.
