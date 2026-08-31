# Current research status

Last consolidated: 2026-09-01

This file controls the current accepted high-level interpretation. Phase-specific frozen plans, first-reveal results and reports remain authoritative for exact methods and numbers.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The project has nevertheless established several reproducible structural constraints and eliminated a large number of attractive semantic, historical-cipher and direct-music interpretations under controlled tests.

The research objective remains constructive: use reproducible constraints to narrow viable generation/transformation mechanisms and, when sufficiently constrained, attack the inverse/decoding problem. Falsification is the discipline, not the objective.

## Read the current token-construction lane correctly

The active structural lane is specifically about **how one space-delimited Voynich token is internally assembled** under a frozen 12-slot representation.

It is **not** sentence-level grammar, and visible spaces are not assumed to be proven natural-language word boundaries.

Normative orientation: `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

The strategic question is not merely whether tokens “look structured.” It is whether a non-trivial token-construction layer survives lower-order controls and independent readings strongly enough to become a prospective constraint on later inverse/decoding models.

## Other strongest structural state

### Paragraph-entry and local recurrence

Phase62–64 established frozen A1/A1-R1 as the leading tested model for short-range near-family recurrence geometry. It received prospective H62 support, survived training-vocabulary restriction, and transferred to an independent EvaT reading without retuning.

This does not identify A1 as the historical production algorithm.

Phase69/70 demonstrated that strong A1-like local recurrence can coexist with exactly recoverable meaningful plaintext. Therefore:

> **Short-range recurrence is a formal surface constraint, not evidence by itself that the text lacks semantics or plaintext.**

The signed paragraph-entry effect S1 remains harder to reproduce. Phase71's tested Alberti initial-signal/reset mechanism failed in the opposite S1 direction.

## Token-internal construction program — #55 → #58A → #58B → #58C

### Issue #55

#55A found cross-leaf slot3×slot5 dependence. #55B showed that essentially all of it reduces to binary occupancy exclusion.

Frozen classification:

> `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`

### Issue #58A

The complete 66-edge audit removed selection bias around slot3×slot5.

- `22/66` edges survived the frozen family-wise primary rule;
- selected `(3,5)` ranked only `22/66`;
- strong positive co-construction and negative exclusion coexist;
- all `66/66` canonical pair co-occupancies are parser-admissible.

Frozen classification:

> `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

### Issue #58B / #62

#58B asked whether the raw complete signed graph is stable across Currier/section/line-position strata.

Real graph similarities were high, but the line-local marginal-preserving null itself generated whole-graph correlations near the same range (`median maxT ≈ 0.949`). No planned similarity was family-wise exceptional and no practical difference gate was met.

Frozen classifications:

> `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`

> `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

Scientific consequence: raw whole-graph similarity is substantially contaminated by lower-order line-local slot prevalence / occupancy architecture.

### Issue #58C / #64 — residual graph beyond line-local prevalence

#58C prospectively calibrated every one of the 66 conditional occupancy edges against its own line-local null distribution.

To prevent circularity it used:

- 1,000 reference nulls only to define the residual transform;
- an independent 1,000 test nulls only to validate residual existence/similarity;
- a pooled residual-existence gate before any cross-stratum interpretation.

Frozen first-reveal overall classification:

> **`RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`**

Pooled residual existence:

- real `E_ALL = 3.23155`;
- test-null median `0.99004`;
- test-null maximum `1.28318`;
- `p_exist_ALL = 1/1001`;
- physical-leaf reliability `W_ALL = 0.94471`.

Thus the real residual graph is far outside the complete independent test-null ensemble and strongly reproducible across physical leaves.

All seven planned strata separately passed the family-wise residual-existence gate (`p_E,maxT = 1/1001`) with high fold reliability.

All seven cross-stratum residual similarities also exceeded the full independent test-null maxT ensemble (`p_R,maxT = 1/1001` each).

Frozen family classifications:

> **`REGISTER/SECTION RESIDUAL MODULATION`**

> **`LINE-POSITION RESIDUAL MODULATION`**

Stable residual relations included all three Currier-B section comparisons and line interior-vs-final. Currier A-vs-B within Herbal and line-initial comparisons were related but modulated. No planned contrast met the frozen `DIFFERENT_RESIDUAL_OR_MIXTURE` gate.

### Accepted token-construction interpretation

The strongest supported description is now:

> **Under the frozen 12-slot representation, Voynich space-delimited tokens contain a broad, reproducible internal interaction system that cannot be explained by line-local slot prevalence alone. A large shared residual construction core is present across the tested manuscript strata, with measurable Currier/section/line-position modulation rather than evidence for wholly separate token grammars.**

Do **not** reduce this to “one universal grammar”: exact invariance was not supported.

Exact #58C report: `experiments/occupancy-graph-residual/REPORT_A.md`.

First-reveal raw SHA-256:

`fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`

## Current token-construction frontier

The main remaining threat before using #58C as an inverse-model constraint is **transcription/representation dependence**.

Next question:

> **Does the #58C residual-existence result and its shared-core-plus-modulation geometry survive a materially independent Voynich transcription/reading without retuning the 12-slot interpretation or selecting favorable edges?**

This replication must distinguish:

1. residual existence in the independent reading;
2. cross-reading agreement of the complete 66-edge residual graph;
3. replication of broad shared-core/modulation geometry.

Only after that should replicated token-construction constraints be used prospectively to restrict reversible generative/inverse models.

## Content-relation program

Phase65–68 externally grounded object-local image↔text tests were negative under frozen representations. These results do not establish semantic absence, plant-name absence, or cipher absence.

## Direct-music program — Issue #26

The bounded direct-music program A–E17 is complete.

Accepted conclusion:

> **No tested, independently constrained direct-musical or music-cipher model provides held-out evidence that Voynich running text encodes music or readable plaintext through a musical state system.**

## Historical real-cipher control lane

The Phase72 source-audit branch remains source-development work, not accepted current science. No Phase72 Voynich target score is authorized until source population and genuine message-entry boundary semantics are frozen prospectively.

## Interpretation limits

Do not infer:

- that spaces are true linguistic word boundaries;
- sentence-level grammar from the token-construction graph;
- that any slot has a semantic meaning;
- that the residual graph is a plaintext alphabet or cipher table;
- that #58C identifies a historical generator;
- that exact token grammar is invariant across all strata;
- that recurrence or token construction proves semantic presence or absence;
- that the manuscript uses or does not use a cipher in general;
- that negative morphology tests falsify all plant-related content;
- that the manuscript is deciphered.

## Reproducibility / repository state

First-reveal provenance is preserved beyond Actions retention for #55, #58A, #58B and #58C. #58C is archived under `experiments/occupancy-graph-residual/first-reveal/` with raw-result SHA-256:

`fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`

Historical reproducibility debts remain documented in `research/REPRODUCIBILITY_AUDIT.md` and phase-specific reports.