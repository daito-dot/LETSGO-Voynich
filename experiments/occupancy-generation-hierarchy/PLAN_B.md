# OGH-B — closing the successor-grammar gap: one preregistered extension of G4

Status: **PREREGISTERED — NO OGH-B TARGET RESULT REVEALED**

Parent: `PLAN_A.md`, `REPORT_A.md` (OGH-A, merged in PR #77); Issue #75 Phases A–F0 (merged in PR #78).

## 1. Question

OGH-A showed that R1 is second-order sufficient to within ≈0.01 (G5) and that the 78-parameter last-occupied-slot successor grammar G4 reaches median `T ≈ 0.90` (gap to the empirical ceiling `−0.064` ZL3b arm, `−0.062` IT2a arm).

> **Does one compact, prospectively chosen extension of the successor grammar close the gap to the Issue #75 M+-equivalence tolerance, so that the R1 search can be declared closed?**

## 2. Frozen candidate extensions (both nest G4)

Let `ℓ1` be the most recent occupied slot before `s` and `ℓ2` the one before that (`none` if absent). Let `q4_f(s | ℓ1)` be the G4 conditional fitted on the same training folds.

- **G7A — second-order successor grammar.** `P(x_s = 1 | ℓ2, ℓ1)`, estimated with back-off to G4: `(n1 + q4) / (n + 1)` where `n1, n` are training counts in context `(ℓ2, ℓ1)`. Nominal contexts `Σ_s [1 + s + C(s,2)] = 298`. Product over slots, restricted to the admissible set `A`, renormalised.
- **G7B — K-gated successor grammar.** Draw the occupied-slot count `K` from the training distribution; conditional on `K`, use `P(x_s = 1 | ℓ1, K)` estimated with the same back-off to `q4`. The full-state distribution is `P(x) = q(K(x)) · P_K(x)`, where `P_K` is the product measure restricted to `{x ∈ A : |x| = K}` and renormalised within class. Nominal parameters `78 × 8` observed `K` classes, plus 7 for `q(K)`.

Back-off strength is fixed at one pseudo-count. No other smoothing, hyperparameter, or context set may be tried.

## 3. Frozen target-blind selection (stage B0)

Compute, on the **ZL3b skeleton only**, the five-fold cross-fitted held-out mean log-likelihood per token (natural log) of G4, G7A and G7B, exactly as in OGH-A preflight. No pair-Q, residual, correlation or sign statistic is computed at this stage.

Selection rule, applied once:

1. a candidate is *eligible* if its held-out gain over G4 is positive in at least 4 of 5 folds;
2. if neither is eligible: `NO EXTENSION LICENSED`; stop, no target score;
3. if one is eligible: select it;
4. if both are eligible: select the one with the larger median gain, unless the median gains differ by less than `0.005` nat/token, in which case select the one with fewer nominal parameters (G7A = 298 < G7B = 631).

The IT2a skeleton's held-out likelihoods are reported for information and do not affect selection. Only the selected candidate receives a target score; the other is not scored in OGH-B.

## 4. Frozen target scoring (stage B1)

Identical to OGH-A: the selected model, both skeletons, realizations `0,1,2`, seed namespace `OGH-B:{source}:{model}:fold{f}:rep{rep}`, candidate-owned nulls `OGH-B:{source}:{model}:rep{rep}:{reference,test}-null`, Issue #68 R1 gate, frozen ZL3b/IT2a targets. G4 and G6 OGH-A results are reused as anchors; they are not rescored.

## 5. Frozen decision

Let `gap_arm = median_rep T(selected) − median_rep T(G6, OGH-A)` with `T = min(r_ZL3b, r_IT2a)`; tolerance `δ = 0.009768313008182594` (Issue #75 Phase-A q95 self-difference).

- `SUCCESSOR GRAMMAR SUFFICIENT UNDER M+ EQUIVALENCE` — `gap ≥ −δ` on both arms and Issue #68 gate passes on both arms. Consequence: declare the R1 generation search closed; the token-construction law is a compact second-order successor grammar.
- `SUCCESSOR GRAMMAR NEAR-SUFFICIENT` — gate passes on both arms and `−0.03 ≤ gap < −δ` on at least one arm. Consequence: the remaining structure is small; record which pairwise couplings G5 matches and the selected grammar does not (diagnostic only), and close the R1 lane without a further rung unless a new mechanism family motivates it.
- `SUCCESSOR EXTENSIONS INSUFFICIENT` — otherwise. Consequence: the pair-specific second-order structure is not expressible as a short successor chain; do not add rungs one at a time; the pairwise maxent remains the descriptive target.

In every case the R1 lane hands over to R2/R3/R4 and to slot-value modelling afterwards.

## 6. Prohibited

Trying additional context sets or smoothing; scoring the non-selected candidate; using target edges; changing `δ`, seeds, gates or skeletons; interpreting any result as slot meaning, plaintext, or decipherment.
