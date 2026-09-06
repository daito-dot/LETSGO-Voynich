# Issue #84 Phase C0 — genre-control source audit

Status: **PREREGISTERED — SOURCE AUDIT ONLY, NO VOYNICH-TARGET SCORING**

Parent: Issue #84 Phase C.

Base authority: `main@f4a9533ab970d5113a8bd833da5f46a241ac3132` after the merged Phase-B first reveal.

This C0 document freezes the candidate source list and source-admission rules **before any Phase-C Q1/Q2 statistic is computed**. C0 is not itself the Phase-C scientific test. Its sole purpose is to establish which public historical editions can be fetched reproducibly and isolated into primary-text spans without consulting Voynich outcomes.

## 1. Scientific reason for C0

Phase A showed that ordinary natural-language prose does not occupy the Voynich inter-token regime. Phase B showed that the frozen common reversible-operation representatives do not move CREMMA Latin prose into the complete regime. The next discriminator is therefore source genre:

> Can recipe, herbal/medical, household-account, or liturgical source texts already possess unusual local/mid-range recurrence before any cipher transform is applied?

Historical editions are heterogeneous. A source can contain prefaces, apparatus, translations, indexes, OCR damage and multiple embedded works. Treating a whole downloaded volume as the historical source would confound genre with edition apparatus. C0 therefore fixes the source candidates first, then inspects only source provenance and extractability. Target statistics are prohibited during C0.

## 2. Frozen candidate-source panel

The panel is fixed now. No source may be added because another source later scores poorly or removed because it looks statistically inconvenient.

### Recipe / enumerative controls

**C-REC-1 — The Forme of Cury**

- historical text: late-14th-century Middle English recipe collection, conventionally c.1390;
- public electronic edition: Project Gutenberg eBook 8102;
- fetch authority: `https://www.gutenberg.org/cache/epub/8102/pg8102.txt`;
- intended unit: individual numbered recipe, with the historical Middle English text retained and editor introduction/glossary excluded.

**C-REC-2 — Two Fifteenth-Century Cookery-Books**

- historical texts: Harleian MS 279 (c.1430) and Harleian MS 4016 (c.1450), plus the edition's explicitly identified historical extracts;
- edition: Thomas Austin (ed.), Early English Text Society OS 91, 1888;
- Internet Archive identifier: `twofifteenthcent00aust`;
- intended unit: recipe/section within each separately identified manuscript text; modern editorial preface, notes and glossary excluded.

### Herbal / medical controls

**C-HERB-1 — Macer Floridus, De viribus herbarum**

- historical text: medieval Latin herbal poem;
- edition: Ludwig Choulant (ed.), Leipzig, 1832;
- Internet Archive identifier: `deviribusherbaru00mace`;
- intended unit: named herb chapter/section in the Latin `De viribus herbarum`; German editorial matter, Greek ancillary material, later appendices and indexes excluded.

**C-MED-1 — Leechdoms, Wortcunning, and Starcraft of Early England, vol. 1**

- historical material: Old English medical/herbal texts printed in Thomas Oswald Cockayne's 1864 edition;
- Internet Archive identifier: `leechdomswortcun01cock`;
- intended unit: separately headed primary remedy/herbal entries from the Old English source text; editor prose and facing/adjacent modern English matter are excluded where the edition permits an objective boundary.

This candidate is allowed to fail C0 if the OCR/edition layout does not permit a deterministic primary-text extraction without language-model judgement or manual target-aware editing.

### Household-account / administrative controls

**C-ACC-1 — Manners and Household Expenses of England in the Thirteenth and Fifteenth Centuries**

- edition: Roxburghe Club, 1841;
- historical components named in the edition: household roll of Eleanor, Countess of Leicester (1265); accounts of the executors of Eleanor of Castile (1291); accounts and memoranda of Sir John Howard (1462–1471);
- Internet Archive identifier: `cu31924027939820`;
- intended unit: dated/account entry within each explicitly delimited historical component; editorial introduction excluded.

**C-ACC-2 — Household Books of John, Duke of Norfolk, and Thomas, Earl of Surrey, 1481–1490**

- edition: J. Payne Collier (ed.), Roxburghe Club, 1844;
- Internet Archive identifier: `cu31924027939861`;
- intended unit: dated/account entry; editorial introduction and index excluded.

### Liturgical / formulaic control

**C-LIT-1 — Manuale et processionale ad usum insignis ecclesiae Eboracensis**

- historical text: York Use manual/processional represented from manuscripts and the printed editions of 1509/1516;
- edition: W. G. Henderson (ed.), Surtees Society, 1875;
- Internet Archive identifier: `manualeetp00cath`;
- intended unit: rubric/rite/office section in the primary Latin text; editor preface/notes and the separately identified comparative appendix are excluded from the primary view.

The edition contains Latin primary text and English editorial matter. C0 must show that deterministic page/section boundaries can isolate the primary text. If not, this candidate fails C0 rather than being hand-cleaned after scoring.

## 3. Why these sources were selected before scoring

The frozen list satisfies four independent design goals:

1. direct representation of the Phase-C genres named in Issue #84: recipe/enumerative, herbal/medical, household-account and liturgical;
2. chronological relevance to the medieval/late-medieval comparison problem rather than modern list prose;
3. public, citable digitization with a stable edition identifier or eBook identifier;
4. enough expected text to support distance-21–40 recurrence estimation at more than toy scale.

No source was selected from its Q1/Q2 relationship to Voynich; no Phase-C Q1/Q2 value exists at the time of this freeze.

## 4. C0 source-admission rules

C0 may inspect download bytes, metadata, OCR structure, printed/page markers, headings and tokenizable text volume. It may **not** import or call `phase84a.score`, read the Phase-A target intervals for classification, or compute the Phase-C primary statistics.

A source is `C0 PASS` only if all applicable conditions hold:

1. **reproducible fetch** — the frozen URL/Internet Archive item resolves and the exact downloaded representation receives a recorded SHA-256;
2. **edition identity** — metadata/title/year are compatible with the edition frozen above;
3. **machine-readable text** — UTF-8/decodable text or Internet Archive OCR exists; source images alone are not sufficient for this phase;
4. **primary-span determinism** — the source has page markers, headings or other edition-internal boundaries from which a rule-based extractor can exclude editorial apparatus without manual semantic selection;
5. **minimum primary-text scale** — the objectively isolatable primary span is expected to yield at least 2,000 whitespace/word-like tokens after a simple source-language normalization; this is a construct-validity floor, not a Voynich-derived threshold;
6. **no target-aware cleaning** — the extraction rule can be written from edition structure alone before any Q1/Q2 score is viewed.

`C0 FAIL` means only that this frozen electronic edition is unsuitable for the preregistered automated comparison. It does not mean the historical work or genre is scientifically unsuitable.

## 5. Allowed C0 outputs

For every frozen source, C0 records:

- source URL / IA identifier;
- metadata title, publication date and file names;
- byte size and SHA-256 of the downloaded text representation;
- encoding/decoding status;
- OCR/page count when available;
- counts of raw lines and simple word-like tokens;
- objective marker candidates needed to delimit primary text;
- up to short diagnostic snippets around those markers in the Actions artifact only;
- C0 PASS / NEEDS-BOUNDARY / FAIL and reason.

No third-party source text is committed to this repository. Only hashes, metadata, extraction rules and fetch scripts may be committed.

## 6. Phase-C firewall during C0

Prohibited until a separate `PLAN_C.md` is frozen:

- computing corrected MI at any distance for these sources;
- computing exact-repeat z-scores or distance profiles for these sources;
- ranking sources by resemblance to any Voynich reading;
- changing the source list because of any target statistic;
- selecting only a favorable chapter, recipe cluster, month, account period or liturgical office;
- manually deleting OCR tokens based on whether they affect target metrics;
- combining source texts with any Phase-B cipher transform.

The C0 executable/workflow must contain no call to the Phase-A scorer. The log must explicitly state `TARGET_SCORE_CALLS=0`.

## 7. What happens after C0

After source bytes and deterministic extraction boundaries are known, a **separate preregistration** `PLAN_C.md` will freeze:

- exact admitted sources and their SHA-256 values;
- exact extraction functions and primary spans;
- normalization/tokenization rules;
- document/unit definition;
- minimum-length handling;
- Phase-A/Phase-B primary statistics and decision rules;
- corpus-level interpretation, including how multiple works per genre are handled;
- sensitivity analyses that cannot promote a failed primary result.

Only after that second freeze may Phase-C Q1/Q2 scoring begin.
