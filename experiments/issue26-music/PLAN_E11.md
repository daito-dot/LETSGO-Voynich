# Issue #26E11 — Öttingen-Wallerstein sequential-dyad music-cipher probe

Status: **FROZEN BEFORE E11 EXECUTABLE / REVEAL**

Parent research state: Issue26E8 branch at `343afac73da2e52b3a75f69e0a43257d54bdf952`.

E11 is an exploratory practical-decoding probe. It does not revise the negative confirmatory conclusions of E7/E8, and it is deliberately a sibling of E9/E10 rather than a rescue of either fitted key.

## Why this mechanism is different

E10 mapped two five-state dimensions **inside one Voynich token** onto a 5×5 historical table. Its 4/5 fitted-key recurrence collapsed because the dominant EMPTY×EMPTY cell was mapped to the multi-character Sloane abbreviation `con`.

Öttingen-Wallerstein's ca.1600 musical steganography uses a structurally different mechanism:

> **two successive notes → one plaintext letter**

Each note is one of five solmisation tones. Order matters: `ut,re` and `re,ut` are different code pairs. This makes E11 a sequential dyad decoder rather than another token-internal 5×5 product.

The system is later than the usual Voynich dating window. E11 therefore tests a known historical mechanism as an exploratory decoder / structural analogue, **not** historical availability to the Voynich author.

## Historical key frozen from the manuscript transcript

Primary source/transcript:

- Herzog August Bibliothek Wolfenbüttel, *Steganographia comitis Friderici Öttingensis in Wallerstein*, Cod. Guelf. 56 Aug. 4°, especially fols. 98v–103v.
- Digital transcript: `https://diglib.hab.de/content.php?dir=edoc/ed000213&distype=optional&xml=briefe/240319.xml&xsl=tei-transcript.xsl`

The transcript explicitly states that only five of the six solmisation notes are used (`ut re mi fa sol`) and that every two notes have an angel name. The first note is indexed beside the table and the second above it. The editorial note strips the angelic names to their third letters and gives the exact plaintext key.

Frozen row order = **first note**:

`ut, sol, fa, mi, re`

Frozen column order = **second note**:

`ut, fa, sol, mi, re`

Frozen matrix:

| first \\ second | ut | fa | sol | mi | re |
|---|---|---|---|---|---|
| ut  | Q | R | S | T | U |
| sol | W | X | Y | Z | — |
| fa  | A | B | C | D | E |
| mi  | L | M | N | O | P |
| re  | F | G | H | I | K |

The `sol,re` cell is historically unused: the editorial note calls it a `Leerstelle` because the alphabet contains 24 letters. It is **not** silently converted into space or another letter.

Historical plaintext alphabet:

`ABCDEFGHIKLMNOPQRSTUWXYZ`

`J` and `V` are absent. External Latin normalization therefore uses `j→i` and `v→u`, matching earlier E8–E10 normalization.

## Voynich representation

Reuse the unchanged Zattera slot parser and frozen ZL3b transcription/input used by E8–E10.

Primary parser: `min`.

Sensitivity parser: `max`.

Exactly two natural adopted slots have five raw states including EMPTY:

- slot3: `EMPTY,t,k,p,f`
- slot5: `EMPTY,cth,ckh,cph,cfh`

A selected slot supplies **one five-state note per parsed Voynich token**.

No other slot, learned clustering, token-internal second coordinate, or Guidonian mapping is permitted in E11.

## Sequential pairing

Primary pairing rule:

1. process each physical transcription line independently;
2. an unparseable token terminates the current note run;
3. within each run, pair notes non-overlapping from the first note: `(0,1), (2,3), ...`;
4. decode each pair with the fixed historical table;
5. if a pair lands on the historical blank `sol,re`, record an **illegal dyad** and break the plaintext n-gram stream at that position; do not drop it silently or reinterpret it as a space.

The final unpaired note of an odd-length run is recorded and ignored.

A separately reported **phase-1 sensitivity** pairs `(1,2), (3,4), ...`. Phase is not fit on held-out material and cannot rescue the primary result.

## Finite key search

The historical letter table is fixed.

For each physical-leaf fold, training data may choose only:

- slot3 or slot5 as the five-state note source;
- one of `5! = 120` bijections from that slot's raw states to the five historical note labels.

Total primary candidates: **240 keys per fold**.

The pairing phase is fixed at 0 for the primary analysis.

### Key-selection objective

Because the historical `sol,re` pair has no plaintext symbol, the optimizer must not exploit it as a deletion channel.

Training keys are ranked lexicographically by:

1. **lower illegal-dyad rate**;
2. then lower medieval-Latin 4-gram cross-entropy;
3. ties: lower slot number, then lexicographic permutation.

The selected key is frozen and applied untouched to the held-out physical leaves.

## External medieval-Latin language model

Reuse the frozen CREMMA population from E8–E10:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- lowercase ASCII;
- `j→i`, `v→u`.

Alphabet = the 24 historical E11 letters.

Build the same additive-smoothed character 4-gram model (`alpha=0.1`). Lower mean negative log2 probability per scored character is more Latin-like.

Compute the same five-fold CREMMA self-prediction baseline so E11 has an absolute scale for genuine held-out medieval Latin.

## Held-out diagnostics

For every fold record:

- selected slot and state→note permutation;
- training illegal-dyad rate and CE;
- held-out illegal-dyad rate;
- held-out CE;
- number of raw note runs, decoded dyads, illegal dyads and scored characters;
- sample untouched plaintext streams;
- character frequency / top-five-character fraction;
- distinct exact CREMMA lexicon hits of length >=6;
- longest exact lexicon hit;
- most frequent decoded tetragrams and their CREMMA counts.

Also report exact full-key recurrence across five folds.

## Sequence-order control

E11 must distinguish a frequency-compatible substitution from actual plaintext-like order.

After all five held-out folds are decoded with their training-selected keys, pool the held-out plaintext streams and create exactly **1,000 deterministic within-stream shuffles**.

Each shuffle preserves:

- every decoded character;
- every stream length;
- fold-specific selected mappings;
- illegal-dyad break locations;
- total unigram distribution.

Only character order inside each valid plaintext stream is randomized.

Seed family: `Issue26E11:HeldStreamShuffle:v1`.

Primary sequence-order p-value:

`p = (1 + #{shuffle CE <= observed CE}) / 1001`.

This asks whether the untouched Voynich order, after the fitted historical decoder, is more Latin-like than the same decoded symbol inventory in random order.

## Frozen lead classification

### `DYADIC MUSIC-CIPHER PLAINTEXT LEAD`

Only if primary `min`, phase 0 satisfies **all**:

1. exact `(slot, state→note permutation)` recurrence in >=4/5 folds;
2. pooled held-out CE is no more than **0.50 bits/char above** the frozen CREMMA self-baseline;
3. within-stream shuffle lower-tail `p <= .001`;
4. pooled held-out illegal-dyad rate <= **1%**;
5. pooled top-five-character fraction <= **80%**;
6. at least **5 distinct** exact CREMMA lexicon hits of length >=6, including at least one length >=8.

This is an exploratory lead threshold, not a decipherment claim.

### `ORDERED BUT NOT READABLE`

If shuffle `p <= .01` but any absolute-readability / recurrence / legality gate above fails.

### `NO ÖTTINGEN PLAINTEXT SIGNAL`

If observed held-out order is not unusually Latin-like (`p > .01`) or the output is plainly collapse-dominated / illegal-code dominated.

## Sensitivities

After the frozen primary result only:

- parser `max` with the same phase-0 protocol;
- phase-1 pairing under `min` and `max`, with the same 240-key training search.

No best-of-phase promotion is allowed.

## Boundaries

- E11 is a practical decoder probe, not evidence that this ca.1600 scheme existed during Voynich production.
- Do not reuse E10's 4/5 slot3×slot5 fitted key.
- Do not use token-internal slot3×slot5 products in E11.
- Do not convert the historical blank cell into a plaintext symbol, word boundary, or deletion.
- Do not inspect held-out text to choose slot, permutation, phase, parser, line grouping, or language.
- Do not manually insert spaces, anagram, Caesar-shift, synonym-substitute, or selectively report favorable folios.
- A visually suggestive short fragment is descriptive only; the frozen held-out diagnostics govern classification.
- Keep E11 on its own research branch and do not merge to `main` without explicit user authorization.
