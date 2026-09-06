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
7. Issue #123 now prospectively localizes that residual to **adjacent visible units within the same source line**: carrying the same byte context across a line break is worse in all five outer folds.

The remaining unexplained signal is therefore not well described as generic long hidden sequence memory. Under the tested fixed-k2 representation it is a small **line-local boundary-edge dependency**.

None of this establishes plaintext, language, semantics, a cipher family, an author, hoax/artificial origin, a historical production algorithm, or a latent semantic state.

## 1. Visible spaces are validated construction boundaries

Phase 4A/B challenged the assumption that transcription spaces were meaningful production cuts.

ZL3b first reveal:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

- real-space vs within-token reset: `D_RESET = +8.811905 bits/event`, positive `5/5`;
- observed cut beats one-atom-left and one-atom-right shifted cuts in `5/5` folds.

Independent Takahashi/IT2a replication:

> **VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a**

- IT2a `D_RESET = +8.092615`, positive `5/5`;
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

- B0 V2: `9.7089061 bits/token`;
- B1 local history: `9.5943670`;
- B2 longer causal history: `9.5461692`;
- B3 + observable line/paragraph state: `9.5172688`.

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

Issue #118 compared the same byte n-gram family in two roles:

- RESET: reset before every visible token;
- CONTINUOUS: carry across visible spaces within the physical leaf.

Both were independently mixed with corrected B3 using inner-fold-only weight selection.

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

L1 removed the byte-order asymmetry by forcing both experts to `k=2, alpha=.01`.

Frozen classification:

> **BOUNDARY-EDGE RESIDUAL SURVIVES SAME-ORDER CONTROL**

`G_edge = bits(MIX_RESET2)-bits(MIX_CONT2)`:

- mean `+0.0106322 bit/token`;
- positive `5/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET2 `9.49729565`;
- MIX_CONT2 `9.48666342`.

Predeclared held-out localization showed essentially all positive non-leaf-start contribution on `SAME_LINE`; cross-line averages were approximately zero or slightly negative. Because that table was descriptive, Issue #123 converted the line-scope hypothesis into a prospectively frozen primary test.

## 8. Issue #123 L2: source-line reset scope

L2 compared three identical fixed byte experts differing only in reset topology:

- RESET2: reset before every visible token;
- LINECONT2: carry across spaces within one source line, reset at each line start;
- LEAFCONT2: carry across line breaks within the physical leaf.

All use `k=2`, `alpha=.01`; mixture weights are selected on pooled inner folds only.

Authority:

- scientific head `87aee03e60e2eab72987eb0cc2bf8c4b992632a0`;
- workflow run `34027611090` — SUCCESS;
- artifact `9987613395`;
- artifact digest `sha256:0e84611da8fb29810a61b25d48f6cc791e5ee39377e3b08de86fa7dc1128b80b`;
- result JSON SHA-256 `dfdfca650a15f1d47bd7124898bc8483a139ce47bb17a2c2802a0d2e946dea55`;
- corrected-core and exact Issue #121 parent regression both reproduced.

Frozen classification:

> **LINE-LOCAL CONTEXT CAPTURES RESIDUAL; NO ROBUST BEYOND-LINE GAIN**

### Within-line information

`G_line = bits(MIX_RESET2)-bits(MIX_LINECONT2)`:

- fold0 `+0.0333904`;
- fold1 `+0.0209321`;
- fold2 `+0.0301701`;
- fold3 `+0.0283997`;
- fold4 `+0.0329147`;
- mean `+0.0291614 bit/token`;
- positive `5/5` — PASS.

### Carry across line breaks

`G_beyond_line = bits(MIX_LINECONT2)-bits(MIX_LEAFCONT2)`:

- fold0 `-0.0194511`;
- fold1 `-0.0128171`;
- fold2 `-0.0208697`;
- fold3 `-0.0175339`;
- fold4 `-0.0219741`;
- mean `-0.0185292 bit/token`;
- positive `0/5` — FAIL.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET2 `9.49729565`;
- MIX_LINECONT2 `9.46813424`;
- MIX_LEAFCONT2 `9.48666342`.

LINECONT2 is therefore not merely sufficient; under this fixed representation it is better than carrying the same context across line breaks in **every fold**.

Mixture weights also move coherently under inner likelihood:

- RESET2 `.04` in all folds;
- LINECONT2 `.15,.16,.15,.15,.15`;
- LEAFCONT2 `.08,.08,.09,.08,.09`.

The prospectively defined state diagnostics point the same way: RESET2→LINECONT2 is positive for ENTRY/BODY and FIRST/MIDDLE/FINAL, while LINECONT2→LEAFCONT2 is negative in every reported stratum.

Supported statement:

> The fixed-k2 residual is prospectively localized to immediate adjacency within a source line. Extending the same raw-surface history across a source-line break is predictively harmful, not beneficial, under the current model family.

This does **not** mean a line is a sentence or semantic unit. It is a production-topology result.

## 9. Cross-linguistic / cipher / historical controls

Issue #84 established a distinctive inter-unit relation regime across seven Voynich readings.

Across 101 natural-language controls, Voynich has much lower adjacent corrected MI, immediate exact-repeat excess, and much weaker 21–40-token recurrence than typical controls. Frozen common reversible-operation representatives and ten historical recipe/herbal/account/liturgical controls produced zero full hits under their preregistered joint criteria.

This narrows easy explanations but does not exclude all meaningful natural language, all historical genres or all cipher systems.

## 10. Current integrated structural picture

### Inside one visible unit

A compact second-order construction grammar largely determines admissible shape.

### At the visible-space boundary

A certain space is a sharp construction reset and its exact location replicates across two transcription lineages.

### Between adjacent units on the same source line

A small immediate raw-surface boundary-edge dependency remains after corrected B3 and same-order emission control. This is now prospectively confirmed as **line-local** under the fixed-k2 representation.

### At source-line breaks

The same short byte history should be reset. Carrying it across the break makes prediction worse in every L2 fold.

### Across nearby units more generally

A separate edit-near recurrence/cache mechanism remains predictive and broadly transportable.

### Across slower document history

Prior-paragraph/cumulative family inventory adds reproducible prediction with Currier-dependent strength.

The overall structure is therefore **compact and multiscale, with a narrow line-local adjacency residual not yet absorbed by the current observable non-latent core**.

## 11. Active frontier — explain the line-local edge before latent state

Issue #123 substantially narrows the remaining residual. The next high-value test should not be a generic hidden-state model.

With `k=2`, the genuinely token-specific cross-boundary information available to LINECONT2 is principally the previous token's terminal byte at the next token's first-byte prediction. The next prospectively frozen challenger should therefore ask:

> Can a compact explicit previous-terminal → next-initial boundary-edge model absorb the LINECONT2 gain when mixed with corrected B3?

This is more diagnostic than fitting a rich sequence model: if the compact observable edge absorbs the gain, latent state becomes less justified. If a material residual remains after that compact edge and after already-authorized Currier/line-position controls, a separately preregistered latent-state challenger becomes more defensible.

A secondary transport question is whether this line-local edge mechanism has stable strength across Currier A/B, analogous to LOCAL40 transport.

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
