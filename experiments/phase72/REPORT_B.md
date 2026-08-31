# Phase 72B — open historical benchmark source audit

Status: **SOURCE AUDIT CLOSED — MECHANICAL READY, SCIENCE NOT READY**

Date: 2026-08-31

No Voynich S1/S2/S3/H62 score was computed in Phase72B.

## Result of the corrected source audit

After the pre-science path-base correction, the pinned `cipher_benchmark` checkout contains **102** records passing the frozen broad source filter:

- Copiale: **101** page transcriptions;
- Gold Bug: **1** literary cryptogram.

All 102 pass the simple line/token **shape** check. Under the literal counting rule frozen in `FEASIBILITY_B.md`, this produces the mechanical label:

> `P72-BENCH READY`

That mechanical label is retained as the output of the frozen audit. It is **not sufficient to authorize a scientific real-cipher entry test**.

## Why the mechanical READY label does not establish entry feasibility

The source audit revealed two semantic problems in its own source-group proxy.

### 1. Copiale `source_record_id` is page-specific

The 101 Copiale records have identifiers such as:

- `copiale_manuscript_page_1`
- `copiale_manuscript_page_10`
- `copiale_manuscript_page_101`

Each page therefore forms a separate manifest `source_record_id` under the frozen Phase72B grouping code. This made every page look like a first source-record entry.

But these are pages of the **same Copiale manuscript**, not 101 independently established messages. A physical page boundary is not an externally established message/paragraph-entry boundary for the S1 question.

Using those 101 page starts as if they were 101 source-native message entries would silently change the scientific object after seeing the metadata. It is not allowed.

### 2. Gold Bug is not real historical cipher practice

The second source satisfying the purely mechanical two-source gate is Poe's 1843 *The Gold-Bug* cryptogram. Its benchmark provenance explicitly identifies it as a literary constructed cryptogram with a known fictional solution.

It is useful as a cipher benchmark but not as an independent sample of historical diplomatic/administrative cipher practice. Therefore it cannot supply the second historical-practice source required by the motivation of Phase72.

## Additional useful source finding

The same pinned benchmark contains substantial Borg diplomatic/cipher manuscript material, including diplomatic and canonical transcription files. However those records are not admitted by the Phase72B `rights_class == open` filter and, more importantly, are also page-level manuscript records rather than an already established set of independent message-entry boundaries.

This is useful source material but does not repair the Phase72B scientific-entry problem.

## Accepted Phase72B conclusion

> **The public benchmark is rich enough for page-level real-cipher controls, but the frozen open-source subset does not yet provide two independent historical-practice collections with externally established message/paragraph entry boundaries.**

Therefore:

- retain the literal source-audit output `P72-BENCH READY` as a mechanical availability label;
- classify the intended scientific frontier as **`P72 REAL-CIPHER ENTRY BOUNDARY BLOCKED`**;
- do not compute Voynich S1 on the Copiale page starts as a substitute for message entries;
- do not promote Gold Bug as historical practice;
- do not relax the two-independent-source requirement.

## Next route

The next source audit should target one of two genuinely orthogonal objects:

1. a corpus of **real enciphered letters/messages** with machine-readable ciphertext transcriptions and document-level boundaries (the Mary Stuart/Castelnau corpus is an especially strong target if the transcriptions can be obtained from a public authority); or
2. a separately frozen **page-entry** control using real historical ciphertext pages, explicitly changing the question from paragraph/message entry to physical page entry rather than pretending the boundaries are equivalent.

The preferred route is (1). No Voynich score is authorized until the exact external message population and boundary semantics are fixed.

## Provenance

Corrected source audit:

- Actions run: `33390668166`
- job: `99483301898`
- branch head used by run: `980665b093f5ea925454b10b6d9078b79b4a4c93`
- artifact: `phase72b-benchmark-source-audit`, ID `9757309480`
- artifact ZIP SHA-256: `4dc29a25a1c775971084797875a895682dbca0788b7b7cf8543371d8798f12d6`

No Phase72 Voynich scientific statistic has been revealed.
