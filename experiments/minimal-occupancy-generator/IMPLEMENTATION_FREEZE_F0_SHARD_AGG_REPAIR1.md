# Issue #75 Phase F0 — shard aggregate repair-1 implementation freeze

Date: 2026-09-02  
Status: **FROZEN BEFORE AGGREGATE-ONLY RETRY / NO F0 CLASSIFICATION YET**

Aggregate-attempt failure record:

- commit `c9ab9368eb1b95ee999aa501836ede38c18b7c85`
- source sharded run `33548214504`
- all ten scientific shards succeeded;
- aggregate authority did not exist.

Numerical-repair plan:

- commit `c3ba85ad3cb90c28df37baac1eb69c3e2a1c7f7b`

Reconciliation implementation:

- commit `200f68c1d5af9d81b22356d04f2a4f46e7cac4c6`
- file `experiments/minimal-occupancy-generator/phase75f0_shard_baseline_reconcile.py`
- Git blob SHA-1 `db539173ce045030d84c85d2698a2cbfa690460c`

## Frozen behavior

The reconciliation program downloads/reads the already-completed raw ten-shard lattice from run `33548214504` and performs no candidate fit.

For each fold it requires exact M5 selected-start equality and the predeclared cross-run numerical tolerances. It then replaces only the redundant G3-shard `m5` metadata object with the numerically equivalent G2-shard `m5` metadata object so that the original frozen exact-equality shard aggregator can proceed.

Before replacement it serializes the G3 candidate object and verifies it is unchanged after baseline reconciliation. No candidate field is modified.

The audit output records only raw shard SHA-256 identities and M5 baseline discrepancies. It does not perform model selection.

The aggregate-only retry must:

1. download the exact ten artifacts from run `33548214504`;
2. reconcile redundant M5 metadata under this frozen audit;
3. call the original frozen `phase75f0_shard_aggregate.py` unchanged;
4. validate the original frozen Phase-F0 decision law;
5. only then upload/commit a complete authority candidate on the isolated prep branch.
