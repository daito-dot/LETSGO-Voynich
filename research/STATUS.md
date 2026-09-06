# Current research status

Last consolidated: 2026-09-06
Authority for the current program: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

This file records the accepted high-level interpretation. Exact methods, first-reveal artifacts, hashes and frozen classifications remain authoritative in phase-specific plans/reports/provenance files.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The strongest current structural picture is:

1. a visible certain-space-delimited unit is a real construction boundary under the tested EVA/IVTFF representations, independently replicated in ZL3b and Takahashi/IT2a;
2. inside that unit, a compact second-order occupied-slot successor grammar explains nearly all of the replicated token-internal topology;
3. between nearby units, a short edit-distance-1 near-family recurrence mechanism is predictive and transports cleanly across Currier A/B;
4. slower previous-paragraph / causal-prefix inventory also predicts, but its useful strength differs by Currier regime and the difference survives matching the common Herbal domain;
5. corrected B3 (V2 + local/long history + observable line/paragraph state) reaches `9.51727 bits/token` from a `9.70891`-bit V2 baseline;
6. Issue #118 found a further small robust cross-boundary residual, and Issue #121 now shows that it survives an exact same-order byte-model control: `G_edge = +0.0106322 bit/token`, positive in `5/5` folds;
7. predeclared L1 diagnostics localize essentially all positive non-leaf-start contribution to **adjacent units within the same source line**; carrying the byte context across a line break gives no positive mean advantage.

The remaining residual is therefore narrower than a generic long hidden sequence memory. It is currently best treated as a small **within-line boundary-edge dependency** until stronger observable/topological controls say otherwise.

None of these results establishes plaintext, language, semantics, a cipher family, an author, hoax/artificial origin, a historical production algorithm, or a latent semantic state.

## 1. Visible spaces are validated construction boundaries

Phase 4A/B directly challenged the assumption that the project could treat visible spaces as meaningful production cuts.

### ZL3b — Issue #112

Frozen first-reveal classification:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

Using a raw-EVA representation independent of the 12-slot parser:

- real-space vs deterministic within-token reset contrast: `D_RESET = +8.811905 bits/event`, positive `5/5`;
- observed cut vs one-atom-left shift: `-8.501803`, observed wins `5/5`;
- observed cut vs one-atom-right shift: `-5.476602`, observed wins `5/5`.

### Independent Takahashi/IT2a — Issue #115

Without changing atomization, model order, smoothing, cut rules or sign gates:

- `D_RESET = +8.092615`, positive `5/5`;
- left shift `-7.968269`, observed wins `5/5`;
- right shift `-5.279450`, observed wins `5/5`.

Frozen cross-transcription classification:

> **VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a**

Literal certain spaces can therefore be treated as transcription-lineage-robust construction/production boundaries under these representations. They are **not** thereby proven natural-language word boundaries.

## 2. Token-internal construction is compact

Issue #75 plus OGH-A/B/C closed the main token-internal model ladder.

The strongest compact construction rule is a second-order occupied-slot successor grammar: the next occupied slot depends only on the previous two occupied slots. It uses 298 counted conditional probabilities and reaches the empirical-signature ceiling to within roughly 1–2% across the tested readings.

A complete memoryless V2 token grammar carries approximately:

- `~7.0 bits/token` in shape;
- `~2.7 bits/token` additional value information;
- `~9.7 bits/token` total.

A rich latent token-internal state is not required by current evidence. Memoryless token generation, however, does not reproduce the major cross-token effects.

## 3. Corrected predictive-information budget

The causal-source-order correction supersedes the original order-sensitive Phase-1/2 numbers.

Corrected Phase 1:

- B0 V2: `9.7089061 bits/token`;
- B1 local history: `9.5943670`;
- B2 longer causal history: `9.5461692`;
- B3 + observable line/paragraph state: `9.5172688`.

Thus corrected B3 improves on V2 by about `0.19164 bit/token`, roughly 2% of the V2 code length. Cross-token structure is reproducible but information-light compared with the information inside each bounded unit.

## 4. Long-history prediction is mostly slow inventory

Corrected Phase 2A/B/C shows that most apparent long-history gain is not literal detailed long-order memory.

The dominant component is an order-free causal-prefix / prior-paragraph inventory of already activated edit-near token families. A smaller actual-order residual remains.

Phase 2C:

- PREV1 conditional gain `+0.0070407 bit/token`, `5/5`;
- OLDER accumulated paragraph inventory `+0.0367964`, `5/5`;
- same-side prior history `+0.0205711`, `5/5`;
- cross-side prior history `+0.0237448`, `5/5`.

The slow signal spans multiple prior paragraphs and crosses facing/page-side topology.

## 5. LOCAL transports; PREV strength is regime-dependent

Phase 3A shows the fixed LOCAL40 edit-near mechanism transports bidirectionally across Currier A/B with nearly unchanged strength:

- A `pi_LOCAL=.14`;
- B `pi_LOCAL=.16`.

The slower PREV_PARAS mechanism is useful in both regimes, but exact scalar strength differs:

- A `alpha_ALL_PREV=.09`;
- B `alpha_ALL_PREV=.19`.

Exact PREV scalar transfer passes A→B and fails B→A, while the full CORE remains bidirectionally transportable.

Phase 3B found writing-hand metadata inadequately crossed with Currier, preventing a clean hand-causality test. Phase 3C therefore matched the common Herbal domain prospectively and still found:

- A-H `pi=.10`, `alpha=.04`;
- B-H `pi=.11`, `alpha=.08`;
- LOCAL40 bidirectional;
- PREV_PARAS A→B only;
- CORE bidirectional.

Frozen interpretation:

> **CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL**

Broad illustration/domain composition is not a sufficient explanation. Hand causality remains unresolved.

## 6. Issue #118: residual beyond corrected B3

Issue #118 asked whether a flexible sequence model adds information because it carries context across visible-space boundaries, rather than merely because it supplies a different model of token spelling.

The same byte n-gram family was used in two matched roles:

- `RESET`: reset byte history before every visible token;
- `CONTINUOUS`: carry byte history across visible spaces until the physical-leaf boundary.

Each expert was mixed independently with corrected B3 using inner-fold-only selection. The primary contrast was:

`G_context = bits(MIX_RESET) - bits(MIX_CONT)`.

Authoritative first reveal:

- scientific head `8311c429e33b292e91582a349934705383335c68`;
- workflow `34026324504`;
- artifact `9987190901`;
- result JSON SHA-256 `0aa224f64f4495dfba3b6433730f42fa553d998ac8d72ee682a8313f4664ce59`.

Frozen classification:

> **ROBUST FLEXIBLE SEQUENCE RESIDUAL EXISTS — LOCALIZATION REQUIRED**

Mean `G_context = +0.0178533 bit/token`, positive `5/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET `9.50451671`;
- MIX_CONT `9.48666342`.

The complete CONT mixture improves B3 by `G_any = +0.0306054 bit/token`, positive `5/5`.

The raw byte experts are worse than B3 in absolute code length, so the result is genuinely complementary rather than replacement by a better emission model.

## 7. Issue #121 L1: same-order boundary-edge control

Issue #118 left one model-class concern: RESET had selected byte order `k=3` in folds 0–1 while CONT selected `k=2` in all folds.

L1 removed that asymmetry prospectively by forcing **both** experts to exactly:

- `k=2`;
- `alpha=.01`.

Only the boundary-history policy differed. Mixture weight `w` was still selected on inner folds only.

Authority:

- scientific head `30a7a8caf1a358d8c98fb4376ff9d4943d44b0ff`;
- run `34026787486` — SUCCESS;
- artifact `9987357230`;
- artifact digest `sha256:3370dc79c17e7d8e700ac42264c242fed7ea93f50c9715ea1bc516e9b0b007cd`;
- result JSON SHA-256 `574216279d545c9c0c7f468c1e36f0b022ab331f21fa450bd8f0e7bf6f17899c`.

Frozen classification:

> **BOUNDARY-EDGE RESIDUAL SURVIVES SAME-ORDER CONTROL**

`G_edge = bits(MIX_RESET2)-bits(MIX_CONT2)`:

- fold0 `+0.0139393`;
- fold1 `+0.0081150`;
- fold2 `+0.0093004`;
- fold3 `+0.0108658`;
- fold4 `+0.0109406`;
- mean `+0.0106322 bit/token`;
- positive `5/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET2 `9.49729565`;
- MIX_CONT2 `9.48666342`.

RESET2 selects `w=.04` in all folds; CONT2 selects `.08,.08,.09,.08,.09`.

### Predeclared localization diagnostic

The per-target held-out contrast was grouped without refitting by relation to the immediately previous visible token.

- `SAME_LINE`: n=22,141, mean `+0.0114974`, total `+254.565 bits`;
- `CROSS_LINE_SAME_ITEM`: n=2,631, mean `-0.0007373`, total `-1.940`;
- `CROSS_ITEM_SAME_DOCUMENT`: n=226, mean `+0.0004219`, total `+0.095`;
- `CROSS_DOCUMENT_SAME_LEAF`: n=36, mean `-0.0087033`, total `-0.313`;
- `LEAF_START`: n=37, mean `+0.327669`, total `+12.124`.

`LEAF_START` is not cross-token evidence because no previous token exists there; it is the predeclared generic BOS/END start-distribution difference between experts.

For actual cross-token transitions, essentially all positive aggregate contribution comes from **SAME_LINE**. Across a line break the mean contribution is approximately zero or slightly negative.

Entry/first-line targets show a larger descriptive mean than body/middle targets (`~0.0193` vs `~0.0083–0.0087`), but this is not yet a causal state attribution.

### Interpretation

The residual is now much narrower than “some flexible sequence memory survives.”

Supported statement:

> A small reproducible amount of immediate raw-surface information passes across adjacent visible construction units even after forcing the competing byte models to identical order and smoothing. In the predeclared localization, that advantage is concentrated within source lines and does not positively carry across line breaks.

This is consistent with line-local boundary-adjacent morphotactics, local production sequencing, or another observable within-line dependency. It does not by itself imply a hidden semantic state.

## 8. Cross-linguistic / cipher / historical controls

Issue #84 established a distinctive inter-unit relation regime across seven Voynich readings.

Across 101 natural-language controls:

- Voynich adjacent corrected MI is roughly `0.053–0.111 bits`;
- controls range about `0.173–1.584`, median `~0.820`;
- Voynich shows immediate exact-repeat excess while most ordinary-language controls suppress it;
- ordinary-language controls show strong 21–40-token recurrence/burstiness while Voynich is weak there.

Frozen common reversible-operation representatives and ten historical recipe/herbal/account/liturgical controls produced zero full hits under their preregistered joint criteria.

This narrows easy explanations but does not exclude all meaningful natural language, all historical genres or all cipher systems.

## 9. Current integrated structural picture

### Inside one visible unit

A compact second-order construction grammar largely determines admissible shape; once shape is fixed, literal values add relatively little information.

### At the visible boundary

A certain space is a sharp raw-shape context reset and the exact cut replicates across two reading lineages.

### Between adjacent units on the same line

A small immediate boundary-edge dependency remains after corrected B3 and same-order emission control. This is currently the narrowest localized residual.

### Between nearby units more generally

A short edit-near recurrence/cache mechanism is predictive and broadly transportable.

### Across slower document history

Prior-paragraph/cumulative family inventory adds reproducible but smaller prediction; its useful scalar strength varies by Currier regime.

The overall structure is therefore **compact and multiscale, with a small line-local adjacency residual not yet absorbed by the current observable non-latent model**.

## 10. Active frontier — confirm line-local scope before latent state

The highest-value next test is not a rich hidden-state model.

L1 suggests the remaining byte-context advantage is carried almost entirely between adjacent visible units on the same source line. That was a predeclared diagnostic, not the primary L1 gate, so the next step should convert it into a prospective confirmatory comparison:

> reset CONT2 history at every source-line boundary while still carrying it across spaces within the line, then compare against RESET2 under the same corrected B3 mixture protocol.

If a line-reset CONT2 reproduces the useful residual, the effective context scope is line-local. If it loses the residual, the L1 descriptive localization was insufficient and broader topology must be reconsidered.

Only after line topology and already-authorized Currier/observable-state effects are tested prospectively should a latent-state challenger receive interpretation.

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
- visible spaces as proven natural-language word boundaries.
