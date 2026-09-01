# Issue #75 Phase F0 — execution-only sharding fallback

Date: 2026-09-02  
Status: **PREPARED OFF THE LIVE RESEARCH BRANCH WHILE REPAIR-1 SERIAL EXECUTION IS STILL RUNNING**

This document defines a computational-scheduling fallback only. It does not change the Phase-F0 scientific design.

## Why sharding may be needed

The frozen Phase-F0 comparison requires five outer physical folds and, for each fold, a refitted M5 baseline plus exactly nine deterministic starts for G2 and exactly nine deterministic starts for G3. A single serial GitHub Actions job can therefore approach the platform timeout even though the individual fits are valid.

Repair-1 run `33545246568` remains the preferred authority if it completes and validates. This sharded fallback must not be promoted while that run can still successfully commit a valid `stage-f0` authority.

If repair-1 fails mechanically or times out before producing a validated authority, the same deterministic calculations may be scheduled independently by `(outer_fold, candidate_family)` and aggregated only after all ten shards complete.

## Scientific invariants

Sharding must not change any of the following:

- source transcription/blob;
- `SlotParser(min)` and 12-slot occupancy representation;
- five physical folds;
- M5 baseline refit implementation;
- G2 architecture, 46 parameters, starts, SHA namespaces, perturbation amplitudes, optimizer settings, gate standardization, weight floor, or likelihood;
- G3 architecture, 65 parameters, starts, SHA namespaces, perturbation amplitudes, optimizer settings, weight floor, or likelihood;
- normalization-only repair specified in `NUMERICAL_REPAIR_F0.md`;
- held-out score `log P(x|K,R,S)` per token;
- `0.01 nat/token` support threshold;
- all-five-positive-fold rule;
- G2/G3 parsimony/displacement rule;
- target-topology firewall.

No shard may read another shard's held-out result when fitting or selecting a start.

## Shard definition

Create exactly ten scientific shards:

`fold in {0,1,2,3,4} × family in {G2,G3}`.

Each shard independently:

1. reconstructs the frozen ZL3b occupancy dataset and exact physical folds;
2. holds out its assigned physical leaf;
3. refits frozen M5 on the remaining four leaves using the unchanged Phase-E fitter;
4. fits only its assigned richer family using the unchanged repaired F0 functions;
5. computes the assigned family's exact held-out conditional log likelihood and the same M5 held-out conditional log likelihood;
6. records the same selected-start, training-likelihood, weight/gate, gradient-audit, and guardrail fields needed by the full diagnostic.

The finite-difference gradient audit remains required only on outer fold 0 for each candidate family, exactly as in the serial executable.

## Aggregation

A separate aggregation job must wait for all ten shards.

It must verify:

- exactly one G2 and one G3 shard for every fold 0..4;
- both shards for a fold report identical source/fold provenance;
- both shards for a fold report the same refitted M5 selected start, training likelihood, held-out likelihood, held-out nat/token, and pi to tight numerical equality;
- all shard numerical/weight/gradient checks pass;
- no target-topology access occurred.

Only after those checks may the aggregator reconstruct the exact five-fold G2 and G3 gain vectors and mechanically apply the already-frozen Phase-F0 selection law.

No partial-shard result may be used for architecture selection.

## Authority precedence

1. If repair-1 serial run `33545246568` succeeds through validation, artifact upload, and repository authority commit, that result remains the Phase-F0 authority and this fallback is not executed.
2. If repair-1 fails or times out before a valid authority exists, the sharded complete ten-shard aggregate may become the Phase-F0 authority.
3. If both somehow complete before branch convergence, they must agree on all five held-out family scores within `1e-10 nat/token` and on the frozen classification before either is promoted. A disagreement is a numerical-audit failure, not a basis for choosing the more favorable result.

This fallback changes wall-clock scheduling only, not the tested hypothesis or decision law.
