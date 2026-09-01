# Issue #72 V2 — FI implementation freeze before target access

Date: 2026-09-01  
Status: **SCORER AND AGGREGATION LAW FROZEN; NO FI TARGET SCORE YET**

The normative FI design is `STAGE_C1_FI_PLAN.md`, committed at `a053efd9803b6c0f74614986289c54a8add7d904` before the Stage D1/PT first reveal.

The FI implementation was added only after Stage D1 completed, without changing the preregistered FI design:

- scorer commit: `efad503afeb45500a8e520680ed7189bf9ee33f1`;
- aggregation-law commit: `285fb10db3f92df401f3f459d73827590af637a7`.

The scorer implements exactly the two preregistered families:

- `FI-G`, indices `0..198`, allocation namespace `issue72v2:C1:FI-G:allocation:<index>`;
- `FI-M`, indices `0..198`, allocation namespace `issue72v2:C1:FI-M:allocation:<index>`.

Each scored allocation uses the preregistered candidate-owned reference namespace `issue72v2:C1:<family>:reference:<index>` and `N_ref=1000`.

The identity authority is the exact Stage-A/Issue68 rep0 primary surface SHA-256 `47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`, with 33,574 complete token instances, 7,146 distinct complete tokens, 29,759 parser-accepted instances, and pooled coverage 0.886370405671055.

The identity measurement is not rescored as part of FI. The preregistered fixed identity statistic remains `T_identity=0.8830282501011794`.

The aggregate implementation uses exactly:

- `p_F = (1 + count(T_perm >= T_identity)) / 200` for each family;
- Holm step-down correction across exactly FI-G and FI-M;
- family-wise alpha `.05`;
- the four-outcome interpretation map already frozen in the plan.

No coverage threshold, arbitrary topology threshold, permutation selection, drop, reroll, extra family, target-reading average, or global R1 PASS/FAIL class is introduced.

At this freeze point no FI-G/FI-M target reference has been loaded by the new scorer, and no FI Q, residual vector, topology correlation, T value, randomization p-value, or allocation classification has been produced. The next licensed action is target-blind replay/allocation preflight only.
