# Phase 60D2 — anti-coupling prospective state test

Status: frozen before execution.

## Why D2 is required
Phase60D found ~40% held-out MSE reduction when line0 predicts the recovery vector `line2-line0`, but absolute line2 prediction did not improve. Because the target algebraically contains `-line0`, regression-to-the-mean / mathematical coupling is a serious alternative explanation even though wrong-entry and shuffled-entry controls failed.

## Primary test
Use paragraphs with >=4 usable lines. Predict **absolute line3 state**, never a target containing line0 algebraically.

Compare on physical-leaf outer folds:
1. metadata only;
2. metadata + line1 state (early-body baseline);
3. metadata + line1 + entry line0 state.

The incremental value of line0 over line1 is the primary statistic.

## Secondary tests
- Predict line4 where available.
- Predict selected body coordinates from entry coordinates excluding the same coordinate (cross-coordinate prediction), preventing direct regression-to-mean exploitation.
- Same-page wrong-entry and within-section shuffled-entry controls.
- H/B/P/S/T separately.

## Falsification
The strong initialization reading of P60-4 fails if line0 adds no held-out information about later absolute body state once line1 and metadata are known.

## Interpretation
If D2 fails, retain only the weaker claim: paragraph entry and early recovery are structurally coupled, but evidence that entry initializes later state is insufficient. If D2 succeeds broadly, the initialization/state-carrying narrative gains substantially stronger support.
