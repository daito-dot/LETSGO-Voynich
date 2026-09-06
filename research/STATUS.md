# Current research status

Last consolidated: 2026-09-06

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

This file controls the **current accepted high-level interpretation**. Exact historical methods, first-reveal artifacts, hashes and frozen classifications remain controlled by phase/Issue-specific plans, reports and provenance files.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The strongest current structural picture is unusually constrained and increasingly compact:

1. certain visible spaces are reproducible construction/production boundaries in both ZL3b and independent Takahashi/IT2a;
2. each bounded unit has a compact token-internal construction grammar: a target-blind second-order occupied-slot successor model nearly reaches the empirical R1 ceiling;
3. short edit-near recurrence/cache effects and slower causal-prefix / prior-paragraph inventory provide real but information-light cross-token prediction;
4. corrected B3 reaches `9.5172688 bits/token` from a `9.7089061`-bit memoryless V2 baseline;
5. Issue #118 found a further small flexible surface residual beyond B3 and matched token-emission control;
6. Issues #121/#123 localize useful short raw context to **adjacent visible units within the same source line**; carrying the same context through a line break is predictively harmful;
7. Issue #125 exactly decomposes the fixed-`k=2` line-local expert into generic line-position/onset support plus an explicit **previous terminal raw symbol → next initial raw symbol** edge;
8. Issue #127 shows that edge architecture is useful in Currier A and B, while literal table transport is directionally asymmetric;
9. Issue #130 removes the major source-support imbalance and the asymmetry persists: support-matched terminal→initial table transport is **B→A only**.

The former “flexible sequence residual” is therefore no longer well described as generic hidden long sequence memory. Under the tested `k=2` representation, a large share of it has collapsed into a compact, directly observable same-line adjacency rule.

None of this establishes plaintext, language, semantics, cipher identity, natural-language words, author/scribe causation, hoax/artificial origin, historical production mechanism or decipherment.

## 1. Certain visible spaces are validated production boundaries

Phase 4 challenged the assumption that transcription spaces were meaningful production cuts using raw EVA representations independent of `SlotParser`.

ZL3b:

- `D_RESET = +8.811905 bits/event`, positive 5/5;
- exact observed cut beats one-atom-left and one-atom-right shifted cuts in 5/5 folds.

Independent Takahashi/IT2a:

- `D_RESET = +8.092615`, positive 5/5;
- exact observed cut again beats both shifted cuts in 5/5.

Supported statement:

> **Visible certain spaces behave as transcription-lineage-robust construction/production boundaries under the tested representations.**

They are not thereby proven natural-language word boundaries.

## 2. Token-internal construction is compact

Issue #75 plus OGH-A/B/C establish that the replicated 66-edge R1 topology does not currently require a rich token-internal latent state.

- target-blind second-order occupied-slot successor grammar;
- 298 counted conditional probabilities;
- median topology agreement `T≈0.948` on the ZL3b arm and `0.962` on the IT2a arm;
- empirical-ceiling gaps about `0.0165 / 0.0079`;
- memoryless V2 code length `9.7089061 bits/token`;
- approximate information split: shape `~7.0 bits/token`, values add `~2.7 bits/token`.

Memoryless token generation does **not** recover the major cross-token responsibilities, so token-internal sufficiency must not be promoted to manuscript-level sufficiency.

## 3. Corrected predictive-information budget

The source-order correction supersedes the original order-sensitive Phase 1/2 numbers.

- B0 V2 `9.7089061 bits/token`;
- B1 local history `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688`.

B3 improves V2 by about `0.19164 bit/token`, roughly 2% of V2 code length. Cross-token structure is reproducible but information-light relative to the information inside each bounded unit.

## 4. Longer-history information is mostly slow inventory

Corrected Phase 2A/B/C shows that most apparent long-history gain does not require detailed literal long ordered memory.

The dominant component is an order-free causal-prefix / prior-paragraph inventory of activated edit-near token families. A smaller actual-order residual remains.

Phase 2C:

- PREV1 conditional gain `+0.0070407 bit/token`, 5/5;
- OLDER accumulated paragraph inventory `+0.0367964`, 5/5;
- same-side prior history `+0.0205711`, 5/5;
- cross-side prior history `+0.0237448`, 5/5.

The slow signal therefore spans multiple prior paragraphs and is not confined to one page side/panel.

## 5. Existing mechanism transport is mixed, not manuscript-universal in every parameter

Phase 3A:

- LOCAL40 edit-near mechanism transports bidirectionally across Currier A/B with similar useful strength;
- PREV_PARAS architecture is useful in both regimes but exact scalar strength does not transport symmetrically.

Phase 3C matched pure-Herbal restriction retains the Currier PREV-strength asymmetry. Broad domain composition is therefore insufficient to explain it.

Writing hand is not cleanly identifiable as a cause because hand and Currier are inadequately crossed in the current metadata.

## 6. A small flexible residual survives corrected B3

Issue #118 compared the same byte-model family under two boundary-history policies and mixed each independently with corrected B3.

- RESET: byte context resets at every visible-space unit;
- CONT: byte context carries across visible spaces until leaf boundary.

Primary result:

- `G_context = bits(MIX_RESET) - bits(MIX_CONT)`;
- folds `+0.0349457, +0.0232139, +0.0093004, +0.0108658, +0.0109406`;
- mean `+0.0178533 bit/token`, positive 5/5.

Any complement beyond B3:

- `G_any = B3 - MIX_CONT = +0.0306054 bit/token`, positive 5/5.

Frozen classification:

> **ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED**

The effect is only about 0.19% of B3 code length. It does not imply a large hidden information channel.

## 7. Same-order and reset-scope controls localize the residual to within-line adjacency

Issue #121 forced RESET and CONT experts to the same `k=2`, `alpha=.01` family.

- `G_edge = RESET2 - CONT2` mean `+0.0106322 bit/token`, positive 5/5.

Predeclared descriptive localization placed essentially all ordinary cross-token gain inside source lines rather than across line/item/document transitions.

Issue #123 then compared reset scopes under the same fixed family:

- `G_line = RESET2 - LINECONT2 = +0.0291614 bit/token`, positive 5/5;
- `G_beyond_line = LINECONT2 - LEAFCONT2 = -0.0185292`, positive 0/5.

Supported statement:

> **Useful immediate raw-surface context is line-local under this representation; carrying the same short context through a source-line break is harmful.**

A source line is not thereby a sentence or semantic clause.

## 8. The line-local flexible expert factorizes into an explicit observable edge

Issue #125 decomposed the fixed-`k=2` line-local expert into:

- POS2: generic line-position/onset context;
- EDGE2: POS2 plus immediately previous visible unit terminal raw symbol → current initial raw symbol.

Results:

- generic position component `+0.00889185 bit/token`, positive 5/5;
- terminal-identity component `+0.02026956`, positive 5/5;
- EDGE2 vs LINECONT2 maximum inner/outer token-logp difference = `0.0`.

Frozen classification:

> **TERMINAL→INITIAL IDENTITY ADDS ROBUST LINE-LOCAL INFORMATION**

Under the tested `k=2` construction, the formerly flexible line-local expert contains no additional token-likelihood information beyond generic line position plus this immediate observable identity edge.

## 9. Currier A/B share the edge architecture but not one universally transportable literal table

Issue #127 separated native architecture, scalar strength and literal conditional-table transport.

- target-native edge: PASS in A and PASS in B;
- source scalar strength applied with target-native identity table: bidirectionally compatible;
- target-calibrated source-table transport: B→A only;
- exact source table + source strength: neither direction.

This suggests a shared compact edge mechanism with regime-dependent mapping rather than one universal literal terminal→initial table.

## 10. Support matching does not remove the directional table asymmetry

Issue #130 prospectively matched source-table estimation support before attaching current-initial outcomes.

For each of five outcome-blind selections:

- 20 shared previous-terminal classes;
- A selected support `8,728` visible source edge events;
- B selected support `8,728`;
- exact A/B selected-count equality separately inside every retained terminal class.

First reveal:

### A→B

- seed passes `0/5`;
- every seed has `3/5` positive target folds;
- grand mean `+0.00693954 bit/token`;
- overall FAIL.

### B→A

- seed passes `5/5`;
- every seed has `4/5` positive target folds;
- grand mean `+0.02697082 bit/token`;
- overall PASS.

Frozen classification:

> **MATCHED_TABLE_TRANSPORT: B→A ONLY**

The earlier directional result is therefore not explained merely by B having roughly twice as many source edge observations.

This does **not** establish that one Currier regime historically derives from or contains the other.

Latest authority:

- scientific head `1604c2f36d106e918c55a24f7bea6b7e08622cff`;
- run `34029536188`;
- artifact `9988168421`;
- ZIP digest `sha256:90a6d658d72dda1e02ad96775822002e96c94858a99cbe15f9b08f95dd3a9707`;
- result JSON SHA-256 `d2ae55675fb7613b4f5000ab81558099f2821ff245acacdcb5a6697e06f7249e`.

## 11. Current compact working model

The most economical live **surface-production** description is now:

1. **bounded unit:** certain visible spaces mark production/construction cuts;
2. **inside unit:** compact second-order occupied-slot construction grammar;
3. **very local history:** edit-near recurrence/cache;
4. **within source line:** generic onset/position effect plus immediate previous-terminal → next-initial identity edge;
5. **line break:** resets that useful short raw context;
6. **slower history:** causal-prefix / prior-paragraph family inventory;
7. **observable regimes:** some strengths and literal edge mappings vary with Currier A/B.

This is a compact multiscale observable model, not a decipherment.

## 12. Current frontier

The next gate is to build an **augmented observable core** containing corrected B3 plus the explicit line-position + terminal→initial edge, with Currier table handling frozen before scoring, and rerun a separately frozen residual-capacity test.

Decision rule at the program level:

- if no robust residual remains, latent-state work is not licensed; consolidate the observable model and shift effort toward replication, reversibility/inverse constraints and independent external/content tests;
- if a robust residual remains, localize remaining observable/support/representation effects before any latent architecture receives interpretation.

See `ROADMAP.md` and `RESUME.md` for current sequencing.