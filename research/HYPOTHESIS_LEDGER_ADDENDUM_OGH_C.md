# Hypothesis ledger addendum — OGH-C

Status: **COMPLETE / FROZEN**. Authority: `experiments/occupancy-generation-hierarchy/PLAN_C.md`, `REPORT_C.md`, `stage-c0/information_budget.json`, `stage-c1/` (aggregate SHA-256 `3eeea95a9469911c52119e8c24258e04a7160dd3167c39b415cc7ab14ede4f55`).

## H-OGH-C-BITS — per-token information budget under the best memoryless grammar

**MEASURED.** Cross-fitted held-out cross-entropy on parsed ZL3b tokens: shape (G7A) `7.01` bits; shape + values (V2, second-order unit chain, target-blind selected 5/5 over V1) `9.71` bits; memorized vocabulary ceiling `9.01` bits on covered tokens with `7.0%` OOV. Values add ≈ `2.7` bits beyond shape.

## H-OGH-C-XT — a complete memoryless token grammar reproduces the cross-token responsibilities

**FROZEN LABEL `MEMORYLESS TOKEN GRAMMAR PARTIAL`; SCIENTIFIC READING: FAILS.** S1 ratio `0.03`, S2 `−0.02`, S3 `0.03` of held-out Voynich (V2; V0 and V+ likewise ≈ 0). The Phase64B H62 "viability vs N0/C0" gate passes only because the raw H62 excess of a memoryless generator (`L1 = 0.002–0.005`) is ≈ 10× smaller than Voynich's (`0.038–0.069`) and the profile normalization turns noise into an arbitrary unit vector; A1-R1 remains far better (`D 0.77`, `|ΔC_short| 0.12` vs V2 `1.14 / 0.56`).

## Methodological note

H62-P1 profile-shape distance must be preceded by a raw-excess magnitude gate in future scorecards (proposal; not applied retroactively).

## Consequence

Cross-token structure (paragraph entry, previous-10 near-family locality, line position, recurrence excess) is not a by-product of token-internal grammar plus layout. The mechanism-discriminating and content-bearing signal lives in cross-token memory; the next frontier is the smallest memory that recovers it at ≈ 10 bits/token baseline capacity.
