# Issue #196 — complete-preservation corpus screening outcome

Date: 2026-09-08  
Parent: #172

## Decision

**Selected for one new prospective, score-free R5 Gate 0:**

`Richard Bean / Megan Piorko / Sarah Lang — Hermeticae Philosophiae medulla, British Library Sloane MS 1902, fol. 13`.

Screening class: **`ADMIT_FOR_PROSPECTIVE_R5_GATE0`**.

This is a source-preservation admission only. No R5 score has been computed on the Dee ciphertext.

## Why this source outranks the stopped candidates

The external scholarly authorities independently provide positive evidence for all five preservation layers required by the frozen #196 screen.

### 1. `CIPHERTEXT_SYMBOLS`

The HistoCrypt 2022 paper publishes a full alphabetic ciphertext transcription and documents the encryption table/key mechanism. Richard Bean's public `ArthurDee` repository identifies itself as the C code used to decipher the manuscript for that paper.

Pinned current public repository authority at screening time:

- repository: `RichardBean/ArthurDee`
- commit: `6bc46f0947b2a4e7f2dee9006899931361165a76`
- tree: `6ed19dcbcf77eaa463979064fa06334867d9e196`
- README git blob: `df626fe94cfbc7929eacb061a4e002fc2ea8e625`

The repository includes the solving notes, C code, `dee-text.zip`, and `c-source.zip`. Binary archive contents are deliberately deferred to the new Gate 0 rather than inspected during candidate selection.

### 2. `PHYSICAL_LINES`

Piorko, Lang, and Bean's Ambix article explicitly introduces the published ciphertext as a **literal transcription of the encrypted text as it was copied onto fol. 13 and bound in Sloane MS 1902 by Arthur Dee**. The ciphertext is printed with manuscript line breaks rather than reflowed into one continuous string.

The HistoCrypt paper additionally identifies the longest encrypted word as hyphenated across the sixth and seventh lines of the first page. This is direct evidence that the source-line layer and a line-crossing lexical unit can be distinguished in the scholarly representation.

### 3. `CIPHER_UNIT_BOUNDARIES`

The HistoCrypt paper treats the manuscript's spaced groups explicitly as **ciphertext words**. Its decipherment procedure forms a list of ciphertext words, sorted by word length, and searches for corresponding Latin words. The public repository README reproduces the critical pipeline:

`cat dee2 | tr ' ' '\n' ...`

and states that this produces a list of ciphertext words.

Thus ordinary source spacing has an independently documented unit role coarser than cipher atoms; it is not being invented from Voynich or from an R5 outcome.

### 4. `PLAINTEXT_LEXICAL_BOUNDARIES`

The HistoCrypt article reports a complete plaintext of 177 Latin words and publishes the plaintext. Word segmentation is part of the authors' decipherment account, not a reconstruction by this project.

### 5. `CIPHER_PLAINTEXT_ALIGNMENT`

The scholarly work supplies:

- the ordinary Porta table used in the analysis;
- the recovered 45-character key phrase;
- ciphertext-word -> Latin-word correspondences during the solve;
- the final plaintext;
- public C code / solving history in `RichardBean/ArthurDee`.

This is enough positive external evidence to justify a mechanical Gate-0 attempt at reproducing the cipher/plaintext correspondence without target-derived alignment.

## Important source-role distinction frozen now

The two textual authorities must not be silently conflated in the next Gate 0.

1. **Literal manuscript-boundary authority:** the Ambix 2023 literal transcription, explicitly described as reproducing what was copied on fol. 13. This controls physical lineation and observed source spacing.
2. **Cryptanalytic/correction authority:** the HistoCrypt 2022 transcription, recovered table/key, plaintext, and public `ArthurDee` code. These may be used to reproduce decryption and identify explicitly documented corrections, but they may not retroactively redefine physical line breaks or source spaces in the literal transcription.

The HistoCrypt paper notes that the final/corrected transcription was informed by plaintext during cryptanalysis. Therefore the Gate 0 must separately audit every difference between literal-source and cryptanalytic transcriptions before any R5 scoring is licensed.

## Stopped candidates

### HCPortal postcards

Final class: `HCPORTAL_POSTCARDS_NO_MACHINE_READABLE_CIPHERTEXT`.

The complete metadata-defined solved+text population supplied plaintext solutions but no machine-readable ciphertext, key, or deterministic alignment. No OCR/manual transcription repair is licensed.

### Mary Stuart / Castelnau

Final class after one preregistered transport recovery: `SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE`.

The paper and CTTS reference are public, but the machine-readable scholarly working transcription/key/alignment corpus was not located through the frozen public CTTS, Crossref, George Lasry GitHub, or Zenodo channels. No private/author-contact rescue is licensed.

### Ramanacoil

Already stopped in #194: the exact frozen DECODE document transport returned unusable identical non-UTF-8 payloads for transcription/key/decryption URLs. No post-reveal URL repair is licensed.

### Borg / Copiale

Retain #181/#182 results. Borg's source-side lexical-boundary attribution is confounded by lossy plaintext transport; Copiale lacks an independent unit boundary in the canonical R5 representation.

### ICDAR generic symbol-manuscript transport

Remains low-priority/non-admissible for this exact R5 responsibility because the official task representation is line-level symbol transcription and explicitly does not provide word grouping suitable for a terminal-unit -> initial-unit event without inventing segmentation.

### DECRYPT/HistoCrypt shared-task lead

Do not treat the historical `cipher_benchmark/source_audit.md` note about 2020–2022 paired shared-task sets as an established authority. During #196 screening, no concrete reproducible public paired shared-task payload was independently identified. It remains a future source lead, not the selected corpus.

## Consequence

Issue #196 has completed its only decision responsibility: select at most one source on preservation architecture before any R5 effect access.

Open a new issue for the Dee corpus Gate 0. That Gate must be score-free and must verify, rather than assume:

- exact literal transcription identity and lineation;
- exact source-space/cipher-word boundaries;
- literal-vs-corrected transcription differences;
- full table/key/plaintext reproduction;
- deterministic word/atom alignment;
- same-line and cross-line event support;
- whether support is sufficient for a separately preregistered source-attribution Stage 1.

No R5 likelihood is licensed by this screening result alone.
