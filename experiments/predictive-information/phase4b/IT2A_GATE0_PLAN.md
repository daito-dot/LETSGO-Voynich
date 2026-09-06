# Issue #115 Phase 4B — IT2a independent-transcription Gate 0

Date: 2026-09-06
Status: **FROZEN BEFORE ANY IT2a P1/P2 SCORE**
Parent: Issue #88
Reference: Phase 4A PRs #113–#114

## Purpose

Replicate the Phase-4A visible-space production-boundary test in the independent Takeshi Takahashi / IT2a reading without retuning the representation, model or pass rules after the ZL3b result.

This Gate 0 audits only source identity, raw-event construction and five-fold support. It must not fit the boundary model or compute P1/P2.

## IT2a source authority

Use the exact source already frozen and independently audited in Issue #58D / #66:

- URL: `https://www.voynich.nu/data/IT2a-n.txt`
- alphabet/lineage: `EvaT` / Takeshi Takahashi
- header: `#=IVTFF EvaT 2.0 M 3`
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git-blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- bytes: `342104`
- lines: `5444`.

Any byte drift invalidates this Gate until separately explained. Do not silently adopt a newer source.

## Frozen representation

Reuse the merged Phase-4A raw-EVA logic exactly:

- REAL_SPACE: literal IVTFF `.` certain word space only;
- `,`, `<->`, `<~>` are not primary REAL_SPACE boundaries;
- connected composites longest-match: `cfh`, `ckh`, `cph`, `cth`, `ch`, `sh`;
- all remaining lowercase Basic-EVA letters are one atom;
- uncertain/alternative/high-ASCII/explicit-ligature/inline/uppercase-connectivity/tick/other exceptional content makes the whole affected certain-space token unclean;
- only `<%>` and `<$>` may be stripped at documented structural edges;
- MID_TOKEN: `floor(n_atoms/2)`, >=2 atoms on each side;
- P2 support: REAL_SPACE with >=3 atoms on each observed side.

No IT2a-specific remapping is licensed.

## Fold authority

Reproduce the same original five physical-leaf folds from the exact ZL3b authority used in Phase 4A. ZL3b is used only to recover/check fold membership; no Phase-4A target score is read by the Gate.

Required fold identity SHA-256:

`cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`

## Required Gate outputs

Archive:

- exact IT2a source identity;
- fold identity/hash;
- REAL_SPACE/MID_TOKEN/P2 event counts by fold;
- event identity hashes;
- clean atom inventory;
- MID source-token length distribution;
- exclusion counts;
- Currier A/B support as a diagnostic only;
- score-free firewall.

## Gate rule

Proceed to IT2a first reveal only if:

1. exact source authority matches;
2. fold identity matches Phase 4A;
3. REAL_SPACE is nonzero in all five folds;
4. MID_TOKEN is nonzero in all five folds;
5. P2 REAL_SPACE is nonzero in all five folds;
6. no predictive score/model fit occurs in Gate 0.

No fold regrouping or boundary-rule repair may be chosen after seeing scores.

## Firewall

Gate 0 must not calculate:

- RESET/CARRY likelihoods;
- P1 reset advantage or D_RESET;
- P2 observed/shift code lengths;
- any ZL3b/IT2a effect agreement statistic;
- token-level R1/LOCAL/PREV/S1/S2/H62 targets;
- semantic/cipher/latent-state outputs.

After a PASS, merge this Gate before committing the IT2a scientific scorer.

Refs #66, #88, #112, #115.
