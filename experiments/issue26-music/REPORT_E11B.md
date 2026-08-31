# Issue26E11B — official STA-family source audit

Status: **COMPLETED — DESCRIPTIVE INFRASTRUCTURE, NOT A SCIENTIFIC REVEAL**

The first E11 strict substitution run stopped at its representation gate because the ad-hoc EVA-ish visible-grapheme tokenizer exposed 31 classes, exceeding the 24-letter normalized Latin alphabet. E11B checked whether a published, Voynich-independent glyph-regularisation system resolves that representation issue without frequency pruning.

## External authority

René Zandbergen's STA1 framework groups visually similar Voynich shapes into published `character families`. The official documentation states that STA was designed to facilitate cross-transliteration comparison, and that different transliterations tend to agree on family while differing on family member. It also explicitly warns that STA/families are not a final claim about the true Voynich character ontology.

E11B used the official ZL3b STA1 file linked from that framework.

## Frozen source

- URL: `https://www.voynich.nu/data/sta/ZL3b.txt`
- header: `#=IVTFF STA1 2.0 M 5`
- byte size: `472861`
- SHA-256: `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`

Audit provenance:

- source-freeze protocol commit: `21c2a03b13511f39c8d10a1818c7c85936eb4a38`
- audit workflow head: `0bb215a70ea42680e844f4184eefbf278f05b5b6`
- Actions run: `33381660646`
- job: `99455169946`
- artifact: `9753971239`
- artifact ZIP SHA-256: `d4cc2cdaeba746bc384e85152a9a930e27b56c7c0578c4c8366d8f908c675ae4`

## Running-text audit

Scope: loci whose IVTFF kind contains `P`, first reading of bracketed alternatives, no plaintext fitting.

- running-text physical lines with STA codes: **4,130**
- STA symbol events: **140,590**
- distinct full STA codes: **200**
- distinct published STA families: **23**
- malformed residue: **0**

Family counts:

| family | count | fraction |
|---|---:|---:|
| A | 51,492 | .366256 |
| B | 22,520 | .160182 |
| Q | 14,244 | .101316 |
| K | 14,128 | .100491 |
| J | 9,185 | .065332 |
| C | 8,219 | .058461 |
| D | 5,359 | .038118 |
| L | 4,314 | .030685 |
| G | 4,016 | .028565 |
| F | 2,268 | .016132 |
| U | 1,790 | .012732 |
| P | 1,639 | .011658 |
| M | 358 | .002546 |
| T | 297 | .002113 |
| E | 276 | .001963 |
| H | 160 | .001138 |
| Z | 132 | .000939 |
| W | 70 | .000498 |
| S | 50 | .000356 |
| X | 31 | .000220 |
| V | 18 | .000128 |
| N | 14 | .000100 |
| R | 10 | .000071 |

## Interpretation

The official family representation has **23** classes, so strict injection into the frozen 24-letter Latin alphabet is structurally definable without deleting rare signs by frequency.

This does **not** mean that 23 is the true Voynich alphabet size. In particular, STA family A deliberately groups several very frequent visually related shapes (including the familiar EVA `o/a/y` family). The official source warns that a family is a comparison/regularisation device, not a proven semantic character.

Therefore a family-based substitution run is scientifically interpretable only as a strong allographic model:

> visually related members of one published STA family are treated as variants of the same underlying cipher-sign class.

A negative result would reject that family-normalized strict substitution representation, not every León-like cipher.

The next experiment, E11C, may now be preregistered because `M_family=23 <= 24` was established without looking at plaintext scores.
