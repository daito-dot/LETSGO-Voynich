# Data setup

The current analysis program uses an EVA/ZL3b transcription as its main working transcription.

## Current expected local file

Historical scripts may refer to variants of the filename. The exact working source currently verified by the project has:

- size: 411,671 bytes
- Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`

The transcription itself is third-party source material and is not automatically redistributed in this repository. Obtain it from an authorized/public source and verify provenance and licensing before redistribution.

When reproducing historical scripts, place the transcription locally and adjust the input path if necessary. New scripts should accept an explicit input path rather than depend on a private filename.

## Licensing boundary

The repository licenses in `LICENSE`, `LICENSE-CODE`, and `LICENSE-CONTENT` apply only to material for which this project has the right to grant those licenses. They do **not** relicense third-party transcriptions, manuscript images, external corpora, quoted material, or other third-party source content.

A checksum, filename, citation, derived statistic, preprocessing recipe, or script that operates on third-party material does not grant permission to redistribute that source material. Always follow the original provider's license, copyright terms, database rights, and terms of use.

## Why provenance matters

A transcription is an analytical representation of the manuscript, not ground truth. Results can depend on glyph segmentation, EVA conventions, uncertain readings, spaces, line boundaries, and editorial normalization. Claims that survive an independent transcription are therefore stronger than claims demonstrated on one transcription lineage only.

## External control corpora

Do not commit third-party corpora unless redistribution is permitted. For every external corpus record:

- source/project
- exact document(s)
- retrieval/version/commit when available
- license
- preprocessing/normalization
- structural units preserved (line, paragraph, folio/page, etc.)

Current research includes medieval Latin manuscript controls from the CREMMA Medii Aevi / CREMMA-Medieval-LAT project, plus exploratory historical-language and formal-language controls. See phase reports for exact scope and limitations.
