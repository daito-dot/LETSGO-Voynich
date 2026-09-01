# Issue #75 Phase F0 — sharded aggregate attempt 1 failure

Date: 2026-09-02  
Status: **TEN SCIENTIFIC SHARDS COMPLETE / AGGREGATE REJECTED BEFORE AUTHORITY**

Isolated sharded run:

- run `33548214504`
- execution head `2f90f3e866f171b5d43d37e85c02260ae7c0710d`
- all 10 `(fold,family)` scientific shard jobs completed successfully and uploaded artifacts;
- aggregate job `99997423536` failed before authority upload or repository commit;
- `stage-f0` was not created.

## Mechanical aggregate failure

The aggregator required separately refitted M5 baselines from the G2 and G3 shard for the same outer fold to agree within `1e-10` in total log likelihood.

For outer fold 2 it observed:

- G2-shard M5 training conditional log likelihood `-29226.896105040003`;
- G3-shard M5 training conditional log likelihood `-29226.89609443809`;
- absolute difference approximately `1.06019e-5 nat` over roughly twenty thousand training tokens.

This is approximately `5e-10 nat/token`, many orders of magnitude below the frozen Phase-F0 predictive-support threshold `0.01 nat/token`.

The two shard jobs independently executed the same optimizer on separate hosted runners. The equality check was therefore stricter than cross-run floating-point optimizer reproducibility.

## Firewall

The aggregate process aborted at this M5 baseline consistency check before computing or printing the five-fold G2/G3 support vectors or an F0 classification.

No aggregate JSON was uploaded, no authority was committed, and no candidate held-out value from the shard artifacts is used here to set a scientific threshold.

The only information used for the repair is the cross-run M5 baseline discrepancy reported by the failed consistency check.
