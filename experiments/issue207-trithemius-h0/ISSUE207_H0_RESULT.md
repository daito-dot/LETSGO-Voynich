# Issue #207 — Trithemius `Polygraphia` sequential word-alphabet H0

Parent: #172  
Candidate: `TP1518-WA0`  
Stage: external H0 authority preflight  
Target access: **none**

## Decision

**`H0_ARCHITECTURE_RECOVERED`**

The historically documented core is sufficiently specified to implement a bounded, first-pass encoder and deterministic inverse without using Voynich behavior to fill missing rules.

This is materially different from T1463 (#183): the crucial encoder-choice rule is actually stated.

## What the source fixes

The 1518 *Clavis Polygraphiae* explains the first book as more than 9,000 Latin words arranged under almost 400 alphabets. Each code-bearing word represents the letter written at its head. The writer takes one word from alphabet 1 for the first secret letter, one from alphabet 2 for the next, and continues through the alphabets without skipping one.

The same source then gives the operational cautions:

- do not take more than one code-bearing word from one alphabet at a time;
- do not skip an alphabet;
- a long hidden message may begin again from the head, and continuation from Book I into Book II is also allowed;
- words placed outside the alphabetical sequence designate no hidden letter and exist to complete the public Latin discourse;
- the receiver examines each word against the alphabets, writes down the represented letters, and concatenates them into the hidden letter stream;
- duplicate/missing words inside one alphabet are explicitly treated as copy errors because they confuse decoding.

Source witness frozen for this audit:

- Johannes Trithemius, *Clavis Polygraphiae*, Basel 1518, HAB witness;
- Trithemius Corpus reading/navigation layer at commit `0e38a37671a5e3b5decd11c19fe82de79883cae7`;
- metadata: `works/prdl-70282_clavis-polygraphiae-ioannis-trithemii-abbatis-diui/metadata.json`;
- relevant reading chunks: `full_chunk_0108.md` through `full_chunk_0111.md`.

The scan remains the primary witness. The modern reading text is not authority for silently repairing damaged table cells.

## Independent historical cross-check

John Falconer, *Cryptomenysis Patefacta* (1685), independently describes Trithemius's ordered-alphabet use and reproduces complete initial alphabets. Frozen transcription:

- repository: `uwgraphics/VEP2_TCP_SimpleText`
- commit: `7f17f7ab87560c8ea24a82d35789a11fd7e03e53`
- path: `A4/A40781.txt`

Three consecutive complete alphabets are frozen in `issue207_h0_result.json`. This is enough for a deliberately bounded external round-trip test without reconstructing hundreds of table rows.

## Exact recoverability level

The strict core recovers the **24-letter Roman letter stream**, not the lexical formatting of the hidden message.

Frozen inventory set:

`a b c d e f g h i k l m n o p q r s t v w x y z`

`j` and `u` are not distinct table letters. Table labels, rather than a modern alphabet ordering assumption, control lookup.

A doubled plaintext letter is simply two successive secret-letter positions and therefore uses two successive alphabets.

Hidden spaces and punctuation are not encoded by the word-alphabet stream. The receiver recovers letters and must group them into words afterward. The recoverability claim is therefore:

**`EXACT_ROMAN_LETTER_STREAM_WITH_TABLE_AND_POSITION; NO_HIDDEN_LEXICAL_BOUNDARY_RECOVERY`**

## Filler and restart do not reopen the H0 ambiguity

The historical overt prose is not globally deterministic. The source permits table-external connective words and gives more than one long-message continuation strategy.

That does not block a bounded H0 architecture result because:

1. the source explicitly says the table-external words designate no letter and do not serve the hidden narrative;
2. the next preflight is restricted to the code-bearing stream;
3. it stops before the end of the frozen consecutive prefix, so no restart choice is exercised;
4. no filler word is selected, optimized or scored.

We therefore do **not** claim that the whole historical Latin cover sentence has a unique deterministic realization. We claim only that the bounded code-bearing transform and its inverse are specified.

## R10 accounting

The large historical codebook is external to the Voynich target, but it is not automatically free side information.

Any executable candidate must charge:

- the exact serialized table cells it uses;
- source/edition identity and frozen hash;
- start alphabet if not the documented first one;
- book/mode identity;
- the 24-letter normalization rule;
- restart/termination policy;
- filler treatment;
- any private table permutation/transposition.

For the next H1 preflight, the exact three-alphabet prefix must be serialized and hashed and its byte/bit size reported. A later target tournament is not licensed until any larger table actually used has been source-verified, frozen and charged.

## H1 license

A single **external-only** bounded round-trip is licensed now.

Current limit: **3 code-bearing positions**, because only the three independently cross-checked consecutive alphabets are frozen for executable use in this result.

Prohibited in H1:

- Voynich access or scoring;
- cycling the three-table excerpt;
- adding/selecting filler for stylistic resemblance;
- repairing a table from a Latin dictionary or language model;
- target-vocabulary lookup.

Pass condition: encode a frozen 24-letter input of at most three positions using alphabets 1→2→3, invert it using the same positional tables, and recover the input exactly.

## Program consequence

Priority 4 has found a historical multi-glyph reversible architecture whose core choice rule is externally documented. That makes it a better-specified candidate than T1463.

It does **not** yet make Trithemius a Voynich candidate. The immediate next step is only the tiny external H1 round-trip. After that, the project should explicitly decide whether digitizing enough of the historical table for a meaningful target-blind generator is worth the added complexity before exposing the mechanism to Voynich statistics.
