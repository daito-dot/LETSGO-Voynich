# Current research status

Last consolidated: 2026-09-06
Authority for the current program: Issue #88 and `research/PREDICTIVE_INFORMATION_PROGRAM.md`.

This file is the current accepted high-level interpretation. Exact methods, hashes, first-reveal artifacts and frozen classifications remain authoritative in the phase-specific plans/reports/provenance files.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The strongest current structural picture is now multiscale and unusually constrained:

1. a visible-space-delimited unit has a compact internal construction grammar;
2. visible certain spaces themselves behave as sharp construction/context resets and this replicates across ZL3b and independent Takahashi/IT2a readings;
3. between those bounded units, a short edit-distance-1 near-family recurrence mechanism is manuscript-wide and transfers cleanly across Currier A/B;
4. a slower previous-paragraph / causal-prefix inventory component is also predictive, but its useful strength differs by regime, especially Currier A versus B;
5. ordinary-language, frozen common-transform and selected historical-formulaic controls do not jointly reproduce the observed inter-unit relation geometry.

These are structural and predictive results. They do **not** establish plaintext, language, semantics, a cipher family, an author, a hoax/artificial origin, or the historical production mechanism.

## 1. The visible unit is now validated as a construction boundary

Phase 4A/B closed the main construct-validity threat in the predictive-information program: the space-delimited unit is no longer being used merely because the transcription happened to contain spaces.

### ZL3b — Issue #112, PRs #113–#114

A score-free Gate froze a raw-EVA representation independent of the 12-slot SlotParser:

- primary REAL_SPACE = literal IVTFF `.` certain space only;
- common connected EVA composites atomized by a fixed longest-match rule;
- uncertain/exceptional local readings excluded as complete events;
- deterministic within-token midpoint pseudo-boundaries;
- original five physical-leaf folds;
- no target-guided boundary search.

Frozen first-reveal classification:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

Held-out results:

- P1 real-space versus within-token reset contrast: `D_RESET = +8.811905 bits/event`, positive in `5/5` folds;
- P2 observed cut minus one-atom-left shift: `-8.501803 bits/event`, observed cut wins `5/5`;
- P2 observed cut minus one-atom-right shift: `-5.476602 bits/event`, observed cut wins `5/5`.

### Independent Takahashi/IT2a — Issue #115, PRs #116–#117

The same atomization logic, cut rules, model order, smoothing and sign gates were frozen before the IT2a reveal. The canonical IT2a source reproduced the earlier independent-transcription byte authority exactly.

Frozen IT2a classification:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

Frozen cross-transcription classification:

> **VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a**

IT2a results:

- P1 `D_RESET = +8.092615 bits/event`, positive `5/5`;
- P2 left shift `-7.968269 bits/event`, negative `5/5`;
- P2 right shift `-5.279450 bits/event`, negative `5/5`.

Magnitude agreement was not a pass criterion, but IT2a effects are descriptively about 92–96% of the corresponding ZL3b effects.

### Interpretation

Literal certain spaces can now be treated as **transcription-lineage-robust construction/production boundaries under the tested EVA/IVTFF representations**.

This does **not** make them proven natural-language words. A natural-language word, cipher group, formal-notation unit, procedural output unit or another bounded historical unit could all create a reset of this kind.

## 2. Token-internal construction is compact

Issue #75 plus OGH-A/B/C established that the residual token-construction topology is much smaller than initially expected.

The strongest compact model is a second-order occupied-slot successor grammar: the next occupied slot depends only on the previous two occupied slots. It uses 298 counted conditional probabilities and reaches the empirical-inventory ceiling to within roughly 1–2%.

A complete memoryless V2 token grammar carries approximately:

- `~7.0 bits/token` in shape;
- `~2.7 bits/token` additional value information;
- `~9.7 bits/token` total.

No rich latent token-construction state or higher-order configuration rule is currently required by the evidence.

The memoryless token generator does **not** reproduce the major cross-token recurrence/paragraph effects, so those structures are genuinely above the token-internal grammar.

## 3. Cross-token predictive information is real but information-light

Corrected source-order reruns supersede the original order-sensitive Phase-1/2 numbers.

Corrected Phase 1:

- B0 V2: `9.7089061 bits/token`;
- B1 local history: `9.5943670`;
- B2 longer history: `9.5461692`;
- B3 + observable position/state: `9.5172688`.

Thus the best tested non-latent Phase-1 ladder reduces the V2 code length by about `0.19164 bit/token`, only about 2% of the ~9.71-bit token code.

This is enough to be reproducible and scientifically important, but it is not evidence for several hidden bits of sentence-level syntax.

## 4. The long-history effect is mostly slow inventory, not literal long memory

Corrected Phase 2A/B/C localizes the apparent long-history gain.

The dominant component is an order-free causal-prefix / previous-paragraph inventory of already activated edit-near token families. A much smaller actual order/lag residual survives after that inventory is represented.

Phase 2C further shows:

- PREV1 conditional gain `+0.0070407 bit/token`, positive `5/5`;
- OLDER accumulated paragraph inventory `+0.0367964`, positive `5/5`;
- same-side prior history `+0.0205711`, positive `5/5`;
- cross-side prior history `+0.0237448`, positive `5/5`.

The slow signal therefore spans multiple prior paragraphs and survives across facing/page-side topology. It is not adequately described as “copy the immediately previous paragraph.”

## 5. Short local recurrence transports; slow strength is regime-dependent

### Phase 3A — Currier A/B

The fixed LOCAL40 edit-near mechanism transports bidirectionally with nearly unchanged strength:

- Currier A source `pi_LOCAL=.14`;
- Currier B source `pi_LOCAL=.16`.

The slower PREV_PARAS architecture is useful in both regimes, but exact scalar strength is asymmetric:

- A `alpha_ALL_PREV=.09`;
- B `alpha_ALL_PREV=.19`.

Exact PREV scalar transfer passes A→B and fails B→A, while the full CORE remains bidirectionally transportable.

This is best read as a shared slow mechanism with regime-dependent strength, not evidence for different mechanism families.

### Phase 3B/C — metadata and matched Herbal

The score-free metadata audit found writing hand `$H` and legacy Currier hand `$C` too confounded with Currier A/B for causal attribution. The only broadly crossed illustration/domain level was Herbal.

Matched pure-Herbal Phase 3C retained:

- A-H `pi=.10`, `alpha=.04`;
- B-H `pi=.11`, `alpha=.08`;
- LOCAL40 bidirectional transport;
- PREV_PARAS A→B only;
- CORE bidirectional transport.

Frozen interpretation:

> **CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL**

Broad illustration/domain composition is therefore not sufficient to explain the slow-strength asymmetry. Hand remains unresolved because the metadata are not adequately crossed.

## 6. Cross-linguistic / cipher / historical controls

Issue #84 established a distinctive inter-unit relation regime across seven Voynich readings.

Across 101 natural-language controls:

- Voynich adjacent corrected MI is roughly `0.053–0.111 bits`;
- language controls range about `0.173–1.584`, median `~0.820`;
- Voynich shows immediate exact-repeat excess;
- ordinary language usually suppresses immediate repeats;
- ordinary language shows strong 21–40-token recurrence/burstiness, while Voynich is weak there.

Frozen common reversible-operation representatives and ten historical recipe/herbal/account/liturgical controls also produced zero full hits under their preregistered joint criteria.

This narrows easy explanations. It does **not** reject all meaningful natural language, all historical genres or all cipher systems.

## 7. Current integrated structural picture

The experimentally separated scales are now:

### Inside a construction unit

A compact second-order slot-successor grammar explains most token-internal topology.

### Between nearby construction units

A short edit-distance-1 near-family recurrence/cache effect is predictive and transports across Currier A/B with nearly stable strength.

### Across paragraphs / slower document history

Accumulated prior token-family inventory adds smaller but reproducible predictive information. Its useful strength varies by Currier regime and the difference survives matching the common Herbal domain.

### Boundary itself

The visible certain space is a sharp reset in local raw-shape construction and its exact location replicates across ZL3b and IT2a.

This combination is compatible with several historical mechanisms. It is not yet an identification of one.

## 8. Active frontier — residual predictive-information gate before latent state

Issue #88 remains open because its latent-state licensing rule is not yet satisfied.

The next high-value question is:

> **After the strongest corrected non-latent predictive core is frozen, does a separately defined flexible sequence challenger add reproducible held-out predictive information?**

The corrected B3 ladder is the current natural anchor because it already combines V2 emission, long causal history and observable line/paragraph state without latent variables. Phase 2/3 provide the mechanism interpretation and transport constraints around that predictive core.

The next experiment should therefore quantify a **conditional residual**, not simply fit a more realistic-looking generator. A flexible challenger may be used only as an empirical model-class ceiling. If it cannot improve the frozen core robustly, rich latent-state work is not licensed. If it does improve the core reproducibly, the residual must then be localized against additional observable/history controls before any latent state receives interpretation.

Do not reopen arbitrary tokenization search: Phase 4 has validated the current construction boundary under two transcription lineages.

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

The research objective remains inverse: progressively narrow viable production/transformation mechanisms using prospective, held-out and transportable constraints, then attack decoding only when the evidence licenses it.
