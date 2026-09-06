# Issue #84 Phase C — frozen historical genre controls

Status: **PREREGISTERED — NO ADMITTED PHASE-C SOURCE HAS BEEN TARGET-SCORED**

Date: 2026-09-06

Parent: Issue #84.

Prior authority:

- Phase A: `REPORT_A.md`, frozen natural-language / seven-transcription baseline;
- Phase B: `REPORT_B.md`, frozen cipher-family map;
- C0: `PLAN_C0_SOURCE_AUDIT.md` and `REPORT_C0_SOURCE_AUDIT.md`.

This plan is frozen after source-only C0 admission and before the first corrected-MI or repeat-z score is computed for an admitted historical genre source.

---

## 1. Question

> Do frozen medieval / late-medieval recipe, herbal-medical, household-account or liturgical source texts themselves occupy the transcription-robust Voynich inter-token regime that ordinary natural-language prose and the tested common cipher representatives do not?

Phase C tests **source genre before encryption**. No Phase-B transform is applied here.

A positive source result is an existence result for a historical text organization, not evidence that the Voynich Manuscript is that source, language or genre. A negative result narrows the tested list/formulaic-natural-language branch but does not reject every possible medieval genre.

---

## 2. Frozen admitted documents

C0 admitted exactly ten primary source documents. C-HERB-1 Macer is excluded because its electronic edition does not permit a target-blind separation of poem and critical apparatus; no replacement is added.

Primary documents:

### Recipe / enumerative

1. `REC1_FormeOfCury` — C-REC-1 main Forme of Cury roll.
2. `REC2_Harl279` — C-REC-2 Harleian MS 279.
3. `REC2_Harl4016` — C-REC-2 Harleian MS 4016.

### Herbal / medical

4. `MED1_Herbarium_OE` — C-MED-1 Old English Herbarium pages only.

### Household / account

5. `ACC1_Countess1265`.
6. `ACC1_Executors1291`.
7. `ACC1_Howard1462_69`.
8. `ACC2_HouseholdBook1`.
9. `ACC2_HouseholdBook2`.

### Liturgical / formulaic

10. `LIT1_YorkManualProcessional` — C-LIT-1 primary York text after frozen music-line exclusion.

Source byte hashes, XML hashes, page spans and C0 extraction logic are fixed by `REPORT_C0_SOURCE_AUDIT.md` and must be asserted by the executable before scoring.

---

## 3. Frozen extraction rules

No OCR correction, spelling modernization, lemmatization, stopword removal, vocabulary pruning or source-specific token replacement is allowed.

### C-REC-1

- read the frozen Gutenberg UTF-8 text;
- span from exact marker `FOR TO MAKE GRONDEN BENES [1]. I.` up to but excluding exact marker `[1]XPLICIT.`;
- split into blank-line paragraphs;
- remove any paragraph whose first non-space characters match `^\[\d+\]`;
- retain all remaining historical text in original order.

### C-REC-2

Read frozen IA DjVu XML.

- `REC2_Harl279`: pages 24–83 inclusive;
- `REC2_Harl4016`: pages 86–126 inclusive;
- retain OCR lines whose vertical bounding-box midpoint is within `[0.10, 0.90] × page_height`.

No other extract in the edition is admitted.

### C-MED-1

Read frozen IA DjVu XML.

- admitted pages: 123, 125, …, 445 only;
- retain OCR lines whose vertical midpoint is within `[0.12, 0.68] × page_height`.

Even pages are the modern English translation and are excluded. Page 447 begins the next named work and is excluded.

### C-ACC-1

Read frozen IA DjVu XML.

- `ACC1_Countess1265`: pages 112–194;
- `ACC1_Executors1291`: pages 202–248;
- `ACC1_Howard1462_69`: pages 258–730;
- retain a line only if its vertical midpoint is within `[0.12, 0.76] × page_height` **and** its OCR line bounding-box height is at least 40 pixels.

### C-ACC-2

Read frozen IA DjVu XML.

- `ACC2_HouseholdBook1`: pages 40–276;
- `ACC2_HouseholdBook2`: pages 320–559;
- same normalized crop `[0.12, 0.76]` and minimum line height 40 pixels.

### C-LIT-1

Read frozen IA DjVu XML.

- pages 34–235 inclusive;
- retain line midpoint within `[0.10, 0.85] × page_height`;
- then retain the line only if all source-validity conditions hold:
  1. at least three Unicode word-like tokens in the line;
  2. alphabetic characters / non-space characters `>= 0.70`;
  3. ASCII-hyphen count / alphabetic-character count `<= 0.03`;
  4. one-character word-like tokens / line word-like tokens `<= 0.25`.

This line filter was frozen from source-only OCR/layout inspection to exclude staff notation and heavily syllabified chant OCR. It may not be changed after a Phase-C score is seen.

---

## 4. Token normalization

After primary-text extraction, concatenate retained lines in source order and apply exactly:

1. Unicode NFC normalization;
2. Unicode `casefold()`;
3. lexical token regex `[^\W\d_]+(?:['’][^\W\d_]+)?` with Unicode semantics;
4. each resulting token becomes a tuple of its Unicode characters for the unchanged Phase-A token scorer.

Consequences intentionally frozen:

- pure Arabic-number tokens and punctuation are excluded;
- alphabetic Roman-numeral / monetary forms such as `xij`, `s`, `d`, `li` remain because they are lexical-looking source forms under the same rule;
- Middle English / Old English letters and diacritics remain;
- OCR misspellings remain;
- line-end hyphenation is **not** repaired;
- no token is removed because it is frequent, formulaic, one character long, archaic or apparently corrupt.

---

## 5. Phase-A comparability cap

Phase A fixed `32,570` New-Testament tokens per natural-language sample. To prevent the very large account books from acquiring a qualitatively different sample-size regime, every Phase-C source document is capped at the **first 32,570 normalized tokens** after the frozen extraction above.

Shorter admitted documents are used in full. No source is resampled or window-selected. The prefix cap is inherited from Phase A and was fixed before any Phase-C target statistic.

Expected C0 source-only sizes before capping:

- REC1 11,850;
- Harl279 26,210;
- Harl4016 19,334;
- MED1 25,012;
- ACC1 Countess 22,109;
- ACC1 Executors 9,588;
- ACC1 Howard 147,864;
- ACC2 Book1 57,203;
- ACC2 Book2 69,847;
- LIT1 41,689.

The executable must reproduce these exact C0 token counts before applying the cap. A mismatch is `IMPLEMENTATION INVALID`, not a scientific result.

---

## 6. Primary target statistics — unchanged

Import the Phase-A scorer definitions unchanged for the target responsibilities. Phase C must not redefine the statistics.

For every source document, compute:

1. `MI1` — Phase-A null-corrected token mutual information at distance 1;
2. `z1_2` — Phase-A exact-repeat z-score for distance bin 1–2;
3. `z21_40` — Phase-A exact-repeat z-score for distance bin 21–40.

The exact seven-reading target intervals remain:

- `MI1`: `[0.05287300267140527, 0.11095606169252736]`;
- `z1_2`: `[2.7963710506633936, 8.455834173591136]`;
- `z21_40`: `[-0.7700738340053305, 3.434624139155326]`.

The executable verifies these endpoints against the frozen Phase-A result JSON (SHA-256 `86d18560b5999836b7c0d22fa9c3d8dbfd9f11ba246613fd0c2527d5ed5ffe1c`) before source scoring.

The invalidated Phase-A far bins are never decisive.

Other Phase-A outputs may be reported descriptively. Q3 cross-fitted unit-chain information is `NOT_APPLICABLE` for single-document source scores because the frozen five-fold document split has no valid held-out training fold; it may be reported only for multi-document genre aggregates where the unchanged routine is defined. Q3 cannot promote or reject a Phase-C source.

---

## 7. Document boundaries and aggregate views

### Primary scientific units

Each of the ten frozen source documents above is scored as **one continuous document** after the prefix cap. Printed page boundaries are not statistical document boundaries.

Reason fixed before reveal: making every recipe, account entry, rite or printed page a separate scorer document would mechanically destroy valid 21–40-token recurrence opportunities and would make the target statistic depend on editorial segmentation rather than source sequence.

### Descriptive genre aggregates

Also report, with component boundaries preserved:

- `GENRE_RECIPE`: three recipe documents;
- `GENRE_MEDICAL`: one MED1 document;
- `GENRE_ACCOUNT`: five account documents;
- `GENRE_LITURGY`: one LIT1 document.

Genre aggregates are descriptive context, not a substitute for work-level results. A long document cannot erase or promote a work-level classification.

---

## 8. Frozen work-level classification

For every frozen source document define:

- `R_MI`: `MI1` inside the exact seven-reading interval;
- `R_SHORT`: `z1_2` inside the exact seven-reading interval;
- `R_MID`: `z21_40` inside the exact seven-reading interval.

Classification:

- **`VOYNICH INTER-TOKEN REGIME SOURCE HIT`** — all 3 pass;
- **`PARTIAL SOURCE HIT (2/3)`** — exactly two pass;
- **`PARTIAL SOURCE HIT (1/3)`** — exactly one passes;
- **`NO SOURCE HIT`** — none pass.

For every primary component report signed distance to the nearest target-interval boundary, zero when inside.

Across the frozen ten-document panel:

- if at least one document is a full hit: `SOME FROZEN HISTORICAL SOURCE IN VOYNICH REGIME`;
- otherwise: `NO FROZEN HISTORICAL SOURCE IN FULL VOYNICH REGIME`.

This is an existence statement over the complete preregistered panel. Every document remains visible; there is no best-source-only reporting.

A hit in one document does **not** license the statement that its whole genre is Voynich-like. Genre-wide generalization requires later replication in independently frozen sources. Conversely, failure of this finite panel does not reject all list-like or liturgical texts.

---

## 9. Pre-score validity gates

Before the first source target score is accepted, the executable/workflow must verify:

1. exact Phase-A JSON SHA-256 and exact target intervals;
2. exact source TXT/XML SHA-256 values from C0;
3. exact C0 extraction token counts listed in §5;
4. all ten source documents remain above 2,000 tokens before capping;
5. prefix caps are exactly `min(n, 32570)`;
6. no Phase-B cipher function is imported or called;
7. C-HERB-1 Macer remains absent from scored documents;
8. no downloaded third-party source text/XML is written into the repository checkout as a commit operation.

A source-hash, extraction-count or source-layout mismatch stops the run before target scoring.

---

## 10. Interpretation matrix

### At least one full source hit

A historical natural-language/formulaic source organization can, without the tested cipher step, reproduce the complete three-component inter-token regime in this frozen panel. The next licensed move is **not** immediate decipherment; it is independent-source replication inside that source class and only then a separately preregistered source×transform test if historically motivated.

### Partial hits only

Record which responsibilities are supplied by which source organization. Do not post-hoc splice a source's successful responsibility with a Phase-B transform or Issue-#81 memory.

### No full hit

The tested recipe, Herbarium, account and liturgical source organizations do not by themselves reproduce the complete regime. Combined with Phase A and Phase B, this materially narrows ordinary meaningful-text explanations under the tested source/transform families, while leaving untested genres, more specialized historical mechanisms and the independent generative-memory branch open.

---

## 11. Prohibited after reveal

- changing OCR crop windows, page ranges or line filters because a source nearly hits;
- correcting historical/OCR spellings selectively;
- changing the 32,570-token cap or selecting another source window;
- splitting or joining scorer documents to repair `z21_40`;
- adding a replacement Macer edition after observing Phase-C target scores;
- tuning any Phase-B transform on a promising genre source;
- combining responsibilities across different sources/mechanisms into a claimed full hit;
- using Q3 or an omnibus average to override a failed primary responsibility;
- claiming plaintext, semantics, authorship, historical cipher or decipherment from a genre-control hit.
