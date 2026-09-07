# Issue #191 Stage 0 provenance

Date: 2026-09-08  
Issue: #191  
Parent: #172  
PR: #192

## Result

**STAGE 1 LICENSED.**

This Stage 0 execution computed no new manuscript productivity statistic. The executable emitted the frozen firewall marker:

`NO ISSUE191 NEW PRODUCTIVITY SCIENTIFIC RESULT COMPUTED`

with:

- `scientific_score_computed = false`
- `new_productivity_score_computed = false`
- `manuscript_transcription_opened = false`
- `stage1_licensed = true`

All frozen Git-blob checks, static lineage checks, historical replay checks, synthetic helper tests, and read-firewall checks passed.

## GitHub Actions authority

- workflow: `issue191-productivity-stage0`
- run ID: `34169112886`
- job ID: `101885881174`
- tested head commit: `649c2a71d42cdeba0d5a9a30452c068bba68b46d`
- conclusion: `success`
- artifact name: `issue191-productivity-stage0`
- artifact ID: `10035116801`
- artifact ZIP SHA-256: `03a94305dc723c588294c919be5da3bd8c1374ed12426cdd870f2e5b2f384d0a`
- raw `issue191_stage0_authority.json` SHA-256 after artifact extraction: `5230ce023cd52d2e4fc70d1c8b61b9a5b35e2e43a0f5f306875b62ce1afb1bb0`

## Exact authorities confirmed

The run confirmed all ten Git blob identities frozen in `research/ISSUE191_PRODUCTIVITY_STAGE0_PLAN_20260908.md`, including the current OGH-A/B/C code, OGH-C report/C0 result, the frozen 12-slot parser, Phase58D common-representation lineage, and the three OGH preflight/admissibility authorities.

Static checks additionally confirmed:

- 12 slots and 33 `(slot,value)` units;
- `SlotParser.parses` / `SlotParser.pick` / parser validation lineage;
- OGH-A 5-fold / 12-slot / IT2a loader lineage;
- OGH-B G7A second-order implementation and frozen backoff;
- OGH-C V2/V+ implementation and the frozen `V2 if positive >= 4 else V1` selection rule;
- Phase58D ZL3b/IT2a source blobs, five folds, and exact 99-leaf universe check;
- admissible population `4077 / 4095` non-empty slot masks.

## Allowed historical replay confirmed

These values were already revealed before Issue #191 and were replayed only as lineage checks:

- OGH-C schema: `ogh-c-c0-v1`
- selected content grammar: `V2`
- V2 positive held-out gain: `5/5` folds
- held-out parsed support: `[4430, 4810, 5516, 5447, 4868]`
- parsed total: `25071`
- historical V+ mean OOV fraction: `0.07034275261192205`
- historical V+ fold OOV fractions: `[0.07652370203160275, 0.07567567567567568, 0.06617113850616385, 0.06370479162841935, 0.06963845521774858]`
- G7A mean shape cost: `7.009998907083391` bits/token
- V2 mean cost: `9.708971376158532` bits/token

No IT2a OOV, new structural decomposition, rarefaction curve, C2 p-value, C3 V2 productivity result, or Issue #191 outcome label was calculated in Stage 0.

## Prospective helper freeze confirmed

Synthetic self-tests passed for:

- exact without-replacement rarefaction expectation;
- character-level Levenshtein-distance-one classification;
- non-exclusive novelty annotations;
- deterministic C2 fold reassignment;
- deterministic seed namespaces;
- linear empirical quantiles.

Stage 1 is therefore licensed under the exact Issue #191 outcome rules. No threshold, parser, fold, null, annotation, or V2 backoff change is licensed after the first Stage-1 reveal.