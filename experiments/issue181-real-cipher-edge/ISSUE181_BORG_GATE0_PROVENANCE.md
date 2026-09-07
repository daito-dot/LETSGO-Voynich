# Issue #181 Borg Gate0 provenance

Date: 2026-09-07
Parent: Issue #181 / Issue #172
Outcome: **GATE0_VALID**
Scientific state at completion: **NO EXTERNAL EDGE LIKELIHOOD REVEALED**

## Frozen external authority

- repository: `matthewdgreen/cipher_benchmark`
- pinned commit: `729aad62d12483c549e64a2541d4f9255538c8cf`
- source population: `benchmark/sources/borg/transcriptions/borg_*.canonical.txt`
- representation authority: `scripts/create_borg_benchmark.py`

The Borg benchmark conversion preserves physical source lines and the original transcription's whitespace-separated cipher groups, emitting the latter as literal `|`-delimited canonical units. Each cipher character is mapped to a stable `S###` atom.

Copiale was inspected before scoring and declared `NON-COMPOSABLE` for this R5 unit-edge question because its canonical transcription preserves physical lines but no corresponding unit boundary. No segmentation was invented to force compatibility.

## Frozen plan

`research/ISSUE181_REAL_CIPHER_EDGE_GATE0_PLAN_20260907.md`

Plan commit: `fed1f454a6ad025b7e97ed361a34d9615d43295c`

Gate0 auditor:

`experiments/issue181-real-cipher-edge/issue181_borg_gate0.py`

Auditor commit: `3bda00ee455cd10a599344995dc7d08de3c1d099`

Workflow commit: `56aaf44bb4a9b527e44927c50337fcb1c7708312`

## Gate0 execution

- workflow run: `34122654918`
- artifact ID: `10018805098`
- artifact ZIP SHA-256: `5b56023bd1c93a883b171851a8940fd1a6a4835dfcbfd28ba3d1e8ec6f91fe78`
- full Gate0 JSON SHA-256: `dc042f32db4d38977e51831bb952cb8e10488fe4ee31da6ec3aa87e1981dc8c0`

Synthetic score-free preflight passed before the pinned external corpus was audited.

## Support

- committed canonical files: 401
- non-empty pages: 397
- empty pages: 4
- physical non-empty lines: 7,195
- cipher units: 24,501
- canonical atoms: 120,191
- same-line immediate unit edges: 17,306
- immediate cross-line edges within page: 6,798
- global atom vocabulary: 77 (`S001`–`S077`)
- malformed units/atoms: 0

Frozen page folds are lexicographic page order modulo five. Support is balanced and non-zero in all folds:

| fold | pages | lines | units | same-line edges | cross-line edges |
|---:|---:|---:|---:|---:|---:|
| 0 | 80 | 1459 | 4874 | 3415 | 1379 |
| 1 | 80 | 1430 | 4888 | 3458 | 1350 |
| 2 | 79 | 1422 | 4849 | 3427 | 1343 |
| 3 | 79 | 1440 | 4933 | 3493 | 1361 |
| 4 | 79 | 1444 | 4957 | 3513 | 1365 |

## Firewall

Gate0 computed no POS likelihood, terminal→initial conditional likelihood, per-edge gain, `G_line`, `G_cross`, or real-cipher R5 classification. The next licensed operation is implementation and target-free synthetic verification of the already-frozen `alpha=0.01` five-fold scorer, followed by a separately frozen one-shot external reveal.
