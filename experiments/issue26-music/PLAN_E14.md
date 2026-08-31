# Issue #26E14 — Kircher 1650 six-instrument × four-count plaintext probe

Status: **FROZEN BEFORE E14 EXECUTABLE / REVEAL**

Base research state: Issue26E8 head `343afac73da2e52b3a75f69e0a43257d54bdf952`.

## Purpose

The H4 exploratory program has already crossed multiple historical music-cipher mechanisms:

- Philip 5×4 pitch/duration;
- Sloane token-internal ~5×5;
- Öttingen sequential two-note 5×5;
- Porta 11×2;
- León/Visigothic monoalphabetic glyph substitution (currently solver-blocked, not negative).

E14 moves to a different family described for Athanasius Kircher's 1650 musical cryptography: six instruments, with one through four successive notes on an instrument encoding four successive alphabet letters, for a 6×4 = 24-letter alphabet. Eric Sams' historical survey describes the rule explicitly: one note on the first instrument means A, two notes B, and so forth; six instruments × up to four notes cover 24 letters. Modern music-cipher surveys repeat the six-instrument/four-note construction.

Kircher 1650 is much later than the usual Voynich production window. E14 is therefore **only an exploratory decoder-family probe**, not evidence that this exact historical construction was available to the Voynich author.

## Why this probe is structurally interesting

Unlike E12, E14 does not require a hypothesis-side k-clustering to manufacture either cardinality.

Under the already adopted Zattera slot grammar:

- slot10 has exactly six raw states: `EMPTY,d,l,r,m,n`;
- exactly two slots have an intrinsically ordinal repeated-unit four-state form:
  - slot6: `EMPTY,e,ee,eee`;
  - slot9: `EMPTY,i,ii,iii`.

These facts pre-exist E14. The 6×4 match is therefore a direct capacity match between a documented music-cipher mechanism and naturally defined Voynich token factors.

Important limitation: the historical values are “1,2,3,4 notes,” while the Voynich repeated-unit states are `EMPTY,1,2,3` visible units. E14 maps their **ordinal ranks** 0..3 to historical count classes 1..4. This is a normalization for the decoder probe, not a claim that Voynich EMPTY literally means one performed note.

## Frozen historical plaintext table

Use the standard 24-letter early-modern Latin alphabet after the same project normalization `j→i`, `v→u`:

`abcdefghiklmnopqrstuwxyz`

The six historical instrument blocks, four count classes each, are frozen row-major as:

```text
instrument 0: a b c d
instrument 1: e f g h
instrument 2: i k l m
instrument 3: n o p q
instrument 4: r s t u
instrument 5: w x y z
```

Columns correspond to historical count `1,2,3,4`.

No plaintext letter, block, or count order may be changed after reveal.

## Frozen Voynich representation

Input and parser are unchanged from Issue26E:

- ZL3b mirror `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`;
- expected ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- adopted deterministic Zattera slot parser.

Primary parser: `min`.
`max` is sensitivity only.

### Instrument factor

Always slot10. Raw-state order for reporting only:

`EMPTY,d,l,r,m,n`.

No alternative six-state slot exists under the adopted grammar.

### Count factor

Primary candidate set is frozen to exactly two slots:

1. slot6 `EMPTY,e,ee,eee`;
2. slot9 `EMPTY,i,ii,iii`.

These are selected because their nonempty states are literal repetitions of one unit and therefore define an external-to-E14 ordinal 0/1/2/3 multiplicity structure. Other four-state slots such as slot0 are **not** eligible because they are categorical rather than repeated-unit ordinal states.

Primary count mapping is fixed by ordinal rank:

- `EMPTY → historical count 1`;
- singleton → count 2;
- double → count 3;
- triple → count 4.

No arbitrary 4! count-state permutation is searched in the primary analysis.

A single preregistered sensitivity may reverse the entire ordinal axis (`EMPTY→4`, triple→1), but may not use arbitrary nonmonotone count permutations.

## Frozen training freedom

For each five-fold physical-leaf split, primary training may choose only:

- count slot: slot6 or slot9 (2 choices);
- a bijection from the six slot10 states to the six historical instrument rows (`6! = 720`).

Total primary keys/fold: **1,440**.

The count-column order is fixed.

Key selection uses the external medieval-Latin character 4-gram model on the 4/5 training leaves only. Ties:

1. lower training cross-entropy;
2. slot6 before slot9;
3. lexicographic instrument permutation.

After selection, the count slot and six-state permutation are frozen and applied to untouched held-out leaves.

## External Latin model

Reuse frozen CREMMA medieval Latin:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- lowercase ASCII;
- `j→i`, `v→u`;
- unsupported letters/nonletters break runs for 4-gram scoring.

Use additive-smoothed character 4-grams (`alpha=.1`) over the exact 24-letter E14 alphabet.

Compute and report five-fold CREMMA self-baseline CE and top-five-character fraction.

## Token-to-plaintext rule

Each successfully parsed Voynich token yields exactly one E14 plaintext character:

1. read its slot10 state;
2. read its selected slot6 or slot9 ordinal state;
3. map slot10 through the frozen instrument permutation;
4. map ordinal rank 0..3 to historical count column 1..4;
5. emit the corresponding table letter.

Unparseable tokens and physical line boundaries break decoded streams. No plaintext word boundaries are inferred from Voynich token boundaries.

## Held-out diagnostics

For each fold and pooled held-out output record:

- selected count slot and instrument permutation;
- training and held-out 4-gram CE;
- scored-character count and parse coverage;
- decoded character frequencies and top-five-character fraction;
- first 20 decoded physical-line streams length >=12;
- every exact CREMMA dictionary substring of decoded length 4..15, without skipping/reordering characters;
- distinct exact dictionary words length >=6 and folds supporting them;
- top decoded 4-grams with CREMMA frequencies.

No manual respacing, skipped characters, spelling repair, anagramming, or favorable-folio selection.

## Mandatory positive control

E14's finite 1,440-key selector must recover a known 6×4 encoding before a Voynich negative is interpretable.

For each of five controls:

1. take frozen supported CREMMA runs at approximately the Voynich eligible-event volume;
2. choose one of the two count-slot labels deterministically only as an abstract model label;
3. encrypt the Latin characters under a deterministic hidden six-instrument permutation, preserving the historical count columns exactly;
4. expose only the resulting six-state-row + four-state-column events to the identical 1,440-key selector;
5. evaluate a held-out fifth.

Positive-control PASS requires:

- hidden count-slot label recovered in >=4/5 controls;
- exact hidden six-row permutation recovered in >=4/5 controls;
- mean occurrence-weighted decoded-letter accuracy >=.99;
- recovered held-out CE within .02 bits/char of true-key held-out CE.

If this fails: `SOLVER INADEQUATE` and no Voynich negative inference.

## Frozen practical lead gate

If positive control passes, primary `min` is called **`KIRCHER 6X4 PLAINTEXT LEAD`** only if all hold:

1. one exact `(count_slot, instrument_permutation)` recurs in >=4/5 physical-leaf folds;
2. mean held-out CE <= Latin self-baseline + `.50 bits/char`;
3. pooled top-five-character fraction <= Latin self-baseline + `.15` absolute;
4. at least 10 distinct exact CREMMA words length >=6 occur across at least 3 held-out folds.

Otherwise frozen classification: **`NO READABLE KIRCHER 6X4 PLAINTEXT`**.

Flag **`LOW-DIVERSITY OPTIMUM`** separately if pooled top-five-character fraction >=.90.

## Ordinal-reversal sensitivity

After the primary result is emitted, run the identical procedure with only one extra freedom: count direction may be ascending or globally reversed. This doubles the key space to 2,880/fold.

The reversal sensitivity cannot promote a primary failure to a confirmatory result. It is descriptive only.

## Interpretation boundaries

- E14 is exploratory and anachronistic relative to usual Voynich dating.
- The independently interesting fact is the natural `6 × repeated-unit-4` capacity match; this alone is not evidence of music.
- Do not use arbitrary four-state categorical slots.
- Do not search arbitrary 4! count permutations after reveal.
- Do not reinterpret EMPTY as a literal sounding note; it is only ordinal class 0 normalized to historical count 1.
- Do not promote a stable key without absolute held-out language/readability evidence.
- Do not merge E14 to main without explicit user authorization.
