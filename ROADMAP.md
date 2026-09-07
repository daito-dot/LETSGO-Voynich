# Research roadmap

Last consolidated: 2026-09-07

This file controls **current sequencing**, not historical exact methods. Frozen plans, first-reveal artifacts and phase reports remain authoritative for historical tests and numbers.

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

Active executable issue: **#151 — shared common-EVA edge table vs reading-specific residual**.

## Current frontier — consolidate the replicated observable edge before adding anything else

The predictive sequence program has now passed four successive narrowing gates:

1. Issue #125 factorized the line-local fixed-k2 expert into generic onset/position plus previous-terminal→next-initial identity;
2. Issue #134 absorbed the previously flexible residual into corrected B3 + that observable edge, leaving no selected RESET/LINE challenger contribution;
3. Issues #139/#145 independently replicated the edge on Takahashi/IT2a and made ZL3b/IT2a directly comparable under one common Basic-EVA representation;
4. Issue #148 transported the **literal** common-EVA edge table in both reading directions, positive 5/5 each and retaining about 96–98% of target-native gain.

Therefore the next question is not whether to add richer capacity. It is whether the current edge model can be simplified further.

Issue #151 asks:

> **Does either reading retain reproducible held-out edge information beyond one frozen reading-balanced common-EVA table?**

The first deliverable is score-free.

## Completed foundation

### 1. Token-internal construction — CLOSED

Issue #75 + OGH-A/B/C:

- residual R1 topology replicates across ZL3b and IT2a;
- a target-blind second-order occupied-slot successor grammar with 298 counted conditional probabilities is near the empirical-inventory ceiling;
- memoryless V2 is `9.7089061 bits/token`, with about 7.0 bits shape + 2.7 bits values.

No new occupancy-only R1 rung is currently licensed.

### 2. Boundary validity — COMPLETE FOR ZL3b + IT2a

Certain visible spaces behave as reproducible construction/production cuts. The exact observed cut beats nearby shifted cuts in both reading lineages.

This does not establish natural-language word boundaries.

### 3. Predictive-information budget — COMPLETE THROUGH B3

Corrected held-out code lengths:

- B0 V2 `9.7089061`;
- B1 local `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688 bits/token`.

Most longer-history gain is causal-prefix / prior-paragraph inventory rather than detailed long ordered memory.

### 4. Flexible residual localization — COMPLETE

Issue #118 found `G_context = +0.0178533 bit/token`, positive 5/5.

Issues #121/#123 localized useful short context to adjacent visible units inside the same source line; carrying it through a line break is harmful.

Issue #125 factorized the fixed-`k=2` line-local expert exactly into:

- generic line-position/onset support `+0.00889185`;
- immediate previous-terminal → current-initial identity `+0.02026956`.

Both are positive 5/5; EDGE2 and LINECONT2 are token-logp identical under the frozen representation.

### 5. Currier transport of the explicit edge — COMPLETE FOR THE ORIGINAL REPRESENTATION

Issue #127 established native usefulness in both Currier A and B while literal table transport was asymmetric.

Issue #130 removed the major source-support imbalance:

- 20 shared previous-terminal contexts;
- exactly 8,728 selected source edge events per Currier regime per seed;
- A→B seed passes `0/5`;
- B→A seed passes `5/5`;
- frozen classification **`MATCHED_TABLE_TRANSPORT: B→A ONLY`**.

This is predictive transport, not historical direction. Whether the asymmetry survives the later common-EVA stabilization is a future gate, not an inference from #130 or #148.

### 6. Augmented-core residual closure — COMPLETE

Issue #134:

- B3 mean `9.517268842963203 bits/token`;
- augmented observable core mean `9.451900585480233`;
- mean gain `+0.06536825748296984`, positive 5/5;
- selected `rho=[0.19,0.22,0.20,0.19,0.21]`;
- RESET and LINE final challenger weights `w=0` in every fold;
- `G_residual=[0,0,0,0,0]`;
- classification **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**.

Authority: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

A rich latent-state search is not licensed by this residual.

### 7. Independent IT2a edge replication — COMPLETE

Issue #139:

- classification **`INDEPENDENT EDGE REPLICATION PASSES`**;
- mean `G_identity_IT2a = +0.15211188542908544 bit/token`;
- positive 5/5;
- run `34061721332`, artifact `9997679250`, result SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`.

The architecture is no longer plausibly treated as a ZL3b-only transcription artifact under the shared EVA/IVTFF framework.

### 8. Common-representation dual-reading test — COMPLETE

Issue #145:

- classification **`COMMON-EVA EDGE ROBUST IN BOTH READINGS`**;
- ZL3b mean `+0.1336232955274749`, positive 5/5;
- IT2a mean `+0.16184998339508744`, positive 5/5;
- exact common representation uses 31 Basic-EVA atoms + END (`V=32`), maximal clean-run reset, fixed `k=2`, `alpha=.01`;
- EDGE2_COMMON equals full clean-run-contiguous k2 exactly at token-logp level;
- run `34062199123`, artifact `9997826217`, result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`.

### 9. Bidirectional literal table transport across readings — COMPLETE

Issue #148:

- classification **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**;
- ZL3b→IT2a mean `+0.15554823663346334 bit/token`, positive 5/5, retention `0.9610642730420239`;
- IT2a→ZL3b mean `+0.13039023868507016`, positive 5/5, retention `0.9758046916172639`;
- minimum previous-terminal context coverage `0.99935469993547` / `0.9988499137435307`;
- Gate0 result SHA-256 `f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf`;
- authoritative run `34073660425`;
- artifact `10001309613`;
- result JSON SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`;
- PR #150 merged as `b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131`.

The concrete mapping is therefore strongly shared across ZL3b/IT2a under the frozen common representation. This is not a claim of independent manuscripts or semantic identity.

## Active gate — Issue #151 shared common-EVA table

### Primary responsibility

Test whether separate reading-native edge tables are still predictively justified.

For each untouched physical-leaf fold, construct on the four training folds of **both** readings:

`C_SHARED = 0.5 * C_ZL3b + 0.5 * C_IT2a`.

The equal half-weights are frozen before target scoring. They preserve approximately one-reading evidence scale and avoid artificially doubling confidence because the same physical manuscript has two transcriptions.

`EDGE2_SHARED` is target-native in every non-edge factor. Only BODY `P(first_common_atom | previous_terminal_common_atom)` uses `C_SHARED`.

### Primary quantities

For target reading `T`:

`G_shared[T,f] = bits(POS2_TARGET) - bits(EDGE2_SHARED)`

`G_specific[T,f] = bits(EDGE2_SHARED) - bits(EDGE2_NATIVE_T)`

A reading-specific residual passes iff:

- mean `G_specific > 0`; and
- positive in at least `4/5` untouched folds.

A valid consolidation also requires the shared table itself to improve POS2 in both readings by the same mean-positive + 4/5 criterion.

### Frozen classes

1. `ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`
2. `ZL3B RETAINS READING-SPECIFIC EDGE INFORMATION`
3. `IT2A RETAINS READING-SPECIFIC EDGE INFORMATION`
4. `BOTH READINGS RETAIN READING-SPECIFIC EDGE INFORMATION`
5. `INVALID SHARED EDGE CONSOLIDATION`

No post-reveal rescue class.

### Gate0 — mandatory first deliverable

Before any `EDGE2_SHARED` target likelihood:

1. pin exact #145/#148 source, representation, fold, scorer/result authorities;
2. prove held-out physical leaves are absent from both readings' shared-table training counts;
3. reproduce target primary and run-body counts;
4. audit per-reading training edge counts and 32×32 cell/context support;
5. deterministically construct the `0.5/0.5` fractional count table on training data only;
6. audit target BODY previous-terminal context support without inspecting current first-atom outcomes;
7. run target-free synthetic tests of fractional-count smoothing;
8. freeze the exact decision classes and thresholds;
9. prove no held-out shared-table likelihood, `G_shared`, `G_specific` or classification was computed.

If authority/support fails, classify INVALID. Do not alter weights, smoothing, representation, exclusions or fallback after reveal.

## Decision fork after #151

### A. One shared table suffices

Promote the edge to one consolidated common-EVA observable table for compact-core work. Then test whether the Currier A/B literal-table asymmetry from #130 survives this stabilized common representation.

### B. A reading-specific residual remains

Retain the large shared component but preserve the justified reading-native correction. Characterize its source only after the primary result is frozen.

### C. Invalid

Stop without target interpretation.

## High-value follow-ups

After #151, and only as licensed by its result:

1. **Common-EVA Currier A↔B table transport** — directly retest whether #130's B→A-only asymmetry survives representation stabilization.
2. **Compact observable-core consolidation** — if one shared table suffices, replace reading-specific edge responsibility with the shared table in a future frozen core.
3. **Reversible/inverse mechanism tournaments** — require candidate mechanisms to reproduce established surface responsibilities without target-aware repair.
4. **Externally anchored content tests** — mappings fixed independently of Voynichese similarity.
5. **Issue #84 Phase D** only where it answers an identifiable question not superseded by Issue #88.

A rich latent-state model is not on the active path unless a new prospectively defined predictive residual independently reopens that license.

## Parked / historical lanes

- generic finite-memory/copy-mutate exploration (#24): theory background, not the current implementation frontier;
- music-motif/self-similarity methods (#25): exploratory and separate; no direct-musical interpretation is supported;
- older R1 generator ladders (#58/#75): completed history, not current frontier.

## Research boundary

Nothing on this roadmap currently establishes plaintext, language, semantic absence, cipher identity/key, natural-language word boundaries, author/scribe causation, historical direction, hoax/artificial origin, a historical production algorithm or decipherment.
