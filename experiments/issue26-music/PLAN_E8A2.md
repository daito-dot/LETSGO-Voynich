# Issue #26E8-A2 — vowel-fixed exhaustive Philip specificity control

Status: **FROZEN BEFORE E8-A2 EXECUTABLE / REVEAL**

Issue: #26

Parent experiment: E8-A, frozen classification **`PHILIP DURATION-GROUP NOT SUPPORTED`**.

## Motivation

E8-A compared Nicholas Philip's historically attested 1436 four-duration alphabet partition

`aeiou | bcdfg | klmnp | qrstz`

against 1,000 equal-capacity random partitions of the same twenty letters.

The primary result was a preregistered negative (`p=.062937`), but with a stable near-hit:

- target mean held-out distance `0.1912990849` vs null median `0.2856364100`;
- target below the null-fold median in 5/5 folds;
- identical target key in 5/5 folds: slot0, permutation `[0,3,1,2]`.

The strongest non-musical explanation is obvious and externally defined: Philip's first group is exactly the five vowels `aeiou`. Random equal-capacity partitions usually destroy the vowel class. A Voynich four-state factor could therefore look unusually Philip-like simply because a vowel-vs-consonant partition creates strong Latin sequence structure.

E8-A2 is an adversarial interpretation test of that explanation. It is **not** an independent replication and cannot retroactively make E8-A positive.

## Frozen question

> Conditional on keeping the Latin vowel class `aeiou` intact in every comparator, is Philip's exact subdivision of the remaining fifteen consonants into `bcdfg | klmnp | qrstz` still unusually close to held-out Voynich four-state sequence geometry under the same training-only slot/key search?

If not, the E8-A near-hit is adequately explained by vowel isolation rather than the specific 1436 musical-cipher partition.

## Frozen data / preprocessing

Use exactly E8-A:

### Voynich

- ZL3b blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`;
- unchanged `issue26e_core.py` slot parser;
- same five physical-leaf folds;
- primary parser `min`;
- `max` descriptive sensitivity only;
- candidate four-state slots exactly 0, 6, 9;
- unparseable tokens and line/paragraph boundaries break runs;
- retain parsed runs length >=5.

### Medieval Latin

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`;
- manuscripts exactly `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`;
- same physical-line parsing and normalization as E8-A;
- `j→i`, `v→u`;
- unsupported `h,w,x,y` break runs;
- supported alphabet exactly the twenty letters in Philip's partition.

### Distance and fitting

Replay E8-A unchanged:

`D = JSD(4-state unigram) + JSD(4×4 ordered adjacent pairs)`

Lower is closer.

For each candidate alphabet partition and each fold independently:

1. use four-fifths Voynich leaves for training;
2. search all three candidate slots;
3. search all 24 state→group bijections;
4. choose training-minimum D with frozen tie-breaks;
5. freeze the key;
6. score the held-out leaves.

Every comparator receives the same search freedom as Philip.

## Exhaustive vowel-fixed comparator universe

Fix one group to exactly:

`aeiou`

The remaining consonant alphabet is exactly:

`bcdfgklmnpqrstz`

Enumerate **every unordered partition** of these fifteen consonants into three groups of five.

The number of unique partitions is:

`C(15,5) * C(10,5) / 3! = 126,126`.

Canonicalization:

- sort letters within each consonant group;
- sort the three consonant groups lexicographically;
- prepend the fixed vowel group `aeiou`.

The historical Philip partition is one member of this exhaustive universe. The scientific null population is the other **126,125** partitions.

No random sampling is used in E8-A2.

## Replay firewall

Before accepting E8-A2 interpretation, the Philip target must replay E8-A primary values within `1e-12`:

- mean held-out D: `0.19129908493223072`;
- selected slot: `0` in all five folds;
- selected permutation: `[0,3,1,2]` in all five folds;
- exact-key recurrence: 5/5;
- held-out fold distances:
  - `0.16711006000869041`
  - `0.18571262717003223`
  - `0.18769991148862764`
  - `0.20508107071913337`
  - `0.21089175527466988`.

If replay fails, stop without scientific classification.

## Statistics

For the complete 126,126-candidate universe under `min`:

- `D_Philip` = target mean held-out distance;
- `rank` = 1 + number of non-Philip candidates with mean D strictly below `D_Philip - EPS`;
- `ties_or_better` = number of all candidates with mean D <= `D_Philip + EPS`;
- exact conditional percentile `p_cond = ties_or_better / 126126`;
- universe median, q05, q01, and minimum;
- per-fold target distance versus exhaustive comparator median;
- fold median wins.

Also report the best five non-Philip partitions and their mean held-out distances for interpretation.

## Frozen primary decision

### `PHILIP CONSONANT SUBDIVISION SURVIVES VOWEL-FIXED CONTROL`

Only if under `min`:

1. replay firewall passes;
2. `p_cond <= .05`;
3. Philip mean D is below the exhaustive-universe median;
4. Philip beats the exhaustive per-fold median in at least 4/5 folds.

This is **not** a new positive music result. It would mean only that the E8-A near-hit cannot be explained by preserving the vowel group alone and that the exact historical consonant subdivision merits another independently preregistered prediction test.

### `VOWEL ISOLATION EXPLAINS E8A NEAR-HIT`

If the replay passes but `p_cond > .05`.

This means the apparent E8-A specificity disappears once the obvious linguistic property `aeiou` is conditioned on. Do not proceed to the five-pitch dimension.

### `MIXED VOWEL-FIXED SPECIFICITY`

If `p_cond <= .05` but one of conditions 3–4 fails.

## Max sensitivity

Repeat the complete vowel-fixed universe under `max`, using its E8-A target path and the same fitting rules. Descriptive only; it cannot rescue `min`.

## Interpretation boundary

E8-A2 addresses only the source of the E8-A near-hit. It does not estimate the prevalence of musical ciphers, establish plaintext, or test the five-pitch dimension.

Do not:

- change the vowel set;
- regroup unsupported letters;
- alter run boundaries;
- switch distance metrics;
- select a different slot set;
- increase/decrease the comparator universe;
- promote `max`;
- run E8-B pitch structure as a rescue if this test fails.

## Chronology / merge policy

This plan must be committed before `phaseE8A2_vowel_fixed.py` exists or any E8-A2 universe score is computed.

Remain on the dedicated E8 branch/draft PR. Do not merge to `main` without explicit user authorization.
