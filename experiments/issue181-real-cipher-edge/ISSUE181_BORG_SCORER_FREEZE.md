# Issue #181 Borg scorer freeze

Date: 2026-09-07
Parent: Issue #181 / Issue #172
State: **FROZEN BEFORE EXTERNAL EDGE REVEAL**

## Gate0 authority

- external repository: `matthewdgreen/cipher_benchmark`
- external pinned commit: `729aad62d12483c549e64a2541d4f9255538c8cf`
- Gate0 run: `34122654918`
- Gate0 artifact ID: `10018805098`
- Gate0 full JSON SHA-256: `dc042f32db4d38977e51831bb952cb8e10488fe4ee31da6ec3aa87e1981dc8c0`
- Gate0 classification: `GATE0_VALID`
- non-empty pages: 397
- same-line immediate edges: 17,306
- cross-line immediate edges: 6,798
- atom vocabulary: 77
- malformed representation items: 0

Gate0 computed no edge likelihood or gain.

## Frozen scorer

Scorer:

`experiments/issue181-real-cipher-edge/issue181_borg_edge_scorer.py`

Scorer commit:

`93aa21fbf97bd3f768ce00828f86f4157405a43d`

Scorer Git blob:

`d5a0a058466f002c82e3bb4f528b22dd0f707a34`

Frozen scientific contract:

`research/ISSUE181_REAL_CIPHER_EDGE_GATE0_PLAN_20260907.md`

Key immutable choices:

1. Borg only for the primary R5 unit-edge comparison; Copiale remains `NON-COMPOSABLE` because no matching cipher-unit delimiter exists in its canonical representation.
2. every non-empty canonical newline is a physical line;
3. literal `|` is the only cipher-unit delimiter;
4. atoms must match `S###`/`S####` exactly;
5. 397 non-empty pages are sorted lexicographically and assigned `index mod 5` to five page-disjoint folds;
6. vocabulary is the complete target-blind canonical atom inventory fixed before fold scoring;
7. additive smoothing is fixed at `alpha=0.01`;
8. same-line comparison is `POS_BODY(Y)` versus `EDGE_BODY(Y|X)` where X is previous unit terminal and Y is current unit initial;
9. cross-line comparison is `POS_LINESTART(Y)` versus `EDGE_CROSS(Y|X)` where X is the previous physical line's final unit terminal and Y is the next physical line's first unit initial;
10. shared token-internal factors are not re-estimated because they cancel in this first-symbol likelihood difference;
11. a quantity passes only if its five-fold mean is positive and at least 4/5 fold means are positive;
12. no hyperparameter fitting, page selection, symbol subgrouping, plaintext alignment, cipher-key use, or Voynich target access is permitted.

Frozen classes:

- `EXTERNAL LINE-LOCAL EDGE`: G_line passes, G_cross fails.
- `EXTERNAL EDGE WITH CROSS-LINE CONTINUATION`: both pass.
- `NO ROBUST EXTERNAL EDGE`: G_line fails.
- `INVALID EXTERNAL REPRESENTATION`: authority/support/parser failure.

## Target-free preflight

Synthetic-only workflow:

- run: `34122961266`
- head: `5a71f07f024cf05a4ffc4240ba9ccc513b0a1092`
- conclusion: `success`
- terminal marker: `SYNTHETIC_EDGE_PREFLIGHT_OK`

The synthetic fixture exercised five-fold splitting, additive-smoothed position and conditional tables, same-line and cross-line pathways, and mechanical classification without reading Borg target gains.

## Reveal license

The next licensed operation is one execution of the frozen scorer against the pinned Borg canonical authority. The reveal workflow must check out an exact pre-reveal research commit and assert the external benchmark commit before scoring.

If a runtime/transport failure occurs before result emission, only a parser/transport repair that leaves population, folds, smoothing, model factors, pass logic and classes unchanged is admissible, and it must be documented before rerun.

After successful reveal, do not change alpha, folds, unit boundaries, pages, symbol inventory, or sign-stability criteria. A positive result is an external compatibility result for a historical ciphertext document, not evidence that monoalphabetic substitution itself causes the topology and not a Voynich decipherment claim.
