# Issue #194 — Ramanacoil complete-preservation R5 source-attribution Gate 0

Date: 2026-09-08  
Parent: #172  
Base main at branch creation: `ff527a3f4562e8591a460a6f6dc9593913ffadfb`  
Status: **FROZEN BEFORE PAYLOAD INSPECTION / SCORE-FREE**

## Purpose

Determine whether DECODE Record 1564 (Ramanacoil, 1674) preserves enough externally defined structure to support the clean R5 source-attribution experiment required by the near-term roadmap.

This Gate 0 does **not** compute any R5 gain, transition likelihood, Voynich statistic, candidate score, or effect direction.

## Prior external authority

Before downloading the current DECODE text payloads, the external record and HistoCrypt 2021 paper establish only the following admissible prior facts:

- DECODE Record 1564 is public, decrypted, 46 pages, and exposes a transcription, a CT2 key, and deciphered text;
- the record describes the cipher as a substitution system using graphical signs;
- the HistoCrypt paper states that the transcription team manually transcribed all pages and assigned each ciphertext symbol a transcription word;
- the paper explicitly recommends ending every transcribed ciphertext line with a hard return so CT2 output preserves line-by-line comparison;
- the paper describes the key as containing graphical signs for alphabetic letters, five double-letter values, and seven word-level nomenclature elements, with only two of the latter observed in the ciphertext;
- CT2 nomenclature syntax is independently documented in the form `[PLAINTEXT];[CIPHER1|CIPHER2|...]`.

These facts motivate, but do not decide, composability.

## Frozen source URLs

Record page:

`https://de-crypt.org/decrypt-web/RecordsView/1564`

The current document links exposed by that record before payload inspection are frozen as:

- transcription: `https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_1564_2026-Feb-20-08-49-57_21421.txt`
- key_CT2: `https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_1564_2026-Feb-20-08-50-13_65682.txt`
- decryption_CT2: `https://de-crypt.org/decrypt-custom/filesrv/?file=DOC_1564_2026-Feb-20-08-50-33_79896.txt`

Gate 0 downloads each URL twice in the same Actions run and requires byte-for-byte identity between the two copies. The first copy is the audited authority. SHA-256, byte size, line count, and newline convention are archived.

No alternate DECODE version, cached mirror, Wayback replay, or filename repair is licensed after reveal.

## Required layers

A future clean R5 attribution scorer is licensed only if all five layers are externally preserved:

1. `CIPHERTEXT_SYMBOLS`
2. `PHYSICAL_LINES`
3. `CIPHER_UNIT_BOUNDARIES`
4. `PLAINTEXT_LEXICAL_BOUNDARIES`
5. `CIPHER_PLAINTEXT_ALIGNMENT`

The critical distinction is between **cipher atoms** and **cipher units**. Because the HistoCrypt paper says every ciphertext symbol was assigned a transcription word, ordinary single whitespace between transcription words is frozen as atom separation only. It may not be reinterpreted as a word/group boundary.

## Frozen parsing and tests

### 1. Text decoding

- Accept UTF-8 with optional BOM; if strict UTF-8 fails, classification is `NON_COMPOSABLE_OTHER`.
- Preserve original CR/LF bytes for the newline audit; structural parsing normalizes CRLF/CR to LF only after the audit.
- A physical transcription line is one normalized source line, not a wrapped display line.

### 2. CT2 key parser

Parse only non-empty lines matching exactly the CT2 nomenclature shape:

`[PLAINTEXT];[CIPHER_ALTERNATIVES]`

where `CIPHER_ALTERNATIVES` is split on literal `|`. Strip outer bracket syntax only; preserve the interior strings exactly except for surrounding whitespace.

If the same cipher token maps to conflicting plaintext values, alignment is not deterministic.

Metadata mappings whose plaintext side begins with `DC` and whose cipher side is numeric are recorded as page/image-marker mappings and excluded from linguistic alignment.

### 3. Transcription atoms

For every non-empty transcription line:

- preserve the raw line;
- split candidate atoms on one-or-more horizontal whitespace;
- metadata/page-marker tokens recognized by the frozen CT2 metadata mapping are not cipher atoms;
- every remaining token is a candidate ciphertext atom.

`CIPHERTEXT_SYMBOLS = true` iff:

- at least 1,000 non-metadata candidate atom occurrences exist;
- at least 20 distinct candidate atoms exist; and
- at least 95% of candidate atom occurrences are present on the cipher side of the supplied CT2 key.

The 95% gate tolerates explicitly documented inline cleartext / punctuation / one-off transcription material without repairing it.

### 4. Physical lines

`PHYSICAL_LINES = true` iff:

- transcription contains at least 100 non-empty lines carrying at least one admitted cipher atom;
- at least 80% of such lines contain at least five admitted cipher atoms; and
- the supplied decryption contains at least 100 non-empty content lines.

This tests preserved hard-return lineation, not correctness of physical line recognition from manuscript images. Images are external corroboration only and are not manually segmented in Gate 0.

### 5. Independent cipher-unit boundaries

Ordinary single spaces used to separate candidate atom tokens are **not** unit boundaries.

The only prospectively admitted independent group-boundary channels are:

1. a literal standalone delimiter token exactly one of `|`, `||`, `/`, `//`, `<SPACE>`, `[SPACE]`, `<WORD>`, `[WORD]`, `WORDSEP`, `WordSeparator`, `SPACE`;
2. a tab character occurring between non-empty atom-bearing fields on one physical line;
3. a run of at least two ASCII spaces occurring between non-empty atom-bearing fields on one physical line;
4. a supplied CT2 key mapping whose plaintext side is exactly one of ` `, `<SPACE>`, `[SPACE]`, `<WORD>`, `[WORD]`, `SPACE`, `WordSeparator`, `WORDSEP`, provided its cipher-side token occurs in transcription;
5. another explicit boundary marker only if it is already self-identifying in the payload by a literal label containing `wordsep`, `word_separator`, or `wordboundary` case-insensitively.

Page/image markers and hard returns are not cipher-unit boundaries.

`CIPHER_UNIT_BOUNDARIES = true` iff at least 100 within-line boundary events from one or more admitted channels are observed and at least 20 physical lines contain one. Otherwise it is false.

No boundary may be inferred from token frequency, plaintext output, dictionary matches, morphology, edit distance, symbol shape, visual spacing in images, or R5 behavior.

### 6. Plaintext lexical boundaries

The decryption is treated as supplied CT2 output, not as a language-corrected text.

A decryption content line is a non-empty line that is not an obvious DECODE/page marker as identified by the frozen metadata mappings.

`PLAINTEXT_LEXICAL_BOUNDARIES = true` iff:

- at least 100 content lines exist;
- at least 100 content lines contain two or more runs of alphabetic characters separated by one-or-more whitespace characters; and
- at least 500 such whitespace-separated alphabetic tokens exist in total.

This is deliberately conservative: punctuation does not create lexical boundaries by itself and no Dutch tokenizer/dictionary is used.

### 7. Cipher/plaintext alignment

Build the deterministic atom->plaintext map from the CT2 key. For each transcription physical line, replace each key-covered non-metadata atom with its exact plaintext-side value and concatenate outputs in atom order. Do not insert spaces unless a key mapping itself outputs a frozen explicit space/boundary value.

Normalize only for the mechanical comparison:

- Unicode NFC;
- convert CRLF/CR to LF;
- trim leading/trailing horizontal whitespace per line;
- collapse runs of horizontal whitespace to one ASCII space;
- compare case-sensitively first and case-insensitively as a separately reported diagnostic;
- do not remove punctuation, accents, brackets, digits, or alphabetic characters.

Because page/image marker mappings may insert navigation text into CT2 output, alignment is evaluated in two prospectively defined forms:

- `STRICT_LINE_ALIGNMENT`: corresponding non-marker transcription and decryption content lines have exact normalized equality after key expansion;
- `SEQUENTIAL_STREAM_ALIGNMENT`: concatenate normalized non-marker lines on each side with `\n` and require exact equality.

`CIPHER_PLAINTEXT_ALIGNMENT = true` iff either exact form covers at least 95% of key-covered cipher-atom occurrences and no conflicting key mapping exists. Coverage is computed only over deterministic key-covered atoms; unknown atoms remain explicit failures and are not deleted to improve matching.

If the decryption transport includes CT2 annotations that make exact comparison impossible, Gate 0 reports that fact and alignment remains false. No ad-hoc annotation stripping is licensed.

## Structural sample firewall

The machine result may archive, for representation audit only:

- first three and last three non-empty raw lines of each payload, escaped and truncated to 240 characters;
- top 30 transcription token frequencies;
- parsed key-entry counts and up to 20 mapping examples sorted lexicographically;
- counts of each admitted boundary channel;
- line/token support and alignment coverage.

It must not print or archive any R5 score or Voynich-derived statistic.

## Frozen classification precedence

1. if any of the three URLs fails double-download byte identity: `AUTHORITY_UNAVAILABLE_OR_UNSTABLE`;
2. if all five required layers are true: `COMPOSABLE_FOR_CLEAN_R5_ATTRIBUTION`;
3. if layers 1,2,4,5 are true but layer 3 is false: `PHYSICAL_LINES_AND_ALIGNMENT_PRESENT_BUT_NO_CIPHER_UNIT_BOUNDARIES`;
4. if layer 3 is true but layer 4 or 5 is false: `PLAINTEXT_OR_ALIGNMENT_NOT_PRESERVED`;
5. otherwise: `NON_COMPOSABLE_OTHER`.

Only `COMPOSABLE_FOR_CLEAN_R5_ATTRIBUTION` licenses Stage 1.

## Stop rules

A non-composable result stops Ramanacoil for Priority 3. No reinterpretation of ordinary atom spaces, image-derived manual grouping, alternate whitespace threshold, Dutch-language repair, page subsetting, post-reveal key modification, or source-version substitution is licensed.
