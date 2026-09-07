# Issue #182 — Stage-1 composability audit and Stage 0-R1 lexical restoration plan

Date: 2026-09-07
Parent: Issue #182 / #172
Status: **PRE-SCORE COMPOSABILITY FAILURE IDENTIFIED; STAGE 1 REMAINS SEALED**

## Why Stage 1 is not yet valid

The first Stage-0 alignment is mechanically valid against the **committed benchmark plaintext tokens**:

- 397/397 pages reproduced;
- no new edge gain was computed;
- 6,657 same-line and 1,409 cross-line boundaries received `LEXICAL_BOUNDARY` under that representation;
- full authority SHA-256: `e3443bf753343eecea73dcd314bf6e78954b724945daa2a1d4eb8eb66704845e`.

However, the intended Stage-1 question is stricter: remove physical-line wrapping that splits a single solved lexical word before asking whether the R5 line-local edge survives.

The benchmark's committed plaintext files cannot by themselves make that distinction.

### Representation fact

`matthewdgreen/cipher_benchmark/scripts/create_borg_benchmark.py` builds each committed Borg plaintext page from Urban Örneholm's corrected-Latin/translation source and then executes:

```python
latin_text = re.sub(r"\s*\|\s*", " ", latin_text)
```

Thus the source manuscript-line marker `|` is erased and replaced with a space regardless of whether the break occurred **between** words or **inside** one word.

The committed page `borg_0002r.txt`, for example, contains:

- `benedic ti`
- `cr ispe`
- `fortis simi`
- `lo co`
- `ui treo`

The official Stockholm University corrected source retains the relevant distinctions as:

- `benedic|ti`
- `cr|ispe`
- `fortis|simi`
- `lo|co`
- `ui|treo`

while genuine between-word line changes appear with whitespace around the marker, e.g. `calamenti thimi | pulegi`.

Therefore the first Stage-0 label `LEXICAL_BOUNDARY` means only **boundary between committed benchmark plaintext tokens**. It is not yet a reliable solved lexical-word boundary. In particular, cross-line within-word splits can be misclassified as lexical boundaries.

The fact that the first Stage-0 authority contains 92 `WITHIN_WORD_SPLIT` events on the same physical line but zero cross-line `WITHIN_WORD_SPLIT` events is not evidence that cross-line word splitting is absent; the source transformation erased exactly the distinction needed to detect it.

## Consequence

Do **not** run the reserved Stage-1 lexical-boundary R5 scorer on the first Stage-0 labels.

Doing so would retain the confound Stage 1 is intended to remove.

No Stage-1 edge gain has been inspected at the time of this audit, so correcting the lexical authority now does not constitute result-driven model repair.

## Independent lexical authority

Use the official Stockholm University Borg project download:

`https://www.su.se/download/18.6856063019d24ef3ecb111e/1774945344171/corrected-Latin-translation.txt`

The project page identifies this file as **Corrected Latin text with translation [by Urban Örneholm]**. It is upstream of the benchmark's committed plaintext extraction and preserves the manuscript-line marker `|`.

Stage 0-R1 must fetch this exact URL before any Stage-1 edge score and record its SHA-256. The source content itself need not be copied into the research repository; its derived authority and hash must be archived.

## Stage 0-R1 source-compatibility audit

Before using the source for lexical restoration:

1. parse `#page` blocks using the benchmark creator's `parse_paged_file` convention;
2. normalize folio IDs with the benchmark creator's `normalize_folio` convention;
3. select Latin lines using the benchmark creator's `extract_latin_plaintext` rule: a non-empty line is Latin if it contains `|` or is a standalone bracketed heading;
4. reproduce the benchmark transformation exactly by joining selected Latin lines and replacing every `\s*\|\s*` with one space;
5. require exact UTF-8 text equality, after `.strip()`, with every committed plaintext file in the frozen 397-page Issue-#181 population.

If all 397 pages are not reproduced, classify `STAGE0R1_INVALID_SOURCE_COMPATIBILITY` and stop. No page-level manual repair is allowed.

This audit proves that the official source being used is the upstream authority represented by the committed benchmark plaintext rather than a separately edited text.

## Frozen lexical restoration rule

The physical-line marker is interpreted from **source whitespace only**, before any lexical normalization:

- if `|` has a non-whitespace character immediately on both sides, remove the marker with **no inserted space**;
- otherwise replace the marker and surrounding whitespace with one ASCII space.

Examples fixed by the source convention:

- `benedic|ti` -> `benedicti`
- `cr|ispe` -> `crispe`
- `calamenti thimi | pulegi` -> `calamenti thimi pulegi`

No dictionary, Latin morphology, edit distance, frequency, cipher terminal/initial identity, or R5 score is allowed to decide whether fragments are joined.

After this marker operation:

1. Unicode NFC + casefold;
2. remove square-bracket delimiters while retaining bracket contents, exactly as the first Stage-0 plaintext normalization intended;
3. replace characters that are not Unicode letters/combining marks with spaces;
4. split on whitespace;
5. no `u/v`, `i/j`, spelling, lemma, morphology, or language-model normalization.

## Stage 0-R1 alignment

Reuse the already-frozen Stage-0 cipher-side representation, published key, exact-run monotone dynamic programming objective, and all-optimal-path ambiguity rule without modification.

Only the plaintext token authority changes from the lossy committed benchmark plaintext tokenization to the score-free restored lexical tokens derived above.

For every immediate cipher-unit boundary, freeze:

- `page_id`;
- left and right cipher-group flat indices;
- `SAME_PHYSICAL_LINE` or `CROSS_PHYSICAL_LINE`;
- `LEXICAL_BOUNDARY`, `WITHIN_WORD_SPLIT`, or `UNALIGNED_OR_AMBIGUOUS`.

Do not include terminal/initial atom identities or likelihoods in the Stage-0R1 derived event authority.

## Stage 0-R1 outputs

Allowed outputs remain score-free:

- official-source SHA-256;
- 397-page source-compatibility audit result;
- restored-token counts and exact alignment coverage;
- boundary counts by physical relation × lexical class;
- count of event labels that changed relative to first Stage 0;
- page support counts;
- full event-ID/class authority without cipher atom identities;
- `edge_gain_computed = false` assertion.

## Stage 0-R1 validity gate

`LEXICAL_RESTORATION_AUTHORITY_VALID` requires all of:

1. the official source reproduces all 397 committed benchmark plaintext pages under the benchmark's own lossy extraction rule;
2. diplomatic/canonical representation still reproduces exactly under the pinned symbol map;
3. at least 100 restored `LEXICAL_BOUNDARY` events remain in each physical relation;
4. at least one `CROSS_PHYSICAL_LINE × WITHIN_WORD_SPLIT` event is recovered, establishing that the restored authority actually distinguishes the known erased boundary class;
5. no terminal/initial edge gain is computed.

If condition 4 fails, classify `STAGE0R1_INVALID_LEXICAL_RESTORATION` rather than treating zero recovered splits as evidence of absence.

## Stage 1 after Stage 0-R1

Only if Stage 0-R1 is valid may a new Stage-1 scorer be frozen.

The reserved question is unchanged:

> On solved **restored lexical-word boundaries only**, does Borg retain positive terminal→initial gain within physical lines while the same factor remains non-positive across physical line breaks?

Stage 1 must use the same #181 page folds, `alpha=0.01`, factor definition, and 4/5 sign-stability rule. It must also verify numerical key-relabel invariance on the exact frozen event population.

A positive result would locate the topology at the source/layout level after word-split control. A collapse would attribute a substantial part of #181 to erased line-wrap/lexical-boundary mixing. Neither result would by itself identify the Voynich mechanism.

Issue #179 remains sealed throughout this recovery.
