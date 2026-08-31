# Issue26E17A — Friderici 8×3 triadic/motif plaintext probe

Status: **PREREGISTERED — NO E17 TARGET REVEAL YET**

Parent research state: E16 report head `7810d01060e75e2324e774b5cba05137bfe8d8f3`.

## Purpose

E16 tested Friderici's separate pure-rhythm ternary construction and was negative. E17A moves to the other Friderici music-cipher construction rather than retuning E16.

Historical descriptions of Johannes Balthasar Friderici's *Cryptographia* (Hamburg, 1685), including the original musical-cipher section at pp. 184–186 and Johannes Wolf's later notation-history reproduction, describe a 24-letter cipher built from **eight tones or tone-groups, each repeated one, two, or three times**. A modern cryptography thesis reproduces the same construction as the **Friderici Triadic Compound Motific Cipher**: eight substitutable motifs, with three alphabetic letters assigned to each motif and distinguished by repetition count 1/2/3.

This source structure fixes an `8 × 3 = 24` product code independently of Voynich statistics.

Friderici is much later than the usual Voynich production window. E17A is therefore an exploratory decoder-family probe, not a claim that Friderici's exact 1685 construction was available to the Voynich author.

A secondary-source figure caption gives 1665 while the bibliographic/original-source record and Wolf give 1685. E17A relies only on the independently agreed 8×3 construction, not on that discrepant caption date.

## Frozen historical table

Use the repository's established 24-letter normalized Latin alphabet:

`abcdefghiklmnopqrstuwxyz`

The historical row groups are the eight consecutive three-letter groups after the usual `j→i`, `v→u` normalization:

```text
row 0: a b c
row 1: d e f
row 2: g h i
row 3: k l m
row 4: n o p
row 5: q r s
row 6: t u w
row 7: x y z
```

Column 0/1/2 corresponds to one/two/three repetitions of the row's tone or motif.

No letter, row membership, or repetition position may be changed after reveal.

## Frozen Voynich representation family

Do not learn an 8-state clustering.

Under the already adopted Zattera slot grammar, there are exactly three natural four-state slots when `EMPTY` is counted:

1. slot0: `EMPTY,q,s,d`
2. slot6: `EMPTY,e,ee,eee`
3. slot9: `EMPTY,i,ii,iii`

There is exactly one natural binary slot:

- slot11: `EMPTY,y`

Crossing one four-state slot with slot11 gives exactly eight raw motif states. Raw order is frozen as Cartesian lexicographic order `(four_state_index, slot11_index)`.

There are exactly five natural three-state slots when `EMPTY` is counted:

1. slot1: `EMPTY,o,y`
2. slot2: `EMPTY,l,r`
3. slot4: `EMPTY,ch,sh`
4. slot7: `EMPTY,s,d`
5. slot8: `EMPTY,o,a`

A representation is one of the `3 × 5 = 15` pairs:

`(four-state slot × slot11) × three-state repetition slot`.

All 15 representations are charged prospectively. No candidate may be removed or added after target reveal.

Primary parser: `min`.
`max` is sensitivity only and cannot promote a primary failure.

## Carrier streams and boundaries

Each successfully parsed visible Voynich token emits exactly one raw `(8-state motif, 3-state repetition)` cell and therefore exactly one candidate plaintext letter.

- paragraph boundaries break decoded scoring runs;
- an unparseable visible token breaks the current run;
- physical line boundaries inside the same paragraph do not break a run;
- no phase, insertion, deletion, local reset, or skipped token is allowed.

This is a token-as-cipher-letter model. Visible Voynich token boundaries are not treated as plaintext word boundaries.

## Frozen key freedom

For each representation and physical-leaf training fold, fit only:

- one permutation of the eight raw motif states onto the eight historical rows: `8!`;
- one permutation of the three raw repetition states onto historical repetition counts 1/2/3: `3!`.

The conceptual key family is therefore `15 × 8! × 3! = 3,628,800` keys per fold.

The same representation, row permutation, and column permutation is frozen and applied to the untouched held-out leaf fold.

Tie order after equal training score:

1. lower four-state slot index;
2. lower repetition-slot index;
3. lexicographically smaller row permutation;
4. lexicographically smaller column permutation.

## Frozen solver

E17A uses one deterministic structured-product solver. It is not allowed to choose among solvers after target reveal.

For each representation/fold:

1. build raw-cell 4-gram pattern counts on training runs;
2. construct six unigram-informed starts, one for each of the six column permutations; for a fixed column permutation, obtain the globally optimal row assignment for the training raw-cell unigram objective by linear assignment against frozen Latin unigram costs;
3. add six deterministic random product-key starts from seed namespace `Issue26E17A:Restart:v1:<representation>:<fold>:<restart>`;
4. from each start run steepest descent over all 28 single row swaps and all 3 single column swaps under the frozen medieval-Latin character 4-gram objective;
5. choose the lowest final training CE, with the frozen key tie order above.

The executable must verify every accepted local move against an independently computed full score to tolerance `1e-10`.

No annealing temperature, restart count, neighborhood, or seed may be changed after target reveal.

## Mandatory external positive control

Voynich must not be evaluated unless this solver is first shown to recover known product ciphers.

Use the same frozen CREMMA medieval-Latin population as the target language model. Construct 12 deterministic hidden Friderici product keys, spanning all six column permutations and two independently seeded row permutations per column permutation.

For each hidden key:

1. take 40,000 normalized Latin characters in intact corpus runs;
2. encrypt each plaintext letter by inverse lookup through the exact historical 8×3 table and hidden product key;
3. split intact runs into the same five run-index folds;
4. fit the frozen solver on 4/5 runs and score/decode the untouched 1/5.

PASS requires all 60 held-out folds to satisfy:

- exact hidden row permutation recovered;
- exact hidden column permutation recovered;
- decoded-character accuracy `1.000`;
- recovered held-out CE equals true-key held-out CE within `1e-10`.

Any failure gives classification **`SOLVER INADEQUATE`** and blocks Voynich interpretation.

## External Latin model

Reuse the E11/E16 frozen CREMMA medieval-Latin source:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- lowercase ASCII;
- `j→i`, `v→u`;
- 24-letter alphabet above;
- additive-smoothed character 4-gram model with `alpha=.1`.

Report five-fold CREMMA self-baseline CE and pooled top-five-character fraction.

## Held-out diagnostics

For every target fold record:

- selected four-state slot and repetition slot;
- row permutation and column permutation;
- training CE and held-out CE;
- visible-token count, parsed-token count, parse coverage, scoring-run count;
- decoded-character count and 4-gram scored-character count;
- decoded character frequencies and top-five-character fraction;
- first 20 decoded runs of length >=12;
- exact CREMMA dictionary substrings of length 4..15;
- distinct exact dictionary substrings length >=6 and folds supporting them;
- top decoded 4-grams and their CREMMA frequencies.

Dictionary substrings are diagnostic because this model has no independently justified plaintext word-boundary channel.

## Frozen Stage-A lead gate

Primary `min` is called **`FRIDERICI 8x3 PLAINTEXT LEAD`** only if all conditions hold after the positive control passes:

1. one exact complete key `(four-state slot, repetition slot, row permutation, column permutation)` recurs in at least `4/5` physical-leaf folds;
2. pooled held-out CE is no more than `0.50 bits/char` above the frozen medieval-Latin self baseline;
3. pooled decoded top-five-character fraction is no more than `.15` absolute above the Latin baseline;
4. at least 10 distinct exact CREMMA substrings of length >=6 occur across at least 3 held-out folds;
5. no fold has parse coverage below `.70`.

Otherwise frozen classification:

**`NO READABLE FRIDERICI 8x3 PLAINTEXT`**.

The substring condition is deliberately only one of several simultaneous gates; substring hits alone are not evidence.

## Stage-B boundary

E17A does **not** authorize a positive interpretation even if the Stage-A lead gate passes.

If and only if E17A passes every Stage-A lead condition, a separate plan-first E17B must be committed before any further target analysis. E17B must test at least:

- fully refitted within-run order nulls preserving raw 24-cell frequencies and run lengths; and
- historical-table specificity against a prospectively generated family of alternative 8×3 alphabet tables, with the complete 15-representation product-key fitting freedom charged for every comparator.

This boundary is required because E11G showed that a low fitted 4-gram CE can be non-identifying even when it reaches a Latin self baseline.

If E17A fails, do not rescue it with a different slot product, learned 8-state clustering, local/section keys, variable repetition semantics, token edits, word respacing, or alternative Friderici table.

## Interpretation boundaries

- Friderici 1685 is chronologically late; this is an exploratory mechanism test only.
- The 8×3 product architecture is historical/model-side.
- The 15 candidate representations are manuscript-side and fully charged.
- A low CE without complete-key recurrence, diversity, and substring support is not a plaintext lead.
- A Stage-A lead still requires Stage-B null and historical-specificity audits before any music-cipher support claim.
- No merge to `main` is authorized.

## Historical sources used to freeze the mechanism

- Johannes Balthasar Friderici, *Cryptographia* (Hamburg, 1685), musical-cipher section pp. 184–186.
- Johannes Wolf, *Handbuch der Notationskunde*, historical reproduction/description: eight tones or tone-groups, repeated one to three times, encode the alphabet.
- modern thesis reproduction, Figure 2.24, “Friderici Triadic Compound Motific Cipher”: eight substitutable motifs, each assigned three letters numbered 1/2/3.

No Voynich target score was inspected in choosing the historical 8×3 table, the 15 representations, solver, or Stage-A gates.
