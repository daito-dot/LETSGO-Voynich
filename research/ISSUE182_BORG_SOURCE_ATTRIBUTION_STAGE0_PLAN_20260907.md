# Issue #182 — Borg source attribution Stage 0 alignment plan

Date: 2026-09-07
Parent: Issue #172
Issue: #182
Status: **FROZEN ALIGNMENT-ONLY PLAN — NO NEW EDGE GAIN LICENSED**

## Question

Issue #181 established that the solved Borg ciphertext has the qualitative R5 topology: previous cipher-unit terminal identity helps next-unit initial prediction within physical lines and hurts across physical line breaks.

Stage 0 asks only whether the solved external authority can assign those cipher-unit boundaries to plaintext lexical structure without using edge scores.

No `G_line`, `G_cross`, position-only likelihood, conditional likelihood, Voynich statistic, or target candidate score may be computed in Stage 0.

## External authority

Use only `matthewdgreen/cipher_benchmark` at pinned commit:

`729aad62d12483c549e64a2541d4f9255538c8cf`

Required files:

- `benchmark/sources/borg/transcriptions/borg_*.diplomatic.txt`
- `benchmark/sources/borg/transcriptions/borg_*.canonical.txt`
- `benchmark/sources/borg/plaintext/borg_*.txt`
- `benchmark/sources/borg/metadata/borg_symbol_map.json`
- `scripts/create_borg_benchmark.py` as transformation provenance

The same 397 non-empty canonical pages admitted by Issue #181 are the Stage-0 page population. No page is removed because alignment looks poor.

## Authority facts fixed before alignment

The benchmark creation code:

- preserves diplomatic physical lines in canonical ciphertext;
- removes `<CLEARTEXT...>` lines;
- removes editorial `[bracketed]` material from the ciphertext transcription before canonicalization;
- splits the remaining diplomatic line on whitespace into cipher groups;
- emits those groups separated by literal `|`;
- extracts corrected Latin plaintext separately and removes original plaintext `|` manuscript-line markers before writing the committed plaintext file.

Therefore the committed solved plaintext is page-linked but no longer independently line-linked. Stage 0 must recover only lexical-token alignment, while physical line relation continues to come from the ciphertext transcription.

The published `cipher_key` contains a one-to-one mapping for a subset of diplomatic cipher characters. Stage 0 treats any cipher group containing at least one character outside that published key as `UNKEYED`; it does not guess or infer the missing key.

## Frozen normalization

### Diplomatic ciphertext

Reproduce the benchmark canonicalization population exactly:

1. process diplomatic text line by line;
2. skip empty lines;
3. skip lines whose stripped text begins with `<CLEARTEXT`;
4. remove every non-greedy `\[.*?\]` editorial bracket span exactly as the benchmark creation script does;
5. split the remaining text on whitespace into cipher groups;
6. retain physical line index and within-line group index.

For every group, verify against the committed canonical page that character-wise `borg_symbol_map.json` mapping reproduces the corresponding `S###` group. A page/group mismatch invalidates Stage 0; do not repair it manually.

### Decrypted group projection

A cipher group is `KEYED` iff every diplomatic character in the cleaned group is a key in the published `cipher_key`.

For a KEYED group, decrypted text is the exact concatenation of published key values in character order, casefolded.

No punctuation stripping or unknown-symbol deletion is allowed inside a group. A group with even one unkeyed character is `UNKEYED` and cannot participate in an exact lexical match.

### Published solved Latin

Normalize each committed plaintext page as follows:

1. Unicode NFC + casefold;
2. remove square-bracket delimiters `[` and `]` while retaining their contents, so editorial completion is concatenated with adjacent letters when written inside a word;
3. replace every run of characters that is not a Unicode letter/combining mark with one ASCII space;
4. split on whitespace into normalized plaintext lexical tokens;
5. do not normalize `u/v`, `i/j`, spelling, morphology, lemmas, abbreviations, or Latin orthography beyond the rules above.

Examples under this rule:

- `se[minum]` -> `seminum`
- `[manipulum]` -> `manipulum`
- punctuation does not create a token.

## Frozen page-local monotone alignment

Let cipher groups be `C[0..n-1]`, each KEYED or UNKEYED, and plaintext tokens be `P[0..m-1]`.

Allowed transitions consume the sequences monotonically:

1. `SKIP_CIPHER`: consume one cipher group with no match reward;
2. `SKIP_PLAIN`: consume one plaintext token with no match reward;
3. `EXACT_RUN_MATCH(i,k,j)`: consume consecutive cipher groups `C[i:k]` and plaintext token `P[j]` iff:
   - every group in the run is KEYED;
   - concatenating their decrypted strings exactly equals `P[j]`;
   - no maximum run length is imposed; candidate extension stops once concatenated length exceeds the plaintext-token length.

An exact run may cross one or more ciphertext physical line boundaries. This is necessary to recognize a plaintext word split by manuscript line wrapping and is determined by exact plaintext equality, not edge behavior.

### Frozen optimization objective

Choose alignments lexicographically by maximizing:

1. total matched plaintext characters;
2. total matched cipher groups;
3. total matched plaintext tokens.

Skip order carries no reward.

No edit-distance, fuzzy match, Latin dictionary, semantic similarity, key completion, or manual correction is permitted.

## Ambiguity handling across all optimal alignments

A deterministic single path is not enough because repeated Latin tokens can permit equally optimal monotone alignments.

Stage 0 must compute forward and backward optimal dynamic-programming values and identify every transition that lies on at least one globally optimal alignment.

For each cipher group:

- collect every plaintext-token index to which that group can be assigned by a globally optimal `EXACT_RUN_MATCH` transition;
- determine whether a globally optimal `SKIP_CIPHER` transition can leave that group unmatched.

A cipher group receives a stable token assignment only if:

1. the possible plaintext-token index set has exactly one member; and
2. the group cannot be skipped on any globally optimal alignment.

Otherwise its assignment is `AMBIGUOUS_OR_UNALIGNED`.

This all-optimal-path rule prevents repeated-word tie-breaking from manufacturing boundary labels.

## Frozen immediate-boundary labels

Use the exact immediate cipher-unit boundaries from the cleaned diplomatic/canonical representation.

For each adjacent pair of cipher groups on a page, retain physical relation from ciphertext:

- `SAME_PHYSICAL_LINE`; or
- `CROSS_PHYSICAL_LINE` only for last group of one physical line -> first group of immediately following non-empty canonical physical line, exactly as Issue #181.

Then assign plaintext boundary class from stable token assignments:

- `WITHIN_WORD_SPLIT`: both groups are stably assigned to the same plaintext-token index;
- `LEXICAL_BOUNDARY`: both are stably assigned and the next token index is exactly previous index + 1;
- `UNALIGNED_OR_AMBIGUOUS`: all other cases, including an intervening skipped plaintext token.

No boundary is promoted from unaligned to lexical by string similarity outside the frozen exact alignment.

## Stage-0 outputs

Score-free outputs only:

1. page/file correspondence audit;
2. canonical-vs-diplomatic reproduction audit;
3. published key size and canonical key-covered atom inventory;
4. total cipher groups and KEYED/UNKEYED group counts;
5. total solved plaintext-token count;
6. stable aligned cipher-group count;
7. ambiguous/unassigned group count;
8. matched plaintext-token and matched-character coverage;
9. immediate boundary counts in the 2×3 table:
   - SAME vs CROSS physical line;
   - LEXICAL vs WITHIN_WORD_SPLIT vs UNALIGNED;
10. per-page alignment support and ambiguity diagnostics;
11. assertion `edge_gain_computed = false`.

## Stage-0 validity gate

`ALIGNMENT_STAGE0_VALID` requires:

- 397 non-empty canonical pages from Issue #181 are reproduced;
- every corresponding diplomatic/canonical page pair reproduces exactly under the committed symbol map and benchmark cleaning rules;
- matching plaintext file exists for every scored page;
- no published-key mutation;
- at least 100 `LEXICAL_BOUNDARY` events in each physical relation (`SAME_PHYSICAL_LINE` and `CROSS_PHYSICAL_LINE`).

The 100-event threshold is fixed before full-corpus alignment output. It is a support floor only, not an effect-size choice.

If either physical relation has fewer than 100 aligned lexical boundaries, Stage 1 lexical-boundary scoring is `INDETERMINATE_INSUFFICIENT_SUPPORT`; do not weaken alignment or add fuzzy matching.

## Reserved Stage 1

Only after the complete Stage-0 alignment output and its SHA are committed may a separate scorer be frozen.

Stage 1 primary will use **only `LEXICAL_BOUNDARY` events** and the same Issue #181 folds, alpha, terminal/initial factor definition and sign-stability rule, separately for same-line and cross-line physical relations.

A key-relabel invariance audit will additionally verify numerical equality between cipher labels and published-key-decrypted labels on an identical frozen key-covered event population.

No Stage-1 score is licensed by this document alone.
