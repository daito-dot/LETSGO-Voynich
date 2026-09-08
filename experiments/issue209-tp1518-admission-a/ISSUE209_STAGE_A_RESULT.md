# Issue #209 — TP1518-WA0 Priority-5 admission Stage A

Parent: #172  
Follows: #207 / PR #208  
Target access: **none**

## Decision

**`MACHINE_EXTRACTION_PARTIAL`**

Stage B is **not licensed**. TP1518-WA0 receives no Voynich target score under the current roadmap.

## Frozen source

Pinned public extraction:

- repository: `Trithemius-Corpus/Trithemius-Corpus`
- commit: `0e38a37671a5e3b5decd11c19fe82de79883cae7`
- data: `site/static/cipher-data.json`
- parser: `scripts/build_cipher_data.py`

Exact JSON:

- 708,505 bytes
- SHA-256 `c7c9b78d8ab3ecfcb6bb1b9b77e9763610663f05702cc77fa0c8e18aad522db5`

Acquisition/audit workflow:

- run `34222568186`
- head `664bf4711167e4f48a2e446c141c0690e6493f9b`
- artifact `10054344940`
- artifact SHA-256 `d85749cdef1d667f1bb2690af295f9df45158adfcb45913dc5a2b694be719666`

No cell was repaired or inferred.

## Machine-readable coverage

The pinned JSON emits 895 substitution columns across 63 distinct emitted chunks; the parser reports 64 source chunks.

Cell coverage:

| populated cells | columns |
|---:|---:|
| 12 | 1 |
| 13 | 2 |
| 17 | 2 |
| 20 | 2 |
| 21 | 2 |
| 22 | 21 |
| 23 | 142 |
| 24 | 723 |

Therefore:

- exact 24/24 columns: **723**
- incomplete columns: **172**

The parser is deliberately tolerant of OCR loss; this confirms that the emitted dataset is a useful exploratory extraction rather than a lossless historical codebook.

## Inverse collisions

There are **52 emitted columns** with an exact repeated output word inside the same column.

More importantly, **40 of those are nominally complete 24/24 columns**. Examples include:

- `full_chunk_0019 · col B`: `divitias` occurs for more than one plaintext letter;
- `full_chunk_0019 · col N`: `carnales` duplicates;
- `full_chunk_0022 · col B`: `tonitrus` duplicates;
- `full_chunk_0023 · col L`: `societas` duplicates;
- `full_chunk_0024 · col H`: `mundi` duplicates.

The 1518 `Clavis` explicitly treats duplicate/missing words inside an alphabet as a decoding problem. These collisions therefore cannot be silently accepted as an exact reversible table and cannot be repaired from Latin semantics.

## Sequence identity also fails the admission requirement

The machine extraction is not simply the three-table Book-I head already frozen in #207 followed by an obvious continuation.

The #207 source-cross-checked initial mappings begin:

1. `A Deus / B Creator / C Conditor`
2. `A Clemens / B Clementissimus / C Pius`
3. `A Creans / B Regens / C Conservans`

None of those three prefix mappings occurs exactly in the emitted 895 columns.

The first emitted column is instead:

`full_chunk_0018 · col A` → `A vitam / B amenitatem / C iocunditatem ...`

There are also observable single-letter column-label gaps in **41 of 63** emitted chunks. Example: `full_chunk_0018` contains `A B C D F G H I J K L M O P`, omitting `E` and `N` in the public emitted sequence.

Thus the pinned JSON does not independently establish that its 895-column order is one complete historical Book-I restart cycle. Selecting a convenient subset would require additional source reconstruction beyond the frozen Stage-A acquisition rule.

## Stop decision

The preregistered pass class required one complete ordered restart cycle with:

- 24/24 cells in every code-bearing alphabet;
- deterministic sequence identity;
- no within-alphabet collision;
- source traceability sufficient for audit.

The current machine extraction does not meet those conditions.

Per the #209 stop rule, the project will **not** manually correct the 172 incomplete columns, the inverse collisions, or the sequence mapping merely to force TP1518-WA0 into the joint tournament.

TP1518-WA0 remains useful as a historically documented, mechanically reversible bounded architecture/control from #207. Its current target-admission lane is closed before first Voynich reveal.
