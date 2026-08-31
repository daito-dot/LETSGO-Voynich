# Issue #26E9 — Nicholas Philip full 5×4 plaintext probe

Status: **FROZEN BEFORE E9 EXECUTABLE / REVEAL**

Parent: Issue26E8 / draft PR #40 at `343afac73da2e52b3a75f69e0a43257d54bdf952`.

## Purpose

E8-A did **not** pass its confirmatory gate, and E8-A2 showed that its near-hit was explained by preserving the Latin vowel group. Those conclusions remain unchanged.

E9 answers a different, explicitly exploratory question requested after that result:

> If we nevertheless apply Nicholas Philip's historically attested 1436 5-pitch × 4-duration cipher as an actual decoding mechanism, using the Voynich four-state correspondence that was closest in E8-A, does a held-out plaintext stream become measurably Latin-like or yield recognizable medieval-Latin material?

A positive E9 would be a lead for a new independently validated hypothesis. It cannot retroactively turn E8-A/E8-A2 positive.

## Historical cipher fixed before reveal

Use the Philip construction already frozen in `PLAN_E8.md`:

- four duration groups: `aeiou | bcdfg | klmnp | qrstz`;
- five pitch positions;
- group contours: ascending, descending, ascending, descending.

Define pitch rank `0..4` from low to high. Therefore the plaintext letter table by `(duration_group, pitch_rank)` is:

- group 0: `a e i o u`;
- group 1: `g f d c b`;
- group 2: `k l m n p`;
- group 3: `z t s r q`.

This is just the alternating historical contour written in common low→high rank coordinates.

Sources remain those cited in E8, especially David Løberg Code, *Cryptologia* 47(4) (2023), DOI `10.1080/01611194.2021.2021565`, and the 1436 Nicholas Philip manuscript.

## Frozen Voynich representation

Reuse the unchanged Zattera slot parser and ZL3b input from E8.

Primary parser: `min`. `max` is sensitivity only.

### Duration dimension — fixed from E8-A, no refit

E8-A selected the identical primary key in all 5/5 folds:

- slot0 raw states: `EMPTY,q,s,d`;
- state→Philip-group permutation: `[0,3,1,2]`.

So E9 fixes:

- `EMPTY → aeiou` group;
- `q → qrstz` group;
- `s → bcdfg` group;
- `d → klmnp` group.

No alternative four-state slot or duration mapping is searched in the primary E9 path.

### Pitch dimension — finite candidates

Under the adopted grammar, exactly two slots have five raw states including EMPTY:

- slot3: `EMPTY,t,k,p,f`;
- slot5: `EMPTY,cth,ckh,cph,cfh`.

For each fold, training data may choose:

- pitch slot 3 or 5;
- one of all `5! = 120` bijections from that slot's raw states to pitch ranks `0..4`.

Thus the primary training search has exactly 240 candidate pitch keys. The duration key and historical letter table are fixed.

Each parsed Voynich **token becomes one candidate plaintext letter** from the 20-letter Philip alphabet. Unparseable tokens and physical line boundaries break streams. No word boundaries are inferred during scoring.

## External Latin language model

Use the same frozen CREMMA medieval-Latin corpus and normalization as E8:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- lowercase ASCII;
- `j→i`, `v→u`;
- only the 20 Philip letters are retained inside a run; unsupported letters break a run.

Build a character **4-gram** model on retained Latin runs. Use additive smoothing `alpha=0.1` over the 20-letter alphabet. Score a decoded population by mean negative log2 probability per predicted character from positions with a full 3-character history. Lower cross-entropy is more Latin-like.

The Latin corpus is external and never fit to Voynich.

## Five-fold selection and held-out scoring

Use the same five physical-leaf folds as E8.

For each fold:

1. build the external Latin 4-gram model once;
2. on 4/5 Voynich training leaves, evaluate all 240 pitch keys under the frozen duration mapping and historical Philip table;
3. select the key with lowest training cross-entropy; ties: lower pitch slot, then lexicographic permutation;
4. freeze that pitch key;
5. decode and score the held-out Voynich leaves only.

Record selected pitch key, training/held-out cross-entropy, decoded character count, and sample held-out decoded streams.

## Cipher-order nulls

To determine whether any apparent plaintext comes from the **historical Philip pitch ordering** rather than merely the already-known four groups / 20-letter capacity, create exactly 1,000 deterministic null ciphers.

Each null preserves:

- the exact same four letter groups `aeiou | bcdfg | klmnp | qrstz`;
- five letters in each group;
- the same frozen E8 duration key;
- the same two pitch-slot choices;
- the same 120 pitch-rank mappings;
- the same folds and Latin language model.

For each null, independently permute the five letters **within each of the four groups**, rejecting the historical Philip table and duplicate complete tables. Seed family: `Issue26E9:PhilipWithinGroupNull:v1`.

Every null receives the identical 240-key training search before held-out scoring.

Primary statistics:

- historical Philip mean held-out cross-entropy across five folds;
- null median / q05 / minimum;
- lower-tail `p = (1 + #{null <= target}) / 1001`;
- folds where historical target beats the null-fold median;
- exact pitch-key recurrence across folds.

## Plaintext inspection

After scoring is complete, emit for the historical target:

- the first 20 held-out streams of length >=12 per fold, capped at 80 characters each;
- the 50 longest substrings of length >=4 that occur as complete normalized words in the frozen CREMMA lexicon, with corpus frequency and source decoded stream;
- the 50 most frequent decoded 4-grams and their CREMMA frequencies.

These are **descriptive**. No manual word spacing, synonym substitution, anagramming, Caesar shifting, homophone replacement, or selective folio cherry-picking is allowed.

## Frozen interpretation

### `PLAINTEXT-LIKE PHILIP LEAD`
Only if primary `min` satisfies all:

1. target lower-tail `p <= .01` against the 1,000 within-group-order nulls;
2. target beats null-fold median in >=4/5 folds;
3. one exact `(pitch_slot, pitch_permutation)` recurs in >=4/5 folds;
4. mean held-out cross-entropy is at least `0.10 bits/char` below the null median.

This is deliberately stronger than E8-A because E9 searches a plaintext key after an already-seen near-hit.

### `LATIN-LIKE BUT NON-SPECIFIC`
If target is better than null median but fails any of the four lead gates.

### `NO PHILIP PLAINTEXT SIGNAL`
If target is at/above null median or held-out direction is inconsistent.

Regardless of class, print decoded samples so the exploratory question is answered directly.

## Boundaries

- E9 is exploratory and post-E8; it does not erase E8-A2.
- Do not search other alphabets/languages after reveal and call them E9.
- Do not alter the historical four groups or alternating contour after reveal.
- Do not use semantic intuition to choose a pitch key; key choice is training-only 4-gram likelihood.
- No claim of decipherment without independent replication and coherent multi-folio semantics.
- E9 remains on its own branch and must not be merged without explicit user authorization.
