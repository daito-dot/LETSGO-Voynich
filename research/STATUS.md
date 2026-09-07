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
8. Issue #139 independently replicates the edge architecture on Takahashi/IT2a;
9. Issue #145 shows the edge is robust in both ZL3b and IT2a under one frozen common Basic-EVA representation;
10. Issue #148 shows the **literal common-EVA edge table itself transports bidirectionally** across those two reading lineages, retaining about 96–98% of target-native gain;
11. the earlier support-matched Currier A/B result remains asymmetric (**B→A only**), so cross-reading robustness must not be conflated with regime universality;
12. the active Issue #151 asks whether the two reading-native common-EVA edge tables can be collapsed to one reading-balanced shared table without a reproducible reading-specific residual.

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

B3 improves V2 by about `0.19164 bit/token`, roughly 2% of V2 code length. Cross-token structure is reproducible but information-light relative to each bounded unit's internal information.

## 4. Longer-history information is mostly slow inventory

Corrected Phase 2A/B/C shows that most apparent long-history gain does not require detailed literal long ordered memory.

The dominant component is an order-free causal-prefix / prior-paragraph inventory of activated edit-near token families. A smaller actual-order residual remains.

Phase 2C:

- PREV1 conditional gain `+0.0070407 bit/token`, 5/5;
- OLDER accumulated paragraph inventory `+0.0367964`, 5/5;
- same-side prior history `+0.0205711`, 5/5;
- cross-side prior history `+0.0237448`, 5/5.

## 5. Existing mechanism transport is mixed

Phase 3A/3C established that:

- LOCAL40 transports bidirectionally across Currier A/B with similar useful strength;
- PREV_PARAS architecture is useful in both regimes but exact scalar strength does not transport symmetrically;
- matched pure-Herbal restriction does not remove that PREV-strength asymmetry;
- writing hand is not cleanly identifiable as a cause because hand and Currier are inadequately crossed.

## 6. The B3 flexible residual was real, small and line-local

Issue #118:

- `G_context = +0.0178533 bit/token`, positive 5/5;
- `G_any = +0.0306054`, positive 5/5.

Issue #121 fixed both raw-context arms to `k=2, alpha=.01` and retained `+0.0106322`, positive 5/5.

Issue #123 separated reset scopes:

- RESET2 → LINECONT2 `G_line = +0.0291614`, positive 5/5;
- LINECONT2 → LEAFCONT2 `G_beyond_line = -0.0185292`, positive 0/5.

Supported statement:

> **Useful immediate raw-surface context is line-local under this representation; carrying the same short context through a source-line break is harmful.**

## 7. The line-local expert factorizes into an observable edge

Issue #125 decomposed fixed-`k=2` LINECONT2 into POS2 plus EDGE2.

- generic position/onset component `+0.00889185 bit/token`, positive 5/5;
- terminal-identity component `+0.02026956`, positive 5/5;
- EDGE2 vs LINECONT2 maximum inner/outer token-logp difference `0.0`.

Frozen classification:

> **TERMINAL→INITIAL IDENTITY ADDS ROBUST LINE-LOCAL INFORMATION**

Under that representation, the flexible line-local expert contains no extra token-likelihood information beyond generic onset/position plus immediate observable terminal identity.

## 8. Currier A/B share the edge architecture but not one frozen literal table

Issue #127 established target-native edge usefulness in Currier A and B and scalar compatibility when target-native identity mapping is supplied.

Issue #130 then removed the major source-support imbalance. Each of five outcome-blind selections used exactly `8,728` source edge events per Currier regime with identical selected counts inside 20 shared previous-terminal classes.

Frozen matched result:

- A→B: seed passes `0/5`, grand mean `+0.00693954 bit/token` — FAIL;
- B→A: seed passes `5/5`, grand mean `+0.02697082` — PASS;
- classification **`MATCHED_TABLE_TRANSPORT: B→A ONLY`**.

This is predictive transport asymmetry, not historical direction or derivation.

## 9. Issue #134 closes the tested residual after observable augmentation

Issue #134 prospectively froze corrected B3 plus the observable same-line edge, including Currier A/B handling and fallback, before any new residual reveal.

First reveal:

- corrected B3 mean `9.517268842963203 bits/token`;
- augmented observable core mean `9.451900585480233`;
- mean gain over B3 `+0.06536825748296984`, positive 5/5;
- selected `rho=[0.19,0.22,0.20,0.19,0.21]`;
- RESET selected final `w=0.0` in all five folds;
- LINE selected final `w=0.0` in all five folds;
- `G_residual=[0,0,0,0,0]`;
- positive residual folds `0/5`.

Frozen classification:

> **NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE**

Authority:

- Gate0 result SHA-256 `3e11615c731654854b6ad982007d5f340b47d3a0c088cd09ab2af08080489db1`;
- first-reveal run `34035108074`;
- artifact `9990011421`;
- result JSON SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

Supported interpretation:

> **The previously measured short flexible sequence residual is absorbed, under the frozen test, when corrected B3 is augmented with the explicit observable same-line edge and prospectively fixed Currier handling.**

This does not prove hidden states do not exist. It says this residual does not provide predictive justification to add one.

## 10. Issue #139 independently replicates the edge on Takahashi/IT2a

Issue #139 carried the fixed edge architecture to the independently maintained Takahashi/IT2a reading with representation and decision rule frozen before target scoring.

Frozen classification:

> **INDEPENDENT EDGE REPLICATION PASSES**

Results:

- fold gains `[+0.1604351582, +0.1236103876, +0.1553216897, +0.1739669556, +0.1472252361]`;
- mean `+0.15211188542908544 bit/token`;
- positive `5/5`;
- EDGE2 equals full source-line-contiguous k2 at token-logp level in all folds.

Authority:

- run `34061721332`;
- artifact `9997679250`;
- result JSON SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`;
- PR #144 merged as `fa32d1dd79f858b83064123b3a307e0da138d7bc`.

This strongly weakens a ZL3b-specific transcription-artifact explanation for the architecture. It does not make the two transcriptions independent manuscripts.

## 11. Issue #145 makes the representation directly comparable

Issue #145 froze one common Basic-EVA representation for both readings.

Frozen classification:

> **COMMON-EVA EDGE ROBUST IN BOTH READINGS**

Results:

- ZL3b mean `G_common = +0.1336232955274749 bit/token`, positive 5/5;
- IT2a mean `+0.16184998339508744`, positive 5/5;
- IT2a−ZL3b mean difference `+0.028226687867612538`;
- EDGE2_COMMON equals the full clean-run-contiguous k2 implementation exactly in all ten reading×fold cells.

Exact fold gains from the authoritative artifact are:

- ZL3b `[0.1401857712184782, 0.11070803603016977, 0.13822277815269501, 0.14814594340112208, 0.13085394883490942]`;
- IT2a `[0.16849676408952696, 0.13944957574347505, 0.16568837114283141, 0.1803439402500029, 0.15527126574960093]`.

Authority:

- run `34062199123`;
- artifact `9997826217`;
- result JSON SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`;
- PR #147 merged as `26ccaa527fc4e1026d031e4773b819137a678f69`.

The large native effect-size discrepancy between #125 and #139 was therefore largely a representation-comparability issue, not an architecture failure.

## 12. Issue #148 shows the literal common-EVA mapping transports both ways

Issue #148 transported only the BODY `P(first_common_atom | previous_terminal_common_atom)` raw source-training count table. START, second-atom, k2 continuation and target population remained target-native. `k=2`, `alpha=.01`, `V=32`; no scalar, temperature, interpolation, calibration, mixture or target-native fallback.

Frozen classification:

> **COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS**

ZL3b→IT2a:

- fold `G_transport = [0.16617550444405893, 0.13437428362215265, 0.16077057068791767, 0.1796534044981435, 0.13676741991504393]`;
- mean `+0.15554823663346334 bit/token`;
- positive 5/5;
- target-native mean `+0.16184998339508744`;
- retention ratio `0.9610642730420239`;
- minimum context coverage `0.99935469993547`.

IT2a→ZL3b:

- fold `G_transport = [0.13208421050786257, 0.10700594617669168, 0.12950827390527841, 0.1397962031635096, 0.14355655967200853]`;
- mean `+0.13039023868507016`;
- positive 5/5;
- target-native mean `+0.1336232955274749`;
- retention ratio `0.9758046916172639`;
- minimum context coverage `0.9988499137435307`.

Authority:

- score-free Gate0 result SHA-256 `f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf`;
- corrected scorer blob `7847c0fea1dcfc4ace5752d0188d70e3739679d3`;
- successful run `34073660425` at pre-merge head `e08e682c9be91ee9cec97dedd66dd2dc3549eac1`;
- artifact `10001309613`;
- ZIP digest `sha256:cfefd670b00ebb3eae3020a4b5308115ec9172b793ed1fe4b598928718f5c622`;
- result JSON SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`;
- PR #150 merged as `b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131`.

PR #150 preserves an important authority-repair chronology: one prior run entered the scorer and aborted on a mis-copied #145 reproduction constant, emitting no transport metric/classification. The existing frozen #145 artifact was re-read, and only copied authority constants were corrected. No #148 scientific model, threshold or transport rule changed.

Supported interpretation:

> **Under one prospectively frozen common-EVA representation, the concrete previous-terminal→next-initial predictive mapping is shared strongly enough that a table learned from either reading transfers to the other, retaining roughly 96–98% of target-native edge gain.**

This is still a surface predictive result. It does not establish token alignment, semantic identity or historical direction.

## 13. Current compact working model

The most economical live **surface-production** description is:

1. certain visible spaces delimit bounded production/construction episodes;
2. inside each episode, a compact second-order occupied-slot grammar captures most topology;
3. short edit-near recurrence/cache contributes very local history;
4. within a source line, generic onset/position plus immediate previous-terminal → next-initial identity contributes a reproducible observable adjacency effect;
5. source-line breaks reset that useful short raw context;
6. the terminal→initial architecture independently replicates across ZL3b/IT2a and its literal mapping is highly transportable under a common representation;
7. slower causal-prefix / prior-paragraph family inventory contributes longer history;
8. some Currier-regime strengths/literal mappings remain asymmetric;
9. no separately frozen flexible RESET/LINE capacity is currently selected beyond the augmented observable core.

This is a compact predictive surface model, not a decipherment.

## 14. Current frontier — Issue #151 shared-table consolidation

The active question is now model simplification:

> **Can ZL3b and IT2a use one reading-balanced common-EVA edge table, or does either reading retain reproducible held-out information that requires its own native table?**

Issue #151 freezes per outer fold:

`C_SHARED = 0.5 * C_ZL3b + 0.5 * C_IT2a`

using only training physical leaves outside the held-out fold in **both** readings. The fixed half-weight prevents the same manuscript evidence from becoming twice as sharp simply because two readings are pooled.

Primary quantities:

- `G_shared[T,f] = bits(POS2_TARGET) - bits(EDGE2_SHARED)`;
- `G_specific[T,f] = bits(EDGE2_SHARED) - bits(EDGE2_NATIVE_T)`.

A reading-specific residual is robust iff mean `G_specific > 0` and positive in at least 4/5 folds. A valid shared-table consolidation also requires `G_shared` itself to be positive by the same 4/5 rule in both readings.

The first deliverable is a **score-free Gate0** freezing #145/#148 authorities, physical-leaf leakage checks, target support, exact fractional-count consensus arithmetic, context support and decision classes before any shared-table target likelihood is inspected.

If one shared table suffices, the next high-value question is whether the Currier A/B literal-table asymmetry from #130 survives this stabilized common representation. If reading-specific residual remains, preserve it rather than averaging it away.

Latent-state work remains **not licensed** by the current residual evidence.
