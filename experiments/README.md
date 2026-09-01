# Experiments

This directory contains reproducible analyses from the ongoing research program.

## Organization

Experiments are grouped by phase. A phase number records research chronology; it is not a confidence score.

Each phase should preferably contain:

- a development/report Markdown file
- the script(s) required to reproduce the analysis
- compact JSON/CSV result files
- explicit notes on whether targets were exploratory, used for model selection, or held out

Generated caches, large third-party corpora, manuscript images, and duplicated transcription files should normally stay out of Git.

## Token-construction lane (2026-09)

- `occupancy-graph*/` — #58A–#58D: the replicated 66-edge residual 12-slot token-construction graph.
- `joint-constraint-tournament/` — Issue #68: first joint R1–R5 tournament (Naibbe passes R1 only).
- `naibbe-r1-decomposition-v2/` — Issue #72: Naibbe R1 causal decomposition (C1 / PT / FI).
- `occupancy-generation-hierarchy/` — OGH-A: minimal occupancy-generation ladder G0–G6; a 78-parameter last-occupied-slot successor grammar passes the Issue #68 R1 gate on both readings and skeletons. Complements Issue #75 (`minimal-occupancy-generator/` on its branch).

## Current consolidation scope

The first public archive concentrates on Phases 44–52 because these contain the current mechanism-comparison frontier:

- Phase 44 — matched generator benchmark, predictive code length, copy/locality tests
- Phase 45 — paragraph-local structure and dynamic-state correction
- Phase 46 — medieval Latin temporal-shape control
- Phase 47 — paragraph-boundary edit-operation/zone decomposition
- Phase 48 — cross-linguistic near-form pilot
- Phase 49 — constructed/programming language pilot
- Phase 50 — formal systems and finite-state DSL
- Phase 51 — frozen DSL falsification
- Phase 52 — document/genre confound tests

Older phases will be added as their historical records are normalized. The hypothesis ledger already preserves their accepted/rejected consequences.

## Reproduction warning

Some historical scripts were written during exploratory work and may contain local filenames. Treat their phase report as part of the executable specification and verify input identity. New contributions should prefer command-line input paths and pinned dependencies.
