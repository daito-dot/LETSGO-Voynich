# Issue #172 — Stage 0 Gate provenance

Date: 2026-09-07
Status: **STAGE0 AUTHORITY READY — SCORE FREE**

This file archives the accepted authority/preflight checkpoint for Issue #172. No Issue #172 candidate R1–R8 scientific target score was computed in Stage 0.

## Frozen design chronology

- post-#88 base main: `a1001cefaab1d3f7f1ef808af3f4614fe8bf7f3b`
- authority-plan commit: `ece76bfe57203a0ed630774984c52f35bfbc2d17`
- authority-plan blob: `638e212e22aaa313fd85ab80103528ce4cfada9f`
- manifest commit: `32407505b97227e8f2a7da7d99b081a94c84ffb5`
- manifest blob: `ce72238107e95f3ed88152a943041d3a827ae945`
- manifest raw SHA-256: `fe15d9c388caa1daddb5a2b1ea46ebd6830647a64ff0902bad40f40b22b46792`
- initial checker commit: `e114aba0f7cac32b247a24399af5f388912e44d0`
- workflow commit: `c77b68beda991b56fddb9c4803883eb28386ee62`
- workflow blob: `e072e46cbbf269ba9698a7b94a1bfb5dc961a706`
- accepted checker/provenance-fix commit: `3faac14564be196fccdded50e894317030f40be2`
- accepted checker blob: `396b0ae7245015bc199f52a139cee20713afb54a`
- Stage0 PR: #173
- Stage0 merge: `6c7f872646e2b906ec83e55831bf70cca060462d`

## Superseded first Gate run

The first exact-checkout Gate execution succeeded scientifically/contractually but its JSON provenance field `git_head` used GitHub Actions `GITHUB_SHA`. On `pull_request` workflows that variable names the synthetic merge ref rather than the exact checked-out PR head.

- run: `34092121959`
- PR head actually checked out: `c77b68beda991b56fddb9c4803883eb28386ee62`
- artifact: `10007196980`
- artifact ZIP SHA-256: `e312e7255ecf31c0c73fdb9d931e0cb38894649e7fb36630a4939cba1673495a`
- result JSON SHA-256: `666ee0f5a67fc9a0b1ef850f0342acae465182a3c43417516da703fed60ddad7`
- checks: `27/27 PASS`
- JSON-recorded head: synthetic merge SHA `67c51f47225149d906fcaaf5963f785720646419`

Disposition: **superseded for provenance only**. No scientific target was involved and no hard gate, candidate roster, authority, threshold, representation, or access rule was changed. The checker was changed only to record `git rev-parse HEAD` from the checked-out tree.

## Authoritative Stage 0 Gate

- exact PR head / checked-out head: `3faac14564be196fccdded50e894317030f40be2`
- run: `34092274963`
- conclusion: `success`
- artifact: `10007249057`
- artifact name: `issue172-stage0-authority-3faac14564be196fccdded50e894317030f40be2`
- artifact ZIP SHA-256: `f0bad01a0680ef8ebf841f995b6f9388eccf6a9a93a4e999e1ecf61e6748ae52`
- result JSON SHA-256: `76080227ad683d620a4888da05f8aef9a1dba0453125e740279dcbdcf9c28a10`
- manifest blob reported by result: `ce72238107e95f3ed88152a943041d3a827ae945`
- manifest SHA-256 reported by result: `fe15d9c388caa1daddb5a2b1ea46ebd6830647a64ff0902bad40f40b22b46792`
- plan blob reported by result: `638e212e22aaa313fd85ab80103528ce4cfada9f`
- checks: `27/27 PASS`
- `score_free=true`
- `candidate_target_scoring_performed=false`
- classification: **`STAGE0 AUTHORITY READY`**

The downloaded artifact ZIP digest was independently recomputed and exactly matched GitHub artifact metadata. The result JSON SHA-256 above was independently recomputed from the downloaded artifact.

## Frozen consequence

Stage 0 is accepted. The next licensed operation is a **fresh post-merge target-plan branch**. The target plan must be committed before any Issue #172 scorer. The scorer must then be committed alone and its blob frozen before any target workflow is added.

No repair of A1/A1-R1 or Naibbe C1-E0 is licensed inside the historical-anchor calibration tournament. Any new mechanism family is a separate preregistered hypothesis after the calibration result is frozen.

## Interpretation boundary

This checkpoint licenses mechanism discrimination only. It does not license plaintext, semantics, natural-language wordhood, language/cipher family, authorship, historical mechanism/direction, artificiality/hoax, or decipherment claims.
