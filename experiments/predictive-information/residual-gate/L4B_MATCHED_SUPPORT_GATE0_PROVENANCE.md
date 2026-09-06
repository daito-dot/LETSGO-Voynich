# Issue #130 L4b support-matched edge-table Gate0 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE GATE**
Parent: Issue #127

## Frozen Gate head

`20a026d155926fb38d3ee06de4619bf995539d95`

No current-initial outcome distribution, edge probability, likelihood, bits/token, rho or matched transport gain was computed or inspected before this Gate ran.

## Workflow authority

- workflow run `34029321885`
- conclusion: **SUCCESS**
- artifact `9988073625`
- artifact ZIP digest `sha256:f52fbb65c3f7d40389a5521f7e85f9a56d41c0bdc6e4a5c5e17f87920fe51d95`
- result JSON SHA-256 `a0f48878506369aa9dff60e06b60be13d41d36dd1ceef3a40c4fc63825db66f5`

The run reproduced the merged Issue #127 score-free Gate0 authority exactly:

`31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`.

## Context-matched source support

Original visible line-body edge-event counts:

- Currier A: `8,967`
- Currier B: `19,049`

Shared previous-terminal raw-byte classes: `20`.

- A-only class: byte `99`
- B-only class: byte `120`

For every shared previous-terminal class `c`, Gate0 froze:

`m_c = min(n_A(c), n_B(c))`.

Across the 20 shared classes:

- matched total per Currier regime per seed: **8,728 events**;
- A and B selected counts are exactly equal for every retained context;
- A and B selected totals are exactly equal for every seed;
- outcome-blind hash selection is deterministic under internal repeat checks.

The five frozen seeds are:

- `issue130-match-v1-r0`
- `issue130-match-v1-r1`
- `issue130-match-v1-r2`
- `issue130-match-v1-r3`
- `issue130-match-v1-r4`

Selection digests by seed:

| seed | Currier A | Currier B |
|---|---|---|
| r0 | `7b6081d6fda137f59eb8d705d5e8e4727b83b7934cfd617c0fd04aa213cd0b3b` | `57ff2e2b5e5082499f43d040f26ee83ebf0eedb1777544c4999aee157fc58372` |
| r1 | `6b9efb4f22c90ac6573a6187b952455a0a73b644e8bc604b321dd20fe41a0488` | `87c7ba3efed5699e9a551e84e0317aca44027053306a6c51fb72947693145c71` |
| r2 | `c1bc9a148857508ae13405b07f74d829246ec4b1e8af0a93c3fd64b7c064ff7b` | `16db9aebab9207ffe6a73ba26eef5a3855676516f4ed2d18495c022f4125a577` |
| r3 | `8b8c494142e5f11b2e8ea3a6643d1844f0e9f35f85d6c5e76f67c6524f383c22` | `99cea7e7ca51cf7562e72fe9e0714b49a280428653f6ef6a44ee853b7fb89f58` |
| r4 | `b1b8dfa85d823e68efea763d70ac776f23839486c5ab2cea3dcb5afe2f47bbcc` | `7f7074ab85a0b24acfb889c8c375258d5ffaece1358348e60e5a00c761f7b904` |

The per-context matched counts are identical A/B for every seed by construction and CI assertion. Major contexts retain substantial support, e.g. byte 121: 2,946 each; 108: 1,744 each; 114: 1,621 each; 110: 1,403 each.

## Frozen Gate classification

> **PASS — PROCEED TO MATCHED TABLE TRANSPORT**

This removes the gross source-table estimation-size imbalance that confounded the first L4 table-transport asymmetry: B is reduced from 19,049 to 8,728 visible source edge events while A is reduced only from 8,967 to 8,728, and each conditioning context is matched exactly rather than only the total.

## Firewall

The Gate selection identity excludes current-initial outcome and current-token string. Gate output reports no current-initial distribution or terminal→initial outcome pairs for the selected samples. It computes no edge probabilities, predictive scores, rho or transport gains.

Predictive L4b must be separately frozen after this Gate is merged.
