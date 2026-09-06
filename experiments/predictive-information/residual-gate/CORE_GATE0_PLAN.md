# Issue #118 — corrected B3 residual-core Gate 0

Date: 2026-09-06
Status: **FROZEN BEFORE RESIDUAL MIXTURE SCORING**
Parent: Issue #88

## Purpose

Before testing any flexible residual beyond B3, reproduce the exact corrected source-order Phase-1 authority from Issue #100 C1. This Gate computes no B3+byte mixture and no new residual statistic.

## Authority

Existing corrected Phase-1 authority:

- source: exact frozen ZL3b;
- source-order adapter: `experiments/predictive-information/source_order_authority.py`;
- scorer: `order-correction/rerun_phase1_source_order.py`;
- authoritative result JSON SHA-256: `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`;
- authoritative run: `34019919131`;
- authoritative artifact: `9985167291`.

Required mean bits/token:

- B0 `9.708906101685841`;
- B1 `9.594367012730386`;
- B2 `9.546169179582169`;
- B3 `9.517268842963203`.

Required B3 fold scores:

- fold0 `9.673387360496681`, n=4430, ENTRY_BODY lambda=.5;
- fold1 `9.58290664304585`, n=4810, LINE4 lambda=.5;
- fold2 `9.353632787765441`, n=5516, LINE4 lambda=.5;
- fold3 `9.38964928066337`, n=5447, ENTRY_BODY lambda=.5;
- fold4 `9.58676814284467`, n=4868, LINE4 lambda=.5.

The Gate must also reproduce corrected byte-family selection/support because Issue #118 reuses that family:

- continuous selected k=2, alpha=.01 in all five outer folds;
- reset selected k=3, alpha=.01 in folds 0/1 and k=2, alpha=.01 in folds 2/3/4;
- accepted byte-scored n equals B3 n in every fold;
- visible byte-scored support equals the original visible target count.

## Gate rule

PASS only if the existing corrected Phase-1 script regenerates the authoritative JSON byte-for-byte / SHA-for-SHA and all explicit B3/byte assertions above hold.

Any mismatch is `INVALID CORE / SUPPORT REGRESSION` and blocks Issue #118 first reveal.

## Firewall

This Gate does not:

- compute `p_mix(w)`;
- select mixture weights;
- calculate `G_any` or `G_context`;
- alter corrected B3 or byte grids;
- score S1/S2/H62/R1 or Issue #84 targets;
- fit latent states.

After PASS, merge this Gate before committing the residual mixture scorer.
