# Phase 2A authoritative first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE PHASE-2A RESULT**
Parent: Issue #88
Implementation issue: #94
PR: #95

## Authority

The authoritative successful reveal is the repeat at the provenance-corrected scientific head. The preceding successful run at `ca84f462...` produced the same scientific values; the later head changes only the Amendment-A chronology text.

- GitHub Actions run: `34019008294`
- head: `297822dc2fff0285de82ba7f5023d61a733b5848`
- workflow conclusion: `success`
- artifact: `issue94-phase2a-order-vs-prefix`
- artifact ID: `9984861590`
- artifact digest: `sha256:ae04c131548fb2223aee3e24b7bf382bbd99d522e4ebf35ad705eb7f1c219b67`
- `phase2a_results.json` SHA-256: `ac1a675b74153a53a542ccba993ce00a874e87df4775c55f12a93253018d6eec`

Regression gates passed:

- A0 LOCAL40 reproduces Issue #92 B1 in all five folds;
- A2 ORDERED128-FIXED reproduces Issue #92 B2 in all five folds;
- direct ordered scorer equals the accumulator implementation;
- amended direct ordered scorer reproduces the same authority.

Firewall fields are all clean:

- `future_test_tokens_used = false`
- `surface_target_metrics_scored = false`
- `issue84_target_used = false`
- `semantic_or_image_context_used = false`
- `latent_state_fitted = false`

## Preregistration chronology

The original Phase-2A PLAN and A0-A4 executable/workflow were committed before Phase-2A results. An initial workflow attempt failed before returning any outer result because a locally defined `mix_probs` helper was referenced through the imported Phase-1 namespace.

Before any successful Phase-2A result artifact, Amendment A strengthened the control side with:

- A5 `LOCAL_PLUS_PREFIX-CV`, preserving LOCAL40 while adding order-free causal-prefix inventory;
- A6 `RANDOM-LAG-CV`, retaining the same five frozen lag permutations while selecting their mixture strength by nested likelihood.

A later interface-only compatibility shim binds the identical local helper to the expected namespace. It does not change probability formulas, grids, seeds, source population or decision rules.

## Frozen result

Classification:

> **MIXED PREFIX + ORDER CONTRIBUTIONS**

Mean held-out code lengths:

| model | bits/token |
|---|---:|
| A0 LOCAL40 | 9.5961811202 |
| A1 PREFIX-BAG-CV | 9.5590296433 |
| A2 ORDERED128-FIXED | 9.5492540389 |
| A3 PREFIX-BAG-FIXED | 9.5590296433 |
| A4 RANDOM-LAG-FIXED | 9.5690181087 |
| A5 LOCAL_PLUS_PREFIX-CV | 9.5518752000 |
| A6 RANDOM-LAG-CV | 9.5690181087 |

A5 nested selections by outer fold:

`rho = .20, .21, .20, .20, .21`

A6 nested selections by outer fold:

`pi_random = .30, .30, .30, .30, .30`

Thus the calibration-robust randomized control independently returns to the same `.30` mixture used in A4; the fixed-pi random-lag result is not an artifact of forcing an unsuitable mixture strength.

## Primary amended contrasts

### Prefix inventory beyond local history

`G_prefix_cond = bits(A0) - bits(A5)`

- mean: `+0.0443059201 bit/token`
- folds: `+0.0360571, +0.0388196, +0.0622477, +0.0561319, +0.0282733`
- positive: `5/5`
- frozen criterion: **PASS**

### Actual ordered history versus local + order-free prefix inventory

`G_order_hybrid = bits(A5) - bits(A2)`

- mean: `+0.0026211611 bit/token`
- folds: `+0.0044812, +0.0034103, -0.0045379, +0.0051238, +0.0046284`
- positive: `4/5`
- frozen criterion: **PASS**

This pass is formally valid but the effect is very small and reverses in one fold.

### Actual lag/source association versus calibrated random-lag control

`G_order_random_cv = bits(A6) - bits(A2)`

- mean: `+0.0197640698 bit/token`
- folds: `+0.0162603, +0.0221712, +0.0206462, +0.0180504, +0.0216922`
- positive: `5/5`
- frozen criterion: **PASS**

## Interpretation boundary

Phase 2A establishes a predictive decomposition under this model family:

1. most of the Phase-1 apparent long-history increment is available from the order-free causal prefix inventory;
2. a smaller order/lag-sensitive residual remains under both stronger controls.

It does **not** establish:

- literal leaf-long historical memory;
- a semantic topic variable;
- syntax;
- a latent state;
- plaintext, language or cipher identity;
- that visible spaces are linguistic word boundaries.

The next program step is to localize the surviving predictive components using observable document state / independently authoritative manuscript strata and then test transport, not to fit a rich hidden-state model.