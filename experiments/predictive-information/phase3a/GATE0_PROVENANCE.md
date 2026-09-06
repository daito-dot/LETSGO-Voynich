# Issue #104 Phase 3A — Currier A/B Gate 0 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE PRE-PREDICTION STRATUM AUTHORITY**
Parent: Issue #88

## Purpose

This record fixes the Currier A/B metadata authority, exclusions and support population before any Phase-3A predictive transport scorer exists.

No held-out predictive code length, S1/S2/H62/R1, Issue #84 target statistic, semantic label, image feature or latent state entered this gate.

## Frozen source

- ZL3b Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- source mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- corrected causal ordering: `experiments/predictive-information/source_order_authority.py`

## First score-free attempt

Run `34021103420` at head `48097faeb249c1ab761100f88653fe594b3b4be1` computed only metadata/support diagnostics.

It found one source-metadata omission:

- `f57v` has no `$L` header field;
- the adjacent comment in the same frozen ZL3b source says `Currier's language B, hand 2 (???)`;
- every other checked A/B header/comment pair agreed;
- both A and B already had nonzero support in all five frozen folds;
- no mixed A/B numeric physical leaf existed.

The first audit JSON SHA-256 was:

`5d5416fb0e87ee8fcdf7b2f3c1be3c88b0602da85de923382905d27efd8fc114`

The workflow stopped before any predictive score.

## Prereveal Amendment A

`AMENDMENT_A.md` was then frozen before any Phase-3A predictive scorer/result.

Rule:

1. `$L=A/B` remains authoritative when present;
2. only when `$L` is missing, exactly one unambiguous adjacent same-source `Currier's language A/B` comment may fill the label;
3. present non-A/B `$L` values are never overwritten;
4. header/comment conflict or conflicting comments fail the gate;
5. otherwise the page remains `UNKNOWN_OTHER`.

This one-time rule resolves exactly `f57v -> B`. No other manual relabeling is licensed.

## Authoritative amended Gate 0

Successful workflow:

- run: `34021189206`
- scientific head: `a4f1a5ca16408b126ca94b416d89c89fd83a4b0f`
- conclusion: `success`
- artifact: `issue104-phase3a-currier-gate0`
- artifact ID: `9985541887`
- artifact digest: `sha256:de11b7f7cfa99df090b9af8e16fc8def1eb632d6fe80609a20820b33e246d95e`
- result JSON SHA-256: `e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`

Gate classification:

> **PASS — PROCEED_TO_FROZEN_CURRIER TRANSPORT**

## Metadata population

Raw `$L` header distribution:

- `A`: 114 page headers
- `B`: 82
- missing: 30

Phase-3A authority after Amendment A:

- A: 114
- B: 83
- UNKNOWN/OTHER: 29

Label sources:

- header `$L`: 196
- missing-`$L` comment fallback: 1 (`f57v -> B`)
- unknown/other: 29

Currier comment checks: 197; conflicts: 0.

## Parsed prediction population

A:

- 54 numeric physical leaves
- 234 paragraph items
- 10,524 visible tokens
- 7,700 parser-accepted tokens

B:

- 40 numeric physical leaves
- 475 paragraph items
- 21,516 visible tokens
- 17,021 parser-accepted tokens

UNKNOWN/OTHER:

- 5 leaves
- 27 items
- 530 visible tokens
- 350 parser-accepted tokens

The `f57v` fallback changes metadata authority completeness but does not add a parsed paragraph item to the current prediction population.

## Mixed-leaf and exclusion audit

- mixed A/B numeric physical leaves: **0**
- mixed-leaf excluded accepted tokens: 0
- UNKNOWN/OTHER excluded accepted tokens: 350

Therefore A and B transport populations do not share a causal/reset leaf.

## Frozen five-fold support

Parser-accepted target tokens by original physical-leaf fold:

| Fold | Currier A | Currier B |
|---:|---:|---:|
| 0 | 1,881 | 2,447 |
| 1 | 1,820 | 2,964 |
| 2 | 1,761 | 3,668 |
| 3 | 1,288 | 4,159 |
| 4 | 950 | 3,783 |

All ten label/fold cells are nonzero. No alternative fold construction is licensed or needed.

## Order authority

The successful gate verifies:

- numeric paragraph order valid;
- raw source page/panel order valid;
- frozen physical-leaf fold identity retained.

## Firewall

The Gate-0 executable reports:

- predictive scores computed: false;
- surface target metrics scored: false;
- Issue #84 target used: false;
- semantic/image context used: false;
- hand/section/scribe used: false;
- latent state fitted: false.

## Consequence

Issue #104's already-frozen A↔B transport design is now executable without changing folds, H/tau, edit relation, history pools, parameter grids or decision rules.

The next scientific reveal must occur in a separate transport implementation after this authority is merged to `main`.