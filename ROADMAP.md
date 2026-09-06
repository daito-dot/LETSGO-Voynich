# Research roadmap

Last consolidated: 2026-09-06

This file controls **current sequencing**, not historical exact methods. Frozen plans, first-reveal artifacts and phase reports remain authoritative for historical tests and numbers.

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

Active executable issue: **#139 — independent IT2a replication of the same-line terminal→initial edge**.

## Current frontier — independent replication before adding capacity

Issue #134 closed the tested ZL3b residual after the observable edge was incorporated into corrected B3.

Frozen classification:

> **NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE**

The primary residual was `[0,0,0,0,0] bits/token`. Nested validation selected final `w=0` for both flexible challenger families in all five outer folds. The augmented observable core improved B3 by mean `0.0653682575 bits/token`, positive 5/5.

Therefore the current program does not license a rich latent-state search. The next question is whether the compact observable edge is transcription-lineage robust.

Issue #139 asks:

> **Does the fixed same-line previous-terminal → next-initial edge replicate on independent Takahashi/IT2a data when the representation is frozen before target scoring?**

Its first deliverable is score-free: source/version/hash, physical-leaf and source-line mapping, uncertainty policy, target population, representation, folds, smoothing, support diagnostics and the primary pass/fail rule must be fixed before any IT2a target gain is inspected.

## Completed foundation

### 1. Token-internal construction — CLOSED

Issue #75 + OGH-A/B/C:

- residual R1 topology replicates across ZL3b and independent IT2a;
- a target-blind second-order occupied-slot successor grammar with 298 counted conditional probabilities is near the empirical-inventory ceiling;
- memoryless V2 is `9.7089061 bits/token`, with about 7.0 bits shape + 2.7 bits values.

No new occupancy-only R1 rung is currently licensed.

### 2. Boundary validity — COMPLETE FOR ZL3b + IT2a

Certain visible spaces behave as reproducible construction/production cuts. The exact observed cut beats nearby shifted cuts in both transcription lineages.

This does not establish natural-language word boundaries.

### 3. Predictive-information budget — COMPLETE THROUGH B3

Corrected held-out code lengths:

- B0 V2 `9.7089061`;
- B1 local `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688 bits/token`.

Most longer-history gain is causal-prefix / prior-paragraph inventory rather than detailed long ordered memory.

### 4. Flexible residual localization — COMPLETE

Issue #118 found a small matched flexible residual beyond B3:

- `G_context = +0.0178533 bit/token`, positive 5/5.

Issues #121/#123 localized useful short context to adjacent visible units inside the same source line; carrying it through a line break is harmful.

Issue #125 factorized the fixed-`k=2` line-local expert exactly into:

- generic line-position/onset support;
- immediate previous-terminal → current-initial identity.

Identity gain: `+0.02026956 bit/token`, positive 5/5. EDGE2 and LINECONT2 are token-logp identical under that frozen representation.

### 5. Currier transport of the explicit edge — COMPLETE FOR CURRENT QUESTION

Issue #127 established native usefulness in both Currier A and B while literal table transport was asymmetric.

Issue #130 removed the major source-support imbalance:

- 20 shared previous-terminal contexts;
- exactly 8,728 selected source edge events per Currier regime per seed;
- A→B seed passes `0/5`;
- B→A seed passes `5/5`;
- frozen classification **`B→A ONLY`**.

This is predictive transport, not historical direction.

### 6. Augmented-core residual closure — COMPLETE

Issue #134 preregistered corrected B3 plus the observable same-line edge, including Currier A/B handling and fallback, before any new residual reveal.

First reveal:

- B3 mean `9.517268842963203 bits/token`;
- augmented observable core mean `9.451900585480233`;
- mean gain `+0.06536825748296984`, positive 5/5;
- selected `rho=[0.19,0.22,0.20,0.19,0.21]`;
- RESET and LINE final challenger weights `w=0` in every fold;
- `G_residual=[0,0,0,0,0]`;
- classification **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**.

Authority is archived in `experiments/predictive-information/residual-gate/ISSUE134_FIRST_REVEAL_PROVENANCE.md`.

## Active gate — Issue #139 independent IT2a replication

### Primary responsibility

Replicate the architecture, not literal ZL3b table values.

Primary quantity:

`G_identity_IT2a = bits(POS2) - bits(EDGE2)`

where POS2 retains generic line-position/onset responsibility and EDGE2 adds only immediately previous terminal identity to line-body first-symbol prediction.

### Score-free requirements

Before target scoring, freeze:

1. exact IT2a/Takahashi source and hash;
2. physical-leaf/source-line mapping;
3. uncertainty/editorial-symbol treatment;
4. visible certain-space policy;
5. outer folds and target population;
6. literal symbol representation;
7. Issue #125 architecture carried over without outcome-driven repair;
8. smoothing/fallback/support policy;
9. stability rule and exactly three decision classes;
10. leakage/firewall checks.

### Decision fork

#### A. Independent edge replication passes

The architecture is less plausibly a ZL3b-specific transcription artifact. Literal table equality across transcriptions remains a separate question.

#### B. Independent edge replication fails

Downgrade the edge from transcription-independent structure to ZL3b-lineage-specific or representation-sensitive structure. Audit the mismatch before treating the edge as manuscript-wide responsibility.

#### C. Independent replication invalid

Stop if source/fold/line/boundary/support authority or a faithful frozen representation cannot be established.

No post-reveal rescue class.

## High-value follow-ups after #139

Ordering depends on the replication result, but the next families are already constrained:

1. **Compact observable-model consolidation** across transcription lineages if #139 passes.
2. **Reversible/inverse mechanism tournaments** that must satisfy the established surface-production responsibilities without target-aware repair.
3. **Externally anchored content tests** where mappings are fixed independently of Voynichese similarity.
4. **Issue #84 Phase D** only where it answers an identifiable question not superseded by Issue #88.

A rich latent-state model is not on the active path unless a new prospectively defined predictive residual independently reopens that license.

## Parked / historical lanes

- generic finite-memory/copy-mutate exploration (#24): theory background, not the current implementation frontier;
- music-motif/self-similarity methods (#25): exploratory and separate; no direct-musical interpretation is supported;
- older R1 generator ladders (#58/#75): completed history, not current frontier.

## Research boundary

Nothing on this roadmap currently establishes plaintext, language, semantic absence, cipher identity/key, natural-language word boundaries, author/scribe causation, hoax/artificial origin, a historical production algorithm or decipherment.
