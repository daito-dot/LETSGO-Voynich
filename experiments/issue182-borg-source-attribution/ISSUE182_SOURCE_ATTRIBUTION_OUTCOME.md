# Issue #182 source-attribution outcome

Date: 2026-09-07
Parent: Issue #172
Status: **COMPLETE — FULL-CORPUS SOURCE ATTRIBUTION INDETERMINATE; NO STAGE-1 EDGE SCORE REVEALED**

## Question

Issue #181 established `EXTERNAL LINE-LOCAL EDGE` in Borg ciphertext. Issue #182 asked whether that topology survives after distinguishing true solved-plaintext lexical boundaries from cipher-unit boundaries created by physical manuscript line wrapping.

## Stage 0 — committed benchmark plaintext tokens

The frozen exact/all-optimal-path alignment succeeded mechanically:

- 397/397 non-empty Borg canonical pages;
- 24,501 cipher groups;
- 18,201 published-key-covered groups;
- 14,404 stably aligned groups;
- same-line committed-token `LEXICAL_BOUNDARY`: 6,657;
- cross-line committed-token `LEXICAL_BOUNDARY`: 1,409;
- same-line `WITHIN_WORD_SPLIT`: 92;
- cross-line `WITHIN_WORD_SPLIT`: 0;
- `edge_gain_computed = false`.

Authority:

- full Stage-0 SHA-256: `e3443bf753343eecea73dcd314bf6e78954b724945daa2a1d4eb8eb66704845e`;
- original workflow run: `34123660555`, artifact `10019196163`;
- full authority subsequently reproduced byte-for-byte and committed to main.

### Pre-score composability failure

Before Stage 1, the benchmark transformation provenance was re-audited. `create_borg_benchmark.py` replaces every corrected-source manuscript-line marker `|` with a space when writing committed plaintext pages.

This erases the distinction between:

- line break between solved words; and
- line break splitting one solved word.

Thus a committed plaintext token boundary is not sufficient authority for the intended lexical-word control.

No Stage-1 gain had been computed when this failure was identified.

## Stage 0-R1 — current Stockholm corrected source

A recovery was preregistered before scoring using Stockholm University's official Urban Örneholm corrected-Latin+translation file. The lexical restoration rule used only whitespace around source `|`:

- no whitespace immediately on either side -> join fragments into one lexical token;
- otherwise retain a lexical boundary.

No dictionary, morphology, edit distance, cipher symbol identity or R5 score entered the restoration.

Result:

- classification: `STAGE0R1_INVALID_OR_INSUFFICIENT`;
- official-source SHA-256: `0c5c0a5b7554a097541e41ac37869f7e00578627fa2aac2ffa9b11d8e6be1d24`;
- source page blocks recovered under the frozen benchmark parser: 302;
- exact benchmark plaintext reproductions: 289/397;
- mismatches: 108;
- `edge_gain_computed = false`.

The failure is transport/format compatibility, not the lexical restoration concept.

### Score-free finding on the compatible population

Without computing any edge statistic, the restored alignment found:

- cross-line restored lexical boundaries: 728;
- cross-line restored within-word splits: **260**;
- same-line restored lexical boundaries: 4,140;
- same-line restored within-word splits: 62.

Relative to the old committed-token labels on the same source-compatible population:

- **260 cross-line events changed from `LEXICAL_BOUNDARY` to `WITHIN_WORD_SPLIT`**;
- another 13 cross-line old lexical boundaries became unaligned/ambiguous.

Therefore the erased line-wrap/lexical distinction is not hypothetical. It materially affects the boundary taxonomy in real Borg pages.

No inference about the direction or magnitude of terminal→initial gain is permitted from these support counts.

## Stage 0-R2 — independently referenced 2024 Wayback transport

The ALICE Borg evaluation independently cites a 2024-09-20 Wayback URL for the corrected-Latin source. R2 froze that URL as the sole permitted transport change and reused the R1 parser/restoration/alignment unchanged.

The replay request returned a payload with the **same SHA-256 as the current Stockholm download**:

`0c5c0a5b7554a097541e41ac37869f7e00578627fa2aac2ffa9b11d8e6be1d24`

Accordingly it reproduced the same 302 parsed source page blocks, 289/397 exact benchmark pages and 108 mismatches.

Classification:

`STAGE0R2_INVALID_ARCHIVAL_TRANSPORT`

Per the frozen R2 firewall, no parser relaxation, `id_` replay variant, page subsetting, current/archive merge or manual reconstruction is allowed after this failure.

## Final classification

> **SOURCE ATTRIBUTION INDETERMINATE ON THE FULL ISSUE-#181 BORG POPULATION**

The reserved Stage-1 R5 scorer was never frozen or executed. No new same-line/cross-line edge likelihood, fold gain or effect size was revealed in Issue #182.

## What #182 establishes

1. The #181 Borg R5-like topology is real on the canonical ciphertext representation.
2. Static substitution alone cannot be credited with creating it merely from that observation.
3. The committed solved-plaintext files are lossy with respect to lexical word continuity at physical line breaks.
4. On 289 source-compatible pages, at least 260 cross-line boundaries previously treated as committed plaintext token boundaries are independently identified by source orthography as within-word line splits.
5. Therefore plaintext inheritance / physical line wrapping remains a live source of the Borg topology and cannot be separated cleanly on the full corpus with the currently frozen authorities.
6. R5 remains unsuitable as a standalone anti-cipher discriminator: a real historical substitution ciphertext has the topology even though its exact source decomposition remains unresolved.

## What #182 does not establish

- that line wrapping causes the Borg edge;
- that substitution causes the Borg edge;
- that Borg is structurally equivalent to Voynich beyond the tested R5 topology;
- that Voynich is encrypted;
- that Voynich spaces are plaintext word boundaries;
- that the 289-page partial population may be used for an unregistered Stage-1 score.

## Program consequence

Return to Issue #172 architecture selection.

The next candidate family should treat R5 as a compatibility responsibility rather than a uniquely diagnostic cipher/no-cipher separator, and it must be independently motivated before any new Voynich target scoring. Do not repair Borg source attribution by relaxing the lexical authority after reveal, and do not compose the failed A1/Naibbe/LM-A0 components to cover the #176 vector.

Issue #179 remains exploratory and unscored.
