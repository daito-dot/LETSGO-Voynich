# Issue #26E15 — Bacon biliteral two-difference musical-carrier probe

Status: **FROZEN BEFORE EXECUTABLE / VOYNICH REVEAL**

Base research state: Issue26E8 head `343afac73da2e52b3a75f69e0a43257d54bdf952`.

## Purpose

The practical music-cipher branch has already crossed several structurally different families: Philip 5×4 pitch/duration, Sloane token-internal ~5×5, Öttingen successive two-note 5×5, Porta 11×2, León visible-sign monoalphabetic substitution, and Kircher 6×4 run-count/instrument coding.

E15 deliberately moves to a **binary sequential carrier** family rather than another pitch table.

Francis Bacon's biliteral cipher, mentioned in 1605 and fully set out in *De augmentis scientiarum* (1623), resolves a 24-letter alphabet into sequences of five instances of two differences, conventionally `a/b`. Bacon explicitly states that the two differences may be presented to the eye or accommodated to the ear, giving bells and trumpets among his examples. The historical mechanism is therefore a general two-difference steganographic carrier that can be instantiated acoustically/musically.

E15 is an exploratory decoder-family probe only. It is **not** a claim that Bacon's specific cipher was historically available to an early-15th-century Voynich author.

## Why this probe is structurally distinct

Under the already adopted Zattera slot grammar, slot11 is the unique natural binary raw-state slot:

- `EMPTY`
- `y`

No clustering cardinality is introduced to manufacture the binary alphabet.

The historical five-position grouping is hypothesis-side, supplied by Bacon. It is not a newly discovered Voynich period of five.

Thus the direct computational question is:

> if successive Voynich tokens carry a hidden two-difference channel in slot11, do five-bit Bacon groups decode into coherent held-out medieval Latin?

## Frozen historical alphabet

Use the 24-letter Bacon/early-modern Latin-compatible alphabet after project normalization `j→i`, `v→u`:

`abcdefghiklmnopqrstuwxyz`

Codes are the first 24 lexicographic five-bit patterns with `a=0`, `b=1`:

```text
a aaaaa   b aaaab   c aaaba   d aaabb
e aabaa   f aabab   g aabba   h aabbb
i abaaa   k abaab   l ababa   m ababb
n abbaa   o abbab   p abbba   q abbbb
r baaaa   s baaab   t baaba   u baabb
w babaa   x babab   y babba   z babbb
```

The eight remaining five-bit patterns (`11000` through `11111`) are **invalid / unassigned** under the frozen 24-letter table. They must never be silently remapped or dropped from the validity diagnostic.

## Frozen Voynich representation

Input and parser are unchanged from Issue26E:

- ZL3b mirror `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`;
- expected ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- adopted deterministic Zattera slot parser.

Primary parser: `min`.
`max` is sensitivity only and cannot rescue the primary classification.

Every successfully parsed Voynich token emits exactly one binary carrier state from slot11:

- raw `EMPTY`
- raw `y`.

Unparseable tokens break the carrier stream. Physical paragraph boundaries also break the stream. Physical line boundaries **do not** reset the five-bit grouping inside a paragraph.

## Frozen key freedom

The historical `a/b` labels can be assigned to the two observable carrier states in either orientation, and the first observed token of a paragraph need not necessarily be the first carrier position of an infolded letter.

Therefore the complete target-side key family is only:

- orientation: 2 choices;
- global phase: 5 choices (`0..4` carrier symbols skipped at the start of every paragraph-level parsed run before grouping by five).

Total: **10 keys**.

The same phase is used for every paragraph and every leaf. No paragraph-specific, line-specific, section-specific, or folio-specific phase is permitted.

Tie order is frozen:

1. lower training invalid-code fraction;
2. lower training medieval-Latin 4-gram CE among valid uninterrupted decoded runs;
3. lower phase;
4. orientation `EMPTY=a,y=b` before the reversal.

The selected key is fit on 4/5 physical leaves only and applied unchanged to untouched 1/5 held-out leaves.

For transparency also report the two literal phase-0 orientations without fitting.

## Invalid code handling

Each five-bit group is decoded independently.

- values 0..23 emit the frozen Bacon letter;
- values 24..31 emit an explicit invalid marker and **break** the decoded Latin scoring run.

Invalid groups count against `valid_group_fraction` and are never removed before computing that fraction.

This prevents a key from appearing language-like by converting inconvenient bit patterns into missing data.

## External Latin model

Reuse frozen CREMMA medieval Latin:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- lowercase ASCII;
- `j→i`, `v→u`;
- unsupported characters break runs.

Use additive-smoothed character 4-grams (`alpha=.1`) over the exact 24-letter E15 alphabet.

Report five-fold CREMMA self-baseline CE and top-five-character fraction.

## Mandatory positive control

Before interpreting a Voynich negative, the exact 10-key decoder/selector must recover deterministic hidden Bacon carriers.

For each of five controls:

1. select normalized CREMMA supported runs at approximately the E15 decoded-letter volume;
2. encode letters through the exact frozen Bacon table;
3. choose a deterministic hidden `a/b` orientation and hidden phase from seed namespace `Issue26E15:Positive:v1:<fold>`;
4. prepend exactly the hidden phase number of deterministic carrier filler states to each synthetic paragraph-like run;
5. expose only the resulting binary carrier stream;
6. select among the same 10 keys on 4/5 synthetic runs;
7. decode untouched 1/5 runs.

PASS requires:

- exact hidden `(phase,orientation)` recovered in >=4/5 controls;
- mean decoded-letter accuracy >=.99 on valid held-out groups;
- mean valid-group fraction >=.99;
- recovered held-out CE within .02 bits/char of the true-key held-out CE.

If this fails: **`SOLVER INADEQUATE`** and no Voynich negative inference.

## Held-out diagnostics

For each fold and pooled output record:

- selected phase/orientation;
- visible token count, parsed carrier count, and parse coverage;
- total five-bit groups;
- valid and invalid group counts/fractions;
- held-out 4-gram CE and scored-character count;
- decoded character frequencies and top-five-character fraction;
- first 20 decoded paragraph streams length >=12;
- exact CREMMA dictionary substrings of decoded length 4..15;
- distinct exact dictionary words length >=6 and folds supporting them;
- top decoded 4-grams with CREMMA frequencies.

No manual respacing, skipped bits, bit insertion/deletion, local phase correction, anagramming, spelling repair, or favorable-folio selection.

## Refitted order-null family

Because E15 is a sequential five-bit code, the primary experiment includes a prospective order test rather than postponing it.

Generate exactly **200 deterministic nulls**. For each paragraph-level parsed carrier run, independently shuffle its `EMPTY/y` bit sequence without replacement, preserving:

- exact binary frequency within the run;
- run length;
- paragraph/leaf identity.

Seed namespace:

`Issue26E15:BitShuffle:v1:<null>:<paragraph_id>:<run_index>`

Every null receives the same complete 10-key training selection independently on all five folds.

Primary order-specific statistic is pooled held-out CE among valid decoded runs. Report:

- lower-tail p = `(1 + # null CE <= real CE) / 201`;
- null median/q05/min;
- real CE advantage below null median;
- valid-group-fraction distribution as a secondary diagnostic.

The null family cannot create a positive result if the absolute readability gates fail.

## Frozen practical lead gate

If the positive control passes, primary `min` is called **`BACON BILITERAL PLAINTEXT LEAD`** only if all hold:

1. one exact `(phase,orientation)` recurs in >=4/5 physical-leaf folds;
2. pooled valid-group fraction >= `.95`;
3. pooled held-out CE <= Latin self-baseline + `.50 bits/char`;
4. pooled top-five-character fraction <= Latin self-baseline + `.15` absolute;
5. at least 10 distinct exact CREMMA words length >=6 occur across >=3 held-out folds;
6. refitted order-null lower-tail p <= `.01`;
7. real pooled CE is at least `.10 bits/char` below the refitted-null median.

Otherwise classification is **`NO READABLE BACON BILITERAL PLAINTEXT`**.

Also flag **`LOW-VALIDITY`** if pooled valid-group fraction < `.80`, and **`LOW-DIVERSITY OPTIMUM`** if pooled top-five-character fraction >= `.90`.

## Interpretation boundaries

- E15 is a binary steganographic carrier probe, not evidence that the manuscript is Baconian or postdates Bacon.
- The five-bit grouping is historical-model-side, not a Voynich discovery.
- slot11's natural two-state arity is manuscript-side and pre-exists E15.
- A stable phase/orientation without absolute readable Latin is not decipherment evidence.
- Do not search other binary slots/features after reveal; slot11 is chosen because it is the unique natural binary raw slot under the adopted grammar.
- Do not introduce variable phases, error-correcting bit edits, homophony, or alternative 24-of-32 codebooks after reveal.
- Do not merge E15 to main without explicit user authorization.

## Historical sources used to freeze the mechanism

- Francis Bacon, *The Advancement of Learning* (1605): `omnia per omnia` / quintuple carrier concept.
- Francis Bacon, *De augmentis scientiarum* (1623): full biliteral alphabet and explicit statement that the two differences may be carried by eye- or ear-perceptible objects, including bells and trumpets.
- Folger Shakespeare Library, *Decoding the Renaissance*: modern institutional explanation of the five-position two-difference biliteral mechanism.

No Voynich target score was inspected in selecting this E15 mechanism or its historical table.
