# Hypothesis ledger addendum — Issue #75 Phase C

Status: **PHASE C COMPLETE / M3 INSUFFICIENT / NONLOCAL-OR-LATENT FRONTIER LICENSED**

## H75-M3 — exact K/R/S plus nearest-neighbor occupancy transitions are sufficient for R1

Prediction: the prospectively frozen cross-fitted `M3-KRS-CHAIN` generator should fall within the frozen stochastic variation of the empirical-signature positive control if a first-order local occupancy grammar carries the required R1 information.

Frozen architecture:

- exact training-only `(K,R,S)` descriptor distribution;
- 11 unary slot parameters;
- 10 adjacent occupied-pair parameters;
- no explicit nonadjacent pair parameters;
- no complete-signature-specific parameters;
- 31 fixed realizations;
- candidate-owned 1000 reference + 1000 test nulls;
- ZL3b and IT2a evaluated separately;
- `T=min(R_ZL3b,R_IT2a)`;
- q95 no-material-loss tolerance `0.009768313008182594`.

Result: **rejected as sufficient**.

- median T: `0.5934673293483207`
- median R ZL3b: `0.5934673293483207`
- median R IT2a: `0.619415484871579`
- median E: `3.1450497603497665`
- median W: `0.9441114543255242`
- median sign agreement: `51/66` ZL3b, `52/66` IT2a
- paired median gap vs M+ center: `-0.37325753997796984`
- no-material-loss: `false`

Interpretation: nearest-neighbor transition structure is strongly informative relative to M2 (`T≈0.287 -> 0.593`) but is not the complete construction law. Additional nonlocal coupling or latent token-construction states are required under the tested hierarchy.

Authority:

`experiments/minimal-occupancy-generator/stage-c-first-reveal/phase75c_aggregate.json`

SHA-256: `34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a`
