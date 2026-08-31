# Issue #26E8 — Nicholas Philip duration-group prospective screen

Status: **FROZEN BEFORE E8 EXECUTABLE / SCIENTIFIC REVEAL**

Issue: #26

Base main: `21ca553d0dc7f5e203465d08ae606b4c43305817`

## Why this experiment exists

E7 strongly weakens the direct reading of the earlier Guidonian slot-lattice fit as literal voces / gamut positions: a sequence-blind static fit did not predict historically required hexachord/mutation dynamics on held-out Voynich order.

Issue #26 still contains H4: music as an intermediate cipher or mnemonic carrier. H4 is too flexible to test generically. E8 therefore tests one historically attested, manuscript-contemporary cipher family with a prediction fixed outside Voynich.

The target is the musical cipher in Friar Nicholas Philip's sermon collection, dated 1436. Modern scholarly descriptions agree on the relevant construction:

- five pitch positions;
- four rhythmic-duration classes;
- twenty pitch×duration symbols;
- the four duration classes encode the fixed five-letter groups
  - quavers: `a e i o u`
  - crotchets: `b c d f g`
  - minims: `k l m n p`
  - semibreves: `q r s t z`;
- the four pitch contours are ascending, descending, ascending, descending respectively.

Historical/source anchors used before reveal:

1. Nicholas Philip, *The Sermon Booklets of Friar Nicholas Philip*, Bodleian MS Lat. th. d. I, cipher dated 1436.
2. David Løberg Code, “Can musical encryption be both? A survey of music-based ciphers,” *Cryptologia* 47(4), 2023, 318–364, DOI `10.1080/01611194.2021.2021565` (published online 2022).
3. University of Nottingham thesis *Musical Cryptography — Codes, Ciphers, Form, and Function*, which explicitly records the four five-letter groups above and the alternating contour directions.

The known 1436 cipher actually encodes a Latin ownership statement. Therefore medieval Latin is the preregistered plaintext comparator for this narrow screen.

## Critical identifiability rule

**The mere existence of a 5×4 product in Voynich will not count as evidence.**

A 5×4 categorical product is mathematically just a 20-symbol code unless an independently historical property of the musical cipher predicts something new. E8-A therefore tests the Philip cipher's externally fixed **duration-group partition of the alphabet** before examining the five-pitch dimension.

Only if E8-A is positive may a separately preregistered E8-B test the full five-pitch × four-duration construction. No 5×4 result may rescue a failed E8-A.

## Frozen data

### Voynich

Use the same ZL3b source as E/E7:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- expected git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.

Use the unchanged `issue26e_core.py` Zattera slot parser and the same five physical-leaf folds.

Primary parser policy: `min`.

Predeclared sensitivity only: `max`; it cannot rescue a failed primary result.

### Medieval Latin reference

Reuse the external medieval Latin corpus already frozen in Issue26A / Phase62:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`
- manuscripts exactly `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`;
- physical transcription lines, no semantic sentence reconstruction.

Normalize letters to lowercase ASCII. Because the historical 20-letter cipher does not distinguish `j` from `i` or `v` from `u`, normalize `j→i` and `v→u` before applying the cipher alphabet. Do not invent mappings for the remaining unsupported letters `h,w,x,y`; they break a Latin encoded run rather than being deleted across an adjacency.

The exact supported alphabet is the union of the four historical groups:

`aeiou | bcdfg | klmnp | qrstz`.

## Voynich four-state candidates

Under the already adopted Zattera slot grammar, exactly three slots have four raw states **including EMPTY**:

- slot0: `EMPTY,q,s,d`
- slot6: `EMPTY,e,ee,eee`
- slot9: `EMPTY,i,ii,iii`

All three are included. No slot may be selected by looking at held-out results.

For a parsed Voynich token, the value of one candidate slot is one four-state event. Unparseable tokens break a run. Never stitch across unparseable tokens, line boundaries, or paragraph boundaries.

Retain only contiguous parsed runs of length >=5 for sequence statistics.

## Latin Philip-duration sequences

For each physical Latin line:

1. normalize its letters as above;
2. map every supported letter to one of the four historical Philip duration groups;
3. unsupported letters break a run;
4. retain contiguous runs length >=5.

No pitch information is used in E8-A.

## Primary comparison statistic

For any four-state sequence population, pool within-run observations and compute:

1. `P1`: the normalized 4-state unigram distribution;
2. `P2`: the normalized 4×4 ordered adjacent-pair distribution, using adjacencies only within retained runs.

Distance between a Voynich population `V` and an externally encoded Latin population `L` is

`D(V,L) = JSD(P1_V, P1_L) + JSD(P2_V, P2_L)`

where JSD is Jensen–Shannon divergence in bits. Zero-mass terms contribute zero; no data-dependent smoothing is used. Each component lies in `[0,1]`, so `D` lies in `[0,2]`. Lower is closer.

## Training-only key / slot fitting

For each Voynich physical-leaf fold and each external four-group alphabet partition independently:

1. use four-fifths of Voynich leaves as training;
2. evaluate all three four-state slots;
3. for each slot evaluate all `4! = 24` bijections from its raw states to the four external group labels;
4. choose the `(slot, permutation)` minimizing `D` on Voynich training leaves;
5. ties: lower slot index, then lexicographically smaller permutation;
6. freeze that pair;
7. score only the held-out leaves.

Thus any selection freedom given to the historical Philip partition is also given to every null alphabet partition.

## External null family — not Voynich-shaped models

The null family is defined entirely on the **external 20-letter alphabet**, not by manufacturing Voynich-like six/four-state structures.

Generate exactly 1,000 deterministic unique alternative partitions of the same 20 supported letters into four **unlabeled** groups of exactly five letters each.

- seed from SHA-256 of `Issue26E8:PhilipPartitionNull:v1` plus candidate index;
- canonicalize each partition by sorting letters within groups and sorting the four groups lexicographically;
- reject duplicate canonical partitions;
- reject the historical Philip partition under any group permutation.

For every null partition:

- encode the same frozen medieval Latin corpus;
- repeat the exact same three-slot × 24-permutation training selection independently in every Voynich fold;
- score held-out Voynich leaves with the selected key.

This null asks a precise question:

> Is the historically attested Philip grouping of letters into four duration classes unusually close to a natural four-state Voynich slot sequence, compared with arbitrary equal-capacity ways of grouping the same medieval-Latin alphabet?

It does **not** estimate how common music-like structures are in the real world.

## Statistics

For the historical target and each of the 1,000 null partitions:

- record held-out `D` in each of five folds;
- record mean held-out `D` across folds;
- record the training-selected slot and state permutation in each fold.

Primary target statistics:

- `D_Philip` = mean held-out target distance;
- null median / q05 / minimum of the 1,000 null mean distances;
- `p = (1 + #{null: D_null <= D_Philip + EPS}) / 1001`;
- fold median wins = number of folds where Philip held-out `D` is strictly below the null-fold median;
- exact-key recurrence = maximum number of folds sharing the identical `(slot, state→duration permutation)` target key.

Lower distance is better.

## Frozen primary decision

### `PHILIP DURATION-GROUP COMPATIBILITY`

Only if all hold under `min`:

1. `p <= 0.05`;
2. `D_Philip < median(D_null)`;
3. Philip beats the null-fold median in at least 4/5 folds;
4. the same exact `(slot, permutation)` target key recurs in at least 4/5 folds.

This would justify a new preregistered E8-B full pitch×duration test. It would **not** yet identify plaintext or prove that Voynich is musical.

### `UNSTABLE FOUR-STATE MATCH / NOT CIPHER SUPPORT`

If conditions 1–3 pass but condition 4 fails.

### `PHILIP DURATION-GROUP NOT SUPPORTED`

Otherwise.

## Max sensitivity

Repeat the whole target/null calculation under `max`. This is descriptive only and cannot rescue a failed `min` classification.

## Sample gates

For every accepted fold/policy target evaluation require:

- at least 1,000 held-out four-state events;
- at least 500 held-out adjacent pairs;
- all four target slot states occur in the training population of the selected slot.

If these fail, classify `INSUFFICIENT SAMPLE` rather than negative.

## Interpretation boundary

A positive E8-A supports only:

> one natural four-state Voynich slot has held-out unigram/transition geometry unusually close to medieval Latin after the letters are grouped by Nicholas Philip's historically attested four duration classes, relative to equal-capacity alternative alphabet partitions under the same slot/key search freedom.

It is not evidence merely because `4` or `20` appears.

A negative E8-A weakens the specific 1436 Philip-like musical-substitution family at its duration-group necessary-condition level. It does not reject every musical cipher.

Do not tune the Latin normalization, slot set, sequence boundary, distance metric, partition null, parser policy, or stability threshold after reveal and call it E8-A.

## Chronology / merge policy

This plan must be committed before `phaseE8_philip_duration.py` exists and before any E8 scientific result is computed.

E8 stays on its own branch/draft PR. Do not merge to `main` without explicit user authorization.
