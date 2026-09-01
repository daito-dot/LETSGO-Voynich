# Issue #75 Phase E0 authority freeze

Date: 2026-09-01  
Status: **VALID TARGET-BLIND E0 AUTHORITY FROZEN**

## Authority

- family: `M5-KRS-2MIX-CHAIN`
- final normative plan commit: `b2ef72d19111445f164d68ded813f1f81e297af6`
- generator commit: `e6eb4fd32a7428a152b6370562f29eb453e4f049`
- implementation freeze commit: `e277f964ceb2cf45959231c471c4d01bd3267b58`
- E0 launch scientific head: `3e1eb27b18cdc087808658763745ca185580d65d`
- workflow run: `33512983928` — success
- artifact ID: `9802492761`
- artifact digest: `sha256:a842abfddca586d47838f4975055b8aaad19a3e9e3b49dbc8066a6bff00c9c3d`
- E0 authority SHA-256: `4c406e60872f8fcfd27901cc41901db04c1aa192fa9ee91a14c01ea3dbe46a89`
- permanent repository commit: `e89023ba6508822f77b49d2bc46a02e35b7a0f15`
- permanent directory: `experiments/minimal-occupancy-generator/stage-e0/`

## Frozen population

- 31/31 reps `0..30`
- 25,071 tokens per corpus
- five frozen fold populations `4430 / 4810 / 5516 / 5447 / 4868`
- 31 distinct occupancy SHA-256 values
- generated distinct-signature range `859..904`
- no drops
- no rerolls
- all target-access fields false

Replay anchors:

- rep 0 occupancy SHA `1a651c319a4dbc52c357fbae9671a1d3ea421f5ff67c8e6a5544c6b42250f21c`
- rep 30 occupancy SHA `4eda55f6b9582784264e5c48f4f3c85b198b0ac6cfe81287d0c34473f1020959`

## Training-only latent fit

Selected deterministic start indices by held-out fold:

`2 / 3 / 2 / 2 / 3`

Canonicalized global `pi=P(Z=1)` by held-out fold:

- fold 0: `0.50513648776233`
- fold 1: `0.5007281446534325`
- fold 2: `0.4847643353490622`
- fold 3: `0.4893164350476849`
- fold 4: `0.488997472100751`

Thus the selected training-only solutions use both hidden modes at roughly equal frequency in every cross-fit split; the result is not a tiny-component artifact.

Exact training conditional log-likelihood gain over the nested M3 baseline:

- fold 0: `+8764.613790765754`
- fold 1: `+8526.688295586206`
- fold 2: `+8118.005517077578`
- fold 3: `+8258.540196385937`
- fold 4: `+8502.170395480589`

Per training token this is approximately `+0.415 .. +0.425` natural-log units across all five splits.

This is training-only evidence that the occupancy inventory has a strong reproducible two-regime structure not captured by a single M3 local chain.

## Component stability diagnostic

The canonicalized components reproduce a qualitatively stable separation across folds. Typical training-`q_d` expected occupancies are:

- component 0: very high slot 8 (`~0.92`) and slot 10 (`~0.88`), relatively low slot 6/7/11;
- component 1: low slot 8 (`~0.18`) and slot 10 (`~0.13`), much higher slot 6 (`~0.54-0.55`), slot 7 (`~0.36`), and slot 11 (`~0.66-0.67`).

These labels are statistical only. No meaning, glyph class, manuscript section, language, or plaintext interpretation is assigned.

## Numerical audits

- analytic-gradient finite-difference audit performed before fitting on fold 0;
- max absolute discrepancy `7.885391141826403e-06`;
- max scaled discrepancy `7.885391141826403e-06`;
- frozen tolerance `1e-5`;
- audit passed;
- maximum descriptor-wise mixture normalization error across folds is below `1.8e-15`;
- selected M5 likelihood exceeds the nested M3 baseline in every fold.

Some selected L-BFGS-B solutions have non-negligible final gradient norms despite optimizer convergence; this does not invalidate E0 because the preregistration explicitly accepts optimizer-reported convergence or gradient infinity norm `<=1e-6`, and start selection was frozen before target access. The exact generated population is now the authority and will be replayed by frozen parameters rather than refitting during target scoring.

## Firewall statement

E0 computed no candidate pair-Q, no residual Z, no ZL3b/IT2a target topology, no target correlation, no sign agreement, and no T.

Next authorized actions only:

1. exact E0 replay preflight on reps `0` and `30` from frozen E0 parameters;
2. target-blocked rep-0 candidate-owned-null smoke;
3. scorer/aggregator and PRETARGET execution freeze;
4. exactly one complete 31-case first reveal.