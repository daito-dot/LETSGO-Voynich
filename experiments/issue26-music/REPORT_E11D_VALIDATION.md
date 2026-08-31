# Issue26E11D — locked monoalphabetic solver validation

Status: **COMPLETED — `E11D SOLVER VALIDATED`**

This is the one-time external/synthetic validation required before any renewed León/STA Voynich substitution probe.

## Authority chain

- parent validation design: `PLAN_E11D.md`
- frozen solver: `E11D_SOLVER_FREEZE.md` at commit `1a9d9f3e9124121f1224a6989e2d615f1870032c`
- operational validation amendment: `PLAN_E11D_VALIDATION_AMENDMENT.md` at `1f735a03dfa2a481b895b7034e07f9aee140a8cb`
- first attempted workflow: run `33386029356` — stopped before any fit or validation score because the requested 140,423-character population exceeded the complete frozen CREMMA capacity after omission of `w`; no artifact/result existed
- capacity-only amendment, before any validation score: `PLAN_E11D_VALIDATION_CAPACITY_AMENDMENT.md` at `d76ace23e56c74881d31f0017df3bc3d586ac04b`, fixing the budget to 70,000 characters
- executable revision applying only that capacity change: `442e094264f7d463174a171c60156e30799ddfe4`
- successful reveal workflow/head: `997f02cc1b07eaae2cd54375434260d2ae75b400`.

## Successful reveal provenance

- Actions run: `33386279243`
- job: `99469514227`
- artifact: `9755697025`
- raw JSON SHA-256: `0bab23a477f107792737d87d4992d5c0c7771cafdb792ca41e84cb116b901cd3`
- artifact ZIP SHA-256: `71addffd929db3bca44d79d342a36bf105e387d40ae819515f1dd1c63da8aa73`.

The job explicitly asserted absence of Voynich/ZL3b/STA/cipher-benchmark target data. Only frozen CREMMA medieval Latin was present.

## Frozen solver

`FREQ-HILL`:

1. 24-letter normalized Latin alphabet `abcdefghiklmnopqrstuwxyz`;
2. 23 observed cipher positions plus one explicit unused-letter position;
3. frequency-ranked initialization;
4. deterministic steepest pair-swap descent on the external Latin character 4-gram objective;
5. no annealing, random starts, dictionary selection, or true-key information;
6. independent direct-score implementation audit.

## Validation battery

Twelve independently constructed 23→24 monoalphabetic ciphers, each with:

- 70,000 plaintext characters;
- distinct deterministic CREMMA run rotation;
- distinct unused plaintext letter from the frozen rarity-ranked schedule;
- distinct hidden random key seed;
- five deterministic held-out folds.

Unused letters in order:

`w, k, z, y, x, h, f, g, b, q, l, p`.

## Result

Frozen classification:

> **`E11D SOLVER VALIDATED`**

Observed across all 12 validation ciphers:

- ciphers with mean occurrence-weighted accuracy >= `.95`: **12/12**
- ciphers with mean recovered-minus-true held CE <= `.05 bits/char`: **12/12**
- median mean weighted accuracy: **1.000**
- worst mean weighted accuracy: **1.000**
- worst mean CE excess: **0.000 bits/char**
- maximum reported score-implementation discrepancy: **0**.

Stronger than the aggregate gates, every individual fold of every validation cipher recovered all occurrence-weighted held-out letters correctly:

- **60/60 folds: weighted accuracy 1.000**
- **60/60 folds: recovered held CE exactly equals true-key held CE**.

All five preregistered validation gates therefore pass.

## What this establishes

This result establishes a narrow methodological capability:

> **At the sequence lengths and 23-symbol/24-letter dimensionality relevant to the León/STA model, the frozen FREQ-HILL solver reliably recovers known monoalphabetic Latin substitutions under the external CREMMA language model.**

Therefore the earlier E11C `SOLVER INADEQUATE` result is no longer a blocker to a new Voynich target run.

## What this does not establish

It is **not evidence that Voynich is Latin**, that STA families are León glyph families, or that the manuscript uses a monoalphabetic substitution. It validates the decoder/optimizer only.

## Next authorized step

A separately preregistered E11E may now apply the **unchanged frozen solver** to the reconciled E11 target population:

- source-level STA family model unchanged;
- numerical-leaf five-fold population 4,119 lines / 140,423 events;
- special `fRos` 11 lines / 166 events excluded from cross-validation only because they lack numerical leaf IDs;
- no solver retuning after target reveal.

Because E11C had already exposed a target run using an invalid solver, E11E must be described as a **validated-solver re-analysis**, not as a pristine first-ever target reveal. Its inferential strength must come from the solver firewall, held-out folds, absolute readability, and independent follow-up predictions rather than pretending the target was never previously seen.
