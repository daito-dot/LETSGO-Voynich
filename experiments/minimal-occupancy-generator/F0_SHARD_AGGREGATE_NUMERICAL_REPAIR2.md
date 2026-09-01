# Issue #75 Phase F0 — shard aggregate numerical repair 2

Date: 2026-09-02  
Status: **FROZEN AFTER REPAIR-1 BASELINE AUDIT ABORT / BEFORE ANY F0 CLASSIFICATION**

All ten scientific shards remain the exact completed artifacts from run `33548214504`. They must not be rerun or modified.

Repair-1 failed only because the independently refitted M5 baseline differed across hosted runners by `3.4445521501780263e-07 nat/token` on outer fold 2. No candidate support vector or F0 classification was produced or inspected.

## Final cross-run M5 reproducibility audit

For the redundant M5 baseline in the G2 and G3 shard of each physical fold require:

- selected deterministic M5 start index: exact equality;
- training conditional log likelihood: absolute difference `<= 1e-3 nat` total;
- held-out conditional log likelihood: absolute difference `<= 1e-2 nat` total;
- held-out nat/token: absolute difference `<= 1e-6 nat/token`;
- global `pi`: absolute difference `<= 1e-4`.

The held-out per-token allowance is 10,000 times smaller than the preregistered `0.01 nat/token` practical predictive-support threshold.

## Unchanged pairing and decision law

Candidate gains are not recomputed against a different baseline:

- G2 keeps the `H_G2-H_M5` value produced inside its own G2 shard;
- G3 keeps the `H_G3-H_M5` value produced inside its own G3 shard;
- direct G3-vs-G2 remains the difference of their absolute candidate held-out nat/token scores on the same physical leaf.

Only redundant M5 metadata may be reconciled after the audit so the already-frozen exact-equality aggregator can consume the shard lattice.

No candidate object, candidate held-out score, selected start, fit, threshold, fold, source, parser, architecture, parameter count, or target-topology firewall may change.

The retry must download the exact ten artifacts from run `33548214504` and perform aggregation only. If another baseline-only reproducibility abort occurs, no further tolerance may be chosen from candidate values; the sharded path must instead be abandoned in favor of the serial authority or a single-run deterministic aggregation redesign.
