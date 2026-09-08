# Issue #198 — Dee Sloane MS 1902 Gate 0 final

## Decision

**`COMPOSABLE_AND_STAGE1_SUPPORT_LICENSED`**

Issue #198 is complete as a score-free source/composability gate. A separately frozen Stage 1 source-attribution experiment is now support-licensed.

This decision contains **no Voynich access, no R5 gain, no terminal/initial score, and no effect direction**.

## Frozen authority

Boundary authority remains the Ambix literal transcription. Cryptanalytic correction/alignment authority remains HistoCrypt 2022 plus the public `RichardBean/ArthurDee` material.

Exact retrieved authorities:

- Ambix mirror SHA-256: `db1c63c41471417f62cbdb7121d31c657cbaaffe197285a968e8f1711824fd4e` (4,304,961 bytes)
- HistoCrypt mirror SHA-256: `7c6bdf5e4d610c76efcf70fc54405fe295bf942f49b6c28333a26bcb236efae1` (20,737,740 bytes)
- `RichardBean/ArthurDee` commit: `6bc46f0947b2a4e7f2dee9006899931361165a76`
- `dee-text.zip` Git blob: `a6752544e40704ccb3e1fe82d670cceb35301ba5`
- `dee-text.zip` SHA-256: `b77f8117a1a1638f27353394b3db9dcc696e3ce5f85ea58cb6a7f8da695917c4`
- public `dee.xlsx` SHA-256: `c339aeac63da1b81560e63b02abb807a187a4003d3df44ebf389d3934055605d`

The fixed-source acquisition was independently run in GitHub Actions run `34218496792`; the archive identity check passed.

## Five-layer result

### 1. Ciphertext symbols — verified

The Ambix literal representation contains 1,099 base alphabetic cipher atoms when bracket annotations are retained as metadata rather than silently promoted into the base stream.

The literal-to-author-sheet transport is boundary preserving. Of 189 literal spaced groups:

- 161 transport identically;
- 25 differ only by same-length substitutions;
- one contains an annotation-derived extra author-sheet atom (`ouat[^a]qx` -> `ouataqx`);
- two adjacent groups on literal line 11 form one unresolved 10-to-9 correction block.

No source boundary was moved to repair that block. Its internal boundary is classified `UNALIGNED_OR_AMBIGUOUS`.

For atom coverage, all ten literal atoms in that block are withheld conservatively rather than guessing which atom was deleted. Deterministic coverage is therefore `1089 / 1099 = 99.09%`.

### 2. Physical lines — verified

- 2 manuscript pages
- 38 physical cipher lines
- 189 literal source-space groups
- 151 same-line adjacent group transitions
- 37 cross-line adjacent group transitions

### 3. Cipher-unit boundaries — verified

All source spaces and physical lines come from the Ambix literal authority. The solving-era `dee2` file is **not** used as boundary authority: it contains 178 analytical units / 1,098 letters and merges/splits some published source groups.

That discrepancy is archived as cryptanalytic working history, not imported into the source segmentation.

### 4. Plaintext lexical boundaries — verified with one publication-count discrepancy retained

The rendered HistoCrypt paper says “177 word Latin plaintext”, but the printed plaintext does not reproduce that count under its visible spacing.

A literal surface transcription has 180 printed tokens before treating the paper's line-wrap `ignis-beneficio` as the single word that HistoCrypt explicitly says it is. After that documented join there are:

- 179 surface segments;
- 178 lexical segments;
- one editorial angle-bracket segment, `<ac>`.

The declared `177` is therefore kept as an unresolved publication-internal aggregate-count discrepancy. No Latin dictionary or language-model repair was used to force the printed text to 177.

The printed plaintext transports exactly to the 1,099-character author-sheet plaintext using six explicit local variants only:

1. `constituetur` -> `contituetur`
2. `aperiant` -> `aperias`
3. `<ac>` -> `oc`
4. second `operi` -> `operis`
5. `continuatiupe` -> `continuatiune`
6. `abbreviata` -> `abbreuiat`

After those frozen local rules and the stated i/j, u/v alphabet normalization, the concatenation is exactly identical to the author-sheet plaintext. Edit-distance alignment is not part of the final mapping.

### 5. Cipher/plaintext alignment — verified

The public author sheet contains 1,099 cipher atoms and 1,099 plaintext atoms. Its reciprocal table/key mechanics were reimplemented and reproduce the cached plaintext with zero mismatches.

Literal source boundaries were then projected through that fixed 1:1 author-sheet position map. Of 188 adjacent source-group transitions:

| Physical relation | Lexical boundary | Within-word split | Ambiguous |
|---|---:|---:|---:|
| Same physical line | 147 | 2 | 2 |
| Cross physical line | 26 | 11 | 0 |

The two ambiguous same-line events are the unresolved line-11 correction-block boundary and one boundary adjacent to editorial `<ac>`.

## Continuation audit

The externally documented line 6 -> 7 example is recovered exactly as a `WITHIN_WORD_SPLIT`: `yogyb=nobttpnze` corresponds to the single plaintext word `ignis=beneficio`.

There are ten cross-line transitions whose left source line ends in `=`. After the independently frozen alignment, all ten classify as within-word splits. There is also one unmarked within-word cross-line split at line 22 -> 23.

Thus `=` is a highly faithful continuation mark in this source, but it is not exhaustive. This is a Gate-0 structural observation only; it was not used to choose or alter any boundary.

## Frozen support gate

| Requirement | Frozen minimum | Observed | Result |
|---|---:|---:|---|
| Aligned same-line lexical-boundary events | 100 | 147 | PASS |
| Aligned cross-line physical events | 25 | 37 | PASS |
| Externally documented cross-line within-word continuation | 1 | 1 | PASS |
| Deterministically covered literal atoms | 95% | 99.09% conservative | PASS |
| Source-boundary changes | 0 allowed | 0 | PASS |

All five layers are reproducible at sufficient support after explicit deterministic exclusions. The final Gate-0 class is therefore `COMPOSABLE_AND_STAGE1_SUPPORT_LICENSED`.

## What this licenses

Only a **new, separately committed Stage 1 preregistration/scorer**. Gate 0 does not say that Dee has a Voynich-like R5 effect. It establishes that Dee is now a clean enough external historical source to ask that question without changing its observed lineation or source spaces after seeing the result.

Machine-readable decision: `issue198_gate0_final.json`.
