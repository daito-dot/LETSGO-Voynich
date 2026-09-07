# Issue #181 Borg external edge reveal provenance

Date: 2026-09-07
Parent: Issue #181 / Issue #172
Outcome: **EXTERNAL LINE-LOCAL EDGE**

## Chronology

Gate0 was completed before any external edge likelihood was computed. It fixed the Borg canonical authority, 397 non-empty pages, 77-atom inventory, deterministic five-fold page split, same-line/cross-line supports, and the absence of malformed representation items.

The scorer was then frozen at commit `93aa21fbf97bd3f768ce00828f86f4157405a43d` and target-free synthetic preflight passed in workflow run `34122961266`.

The complete pre-reveal research state was frozen at:

`a4c81e28116351e817db99dbc673e858226c4ff0`

The reveal workflow was added later but explicitly checked out that exact pre-reveal state before scoring.

## External authority

- repository: `matthewdgreen/cipher_benchmark`
- pinned commit: `729aad62d12483c549e64a2541d4f9255538c8cf`
- source: committed Borg canonical transcriptions
- canonical units: literal `|` groups preserved by the benchmark converter
- physical lines: canonical newlines

Copiale remained `NON-COMPOSABLE` for this unit-edge test because its canonical representation does not contain the corresponding unit delimiter. No segmentation was created after inspection.

## Reveal authority

- workflow run: `34123034953`
- workflow trigger commit: `c3eefde5f00e12efb2c37e4cdc46d3108353558d`
- exact checked-out scientific state: `a4c81e28116351e817db99dbc673e858226c4ff0`
- artifact ID: `10018952850`
- artifact ZIP SHA-256: `a933c729e84e4caa224ec826f687e94cf20ffc7eae90b0683374022658c50e7c`
- full result JSON SHA-256: `d5642d108bdbbbbc3dd70d26d65a605a7a69a59ace0c8a92a250bc981a7b143d`

The workflow re-ran `SYNTHETIC_EDGE_PREFLIGHT_OK` immediately before fetching the pinned external corpus.

## Same-line edge

Frozen comparison: `POS_BODY(Y)` versus `EDGE_BODY(Y|X)`, where X is the immediately previous cipher-unit terminal atom and Y is the current unit initial atom.

Held-out fold gains in bits/edge:

- fold 0: `+0.0203527472`
- fold 1: `+0.0519321831`
- fold 2: `+0.0733948866`
- fold 3: `+0.0685062497`
- fold 4: `+0.0482047568`

Mean:

`G_line = +0.0524781647 bits/edge`

Positive folds: `5/5`.

Frozen pass rule therefore gives:

`G_line PASS`.

## Cross-line edge

Frozen comparison: `POS_LINESTART(Y)` versus `EDGE_CROSS(Y|X)`, where X is the final cipher-unit terminal atom of the preceding physical line and Y is the first unit initial atom on the next physical line.

Held-out fold gains:

- fold 0: `-0.0329079926`
- fold 1: `-0.1358907813`
- fold 2: `-0.0549554745`
- fold 3: `-0.0846607988`
- fold 4: `-0.0718251941`

Mean:

`G_cross = -0.0760480483 bits/edge`

Positive folds: `0/5`.

Frozen pass rule therefore gives:

`G_cross FAIL`.

## Mechanical classification

The preregistered class logic was:

- G_line PASS + G_cross FAIL -> `EXTERNAL LINE-LOCAL EDGE`
- both PASS -> `EXTERNAL EDGE WITH CROSS-LINE CONTINUATION`
- G_line FAIL -> `NO ROBUST EXTERNAL EDGE`

Observed classification:

> **EXTERNAL LINE-LOCAL EDGE**

The page-level non-gating diagnostic is also broad rather than confined to a few pages: 61.96% of pages with a same-line event have positive held-out mean gain.

## Interpretation

This is a substantive external compatibility result. A known historical monoalphabetic ciphertext manuscript exhibits the same qualitative topology targeted by Voynich R5: previous-unit terminal identity improves next-unit initial prediction within physical lines, while carrying the same identity across physical line breaks is harmful under held-out scoring.

It does **not** establish that monoalphabetic substitution creates this topology. A static substitution can preserve source-side dependencies, and Borg's canonical unit grouping and manuscript lineation are also part of the observed surface. The result therefore weakens any attempt to treat R5 alone as evidence against ciphertext, but does not promote Borg's cipher family as a Voynich candidate.

## Next licensed question

Per the frozen Issue #181 consequence fork, the next step is a separate external source-attribution phase using Borg's solved plaintext/key/alignment evidence to ask where this line-local topology originates:

- plaintext/source sequence;
- cipher-unit grouping;
- physical lineation;
- encryption transform;
- or their interaction.

That source-attribution plan must be frozen before its effect is inspected. No Voynich target scoring is licensed by Issue #181.
