# Issue #161 — outcome-only Currier factorization Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

No real-target `EDGE_OUTCOME` probability, likelihood, `G_outcome`, `G_interaction`, or scientific classification was computed.

## Frozen chronology

- post-#158/docs main entry: `45d01bfcbed9c5307f823f8d23f59cdedcab35b0`;
- initial plan commit `9785179c5f7916442441f24986c60e6148b9b5a3`;
- before any Gate code existed, one copied #158 first-reveal provenance blob in the plan was corrected against current GitHub;
- final plan commit `91043aecefd22c9c6b523a434b2b1ff84dd4befd`, plan blob `68cb29a11cb147c8ecd9e70b3349a4102744e0ed`;
- score-free Gate script committed separately at `cd5526810e9c6ee7f15d212a71e113589fa2bd1c`, Gate blob `00e5bddc0484b9472bb4fce9dadb89dd52bf578f`;
- workflow committed afterward at `8b4cec9ac610bafb031dcdad624c3f21c1c5104d` and pins both plan and Gate blobs exactly;
- first Gate run `34077029709` at exact workflow head `8b4cec9ac610bafb031dcdad624c3f21c1c5104d` completed SUCCESS.

No Issue #161 scientific scorer exists at this stage.

## Authoritative score-free result

- workflow: `Issue161 outcome-only Currier factorization Gate0`
- run: `34077029709`
- scoring/Gate head: `8b4cec9ac610bafb031dcdad624c3f21c1c5104d`
- conclusion: `success`
- artifact ID: `10002425443`
- artifact ZIP digest: `sha256:d2517c20facd273218c3767dbf4acd7ae3d68089ba039e8bfbef5b88b92bde9e`
- result JSON SHA-256: `32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94`

Gate disposition:

> **`PASS — PROCEED TO SEPARATELY COMMITTED OUTCOME-FACTOR SCORER`**

## Reproduced entry authority

The Gate reproduces and pins:

- Issue #158 Gate0 result SHA-256 `605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099`;
- Issue #158 Gate script blob `4dbc919f3e9ededa17d2e10f56de46c98456cdea`;
- Issue #158 Gate provenance blob `07595bf7314cfb71763eba1a810bfd3aaa01a239`;
- Issue #158 scorer blob `e7a70a10dd7b663f3482993b0adfa8f804816158`;
- Issue #158 first-reveal provenance blob `0f3c14d2f592dea020c180669670cafca5ba1b05`;
- Issue #158 first-reveal result SHA-256 `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`;
- Issue #158 Gate merge `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- Issue #158 science merge `1741bed875a582594dc797ef18e30dd2ef3351ce`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

## Frozen factorization

For each fold, exact Issue #158 rational `A`, `B`, and `POOL` tables are reused. For each of the fixed 32 outcomes:

`G_R(y)=sum_c C_R^MATCH(c,y)`

`W_R(y)=(G_R(y)+0.01)/(G_POOL(y)+0.01)`.

Within every retained context:

`P_OUTCOME_R(y|c) proportional to P_POOL(y|c) * W_R(y)`.

The multiplier is context-invariant. No Currier×previous-terminal×outcome interaction is present in this Gate model.

## Exact aggregate mass audit

A/B/POOL aggregate effective masses are exactly equal within each fold:

| fold | exact aggregate mass |
|---:|---:|
| 0 | `5479` |
| 1 | `5283` |
| 2 | `5452` |
| 3 | `5837` |
| 4 | `12131/2` |

The pooled aggregate outcome vector is also exactly `0.5*A + 0.5*B` outcome by outcome.

## Frozen multiplier identities

| fold | `W_A` SHA-256 | `W_B` SHA-256 |
|---:|---|---|
| 0 | `02ae710cfbb8bc955d588f89eb24a4f35d8199c52eb6cb119c3085a51f4fdc36` | `fe6e77813a4d46fb85abde4d29f7da358db513cab3af70472f56da9f6b0e8197` |
| 1 | `b12493c40cf9805ea0b11cd82f91f800e0e785580c9caa1c26319aee562b5189` | `6eb9a36216077be9b796bdeabab0b716d24f6eaceb391bdf1fcf73c637e91f6a` |
| 2 | `ef53ddce81b8ded99c6f8a9e9f6ed6ffe163fda4cf06375ef66542cb9abec230` | `45f4edbfc7c6047875b402fd5f66d93b361c8e0f653019a35c7a6af53608bb95` |
| 3 | `5a8e109a7770f7b9d4938a0b981e20d4cf114e75e5dcc1a9f6b4e610177731e3` | `d08819ab0c5e39ce6eb26f31c1b74a634f7952ba04b3389c92fe959bfbb6b6a6` |
| 4 | `3f96822404f7e1cfc15ad89eb44ee4c6c542b11a40847a56db55a515d30d886f` | `82196f48baa87ad379fe161d5e8d0f0ada944891e2ff78cb8bbd1fe328ca7119` |

All 32 outcomes are frozen in each vector, including `<END_TOKEN>` whose multiplier is exactly 1 because it has zero first-atom training count in both regime and pool.

## Outcome-only conditional identities

Exact rational normalization was verified for all 32 outcomes separately inside every retained previous-terminal context.

| fold | A conditional SHA-256 | B conditional SHA-256 |
|---:|---|---|
| 0 | `019e1c189a49a9f270bc2be807875dc026f87aeccbc7c2776058a7940baf321d` | `a7a5962dadb6ab38d3cba7f9a85dc4570d7912428f22353396f66566026c702f` |
| 1 | `7271d2bda7a46b211079635c38533e433127186e0bfd5c3a44475931d16486db` | `ac0ccb176ea7d0de8526797407443aecb1189f390e9acdb86d47161d37261d5d` |
| 2 | `622b5a7a91b4191a16313bc848a1eaa7254a0b7444a8cf65778659a48821229e` | `2984de1bc883ca93d2ec91128f36952c9c661e193e93a65c62c4e454eee424b1` |
| 3 | `6597c0678fd8858e1fe7fa5a2c1c3b2b8e546b78d5cf40fab27698e40d81e486` | `a30fca64aef0840dd1f039a79af6cc6690089cc5b4d326a795363599a2a39cef` |
| 4 | `f23a96396a32209a45e365c333dbba4a00829c08eed071f0f7ef595ac25ca583` | `cfa60d78cb3a867401468b465babc830328821b39fc76d93209967ea23e032e8` |

## Support and leakage

The exact Issue #158 reading×Currier×fold target support cells were reproduced.

- every target primary run-body count is >=300;
- every matched-context-supported target primary run-body count is >=300;
- held-out current first atom is never used for context selection;
- training-union ∩ held-out physical leaves is empty in all five folds.

## Synthetic controls

The target-free synthetic test passes both required controls:

1. a pure global outcome shift moves both contexts in the same direction under the fixed multiplier;
2. a context-specific contrast with unchanged aggregate outcome totals yields unit global multipliers and remains context-specific, proving the global multiplier cannot silently absorb that interaction.

No real target source is used in the synthetic test.

## Firewall

The Gate artifact records false for every scientific reveal/tuning flag, including:

- real-target `EDGE_OUTCOME` probability or likelihood;
- `G_outcome`;
- `G_interaction`;
- scientific classification;
- target-outcome atom/context selection;
- multiplier tuning;
- Currier-label/support changes;
- alpha/smoothing/temperature/interpolation/fallback/mixture tuning;
- hand/section/domain conditioning;
- latent-state fitting;
- S1/S2/H62/R1 tuning.

## Consequence

The only allowed next sequence is:

1. merge this Gate0 authority;
2. branch from post-Gate main;
3. commit the Issue #161 scientific scorer separately, pinned to the merged Gate result/script/provenance and plan;
4. only after scorer blob freeze, add the first target workflow.

Refs #88 #155 #158 #160 #161 #163.
