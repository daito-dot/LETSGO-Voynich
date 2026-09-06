# Current research status

Last consolidated: 2026-09-06
Authority for the current program: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

This file records the accepted high-level interpretation. Exact methods, first-reveal artifacts, hashes and frozen classifications remain authoritative in phase-specific plans/reports/provenance files.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The strongest current structural picture is now unusually constrained:

1. visible certain spaces behave as reproducible construction/production boundaries in both ZL3b and independent Takahashi/IT2a;
2. inside each visible unit, a compact second-order occupied-slot successor grammar explains nearly all replicated token-internal topology;
3. nearby units are weakly coupled by a short edit-distance-1 recurrence/cache process that transports across Currier A/B;
4. slower prior-paragraph / causal-prefix inventory is predictive but its useful strength differs by Currier regime and the difference survives matched Herbal restriction;
5. corrected B3 (V2 + local/long history + observable line/paragraph state) reaches `9.5172688 bits/token` from a `9.7089061`-bit V2 baseline;
6. a further small surface residual survives B3, matched emission control and same-order byte control;
7. Issue #123 prospectively localizes that residual to adjacent visible units within the same source line: carrying the same short context across a line break is worse in all five folds;
8. Issue #125 exactly decomposes the line-local model and shows that generic line-position onset contributes `+0.00889 bit/token`, while **previous-token terminal identity adds a further `+0.02027 bit/token`, positive in 5/5 folds**.

The remaining unexplained signal is therefore not well described as generic long hidden sequence memory. A large share of the flexible line-local residual is already explained by one explicit observable edge: **previous visible unit terminal symbol → next visible unit initial symbol**.

None of this establishes plaintext, language, semantics, a cipher family, an author, hoax/artificial origin, a historical production algorithm, or a latent semantic state.

## 1. Visible spaces are validated construction boundaries

Phase 4A/B challenged the assumption that transcription spaces were meaningful production cuts.

ZL3b:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

- real-space vs within-token reset `D_RESET = +8.811905 bits/event`, positive `5/5`;
- observed cut beats one-atom-left and one-atom-right shifted cuts in `5/5` folds.

Independent Takahashi/IT2a:

> **VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a**

- `D_RESET = +8.092615`, positive `5/5`;
- observed cut again beats both shifted cuts in `5/5`.

Literal certain spaces can therefore be treated as transcription-lineage-robust construction/production boundaries under these representations. They are **not** thereby proven natural-language word boundaries.

## 2. Token-internal construction is compact

Issue #75 plus OGH-A/B/C established that the next occupied slot is well modeled from only the previous two occupied slots.

- 298 counted conditional probabilities;
- within roughly 1–2% of the empirical-signature ceiling across tested readings;
- complete memoryless V2 ≈ `7.0 bits/token` shape + `2.7 bits/token` values ≈ `9.7 bits/token` total.

A rich latent token-internal construction state is not currently required. Memoryless token generation, however, does not reproduce the major cross-token effects.

## 3. Corrected predictive-information budget

The causal-source-order correction supersedes the original order-sensitive Phase-1/2 numbers.

- B0 V2 `9.7089061 bits/token`;
- B1 local history `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688`.

B3 improves V2 by about `0.19164 bit/token`, roughly 2% of V2 code length. Cross-token structure is reproducible but information-light relative to the information inside each bounded unit.

## 4. Long-history prediction is mostly slow inventory

Corrected Phase 2A/B/C shows that most apparent long-history gain is not detailed long ordered memory.

The dominant component is an order-free causal-prefix / prior-paragraph inventory of activated edit-near token families. A smaller actual-order residual remains.

Phase 2C:

- PREV1 conditional gain `+0.0070407 bit/token`, `5/5`;
- OLDER accumulated paragraph inventory `+0.0367964`, `5/5`;
- same-side prior history `+0.0205711`, `5/5`;
- cross-side prior history `+0.0237448`, `5/5`.

The slow signal spans multiple prior paragraphs and crosses page-side topology.

## 5. LOCAL transports; PREV strength is regime-dependent

Phase 3A:

- LOCAL40 transports bidirectionally across Currier A/B with nearly unchanged strength (`pi_LOCAL=.14` vs `.16`);
- PREV_PARAS architecture is useful in both, but exact scalar strength differs (`alpha=.09` A vs `.19` B);
- full CORE remains bidirectionally transportable.

Phase 3C matched pure Herbal and still found approximately twofold PREV strength difference (`.04` A-H vs `.08` B-H) with A→B-only exact scalar transfer.

Frozen interpretation:

> **CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL**

Broad illustration/domain composition is not a sufficient explanation. Writing hand remains unresolved because it is inadequately crossed with Currier.

## 6. Issue #118: flexible residual beyond corrected B3

Issue #118 compared the same byte n-gram family in two roles: RESET before every visible token versus CONTINUOUS across visible spaces within the physical leaf. Both were independently mixed with corrected B3 using inner-fold-only weight selection.

Frozen classification:

> **ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED**

`G_context = bits(MIX_RESET)-bits(MIX_CONT)`:

- mean `+0.0178533 bit/token`;
- positive `5/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET `9.50451671`;
- MIX_CONT `9.48666342`.

The residual is small but robust. It licensed localization, not latent-state interpretation.

## 7. Issue #121 L1: same-order boundary-edge control

L1 forced both byte experts to identical `k=2, alpha=.01`.

> **BOUNDARY-EDGE RESIDUAL SURVIVES SAME-ORDER CONTROL**

`G_edge = bits(MIX_RESET2)-bits(MIX_CONT2)`:

- mean `+0.0106322 bit/token`;
- positive `5/5`.

Predeclared held-out localization showed essentially all positive non-leaf-start contribution on `SAME_LINE`; cross-line averages were approximately zero or slightly negative.

## 8. Issue #123 L2: source-line reset scope

L2 compared identical fixed-k2 experts differing only in reset topology:

- RESET2 — reset before every visible token;
- LINECONT2 — carry across spaces within one source line, reset at each line start;
- LEAFCONT2 — carry across line breaks within the physical leaf.

Authority:

- scientific head `87aee03e60e2eab72987eb0cc2bf8c4b992632a0`;
- run `34027611090` — SUCCESS;
- result JSON SHA-256 `dfdfca650a15f1d47bd7124898bc8483a139ce47bb17a2c2802a0d2e946dea55`.

> **LINE-LOCAL CONTEXT CAPTURES RESIDUAL; NO ROBUST BEYOND-LINE GAIN**

`G_line = bits(MIX_RESET2)-bits(MIX_LINECONT2)`:

- mean `+0.0291614 bit/token`;
- positive `5/5`.

`G_beyond_line = bits(MIX_LINECONT2)-bits(MIX_LEAFCONT2)`:

- mean `-0.0185292 bit/token`;
- positive `0/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET2 `9.49729565`;
- MIX_LINECONT2 `9.46813424`;
- MIX_LEAFCONT2 `9.48666342`.

Under this fixed representation, carrying the same short context across source-line breaks is predictively harmful in every outer fold.

## 9. Issue #125 L3: explicit terminal→initial edge identity

L2's LINECONT2 still combined two observable effects:

1. generic onset differences between source-line-start and line-interior tokens;
2. actual identity of the immediately previous token's terminal raw symbol.

L3 factorized LINECONT2 exactly into:

- POS2 — line-start/interior onset distributions, no previous-token identity;
- EDGE2 — POS2 plus previous-terminal-conditioned first-symbol probability for line-interior tokens.

EDGE2 is **exactly equivalent** to Issue #123 LINECONT2:

- max inner token-logp difference `0.0`;
- max outer token-logp difference `0.0`;
- exact Issue #123 weights and foldwise `G_line` reproduced.

Authority:

- scientific head `8a3cd11543bc8ccbd7aacfa47486048d1b75cb5f`;
- workflow run `34028083557` — SUCCESS;
- artifact `9987750791`;
- artifact digest `sha256:dab4dc3ad4362044cbdd02fa1a9bcc200c846ac8e08d5852edd42ecc88e9323a`;
- result JSON SHA-256 `f329b01a4645b4510bb8b2d5f6a1f194f01395bf707c4870195c3ea6f55f6b45`.

Frozen classification:

> **TERMINAL→INITIAL IDENTITY ADDS ROBUST LINE-LOCAL INFORMATION**

Generic line-position onset contribution:

`G_position = bits(MIX_RESET2)-bits(MIX_POS2)`

- mean `+0.00889185 bit/token`;
- positive `5/5`.

Previous-terminal identity contribution:

`G_identity = bits(MIX_POS2)-bits(MIX_EDGE2)`

- fold0 `+0.0232774`;
- fold1 `+0.0145110`;
- fold2 `+0.0191062`;
- fold3 `+0.0212060`;
- fold4 `+0.0232472`;
- mean `+0.02026956 bit/token`;
- positive `5/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET2 `9.49729565`;
- MIX_POS2 `9.48840380`;
- MIX_EDGE2 `9.46813424`.

Both components are positive across reported ENTRY/BODY and FIRST/MIDDLE/FINAL strata. The direct previous-terminal identity effect is therefore not merely a line-position proxy under this test.

Supported statement:

> After controlling generic source-line-start versus line-interior token-onset distributions, the immediately preceding visible unit's terminal raw symbol still predicts the next visible unit's onset within the same source line.

This is a compact observable adjacency relation, not a semantic interpretation.

## 10. Cross-linguistic / cipher / historical controls

Issue #84 established a distinctive inter-unit relation regime across seven Voynich readings. Relative to 101 natural-language controls, Voynich has much lower adjacent corrected MI, immediate exact-repeat excess, and much weaker 21–40-token recurrence. Frozen common reversible-operation representatives and ten historical recipe/herbal/account/liturgical controls produced zero full hits under preregistered joint criteria.

This narrows easy explanations but does not exclude all meaningful natural language, all historical genres or all cipher systems.

## 11. Current integrated structural picture

### Inside one visible unit

A compact second-order construction grammar largely determines admissible shape.

### At the visible-space boundary

A certain space is a sharp construction reset and its exact location replicates across two transcription lineages.

### Between adjacent units on the same source line

Two small observable effects survive corrected B3:

- generic line-start versus line-interior onset distribution;
- a stronger direct previous-terminal → next-initial identity edge.

### At source-line breaks

The short edge context should reset. Carrying it across the break makes prediction worse.

### Across nearby units more generally

A separate edit-near recurrence/cache mechanism remains predictive and broadly transportable.

### Across slower document history

Prior-paragraph/cumulative family inventory adds reproducible prediction with Currier-dependent strength.

The overall structure is therefore **compact and multiscale, with the formerly flexible residual increasingly reduced to explicit observable components**.

## 12. Active frontier — transport the compact edge and retest residual capacity

The strongest next steps are now constrained.

First, test whether the explicit terminal→initial edge architecture/strength transports across Currier A/B. This is an observable-regime question analogous to the successful LOCAL40 transport work and can be done without invoking hand or semantics.

Second, once a compact edge is included directly in the observable core, rerun a residual-capacity challenger. A latent-state model becomes scientifically interesting only if material held-out predictive information remains after:

- corrected V2/local/long/state core;
- line-position onset;
- explicit line-local terminal→initial edge;
- already-authorized regime controls.

Until then, rich hidden-state interpretation is premature.

## Interpretation firewall

Current evidence does not license claims of:

- decipherment or recovered plaintext;
- language identification;
- semantic interpretation of tokens or states;
- absence of meaning;
- hoax/artificial-text origin;
- a specific cipher key or historical cipher family;
- a historical copy/mutate algorithm;
- latent semantic states;
- visible spaces as proven natural-language word boundaries;
- source lines as proven sentences or semantic clauses.
