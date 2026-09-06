# Issue #127 L4 Currier edge transport Gate0 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE GATE**
Parent: Issue #88 / Issue #104 / Issue #125

## Gate head and execution

The Gate definition/audit head after the CI-only runtime dependency repair is:

`ab9f4d40f3872344d75b7077ab8e0f8cdaa6d483`

The preceding head `be7657fceb2a6f628385fe728769e3653b11a6d5` failed before audit execution because the workflow omitted imported runtime dependencies. It produced no Gate support result and no predictive score. The repair added only `numpy scipy` installation and changed no Gate rule, support definition, Currier authority or scientific code.

Authoritative run:

- workflow run `34028596254`
- conclusion: **SUCCESS**
- artifact `9987857434`
- artifact ZIP digest `sha256:230797cb197a218c3c9f26db5f1e4f59ed0e29f4de0c901008a61c875acf1eac`
- result JSON SHA-256 `31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`

## Frozen Phase 3A Currier authority

The audit reproduced the existing Phase 3A score-free Currier authority exactly:

- JSON SHA-256 `e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`
- Gate PASS
- no eligible mixed A/B physical leaves
- fold identity SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`
- the sole frozen comment fallback remains `f57v -> B`.

## Score-free edge support

Edge event = current visible token is not first on its source line; previous symbol is the immediately previous visible token's final raw byte; current outcome is the current token's first raw byte. Scientific target count requires the current token to be SlotParser-accepted; the previous token need not be accepted, matching Issue #125 EDGE2 construction.

### Currier A global

- items `234`
- source lines `1,557`
- visible line-body edges `8,967`
- accepted edge targets `6,634`
- previous-terminal classes `21`
- current-initial outcomes `15`
- observed terminal→initial pairs `147`

By fold accepted edge targets / terminal classes / initial outcomes / pairs:

- fold0: `1608 / 18 / 15 / 100`
- fold1: `1608 / 17 / 14 / 94`
- fold2: `1512 / 18 / 15 / 108`
- fold3: `1102 / 17 / 14 / 83`
- fold4: `804 / 15 / 13 / 75`

### Currier B global

- items `475`
- source lines `2,467`
- visible line-body edges `19,049`
- accepted edge targets `15,217`
- previous-terminal classes `20`
- current-initial outcomes `16`
- observed terminal→initial pairs `158`

By fold accepted edge targets / terminal classes / initial outcomes / pairs:

- fold0: `2197 / 14 / 13 / 84`
- fold1: `2629 / 16 / 15 / 99`
- fold2: `3271 / 15 / 14 / 103`
- fold3: `3728 / 15 / 15 / 103`
- fold4: `3392 / 18 / 15 / 114`

Every one of the ten A/B × fold cells has substantial accepted edge support. The smallest is A-fold4 with 804 accepted targets, 15 previous-terminal classes and 13 current-initial outcomes.

## Frozen Gate classification

> **PASS — PROCEED TO FROZEN EDGE TRANSPORT**

The support Gate therefore does not block a bidirectional Currier transport test.

## Firewall

This Gate computed no edge probabilities, likelihoods, bits/token, transport gains, scalar strengths, Issue #84 targets, hand variables, semantic/image variables or latent states.

Issue #127 remains open. Predictive transport must be separately frozen after this Gate is merged.
