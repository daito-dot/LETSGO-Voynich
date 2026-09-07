# Issue #158 — Currier-gate decomposition Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

No real-target pooled-table probability, likelihood, bits/token, `G_pool`, `G_Currier`, or scientific classification was computed.

## Current authoritative chronology

Current GitHub / current branch history is the descriptive authority.

- entry main / Issue #155 merge: `6bd7c6fadb8fc590052496299c13da24f88585a2`;
- plan committed at `3bd5a7924c35dac8e21c12c833c3626c126a76ac`, plan blob `9ae7d7ea54aca4deea76f482b10010114cc1dac7`;
- score-free Gate script committed at `4e1d787e3bca61a0facd433e4c1ab0fcb7a5ec67`, Gate blob `4dbc919f3e9ededa17d2e10f56de46c98456cdea`;
- first workflow committed at `2cccd63972c66c0a3ce985eeaa3c894df8e417f1`;
- `c9f8fe74839a77ebe73db603fadfbb4707bdfc99` added an earlier provenance record, but that record referenced plan/Gate commits and blobs not present in the current repository history;
- the current-head run at `c9f8fe...` (`34075538245`) failed at the upfront frozen-blob assertion before source retrieval or Gate execution, so it produced no Gate result and no scientific metric;
- workflow-only repair `75b308785663aaee5d26a518ba33a46fd53bd819` changed only the expected Issue #158 plan/Gate blob pins to the actual already-committed current-history blobs above. It did not change the plan, Gate algorithm, pooled-table rule, support rule, representation, target population, or any scientific scoring code;
- run `34076055308` at exact head `75b308785663aaee5d26a518ba33a46fd53bd819` completed SUCCESS and is the current authoritative score-free Gate0 result.

The superseded provenance references to run `34075806201`, head `9b430a24...`, plan blob `9ae737e4...`, and Gate blob `7feb1693...` are not accepted as current authority because those referenced commits/blobs are not the objects present in the current PR history. No Issue #158 target score was exposed during this repair because this lane is Gate0-only.

## Authoritative Gate0 result

- workflow: `Issue158 Currier-gate decomposition Gate0`
- run: `34076055308`
- exact workflow head: `75b308785663aaee5d26a518ba33a46fd53bd819`
- conclusion: `success`
- artifact ID: `10002078944`
- artifact ZIP digest: `sha256:7724eff1b514516f7ed0c2a2ec0db963c42db14606548915cb66c81dabd10972`
- result JSON SHA-256: `605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099`

Gate disposition:

> **`PASS — PROCEED TO SEPARATELY COMMITTED CURRIER-GATE SCORER`**

The successful workflow completed the entry-ancestry/blob assertions, frozen-source verification, target-free synthetic self-test, score-free Gate execution, frozen Gate-contract assertions, and artifact upload.

## Reproduced entry authority

The Gate reproduced exact Issue #155 authority:

- Gate0 result SHA-256 `01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3`;
- Gate0 script blob `f5ab4fa31a92b3c303401da33611ffd5f77b402d`;
- Gate0 provenance blob `ba2f443b24237ed5ee0dce127b1a43ad082481c4`;
- first-reveal scorer blob `0d57fdd32d298773b5ee38f97c9f104d29fa8377`;
- first-reveal provenance blob `0e2fd1cbf35c2c64cfb5dcfa1529ed8dcc5292d9`;
- declared first-reveal result SHA-256 `041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737`;
- Issue #155 merge `6bd7c6fadb8fc590052496299c13da24f88585a2`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

## Frozen pooled-table construction

For every outer fold:

`C_POOL(c,y) = 0.5*C_A^MATCH(c,y) + 0.5*C_B^MATCH(c,y)`.

The input A/B matched tables are the exact rational Issue #155 Gate tables. For every retained previous-terminal context, the Gate proves with exact `Fraction` arithmetic:

`mass(A) = mass(B) = mass(POOL)`.

Current authoritative foldwise pooled identities:

| fold | contexts | positive pooled cells | pooled table SHA-256 |
|---:|---:|---:|---|
| 0 | 22 | 254 | `c03cf03a317f8531b84f12b6214e06bfe402a67776733c993fb01fda8d8725fa` |
| 1 | 19 | 247 | `4e72f0b05561684844af1f22e58988592bdf6c3c92088b00e96412110d439cf6` |
| 2 | 22 | 254 | `96fe6cbe449cd0f3916aaeb7d20952bd992f0d88f6bd6019dd4dccb48041f029` |
| 3 | 20 | 249 | `f8049dfc7a2d2041e119c671812ca4a1da29e4078166288200cd52bbf23551e5` |
| 4 | 19 | 244 | `83e91653b34891b1aa83df0fd64c085847eed3861a9ba1cee29e8ae2a9eb5a89` |

Weights remain fixed `A=1/2`, `B=1/2`; future smoothing remains `alpha=1/100`, `V=32`. No target-native fallback, rho, temperature, calibration, interpolation, or mixture fit is licensed.

The older pooled-cell counts and table SHAs recorded in the superseded provenance are not current authority.

## Support / leakage reproduction

The Gate revalidated all 20 reading × Currier × fold target-support cells under the unchanged Issue #155 target population.

- every target primary run-body cell exceeds the frozen 300-event minimum;
- every matched-context-supported cell exceeds the frozen 300-event minimum;
- minimum matched-context coverage is `1206/1209 = 0.9975186104218362` (ZL3b, Currier A, fold 1);
- all five training-union ∩ held-out-physical-leaf intersections are empty;
- held-out current first atom is never used for context selection.

## Synthetic check

The target-free synthetic test verifies:

- exact 0.5/0.5 rational pooling;
- exact A/B/POOL context-mass equality;
- finite additive-smoothed seen probability;
- finite additive-smoothed END probability under `alpha=.01`, `V=32`;
- no real target source loaded.

## Firewall

The authoritative artifact records all scientific reveal flags as false, including:

- real-target pooled probability/likelihood;
- pooled bits/token;
- `G_pool`;
- `G_Currier`;
- scientific classification;
- held-out-current-first context selection;
- pooled-weight tuning;
- Currier-label/support-rule changes;
- `k`, `alpha`, smoothing/fallback tuning;
- rho/mixture fitting;
- hand/section/domain conditioning;
- latent-state fitting;
- S1/S2/H62/R1 tuning.

## Consequence

The next allowed sequence remains:

1. merge this corrected Gate authority;
2. branch from post-Gate main;
3. commit the Issue #158 scientific scorer separately, pinned to this exact Gate result and merged blobs;
4. only after scorer blob freeze, add the first target workflow.

Refs #88 #155 #157 #158 #159.
