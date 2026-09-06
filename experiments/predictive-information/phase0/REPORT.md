# Issue #90 / Issue #88 Phase 0 — soft near-family / recency closure

Date: 2026-09-06
Status: **COMPLETE — AUTHORITATIVE FIRST REVEAL ARCHIVED**

Authority:

- preregistration: `PLAN.md`;
- variance-neutral target-gate correction: `AMENDMENT_A.md`;
- score-free implementation freeze: `IMPLEMENTATION_PREFLIGHT.md`;
- target-blind decay-scale boundary handling: `PREFLIGHT_A_PROVENANCE.md`, `AMENDMENT_B.md`;
- authoritative score-free selector: `PREFLIGHT_B_PROVENANCE.md`;
- first-reveal provenance: `FIRST_REVEAL_PROVENANCE.md`;
- final scientific artifact: run `34017687319`, artifact `9984482299`, `phase0_final.json` SHA-256 `028d0feb20ac92c2936611af1daee4fb9446a7473e7b4dfc8afb2d7153f4c22e`.

## Decision

> **`PREDICTIVE BUT SURFACE-INCOMPLETE`**

The likelihood-selected recency model is a materially better predictor than Issue #81 X2 and it fixes X2's raw-H62 overshoot. It nevertheless fails the complete frozen local surface responsibility because S2 is too weak and the H62 short-range concentration error remains above the frozen A1-R1 comparator.

R1 is not the blocker: all three fixed generated populations pass the complete-66 R1 gate on both ZL3b and IT2a.

No further Phase-0 retuning is licensed. Under Issue #88 the research lane moves to Phase 1: measure how much held-out sequence information remains, rather than repairing S2/H62 after reveal.

## 1. Target-blind model selection

Phase 0 prospectively compared two new forms against the Issue #81 anchor:

- `DECAY40`: an edit-distance-1 memory branch using the previous at most 40 surface tokens, with source occurrences weighted by an exponential recency kernel;
- `TILT10`: a multiplicative V2 probability tilt toward edit-1 neighbours activated by the previous at most 10 tokens;
- `X2-HARD10`: Issue #81 replay anchor.

All model/hyperparameter selection used nested literal-surface likelihood only. S1, S2, H62, R1 and Issue #84 target statistics were unavailable to the selector.

The initial score-free preflight selected `DECAY40, tau=32` in all five folds, but `tau=32` was the grid boundary. Before any target scoring, Amendment B extended the scale grid once to `{1,2,4,8,16,32,64,128,INF}` while keeping the history window fixed at 40.

The result remained identical and became an interior optimum:

| outer fold | selected family | `pi` | `tau` |
|---:|---|---:|---:|
| 0 | DECAY40 | 0.21 | 32 |
| 1 | DECAY40 | 0.21 | 32 |
| 2 | DECAY40 | 0.20 | 32 |
| 3 | DECAY40 | 0.21 | 32 |
| 4 | DECAY40 | 0.21 | 32 |

Compared with `tau=32`, the best nested-validation likelihood at `tau=64` was worse by `3.27–11.55` nats depending on fold; `tau=128` by `18.46–30.22`; and the uniform-within-40 limit by `42.96–57.49`.

Thus the tested sequence contains likelihood evidence for a broad but non-uniform recency weighting inside a bounded recent-history model. This conclusion is independent of the later surface-statistic reveal.

## 2. Predictive information

| model | mean held-out bits/token | gain vs V2 |
|---|---:|---:|
| frozen V2 / X0 | `9.708906` | — |
| Issue #81 X2-HARD10 replay | `9.649571` | `0.059336` |
| selected DECAY40 | **`9.596181`** | **`0.112725`** |

DECAY40 improves held-out code length in every outer fold:

`+0.10982, +0.11693, +0.14039, +0.10287, +0.09362 bits/token`.

The preregistered predictive criterion therefore passes `5/5` folds.

This is the clearest Phase-0 result: replacing the hard uniform previous-10 memory with a broader recency-weighted edit-1 memory almost doubles the predictive gain measured in Issue #81.

The gain remains modest relative to the total ~9.7-bit token code length. Phase 0 therefore strengthens the existence of a real local dependency without showing that local memory carries a large fraction of total token information.

## 3. S2

Frozen five-fold held-out Voynich S2 values define the immutable interval:

`0.041159 ... 0.048641`.

Selected DECAY40 aggregate:

`S2 = 0.033222`.

Three fixed realization values:

`0.034298, 0.032345, 0.033024`.

Decision:

> **S2 FAIL — too low.**

The failure is not a Monte Carlo boundary effect; all three realizations lie below the immutable target interval.

Issue #81 X2 had recovered much more of S2 while overproducing raw recurrence. The likelihood-selected broader recency kernel trades away some of that immediate/local effect.

## 4. Raw H62 recurrence amount

Frozen five-fold Voynich `abs_excess_sum` interval:

`0.037951 ... 0.068720`.

Selected DECAY40 aggregate:

`0.038792`.

Three fixed realizations:

`0.035515, 0.038721, 0.042141`.

Decision:

> **RAW H62 PASS.**

This is a material change from Issue #81 X2, whose raw recurrence was about `2.12x` the held-out Voynich magnitude. The recency-weighted architecture reduces the excess to the observed scale without using H62 for parameter selection.

## 5. H62 lag geometry

Frozen A1-R1 positive-control means:

- `mean D_profile = 0.766601`;
- `mean abs_C_short_diff = 0.117687`.

Selected DECAY40:

- `mean D_profile = 0.491159` — substantially better than the comparator;
- `mean abs_C_short_diff = 0.152967` — worse than the comparator.

Because the frozen gate requires both components to be no worse than A1-R1:

> **H62 PROFILE FAIL.**

This is informative rather than a near-total failure. The broad normalized lag profile is strong, but the model does not concentrate the short-range component in exactly the accepted way. Together with the S2 miss, this shows that maximizing held-out literal-surface prediction is not equivalent to matching the high-contrast recurrence summaries.

## 6. R1 retention

All three frozen selected-model generations reparsed at `100%` coverage and passed residual existence plus topology against both frozen readings.

| rep | ZL3b Pearson | ZL3b signs | IT2a Pearson | IT2a signs | R1 |
|---:|---:|---:|---:|---:|---|
| 0 | `0.96130` | `63/66` | `0.96067` | `64/66` | PASS |
| 1 | `0.95804` | `63/66` | `0.95946` | `64/66` | PASS |
| 2 | `0.94191` | `62/66` | `0.94878` | `63/66` | PASS |

All familywise residual/topology p-values are `1/1001` under the unchanged Issue #81/Issue #68 interface.

The local-history modification therefore leaves the compact token-internal emission grammar intact.

## 7. What Phase 0 changes

Issue #81 left an ambiguity: X2 could be viewed either as a roughly correct local-memory mechanism with an unfortunate hard window, or as a surface-target-specific trick whose predictive contribution was too small to take seriously.

Phase 0 resolves part of that ambiguity.

1. **Local edit-1 history is genuinely predictive.** A broader independently selected recency form improves held-out prediction by `0.113 bit/token`, almost twice X2's gain, and the gain is positive in every physical-leaf fold.
2. **The hard previous-10 window was not the best predictive form.** Within the frozen candidate family, a smooth `tau=32` kernel over the previous at most 40 tokens is preferred consistently.
3. **X2's raw recurrence overshoot was architectural, not an unavoidable consequence of predictive near-family memory.** DECAY40 brings raw H62 into the frozen target range without looking at H62 during selection.
4. **Prediction and surface-summary fit separate.** The best target-blind predictor still undershoots S2 and misses the frozen `C_short` criterion even while producing a better overall H62 `D_profile`.

The last point is central to Issue #88. S2/H62 are useful high-contrast diagnostics, but they cannot be treated as direct measures of the amount of predictive information in the sequence.

## 8. What Phase 0 does not license

Do not infer from DECAY40 that:

- the manuscript was historically generated by a copy/mutate algorithm;
- the 32-token decay scale has semantic or cognitive meaning;
- the text lacks plaintext or semantics;
- visible spaces are proven word boundaries;
- a latent state has been found;
- the remaining S2/C_short discrepancy should now be repaired by hand-tuning `pi`, `tau`, the neighbour kernel, or window size.

The tested mechanism is a predictive surface model.

## 9. Next move under Issue #88

Phase 0 is closed as `PREDICTIVE BUT SURFACE-INCOMPLETE`.

The next question is deliberately not “how do we make DECAY40 pass S2?” It is:

> **How much additional held-out predictive information remains beyond V2 and the selected local recency mechanism?**

Issue #92 is the Phase-1 implementation lane. It will compare increasingly informative context classes using held-out code length only, including longer-history and observable-document-state challengers plus a separately controlled flexible sequence predictor.

Only after that predictive budget is known should the program decide whether richer state/source-attribution work is warranted.