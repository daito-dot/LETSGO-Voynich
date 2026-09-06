# Phase 0 score-free Preflight A provenance

Date: 2026-09-06
Status: **SUPERSEDED FOR FINAL SELECTION BY PREREVEAL AMENDMENT B; RETAINED AS AUDIT EVIDENCE**

Preflight A was executed before any DECAY40/TILT10 S1/S2/H62/R1 target score existed.

## Authority

- GitHub Actions run: `34016219452`
- scientific / workflow head: `f28cbe50b922fd6f8c4e74f0683a7f001374953f`
- artifact: `issue90-phase0-preflight`
- artifact ID: `9984049876`
- artifact digest: `sha256:84126094276d7b5df644fc8cab597db7f6d6b804500db6844cbe44f3a1b942ff`
- `phase0_preflight.json` SHA-256: `0d7e207935fb58192ae99370748c9f8d4e564c67d82950b4dd44c5a0367052f7`
- explicit preflight field: `target_score_calls = 0`
- workflow conclusion: `success`

The artifact is the full authority. This file records the target-blind result that motivated the one allowed prereveal grid amendment.

## Target-blind selection result

All five outer-fold selectors chose DECAY40:

| outer fold | family | pi | tau |
|---:|---|---:|---:|
| 0 | DECAY40 | 0.21 | 32 |
| 1 | DECAY40 | 0.21 | 32 |
| 2 | DECAY40 | 0.20 | 32 |
| 3 | DECAY40 | 0.21 | 32 |
| 4 | DECAY40 | 0.21 | 32 |

Selection SHA-256: `5d44ab69783185f2cdb08295f18b800fe67e83ede75502ddf6f070a376f0a08c`.

The fold identity SHA-256 was `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

## Predictive-only result

No surface target metric entered these numbers.

- frozen X0 mean: `9.7089061017 bits/token`
- Issue #81 X2-HARD10 replay: `9.6495705599 bits/token`
- X2 gain over X0: `0.0593355418 bits/token`
- selected DECAY40 mean: `9.5961811202 bits/token`
- selected gain over X0: `0.1127249815 bits/token`
- selected gain was positive in `5/5` outer folds: `0.1098184, 0.1169346, 0.1403904, 0.1028663, 0.0936153 bits/token`
- predictive criterion: PASS

The X2 replay selector returned `pi=0.10` in all five folds, reproducing the archived Issue #81 likelihood result.

TILT10 did not narrowly lose. Its best setting was `beta=0.40` in every fold, with DECAY40 ahead by roughly `745–834` summed nested-validation nats depending on outer fold.

## Why this preflight is not the final selector authority

`tau=32` was the **largest preregistered decay scale** and was selected in all five folds. More importantly, best nested likelihood improved monotonically from `tau=1` through `2,4,8,16,32` in every outer fold.

This is a target-blind boundary hit. Freezing `tau=32` without checking whether the selector wants a flatter kernel would turn an arbitrary grid edge into a scientific conclusion.

No history-window extension is licensed here. Phase 0 remains bounded to the previous 40 surface tokens. Amendment B only extends the decay scale inside that already-frozen 40-token window and includes an exact uniform-within-40 limit. If the uniform limit wins, Phase 0 stops extending; longer history belongs to Issue #88 Phase 1.
