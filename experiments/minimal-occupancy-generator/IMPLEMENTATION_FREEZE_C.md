# Issue #75 Phase C — implementation freeze before target access

Date: 2026-09-01  
Status: **M3 SCORER / AGGREGATION FROZEN; NO PHASE-C TARGET SCORE**

Normative scientific plan: `PLAN_C.md`.

Phase C is licensed only by the frozen Phase-B decision marker `DECISION_B_M3_LICENSED.md`.

Target-blind C0 authority:

- `stage-c0/generator_authority.json`;
- exact SHA recorded in `C0_FREEZE_C.md`;
- 31/31 M3-KRS-CHAIN corpora;
- zero drops / zero rerolls;
- no target vector, Q, residual Z, target correlation or Phase-C classification computed.

Frozen M3 model:

- joint training-only K/R/S descriptor distribution;
- within descriptor class, maximum-entropy unary position terms plus nearest-neighbor occupied-pair terms;
- gauges `h_0=0`, `J_0=0`;
- 11 free unary parameters + 10 free adjacent interaction parameters = 21 continuous parameters per cross-fit training split;
- zero explicit nonadjacent pair parameters;
- zero empirical complete-signature-specific parameters.

Frozen scorer: `phase75c_score.py`.

Before target access the scorer must:

1. verify `C0_FREEZE_C.md` and exact C0 authority SHA;
2. refit training-only descriptor/unary/adjacent moments;
3. require exact training empirical moments and descriptor distribution;
4. require fit error `<=1e-10`;
5. regenerate the requested rep with the frozen namespace;
6. require exact occupancy SHA equality with C0.

Only then may it run the unchanged candidate-owned 1000-reference / 1000-test residual calibration and load the frozen ZL3b/IT2a target vectors.

`--verify-only` stops before Q/Z and target access.

Frozen aggregator: `phase75c_aggregate.py`.

It reuses the permanent Phase-A positive-control aggregate by exact SHA:

`fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

and the frozen q95 positive-control variation:

`delta_plus = 0.009768313008182594`.

Primary decision:

`gap_M3 = median(T_M3[r] - T_plus_center_PhaseA[r])`.

- if `gap_M3 >= -0.009768313008182594`: `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_SUFFICIENT` and the R1 model-complexity ladder stops;
- otherwise: `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED`.

No target-edge loss, selected nonadjacent edge, reading average, positive-control reselection, or richer post-reveal R1 model is permitted.

The next licensed action is target-blind exact-replay preflight for reps 0 and 30, followed by one rep0 full candidate-null smoke with target loader unused. Only after both succeed may the 31-case Phase-C first reveal begin.
