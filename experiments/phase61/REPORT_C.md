# Phase 61C — A1 joint-model result

Status: **A1 SURVIVES the frozen first joint gate**.

## Question

Can A0 plus exactly one additional local-family body mechanism bring the three primary exposed structural targets into the same held-out broad regime without adding persistent paragraph state, section-specific grammar, or another line-position rule?

Frozen specification:

- `PLAN_C.md`
- `IMPLEMENTATION_C.md`
- `phase61c_joint_model.py`

Primary input was the exact ZL3b/EVA v3b file with Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.

## Compatibility audit

Before fresh evaluation, the new executable had to reproduce the already-exposed Phase61B metric regime.

Observed versus recorded Phase61B:

| metric | recorded | recomputed |
|---|---:|---:|
| edit1 type density | 0.80374 | 0.803978 |
| local-prev10 fraction | 0.09778 | 0.094228 |
| line-position eta2 mean | 0.03115 | 0.034536 |
| entry/pseudo norm | 1.28505 | 1.285053 |

All frozen compatibility gates passed. In particular, the entry/pseudo norm is reproduced essentially exactly.

## Model selection

Outer evaluation used five physical-leaf folds. Within each fold, training leaves alone selected among the frozen grid:

- entry strength: `0.5, 1.0, 1.5, 2.0`
- local-family probability: `0.05, 0.10, 0.20, 0.30`

Selected pairs by fold:

- fold 0: `(0.5, 0.20)`
- fold 1: `(0.5, 0.20)`
- fold 2: `(0.5, 0.30)`
- fold 3: `(0.5, 0.30)`
- fold 4: `(0.5, 0.20)`

The selected entry strength is therefore stable at the lowest allowed nonzero setting, while the local-family mechanism uses a moderate 0.20–0.30 activation probability.

## Held-out joint result

Across-fold held-out means:

| primary target | Voynich | A1 generated | generated / Voynich |
|---|---:|---:|---:|
| entry projection | 1.18798 | 0.94667 | **0.797** |
| local-prev10 fraction | 0.09386 | 0.06729 | **0.717** |
| line-position eta2 mean | 0.04096 | 0.04572 | **1.116** |

The preregistered broad-regime gate required every ratio to fall in `[0.5, 2.0]`. All three pass.

Fold-level ratios are heterogeneous, especially for line-position eta2, but no held-out fold requires a post-hoc mechanism to make the aggregate gate pass. The strongest line-position overshoot occurs in folds 2–3, while folds 0, 1 and 4 are near or below the Voynich level.

## Decision

A1 survives as a **structural generator family** at this gate.

This is materially different from A0. A0 produced only about 6.7% of the Voynich local-prev10 level and strongly overstated line-position structure. Adding one bounded local-family mechanism moves locality into the same broad regime and simultaneously brings line-position dependence into the aggregate Voynich regime while retaining the entry effect.

This does **not** establish that the manuscript is meaningless or that A1 is historically plausible. A1 uses the empirical Voynich token-type inventory, so edit1 type density is not an independent prediction. It also now pays an explicit complexity increment: one local-family mechanism and one fitted scalar `local_family_p` in addition to A0's boundary-aware entry parameter.

## Next action

Freeze A1. Do not create A2 now.

The next decision must compare A1 directly with:

- **N0** — source-native structured medieval plaintext;
- **B0/C0** — the same meaningful structured plaintext under a bounded, global, boundary-blind encoder.

All families must use the same scorecard and explicit complexity accounting. A genuinely new prospective holdout should be frozen before any model-family winner is claimed.

Exact compact results are in `phase61c_results.json`. The full 16-pair training grid is deterministically reproducible from the frozen executable and seeds.