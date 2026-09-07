# Issue #158 — Currier-gate decomposition Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

No real-target pooled-table probability, likelihood, bits/token, `G_pool`, `G_Currier`, or scientific classification was computed.

## Chronology

- frozen plan commit `3bd204c47da60bcc30e5b73910e0e919b20cccac`, plan blob `9ae737e4d5c6b5e0a3ad483fa815d5968b486183`;
- score-free Gate script commit `29ca315ca981241371494229631c5b33a7c277d2`, Gate blob `7feb169377294144988aa1dcf8f1a40da9a5a924`;
- first workflow/head commit `9b430a24b63e2b037fe6288873624fd8b2ee4d1d`;
- PR #159 opened only after plan, Gate, and workflow were committed;
- no Issue #158 scientific scorer existed before the successful Gate run.

## First successful Gate authority

- workflow: `Issue158 Currier-gate decomposition Gate0`
- run: `34075806201`
- exact workflow head: `9b430a24b63e2b037fe6288873624fd8b2ee4d1d`
- conclusion: `success`
- artifact ID: `10001992308`
- artifact ZIP digest: `sha256:ffe37517b8288da87798b7694e8abf6b08b0325255f757c10a4d70fc4c56dba2`
- result JSON SHA-256: `8d2ca00de132660dc9003e5297961be7f0306f58f05fd4d05dc81d7f0ea79e16`

Gate disposition:

> **`PASS — PROCEED TO SEPARATELY COMMITTED CURRIER-GATE SCORER`**

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

The input A/B matched tables are the exact rational Issue #155 Gate tables. For every retained previous-terminal context, the Gate proves:

`mass(A) = mass(B) = mass(POOL)`

with exact `Fraction` arithmetic.

Foldwise pooled identities:

| fold | contexts | positive pooled cells | pooled table SHA-256 |
|---:|---:|---:|---|
| 0 | 22 | 248 | `bd7390d8872ab440b4543ac8b1182e7cf1f4da96b726e0fed08ee1c04ac0dac6` |
| 1 | 19 | 242 | `df9502a8ac2550a1f580836c14ad09757443fe1991a6d45aef342a88d02becf5` |
| 2 | 22 | 239 | `205fd8c79ba8bc2bc747d361ef27c85e81a502829be3ac31f0ba391ee98bd954` |
| 3 | 20 | 241 | `87663ad697debeee1d7068ef55e083a896e52168459644222412549b5fc8de8d` |
| 4 | 19 | 230 | `5073c5a9175ef125037ff35ca752252931bef73f389a83faf5d2768e3696a99b` |

Weights are fixed `A=1/2`, `B=1/2`; future smoothing remains `alpha=1/100`, `V=32`. No target-native fallback, rho, temperature, calibration, interpolation, or mixture fit is licensed.

## Support / leakage reproduction

The Gate reuses and revalidates all 20 Issue #155 target reading×Currier×fold support cells, including the same >=300 total and >=300 matched-context-supported BODY thresholds.

For every fold:

- training union ∩ held-out physical leaves = empty;
- retained previous-terminal contexts are exactly the Issue #155 contexts;
- held-out current first atom is not used for context selection.

## Synthetic check

The target-free synthetic test verifies:

- exact 0.5/0.5 rational pooling;
- exact A/B/POOL context-mass equality;
- finite additive-smoothed seen probability;
- finite additive-smoothed END probability under `alpha=.01`, `V=32`;
- no real target source loaded.

## Firewall

The artifact records all scientific reveal flags as false, including:

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

The next allowed sequence is:

1. merge this Gate authority;
2. branch from post-Gate main;
3. commit the Issue #158 scientific scorer separately, pinned to this exact Gate result and merged blobs;
4. only after scorer blob freeze, add the first target workflow.

Refs #88 #155 #157 #158 #159.
