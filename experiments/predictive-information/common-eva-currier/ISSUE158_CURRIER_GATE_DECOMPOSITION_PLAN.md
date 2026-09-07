# Issue #158 — incremental predictive information of the Currier gate

Status: **FROZEN BEFORE REGIME-NEUTRAL POOLED-TABLE SCORING**
Date: 2026-09-07
Parent: Issue #88
Entry result: Issue #155 / PR #157

## Entry authority

Issue #155 frozen classification:

> **`COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`**

Authority:

- Gate0 merge `920130f721b83902c000c48f951c499a660f0683`;
- Gate0 result SHA-256 `01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3`;
- Gate0 script blob `f5ab4fa31a92b3c303401da33611ffd5f77b402d`;
- Gate0 provenance blob `ba2f443b24237ed5ee0dce127b1a43ad082481c4`;
- first-reveal scorer blob `0d57fdd32d298773b5ee38f97c9f104d29fa8377`;
- first-reveal provenance blob `0e2fd1cbf35c2c64cfb5dcfa1529ed8dcc5292d9`;
- first-reveal result SHA-256 `041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737`;
- first-reveal run `34075146845`, artifact `10001781210`;
- PR #157 merge `6bd7c6fadb8fc590052496299c13da24f88585a2`.

## Question

How much held-out predictive information is added by the observable Currier A/B regime label itself after support, effective mass, common-EVA representation, reading consensus, folds, and all non-edge factors are held fixed?

## Frozen starting tables

For each outer fold reuse the exact Issue #155 Gate0 rational tables:

- `C_A^MATCH(c,y)`
- `C_B^MATCH(c,y)`.

For every retained previous-terminal context `c`, Issue #155 already enforces:

`sum_y C_A^MATCH(c,y) = sum_y C_B^MATCH(c,y) = m(c)`.

Define the regime-neutral table prospectively:

`C_POOL(c,y) = 0.5*C_A^MATCH(c,y) + 0.5*C_B^MATCH(c,y)`.

The weights are fixed and untuned. Because A/B masses already match, `C_POOL` has exactly the same total effective mass `m(c)` in every retained context.

## Frozen target-local models

For target reading `T`, Currier regime `R`, and outer fold `f`:

- `POS2_T,R`: exact Issue #155 target-local generic common-EVA model;
- `EDGE_POOL_T,R`: only BODY first-atom probability uses `C_POOL`;
- `EDGE_REGIME_T,R`: only BODY first-atom probability uses target regime `C_R^MATCH`.

All other factors are identical and target-reading/target-regime native. Fixed `k=2`, `alpha=.01`, `V=32`; unsupported exact context uses empty additive smoothing. No target-native fallback, rho, temperature, calibration, interpolation or mixture fit.

## Primary quantities

`G_pool[T,R,f] = bits(POS2_T,R) - bits(EDGE_POOL_T,R)`

`G_Currier[T,R,f] = bits(EDGE_POOL_T,R) - bits(EDGE_REGIME_T,R)`.

Within one reading/regime, Currier gating passes iff mean `G_Currier > 0` and positive in at least `4/5` folds.

Regime `R` is robustly Currier-gated only if that criterion passes independently in both ZL3b and IT2a.

`G_pool` is reported prospectively, but is not a prerequisite for recognizing positive incremental Currier information.

## Frozen classes

Exactly one:

1. `CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`
2. `CURRIER GATE ADDS ROBUST EDGE INFORMATION IN A ONLY`
3. `CURRIER GATE ADDS ROBUST EDGE INFORMATION IN B ONLY`
4. `NO ROBUST CURRIER-GATE EDGE RESIDUAL`
5. `INVALID CURRIER-GATE DECOMPOSITION`

No equivalence margin, post-reveal threshold, context selection or rescue class.

## Mandatory score-free Gate0

Before any real-target `EDGE_POOL` likelihood:

1. reproduce exact Issue #155 Gate0 result and merged blobs;
2. pin #155 first-reveal scorer/provenance/result authority;
3. reproduce all five exact rational A/B matched tables;
4. construct exact rational `C_POOL` training-only;
5. prove A, B and POOL have identical total mass separately in every retained context;
6. archive pooled rational table identities;
7. reproduce all #155 target BODY support, matched-context coverage, and zero leakage;
8. retain the same >=300 support requirements;
9. target-free synthetic exact-pooling + additive-smoothing check;
10. firewall: no real target pooled probability/likelihood, bits/token, `G_pool`, `G_Currier` or classification computed.

If authority/support fails, stop INVALID without changing the pooled rule.

## Firewall

Do not alter Currier labels, common-EVA atomization, folds, reading weights, A/B support matching, pooled weight, `k`, `alpha`, fallback or target population. Do not condition on hand/section/domain, fit latent states, tune S1/S2/H62/R1, or infer words/plaintext/semantics/language/cipher/authorship/history/hoax/decipherment.

Refs #88 #130 #145 #151 #155 #157 #158.
