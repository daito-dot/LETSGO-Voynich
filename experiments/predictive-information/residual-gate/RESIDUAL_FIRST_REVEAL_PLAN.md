# Issue #118 — flexible sequence residual first-reveal implementation lock

Date: 2026-09-06
Status: **FROZEN AFTER MERGED CORE GATE #119 AND BEFORE RESIDUAL SCORER / TARGET REVEAL**
Parent: Issue #118 / Issue #88

## Entry authority

Merged PR #119 established that the corrected source-order Phase-1 core is reproducible under `CORE_GATE0_AMENDMENT_A.md`.

The first-reveal scorer must internally rerun and verify that authority before any Issue #118 mixture score is computed. The only permitted numerical normalization is the exact one-cell Gate-0 rule already merged; normalized full JSON SHA must be:

`0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`.

## Frozen implementation interpretation of Issue #118

For each untouched outer physical-leaf fold:

1. reuse the corrected Phase-1 outer selection for B2 and B3, selected from the four inner folds exactly as in the merged authority;
2. reuse the Phase-1 byte-family inner likelihood tables but re-apply the Issue-#118 deterministic tie rule: higher likelihood, then smaller `k`, then **larger alpha**;
3. for each inner validation fold, fit the B3 probability model and the selected RESET or CONT byte expert on the other three non-outer folds;
4. score the exact common parser-accepted target positions on that inner validation fold;
5. select `w` from `0.00..1.00` by pooled inner validation token log-likelihood, ties to smaller `w`;
6. refit B3 and each selected byte expert on all four non-outer folds and score the untouched outer fold once.

The B3 hyperparameters used for the inner mixture-weight surface are the already selected outer-B3 hyperparameters. No new state/recency hyperparameter layer is introduced for Issue #118.

## Byte token probability

For the selected `(k, alpha)`, the byte expert assigns a token probability equal to the product of the selected byte n-gram probabilities for every UTF-8 byte of the literal visible token plus the frozen `END_TOKEN` symbol.

- `RESET`: byte history clears before every visible token;
- `CONT`: byte history carries through every visible token on a physical leaf and clears only when physical leaf changes;
- rejected/non-scientific visible tokens still update CONT history, matching the frozen Phase-1 family;
- scientific likelihood is accumulated only at the exact parser-accepted B3 target positions.

## Mixture

For each accepted target token:

`p_mix = (1-w) * p_B3 + w * p_byte`.

Compute in log space. No renormalization or token-length correction is added.

## Frozen reported quantities

Per outer fold:

- B3 bits/token;
- RESET and CONT selected `(k, alpha, w)`;
- raw RESET and CONT byte bits/token on the accepted population;
- MIX_RESET and MIX_CONT bits/token;
- common accepted/visible support counts;
- `G_any = bits_B3 - bits_MIX_CONT`;
- `G_context = bits_MIX_RESET - bits_MIX_CONT`.

Primary aggregate:

- mean `G_context`;
- fold values;
- positive-fold count.

Frozen pass remains mean `G_context > 0` and positive in at least 4/5 outer folds.

## Frozen classification

Exactly one valid-science class:

- `NO ROBUST FLEXIBLE SEQUENCE RESIDUAL BEYOND CORRECTED CORE`
- `ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED`

or pre-scoring failure:

- `INVALID CORE / SUPPORT REGRESSION`.

No effect-size threshold may be added after reveal.

## Secondary diagnostics

Currier and line/paragraph localization are non-authoritative and may be appended after the primary reveal using the same frozen outer models. They may not alter this first-reveal classification or tune the model.

## Firewall

The first-reveal scorer must not call or inspect manuscript surface-target scorecards, extend byte/state/history grids, change segmentation, fit latent states, use image/semantic metadata, or identify plaintext/language/cipher/history.
