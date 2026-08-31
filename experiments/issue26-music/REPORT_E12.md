# Issue #26E12 — Porta 1602 11×2 music-cipher plaintext probe report

Status: **FIRST REVEAL RECORDED**

Frozen classification: **`NO READABLE PORTA PLAINTEXT`**

Anti-collapse diagnostic: **`NO LOW-DIVERSITY FLAG`**

## Question

After the Sloane 351 and Öttingen-Wallerstein 5×5 probes, E12 deliberately moved to a structurally different historical music-cipher family: Giambattista della Porta's 1602 two-note-value × eleven-pitch substitution system.

The test is exploratory because Porta postdates the usual Voynich production window. The question is practical rather than historical-origin inference:

> if the documented Porta mechanism is imposed as a decoder and all remaining mapping freedom is selected on training leaves only, does untouched Voynich become recognizably medieval Latin?

## Frozen historical decoder

Pitch rank is low→high.

- semibreve row: `abcdefghilm`
- minim row: `zyxutsrqpon`

The supported 22-letter alphabet omits the historical unsupported `j/k/v/w` after the fixed normalization `j→i`, `v→u`.

Voynich representation:

- the only natural raw binary Zattera slot, slot11 = `EMPTY/y`, supplies the two note-value classes;
- there is no natural eleven-state Voynich slot;
- therefore `11` is explicitly **hypothesis-side**, supplied by Porta;
- residual morphology (slots0..10) is clustered to `k=11` on unique training token types only and frozen before held-out assignment.

No result below should be read as an independently discovered Voynich eleven-pitch system.

## Pre-reveal corrections

Chronology:

- plan-first: `8cf6532b0e6ab9799e64b55f4706905780515961`
- word-diagnostic amendment: `0440a970619a5ca639c7b4dac7e22f6cabec19ae`
- first executable: `031fc2aa82783c86c432cba77a3c379e1f5034e6`
- pre-reveal analysis-population wrapper: `3d5b7d1a0de65036e2cc8e6cef3f136d8ce2136a`
- first-reveal head: `687ac799a824c7b154df03193dfd37a5695c0f23`

Two corrections were frozen before execution:

1. since one Voynich token decodes to one Porta letter, the original impossible “whole Voynich token = Latin word” diagnostic was replaced by exact dictionary substrings within uninterrupted decoded physical-line runs;
2. the positive-control target size was restricted to the exact 99-leaf analysis universe, and a mislabeled raw-code-count output field was renamed without changing values.

The workflow verified that the plan and amendment precede both executables.

## Provenance

- Actions run: `33382084306`
- job: `99456505568`
- artifact: `9754151971`
- raw JSON SHA-256: `44c076ad8bc8df49a6bb835cbd4b8dbfbb2950994b2282e827532bae2306c036`
- artifact ZIP SHA-256: `aa5f88bd2bf03ef303b101ac112c055c24778378948dabf8962eef06ae584a61`
- ZL3b source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`

## Mandatory positive control

The same optimizer was first required to recover a known Porta encoding at comparable length.

Result:

- gate: **PASS**
- mean true-key held-out CE: `1.8623598005 bits/char`
- mean recovered-key held-out CE: `1.8623598005 bits/char`
- decoded-letter accuracy: **1.0000**

Thus the E12 Voynich negative cannot be dismissed as failure of the structured 11×2 key solver on its own model class.

## External Latin baseline

Supported-character CREMMA self-baseline:

- mean held-out 4-gram CE: **`2.4368996485 bits/char`**
- top-five-character fraction: **`0.5102677352`**

## Primary `min`

- analysis leaves: **99**
- mean held-out 4-gram CE: **`5.0133524388 bits/char`**
- same duration orientation: **5/5 folds**
- modal orientation: `0` = slot11 `EMPTY→semibreve`, `y→minim`
- pooled top-five-character fraction: **`0.5626819832`**
- distinct exact CREMMA substrings length >=6: **1**
- folds containing any length>=6 exact word: **1/5**
- only such word: `missus`

Held-out CEs:

- fold0 `5.0779152632`
- fold1 `4.9947357891`
- fold2 `5.0417483570`
- fold3 `5.0324929045`
- fold4 `4.9198698804`

Representative untouched decoded lines:

```text
liegefiieirg
geurcuuauroc
engleffueumc
uruiruaggcap
uiiigglgaigiuc
ogloiuuaumlc
dnceurucrairm
ciccilhtarnd
ifddeeecdeed
imitimalmlcc
sumumudmusacn
uicmmmuumnim
lisuesnssine
spauieusauta
susgesundeebe
```

These have reasonable alphabet diversity compared with E10/E11-O, but they do not form coherent Latin and their 4-gram probability is dramatically worse than the external Latin baseline.

The only length-six dictionary hit was `missus`, appearing in one fold/context (`f111v`) and not supported by surrounding coherent text.

## Primary frozen gates

- CE within Latin baseline +0.50: **FAIL** (`5.0134` vs threshold `2.9369`)
- top-five fraction within Latin +0.15: **PASS** (`.5627` vs threshold `.6603`)
- >=10 distinct words length>=6: **FAIL** (1)
- qualifying long words across >=3 folds: **FAIL** (1 fold)
- same duration orientation >=4/5: **PASS** (5/5)

Frozen classification:

**`NO READABLE PORTA PLAINTEXT`**

## `max` sensitivity

- mean held-out CE: `4.9840339497`
- duration orientation recurrence: **5/5**, orientation 0
- pooled top-five fraction: `.5393881377`
- distinct words length>=6: **0**

So `max` does not rescue the Porta reading.

## What is and is not interesting

Unlike the Sloane/Öttingen probes, E12 does **not** collapse to a tiny output alphabet. This is useful because the negative is not merely another version of the same low-diversity optimizer pathology.

The stable 5/5 note-value orientation is a real numerical observation:

> across all physical-leaf folds, training prefers slot11 `EMPTY` to the Porta semibreve row and slot11 `y` to the minim row.

But this is only one bit of a much larger decoder and does not create readable plaintext. It also has an immediate non-musical candidate explanation: the two historical rows have different Latin marginal/transition profiles, while slot11 `EMPTY/y` have different Voynich frequencies. Therefore orientation stability alone is **not evidence for Porta or music**.

If preserved as a residual, it should later be tested against row-label/frequency controls rather than promoted inside the music hypothesis.

## Cross-probe interpretation

The practical music-cipher probes now fail for different reasons:

- Nicholas Philip: fitted output collapses heavily and full pitch key only recurs 3/5;
- Sloane 351: 4/5 recurrent full key, but optimizer exploits `con` and output collapses;
- Öttingen-Wallerstein: only 3/5 full-key recurrence and strong low-diversity collapse;
- Porta: solver is demonstrably adequate and output diversity is acceptable, yet held-out language likelihood and lexical coherence remain very poor.

This weakens the idea that the previous failures were merely a single local optimum of one 5×5 decoder family.

It does **not** exhaust historical music cryptography. Future probes should remain structurally distinct and historically sourced, and failures should not be rescued by post-reveal remapping.

## Merge policy

Keep E12 on `issue26-music-e12-porta-probe` as a dedicated exploratory research branch. Do not merge to `main` without explicit user authorization.
