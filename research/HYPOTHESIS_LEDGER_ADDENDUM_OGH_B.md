# Hypothesis ledger addendum — OGH-B

Status: **FIRST REVEAL COMPLETE / FROZEN — R1 GENERATION LANE CLOSED**

Aggregate SHA-256 `b6bb8c3e124e9adb3d7af38c58d28c4cdc3e404f5059525c4128c9762ef204be`; pre-reveal head `2ea0a68482378c94218d9328192c23bdb25fe33a`. Authority: `experiments/occupancy-generation-hierarchy/PLAN_B.md`, `stage-b0/selection.json`, `REPORT_B.md`, `first-reveal-b/`.

## H-OGH-B-SEL — a compact extension of the successor grammar improves held-out occupancy prediction

**SUPPORTED for the second-order successor context (G7A), REFUTED for K-gating (G7B).** G7A gains `+0.167..+0.206` nat/token over G4 in 5/5 ZL3b folds (IT2a agrees); G7B gains in only 2/5 folds. Target-blind; G7A selected.

## H-OGH-B — the second-order successor grammar reproduces R1 within the empirical-ceiling tolerance

**NEAR-SUFFICIENT (frozen label).** Median `T`: `0.948` (ZL3b arm; gap to G6 `−0.0165`, δ = `0.0098`) and `0.962` (IT2a arm; gap `−0.0079`, inside δ). Issue #68 gate passes 6/6; signs `62–65/66`; `W ≈ 0.98–0.99`; all `p = 1/1001`. On the IT2a arm G7A exceeds the pairwise maxent control (`0.962` vs `0.957`).

## Consequence

A second-order Markov chain over the ordered occupied slots (298 counted probabilities, no tuning, no target access) reproduces the replicated 66-edge R1 topology to within `0.01–0.02` of inventory memorization on both readings. The R1 generation search is closed under PLAN_B §5; R1 becomes a cheap necessary condition for candidate emission stages. Next frontier: slot values and cross-token responsibilities (R2/R3).

No slot meaning, plaintext, cipher-table, word-boundary, historical or decipherment claim.
