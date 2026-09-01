# Hypothesis ledger addendum — OGH-A minimal occupancy-generation hierarchy

Status: **FIRST REVEAL COMPLETE / FROZEN — local execution, Actions replay workflow provided**

Aggregate SHA-256: `6cabec85dcb4e49ca412df3468b544d7e427dacfb398379cb48248df7fa7a788` (42/42 jobs, 0 drops, 0 rerolls).

Authority: `experiments/occupancy-generation-hierarchy/PLAN_A.md` (frozen first), `IMPLEMENTATION_A.md`, `REPORT_A.md`, `first-reveal/PROVENANCE.md`, `first-reveal/ogh_a_aggregate.json`.

Frozen classification (plan §7, realization 0, identical on ZL3b and IT2a skeletons):

> **`COMPACT CONSTRUCTION GRAMMAR SUFFICIENT`** under the Issue #68 R1 pass gate.

## H-OGH-G1 — parser admissibility alone induces the R1 topology

**REFUTED.** `4,077/4,095` non-empty signatures are `SlotParser(min)`-admissible; uniform sampling over them gives `E ≈ 0.9–1.0`, `r ≈ 0.06–0.14`, no existence. R1 is not a representation artifact.

## H-OGH-G2/G3 — slot marginals, or marginals plus occupied-slot count, are sufficient

**REFUTED (both arms).** G2: `E ≈ 1.8–2.0`, `r ≈ 0.02–0.04`. G3: strong residual energy (`E ≈ 3.2`, `p = 1/1001`) but wrong geometry, `r ≈ 0.02–0.09`, signs `37–38/66`. Independent-harness replication of Issue #75 Phase A (M0/M1).

## H-OGH-G4 — a left-to-right grammar conditioned on the last occupied slot generates the replicated topology

**SUPPORTED UNDER THE FROZEN ISSUE #68 GATE.**

- ZL3b arm rep0: `E 3.128`, `W 0.972`, `r_ZL3b 0.917` (`62/66`), `r_IT2a 0.933` (`63/66`), all maxT `p = 1/1001`.
- IT2a arm rep0: `E 3.197`, `W 0.975`, `r_ZL3b 0.908` (`62/66`), `r_IT2a 0.933` (`63/66`).
- 78 counted conditional probabilities, add-½ smoothing, no tuning, no target access; best held-out log-likelihood of any non-saturated model (`≈ −5.04` nats/token).
- exceeds published Naibbe under the same gate (`0.883 / 0.900`) and the Issue #75 ladder to date (best M5 `≈ 0.725`).
- **not** within the Issue #75 M+-equivalence tolerance (`0.0098`): median gap to the empirical ceiling `−0.064` (ZL3b arm) and `−0.062` (IT2a arm).

## H-OGH-G5 — the topology is second-order sufficient (non-promoting control)

**SUPPORTED TO WITHIN ≈ 0.01.** Full pairwise maxent (12 + 66 moments from training folds) reaches `r 0.948–0.969`, signs `63–65/66`; median gap to the empirical ceiling `−0.001` (ZL3b arm, inside the Issue #75 tolerance `0.0098`) and `−0.012` (IT2a arm). Higher-order configuration information contributes at most about one hundredth of correlation to R1.

## H-OGH-G6 — cross-fitted empirical signature resampling reproduces R1 (ceiling)

**SUPPORTED.** `r 0.967 / 0.965` (ZL3b arm), `0.967 / 0.964` (IT2a arm); matches Issue #75 M+ (`0.964–0.966`). Re-confirms for the manuscript itself the Issue #72 FI conclusion that within-line placement is not required.

## Boundaries

No slot meaning, plaintext, cipher table, word-boundary, historical-mechanism, R2/R3/R4 or decipherment claim follows. G4 is a structural transition grammar under the frozen 12-slot coordinates.
