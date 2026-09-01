# Issue #72 V2 — Stage D1 authority-rebind execution adapter

Date: 2026-09-01  
Status: **PRETARGET IMPLEMENTATION / AUTHORITY REPAIR ONLY**

## Discovery

Before any Stage D1 PT R1 target score was produced, the repository was re-audited end to end.

The audit found two simultaneously preserved D1 implementation generations:

1. `d1_pt_r1_target72_v2.py` + `d1_pt_aggregate72_v2.py` form a coherent older pair, but they bind to the pre-rebind D0 authority layout.
2. commit `127c86f253a5cc12e3802d0976c96649a2c91524` added `d1_pt_r1_score72_v2.py`, which correctly binds Stage D1 scoring to the compact PT authority and the validated 155-case D0 population after the B0/D0 transport-authority repair.

The new scorer intentionally outputs only the PT R1 measurement after exact D0 surface replay. It does not compute the B2 paired-baseline delta itself. Therefore the older aggregator cannot consume its schema directly.

The existing D1 preflight workflow also invokes the older scorer and does not exercise the scorer frozen in `127c86f...`.

## Scientific firewall at discovery

This discrepancy was found while the D0 authority record still states:

- target loaded: false;
- R1 computed: false;
- scientific intervention changed: false.

No Stage D1 result directory or Stage D1 report existed at the audited branch head. No PT target result had been used to choose or alter an assignment, RNG block, shuffle, target, scoring rule, or aggregation rule.

## Repair scope

The repair is restricted to execution/transport glue:

- keep `d1_pt_r1_score72_v2.py` unchanged as the scoring authority frozen in `127c86f...`;
- add a post-score aggregation adapter for that scorer's nested output schema;
- load the already-frozen B2 top-level `per_rep` baseline from schema `issue72-v2-stage-b2-25rep-positive-control-v1` without rescoring unchanged Naibbe;
- compute the preregistered per-case `delta_R = R_PT - R_baseline`;
- aggregate exactly 31 assignments × 5 historical RNG blocks with the already-frozen Stage D1 law;
- add a new target-blind preflight for the rebind-aware scorer before any first reveal;
- retain the older scorer/workflow/aggregator unchanged for audit history, but do not use them as the authoritative rebind-aware first-reveal path.

## Target-blind preflight incident

The first rebind-aware preflight was GitHub Actions run `33493894496` at head `f93cbed3ca3b15322987cbbb21ac686c43809f8b`.

Both endpoint cases (`j0/rep0` and `j30/rep4`) passed:

- frozen repository authority SHA checks;
- exact D0 PT surface replay;
- paired baseline surface replay;
- raw/support/line-invariant replay gates;
- the target firewall, with every target-access flag false.

The run then failed in the downstream B2 baseline adapter before any target access. The adapter incorrectly looked for `positive_control_summary.per_rep`; the frozen B2 archive stores `per_rep` at the top level. This was a transport/schema mismatch only. Commit `5b5926fa1166d9361a2daf5fb80c81233f8c8f25` binds the adapter to the frozen B2 schema and adds explicit gates that the archived Issue #72 intervention surface and R1 were still uncomputed.

No Stage D1 R1 target score existed when this repair was made.

## Scientific commitments unchanged

This repair does not change any of the following:

- PT assignments `j=0..30`;
- RNG blocks `rep=0..4`;
- within-line plaintext shuffle law;
- the 155 frozen D0 PT surface identities;
- `SlotParser(min)` or the 66-edge R1 construction;
- ZL3b / IT2a target loader or separate-reading policy;
- reference namespace `issue72v2:stageD:PT:j{j}:rep{rep}:reference`;
- `N_ref=1000`;
- paired B2 baseline source;
- `D[j,t] = mean_rep(delta_R[j,rep,t])` over exactly rep0..rep4;
- `p_nonloss[t] = (1 + count_j(D[j,t] >= 0))/32`;
- `p_both = max(p_nonloss[ZL3b], p_nonloss[IT2a])`;
- descriptive-only coverage treatment;
- absence of a post-reveal hard intervention threshold.

This document licenses only the authority/schema adapter and the rebind-aware execution workflow. Any scientific interpretation remains forbidden until the complete 155-case first-reveal population has been scored and aggregated.
