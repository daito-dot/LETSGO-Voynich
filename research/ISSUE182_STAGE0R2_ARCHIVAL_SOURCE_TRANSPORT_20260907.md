# Issue #182 — Stage 0-R2 archival corrected-Latin transport recovery

Date: 2026-09-07
Parent: Issue #182 / #172
Follows: Stage 0-R1 `STAGE0R1_INVALID_OR_INSUFFICIENT`
Status: **SCORE-FREE SOURCE-TRANSPORT RECOVERY ONLY — STAGE 1 REMAINS SEALED**

## Why R2 is licensed

Stage 0-R1 established two separate facts before any Stage-1 edge gain:

1. the current Stockholm University corrected-Latin download is not transport-compatible with the frozen benchmark creator's `^#page` parser across the full 397-page population;
2. on the 289 pages that do reproduce exactly, restoring source-native no-whitespace `|` joins recovers 260 `CROSS_PHYSICAL_LINE × WITHIN_WORD_SPLIT` events that the committed benchmark plaintext tokenization had mislabeled as token boundaries.

Stage 0-R1 is therefore archived as invalid for full-corpus authority. Its partial result may not be scored.

The current source file is not modified or reparsed to rescue it.

## Independently referenced archival authority

Use exactly the archived corrected-Latin source cited in the Borg evaluation of the ALICE cryptogram work:

`https://web.archive.org/web/20240920225756/https://www.su.se/polopoly_fs/1.689014.1699461276!/menu/standard/file/corrected-Latin-translation.txt`

Snapshot timestamp: **2024-09-20 22:57:56 UTC**.

The archival source predates the current Stockholm site migration and is independently referenced as the Borg corrected-Latin evaluation source. It is selected by external provenance, not by any R5 score.

Stage 0-R2 must record the downloaded payload SHA-256 before deriving any lexical-boundary authority.

## Frozen implementation

Reuse **without modification**:

- pinned Borg benchmark commit `729aad62d12483c549e64a2541d4f9255538c8cf`;
- first Stage-0 diplomatic/canonical representation;
- published key;
- `parse_paged_text` with the benchmark creator's line-anchored `^#page` convention;
- benchmark-lossy plaintext reproduction function;
- source-whitespace lexical restoration rule from Stage 0-R1;
- exact-run monotone DP and all-optimal-path ambiguity rule;
- Stage 0-R1 event representation containing only page/group indices, physical relation and boundary class;
- no terminal/initial atom identities in the derived authority.

The only licensed change from Stage 0-R1 is the external corrected-Latin file transport URL.

## Validity gate

`LEXICAL_RESTORATION_ARCHIVAL_AUTHORITY_VALID` requires all of:

1. the archival source parses without manual repair;
2. the benchmark creator's lossy extraction reproduces all **397/397** committed benchmark plaintext pages exactly;
3. diplomatic/canonical reproduction remains exact;
4. restored `LEXICAL_BOUNDARY` support remains at least 100 events for SAME and CROSS physical relations;
5. at least one `CROSS_PHYSICAL_LINE × WITHIN_WORD_SPLIT` event is recovered;
6. `edge_gain_computed = false`.

If 397/397 exact reproduction fails, classify `STAGE0R2_INVALID_ARCHIVAL_TRANSPORT` and stop. Do not change the page parser, normalize page content, subset pages, or merge current and archival Stockholm files.

## Consequence

If valid, commit:

- archival source URL and SHA-256;
- compact summary;
- full score-free boundary event authority;
- full authority SHA-256.

Only after that commit may a separate Stage-1 scorer be frozen.

If invalid, Issue #182 cannot answer lexical-word source attribution on the full #181 population using currently established external authorities; record the result as indeterminate and return to #172 rather than inventing a lexical restoration model.

Issue #179 remains sealed.
