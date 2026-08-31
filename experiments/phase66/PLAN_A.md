# Phase 66A — direct-music screen: cadence and motif structure

Status: **FROZEN BEFORE SCIENTIFIC REVEAL**

Issue: #26

## Question

Does Voynich running text, after a sequence-blind seven-state reduction based only on token-internal form, show phrase-ending concentration and short motif recurrence closer to medieval plainchant than to structured medieval Latin prose?

This is a direct-music hypothesis test. It is separate from Issue #25, which only borrows music-analysis methods without proposing musical content.

A positive result would not identify notes or melodies. A negative result would weaken the simplest direct monophonic / finite musical-state interpretations.

## Authority and source freeze

Repository scientific base:

- LETSGO-Voynich main: `61cb3905eb88a4cec77e8f6e62fe89bae9d9eda1`
- this plan must exist in branch history before any Phase66A scientific output is computed.

Voynich source:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- expected git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- use the existing Phase62 paragraph parser semantics: paragraph loci only (`P`), `<%>` starts, visible alphabetic EVA runs as tokens.

Latin comparator:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`
- primary equal-weight manuscripts exactly as Phase62: `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`.
- use physical transcription lines inside pilcrow-delimited items; no semantic sentence reconstruction.

Plainchant comparator:

- `bacor/ISMIR2020@ab3edb742a718fe5c3fd40550c54f104fe9b6078`
- file: `data/run-0/antiphon/subset/test-chants.csv`
- expected git blob SHA-1: `616fcd986226873cb1f58b8711c1936ad0794af4`
- use only rows with a non-empty `volpiano` field.
- this file is a frozen research dataset derived from CantusCorpus; do not redistribute it in LETSGO-Voynich.

The chant corpus is CC BY-NC-SA 4.0; Phase66A stores only aggregate derived statistics and source identity, not the source CSV.

## Primary population and boundaries

### Voynich

Primary sequence unit = each running-text line with at least 5 tokens, inside parsed paragraphs.

Use the existing five physical-leaf folds from Phase62. For each outer fold:

- fit the seven-state form reduction on token **types from training leaves only**;
- assign states to held-out tokens without using sequence position or neighbors;
- compute scientific metrics only on held-out lines.

### Latin

Primary sequence unit = each physical transcription line with at least 5 words inside the four fixed manuscripts.

Fit one seven-state form reduction on the union of word types from the four primary manuscripts. Report each manuscript separately and their equal-weight mean.

### Plainchant

Parse Volpiano strings directly.

Pitch symbols are the ordered Volpiano basic pitch alphabet:

`89abcdefghijklmnopqrs`

Normalize alphabetic pitch symbols to lowercase. Ignore non-pitch symbols except phrase delimiters.

Phrase delimiters are Volpiano barline codes `3`, `4`, `5`. Split each chant at those codes. Retain phrases containing at least 5 pitch events.

Map the 21 ordered pitch symbols to seven diatonic pitch classes by `pitch_index mod 7`. This preserves register-independent diatonic class while using no Voynich information.

## Seven-state form reduction for Voynich and Latin

The reduction must be sequence-blind: state assignment may use token spelling/form only, never token order, line position, paragraph position, neighboring tokens, manuscript section, or target music metrics.

### Token feature vector

Normalize each token to lowercase ASCII letters `a-z`; Latin diacritics are NFKD-folded and combining marks removed.

For each token type create the following generic vector:

1. token length;
2. normalized counts of each of 26 letters;
3. one-hot first letter over 26 letters;
4. one-hot last letter over 26 letters.

Total dimension = 79.

### Fit

- fit on unique training token types, unweighted by occurrence;
- standardize each feature with training-type mean and SD; zero SD becomes 1;
- deterministic 7-means clustering;
- initialization: first centroid = lexicographically smallest normalized token; subsequent centroids = type maximizing distance to nearest existing centroid, ties lexicographically;
- Euclidean distance;
- Lloyd updates until assignments stop changing or 100 iterations;
- empty cluster: replace centroid with the type farthest from its assigned centroid, ties lexicographically;
- cluster labels themselves have no interpretation.

Held-out or evaluation token types are assigned to nearest frozen centroid; ties use smallest centroid index.

No alternative clustering, `k`, feature set, weighting or initialization may be selected after reveal.

## Primary metrics

All metrics are invariant to a global permutation of state labels.

For each evaluated corpus/fold, let each retained line/phrase be a state sequence of length >=5.

### M1 — final-state concentration excess

Observed final collision probability:

`CP_final = sum_s p_final(s)^2`

Body collision probability uses every non-final position pooled across sequences:

`CP_body = sum_s p_body(s)^2`

`M1 = CP_final - CP_body`

Positive values indicate convergence onto fewer terminal states than body states.

### M2 — final-transition concentration excess

For each sequence, take the final ordered state pair `(x[-2], x[-1])`.

`CP_final2 = sum_pair p_final2(pair)^2`

Body pair collision probability uses all ordered adjacent pairs except the final pair of each sequence.

`M2 = CP_final2 - CP_body2`

Positive values indicate a restricted cadence-like transition inventory.

### M3 — repeated 3-state motif mass

Pool all contiguous state 3-grams **within each document/item**, never crossing a line/phrase boundary.

For each document/item separately, define repeated mass as:

`sum_g max(count(g)-1, 0) / total_3grams`

Then average across eligible documents/items weighted by their total 3-gram count.

For Voynich, document/item = paragraph. For Latin, item = pilcrow-delimited item. For chant, item = chant.

### M4 — repeated 4-state motif mass

Same as M3 using contiguous 4-grams.

## Order-preserving null / effect normalization

For every corpus evaluation, compute 500 deterministic within-sequence shuffles.

Each replicate independently permutes states **inside each retained line/phrase**, preserving:

- number of sequences;
- every sequence length;
- each sequence's state multiset;
- global state frequencies;
- document/item grouping.

This destroys terminal placement and local order while preserving state composition.

Seeds are SHA-256-derived from exact corpus/fold label plus replicate index.

For each metric report:

- observed value;
- null mean;
- null SD;
- `Z = (observed-null_mean)/null_SD` when SD > 0;
- empirical two-sided `p = (1 + #(|null-mean| >= |observed-mean|)) / 501`.

Primary cross-corpus comparison uses the four-dimensional Z vector `(Z_M1..Z_M4)`.

## Primary reference vectors

- `CHANT` = one vector from all eligible frozen antiphon test-subset phrases.
- `LATIN` = equal-weight arithmetic mean of the four manuscript Z vectors.
- `VOYNICH_i` = held-out vector for each of five physical-leaf folds.

For each Voynich fold compute Euclidean distances:

- `D_music_i = ||VOYNICH_i - CHANT||_2`
- `D_latin_i = ||VOYNICH_i - LATIN||_2`

No feature weighting.

## Frozen classification

### DIRECT-MUSIC SCREEN POSITIVE

Require all of:

1. `D_music_i < D_latin_i` in at least 4/5 Voynich folds;
2. mean `D_music` < mean `D_latin`;
3. Voynich mean M1 Z and mean M2 Z have the same sign as chant M1 Z and M2 Z respectively;
4. at least one of M1 or M2 has absolute mean Voynich-vs-chant Z difference smaller than Voynich-vs-Latin difference.

### DIRECT-MUSIC SCREEN NEGATIVE

If condition 1 fails (fewer than 4/5 music-distance wins), classify the simple seven-state direct-music screen as negative.

### MIXED

Otherwise classify mixed.

The result applies only to this frozen reduction and these four diagnostics. It does not exclude all musical encodings.

## Sensitivities

Predeclared descriptive sensitivities only; they cannot rescue the primary classification:

1. Voynich paragraph-final lines only vs all retained lines.
2. Chant barline `4` phrase endings only, if at least 100 eligible phrases remain.
3. `k=6` form clustering for Voynich/Latin and pitch class modulo 6 for chant, reported only as a historical-solmization sensitivity.

No `k=12` sensitivity in Phase66A. Chromatic mapping requires a separate rationale.

## Falsification and interpretation rules

A positive screen permits only:

> Under a frozen sequence-blind seven-state form reduction, Voynich line sequences show cadence/motif effect geometry closer to the tested medieval plainchant comparator than to the tested structured medieval Latin comparator.

It does not justify mapping EVA glyphs/tokens to notes.

A negative screen supports only:

> The simplest morphology-to-seven-state direct-music model does not make Voynich sequence effects more chant-like than Latin under the frozen diagnostics.

Do not tune state definitions, cadence metrics, phrase segmentation, corpus subset or distance weighting after reveal and call it Phase66A.
