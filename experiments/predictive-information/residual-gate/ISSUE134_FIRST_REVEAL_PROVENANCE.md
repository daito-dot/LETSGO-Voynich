# Issue #134 first-reveal provenance

Date: 2026-09-06

This records the first successful predictive reveal for the residual-closure test frozen in `ISSUE134_AUGMENTED_CORE_PLAN.md` and admitted by the merged score-free Gate0.

## Frozen revisions

- Gate0 merged via PR #136, merge: `236b5d69fbca6e1304c4dd9c352b4abd6dbf1dcf`
- predictive scorer committed before first execution: `dbd787a457659b7d833dc06c3931f937031172b8`
- first-reveal workflow head: `b253e81b01eba4300c94496337c17be778c74e48`
- PR: #137

## First successful reveal

- workflow run: `34035108074`
- artifact: `9990011421`
- artifact digest: `sha256:c759783dd23b6390781168db83786b5f0cd19d103704adf92a2ac9d8a91a1853`
- result JSON SHA-256: `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`
- Gate0 result SHA-256 reproduced inside scorer: `3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1`
- corrected B3 normalized authority SHA-256 reproduced: `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`

## Frozen classification

**NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE**

The preregistered residual vector was exactly:

`[0.0, 0.0, 0.0, 0.0, 0.0] bits/token`

- mean `G_residual`: `0.0 bits/token`
- positive outer folds: `0/5`
- required rule: mean `> 0` and positive in at least `4/5`
- rule result: **FAIL**

This zero is not caused by an equality of the raw RESET and LINE byte experts. The source-line-local raw expert is lower-bits than the token-reset raw expert in every outer fold. Instead, nested inner validation selected final challenger mixture weight `w=0.0` for both families in every outer fold. The augmented observable core therefore receives no predictive contribution from either flexible challenger on the untouched outer folds.

## Augmented observable core

Mean across the five untouched outer folds:

| quantity | bits/token |
|---|---:|
| corrected B3 | 9.517268842963203 |
| augmented observable core | 9.451900585480233 |
| MIX_RESET | 9.451900585480233 |
| MIX_LINE | 9.451900585480233 |

Mean gain of augmented core over corrected B3:

`0.06536825748296984 bits/token`

The observable edge itself is weaker than B3 when used alone; the gain comes from the prospectively frozen probabilistic mixture. Selected augmented-core edge weights were stable and nonzero:

`rho = [0.19, 0.22, 0.20, 0.19, 0.21]`

## Fold details

| fold | B3 | augmented core | rho | RESET raw k/alpha | RESET w | LINE raw k/alpha | LINE w | G_residual |
|---:|---:|---:|---:|---|---:|---|---:|---:|
| 0 | 9.673387360496681 | 9.584639495492530 | 0.19 | 3 / 0.01 | 0.00 | 2 / 0.01 | 0.00 | 0.0 |
| 1 | 9.582906643045850 | 9.533953119326018 | 0.22 | 3 / 0.01 | 0.00 | 2 / 0.01 | 0.00 | 0.0 |
| 2 | 9.353632787765441 | 9.288676578183203 | 0.20 | 2 / 0.01 | 0.00 | 2 / 0.01 | 0.00 | 0.0 |
| 3 | 9.389649280663370 | 9.333167273238633 | 0.19 | 2 / 0.01 | 0.00 | 2 / 0.01 | 0.00 | 0.0 |
| 4 | 9.586768142844670 | 9.519066461160781 | 0.21 | 2 / 0.01 | 0.00 | 2 / 0.01 | 0.00 | 0.0 |

The augmented-core gain over B3 was positive in all five outer folds:

`[0.08874786500415155, 0.04895352371983286, 0.06495620958223824, 0.05648200742473719, 0.06770168168388935] bits/token`.

## Fallback behavior on accepted outer targets

The preregistered Currier fallback was actually exercised:

| fold | line-start | native A/B | pooled fallback | line-body fallback |
|---:|---:|---:|---:|---:|
| 0 | 540 | 3,804 | 85 | 1 |
| 1 | 548 | 4,237 | 25 | 0 |
| 2 | 661 | 4,783 | 72 | 0 |
| 3 | 617 | 4,829 | 1 | 0 |
| 4 | 564 | 4,195 | 109 | 0 |

No fallback, smoothing, grid, tie rule, challenger topology, or decision threshold was changed after reveal.

## Interpretation boundary

This result closes the preregistered predictive-residual gate only. Under this test, the previously observed source-line cross-token residual is absorbed once corrected B3 is augmented with the explicit observable terminal→initial layer and Currier-conditioned fallback policy.

It does **not** establish that Voynichese has no hidden state, and it does not identify semantics, plaintext, language, cipher mechanism, or an entropy bound. It says that Issue #134 supplies no predictive justification for escalating to a latent-state model on this residual.
