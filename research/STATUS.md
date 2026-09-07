# Current research status

Last consolidated: 2026-09-07

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

This file controls the **current accepted high-level interpretation**. Exact historical methods, first-reveal artifacts, hashes and frozen classifications remain controlled by phase/Issue-specific plans, reports and provenance files.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The strongest current structural picture is compact:

1. certain visible spaces behave as reproducible construction/production boundaries in ZL3b and Takahashi/IT2a;
2. each bounded unit has a compact token-internal construction grammar; a target-blind second-order occupied-slot successor model nearly reaches the empirical R1 ceiling;
3. cross-unit predictive information is real but small relative to token-internal information;
4. longer history is dominated by causal-prefix / prior-paragraph inventory rather than detailed long ordered memory;
5. useful immediate raw context is localized to adjacent visible units inside the same source line and resets at line breaks;
6. under fixed `k=2`, the previously flexible line-local expert is exactly represented by generic line-position/onset plus an explicit previous-terminal → next-initial edge;
7. after corrected B3 is prospectively augmented with that observable edge, Issue #134 finds **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`** and does not license rich latent-state escalation;
8. Issues #139/#145 independently replicate the edge across ZL3b/IT2a under one common Basic-EVA representation;
9. Issue #148 shows the literal common-EVA edge table transports bidirectionally across those reading lineages;
10. Issue #151 shows **one reading-balanced common-EVA edge table suffices**; neither reading retains a robust table-specific residual;
11. Issue #155 shows the stabilized literal table is not interchangeable across Currier A/B in either direction under support matching;
12. Issue #158 shows the observable Currier A/B label adds robust held-out edge information in **both** A and B, independently in both readings;
13. the active Issue #161 asks whether that Currier distinction can be compressed to a context-invariant next-initial bias or requires a genuine previous-terminal × next-initial interaction.

The current minimal edge responsibility is:

> **shared reading-independent terminal→initial architecture + explicit Currier-conditioned literal mapping.**

None of this establishes plaintext, language, semantics, cipher identity, natural-language words, author/scribe causation, historical direction, hoax/artificial origin, historical production mechanism or decipherment.

## 1. Certain visible spaces are validated production boundaries

Phase 4 challenged whether transcription spaces are meaningful production cuts using representations independent of `SlotParser`.

ZL3b:

- `D_RESET = +8.811905 bits/event`, positive 5/5;
- exact observed cut beats one-atom-left and one-atom-right shifted cuts in 5/5 folds.

Takahashi/IT2a:

- `D_RESET = +8.092615`, positive 5/5;
- exact observed cut again beats both shifted cuts in 5/5.

Supported statement:

> **Visible certain spaces behave as transcription-lineage-robust construction/production boundaries under the tested representations.**

They are not thereby proven natural-language word boundaries.

## 2. Token-internal construction is compact

Issue #75 plus OGH-A/B/C establish that the replicated 66-edge R1 topology does not currently require a rich token-internal latent state.

- target-blind second-order occupied-slot successor grammar;
- 298 counted conditional probabilities;
- median topology agreement `T≈0.948` on ZL3b and `0.962` on IT2a;
- memoryless V2 code length `9.7089061 bits/token`;
- approximate information split: shape `~7.0 bits/token`, values add `~2.7`.

Memoryless token generation does not recover the major cross-token responsibilities, so token-internal sufficiency is not manuscript-level sufficiency.

## 3. Corrected predictive-information budget

After source-order correction:

- B0 V2 `9.7089061 bits/token`;
- B1 local history `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688`.

B3 improves V2 by about `0.19164 bit/token`. Cross-token structure is reproducible but information-light relative to each bounded unit's internal information.

Longer-history gain is dominated by causal-prefix / prior-paragraph inventory; actual long ordered-memory residual is much smaller.

## 4. The short flexible residual localized to a same-line observable edge

Issue #118:

- `G_context = +0.0178533 bit/token`, positive 5/5;
- `G_any = +0.0306054`, positive 5/5.

Issue #121 fixed both raw-context arms to `k=2, alpha=.01` and retained `+0.0106322`, positive 5/5.

Issue #123:

- same-line continuation `G_line = +0.0291614`, positive 5/5;
- carrying context beyond a source-line break `G_beyond_line = -0.0185292`, positive 0/5.

Issue #125:

- generic position/onset `+0.00889185`, positive 5/5;
- terminal identity adds `+0.02026956`, positive 5/5;
- EDGE2 and LINECONT2 have maximum token-logp difference `0.0`.

Supported statement:

> **Useful immediate raw-surface context is line-local and, under the frozen representation, is fully represented by generic onset/position plus immediate previous-terminal identity.**

## 5. Issue #134 closes the tested residual after observable augmentation

First reveal:

- corrected B3 mean `9.517268842963203 bits/token`;
- augmented observable core mean `9.451900585480233`;
- mean gain over B3 `+0.06536825748296984`, positive 5/5;
- RESET selected final `w=0.0` in all five folds;
- LINE selected final `w=0.0` in all five folds;
- `G_residual=[0,0,0,0,0]`.

Frozen classification:

> **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**

Authority: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

This does not prove hidden states do not exist. It says the tested residual does not justify adding one.

## 6. The terminal→initial edge independently replicates

Issue #139 carried the fixed edge architecture to Takahashi/IT2a.

Frozen classification:

> **`INDEPENDENT EDGE REPLICATION PASSES`**

- fold gains `[+0.1604351582,+0.1236103876,+0.1553216897,+0.1739669556,+0.1472252361]`;
- mean `+0.15211188542908544 bit/token`;
- positive 5/5.

Authority: run `34061721332`, artifact `9997679250`, result SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`.

## 7. One common representation preserves the edge in both readings

Issue #145 froze one common Basic-EVA representation.

Frozen classification:

> **`COMMON-EVA EDGE ROBUST IN BOTH READINGS`**

- ZL3b mean `G_common = +0.1336232955274749 bit/token`, positive 5/5;
- IT2a mean `+0.16184998339508744`, positive 5/5;
- EDGE2_COMMON equals full clean-run-contiguous k2 exactly in all ten reading×fold cells.

Authority: run `34062199123`, artifact `9997826217`, result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`.

## 8. The literal common-EVA edge table transports across readings

Issue #148 transports only BODY `P(first_common_atom | previous_terminal_common_atom)`; all non-edge factors remain target-native.

Frozen classification:

> **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**

ZL3b→IT2a:

- mean `G_transport = +0.15554823663346334`, positive 5/5;
- retention ratio `0.9610642730420239`.

IT2a→ZL3b:

- mean `+0.13039023868507016`, positive 5/5;
- retention ratio `0.9758046916172639`.

Authority: run `34073660425`, artifact `10001309613`, result SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`.

Supported interpretation:

> **Under one frozen common-EVA representation, the concrete previous-terminal→next-initial predictive mapping is strongly shared across ZL3b/IT2a.**

## 9. Issue #151 collapses the two reading-native tables to one shared table

Issue #151 asks whether each reading still needs its own table after #148.

Frozen classification:

> **`ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`**

A fixed `0.5/0.5` reading-balanced table constructed from training folds only is useful in both readings:

- ZL3b `G_shared` mean `+0.13564574057416792`, positive 5/5;
- IT2a `+0.16380858130203818`, positive 5/5.

Reading-specific residuals fail:

- ZL3b `G_specific` mean `-0.002022445046693022`, positive 3/5;
- IT2a `-0.001958597906950743`, positive 1/5.

Authority: run `34074437422`, artifact `10001563139`, result SHA-256 `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`, merged PR #154.

Thus reading lineage no longer needs to be a model gate for this edge under the frozen common representation.

## 10. Issue #155 shows Currier A/B remains a real literal-table distinction

Issue #155 repeats Currier table transport under stabilized common-EVA, reading-balanced training tables and context-mass support matching.

Frozen classification:

> **`COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`**

Wrong-regime transport is strongly negative in all four reading×direction cells:

- A→B: ZL3b mean `-0.2992311805`, IT2a `-0.2986494755`, positive 0/5 each;
- B→A: ZL3b `-0.3753370873`, IT2a `-0.3873299031`, positive 0/5 each.

Same-regime matched edge tables remain useful:

- target A: ZL3b `+0.0568990376`, IT2a `+0.0769484203`;
- target B: ZL3b `+0.1705252416`, IT2a `+0.2085317706`.

Authority: run `34075146845`, artifact `10001781210`, result SHA-256 `041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737`, PR #157 merge `6bd7c6fadb8fc590052496299c13da24f88585a2`.

This current common-EVA result supersedes the older #130 B→A-only asymmetry as the live Currier transport picture. Neither result licenses historical direction.

## 11. Issue #158 isolates robust incremental information from the Currier gate

Issue #158 uses the exact support-matched A/B tables from #155 and constructs per fold:

`C_POOL = 0.5*C_A^MATCH + 0.5*C_B^MATCH`.

A/B/POOL have exactly equal effective mass inside every retained previous-terminal context. It compares the pooled table with the target Currier regime's own table while keeping all non-edge factors fixed.

Frozen classification:

> **`CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`**

Currier A incremental residual:

- ZL3b `G_Currier` mean `+0.06327673406664047`, positive 4/5;
- IT2a `+0.06782616617812458`, positive 4/5.

Currier B:

- ZL3b `+0.1012061292632481`, positive 5/5;
- IT2a `+0.10456811219559015`, positive 5/5.

Cross-reading differences are only:

- A: `ZL3b-IT2a = -0.004549432111484106`;
- B: `-0.0033619829323420503 bit/token`.

Authority:

- corrected score-free Gate result SHA-256 `605e0a82817f394176a3e19c972ed409dfb15df60c72df22db3c0cc765e31099`;
- Gate merge / PR #159 `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- scorer blob `e7a70a10dd7b663f3482993b0adfa8f804816158`;
- first-reveal run `34076400927`;
- artifact `10002205049`;
- result SHA-256 `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`;
- PR #160 merge `1741bed875a582594dc797ef18e30dd2ef3351ce`.

Supported interpretation:

> **The boundary architecture is reading-independent, but its literal transition mapping contains robust Currier-conditioned information.**

## 12. Current compact working model

The most economical live **surface-production** description is:

1. certain visible spaces delimit bounded production/construction episodes;
2. inside each episode, a compact second-order occupied-slot grammar captures most topology;
3. short edit-near recurrence/cache contributes very local history;
4. within a source line, generic onset/position plus immediate previous-terminal → next-initial identity contributes a reproducible observable adjacency effect;
5. source-line breaks reset that useful short raw context;
6. the terminal→initial architecture and one reading-balanced common-EVA base table are stable across ZL3b/IT2a;
7. the literal edge mapping is explicitly Currier-conditioned;
8. slower causal-prefix / prior-paragraph family inventory contributes longer history;
9. no separately frozen flexible RESET/LINE capacity is selected beyond the augmented observable core.

This is a compact predictive surface model, not a decipherment.

## 13. Current frontier — Issue #161 Currier edge factorization

Issue #158 establishes that Currier conditioning matters. Issue #161 asks whether it matters only through a global next-initial outcome bias or through a genuine context-specific interaction.

For each training fold and fixed outcome `y`:

`G_R(y) = Σ_c C_R^MATCH(c,y)`

`G_POOL(y) = Σ_c C_POOL(c,y)`

with fixed multiplier:

`W_R(y) = (G_R(y)+alpha)/(G_POOL(y)+alpha)`, `alpha=.01`.

The frozen outcome-only model applies `W_R(y)` to the pooled conditional and renormalizes inside every previous-terminal context. This model has a Currier×outcome main effect but no Currier×previous-terminal×outcome interaction.

Primary quantities:

- `G_outcome[T,R,f] = bits(EDGE_POOL) - bits(EDGE_OUTCOME)`;
- `G_interaction[T,R,f] = bits(EDGE_OUTCOME) - bits(EDGE_REGIME)`.

A robust context-specific Currier residual requires mean `G_interaction > 0` and positive in at least 4/5 folds independently in both ZL3b and IT2a for the same regime.

Frozen classifications:

1. `CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN BOTH A AND B`
2. `CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN A ONLY`
3. `CURRIER EDGE CONTRAST REQUIRES CONTEXT-SPECIFIC INTERACTION IN B ONLY`
4. `NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`
5. `INVALID CURRIER EDGE FACTORIZATION`

The first #161 deliverable is **score-free Gate0**. No real-target `EDGE_OUTCOME` likelihood, `G_outcome`, `G_interaction` or classification may be inspected before merged #158 authority, aggregate mass equality, all 32 fixed multipliers, normalization, support/leakage and synthetic tests are frozen.

If interaction remains, the next compression target should be a separately preregistered low-rank interaction model. If not, the edge can simplify to one shared terminal→initial table plus a Currier-specific global next-initial bias.

Latent-state work remains **not licensed** by the current residual evidence.
