# Issue #98 order correction protocol — corrected Phase 1 replay

Date: 2026-09-06
Status: **FROZEN BEFORE CORRECTED PREDICTIVE SCORING**
Parent: Issue #88
Implementation issue: #98
Entry authority: `ORDER_AUDIT_PROVENANCE.md`

## Purpose

Gate 0 established that the historical prediction-only Phase 1/2A/2B path used a lexical item/document ordering that is not a valid causal-order authority for all ZL3b paragraphs. The correction must repair ordering only and must not use old surface-target outcomes to improve any model.

This protocol freezes the first repair step: correct causal ordering, then replay Phase 1 under the exact previously declared model families and grids.

## Correction authority

The corrected Voynich causal order is defined by the frozen raw ZL3b source itself:

1. numeric physical leaf remains the outer history/reset unit;
2. within a numeric physical leaf, page-side/document order is the order in which raw ZL3b page headers occur;
3. within a page-side/document, paragraph order is the numeric suffix in parser item ids (`p1,p2,...`), not lexical string order;
4. line and token order inside each paragraph is unchanged.

No semantic, Currier, section, scribe, image or target-statistic information enters this authority.

The corrected loader must hard-fail if a parsed page-side is absent from the raw page-header authority, a paragraph id lacks a numeric suffix, duplicate item ids exist, or the corrected order fails the score-free Gate-0 invariants.

## What does not change

- frozen ZL3b bytes/blob;
- parser and accepted-token population;
- five physical-leaf folds and membership;
- V2 token-internal model;
- exact edit-distance-1 neighbour relation;
- Phase-1 B1/B2 candidate grids;
- Phase-1 B3 state families and lambda grid;
- Phase-1 B4 byte families and grids;
- nested-likelihood selection and tie rules;
- prediction-only firewall.

## Corrected Phase 1 replay

Replay the exact Phase-1 selection/scoring machinery on corrected item order.

The historical Phase-0 B1 numerical regression is **not** a pass gate after an order correction because B1 is itself order-sensitive. It is retained only as an old-vs-corrected comparison.

The following remain hard gates:

- B0 V2 code length reproduces the historical value in every fold to `1e-9` because B0 is order-free;
- parser-accepted and visible-token counts are unchanged;
- fold identity is unchanged;
- corrected order matches raw page-side order plus numeric paragraph order;
- all Phase-1 model/hyperparameter selection uses only nested training likelihood.

Report corrected B0/B1/B2/B3/B4 code lengths, all selected parameters, foldwise gains, and the original Phase-1 classification rule without changing thresholds.

## Downstream gate

After corrected Phase 1:

- if the corrected B2 winner remains `H=ALL, tau=128, pi=.30` in all five folds, the historical Phase-2A reference topology remains licensed for an exact corrected-order replay; corrected B1 per-fold mixture weights replace the invalid old-order local anchor values where the Phase-2A conditional control requires the current Phase-1 local winner;
- if any fold selects a different B2 architecture, **stop before Phase 2A scoring** and freeze a separate correction protocol defining how the corrected Phase-1 winner becomes the Phase-2A reference. Do not silently retain the old B2 architecture.

Phase 2B is not replayed until corrected Phase 2A is frozen and evaluated.

## Firewall

No S1/S2/H62/R1, Issue #84 target interval, proposed plaintext, semantic label, page imagery or latent state may guide the correction or corrected replay.

This is a correction/reproducibility exercise, not a new model search.