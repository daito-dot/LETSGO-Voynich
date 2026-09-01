# Issue #72 V2 — Stage B0 unchanged-Naibbe support freeze

Status:

> **`UNCHANGED_NAIBBE_REP0_REP4_SURFACES_FROZEN`**

No new R1 quantity was computed in Stage B0.

## Provenance

- workflow run: `33462658689`
- job: `99715920669`
- exact workflow head: `135e8ac956541e2c2259431efee0fdb064b9c03e`
- Stage-B plan first-add: `02a3376a9f81edd3a0985cecf162f84646674284`
- B0 script first-add: `cb79c12562671263f5c58b18490d976b9574f7ec`
- B0 workflow first-add: `135e8ac956541e2c2259431efee0fdb064b9c03e`
- artifact ID: `9783720673`
- artifact ZIP SHA-256: `0bdb5022c5c348b0898a8de253c2b644576c2654c19710059edabc79bb3b03b5`
- exact `stage_b0_support.json` SHA-256: `96b2865496306b48a4d843b590da32b06684520e4db6a21dd0ed0b859ca27d58`
- exact raw JSON is permanently archived at `stage_b0_support.json`.

Scientific firewall recorded:

- `rep1_rep4_R1_scored=false`
- `issue72_intervention_R1_scored=false`
- no ZL3b/IT2a target vector loaded;
- no pair Q, residual Z, E/W, topology/sign, or R1 p-value computed.

## Frozen five-surface population

These are exactly the Phase64B historical `CIPHER_REPS=5` published Naibbe realizations, fixed before Issue #68 introduced R1.

| rep | pooled primary SHA-256 | visible | parsed | coverage |
|---:|---|---:|---:|---:|
| 0 | `47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd` | 33,574 | 29,759 | 0.8863704057 |
| 1 | `8c78d8a1f18eaa3d218cf4a16ce06e8cb50c11182825606c6762061695976ba5` | 33,557 | 29,705 | 0.8852102393 |
| 2 | `cbec51a5a4740abd06935610a9dd8d3b590153d5dc71fb0fc8b9c8dab94b53ed` | 33,577 | 29,732 | 0.8854870894 |
| 3 | `c55e78842eba439b4c4d4b55a7d602b80a67415a8e46279d34b4e7649294f2dc` | 33,611 | 29,852 | 0.8881616138 |
| 4 | `0818120d4f11642597d125844f35a65c53edfad7308511eb6a9f79cb5a5f2a22` | 33,648 | 29,853 | 0.8872146933 |

Coverage range is only `0.0029513745` absolute (about 0.30 percentage points), so the unchanged-mechanism positive controls have very similar direct 12-slot interface support.

This does **not** establish narrow R1 variation. It only removes one obvious representation-support confound before B1.

## Generation-path variation is real

The unchanged mechanism nevertheless takes different stochastic paths. Ambiguity retries by rep, ordered BIS193 / CLM13027 / Mazarine915 / UBL758:

- rep0: `401 / 471 / 320 / 99`
- rep1: `492 / 475 / 334 / 117`
- rep2: `492 / 476 / 336 / 96`
- rep3: `445 / 501 / 317 / 99`
- rep4: `450 / 515 / 343 / 97`

Thus Stage B is measuring genuine stochastic realization variation of the unchanged published pipeline, not byte-identical copies.

## Implication for B1

The five surfaces are all authorized for unchanged-mechanism R1 calibration as a **T2 positive-control family**.

B1 must still separate:

1. variation caused by changing the Naibbe realization seed;
2. Monte Carlo variation introduced by the finite 1,000-reference-null residual calibration itself.

No Issue #72 intervention may be R1-scored until that calibration is frozen and interpreted.
