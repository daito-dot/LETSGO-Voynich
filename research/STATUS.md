# Current research status

Last consolidated: 2026-09-01

This file controls the current accepted high-level interpretation. Phase-specific frozen plans, first-reveal results and reports remain authoritative for exact methods and numbers.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The project has nevertheless established several reproducible manuscript-level structural constraints and eliminated many attractive semantic, historical-cipher and direct-music interpretations under controlled tests.

The research objective is constructive: use reproducible constraints to narrow viable generation/transformation mechanisms and then attack the inverse/decoding problem. Falsification is the discipline, not the objective.

## Read the current token-construction lane correctly

The token-construction program concerns **how one space-delimited Voynich token is internally assembled** under an established 12-slot representation.

It is **not** sentence-level grammar, and visible spaces are not assumed to be proven natural-language word boundaries.

Normative orientation: `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

The lane has now moved beyond asking whether tokens merely “look structured.” It has established a cross-reading replicated token-internal surface signature strong enough to be used prospectively to reject later reversible/generative/inverse models that cannot reproduce it.

## Other strongest structural state

### Paragraph-entry and local recurrence

Phase62–64 established frozen A1/A1-R1 as the leading tested model for short-range near-family recurrence geometry. It received prospective H62 support, survived training-vocabulary restriction, and transferred to an independent EvaT reading without retuning.

This does not identify A1 as the historical production algorithm.

Phase69/70 demonstrated that strong A1-like local recurrence can coexist with exactly recoverable meaningful plaintext. Therefore:

> **Short-range recurrence is a formal surface constraint, not evidence by itself that the text lacks semantics or plaintext.**

The signed paragraph-entry effect S1 remains harder to reproduce. Phase71's tested Alberti initial-signal/reset mechanism failed in the opposite S1 direction.

## Token-internal construction program — #55 → #58A → #58B → #58C → #58D

### Issue #55

#55A found cross-leaf slot3×slot5 dependence. #55B showed that essentially all of it reduces to binary occupancy exclusion.

> `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`

### Issue #58A

The selection-aware complete 66-edge audit removed selection bias around slot3×slot5.

- 22/66 edges survived the frozen family-wise primary rule;
- selected `(3,5)` ranked only 22/66;
- strong positive co-construction and negative exclusion coexist;
- all 66/66 canonical pair co-occupancies are parser-admissible.

> `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

### Issue #58B / #62

Raw complete-graph similarities across Currier/section/line-position strata were high, but the line-local marginal-preserving null itself generated correlations near the same range (`median maxT ≈ 0.949`).

> `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`

> `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

Scientific consequence: raw whole-graph resemblance is substantially contaminated by lower-order line-local slot prevalence / occupancy architecture.

### Issue #58C / #64 — residual graph beyond line-local prevalence

#58C prospectively calibrated every one of the 66 conditional edges against its own line-local null distribution, using 1,000 reference nulls to define residuals and an independent 1,000 test nulls for validation.

Frozen classification:

> **`RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`**

Pooled ZL3b result:

- `E_ALL = 3.23155`;
- test-null maximum `1.28318`;
- `p_exist_ALL = 1/1001`;
- `W_ALL = 0.94471`.

All seven planned strata passed residual existence. Stable residual relations were the three Currier-B section comparisons and interior-vs-final; Currier A/B within Herbal and line-initial comparisons were related but modulated. No planned contrast met the multiple/different-grammar gate.

### Issue #58D / #66 — independent Takahashi/IT2a reading replication

#58D tested whether #58C was merely a ZL3b reading artifact.

A source/population-only Stage A froze IT2a before target scoring:

- Takeshi Takahashi / `EvaT`;
- exact SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- 99/99 #58C physical leaves overlap;
- 34,411 clean tokens;
- 28,280 directly accepted by the unchanged 12-slot parser;
- coverage `82.18%`.

No pair/residual target metric was computed during source selection.

IT2a then received its **own** 1,000-reference + independent 1,000-test line-local null calibration.

Frozen overall classification:

> **`INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE`**

#### Independent residual existence

- `E_IT_ALL = 3.21363`;
- IT test-null median `0.99252`;
- IT test-null maximum `1.25891`;
- `p_exist_IT = 1/1001`;
- `W_IT_ALL = 0.95377`.

All seven planned IT2a strata separately passed family-wise residual existence at `1/1001`.

#### Direct complete-graph reading-to-reading replication

The confirmatory comparison retained **all 66 edges**.

Pooled ZL3b↔IT2a:

- Pearson correlation: **`0.98845`**;
- residual sign agreement: **`65/66`**;
- correlation maxT p: `1/1001`;
- sign-agreement maxT p: `1/1001`.

All eight planned groups (`ALL`, four Currier/section groups, three line-position groups) independently meet the frozen strong cross-reading replication class:

- Pearson range `0.97031–0.99548`;
- sign agreement `64/66–66/66`;
- every group has both maxT p-values `1/1001`.

The 1,000 independent IT2a test nulls never exceeded:

- cross-reading correlation maxT `0.43199`;
- sign-agreement maxT `47/66`.

This materially reduces the explanation that the #58C topology is peculiar to the ZL3b reading.

#### Broad modulation geometry

Within IT2a, the same family-level classifications reappear:

> `REGISTER/SECTION RESIDUAL MODULATION`

> `LINE-POSITION RESIDUAL MODULATION`

All seven contrasts are stable or related/modulated; none is materially different.

The secondary finer ordering test did **not** pass:

- `G_core = 0.83696`;
- `G_mod = 0.68217`;
- `Delta = 0.15479`;
- `p_Delta = 0.08791`.

Therefore the broad shared-core-plus-modulation geometry is supported, but do not claim that every fine ordering of “stable” versus “modulated” contrasts is identical across readings.

### Accepted token-construction interpretation after #58D

The strongest supported description is now:

> **Within a common EVA/IVTFF representational framework, Voynich space-delimited tokens exhibit a manuscript-level internal construction signature that survives independent ZL3b and Takahashi/IT2a readings. A broad residual core is shared across manuscript strata with measurable modulation rather than an exactly uniform token grammar.**

This cross-reading replicated signature is now strong enough to serve as a **prospective surface-generation constraint** on later mechanism/inverse-model tests.

It is still not a semantic interpretation or decipherment.

Exact #58D report: `experiments/occupancy-graph-independent-transcription/REPORT_A.md`.

#58D first-reveal raw SHA-256:

`f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6`

## Current frontier — constrained reversible/inverse mechanism discrimination

The immediate high-information question is no longer another local occupancy discovery or another ZL/IT replication.

Next question:

> **Can a bounded reversible/generative/inverse mechanism jointly reproduce the already established manuscript-level constraints on unseen material without post-hoc repair?**

At minimum the next plan-first tournament should jointly enforce:

1. the cross-reading replicated residual token-construction constraints from #58C/#58D;
2. accepted A1/H62 short-range near-family recurrence geometry;
3. the difficult signed S1 paragraph-entry specialization;
4. prospectively selected additional manuscript-level constraints;
5. explicit complexity / degrees-of-freedom accounting.

Candidate mechanisms should now be rejected for failing the established constraints rather than allowed to invent new explanations after seeing each mismatch.

A GC2a/v101 alphabet-level robustness lane remains scientifically useful, but after the strong IT2a reading-lineage replication it is a secondary robustness lane rather than the highest-information immediate frontier.

## Content-relation program

Phase65–68 externally grounded object-local image↔text tests were negative under frozen representations. These results do not establish semantic absence, plant-name absence, or cipher absence.

## Direct-music program — Issue #26

The bounded direct-music program A–E17 is complete.

> **No tested, independently constrained direct-musical or music-cipher model provides held-out evidence that Voynich running text encodes music or readable plaintext through a musical state system.**

## Historical real-cipher control lane

The Phase72 source-audit branch remains source-development work, not accepted current science. No Phase72 Voynich target score is authorized until source population and genuine message-entry boundary semantics are frozen prospectively.

## Interpretation limits

Do not infer:

- that spaces are true linguistic word boundaries;
- sentence-level grammar from token-construction structure;
- that any slot has semantic meaning;
- that the residual graph is a plaintext alphabet or cipher table;
- that #58C/#58D identifies a historical generator;
- that exact token grammar is invariant across all strata;
- that IT2a gives complete alphabet/publication-pipeline independence from ZL3b;
- that recurrence or token construction proves semantic presence or absence;
- that the manuscript uses or does not use a cipher in general;
- that negative morphology tests falsify all plant-related content;
- that the manuscript is deciphered.

## Reproducibility / repository state

First-reveal provenance is preserved beyond Actions retention for #55, #58A, #58B, #58C and #58D.

#58D is archived directly under `experiments/occupancy-graph-independent-transcription/first-reveal/` with raw-result SHA-256:

`f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6`

During #58D preflight, a single corrupted text-transport chunk in the later repository copy of #58C was discovered. The original #58C Actions artifact remained intact; only the transport copy was repaired from that verified original. #58C scientific bytes and classification did not change. See `experiments/occupancy-graph-residual/first-reveal/ARCHIVE_REPAIR_20260901.md`.

Historical reproducibility debts remain documented in `research/REPRODUCIBILITY_AUDIT.md` and phase-specific reports.