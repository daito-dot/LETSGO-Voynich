# Phase 63B parser preflight

Status: **complete before scientific replication implementation**.

No edit-distance graph, feature vector, S1/S2/S3, H62-P1 or A1 output was computed in this preflight.

## Provenance

Successful B1 parser preflight:

- workflow run `33317368945`
- job `99273208974`
- artifact `9734023192`
- artifact ZIP SHA-256 `92f08c5a63866548237947fd5906734d35487c9305e4e2d732bb3f60c8a4df98`
- preflight JSON SHA-256 `24c0192332454751b1e3d85fb2d25ba8fba62f0aac3da7249f30e14a99dd08fb`

The earlier strict parser attempt failed before science on ZL Eva- apostrophe/zero syntax. `PARSER_AMENDMENT_B1.md` records that pre-result syntax correction. IT and GC token rules were not broadened.

## Population summary

| source/view | paragraphs | usable lines | usable tokens | token types | base eligible | S1 eligible | leaves | excluded uncertain/unreadable |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ZL W1 | 740 | 4,084 | 37,890 | 8,201 | 555 | 453 | 99 | 830 |
| ZL W2 | 740 | 4,084 | 37,890 | 8,211 | 562 | 458 | 99 | 830 |
| GC W1 | 775 | 4,044 | 38,517 | 8,940 | 633 | 512 | 99 | 48 |
| GC W2 | 775 | 4,044 | 38,517 | 8,918 | 632 | 513 | 99 | 48 |
| IT W1 | 772 | 4,095 | 37,995 | 8,379 | 575 | 470 | 99 | 129 |
| IT W2 | 772 | 4,095 | 37,995 | 8,379 | 575 | 470 | 99 | 129 |

Paragraph starts consumed exactly match the source-audit start counts:

- ZL 740
- GC 775
- IT 772

All views retain all 99 physical leaves.

IT W1/W2 are identical because the frozen IT source contains no uncertain comma spaces. GC and ZL show modest W1/W2 population/type differences, as intended by the preregistered sensitivity.

## Lines outside explicit paragraph state

Nonempty P-lines outside a source-native paragraph state:

- ZL: 27
- GC: 13
- IT: 18

The frozen parser ignores rather than guessing paragraph membership for these lines.

## Consequence

The independent sources provide ample eligible population in every transcription and no fold/source exclusion is required. Scientific implementation may now proceed under the already-frozen GC-R1/R2 and IT-R1/R2/R3 criteria.

Population differences are retained as part of the transcription challenge; they will not be normalized away after seeing replication results.