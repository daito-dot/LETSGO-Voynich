# Issue #26E16 — Friderici three-duration × three-note rhythm plaintext probe

Status: **FROZEN BEFORE EXECUTABLE / VOYNICH REVEAL**

Parent research state: E15 report head `d0d704df445e0b2584f38f5afa6c29e3f3c960e4`.

## Purpose

E16 moves to a historical music-cipher mechanism that discards pitch entirely.

Johannes Balthasar Friderici's 1685 *Cryptographia* includes a rhythmic cipher in which plaintext letters are represented by three successive notes and the relevant distinctions are three duration classes (described in modern scholarly sources as whole, half, and quarter notes); pitch is irrelevant. A modern scholarly reproduction labels it the **Friderici Rhythmic Compound Motific Cipher**. The surviving/reproduced chart is arranged as a 3×3 ternary construction over the 24-letter Latin alphabet.

Friderici is much later than the usual Voynich production window. E16 is therefore an **exploratory decoder-family probe only**, not evidence that Friderici's exact construction was available to the Voynich author.

## Frozen historical codebook

Use the project 24-letter normalized Latin alphabet:

`abcdefghiklmnopqrstuwxyz`

Use three ordered duration classes for the historical rhythm alphabet:

- rank 0 = whole note
- rank 1 = half note
- rank 2 = quarter note.

Each plaintext letter is a three-duration motif. Reading the reproduced Friderici chart as a ternary 3×3×3 construction gives the following first 24 patterns in lexicographic ternary order:

```text
A 000   B 001   C 002
D 010   E 011   F 012
G 020   H 021   I 022
K 100   L 101   M 102
N 110   O 111   P 112
Q 120   R 121   S 122
T 200   U 201   W 202
X 210   Y 211   Z 212
```

The remaining three ternary patterns are unassigned:

`220, 221, 222`.

This is consistent with Friderici's related ternary notation principle, in which three groups taking one of three values enumerate the 24-letter alphabet in shifted ternary order.

No plaintext letter, ternary codeword, or unused pattern may be changed after reveal.

## Frozen Voynich candidate family

Under the already adopted Zattera slot grammar, exactly five raw slots have **three states including EMPTY**:

1. slot1: `EMPTY,o,y`
2. slot2: `EMPTY,l,r`
3. slot4: `EMPTY,ch,sh`
4. slot7: `EMPTY,s,d`
5. slot8: `EMPTY,o,a`

All five are prospectively charged as candidates. No three-state slot may be selected after seeing target results.

For a selected slot, every successfully parsed Voynich token emits exactly one raw ternary carrier state.

Unparseable tokens break the carrier stream. Paragraph boundaries break the stream. Physical line boundaries do **not** reset triple grouping inside a paragraph.

Primary parser: `min`.
`max` is sensitivity only and cannot promote a primary failure.

## Frozen key freedom

For each physical-leaf fold, training may choose:

- candidate slot: 5 choices;
- one bijection from its three raw states to historical duration ranks 0/1/2: `3! = 6` choices;
- one global triple phase: 3 choices (`0,1,2` states skipped at the start of every paragraph-level parsed run before grouping into triples).

Total target key family: **90 keys per fold**.

The same slot, permutation, and phase are applied to every paragraph/leaf in the held-out fold after training selection.

Tie order is frozen:

1. lower training invalid-code fraction;
2. lower training medieval-Latin 4-gram CE among uninterrupted valid decoded runs;
3. lower slot index;
4. lower phase;
5. lexicographically smaller raw-state→duration permutation in the slot-state reporting order above.

## Invalid-code handling

Each complete ternary triple is decoded independently.

- code values `0..23` emit the fixed historical letter;
- values `24..26` (`220/221/222`) emit an explicit invalid marker and **break** the decoded Latin scoring run.

Invalid groups count against `valid_group_fraction`. They may not be discarded before the validity diagnostic.

## External Latin model

Reuse frozen CREMMA medieval Latin:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- lowercase ASCII;
- `j→i`, `v→u`;
- unsupported characters break runs.

Use additive-smoothed character 4-grams (`alpha=.1`) over the exact 24-letter E16 alphabet.

Report five-fold CREMMA self-baseline CE and pooled top-five-character fraction.

## Mandatory positive control

Synthetic data cannot identify a Voynich slot label. The mandatory control therefore validates the actual historical ternary decoder only: `3 phases × 3! state permutations = 18 keys`.

For each of five deterministic controls:

1. take normalized CREMMA runs at approximately the E16 decoded-letter volume;
2. encode letters with the exact frozen Friderici ternary table;
3. choose a deterministic hidden ternary-state permutation and hidden phase from seed namespace `Issue26E16:Positive:v1:<control>`;
4. prepend exactly the hidden phase number of deterministic ternary filler states to each synthetic paragraph-like run;
5. expose only the resulting abstract three-state stream;
6. fit all 18 keys on 4/5 synthetic runs;
7. decode untouched 1/5 runs.

PASS requires all:

- exact hidden `(phase, permutation)` recovered in >=4/5 controls;
- mean valid-group fraction >= `.99`;
- mean decoded-letter accuracy >= `.99` on held-out groups;
- mean recovered held-out CE within `.02 bits/char` of true-key held-out CE.

If this fails: **`SOLVER INADEQUATE`** and no Voynich negative inference.

## Held-out diagnostics

For each fold and pooled output record:

- selected slot, phase, and raw-state→duration permutation;
- visible token count, parsed carrier count, parse coverage;
- total ternary groups;
- valid/invalid group counts and fractions;
- held-out 4-gram CE and scored-character count;
- decoded character frequencies and top-five-character fraction;
- first 20 decoded segments length >=12;
- exact CREMMA dictionary substrings length 4..15;
- distinct exact dictionary words length >=6 and folds supporting them;
- top decoded 4-grams and their CREMMA frequencies.

No manual respacing, skipped ternary states, state insertion/deletion, local phase correction, spelling repair, anagramming, or favorable-folio selection.

## Fully refitted order-null family

Generate exactly **200 deterministic nulls**.

For every candidate slot and paragraph-level parsed carrier run independently, shuffle its raw three-state sequence without replacement, preserving exactly:

- the within-run three-state multiset;
- run length;
- paragraph and leaf identity.

Seed namespace:

`Issue26E16:TernaryShuffle:v1:<null>:<slot>:<paragraph_id>:<run_index>`

Every null receives the **complete 90-key search from scratch** in every fold. No real-data selected key is reused.

Primary order-specific statistic: pooled held-out CE among valid decoded runs.

Report:

- lower-tail p = `(1 + # null CE <= real CE) / 201`;
- null median/q05/min;
- real CE advantage below null median;
- null valid-fraction distribution;
- null exact-key-recurrence distribution.

## Frozen practical lead gate

If positive control passes, primary `min` is called **`FRIDERICI RHYTHM PLAINTEXT LEAD`** only if all hold:

1. one exact `(slot, phase, permutation)` recurs in >=4/5 physical-leaf folds;
2. pooled valid-group fraction >= `.95`;
3. pooled held-out CE <= Latin self-baseline + `.50 bits/char`;
4. pooled top-five-character fraction <= Latin self-baseline + `.15` absolute;
5. at least 10 distinct exact CREMMA words length >=6 occur across >=3 held-out folds;
6. refitted order-null lower-tail p <= `.01`;
7. real pooled CE is at least `.10 bits/char` below the refitted-null median.

Otherwise frozen classification: **`NO READABLE FRIDERICI RHYTHM PLAINTEXT`**.

Auxiliary flags:

- `LOW-VALIDITY` if pooled valid-group fraction < `.80`;
- `LOW-DIVERSITY OPTIMUM` if pooled top-five-character fraction >= `.90`.

## Interpretation boundaries

- Friderici 1685 is chronologically late and E16 is exploratory only.
- The three duration classes and triple grouping are historical/model-side.
- The existence of exactly five natural three-state Voynich slots is manuscript-side, but candidate selection across all five is fully charged.
- A stable slot/phase/permutation without absolute readable Latin is not decipherment evidence.
- Do not post-hoc add pitch, variable phases, null notes, state edits, local keys, or alternative ternary codebooks after reveal.
- Friderici's separate triadic/pitch-motif cipher is a different historical mechanism and is not part of E16.
- Do not merge E16 to `main` without explicit user authorization.

## Historical sources used to freeze the mechanism

- Johannes Balthasar Friderici, *Cryptographia* (1685), bibliographic record / digitized original.
- modern scholarly thesis reproduction: Figure 2.25, **Friderici Rhythmic Compound Motific Cipher**;
- modern historical-cryptography description: each letter represented by three notes whose whole/half/quarter duration pattern carries the symbol while pitch is irrelevant;
- independent description of Friderici's ternary three-group alphabet enumerating the 24-letter Latin alphabet.

No Voynich target score was inspected in choosing the historical table or the 90-key target family.
