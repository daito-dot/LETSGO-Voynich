# Issue #26E14 — Kircher 1650 six-instrument × four-count plaintext probe

Status: **COMPLETED — NO READABLE KIRCHER 6X4 PLAINTEXT**

## Question

Athanasius Kircher's later 1650 musical cryptography uses six instruments and one through four successive notes on each instrument to cover a 24-letter alphabet. E14 asked whether that historically documented 6×4 decoder family, applied to the already-adopted Voynich slot grammar, yields readable held-out medieval Latin.

This is an exploratory decoder-family probe only. Kircher 1650 is later than the usual Voynich production window and cannot establish historical transmission.

## Why this was worth testing

Unlike Porta E12, neither E14 dimension required a hypothesis-side clustering cardinality:

- Voynich slot10 has exactly six raw states: `EMPTY,d,l,r,m,n`;
- slot6 has repeated-unit states `EMPTY,e,ee,eee`;
- slot9 has repeated-unit states `EMPTY,i,ii,iii`.

The primary decoder therefore used a natural six-state factor and one of two natural ordinal four-state factors. Training freedom was restricted to count-slot choice (slot6/slot9) and a six-row permutation; the four-count order was fixed.

## Preregistration provenance

- parent plan first commit: `0803c49af02ea11b5604a213cf735bafb425acd2`
- positive-control amendment: `83965d709c257b787a209317a19e4e4042a722cf`
- first executable commit: `c59d667d50615fc359b345ed6aedbd7c56f47abb`
- first-reveal workflow/head: `8ebdc1b5125a9d5c9aa94ee0b596f5a880e74974`
- Actions run: `33385466125`
- job: `99466974957`
- artifact: `9755397548`
- raw JSON SHA-256: `2796b921d4ebe4b875b962332e76c1d09d7b74d93d1cf1896ee6b3834eee449a`
- artifact ZIP SHA-256: `7a5d42b3dc7f752c05e132de3a58b2abbe3ec00962eacf13f4990bc4ee07bd66`.

The workflow verified the exact frozen ZL3b mirror and CREMMA commit before reveal.

## Mandatory positive control

**PASS**.

Across five hidden six-row permutations:

- exact hidden permutation recovered: **5/5**
- mean occurrence-weighted decoded-letter accuracy: **1.000**
- recovered-minus-true held-out CE: **0.000 bits/char**.

Therefore a real-data negative is interpretable; the finite historical key selector is capable of recovering known Kircher-style encodings.

## External Latin baseline

Frozen CREMMA medieval-Latin self baseline:

- mean held-out 4-gram CE: **2.4515716158 bits/char**
- pooled top-five-character fraction: **0.5102175496**.

## Primary `min` result

Frozen classification:

> **`NO READABLE KIRCHER 6X4 PLAINTEXT`**

Observed:

- mean held-out CE: **4.4336765251 bits/char**
- pooled CE: **4.4257976987**
- exact `(count_slot, instrument permutation)` recurrence: **3/5**
- modal count slot: **slot9**
- modal six-row permutation: `[2,1,5,0,4,3]`
- pooled top-five-character fraction: **0.8966136173**
- distinct exact CREMMA words length >=6: **0**
- folds containing any >=6 word: **0**
- parser coverage across folds: approximately **0.761–0.776**.

All preregistered lead gates fail:

- exact-key recurrence >=4/5: FAIL
- held CE within Latin +0.50: FAIL
- top-five fraction within Latin +0.15: FAIL
- >=10 distinct words length >=6: FAIL
- word hits across >=3 folds: FAIL.

The pooled top-five fraction is very high but remains just below the separately frozen `.90` `LOW-DIVERSITY OPTIMUM` threshold, so the formal anti-collapse label is `NO LOW-DIVERSITY FLAG`. Descriptively, however, the output is strongly concentrated.

Representative held-out streams include:

- `ipwiewppeoir`
- `iwiieiiwiiiw`
- `iiiaiipiiapa`
- `iiiiwiipiaiw`
- `iiawiiiaiapii`
- `iiiiiiiiiiwai`.

No coherent Latin plaintext emerges.

## Max-parser sensitivity

Also negative:

- mean held CE: **4.6652430712**
- exact-key recurrence: **4/5**
- modal count slot: slot9
- pooled top-five fraction: **0.8966136173**
- >=6-letter exact dictionary words: **0**.

The higher 4/5 key stability under `max` does not rescue the hypothesis because absolute language/readability evidence is worse than the primary result.

## Ordinal-reversal sensitivity

Allowing the sole preregistered extra freedom — globally reversing the four-count axis — selected the same ascending primary solution and produced **no improvement at all**:

- mean held CE: `4.4336765251`
- recurrence: 3/5
- >=6 words: 0.

Thus the negative is not an artifact of choosing the wrong monotone direction.

## Interpretation

E14 separates two claims that must not be conflated:

1. **Structural observation:** the adopted Voynich grammar genuinely contains a natural 6-state factor and natural repeated-unit 4-state factors, giving a striking 6×4 capacity match to the later Kircher construction.
2. **Decoder claim:** the historical Kircher 6×4 alphabet/order does **not** turn that structure into readable held-out Latin.

The first observation may be retained as part of the wider manuscript-structure inventory. The second claim is falsified by this probe.

E14 therefore adds another mechanism-diverse negative to H4: direct application of an established historical music-cipher decoder does not recover readable plaintext.

No merge to `main` is authorized.
