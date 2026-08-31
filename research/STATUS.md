# Current research status

Last consolidated: 2026-09-01

This file controls the current accepted high-level interpretation. Phase-specific frozen plans, first-reveal results and reports remain authoritative for exact methods and numbers.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The project has nevertheless established several reproducible structural constraints and eliminated a large number of attractive semantic, historical-cipher and direct-music interpretations under controlled tests.

The research objective remains constructive: use reproducible constraints to narrow the space of viable generation/transformation mechanisms and, when sufficiently constrained, attack the inverse/decoding problem. Falsification is the discipline, not the objective.

## Read the current token-construction lane correctly

The active structural lane is specifically about **how one space-delimited Voynich token is internally assembled** under a frozen 12-slot representation.

It is **not** sentence-level grammar, and visible spaces are not assumed to be proven natural-language word boundaries.

Normative orientation: `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

The current strategic question is:

> Do the non-trivial internal token-construction constraints form one shared manuscript-wide system, or do they change by Currier/register/section/line position?

Equivalently, this lane is partly determining **how many token-generation systems a later inverse/decoding model must explain**.

## Current strongest structural state

### Paragraph-entry and local recurrence

Phase62–64 established the frozen A1/A1-R1 mechanism as the leading tested model for short-range near-family recurrence geometry. It received prospective H62 support, survived training-vocabulary restriction, and transferred to an independent EvaT reading without retuning.

This does not identify A1 as the historical production algorithm.

Phase69/70 then demonstrated that strong A1-like local recurrence can coexist with exactly recoverable meaningful plaintext. Therefore:

> **Short-range recurrence is a formal surface constraint, not evidence by itself that the text lacks semantics or plaintext.**

The harder discriminator remains the signed paragraph-entry effect S1. The tested reversible meaningful-text constructions reproduce much of S2/S3/H62 but remain weak on S1.

### Paragraph-entry boundary mechanism

Phase71 tested an independently motivated Alberti initial-alignment signal and paragraph reset. The reset arm projected in the opposite S1 direction from Voynich and failed in all five folds.

Accepted conclusion:

> **The tested Alberti message-initial signal/reset mechanism is not sufficient to explain the Voynich paragraph-entry direction.**

This is one bounded historical-mechanism failure, not a rejection of all ciphers or boundary mechanisms.

## Token-internal construction program — Issues #55, #58A, #58B

### Issue #55

#55A found cross-leaf dependence between native slot3 and slot5 factors. #55B showed that essentially all of that signal reduces to the binary fact that the two slots are almost never occupied together:

- five-state gain: `0.04417745 bits/token`;
- binary EMPTY/nonEMPTY gain: `0.04421504`;
- subtype residual: `-0.00003747`;
- subtype-residual null p: `0.26973`;
- only 3 pooled tokens co-occupy slot3 and slot5;
- canonical nonempty slot3×slot5 combinations are parser-admissible.

Frozen classification:

> `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`

### Issue #58A — complete 66-edge occupancy graph

#58A removed selection bias around slot3×slot5 by auditing all `C(12,2)=66` binary slot pairs under one frozen family-wise test.

First-reveal result:

- `22/66` edges survive global `p_maxT <= .01` with all five held-out gains positive;
- selected `(3,5)` ranks only `22/66`;
- `(3,5)` remains a real exclusion but loses family-wise exceptionality after controlling for other-slot occupancy complexity (`K_other` conditional `p_maxT=0.55644`);
- all `66/66` canonical two-slot co-occupancies are parser-admissible;
- the graph contains strong positive co-construction and strong negative exclusion relations;
- strongest primary edge `(8,10)` has mean held-out gain `0.76767 bits/token`, phi `+0.92378`, and remains family-wise strong after `K_other` conditioning.

Frozen classification:

> `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

Correct interpretation: the selected slot3×slot5 relation was real but not a unique key. The research object became the complete signed token-internal occupancy graph.

### Issue #58B / #62 — graph stability across manuscript strata

#58B asked whether the complete signed 66-edge graph is the same across externally defined Currier/section/line-position strata.

The preregistered test used `K_other`-conditional Yule-Q graph vectors, five physical-leaf folds, directional held-out transfer, and 1,000 deterministic line-local slot-occupancy relocation nulls preserving line×slot marginal counts and metadata.

Observed real-data graph similarities were mostly high:

- register/section `R_full`: `0.6995–0.9613`;
- position `R_full`: `0.8682–0.9431`;
- within-stratum reliabilities were approximately `0.94–0.99`;
- held-out cross-stratum transfers were mostly strong.

But the null itself generated extremely high complete-graph resemblance:

- median maxT: `0.94939`;
- 95th percentile: `0.96323`.

None of the seven planned similarities reached the frozen family-wise `p_maxT <= .01` support criterion. At the same time, no contrast approached the frozen practical difference gates (`R<.40` or transfer `<.30`).

Frozen global classifications:

> **`CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`**

> **`LINE-POSITION GRAPH STABILITY INCONCLUSIVE`**

This means:

- **not established:** one deep shared 66-edge interaction graph;
- **not established:** material Currier/section/position differences;
- **retained:** strong token-internal occupancy structure and high numerical cross-stratum resemblance;
- **new constraint:** raw whole-graph similarity is substantially driven by lower-order line-local slot prevalence / occupancy architecture.

Exact report: `experiments/occupancy-graph-stability/REPORT_A.md`.

Program purpose: `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

## Current token-construction frontier

Do not repeat #58B with a looser threshold or select visually strong individual edges.

The next plan-first question is:

> **After subtracting/standardizing the interaction expected from line-local slot prevalence, does a graph-level residual token-construction signal exist, and if it exists, does that residual pattern transfer across manuscript strata?**

The follow-up should separate two gates:

1. **residual existence** — prove that the residual interaction vector itself exceeds an independent null;
2. **residual transfer** — only then ask whether its signed pattern is shared across Currier/section/position.

To avoid circularity, use separately frozen reference-null and test-null ensembles. The reference ensemble defines edge-wise null expectation/scale; the independent test ensemble validates residual existence/transfer and controls multiplicity.

This is a new hypothesis generated by #58B, not a repair of the frozen #58B test.

## Content-relation program

Phase65–68 produced externally grounded object-local image↔text tests and returned null results under frozen representations.

Retained content state:

- Phase65A established a defensible localized pharmaceutical image↔label population;
- Phase66 explicit morphology/color ↔ attached-label structure: not supported;
- the same coarse morphology coding detected a known-positive historical botanical image↔description relation;
- Phase67 visible leaf/root morphology ↔ adjacent body-paragraph surface: not supported;
- Phase67 formal-channel masking did not reveal a hidden morphology signal;
- Phase68 morphology ↔ residual lexical/edit1-family selection: strongly not supported.

These results do not establish semantic absence, plant-name absence, or cipher absence.

## Direct-music program — Issue #26

The bounded direct-music program A–E17 is complete.

Accepted conclusion:

> **No tested, independently constrained direct-musical or music-cipher model provides held-out evidence that Voynich running text encodes music or readable plaintext through a musical state system.**

Useful residuals remain only after removing musical meaning. slot3×slot5 is now subsumed into the broader token-construction program.

## Historical real-cipher control lane

The Phase72 source-audit branch remains source-development work, not accepted current science. Public benchmark records did not yet supply two independent historical-practice collections with externally established message-entry boundaries suitable for a fair S1 control.

No Phase72 Voynich target score is authorized until source population and boundary semantics are frozen prospectively.

## Interpretation limits

Do not infer:

- that spaces are true linguistic word boundaries;
- that the manuscript is meaningless or lacks semantics;
- that A1 is the historical generator;
- that the manuscript uses or does not use a cipher in general;
- that any slot has a semantic meaning;
- that the occupancy graph is a cipher table;
- that #58B proved one shared graph or proved multiple grammars;
- that direct music is impossible under every conceivable encoding;
- that negative morphology tests falsify plant names or all plant-related content;
- that the manuscript is deciphered.

## Reproducibility / repository state

First-reveal provenance is preserved beyond Actions retention for Issues #55 and #58A. #58B first reveal is now also archived under `experiments/occupancy-graph-stability/first-reveal/` with raw-result SHA-256:

`45024fd1d15b2d2484ffc26657ccc8007fd6a04dc3ed1b53b243f77ba455f8a0`

Historical reproducibility debts remain documented in `research/REPRODUCIBILITY_AUDIT.md` and phase-specific reports.