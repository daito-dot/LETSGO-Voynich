# Issue #75 Phase F0 — isolated sharded fallback execution authorization

Date: 2026-09-02  
Status: **AUTHORIZED ON `issue75-f0-sharded-prep` ONLY**

The live repair-1 serial run `33545246568` is still running and retains scientific-authority precedence if it succeeds.

To avoid waiting for a likely serial timeout before beginning equivalent computation, the already-frozen ten-shard fallback may execute now on the isolated branch `issue75-f0-sharded-prep`.

This isolated execution:

- must call only the frozen shard runner and aggregator from `IMPLEMENTATION_FREEZE_F0_SHARDING.md`;
- must use the same source blob and frozen dependencies;
- may write `stage-f0` only to `issue75-f0-sharded-prep`;
- must not move or write the live `issue75-minimal-occupancy-generator` branch;
- cannot supersede a successful serial authority merely by finishing earlier;
- becomes promotable only if the serial live run fails/times out before producing a validated authority;
- if both complete, their five G2 and G3 held-out scores must agree within `1e-10 nat/token` and their classifications must be identical before the sharded branch may be treated as a replication.

No partial shard result is scientific authority or may be used for architecture selection.
