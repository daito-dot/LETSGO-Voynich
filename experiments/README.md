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
