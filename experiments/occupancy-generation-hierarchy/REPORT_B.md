# OGH-B — second-order successor grammar: first-reveal report

Status: **FIRST REVEAL COMPLETE — FROZEN DECISION `SUCCESSOR GRAMMAR NEAR-SUFFICIENT`; R1 GENERATION LANE CLOSED**

Plan: `PLAN_B.md` (frozen first). Selection authority: `stage-b0/selection.json`. Results and hashes: `first-reveal-b/` (aggregate SHA-256 `b6bb8c3e124e9adb3d7af38c58d28c4cdc3e404f5059525c4128c9762ef204be`).

## 1. Stage B0 — target-blind selection

Five-fold cross-fitted held-out log-likelihood per token (natural log, ZL3b skeleton; no R1 statistic computed):

| model | nominal params | held-out LL by fold | gain over G4 | eligible |
|---|---:|---|---|---|
| G4 last-occupied successor (anchor) | 78 | −5.107 / −5.050 / −5.005 / −5.024 / −5.026 | — | — |
| **G7A second-order successor** | 298 | −4.900 / −4.883 / −4.826 / −4.842 / −4.843 | **+0.206 / +0.167 / +0.179 / +0.182 / +0.183**, 5/5 positive | **yes** |
| G7B K-gated successor | 631 | −5.116 / −5.081 / −4.994 / −5.014 / −5.045 | −0.009 / −0.031 / +0.011 / +0.009 / −0.019, 2/5 | no |

Selected by the frozen rule ("single eligible candidate"): **G7A**. The IT2a skeleton, not used for selection, shows the same picture (G7A +0.172 to +0.206, 5/5; G7B 2/5). Gating the successor table by total occupied count adds nothing once the successor context is known; conditioning on the two most recent occupied slots adds about 0.18 nat per token, roughly a quarter of the gap between G4 (≈ −5.04) and the saturated inventory (≈ −4.77).

## 2. Stage B1 — frozen R1 result for G7A

| arm | rep | E | W | r vs ZL3b | signs | r vs IT2a | signs | R1 gate |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| ZL3b | 0 | 3.234 | 0.987 | 0.953 | 63/66 | 0.948 | 64/66 | PASS |
| ZL3b | 1 | 3.216 | 0.985 | 0.951 | 62/66 | 0.950 | 63/66 | PASS |
| ZL3b | 2 | 3.215 | 0.991 | 0.939 | 63/66 | 0.943 | 64/66 | PASS |
| IT2a | 0 | 3.237 | 0.987 | 0.950 | 63/66 | 0.972 | 64/66 | PASS |
| IT2a | 1 | 3.215 | 0.981 | 0.962 | 64/66 | 0.970 | 65/66 | PASS |
| IT2a | 2 | 3.245 | 0.989 | 0.965 | 64/66 | 0.971 | 65/66 | PASS |

All familywise maxT p-values `1/1001`. Median `T = min(r_ZL3b, r_IT2a)` and the frozen comparison against the OGH-A anchors (not rescored):

| arm | G4 | **G7A** | G5 pairwise control | G6 ceiling | gap G7A − G6 | δ |
|---|---:|---:|---:|---:|---:|---:|
| ZL3b skeleton | 0.9011 | **0.9481** | 0.9634 | 0.9646 | **−0.0165** | 0.0098 |
| IT2a skeleton | 0.9075 | **0.9617** | 0.9572 | 0.9695 | **−0.0079** | 0.0098 |

Frozen decision (PLAN_B §5):

> **`SUCCESSOR GRAMMAR NEAR-SUFFICIENT`** — Issue #68 gate passes in 6/6 realizations; the gap to the empirical ceiling is inside the Issue #75 M+-equivalence tolerance on the IT2a arm and `0.007` outside it on the ZL3b arm.

## 3. Reading the result

- The extension recovers about three quarters of what G4 left on the table (`+0.047` / `+0.054` in median T). On the IT2a arm G7A exceeds the full pairwise maxent control (`0.962` vs `0.957`) with 298 counted probabilities instead of 78 fitted moments; on the ZL3b arm it is `0.015` below it.
- Combined with OGH-A, the token-construction law is now bracketed tightly: a second-order Markov chain over the ordered sequence of occupied slots reproduces the replicated 66-edge residual topology to within `0.01–0.02` of what memorizing the empirical signature inventory achieves, on both independent readings.
- The remaining `≈0.01` is at the level of the ceiling's own realization-to-realization variation (`δ ≈ 0.0098`). Chasing it further with a third successor rung would be fitting noise-level structure. The plan's consequence for this class therefore applies: **the R1 generation lane is closed.** The pairwise maxent (G5) remains the descriptive target; the second-order successor grammar (G7A) is the frozen compact mechanistic comparator.

## 4. What closes and what opens

Closed: "what generates R1". A compact, interpretable, memoryless-across-tokens grammar with about 300 counted probabilities does. R1 should from now on be a cheap necessary condition on a candidate mechanism's emission stage, not a discriminator.

Open, and now the correct frontier:

1. **Slot values.** OGH-A/B model only which structural positions are filled. A token's information beyond shape lies in the values chosen in each filled slot. Extending the successor grammar from occupancy to values (a token generator conditioned on the previous value) quantifies the per-token information budget for the first time and produces a complete token generator.
2. **Cross-token responsibilities.** Test whether that complete, memoryless token generator reproduces R2 (H62 near-family recurrence) and R3 (signed S1 paragraph entry). A negative result would locate the content-bearing signal in cross-token memory, where inverse methods should concentrate.

## 5. Limits

Three realizations per arm; local execution; the ZL3b arm misses the equivalence tolerance by `0.007`, so the label is "near-sufficient", not "sufficient". Nothing here bears on slot meaning, plaintext, cipher tables, word boundaries, Naibbe, R2/R3/R4, or decipherment.
