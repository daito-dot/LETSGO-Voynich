# Phase 64A implementation freeze

Status: **frozen before first scientific reveal**.

Normative design authority:

- `DECISION_64.md`
- `PLAN_A.md`

Implementation files:

- `phase64a_mg0.py` — MG0 order selection, smoothed character model, deterministic synthetic-vocabulary sampling and morphology diagnostics;
- `phase64a_inventory_autonomy.py` — ZL/IT arm reconstruction, exact A1-R2 generation/scoring and frozen source-arm/overall criteria;
- `phase64a_science.py` — official first-reveal entrypoint.

## Pre-result implementation correction

The first committed implementation body referred in its unused `main()` authority guard to a nonexistent short key:

`phase63a['across_fold']['robust']`

The actual committed Phase63A key is:

`phase63a['across_fold']['robust_to_heldout_vocabulary_removal']`

This was discovered by static authority inspection **before any Phase64A scientific source/result was computed**.

The official `phase64a_science.py` entrypoint uses the correct committed key. No model, metric, seed, fold, source, threshold, MG0 rule or A1 behavior changed. The underlying arm functions are unchanged.

## Non-scientific preflight

A separate push-triggered preflight was committed and run before first reveal. It:

1. byte-compiles all Phase64A Python implementation files;
2. verifies exact committed Phase62P/63A/63B result hashes and accepted authority keys;
3. runs MG0 only on synthetic toy token types;
4. verifies deterministic order selection/sampling and zero empirical-vocabulary membership queries in the sampler.

It does **not** download/read ZL3b or IT2a scientific source files and cannot reveal the Phase64A result.

Preflight head:

`916ebf3a5a5e0cdfc47a08492e5e9bb48666071a`

Preflight Actions run:

`33335257971`

All substantive preflight steps completed successfully.

## First-reveal rule

The first Phase64A scientific result must be produced only after this implementation and the read-only science workflow are committed. After the reveal, do not edit MG0/A1-R2 to repair any failure. Preserve the first result artifact/digest before recording interpretation.
