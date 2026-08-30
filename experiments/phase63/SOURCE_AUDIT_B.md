# Phase 63B0 — independent-transcription source audit

Status: **complete; source/design freeze only, no scientific replication metric computed**.

Exact machine-readable authority: `SOURCE_MANIFEST_B.json`.

## Frozen source identities

| source | lineage/alphabet | bytes | SHA-256 | Git-blob SHA-1 |
|---|---|---:|---|---|
| ZL3b | ZL / Eva- | 411,671 | `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc` | `2a4533ab9bdfa85db9bad602d590978953055df1` |
| **GC2a** | **Glen Claston / v101** | 314,916 | **`b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f`** | `8417a644fbd9c11cdaf85224f29cafee9ba1bdb0` |
| **IT2a** | **Takeshi Takahashi / EvaT** | 342,104 | **`7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`** | `4d6d3f2537b1f507a257529b49c94af7d6e03446` |

Headers captured by the frozen audit:

- ZL3b: `#=IVTFF Eva- 2.0 M 5`; `Version 3b of 13/05/2025`
- GC2a: `#=IVTFF v101 2.0 M 6`; original `voyn101.txt`; IVTFF 2a modified 25/06/2025
- IT2a: `#=IVTFF EvaT 2.0 M 3`; extracted from `LSI_ivtff_0d.txt`; IVTFF 2a modified 25/06/2025

Canonical live GC/IT URLs were fetched only for this audit. The SHA-256 values above are now the Phase63B input authority. A later live-file change must cause scientific execution to fail.

First successful source-only manifest artifact:

- workflow run `33316656246`
- artifact `9733651491`
- artifact ZIP SHA-256 `336aae4a89742cacb65247e6883dd6f48045f35aee74bb507631129ab55bef06`
- manifest JSON SHA-256 `527d4b6c8f0bba5cc866023b7c01c0cc648e3f8f1295d58e7a307e8cb86a8ed5`

A subsequent workflow re-fetch verified the exact GC/IT hashes and exact manifest digest before persisting `SOURCE_MANIFEST_B.json`.

## Coverage

All three sources contain P-coded prose on the same **99 physical leaves**.

The preregistered common-leaf rule therefore leaves the original Phase62 folds unchanged:

- fold0: 20 leaves
- fold1: 20
- fold2: 20
- fold3: 20
- fold4: 19

No fold rebalance or source-dependent leaf selection is required.

P-coded loci:

- ZL3b: 4,130
- GC2a: 4,130
- IT2a: 4,118

Locus overlap:

- ZL ↔ GC: **4,130 / 4,130**, Jaccard **1.000**
- ZL ↔ IT: 4,118 intersection, Jaccard **0.9971**
- GC ↔ IT: 4,118 intersection, Jaccard **0.9971**

Thus page/locus alignment is essentially complete and does not require fuzzy text matching.

## Paragraph segmentation independence

Source-native paragraph starts:

- ZL3b: **740**
- GC2a: **775**
- IT2a: **772**

Pairwise paragraph-start locus overlap:

| pair | intersection | union | Jaccard |
|---|---:|---:|---:|
| ZL ↔ GC | 730 | 785 | **0.9299** |
| ZL ↔ IT | 724 | 788 | **0.9188** |
| GC ↔ IT | 722 | 825 | **0.8752** |

This is methodologically useful. The transcriptions share a standardized locus/page framework, but paragraph segmentation is not identical. Phase63B will therefore use each source's own `<%>/<\$>` decisions exactly as frozen in `PLAN_B.md`, rather than transferring ZL paragraph boundaries.

## Representation differences are substantial

### ZL3b / Eva-

- definite `.` spaces: 27,730
- uncertain `,` spaces: 2,463
- drawing interruptions `<->`: 746
- uncertain-reading brackets: 656
- unreadable `?`: 223
- ligature braces: 394
- high-ASCII glyph occurrences: 127

### GC2a / v101

- definite `.` spaces: 30,330
- uncertain `,` spaces: 2,243
- drawing-interruption tags in P text: 0
- uncertain-reading brackets: 0
- unreadable `?`: 48
- ligature braces: 0
- high-ASCII glyph occurrences: 276

The raw v101 inventory includes upper/lower case, digits and punctuation such as `! # $ % & ( * + | \\`. These are retained as native glyph units under the frozen parser. They must not be stripped as ASCII punctuation.

### IT2a / EvaT

- definite `.` spaces: 29,594
- uncertain comma spaces: 0
- drawing interruptions `<->`: 779
- uncertain-reading brackets: 0
- unreadable `?`: 129
- ligature braces: 0
- high-ASCII occurrences: 0

These differences make Phase63B a meaningful segmentation/transcription challenge rather than a byte-level duplicate comparison.

## Consequence for replication design

The source audit supports the preregistered responsibility split:

- **GC2a/v101** remains the primary independent-alphabet observational replication for paragraph-entry specialization and H62-P1 recurrence geometry.
- **IT2a/EvaT** remains the secondary full frozen-A1-R1 transfer because its alphabet permits the existing literal EVA `k/t` entry feature without inventing a GC↔EVA mapping.

Do not force the full A1 model onto GC by constructing a v101 equivalent of EVA `k/t` after inspection.

## Source-only firewall confirmed

`SOURCE_MANIFEST_B.json` explicitly records:

`"scientific_metrics_computed": false`

No S1/S2/S3, edit-distance recurrence, H62-P1, entry-vs-pseudo projection, A1 generation, or scientific pass/fail outcome was computed while selecting/freezing these sources.

The next allowed action is to merge this source/design freeze, then implement GC-R1/R2 and IT-R1/R2/R3 on a new branch before computing their outcomes.