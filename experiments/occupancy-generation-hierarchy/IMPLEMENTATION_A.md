# OGH-A — implementation notes (frozen before target scoring)

Executable: `ogh_a.py`. Plan authority: `PLAN_A.md` (committed first).

## Exact correspondence to the plan

- **Signature space.** Masks `1..4095`; bit `s` = slot `s` occupied. Every model is materialized as an explicit probability vector over these 4,095 states, so generation is identical for all models: `numpy.random.default_rng(stable_seed(label)).choice(4095, size=n_tokens, p=vector) + 1`, one call per held-out fold, label `OGH-A:{source}:{model}:fold{f}:rep{rep}`.
- **Admissible set `A`.** `--admissible` enumerates every value assignment for every mask (4,643,467 distinct candidate strings), parses each with the unchanged `SlotParser(min)`, and keeps a mask iff at least one string's minimal parse equals that mask. The list is stored in `preflight/admissible_signatures.json`; scoring loads it and records its SHA-256. Observed manuscript signatures are asserted to lie inside `A` (they must, by construction of the parser).
- **Cross-fitted generation.** For held-out fold `f`, parameters are estimated from accepted-token signatures of the other four physical-leaf folds of the same source; the generated tokens fill exactly the skeleton positions whose token belongs to fold `f`. The skeleton contributes only line membership, order and fold label.
- **Maxent fits (G2, G3, G5).** Exact maximum likelihood by enumeration on `A`: L-BFGS-B on the convex negative log-likelihood with analytic gradient, followed by three polishing restarts. A feature whose empirical moment is exactly 0 or exactly 1 is handled as the maximum-likelihood boundary solution (states violating it are removed from the support and the feature is dropped); the number of such features is recorded. A fit is accepted only if the maximum absolute moment error is `≤ 1e-6`; otherwise the model is `FIT_FAILED` for that fold and the whole model receives no R1 score.
- **Parameter bookkeeping.** The plan's nominal parameter counts are 12 / 0 / 12 / 23 / 78 / 78 / `#observed` for G0–G6. For G3 the twelve count indicators are linearly dependent on the twelve slot marginals (`Σ_s x_s = Σ_k k·1[|x|=k]`) and on the constant (`Σ_k 1[|x|=k] = 1`), so the effective dimension is at most 22; the executable records the numerical rank of each design on `A`. These are reporting quantities and do not change any gate.
- **G4 grammar.** Left-to-right over slots `0..11`; context is the most recent occupied slot (or `none`); `P(x_s=1 | ℓ)` is estimated with add-½ smoothing. The product over slots defines a distribution on all 4,096 patterns; it is restricted to `A` (and to non-empty patterns) and renormalized. The mass on `A` before renormalization is recorded.
- **R1 scoring.** `q_views_candidate`, `build_reference`, `residualize`, `reliability`, `test_nulls`, `topology_result` are the Issue #68 `target68.py` functions with `N_FOLDS=5` (five physical-leaf folds instead of four CREMMA manuscripts). Null operation is `phase58c_residual_graph.shuffled_flat` on the candidate's own padded line matrix. Gates are unchanged: existence (`valid_folds ≥ 4`, `W ≥ .50`, `p_exist ≤ .01`) and per reading `r ≥ .70`, `p_r ≤ .01`, signs `≥ 50/66`, `p_sign ≤ .01`, with maxT over the two readings.
- **Frozen references.** `#58C` raw SHA-256 `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d` and `#58D` raw SHA-256 `f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6` are verified on every run, and the pooled ZL3b↔IT2a cross-check `r=0.9884483852763541`, `65/66` must hold before any candidate is scored.
- **Aggregate.** `--aggregate` applies the plan's ordered classification to `rep=0` of each arm and evaluates the G0 sanity gate (G0 must fail R1 and have `E` no larger than 1.5× the maximum test-null energy).

## Deviations from the plan

None at implementation freeze. Any later deviation must be recorded here before the corresponding result is used.

## Preflight (target blind)

Recorded in `preflight/preflight_ZL3b.json` and `preflight/preflight_IT2a.json` (no pair-Q, residual, or topology statistic is computed in preflight). Headline numbers are appended below after the preflight run.

### Preflight headline numbers (recorded before any R1 score)

Admissible set (`preflight/admissible_signatures.json`):

- `4,077 / 4,095` non-empty signatures are emittable by `SlotParser(min)`; only 18 are not (all involve slots 7 or 11 without the disambiguating context that lets the minimal parse choose them; singleton slots 7 and 11 are inadmissible).
- 4,643,467 distinct candidate strings were parsed; enumeration took ~351 s.
- Consequence recorded in advance: parser admissibility is a very weak constraint, so G1 is nearly uniform over all signatures and the "representation-admissibility dominant" class is unlikely on structural grounds. This is a target-blind observation about the representation, not a target result.

Skeletons:

| arm | lines | accepted tokens | fold tokens | distinct observed signatures | fraction of `A` used |
|---|---:|---:|---|---:|---:|
| ZL3b | 4,082 | 25,071 | 4430 / 4810 / 5516 / 5447 / 4868 | 643 | 0.158 |
| IT2a | 4,089 | 28,280 | 4976 / 5416 / 6261 / 6197 / 5430 | 664 | 0.163 |

Observed occupancy-count distribution (ZL3b): `|x| = 1..8` with mass `.017 / .082 / .221 / .293 / .232 / .131 / .021 / .002`; no token occupies 9 or more slots. G3 therefore drops 3–4 count indicators per fold as boundary features (support 3,998 or 3,778 states); its effective rank is 18–19. G2 and G5 have full rank (12, 78) and full `A` support. All maxent moment errors are `≤ 1.2e-8`. G4's unrestricted product measure already places `0.9999` of its mass on `A`.

Cross-fitted held-out mean log-likelihood per token (natural log; `covered` excludes zero-probability tokens, relevant only for G3 (`4e-5` of tokens) and G6 (`0.8%`)):

| model | params | ZL3b held-out | IT2a held-out |
|---|---:|---:|---:|
| G0 | 12 | −7.070 | −6.997 |
| G1 | 0 | −8.313 | −8.313 |
| G2 | 12 | −7.050 | −6.975 |
| G3 | 23 (rank 18–19) | −7.018 | −6.947 |
| G4 | 78 | −5.042 | −5.014 |
| G5 | 78 | −5.119 | −5.090 |
| G6 | 611–643 | −4.775 (covered) | −4.752 (covered) |

Note for interpretation later: with equal nominal parameter count, the left-to-right last-occupied grammar (G4) predicts held-out signatures better than the full pairwise maxent (G5) on both readings. This is a predictive-fit statement only; it says nothing yet about R1.

Primary-corpus SHA-256 prefixes (rep 0) are recorded in the preflight JSONs and must match the scored corpora.
