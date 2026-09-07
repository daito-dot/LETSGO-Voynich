# Research roadmap

Last consolidated: 2026-09-07

This file controls **current sequencing**, not historical exact methods. Frozen plans, first-reveal artifacts and phase reports remain authoritative for historical tests and numbers.

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

Active executable issue: **#161 — global next-initial bias vs context-specific Currier edge interaction**.

## Current frontier — compress the Currier gate before adding capacity

The predictive sequence program has now passed a sequence of narrowing gates:

1. Issue #125 factorized the line-local fixed-k2 expert into generic onset/position plus previous-terminal→next-initial identity;
2. Issue #134 absorbed the previously flexible residual into corrected B3 + that observable edge, leaving no selected RESET/LINE challenger contribution;
3. Issues #139/#145 independently replicated the edge on Takahashi/IT2a and made ZL3b/IT2a directly comparable under one common Basic-EVA representation;
4. Issue #148 transported the **literal** common-EVA edge table in both reading directions, retaining about 96–98% of target-native gain;
5. Issue #151 showed one fixed reading-balanced table suffices across ZL3b/IT2a; neither reading retains a robust table-specific residual;
6. Issue #155 showed the stabilized literal table does not transport across Currier A/B in either direction under matched support;
7. Issue #158 isolated that difference directly: the observable Currier label adds robust held-out edge information in both A and B, independently in both readings.

Therefore the next question is not whether to add richer hidden capacity. It is whether the Currier split can be **compressed**.

Issue #161 asks:

> **Can the Currier A/B edge contrast be explained by a context-invariant next-initial atom bias, or does a genuine previous-terminal × next-initial Currier interaction remain?**

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

Both are positive 5/5; EDGE2 and LINECONT2 are token-logp identical.

### 5. Augmented-core residual closure — COMPLETE

Issue #134:

- B3 mean `9.517268842963203 bits/token`;
- augmented observable core mean `9.451900585480233`;
- mean gain `+0.06536825748296984`, positive 5/5;
- RESET and LINE final challenger weights `w=0` in every fold;
- `G_residual=[0,0,0,0,0]`;
- classification **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**.

Authority: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

A rich latent-state search is not licensed by this residual.

### 6. Independent IT2a edge replication — COMPLETE

Issue #139:

- classification **`INDEPENDENT EDGE REPLICATION PASSES`**;
- mean `G_identity_IT2a = +0.15211188542908544 bit/token`;
- positive 5/5;
- run `34061721332`, artifact `9997679250`, result SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`.

### 7. Common-representation dual-reading test — COMPLETE

Issue #145:

- classification **`COMMON-EVA EDGE ROBUST IN BOTH READINGS`**;
- ZL3b mean `+0.1336232955274749`, positive 5/5;
- IT2a mean `+0.16184998339508744`, positive 5/5;
- fixed `k=2`, `alpha=.01`, common Basic-EVA with 31 atoms + END (`V=32`);
- run `34062199123`, artifact `9997826217`, result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`.

### 8. Bidirectional literal table transport across readings — COMPLETE

Issue #148:

- classification **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**;
- ZL3b→IT2a mean `+0.15554823663346334`, positive 5/5, retention `0.9610642730420239`;
- IT2a→ZL3b mean `+0.13039023868507016`, positive 5/5, retention `0.9758046916172639`;
- run `34073660425`, artifact `10001309613`, result SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`.

### 9. Reading-shared table consolidation — COMPLETE

Issue #151:

- classification **`ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`**;
- ZL3b shared gain `+0.13564574057416792`, positive 5/5;
- IT2a shared gain `+0.16380858130203818`, positive 5/5;
- ZL3b native-over-shared residual `-0.002022445046693022`, positive 3/5 — FAIL;
- IT2a residual `-0.001958597906950743`, positive 1/5 — FAIL;
- run `34074437422`, artifact `10001563139`, result SHA-256 `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`.

Reading lineage is therefore not retained as an edge-table gate under the frozen common representation.

### 10. Common-EVA Currier table transport — COMPLETE

Issue #155:

- classification **`COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`**;
- A→B: ZL3b `-0.2992311805`, IT2a `-0.2986494755`, positive 0/5;
- B→A: ZL3b `-0.3753370873`, IT2a `-0.3873299031`, positive 0/5;
- same-regime matched edge gain remains positive for A and B in both readings;
- run `34075146845`, artifact `10001781210`, result SHA-256 `041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737`;
- PR #157 merge `6bd7c6fadb8fc590052496299c13da24f88585a2`.

This replaces the old #130 B→A-only result as the current common-EVA Currier transport picture. Predictive transport does not establish historical direction.

### 11. Incremental Currier gate — COMPLETE

Issue #158 uses exact rational support-matched A/B tables and a fixed regime-neutral pooled table:

`C_POOL = 0.5*C_A^MATCH + 0.5*C_B^MATCH`.

A/B/POOL have identical effective mass separately within every retained previous-terminal context.

Frozen classification:

> **`CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`**

Currier A:

- ZL3b mean `G_Currier = +0.06327673406664047`, positive 4/5;
- IT2a `+0.06782616617812458`, positive 4/5.

Currier B:

- ZL3b `+0.1012061292632481`, positive 5/5;
- IT2a `+0.10456811219559015`, positive 5/5.

Cross-reading differences are small: A `-0.004549432111484106`, B `-0.0033619829323420503 bit/token`.

Authority:

- Gate result SHA-256 `605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099`;
- Gate merge / PR #159 `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- scorer blob `e7a70a10dd7b663f3482993b0adfa8f804816158`;
- first-reveal run `34076400927`;
- artifact `10002205049`;
- result SHA-256 `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`;
- PR #160 merge `1741bed875a582594dc797ef18e30dd2ef3351ce`.

The current minimal edge responsibility is **reading-independent architecture + Currier-conditioned literal table**.

## Active gate — Issue #161 outcome-only vs context-specific Currier factorization

### Primary responsibility

Test whether the Currier distinction can be compressed from a full context×outcome table change to a context-invariant outcome bias.

For each outer fold, using only the exact Issue #158 training rational tables:

`G_R(y) = Σ_c C_R^MATCH(c,y)`

`G_POOL(y) = Σ_c C_POOL(c,y)`

and the fixed training-only multiplier:

`W_R(y) = (G_R(y)+alpha)/(G_POOL(y)+alpha)`, with `alpha=.01`.

For retained context `c`:

`P_OUTCOME_R(y|c) ∝ P_POOL(y|c) * W_R(y)`.

The probability is normalized over the frozen 32 outcomes. This is a Currier×outcome main-effect model; it contains **no Currier×previous-terminal×outcome interaction**.

### Frozen target comparison

For each target reading `T` and Currier regime `R`:

- `EDGE_POOL_T,R` — exact Issue #158 pooled edge;
- `EDGE_OUTCOME_T,R` — pooled edge plus the fixed outcome-only multiplier;
- `EDGE_REGIME_T,R` — exact Issue #158 target-regime matched table.

All non-edge factors are identical.

### Primary quantities

`G_outcome[T,R,f] = bits(EDGE_POOL) - bits(EDGE_OUTCOME)`

`G_interaction[T,R,f] = bits(EDGE_OUTCOME) - bits(EDGE_REGIME)`

A reading×regime interaction residual passes iff:

- mean `G_interaction > 0`; and
- positive in at least `4/5` folds.

A regime is robustly context-specific only if that condition passes independently in **both** ZL3b and IT2a.

### Frozen classes

1. `CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN BOTH A AND B`
2. `CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN A ONLY`
3. `CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN B ONLY`
4. `NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`
5. `INVALID CURRIER EDGE FACTORIZATION`

No rescue class or post-reveal reparameterization.

### Gate0 — mandatory first deliverable

Before any real-target `EDGE_OUTCOME` likelihood:

1. pin/reproduce merged Issue #158 Gate/result/scorer/provenance authority;
2. reproduce all five A/B/POOL rational table identities and physical-leaf folds;
3. construct aggregate A/B/POOL outcome counts from training data only;
4. prove exact aggregate effective-mass equality;
5. freeze/archive all 32 outcome multipliers for A and B;
6. prove finite normalized outcome-only conditionals for every retained context without target outcomes;
7. reproduce all reading×regime×fold support and zero leakage;
8. run synthetic tests that distinguish global outcome bias from a context-specific interaction;
9. prove no held-out `EDGE_OUTCOME` likelihood, `G_outcome`, `G_interaction` or classification was computed.

If authority/support/normalization fails, classify INVALID. Do not change the factorization after reveal.

## Decision fork after #161

### A. Interaction residual robust in both A and B

Currier changes the **conditional relation** between previous-terminal and next-initial, not merely the marginal next-initial distribution. The next compression target should be a separately preregistered low-rank interaction model, not post-hoc atom/context selection.

### B. Interaction residual only in one regime

Retain a global outcome gate for one side and a context-specific correction for the other. Characterize asymmetry only after the primary result is frozen.

### C. No robust interaction residual

Promote the simpler responsibility:

> **one shared terminal→initial table + Currier-specific global next-initial bias.**

This would sharply reduce the dimensionality of the Currier distinction.

### D. Invalid

Stop without target interpretation.

## High-value follow-ups

Only as licensed by #161:

1. **Low-rank Currier interaction** — only if context-specific residual survives; rank/dimension must be frozen prospectively rather than selected from target performance.
2. **Compact observable-core consolidation** — replace obsolete reading-specific edge responsibility with the minimal #161-supported form in a future core.
3. **Reversible/inverse mechanism tournaments** — require candidates to reproduce the established boundary, recurrence, inventory and Currier-gated edge responsibilities without target-aware repair.
4. **Externally anchored content tests** — mappings fixed independently of Voynichese similarity.
5. **Issue #84 Phase D** only where it answers an identifiable question not superseded by Issue #88.

A rich latent-state model is not on the active path unless a new prospectively defined predictive residual independently reopens that license.

## Parked / historical lanes

- generic finite-memory/copy-mutate exploration (#24): theory background, not current implementation frontier;
- music-motif/self-similarity methods (#25): exploratory and separate; no direct-musical interpretation is supported;
- older R1 generator ladders (#58/#75): completed history, not current frontier.

## Research boundary

Nothing on this roadmap currently establishes plaintext, language, semantic absence, cipher identity/key, natural-language word boundaries, author/scribe causation, historical direction, hoax/artificial origin, a historical production algorithm or decipherment.
