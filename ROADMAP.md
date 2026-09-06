# Research roadmap

Last consolidated: 2026-09-06

This file controls **current sequencing**, not historical exact methods. Frozen plans, first-reveal artifacts and phase reports remain authoritative for historical tests and numbers.

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

Active executable issue: **#139 — independent IT2a replication of the same-line terminal→initial edge**.

## Current frontier — replicate the explicit edge independently

Issue #134 has closed the previously measured flexible residual for its prospectively frozen model-class comparison.

The immediate question is now:

> **Does the same-line previous-terminal → next-initial predictive architecture survive on independent Takahashi/IT2a when source, line mapping, symbol treatment, folds, smoothing and decision rule are frozen before target scoring?**

Issue #139 owns this gate. Its first deliverable is score-free. No IT2a edge gain may be used to choose normalization, exclusions, folds, symbol representation, smoothing, fallback or model family.

## Completed foundation

### 1. Token-internal construction — CLOSED

Issue #75 + OGH-A/B/C:

- residual R1 topology replicates across ZL3b and independent IT2a;
- a target-blind second-order occupied-slot successor grammar with 298 counted conditional probabilities is near the empirical-inventory ceiling;
- memoryless V2 is `9.7089061 bits/token`, with about 7.0 bits shape + 2.7 bits values;
- memoryless token generation does not reproduce the major cross-token responsibilities.

No new occupancy-only R1 rung is currently licensed.

### 2. Predictive-information budget — COMPLETE THROUGH B3

After source-order correction:

- B0 V2 `9.7089061`;
- B1 local `9.5943670`;
- B2 longer history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688 bits/token`.

Cross-token information is real but small relative to token-internal information.

### 3. Long-history source attribution — COMPLETE FOR CURRENT FAMILIES

The dominant longer-history increment is mostly causal-prefix / prior-paragraph inventory, with a smaller actual-order residual. Same-side and cross-side prior history both remain predictive.

### 4. Visible-space boundary validity — COMPLETE FOR ZL3b + IT2a

Certain visible spaces behave as reproducible construction/production cuts. The exact cut beats nearby shifted cuts in both independent readings.

This validates the tested production boundary, not a natural-language word interpretation.

### 5. Flexible residual localization — COMPLETE

Issue #118:

- `G_context = +0.0178533 bit/token`, positive 5/5;
- class `ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED`.

Issue #121 same-order control:

- boundary-edge residual `+0.0106322`, positive 5/5.

Issue #123 reset-scope control:

- same-line continuation `+0.0291614`, 5/5;
- beyond-line continuation `-0.0185292`, 0/5.

Issue #125 exact decomposition:

- generic line-position/onset `+0.00889185`, 5/5;
- previous-terminal identity `+0.02026956`, 5/5;
- EDGE2 and LINECONT2 token-logp identical under fixed `k=2`.

The tested flexible line-local expert therefore reduces exactly to observable line position plus immediate terminal→initial identity.

### 6. Currier transport of the explicit edge — COMPLETE

Issue #127:

- native edge useful in A and B;
- scalar strength compatible bidirectionally when target table is supplied;
- literal table transport B→A only;
- exact table+strength transport none.

Issue #130 support-matched follow-up:

- 20 shared previous-terminal contexts;
- exactly 8,728 selected source edge events per Currier regime per seed;
- five outcome-blind matched selections;
- A→B seed passes `0/5`, grand mean `+0.00693954`;
- B→A seed passes `5/5`, grand mean `+0.02697082`;
- frozen classification **`B→A ONLY`**.

The table asymmetry survives removal of the major A/B source-support imbalance.

### 7. Augmented observable-core residual closure — COMPLETE

Issue #134 prospectively froze corrected B3 plus the explicit edge and Currier fallback policy before scoring.

Gate0:

- passed before predictive scorer creation;
- Gate result JSON SHA-256 `3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1`.

First successful reveal:

- scorer commit `dbd787a457659b7d833dc06c3931f937031172b8`;
- run `34035108074` — SUCCESS;
- artifact `9990011421`;
- result JSON SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

Mean bits/token:

- B3 `9.517268842963203`;
- augmented observable core `9.451900585480233`;
- MIX_RESET `9.451900585480233`;
- MIX_LINE `9.451900585480233`.

Augmented core improves B3 by mean `+0.06536825748296984 bit/token`, positive 5/5, with `rho=[.19,.22,.20,.19,.21]`.

Primary residual:

- `G_residual=[0,0,0,0,0]`;
- mean `0`;
- positive outer folds `0/5`;
- RESET and LINE final challenger `w=0` in all five folds.

Frozen classification:

**`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**.

Consequence: rich latent-state work is not licensed by the current residual program.

## Active gate — Issue #139 independent IT2a edge replication

### Replication responsibility

Test the architecture established in Issue #125 without using IT2a target outcomes to redesign it.

The score-free contract must freeze:

1. exact independent Takahashi/IT2a source/version/hash and provenance;
2. mapping to physical leaves and source lines;
3. uncertainty/editorial-symbol treatment and visible-certain-space policy;
4. physical-leaf outer-fold authority;
5. target population and finite support;
6. literal symbol representation;
7. line reset and line-start/body onset representation;
8. previous-terminal-conditioned next-initial identity edge;
9. fixed short-order continuation representation;
10. smoothing/fallback;
11. held-out comparison and stability rule;
12. leakage firewall.

### Primary comparison

`G_identity_IT2a = bits(POS2) - bits(EDGE2)`.

POS2 carries generic line-position/onset responsibility. EDGE2 differs only by conditioning the line-body first-symbol prediction on the immediately previous visible unit's terminal identity.

### Frozen classes

#### `INDEPENDENT EDGE REPLICATION PASSES`

The preregistered held-out stability rule passes.

Consequence: the edge architecture is less plausibly a ZL3b-specific transcription artifact. Literal cross-transcription table equality remains a separate question.

#### `INDEPENDENT EDGE REPLICATION FAILS`

The preregistered rule fails.

Consequence: downgrade the edge to ZL3b-lineage-specific or representation-sensitive structure before using it as a manuscript-wide production responsibility.

#### `INVALID INDEPENDENT REPLICATION`

Source/fold/line/boundary/support authority or faithful frozen representation cannot be established.

Consequence: stop without interpreting the target.

No fourth post-reveal class.

## High-value follow-ups after Issue #139

1. **Reversible/inverse mechanism tournaments** that must satisfy the constrained surface-production responsibilities without target-aware repair.
2. **Localized externally anchored content tests** where the external mapping is fixed independently of Voynichese similarity.
3. **Issue #84 Phase D** only where it addresses a question not superseded by Issue #88 and uses identifiable metadata.
4. If IT2a replication passes, a separately preregistered cross-transcription table/representation comparison may ask which parts of the edge mapping are transcription-stable.

## Parked / historical lanes

- latent-state sequence modeling: not licensed after Issue #134 residual closure;
- generic finite-memory/copy-mutate exploration (#24): theory background, not current executable frontier;
- music-motif/self-similarity methods (#25): exploratory and separate; no direct-musical interpretation supported;
- older R1 generator ladders (#58/#75): completed scientific history.

## Research boundary

Nothing on this roadmap currently establishes:

- plaintext or a natural language;
- semantic absence;
- a cipher family/key;
- natural-language word boundaries;
- author/scribe causation;
- hoax/artificial origin;
- a historical production algorithm;
- decipherment.

The current job is narrower: test whether the compact observable terminal→initial architecture is transcription-independent before promoting it to a manuscript-wide production responsibility.
