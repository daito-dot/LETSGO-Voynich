# Issue #100 C1 — corrected-source-order Phase 1 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE CORRECTED PHASE-1 RESULT**

## Authority

- GitHub Actions run: `34019919131`
- head: `fab8c77c32b35bddbe490d246feaba8500495578`
- workflow conclusion: `success`
- artifact: `issue100-c1-phase1-source-order`
- artifact ID: `9985167291`
- artifact digest: `sha256:4094f0b9150ca8ea12ecc43a1f86889c53104d28baec06ca355f0a854998f279`
- `issue100_c1_phase1.json` SHA-256: `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`

Source-order authority verified:

- numeric paragraph order valid;
- raw source document/page order valid;
- ordered item-id authority SHA-256 `1775d7623946adae3e5647d87ba3258bcf75044a7d5354f14dc5023460581dfb`;
- 736 items / 206 parsed documents;
- folds unchanged.

## Corrected result

Classification remains:

> **MATERIAL PREDICTIVE INFORMATION REMAINS**

Mean held-out code lengths:

| model | corrected bits/token | legacy bits/token | corrected - legacy |
|---|---:|---:|---:|
| B0 V2 | 9.7089061017 | 9.7089061017 | ~0 |
| B1 local | 9.5943670127 | 9.5961811202 | -0.0018141 |
| B2 longer history | 9.5461691796 | 9.5492540389 | -0.0030849 |
| B3 + observable state | 9.5172688430 | 9.5203245471 | -0.0030557 |

Corrected B1 selected `H=40,tau=32` in all five outer folds. Selected pi:

- fold0 `.21`
- fold1 `.21`
- fold2 `.21`
- fold3 `.21`
- fold4 `.22`

Corrected B1 outer code lengths:

- fold0 `9.74133358571672`
- fold1 `9.653977794584556`
- fold2 `9.440059238964276`
- fold3 `9.47837639594045`
- fold4 `9.658088048445927`

Corrected B2 independently selected `H=ALL,tau=128,pi=.30` in all five folds, exactly the same architecture as the legacy Phase 1. Corrected B2 outer code lengths:

- fold0 `9.703129096315228`
- fold1 `9.611477410270004`
- fold2 `9.381483548665923`
- fold3 `9.415300895065752`
- fold4 `9.619454947593933`

Predictive increments:

- local B0→B1: `+0.1145390890 bit/token`, positive 5/5;
- longer-history B1→B2: `+0.0481978331 bit/token`, positive 5/5;
- observable-state B2→B3: `+0.0289003366 bit/token`, positive 5/5;
- flexible byte challenger over local: `+0.0147985093 bit/token`, positive only 3/5, FAIL under the frozen stability rule.

B3 continues to select only the same two observable state families with lambda `.5`: ENTRY_BODY in folds 0/3 and LINE4 in folds 1/2/4.

## Robustness judgement

The old Phase-1 scientific conclusion is:

> **ROBUST TO ORDER CORRECTION.**

The exact code lengths improve slightly under correct order, and two local-mixture fold values shift, but the selected local horizon, selected long-history architecture, sign stability, observable-state contribution and overall classification remain the same.

The C2 source-attribution rerun is therefore directly comparable to the old Phase 2A: its ordered reference remains `H=ALL,tau=128,pi=.30`, while its local reference uses the corrected B1 per-fold pi values above.

## Firewall

No S1/S2/H62/R1, Issue #84 target, semantic/image context, future token, latent state or candidate-grid extension was used.