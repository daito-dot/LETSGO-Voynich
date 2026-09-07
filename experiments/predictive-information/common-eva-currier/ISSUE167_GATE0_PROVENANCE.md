# Issue #167 — sparse Currier outcome Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

No held-out `EDGE_SPARSE_K` probability or likelihood, `G_sparse`, `G_missing`, or minimal-K scientific classification was computed.

## Frozen chronology

- current-main entry: `5545b2657d058abea7973df2386a095b805669ef`;
- preregistration plan committed before Gate code at `f364028ad16692bba44ba2e343b21bf68532da18`, plan blob `d5b79c64ffc8297672f2de39f6478156ee3442b7`;
- score-free Gate script committed separately afterward at `b0ff342af1e3e711f6d2b4649582fe5319ed86b0`, Gate blob `5b3aac1a03ef087340f6e0ffd241a4909476c815`;
- workflow committed only after both were frozen at `8bc9e390ae9953dd7d17eeacf66236237c2a6ab9`, pinning the plan and Gate blobs exactly;
- no Issue #167 scientific scorer exists at Gate0 time.

## Authoritative Gate0 result

- workflow: `Issue167 sparse Currier outcome Gate0`
- run: `34079560066`
- exact workflow head: `8bc9e390ae9953dd7d17eeacf66236237c2a6ab9`
- conclusion: `success`
- artifact ID: `10003249272`
- artifact name: `issue167-sparse-currier-gate0-8bc9e390ae9953dd7d17eeacf66236237c2a6ab9`
- artifact ZIP digest: `sha256:1891c57c52b53050633097fbc76d0eb57983d6d7a0ed0f17beef497364be08ba`
- result JSON SHA-256: `ff5dfe546333f6e454bb5a36907f88f30ade2ecb36354f20064879e16276484c`

Gate disposition:

> **`PASS — PROCEED TO SEPARATELY COMMITTED SPARSE CURRIER SCORER`**

## Reproduced #161 authority

The Gate pins and reproduces:

- Issue #161 Gate0 result SHA-256 `32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94`;
- Issue #161 Gate script blob `00e5bddc0484b9472bb4fce9dadb89dd52bf578f`;
- Issue #161 Gate provenance blob `67e91ba26a76898f679a5182828ab3e9f512d49a`;
- Issue #161 scientific scorer blob `d24149977770118505f2147c5aa2bb727631906f`;
- Issue #161 first-reveal provenance blob `73100548fef5dbc0d08a1951e3c0ca5b370cd6f4`;
- Issue #161 declared result JSON SHA-256 `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`;
- Issue #161 Gate merge `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`;
- Issue #161 science merge `72ff98da2eac4b830dd02eae7623577362c29150`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

The exact support-matched A/B/POOL tables, equal aggregate masses, frozen 32-outcome order, and full #161 `W_A`/`W_B` identities were reproduced in all five folds. Held-out physical-leaf overlap remained empty and the #161 support/leakage cells were reproduced.

## Frozen training-only sparse ranking

For every outer fold, the Gate constructs exact smoothed aggregate probabilities

`q_R(y)=(G_R(y)+0.01)/(M+0.01*32)`

and ranks the fixed outcomes by

`J(y)=(q_A(y)-q_B(y))*ln(q_A(y)/q_B(y))`.

All `J(y)` values are nonnegative to the frozen numerical criterion. Exact ties use the frozen #161 vocabulary order. No held-out current outcome enters ranking or support selection.

Ranking identities:

| fold | ranking SHA-256 | top-1 | frozen top-16 in rank order |
|---:|---|---|---|
| 0 | `1a178da8419936818c9f263137a40a8d3daa26925ed26eee6cb6bedfe7705b66` | `l` | `l, cth, d, a, ckh, o, s, ch, q, cph, y, r, cfh, c, n, x` |
| 1 | `7256de83003d7e02668888076ef06403d9400b9c00eb0af6af3c9c3c1087c478` | `cth` | `cth, l, a, d, ckh, o, q, ch, s, cph, r, cfh, y, c, n, k` |
| 2 | `343b74b6db63f0beb8d842def94d56a655ac43bdaa1d831f319ffff2f205d3dc` | `l` | `l, cth, a, d, ckh, q, o, s, r, ch, cph, cfh, y, c, n, x` |
| 3 | `05d551f67e613133fbd61a8a2e06fabf617d415ae74619e28bd805aa0ef6ef61` | `l` | `l, cth, d, a, ckh, o, q, s, r, ch, cph, y, cfh, i, c, n` |
| 4 | `77c6aecf5465bf7c0406a41c01eb9194771e0571dc6c0fd1623fe59c549459f3` | `l` | `l, cth, d, a, ckh, q, s, o, y, r, cph, ch, cfh, n, c, g` |

These are training-derived EVA outcome identifiers only; the Gate assigns no semantic interpretation to them.

## Frozen sparse family audit

For each fold and `K ∈ {1,2,4,8,16}`:

- `S_K` is exactly the top-K prefix of the frozen training ranking;
- strict nesting `S_1 ⊂ S_2 ⊂ S_4 ⊂ S_8 ⊂ S_16` passes;
- `W_R^K(y)=W_R(y)` only inside `S_K`, with unit multiplier outside;
- both A and B sparse conditionals are exactly normalized over all 32 outcomes in every retained previous-terminal context;
- no Currier×previous-terminal parameter is introduced;
- unsupported target-native fallback remains forbidden.

The target-free synthetic control confirms that a selected global outcome shift is represented, an excluded outcome retains unit multiplier, and no previous-terminal interaction is introduced.

## Firewall

The artifact records false for every scientific-reveal/tuning flag, including:

- held-out sparse target probability or likelihood;
- `G_sparse` and `G_missing`;
- minimal-K classification;
- held-out target outcome ranking/selection;
- K-ladder or ranking-score changes;
- Currier-label, representation, fold, support, or pooling changes;
- alpha/temperature/interpolation/fallback/mixture tuning;
- Currier×previous-terminal interaction;
- hand/section/domain conditioning;
- latent-state fitting;
- semantic/cipher/historical inference.

## Consequence

The only allowed next sequence is:

1. merge this Gate0 authority;
2. branch from post-Gate main;
3. commit the Issue #167 scientific scorer separately, pinned to this merged Gate result/script/provenance and the frozen plan;
4. only after scorer blob freeze, add the first target workflow.

Refs #88 #158 #161 #164 #165 #167 #169.
