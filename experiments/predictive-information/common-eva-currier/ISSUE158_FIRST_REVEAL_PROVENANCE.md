# Issue #158 — Currier-gate incremental information first reveal provenance

Date: 2026-09-07
Status: **SCIENTIFIC FIRST REVEAL COMPLETE**

Frozen classification:

> **`CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`**

## Frozen chronology

- corrected score-free Gate0 merged in PR #159 at `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- post-Gate branch created from that exact merge;
- scientific scorer committed before any target workflow at `eb72dc18845c71684b2d82b4c7b1fa0b6a5fcfaf`;
- frozen scorer blob `e7a70a10dd7b663f3482993b0adfa8f804816158`;
- first-reveal workflow added afterward at `ecacac235d1b7682152c926c8fa70454c328416e` and pins that scorer blob exactly;
- no Issue #158 target result was available when the scorer architecture, class set, pooled weights, support rule, or pass rule were frozen.

## Authoritative first reveal

- workflow: `Issue158 Currier-gate first reveal`
- run: `34076400927`
- exact workflow head: `ecacac235d1b7682152c926c8fa70454c328416e`
- conclusion: `success`
- artifact ID: `10002205049`
- artifact ZIP digest: `sha256:ff54c0e617745cc747db6913a9f56d6f1d09bfa0ce9df7cd8c5e532d08c67462`
- result JSON SHA-256: `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`

The workflow passed merged-Gate ancestry/blob assertions, frozen source verification, target-free synthetic self-test, scientific scoring, frozen classification assertions, and artifact upload.

## Reproduced authority

The scorer reproduced:

- Issue #158 Gate0 result SHA-256 `605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099`;
- Gate script blob `4dbc919f3e9ededa17d2e10f56de46c98456cdea`;
- corrected Gate provenance blob `07595bf7314cfb71763eba1a810bfd3aaa01a239`;
- frozen plan blob `9ae7d7ea54aca4deea76f482b10010114cc1dac7`;
- Gate merge `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- Issue #155 scorer blob `0d57fdd32d298773b5ee38f97c9f104d29fa8377`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

## Frozen decomposition

For each reading `T`, Currier regime `R`, and outer fold:

- `POS2_T,R`: target-local generic common-EVA model;
- `EDGE_POOL_T,R`: only BODY first-atom probability uses `C_POOL = 0.5*C_A^MATCH + 0.5*C_B^MATCH`;
- `EDGE_REGIME_T,R`: only BODY first-atom probability uses target regime `C_R^MATCH`.

All other factors are identical and target-reading / target-Currier native. Fixed `k=2`, `alpha=.01`, `V=32`; unsupported exact context uses the empty additive distribution. No target-native fallback, rho, temperature, calibration, interpolation, mixture, hand/section/domain conditioning, or latent state is used.

Primary quantities:

`G_pool = bits(POS2) - bits(EDGE_POOL)`

`G_Currier = bits(EDGE_POOL) - bits(EDGE_REGIME)`

and the exact decomposition check is

`G_pool + G_Currier = bits(POS2) - bits(EDGE_REGIME)`

within `1e-12` in every reading × regime × fold cell.

## Results

### Currier A

ZL3b:

- `G_Currier` by fold: `[+0.1064675191, -0.0303223825, +0.0590524282, +0.0882553912, +0.0929307143]`
- mean `G_Currier = +0.0632767341 bit/token`
- positive folds `4/5` — PASS
- `G_pool` by fold: `[-0.0844717369, +0.1079766976, -0.0080416491, -0.0597247608, +0.0123729668]`
- mean `G_pool = -0.0063776965 bit/token`
- mean full target-regime edge gain `+0.0568990376 bit/token`.

IT2a:

- `G_Currier` by fold: `[+0.1124583515, -0.0405523891, +0.0617081595, +0.0681372129, +0.1373794960]`
- mean `G_Currier = +0.0678261662 bit/token`
- positive folds `4/5` — PASS
- `G_pool` by fold: `[-0.0715435876, +0.1302769880, +0.0073140407, -0.0024092186, -0.0180269517]`
- mean `G_pool = +0.0091222541 bit/token`
- mean full target-regime edge gain `+0.0769484203 bit/token`.

Currier A is therefore robustly gated in both independent readings.

### Currier B

ZL3b:

- `G_Currier` by fold: `[+0.1454391724, +0.0892340771, +0.1210768230, +0.1187060172, +0.0315745566]`
- mean `G_Currier = +0.1012061293 bit/token`
- positive folds `5/5` — PASS
- `G_pool` by fold: `[+0.0646070471, +0.0484399242, +0.0461049074, +0.0727643279, +0.1146793550]`
- mean `G_pool = +0.0693191123 bit/token`
- mean full target-regime edge gain `+0.1705252416 bit/token`.

IT2a:

- `G_Currier` by fold: `[+0.1501079569, +0.0850797434, +0.1257723008, +0.1214304078, +0.0404501521]`
- mean `G_Currier = +0.1045681122 bit/token`
- positive folds `5/5` — PASS
- `G_pool` by fold: `[+0.1180823131, +0.0882443232, +0.0855566684, +0.1055181559, +0.1224168316]`
- mean `G_pool = +0.1039636584 bit/token`
- mean full target-regime edge gain `+0.2085317706 bit/token`.

Currier B is therefore robustly gated in both independent readings.

## Cross-reading stability

The incremental Currier-gate effect is nearly the same in the two readings:

- Currier A mean difference `ZL3b - IT2a = -0.0045494321 bit/token`;
- Currier B mean difference `ZL3b - IT2a = -0.0033619829 bit/token`.

This is the key transport result: the boundary architecture and its Currier-conditioned contrast reproduce across ZL3b and IT2a, while Issue #155 showed that substituting the wrong Currier literal table fails strongly in both directions.

## Interpretation boundary

Accepted claim:

> Under the frozen common-EVA, reading-balanced, context-mass-matched model family, the observable Currier A/B regime label contributes robust held-out predictive information to the previous-terminal → next-initial boundary rule in both Currier regimes, independently in both ZL3b and IT2a.

The result supports a compact observable hierarchy: reading-independent boundary architecture with a Currier-conditioned literal transition mapping.

It does **not** identify words, plaintext, semantics, language, cipher family, authorship, historical production mechanism, hoax/artificiality, or a decipherment. It also does not establish that Currier is the only possible observable partition or that no further low-dimensional compression of the A/B contrast exists.

## Firewall

The artifact records all post-reveal scientific-change flags as false:

- no context/atom reselection;
- no Currier-label change;
- no pooled-weight change;
- no support-match change;
- no `k`, `alpha`, smoothing, or fallback tuning;
- no rho/temperature/calibration/interpolation/mixture fit;
- no hand/section/domain conditioning;
- no latent-state fit;
- no S1/S2/H62/R1 tuning;
- no semantic/cipher/historical inference.

Refs #88 #145 #151 #155 #158 #159 #160.
