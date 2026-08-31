# Issue #26E16 — Friderici three-duration × three-note rhythm plaintext probe

Status: **COMPLETED — `NO READABLE FRIDERICI RHYTHM PLAINTEXT`**

## Question

E16 moved to a historical music-cipher mechanism that discards pitch entirely. Friderici's rhythmic construction represents plaintext letters by three successive note durations; pitch is irrelevant. The frozen computational representation used three duration ranks and the 24-letter Latin alphabet as the first 24 ternary triples, leaving `220/221/222` unassigned.

Friderici is much later than the usual Voynich production window. E16 is therefore an exploratory decoder-family probe only, not evidence for historical transmission.

## Voynich representation and search burden

Under the already-adopted Zattera slot grammar, all five natural three-state raw slots were prospectively charged:

- slot1: `EMPTY,o,y`
- slot2: `EMPTY,l,r`
- slot4: `EMPTY,ch,sh`
- slot7: `EMPTY,s,d`
- slot8: `EMPTY,o,a`.

For every physical-leaf fold the complete search was:

- 5 candidate slots;
- `3! = 6` raw-state→duration permutations;
- 3 global triple phases.

Total: **90 keys/fold**.

No slot, phase, or duration mapping was selected after target reveal.

## Preregistration and performance chronology

- plan-first commit: `397d6393164b37436c7dab24726884d5edc591d9`
- original frozen executable/workflow head: `f3c96a5d27e207e8dad81ee60f4e6a74cf798c72`
- performance-only amendment, frozen while the original run had emitted no E16 result: `90b7b1a39ab024d4b2ed32284541da22b6d780ec`
- vectorized equivalent executable: `42e709628411f0634c710e512728931221c56fe9`
- first successful result-emitting vectorized workflow/head: `909051082639874de50bf628539853fff9eb12fe`
- Actions run: `33390106039`
- job: `99481528598`
- artifact: `9757134161`
- raw JSON SHA-256: `4756ae9d377826180b90d4a8a874330fda77429d33e8db75f44887e8e1b12ac9`
- artifact ZIP SHA-256: `a37952a67a02726b20bfb7dcff972c2af51e339d6d6a7ff8f9ca7826cb7b939a`
- ZL3b source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`.

The performance amendment changed only how the 200×90-key null tournament was evaluated. Scientific inputs, seeds, nulls, key family, folds, objective, thresholds, and classifications were unchanged.

## Mandatory optimization-equivalence gate

**PASS exactly.**

Null index 0 was evaluated through both the original slow implementation and the vectorized implementation before the vectorized tournament was accepted.

Agreement:

- pooled CE absolute difference: `0.0`
- pooled valid-fraction difference: `0.0`
- exact-key recurrence: identical
- selected key in all five folds: identical
- held group/invalid/scored-character counts in all five folds: identical
- held NLL difference in all five folds: `0.0`.

Thus the vectorized null tournament is numerically the same experiment, not a post-reveal model change.

## Mandatory positive control

**PASS.**

Across five hidden Friderici ternary encodings:

- exact hidden phase/permutation recovered: **5/5**
- mean decoded-letter accuracy: **1.000**
- mean valid-group fraction: **1.000**
- mean recovered-minus-true held CE: **0.000 bits/char**.

Therefore the target negative cannot be attributed to inability of the finite 18-key historical decoder to recover known encodings.

## External Latin baseline

Frozen CREMMA medieval-Latin self baseline:

- mean held-out 4-gram CE: **`2.4515716158 bits/char`**
- pooled top-five-character fraction: **`.5102175496`**.

## Primary `min` result

Frozen classification:

> **`NO READABLE FRIDERICI RHYTHM PLAINTEXT`**

Pooled held-out diagnostics:

- ternary groups: **6,323**
- invalid groups: **0**
- valid-group fraction: **1.000**
- 4-gram scored characters: **874**
- pooled held-out CE: **`4.8591302356 bits/char`**
- decoded top-five-character fraction: **`.7866519057`**
- distinct exact CREMMA words length >=6: **0**
- folds with any >=6 word: **0**.

The modal target key was:

- slot **7** = `EMPTY,s,d`
- phase **0**
- raw-state→duration permutation **`[1,2,0]`**
- exact complete-key recurrence: **4/5 folds**.

Fold results:

- fold0: slot7 / phase0 / `[1,2,0]`, held CE `4.7563967021`
- fold1: slot7 / phase0 / `[1,2,0]`, held CE `4.8034784803`
- fold2: slot7 / phase0 / `[1,2,0]`, held CE `4.8015484188`
- fold3: slot7 / phase0 / `[0,2,1]`, held CE `4.9146299848`
- fold4: slot7 / phase0 / `[1,2,0]`, held CE `4.9746078806`.

Representative untouched decoded segments include:

```text
kkkonbbbadakkb
edeanbnnebolnn
blploooxeeeoee
aaaaaaakkaaa
kduoloobnddy
```

They do not form coherent Latin.

## Frozen gates

- exact key recurrence >=4/5: **PASS**
- valid-group fraction >=.95: **PASS**
- CE within Latin +.50: **FAIL** (`4.8591` vs threshold `2.9516`)
- top-five fraction within Latin +.15: **FAIL** (`.7867` vs threshold `.6602`)
- >=10 distinct words length >=6: **FAIL** (0)
- long words across >=3 folds: **FAIL**
- refitted order-null p <=.01: **FAIL**
- real CE >=.10 below null median: **FAIL**.

Neither auxiliary threshold changes the conclusion. The primary output is highly concentrated but remains below the separately frozen `.90` low-diversity flag threshold.

## Fully refitted 200-null order test

Each null independently shuffled every candidate slot's three-state sequence within every paragraph-level carrier run while preserving exact state multiset, run length, paragraph, and leaf. Every null then received the complete **90-key** search from scratch in every fold.

Results:

- real CE: **`4.8591302356`**
- null median CE: **`4.8177343428`**
- null q05: **`4.7666721069`**
- null minimum: **`4.7500736347`**
- nulls with CE <= real: **165/200**
- lower-tail p: **`.8258706468`**
- real advantage below null median: **`-0.0413958928 bits/char`**.

The real order is therefore slightly **worse** than the refitted null median, not better.

Key recurrence is also non-specific under the full search:

- 1/5 recurrence: 1 null
- 2/5: 22 nulls
- 3/5: 62 nulls
- 4/5: 65 nulls
- 5/5: 50 nulls.

Thus the target's nominal 4/5 full-key recurrence is common under frequency-preserving order destruction and must not be promoted as a residual music signal.

## `max` parser sensitivity

Also negative:

- pooled CE: **`4.7138422402`**
- valid-group fraction: **1.000**
- exact key recurrence: **5/5**
- modal key: slot2 / phase0 / identity permutation `[0,1,2]`
- top-five-character fraction: **`.9256681955`**
- distinct >=6 words: **0**.

The higher key recurrence is accompanied by stronger output collapse and cannot rescue the primary result.

## Interpretation

E16 is a mechanism-diverse negative. It does not depend on pitch, 5×5 tables, an 11-pitch hypothesis-side clustering, a 6×4 instrument table, or a binary five-bit carrier.

A natural Voynich three-state slot can yield a cross-fold-stable fitted ternary key, but the same or stronger recurrence is common after destroying order, the real order is not unusually Latin-like under full refit, absolute Latin likelihood is poor, and no long lexical material appears.

This substantially weakens the idea that previous music-cipher failures were merely local optima of pitch-table decoder families.

Do not rescue E16 post hoc by adding pitch, variable phases, null notes, state edits, section-specific keys, or alternative ternary codebooks. Friderici's separate triadic/motif construction is a different model family and would require its own independent preregistration if ever tested.

No merge to `main` is authorized.
