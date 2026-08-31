# Issue26E11D — DEV3 Voynich-blind robustness battery

Status: **COMPLETED — DEVELOPMENT ROBUST — VALIDATION STILL UNOPENED**

DEV3 was the final development battery before freezing a candidate monoalphabetic solver for the one-time locked E11D validation. It used no Voynich target data.

## Preregistration and firewall

- plan commit: `79b2be8030b8c0da397f3875a5eee399cad62d30`
- executable commit: `79b60fae7e303874dfc681dfa29b76d4e53a848a`
- workflow/head: `2dcbb21106741ac54b7a7cd1302e6d8949bf6636`
- Actions run: `33385164390`
- job: `99466052500`
- artifact: `9755392776`
- raw JSON SHA-256: `f0da9ab6630331cd28693248c2553bfa73889f179a79bf7487ab274ef2928fb7`
- artifact ZIP SHA-256: `8a54bc9aec7490e400f2fba24d3c275e3c526ea0cbe2d4ed74cbc2bd219e2df6`.

The workflow asserted absence of ZL3b/STA/cipher-benchmark target data before execution. Only frozen CREMMA medieval Latin was available.

## Development cases

Six independent known-key substitutions were generated with 40,000 retained plaintext characters each, deliberately varying the unused plaintext letter:

`q, x, z, y, k, w`.

This makes the unused 24th key position vary and prevents the single DEV2 construction from being the only tuning case.

## Candidates

Frozen candidates:

- `FREQ-HILL`: frequency-ranked initialization + deterministic 4-gram steepest pair-swap descent;
- `T001`: four conservative annealing starts at `T0=.001`;
- `T005`: same at `.005`;
- `T020`: same at `.020`.

Frozen preference if multiple candidates passed:

`FREQ-HILL > T001 > T005 > T020`.

## Result

All four candidate families are development-robust.

For **every one of the six cases and every candidate**:

- occurrence-weighted decoded-letter accuracy: **1.000**
- recovered CE excess over true key: **0.000 bits/char**
- direct scorer vs shared/incremental scorer discrepancy: **0**.

Aggregate:

| candidate | mean weighted accuracy | worst weighted accuracy | cases >=.95 | mean CE excess | worst CE excess |
|---|---:|---:|---:|---:|---:|
| FREQ-HILL | 1.000 | 1.000 | 6/6 | 0.000 | 0.000 |
| T001 | 1.000 | 1.000 | 6/6 | 0.000 | 0.000 |
| T005 | 1.000 | 1.000 | 6/6 | 0.000 | 0.000 |
| T020 | 1.000 | 1.000 | 6/6 | 0.000 | 0.000 |

The frozen preference therefore selects:

> **`FREQ-HILL`**

because it reaches the same perfect observed decoding with the least stochastic search freedom.

## Exact-key nuance

Some cases report exact 23-position key accuracy `22/23 = .95652` despite occurrence-weighted decoded-letter accuracy 1.0 and exactly identical CE. This is not a plaintext error: one observed-symbol key position can have zero occurrence in the truncated development population, making its assignment observationally unidentifiable. The decoded characters that actually occur are all correct.

Accordingly, the preregistered validation authority remains occurrence-weighted key accuracy plus held-out CE, exactly as specified in `PLAN_E11D.md`.

## Interpretation

DEV2 showed that the original E11C failure came from the excessively hot `T0=.50` annealing schedule. DEV3 now shows that the simpler deterministic frequency-seed + hill-climb solver is robust across six independent known substitutions with different unused letters.

This is still **not** the locked validation and is not evidence about Voynich. It authorizes only the next procedural step:

1. freeze `FREQ-HILL` exactly as `E11D_SOLVER_FREEZE`;
2. after that commit, create the locked 12-cipher validation executable;
3. emit the validation once;
4. do not retune E11D after seeing that validation.

Only a validation pass may authorize a separately preregistered E11E Voynich reveal.
