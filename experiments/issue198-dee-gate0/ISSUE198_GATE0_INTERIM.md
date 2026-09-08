# Issue #198 — Dee / Sloane MS 1902 Gate 0 interim audit

Date: 2026-09-08  
Parent: #172  
Branch: `issue198-dee-gate0`

## Status

**Gate 0 remains open. Stage 1 is not licensed.**

This note records only source preservation, boundary counts, and deterministic decryption transport checks. No Voynich data, R5 gain, terminal/initial likelihood, candidate score, or effect direction was inspected.

Machine-readable counts and hashes are in `issue198_gate0_interim.json`.

## 1. Literal boundary layer

Boundary authority: Piorko, Lang, Bean, *Ambix* 2023, DOI `10.1080/00026980.2023.2201744`.

Mirror fixed by #198:
`https://richardbean.id.au/papers/ambix_hermeticae.pdf`

The literal ciphertext block gives:

- 2 physical pages;
- 38 physical lines: 18 on page 1 and 20 on page 2;
- 189 source-space groups;
- 151 same-line source-space boundaries;
- 37 physical line transitions;
- 10 line-final `=` continuation marks, on lines 6, 15, 16, 20, 21, 28, 29, 30, 32, and 36;
- therefore 27 cross-line transitions without a line-final continuation mark.

The HistoCrypt paper independently describes the line 6→7 case as one ciphertext word split across physical lines, corresponding to `ignis=beneficio`. Thus the required existence proof for a within-word cross-line continuation is externally supported.

There are three literal groups carrying bracketed annotations: line 9 `ouat[^a]qx`, line 20 `[h]woruuod`, and line 32 `wu[y]`. Their atom-retention semantics must remain separate from source boundaries.

The alphabetic atom total depends on how those annotations are treated:

- strip all bracket annotations: 1099;
- retain only the superscript `a`: 1100;
- retain all bracket letters: 1102.

No one of these policies is selected here by agreement with the solved text.

## 2. Literal vs HistoCrypt working transcription

HistoCrypt 2022 prints the working ciphertext in the same 38-line / 189-group structure. The number of spaced groups on every physical line matches the Ambix literal transcription.

Text differs on 12 lines: 2, 4, 6, 7, 9, 14, 19, 20, 23, 32, 33, and 37. These include ordinary letter substitutions and uncertainty notation. At this stage no line break or source-space boundary has to be moved, inserted, or deleted to compare the two published representations.

Table 1 of the HistoCrypt paper gives a corrected-transcription frequency total of 1099 alphabetic atoms.

This means the current problem is not a physical-boundary mismatch. It is the exact corrected atom transport from literal transcription to the solved 1099-character stream.

## 3. Public author alignment sheet

Richard Bean's public `ArthurDee` repository at the commit frozen by #198 links an illustration of the decipherment:

`https://docs.google.com/spreadsheets/d/1SIB59QxKms1ka8KCQtXwLYEOujf7tI5a/edit?usp=sharing`

Downloaded workbook identity for this audit:

- file: `dee.xlsx`
- SHA-256: `c339aeac63da1b81560e63b02abb807a187a4003d3df44ebf389d3934055605d`
- sheet: `testing fixes`

The sheet contains:

- the 45-character key phrase `sicalteriasonaureafeliciportabisuelleracolcho`;
- a 1099-character ciphertext stream;
- a 1099-character plaintext stream;
- the tabular reciprocal mapping used by its formulas.

Reimplementing the sheet formula mechanically from its own table and 45-position key reproduces all 1099 cached plaintext characters exactly: 0 mismatches.

This verifies that the public author spreadsheet is internally deterministic. It does not yet prove that its 1099-character ciphertext is exactly the frozen HistoCrypt corrected transcription while preserving the Ambix literal boundary map.

## 4. Published plaintext boundary check

HistoCrypt Section 4 states that the solution contains 177 Latin words. Under a frozen surface-only parse of the printed solution:

- editorial `<ac>` is excluded;
- only typographic line-break hyphenation is joined;
- displayed `ignis-beneficio` is retained as one surface token;
- footnoted Latin corrections are not applied;

I obtain 178 surface tokens.

The one-token discrepancy is not repaired here. A Latin dictionary, language model, or semantic preference would violate #198. The published 177-word statement remains an authority fact; the project still needs a deterministic rule or author transport that reproduces it.

## 5. What is already sufficient and what is not

The raw boundary support is numerically large enough to make the prospective thresholds plausible before alignment: 151 same-line boundaries and 27 non-continuation cross-line transitions, plus multiple explicit continuation marks. These are only source counts, not licensed aligned event counts.

The remaining Gate-0 responsibility is exact transport:

`Ambix literal atoms/boundaries -> documented corrections -> corrected 1099-atom ciphertext -> published plaintext boundaries`.

The fixed public repository contains `dee-text.zip`, which may hold the exact `dee2` transport used in the authors' workflow. The current GitHub connector exposes the blob identity but cannot decode that binary archive through its UTF-8-only file path. That tool limitation is not treated as evidence against the source.

Accordingly no frozen Gate-0 class is assigned yet. Issue #198 stays open and Stage 1 remains prohibited until the pinned archive or another already-frozen author transport closes the corrected-stream identity without changing source boundaries.

## Reproducibility identities

Public code authority frozen by #198:

- repository: `RichardBean/ArthurDee`
- commit: `6bc46f0947b2a4e7f2dee9006899931361165a76`
- tree: `6ed19dcbcf77eaa463979064fa06334867d9e196`
- `dee-text.zip` blob: `a6752544e40704ccb3e1fe82d670cceb35301ba5`

Author-sheet stream hashes from this audit:

- ciphertext SHA-256: `3e0aab0f59160896fa8fdf088c7ee15af2c9bad1eced404f8ed7b6d020a56446`
- plaintext SHA-256: `21458f41a44a4ec45938f84bd6c341b0e695bb9f8b2c6fb3afee14bea61d4c27`

No score-bearing artifact was produced.
