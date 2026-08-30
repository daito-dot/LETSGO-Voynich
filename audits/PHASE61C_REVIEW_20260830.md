# Phase 61C independent review — 2026-08-30

Status: audit-only. No accepted `main` result is modified.

## Verdict

Phase61C **validly passes its frozen preregistered first joint gate**. The plan, implementation freeze, executable and result were committed in the correct order, the exact ZL3b input identity is checked, model selection is training-leaf-only, and held-out leaves are not used to choose parameters.

However, the scientific interpretation must remain narrower than “A1 reproduces the Voynich line-position grammar.” The frozen line-position target is the **mean eta2 over 11 features**, and a new held-out decomposition shows substantial coordinate-level mismatch hidden by that mean.

## Freeze chronology

- `PLAN_C.md`: commit `5744f37771c9dda471394c5c4f59fa5c825b3eb4`, 2026-08-30 11:26:56Z
- `IMPLEMENTATION_C.md`: commit `f24b9bbbc057f6f613a7e019bb75369de1867d7e`, 2026-08-30 12:22:24Z
- executable: commit `f081e0cd20048df2bcf86d16802761c91a0c5fd0`, 2026-08-30 12:24:36Z
- held-out result: commit `ca2184950497800a8cd2f18ec99fc279b029efdf`, 2026-08-30 12:30:09Z

This is consistent with prospective freezing before the stored held-out result.

## Frozen gate result

Generated / Voynich held-out ratios:

- entry projection: `0.7969`
- local-prev10: `0.7169`
- line-position eta2 mean: `1.1163`

All are inside the preregistered `[0.5, 2.0]` broad-regime gate, so `A1 SURVIVES first joint gate` is a correct procedural verdict.

## Cross-fit review

The executable correctly performs, per outer physical-leaf fold:

- feature scaling from training leaves;
- real-entry direction estimation from training leaves;
- entry-shape scoring from training leaves;
- 16-pair parameter selection using training metrics only;
- held-out evaluation only after parameter selection.

The original implementation does share the full-manuscript token-type inventory across folds. A separate stricter audit already removed held-out-only vocabulary from every fold and found nearly unchanged primary ratios (`0.7947`, `0.7181`, `1.0981`) with exactly the same selected parameter pairs. Therefore full-vocabulary sharing is not driving the frozen survival verdict.

## New line-position eta2 decomposition

The frozen `line_position_eta2_mean` averages eta2 across these 11 features:

TTR, mean length, length SD, unit inventory, unit entropy, first entropy, last entropy, edit1 fraction, local-prev10, k/t mass, and k-share.

Replaying the exact frozen selected models and held-out seeds gives:

| feature | real eta2 | A1 eta2 | A1 / real |
|---|---:|---:|---:|
| TTR | 0.01464 | 0.00968 | 0.661 |
| mean length | 0.09668 | 0.02517 | 0.260 |
| length SD | 0.01922 | 0.00598 | 0.311 |
| unit inventory | 0.11872 | 0.05824 | 0.491 |
| unit entropy | 0.06680 | 0.05056 | 0.757 |
| first entropy | 0.04123 | 0.05360 | 1.300 |
| last entropy | 0.01001 | 0.02590 | 2.587 |
| edit1 fraction | 0.02047 | 0.12357 | 6.037 |
| local-prev10 | 0.01975 | 0.11712 | 5.929 |
| k/t mass | 0.02174 | 0.02841 | 1.307 |
| k-share | 0.02129 | 0.00470 | 0.221 |

Only four of the eleven individual feature ratios lie inside `[0.5, 2.0]` if that broad range is applied diagnostically per coordinate. This per-coordinate rule was **not preregistered**, so it does not retroactively falsify Phase61C; it is a post-hoc diagnostic showing what the aggregate gate does and does not establish.

Grouped decomposition:

- all 11 features: ratio `1.1163`
- near-family coordinates only (`edit1_fraction`, `local_prev10`): `5.9840`
- excluding near-family coordinates: `0.6391`
- entry-shape-related coordinates (`mean_len`, first/last entropy, k/t mass, k-share): `0.7215`
- excluding near-family and k/t coordinates: `0.6238`

Thus the aggregate line-position match is partly produced by cancellation between a large near-family overshoot and under-reproduction of several other line-position coordinates. Importantly, the non-near-family aggregate is still within the original broad `[0.5,2.0]` regime, so the line-position result is not *only* the local-family feature fed back into itself.

## Scientific interpretation

Supported:

> A boundary-aware generator plus one bounded local-family mechanism can simultaneously enter the broad held-out regime for the frozen scalar entry projection, global local-prev10 level, and aggregate 11-feature line-position eta2 mean.

Not supported:

> A1 reproduces the full Voynich line-position grammar or the multivariate line-position feature profile.

The latter would require a profile-level target or new prospective holdout rather than the current mean eta2 scalar.

## Consequence

Do not reject the stored Phase61C result and do not create A2 to repair this post-hoc diagnostic. Freeze A1 as planned and carry this limitation into Phase62 family comparison. Phase62 should score N0/C0/G-A1 with a common profile-aware scorecard and the already-sealed prospective discriminator, so A1 cannot benefit from cancellation across exposed coordinates without paying for the mismatch.

## Audit provenance

Workflow run: `33312993742`

Artifact: `phase61c-eta2-decomposition`

Executable: `audits/phase61c_eta2_decomposition.py`
