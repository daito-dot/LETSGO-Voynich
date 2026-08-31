# Issue #26E8 — Nicholas Philip duration-group prospective screen

Status: **PHILIP DURATION-GROUP NOT SUPPORTED**

## 1. Question

E7 weakened the literal Guidonian sequence reading by asking a sequence-blind static fit to predict unused historical hexachord/mutation dynamics. E8 moves to a genuinely different Issue #26 H4 family: **music as an intermediate substitution cipher**.

The target is the historically attested musical cipher in Friar Nicholas Philip's sermon collection, dated 1436. In the source tradition used for this preregistration, twenty letters are encoded by five pitch positions crossed with four note-duration classes. The four duration classes correspond to the fixed five-letter groups:

- quavers: `aeiou`
- crotchets: `bcdfg`
- minims: `klmnp`
- semibreves: `qrstz`

E8-A intentionally does **not** test the full 5×4 product. A generic 5×4 product is merely a twenty-symbol substitution code unless an independently historical feature predicts something new. E8-A therefore tests only whether Philip's fixed external four-way alphabet partition has unusually close held-out four-state sequence geometry in Voynich.

## 2. Frozen design

Voynich candidate four-state factors were not invented after seeing the target. Under the adopted Zattera slot grammar, exactly three slots have four raw states including EMPTY:

- slot0: `EMPTY,q,s,d`
- slot6: `EMPTY,e,ee,eee`
- slot9: `EMPTY,i,ii,iii`

For each physical-leaf fold, each external alphabet partition independently received the same fitting freedom:

1. use only the four-fifths Voynich training leaves;
2. search all three candidate slots;
3. search all `4! = 24` raw-state→external-group bijections;
4. freeze the training-best `(slot, permutation)`;
5. score held-out leaves only.

Distance is the sum of Jensen–Shannon divergences between:

- four-state unigram distributions;
- 4×4 ordered adjacent-pair distributions.

Lower is closer.

The external comparator is frozen medieval Latin (the same four CREMMA manuscripts used in Issue26A), encoded according to the target partition. The null consists of 1,000 deterministic alternative equal-capacity partitions of the **same twenty Latin letters** into four unlabeled groups of five. Every null partition receives exactly the same Voynich slot/permutation search.

This null does not manufacture Voynich-like four-state systems. It asks whether the historical Philip alphabet grouping itself is unusual among equal-capacity external alphabet groupings.

## 3. First reveal

Frozen primary classification:

**`PHILIP DURATION-GROUP NOT SUPPORTED`**

### Primary `min`

- Philip mean held-out distance: **`0.1912990849`**
- 1,000-null median: `0.2856364100`
- null q05: `0.1862773689`
- null minimum: `0.1241821903`
- empirical lower-tail p: **`0.0629370629`**
- Philip beats the per-fold null median: **5/5 folds**
- identical fitted key recurrence: **5/5 folds**
- recurrent key: **slot0**, permutation `[0,3,1,2]`
- sample gate: PASS

The exact same key was selected on training data in all five folds and the target beat the null-fold median in all five held-out folds. Nevertheless, the preregistered significance requirement was `p <= .05`; the target rank is only about the top **6.3%** of the 1,000 equal-capacity partitions. The frozen positive gate therefore fails.

Held-out fold distances:

| fold | Philip D | null-fold median D | selected key |
|---:|---:|---:|---|
| 0 | `0.1671101` | `0.2815253` | slot0 / `[0,3,1,2]` |
| 1 | `0.1857126` | `0.3076705` | slot0 / `[0,3,1,2]` |
| 2 | `0.1876999` | `0.2631853` | slot0 / `[0,3,1,2]` |
| 3 | `0.2050811` | `0.3100386` | slot0 / `[0,3,1,2]` |
| 4 | `0.2108918` | `0.2674136` | slot0 / `[0,3,1,2]` |

### `max` sensitivity

- Philip mean held-out distance: `0.2140154357`
- null median: `0.2837942840`
- p: **`.1428571429`**
- fold median wins: 5/5
- exact key recurrence: 5/5
- recurrent key: slot6 / `[0,3,2,1]`

This is clearly non-significant and cannot rescue the primary result.

## 4. What is interesting despite the negative classification

The primary result is not a generic null-like pattern:

- the target is materially below the null median;
- the direction repeats in every held-out fold;
- the same exact target key recurs in all five folds.

But those facts were already incorporated into the frozen decision rule. The result remains negative because enough alternative alphabet partitions perform at least as well to give `p=.06294`.

It would be incorrect to lower the threshold, increase the apparent importance of the 5/5 stability after seeing it, or proceed directly to the reserved five-pitch dimension as a rescue.

## 5. Most important alternative explanation

Philip's first duration group is exactly `aeiou`. Therefore the near-hit may have nothing specifically to do with a musical cipher. It may simply reflect a **vowel-vs-consonant sequence partition**, which is a strong linguistic property of Latin and could align with a natural Voynich slot factor for non-musical reasons.

The original 1,000-partition null usually destroys that vowel grouping. Consequently it is not the strongest control for interpreting the near-hit as Philip-specific.

This motivates a new, separately preregistered adversarial follow-up:

> Keep the historical vowel group `aeiou` fixed in every comparator and vary only the remaining fifteen consonants among three equal five-letter groups. Does Philip's exact `bcdfg / klmnp / qrstz` subdivision remain unusually close and preserve the same held-out Voynich key?

If the effect collapses under that stronger external control, the E8-A near-hit is parsimoniously explained by isolating vowels rather than by Philip's musical cipher structure.

If the exact Philip consonant partition remains exceptional, that would justify a further prospective test. It still would not authorize the full 5×4 pitch test automatically; the next step would need its own frozen design.

## 6. Interpretation

Observed numerical fact:

> The 1436 Philip duration partition gives a stable slot0 mapping on all five folds and is closer to the frozen medieval-Latin duration-group sequence than the median equal-capacity partition in all five held-out folds.

Null-specific result:

> Among the 1,000 preregistered equal-capacity alphabet partitions, the Philip target is not rare enough to pass the frozen `.05` criterion (`p=.06294`).

What is not identified:

> This does not support a Philip-like musical cipher, a twenty-symbol code, a plaintext language, pitch values, or musical content. In particular, the result may be driven simply by the external `aeiou` vowel group.

Frozen classification therefore remains:

**`PHILIP DURATION-GROUP NOT SUPPORTED`**.

## 7. Provenance

- branch: `issue26-music-e8-philip-cipher`
- plan-first commit: `5568e66ce772178d024cf4162276dcecd63264b2`
- first executable commit: `92486b80367ab23560e5c11a8f6366cce0c6e27f`
- pre-reveal computational-only optimization: `09dc0828e1fc204e2ac7ffb1f92f627e33a20998`
- first-reveal scientific head: `d2e196d50026ae39c469117bfc2f937a338b2682`
- Actions run: `33375659570`
- job: `99436451151`
- artifact: `9751775894`
- artifact ZIP SHA-256: `30baa6e000872a4e7bdecad67de9c68cdb0a05db98deb823ec7ca7def916e543`
- raw JSON SHA-256: `8873632372a425bfd82103bb7c818b2cdb2d6cdaa8a581f084204d03498d3944`
- plan SHA-256: `c7a2d2189a58f40debc8427b294b705a627e3afa58ed927cfaff1828eb6397c6`
- executable SHA-256 at reveal: `8de3919cedc2e84e58dad60c0db93fc25935b90d881658a871ab0be06d29cb85`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`

No merge to `main` is authorized by this result.
