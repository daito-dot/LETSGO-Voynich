# Issue #145 — common-EVA dual edge Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

This document archives the first successful score-free Gate0 for Issue #145. It contains support/provenance only and does not change the preregistered common representation, clean-run reset rule, target population, smoothing, future POS2/EDGE2 architecture, pass rule or interpretation boundary.

## Chronology

The Issue #145 common-representation contract was frozen before any Issue #145 predictive scorer existed:

1. Issue #145 created after closed Issue #139 / merged PR #144.
2. Pre-Gate Amendment A froze maximal-clean-run reset semantics before Gate code existed.
3. plan commit: `14c57d8fd1705de042023ff0b6bd306ccbab23ca`;
4. Gate0 executable commit: `c4e544b4552ff337a1bdef7b929c3499c621c528`;
5. Gate workflow head: `245cc39ff6bb010f6058798ea04b98b05175b577`;
6. first PR-triggered Gate0 run completed successfully before any Issue #145 POS2/EDGE2 scientific scorer existed.

No Issue #145 POS2/EDGE2 probability, likelihood, bits/token, `G_common`, cross-reading effect ratio, literal-table similarity or scientific classification had been computed at this point.

## First successful Gate authority

- Issue: #145
- PR: #146
- workflow: `Issue145 common-EVA edge Gate0`
- run: `34062035436`
- workflow head: `245cc39ff6bb010f6058798ea04b98b05175b577`
- run conclusion: `success`
- artifact ID: `9997776831`
- artifact name: `issue145-common-eva-edge-gate0-245cc39ff6bb010f6058798ea04b98b05175b577`
- artifact ZIP digest: `sha256:7a234acd6564f046e25b8ecd4b368e8f2712bb0ddf2876a5254adb9b5fe3b78c`
- result JSON: `issue145_common_eva_edge_gate0.json`
- result JSON SHA-256: `563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48`

Gate disposition:

> `PASS — PROCEED TO SEPARATELY COMMITTED COMMON-EVA DUAL EDGE SCORER`

## Reproduced authorities

### Sources

ZL3b:

- SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`;
- Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`;
- header `#=IVTFF Eva- 2.0 M 5`.

IT2a:

- SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- Git blob SHA-1 `4d6d3f2537b1f507a257529b49c94af7d6e03446`;
- header `#=IVTFF EvaT 2.0 M 3`;
- 342,104 bytes / 5,444 lines.

### Common representation / parser

- Phase4A Basic-EVA authority blob `756380dcd6f1b024a359923852627460c0f64dd0`;
- Phase4B IT2a adapter blob `7520e1a5f2c64a4ccbc3cc0e65668a4e0a5391cb`;
- unchanged SlotParser blob `8bafba7f2bce4cf77c9001c729936c1ce619759b`;
- physical-leaf fold identity SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- frozen common atom outcomes: 25 Basic-EVA single atoms + 6 connected composites = 31 atom outcomes; future `END_TOKEN` makes `V=32`.

## Score-free support — ZL3b

Totals:

- P-coded loci in frozen folds: `4,119`;
- clean tokens: `28,052`;
- clean runs: `6,121`;
- run-start tokens: `6,121`;
- run-body tokens: `21,931`;
- SlotParser-accepted primary targets: `23,089`;
- accepted run-start targets: `4,835`;
- accepted run-body targets: `18,254`.

By outer fold:

| fold | clean tokens | clean runs | primary targets | primary run-body targets |
|---:|---:|---:|---:|---:|
| 0 | 4,932 | 1,156 | 4,038 | 3,122 |
| 1 | 5,440 | 1,179 | 4,392 | 3,478 |
| 2 | 6,174 | 1,311 | 5,129 | 4,073 |
| 3 | 6,039 | 1,285 | 4,993 | 3,976 |
| 4 | 5,467 | 1,190 | 4,537 | 3,605 |

Training-complement previous-terminal atom contexts: `[23, 23, 23, 23, 21]`.

Training-complement previous-terminal→initial atom pairs: `[213, 219, 211, 213, 216]`.

Observed common atom inventory uses all 31 frozen atom outcomes.

Event identity SHA-256: `41f32c690fa2d20531a34d2a29e12e0b13665fe892e93342ee65ef80e7e19cb2`.

## Score-free support — IT2a

Totals:

- P-coded loci in frozen folds: `4,118`;
- clean tokens: `32,956`;
- clean runs: `4,706`;
- run-start tokens: `4,706`;
- run-body tokens: `28,250`;
- SlotParser-accepted primary targets: `27,112`;
- accepted run-start targets: `3,636`;
- accepted run-body targets: `23,476`.

By outer fold:

| fold | clean tokens | clean runs | primary targets | primary run-body targets |
|---:|---:|---:|---:|---:|
| 0 | 5,788 | 903 | 4,729 | 4,031 |
| 1 | 6,400 | 910 | 5,171 | 4,483 |
| 2 | 7,212 | 1,016 | 6,020 | 5,220 |
| 3 | 7,128 | 1,011 | 5,896 | 5,093 |
| 4 | 6,428 | 866 | 5,296 | 4,649 |

Training-complement previous-terminal atom contexts: `[22, 22, 21, 22, 22]`.

Training-complement previous-terminal→initial atom pairs: `[251, 250, 248, 250, 245]`.

IT2a clean data observe 27 of the 31 frozen common atoms; the outcome vocabulary nevertheless remains prospectively fixed at all 31 atoms + `END_TOKEN` (`V=32`) in both readings.

Event identity SHA-256: `2effc64d9e1c733e6cea7049e6e04b2f4dc1d36d8bea56a4c0de2df6626619d8`.

## Gate conclusion

Every outer fold in both readings exceeds the preregistered minimum of 300 accepted primary targets and 300 accepted run-body targets. Every training complement has nonzero START/BODY support and broad previous-terminal context/pair support. No support repair, reading-specific atom mapping, fold regrouping or post-Gate normalization is required.

The common-EVA representation is therefore scientifically usable for the frozen dual-reading edge test.

## Firewall status

The successful Gate artifact records all of the following as false:

- scientific target metrics computed;
- POS2/EDGE2 probability computed;
- likelihood/code length computed;
- edge gain computed;
- cross-reading effect ratio computed;
- literal-table similarity computed;
- target-selected normalization;
- surface-similarity token alignment;
- latent-state fit;
- S1/S2/H62/R1 tuning.

The next step is allowed only after this Gate authority is merged: create a new branch from the Gate merge, commit the frozen common-EVA POS2/EDGE2 scorer separately, record its blob, and only then add/run its first target workflow.

Refs #88 #112 #115 #125 #139 #145 #146.
