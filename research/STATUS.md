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
6. Issue #118 now shows a further **small but robust cross-boundary residual** beyond B3 and a matched byte-level emission complement: `G_context = +0.01785 bit/token`, positive in `5/5` physical-leaf folds.

The new residual means the tested non-latent core has **not** exhausted all surface predictability. Its absolute information rate is small. It licenses localization against observable regime/state/support effects; it does not yet license semantic interpretation of a latent state.

None of these results establishes plaintext, language, semantics, a cipher family, an author, hoax/artificial origin, or the historical production algorithm.

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

## 6. Issue #118: robust residual beyond corrected B3

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

`G_context` by fold:

- fold0 `+0.0349457`;
- fold1 `+0.0232139`;
- fold2 `+0.0093004`;
- fold3 `+0.0108658`;
- fold4 `+0.0109406`.

Mean `G_context = +0.0178533 bit/token`, positive `5/5`.

The complete CONT mixture improves B3 by `G_any = +0.0306054 bit/token`, also positive `5/5`.

Mean code lengths:

- B3 `9.51726884`;
- MIX_RESET `9.50451671`;
- MIX_CONT `9.48666342`.

CONT receives inner-selected mixture weights `.08–.09`; RESET receives only `.01–.04`. The raw byte experts are worse than B3 in absolute code length, so the result is genuinely complementary rather than replacement by a better emission model.

### Scale and interpretation

The cross-boundary residual is only about `0.018 bit/token`, roughly `0.19%` of B3 code length. It is robust under the frozen 5-fold rule but quantitatively small.

Supported statement:

> A small, stable component of literal surface prediction remains after corrected B3 and after matching out byte-level token-emission complement; this component depends on carrying short byte context across visible-space construction boundaries.

This could still be incomplete observable-history specification, Currier/regime-dependent strength, boundary-adjacent morphotactics, support effects, or a genuinely unobserved state. Issue #118 does not distinguish them.

## 7. Cross-linguistic / cipher / historical controls

Issue #84 established a distinctive inter-unit relation regime across seven Voynich readings.

Across 101 natural-language controls:

- Voynich adjacent corrected MI is roughly `0.053–0.111 bits`;
- controls range about `0.173–1.584`, median `~0.820`;
- Voynich shows immediate exact-repeat excess while most ordinary-language controls suppress it;
- ordinary-language controls show strong 21–40-token recurrence/burstiness while Voynich is weak there.

Frozen common reversible-operation representatives and ten historical recipe/herbal/account/liturgical controls produced zero full hits under their preregistered joint criteria.

This narrows easy explanations but does not exclude all meaningful natural language, all historical genres or all cipher systems.

## 8. Current integrated structural picture

### Inside one visible unit

A compact second-order construction grammar largely determines admissible shape; once shape is fixed, literal values add relatively little information.

### At the visible boundary

A certain space is a sharp raw-shape context reset and the exact cut replicates across two reading lineages.

### Between nearby units

A short edit-near recurrence/cache mechanism is predictive and broadly transportable.

### Across slower document history

Prior-paragraph/cumulative family inventory adds reproducible but smaller prediction; its useful scalar strength varies by Currier regime.

### Beyond the strongest current non-latent summary

A further `~0.018 bit/token` cross-boundary byte-context residual survives matched-emission control in all five folds.

The overall structure is therefore **compact and multiscale, but not yet completely closed by the current observable non-latent model**.

## 9. Active frontier — localize the residual before latent state

Issue #118 passes the first residual-capacity gate but does **not** directly license a rich hidden-state model.

The next confirmatory step must ask where the `~0.018 bit/token` residual lives, using prospectively frozen controls. Priority order:

1. Currier A/B or other already-authorized observable regime dependence;
2. already-defined paragraph-entry/body and line-position states;
3. support/emission and boundary-adjacent representation effects under the same matched RESET/CONT design;
4. independent representation/transcription replication where the byte representation can be frozen without target-driven mapping.

Only a residual that survives these observable/support controls should motivate a separately preregistered latent-state challenger.

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
