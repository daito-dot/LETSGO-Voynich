# Issue #26 H4 — historical music-cipher candidate frontier after E8

Status: **DESIGN / LITERATURE BOUNDARY — NO NEW VOYNICH REVEAL**

## Purpose

E8-A/E8-A2 tested one historically attested music-as-intermediate-cipher family, Nicholas Philip (1436), and found that its apparent four-state compatibility is explained by preserving the Latin vowel class rather than by Philip's specific consonant subdivision.

The next methodological risk is obvious: trying named historical music ciphers one after another until one happens to fit Voynich. This document records the current literature frontier and why no new H4 statistical test is being launched yet.

## Current pre-1500 / manuscript-contemporary examples surfaced by the literature search

### 1. Martinus Polonus — 1277 attribution

A modern historical-cipher gallery by Klaus Schmeh identifies a musical cipher described by Martinus Polonus in 1277 and points to David A. King, *The Ciphers of the Monks* (2001), p. 114.

Current limitation:

- the web-accessible source found in this pass establishes the attribution/example but does not provide a sufficiently auditable textual transcription of the exact cipher key;
- the scientific test must not reconstruct or guess a key from a low-resolution image after looking at Voynich statistics.

Disposition: **eligible historical lead, not currently executable** until the exact source/key can be recovered independently and frozen.

### 2. Nicholas Philip — 1436

The 1436 sermon-booklet cipher is well enough documented to freeze its relevant structure:

`aeiou | bcdfg | klmnp | qrstz`

with five pitch positions and four duration classes.

Disposition: **tested in E8-A/E8-A2; specific duration-group signature not supported**. The reserved pitch-stage must not be run as a rescue.

### 3. British Library Sloane MS 351, f. 15b — 15th century / late 15th century

British Library catalogue metadata records f. 15b as 15th-century “Rules for a cipher.” Eric Sams' historical account describes the musical cipher as using five different pitches on a three-line staff, modified by stem direction and note values, to represent 24 letters plus `et`, with an example plaintext beginning `In nomine summe et individue trinitatis ...`.

Current limitations:

- the item is commonly described as late 15th century, making direct chronological relevance to an early-15th-century Voynich production weaker than Philip;
- the exact complete letter→symbol key was not recovered in a sufficiently auditable machine-readable form during this pass;
- treating a later scheme as a direct source without an independent manuscript-local selector would add historical as well as statistical freedom.

Disposition: **historically relevant comparison, not currently justified as the next Voynich test**.

## Sources consulted in this pass

- David Løberg Code, “Can musical encryption be both? A survey of music-based ciphers,” *Cryptologia* 47(4), 2023, 318–364. DOI `10.1080/01611194.2021.2021565`.
- Klaus Schmeh, “Musical Ciphers,” historical gallery; entries for 1277 Martinus Polonus, 1436 Nicholas Philip, late-15th-century BL Sloane 351.
- Eric Sams, “Musical Cryptography,” *The Musical Times* / cryptography essay (1979), description of Sloane 351 f.15b.
- British Library Archives and Manuscripts catalogue, Sloane MS 351: f.15b “Rules for a cipher,” 15th century.

## Frozen methodological rule from this point

Do **not** run another named H4 historical cipher merely because it is available.

A new H4 experiment is justified only if one of these conditions is met before inspecting the new Voynich target score:

1. **Finite-family route:** recover exact, auditable keys for a historically defined candidate set, freeze the complete set and a family-level multiplicity rule, then test the family together; or
2. **Independent-selector route:** a manuscript-local visual/textual feature independently selects one historical cipher construction before any sequence/statistical fit is examined.

If neither condition can be met, H4 should remain unresolved rather than become an open-ended cipher search.

## Current scientific implication

The immediate positive object produced by E8 is not musical:

> a natural four-state Voynich slot can have a stable sequence relationship to a Latin categorization that isolates vowels from consonants.

E8-A2 shows that this relationship does not care about Philip's historical consonant subdivision. If pursued, that signal belongs in a linguistic/morphological branch with its own controls, not as evidence for music.

No new cipher test is preregistered by this document, and no new Voynich score has been inspected.
