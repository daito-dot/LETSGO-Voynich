# Hypothesis ledger addendum — Issue #75 Phase B

Status: **PHASE B COMPLETE / M3 LICENSED**

## H75-M2 — generic K/R/S occupancy geometry plus slot main effects is sufficient

Prediction: a cross-fitted M2-KRS generator should fall within frozen Phase-A M+ variation if coarse occupancy geometry carries the required R1 information.

Frozen test: 31 target-blind M2 corpora; candidate-owned reference/test calibration; ZL3b and IT2a separate; `T=min(R_ZL3b,R_IT2a)`; paired comparison to frozen M+ center; allowed loss `0.009768313008182594`.

Result: **rejected**.

- median T: `0.28733805532370377`
- median R ZL3b: `0.28733805532370377`
- median R IT2a: `0.2954904251327472`
- median gap vs M+ center: `-0.6777560206049392`
- no material loss: `false`

Interpretation: `(K,R,S)` geometry recovers a nontrivial part of topology but is far from sufficient. A compact state/configuration mechanism beyond coarse geometry is required by the tested hierarchy.

Authority: `experiments/minimal-occupancy-generator/stage-b-first-reveal/phase75b_aggregate.json`, SHA-256 `f0c5e9e210f3cf9bd0fa9c9b818c0ee61649a906b051998346db1583c60fb566`.
