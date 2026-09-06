# Current research status

Last consolidated: 2026-09-06

Program authority: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

This file controls the **current accepted high-level interpretation**. Exact historical methods, first-reveal artifacts, hashes and frozen classifications remain controlled by phase/Issue-specific plans, reports and provenance files.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The strongest current surface-production picture is compact and mostly observable under the tested representations:

1. certain visible spaces are reproducible construction/production boundaries in both ZL3b and independent Takahashi/IT2a;
2. each bounded unit has a compact token-internal construction grammar: a target-blind second-order occupied-slot successor model nearly reaches the empirical R1 ceiling;
3. short edit-near recurrence/cache effects and slower causal-prefix / prior-paragraph inventory provide real but information-light cross-token prediction;
4. corrected B3 reaches `9.5172688 bits/token` from a `9.7089061`-bit memoryless V2 baseline;
5. Issue #118 found a small flexible residual beyond B3, then Issues #121/#123 localized its useful short raw context to adjacent visible units within the same source line;
6. Issue #125 exactly decomposed the fixed-`k=2` line-local expert into generic onset/position support plus an explicit **previous terminal raw symbol → next initial raw symbol** edge;
7. Issues #127/#130 showed the edge architecture in both Currier A/B, while the literal conditional table is not bidirectionally universal; support-matched table transport remains **B→A only**;
8. Issue #134 put that observable edge directly into a prospectively frozen augmented core and reran the residual test. The augmented core improved B3 by `+0.0653682575 bit/token` mean, while both residual challengers selected final `w=0` in every outer fold. `G_residual=[0,0,0,0,0]`.

Frozen Issue #134 classification:

> **NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE**

Under this residual program, rich latent-state escalation is therefore **not licensed**. This does not prove that hidden state is absent from the manuscript; it says the tested residual no longer supplies held-out predictive justification for adding it.

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

The slow signal spans multiple prior paragraphs and is not confined to one page side/panel.

## 5. Existing mechanism transport is mixed

Phase 3A:

- LOCAL40 edit-near mechanism transports bidirectionally across Currier A/B with similar useful strength;
- PREV_PARAS architecture is useful in both regimes but exact scalar strength does not transport symmetrically.

Phase 3C matched pure-Herbal restriction retains the Currier PREV-strength asymmetry. Broad domain composition is insufficient to explain it.

Writing hand is not cleanly identifiable as a cause because hand and Currier are inadequately crossed in the current metadata.

## 6. The flexible residual was real, small, and line-local

Issue #118 compared the same byte-model family under matched boundary-history policies and mixed each independently with corrected B3.

- `G_context = bits(MIX_RESET) - bits(MIX_CONT)`;
- folds `+0.0349457, +0.0232139, +0.0093004, +0.0108658, +0.0109406`;
- mean `+0.0178533 bit/token`, positive 5/5;
- `G_any = B3 - MIX_CONT = +0.0306054 bit/token`, positive 5/5.

Issue #121 forced RESET and CONT to the same `k=2, alpha=.01`; the edge gain remained `+0.0106322 bit/token`, positive 5/5.

Issue #123 then separated reset scopes:

- `G_line = RESET2 - LINECONT2 = +0.0291614`, positive 5/5;
- `G_beyond_line = LINECONT2 - LEAFCONT2 = -0.0185292`, positive 0/5.

Useful immediate raw-surface context is therefore line-local under this representation; carrying the same short context through a source-line break is harmful.

## 7. The line-local expert factorizes into an explicit observable edge

Issue #125 decomposed fixed-`k=2` LINECONT2 into:

- POS2: generic line-position/onset context;
- EDGE2: POS2 plus immediately previous visible unit terminal raw symbol → current initial raw symbol.

Results:

- generic position component `+0.00889185 bit/token`, positive 5/5;
- terminal-identity component `+0.02026956`, positive 5/5;
- EDGE2 vs LINECONT2 maximum inner/outer token-logp difference = `0.0`.

Frozen classification:

> **TERMINAL→INITIAL IDENTITY ADDS ROBUST LINE-LOCAL INFORMATION**

Under this tested construction, the formerly flexible line-local expert contains no additional token-likelihood information beyond generic line position plus this immediate observable identity edge.

## 8. Currier A/B share the edge architecture but not one universal literal table

Issue #127 separated native architecture, scalar strength and literal conditional-table transport.

- target-native edge: PASS in A and PASS in B;
- source scalar strength applied with target-native identity table: bidirectionally compatible;
- target-calibrated source-table transport: B→A only;
- exact source table + source strength: neither direction.

Issue #130 prospectively matched source-table estimation support before attaching current-initial outcomes. For each of five outcome-blind selections:

- 20 shared previous-terminal classes;
- A selected support `8,728` visible source edge events;
- B selected support `8,728`;
- exact A/B selected-count equality inside every retained terminal class.

First reveal:

- A→B: seed passes `0/5`; grand mean `+0.00693954 bit/token`; FAIL;
- B→A: seed passes `5/5`; grand mean `+0.02697082`; PASS;
- frozen classification **`MATCHED_TABLE_TRANSPORT: B→A ONLY`**.

The directional result is not explained merely by B having more source edge observations. It does not establish historical derivation or nestedness between Currier regimes.

## 9. Issue #134 closes the tested flexible residual after observable augmentation

Issue #134 prospectively froze an augmented core before target reveal:

- corrected B3;
- Issue #125 line-position/onset and terminal→initial representation with `k=2, alpha=.01`;
- target-native Currier A/B previous-terminal table when supported;
- pooled previous-terminal fallback, then pooled `LINE_BODY` onset;
- original five physical-leaf outer folds;
- augmented-core mixture `rho=0.00..1.00` by `.01`, inner-only selection;
- matched flexible challengers RESET vs source-line-local LINE;
- challenger `k∈{0..6}`, `alpha∈{.01,.10,1.0}` and final mixture `w=0.00..1.00`, all inner-only;
- frozen residual rule: mean `G_residual>0` and positive in at least `4/5` outer folds.

Gate0 passed before the predictive scorer existed. First successful reveal:

- scorer commit `dbd787a457659b7d833dc06c3931f937031172b8`;
- run `34035108074` — SUCCESS;
- artifact `9990011421`;
- artifact ZIP digest `sha256:c759783dd23b6390781168db83786b5f0cd19d103704adf92a2ac9d8a91a1853`;
- result JSON SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

Mean held-out code lengths:

- B3 `9.517268842963203 bits/token`;
- augmented observable core `9.451900585480233`;
- MIX_RESET `9.451900585480233`;
- MIX_LINE `9.451900585480233`.

Augmented-core gain over B3:

- mean `+0.06536825748296984 bit/token`;
- positive in all five outer folds;
- selected `rho=[0.19,0.22,0.20,0.19,0.21]`.

Primary residual:

- `G_residual=[0.0,0.0,0.0,0.0,0.0]`;
- mean `0.0`;
- positive folds `0/5`;
- both RESET and LINE selected final `w=0.0` in every fold.

Frozen classification:

> **NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE**

The zero residual is not a claim that the raw RESET and LINE experts are identical. It means nested inner validation assigns neither challenger any weight once the common augmented observable core is present.

Exact provenance: `experiments/predictive-information/residual-gate/ISSUE134_FIRST_REVEAL_PROVENANCE.md`.

## 10. Current compact working model

The most economical live **surface-production** description is now:

1. **bounded unit:** certain visible spaces mark production/construction cuts;
2. **inside unit:** compact second-order occupied-slot construction grammar;
3. **very local history:** edit-near recurrence/cache;
4. **within source line:** generic onset/position effect plus immediate previous-terminal → next-initial identity edge;
5. **line break:** resets that useful short raw context;
6. **slower history:** causal-prefix / prior-paragraph family inventory;
7. **observable regimes:** some strengths and literal edge mappings vary with Currier A/B.

For the frozen Issue #134 challenger family, this observable description absorbs the previously measured flexible residual. It remains a predictive/surface-production model, not a historical production algorithm or decipherment.

## 11. Current frontier

Issue #134 is closed. The active next question is Issue #139:

> **Does the same fixed same-line previous-terminal → next-initial architecture replicate on independent Takahashi/IT2a when source, line mapping, symbol treatment, folds, smoothing and decision rule are frozen before target scoring?**

This is the most direct test of whether the newly consolidated edge is manuscript-level structure rather than a ZL3b-lineage or representation-specific effect.

Issue #139 must begin with a score-free independent-transcription contract. Do not use IT2a outcomes to repair glyph normalization, exclusions, folds, smoothing, fallback or model family.

If the edge replicates independently, the next high-value lanes are reversible/inverse mechanism constraints and externally anchored content tests. If it fails, downgrade the edge to transcription-lineage-specific or representation-sensitive structure before treating it as a manuscript-wide production responsibility.
