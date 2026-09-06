# Issue #115 Phase 4B — IT2a Gate 0 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE GATE — PASS**

## Scientific head and artifact

- PR: #116
- scientific head: `5c9e1c1378a4752225be16c6a39d6fecbd07a1de`
- workflow run: `34024794242`
- workflow conclusion: `success`
- artifact ID: `9986699929`
- artifact digest: `sha256:facadee6f5695a2df63f2bd8539694d96bbffecd147fdefb5eaaf91b45babea5`
- `phase4b_it2a_gate0.json` SHA-256: `5698469677afd40b30ee26c9c1421b584a07106dd909c4a912d375f393c9bbfe`

## Exact IT2a authority

The live canonical retrieval reproduced the pre-existing #58D/#66 authority exactly:

- SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- 342,104 bytes
- 5,444 lines
- `#=IVTFF EvaT 2.0 M 3`
- `# Extracted from LSI_ivtff_0d.txt`
- `# Version 2a of 02/02/2023 modified 25/06/2025`.

No source drift occurred.

## Frozen fold authority

Phase-4A fold identity reproduced exactly:

`cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`

All 4,118 IT2a P-loci are on the 99 frozen physical leaves.

## Score-free support

Eligible events:

- clean certain-space tokens: `32,956`
- REAL_SPACE: `27,436`
- MID_TOKEN: `24,239`
- P2 REAL_SPACE: `23,379`

By frozen fold:

| Fold | clean | REAL | MID | P2 |
|---:|---:|---:|---:|---:|
| 0 | 5,788 | 4,757 | 4,184 | 4,063 |
| 1 | 6,400 | 5,342 | 4,807 | 4,603 |
| 2 | 7,212 | 6,000 | 5,201 | 5,147 |
| 3 | 7,128 | 5,917 | 5,240 | 5,037 |
| 4 | 6,428 | 5,420 | 4,807 | 4,529 |

All three prospective support predicates pass 5/5.

Event identity hashes:

- REAL_SPACE `465c93d24b7b96e5d48d7e31d524f700beff849c9fae49a302a7f4ba0d62f675`
- MID_TOKEN `c8c75745d4878f9695868e3797cd23c82ed6eb1aa047dd49194482778c53ad75`
- P2 REAL_SPACE `5a74abbbedc46b7dca38e5afbec5707e72a1c67f9becbb4843e7be0ee52c7505`.

## Currier diagnostic support

- A: REAL 7,670 / MID 6,564 / P2 6,280
- B: REAL 19,375 / MID 17,320 / P2 16,770
- unknown/other: REAL 391 / MID 355 / P2 329.

Currier does not affect primary eligibility.

## Firewall

The authoritative Gate JSON records:

- predictive scores computed: false
- boundary model fitted: false
- SlotParser used for event eligibility: false
- ZL3b Phase-4 target scores read: false
- semantic/image context used: false
- latent state fitted: false.

Frozen disposition:

> **PASS — PROCEED TO IT2a P1/P2 FIRST REVEAL**

Refs #66, #88, #112, #115, #116.
