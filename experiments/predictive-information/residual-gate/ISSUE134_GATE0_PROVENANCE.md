# Issue #134 Gate0 provenance

Date: 2026-09-06

This records the first successful score-free Gate0 run for the augmented observable-core residual closure. No new Issue #134 predictive probability, likelihood, bits/token or residual was computed in this Gate.

## Frozen revision

- PR: #136
- Gate head: `621112519f697758086dcbbc8714cc4dcdef1cca`
- Base main at branch creation: `3e9d3c5df30c80ff0c80e765952b71ebf03baf54`
- Frozen design: `ISSUE134_AUGMENTED_CORE_PLAN.md`
- Gate executable: `issue134_augmented_core_gate0.py`
- Workflow: `.github/workflows/issue134-augmented-core-gate0.yml`

## First successful Gate run

- workflow run: `34034719113`
- artifact: `9989826572`
- artifact digest: `sha256:b1e3fd9b3c377d3e98897278abfa4874accbc3136505cd58ab12e3ac83a65875`
- result JSON SHA-256: `3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1`
- Gate result: **PASS — PROCEED TO COMMITTED PREDICTIVE SCORER**

## Reproduced authorities

- corrected B3 normalized authority SHA-256: `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`
- Issue #127 Currier edge Gate0 JSON SHA-256: `31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`
- ZL3b git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- outer parser-accepted target counts: `4430, 4810, 5516, 5447, 4868`
- outer splits: `5/5` pass
- outer+inner splits: `20/20` pass

## Outer training support

| outer fold | A edge events | B edge events | other edge events | A prev-terminal contexts | B prev-terminal contexts | pooled contexts |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 6,845 | 16,270 | 295 | 20 | 21 | 21 |
| 1 | 6,774 | 15,739 | 404 | 21 | 21 | 22 |
| 2 | 6,936 | 14,990 | 319 | 21 | 21 | 22 |
| 3 | 7,491 | 14,340 | 435 | 20 | 20 | 22 |
| 4 | 7,822 | 14,857 | 287 | 21 | 20 | 22 |

The prospectively frozen pooled fallback is exercised structurally: A/B native context support is not identical to pooled support in several folds. This is a support fact only; no current-initial outcome distribution was revealed by Gate0.

## Firewall

The artifact records all of the following as false:

- new Issue #134 edge probabilities computed;
- new challenger probabilities computed;
- new likelihoods computed;
- new bits/token computed;
- new residual computed;
- outer outcomes used for selection;
- current-initial outcomes exposed;
- latent state fit;
- hand conditioning used;
- surface scorecard used;
- semantic/image context used.

The predictive scorer may now be committed under the already-frozen contract. Any change to Currier policy, smoothing, fallback, candidate grids, tie rules, challenger topology or residual pass rule after this point requires a named correction and a new preregistration before another first reveal.
