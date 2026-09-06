# Issue #139 — IT2a edge replication Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

This document archives the first successful score-free Gate0 for Issue #139. It does not alter the preregistered representation, support rule, smoothing, model family, pass rule, or interpretation boundary.

## Scientific chronology

1. Score-free replication plan committed first at `03300905169e5e3d8644be2c2d5c1740542021f4`.
2. Repository code authorities were frozen at `bd015c0a1fff844a6be34dddedd071dfaa8436a2`.
3. Gate0 executable was committed at `cdca968b5cc7142a2b79742f7956bd24af3e56e7`.
4. Gate workflow head was `d07a3c844c304a8b4490f4f8ae13c6d76dc59093`.
5. The first PR-triggered Gate run completed successfully before any Issue #139 POS2/EDGE2 scorer existed.

No Issue #139 POS2/EDGE2 probability, log likelihood, bits/token, `G_identity_IT2a`, or scientific classification had been computed at this point.

## First successful Gate authority

- PR: #143
- workflow: `Issue139 IT2a edge Gate0`
- run: `34061441684`
- workflow head: `d07a3c844c304a8b4490f4f8ae13c6d76dc59093`
- run conclusion: `success`
- artifact ID: `9997590970`
- artifact name: `issue139-it2a-edge-gate0-d07a3c844c304a8b4490f4f8ae13c6d76dc59093`
- artifact ZIP digest: `sha256:10652e7bf44d648d4d8f8419b124b6ec4704048b7e618a8fbbd6e1217ab39695`
- result JSON: `issue139_it2a_edge_gate0.json`
- result JSON SHA-256: `b97fe44633b088a97e86d5e08a74e9688647b8bb5eeeb7a44a43c98887b80fea`

Gate disposition:

> `PASS — PROCEED TO SEPARATELY COMMITTED FROZEN IT2A EDGE SCORER`

## Reproduced source and parser authorities

- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- IT2a Git blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- Phase63B W1 parser blob: `99cc6d49669c67432b4798b81c8250a17b3fbb38`
- SlotParser blob: `8bafba7f2bce4cf77c9001c729936c1ce619759b`
- Issue #66 source-audit JSON blob: `85c172c113927b91215463ee9297630580b57769`
- Issue #66 source-audit JSON SHA-256: `bed86e92fcb854b614dfb474cd3bab9e6fc1e5746399fc14bced9f8e4448eddf`

## Reproduced population

- P-coded loci: `4,118`
- paragraphs: `772`
- pages: `206`
- physical leaves: `99`
- nonempty retained source lines: `4,117`
- uncertain/unreadable tokens excluded: `80`
- clean W1 visible tokens: `34,411`
- primary SlotParser-accepted targets: `28,280`
- rejected current tokens: `6,131`
- accepted tokens with >1 legal parse: `9,492`
- tokens where min/max parse differ: `9,492`

Frozen fold clean counts reproduced exactly:

`[6102, 6692, 7528, 7484, 6605]`

Frozen fold primary-target counts reproduced exactly:

`[4976, 5416, 6261, 6197, 5430]`

Accepted line-body target counts, revealed only as score-free support:

`[4393, 4824, 5545, 5517, 4832]`

Every fold therefore exceeds the preregistered minimum of 300 primary line-body targets without repair.

## Training-complement support

For outer folds 0..4 respectively:

- training clean tokens: `[28309, 27719, 26883, 26927, 27806]`
- training line-start tokens: `[3352, 3331, 3218, 3251, 3316]`
- training line-body tokens: `[24957, 24388, 23665, 23676, 24490]`
- unique previous-terminal byte contexts: `[19, 19, 19, 19, 19]`
- unique previous-terminal→initial byte pairs: `[202, 199, 202, 197, 197]`
- train/test physical-leaf overlap: zero in all five outer folds.

No support repair, fold regrouping, glyph normalization, smoothing change, fallback addition, or model-family expansion is required.

## Frozen firewall status

The archived JSON records:

- `scientific_edge_metrics_computed = false`;
- no POS2 probability;
- no EDGE2 probability;
- no log likelihood;
- no bits/token;
- no `G_identity_IT2a`;
- no scientific classification;
- no Currier/hand/section-conditioned fit;
- no latent-state fit;
- no S1/S2/H62/R1 tuning.

The next scientific step is allowed only after this Gate authority is merged: commit the frozen IT2a POS2/EDGE2 scorer separately, then run its first target reveal once at that scientific head.

Refs #66 #88 #123 #125 #134 #139 #143.
