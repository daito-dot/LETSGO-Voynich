# Current research status

Last consolidated: 2026-09-01

This file controls the current accepted high-level interpretation. Phase-specific frozen plans, first-reveal results and reports remain authoritative for exact methods and numbers.

## Bottom line

The Voynich Manuscript is **not deciphered**.

The project has nevertheless established several reproducible structural constraints and has eliminated a large number of attractive semantic, historical-cipher and direct-music interpretations under controlled tests.

The current research objective is constructive: preserve falsified models as boundaries, retain any reusable mathematical structure they expose, and use those constraints to narrow the space of viable transformations or generation mechanisms.

## Current strongest structural state

### Paragraph-entry and local recurrence

The Phase62–64 program established that the frozen A1/A1-R1 mechanism is the leading tested model for the manuscript's short-range near-family recurrence geometry. It received sealed prospective support on H62-P1, survived training-only vocabulary restriction and transferred to an independent EvaT reading without retuning.

This does **not** identify A1 as the historical production algorithm.

Later constructive work changed the interpretation of the recurrence evidence. Phase69 and Phase70 demonstrated that strong A1-like local recurrence can coexist with exactly recoverable meaningful plaintext. Therefore:

> **Short-range recurrence is a formal surface constraint, not evidence by itself that the text lacks semantics or plaintext.**

The harder discriminator is the signed paragraph-entry effect S1. The tested reversible meaningful-text constructions reproduce much of S2/S3/H62 but remain weak on S1.

### Paragraph-entry boundary mechanism

Phase71 tested an independently motivated Alberti initial-alignment signal and paragraph reset. The paragraph-reset arm projected in the opposite S1 direction from Voynich and failed in all five folds.

Accepted conclusion:

> **The tested Alberti message-initial signal/reset mechanism is not sufficient to explain the Voynich paragraph-entry direction.**

This is one bounded historical mechanism failure, not a rejection of all ciphers or all boundary mechanisms.

### Slot-occupancy grammar — Issues #55 and #58A

Issue #55 followed a residual from the failed Sloane 351 music-cipher experiment while removing all Sloane, music, Latin and plaintext assumptions.

#55A found real cross-leaf predictive dependence between the native five-state slot3 and slot5 factors. #55B then showed that essentially all of that signal reduces to the binary fact that the two slots are not occupied together:

- full five-state gain: **0.04417745 bits/token**;
- binary EMPTY/nonEMPTY gain: **0.04421504**;
- subtype residual: **-0.00003747 bits/token**;
- subtype-residual null p: **0.26973**;
- only 3 pooled tokens co-occupy slot3 and slot5;
- the parser admits all canonical nonempty slot3×slot5 subtype combinations.

#55B frozen classification:

> **`DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`**

Issue #58A then audited the complete `C(12,2)=66` binary slot-occupancy graph under one frozen five-fold held-out statistic and one 1,000-null global maxT family.

First-reveal result:

- **22/66** edges survive `p_maxT <= .01` with all five held-out gains positive;
- selected `(3,5)` ranks only **22/66** by mean held-out gain;
- `(3,5)` still has mean gain **0.04421504 bits/token**, all five folds positive, `p_maxT = 1/1001`, and phi **-0.20648**;
- after conditioning on occupancy of the other ten slots (`K_other`), `(3,5)` remains positive but is no longer family-wise exceptional: conditional `p_maxT = 0.55644`;
- all **66/66** canonical two-slot co-occupancies are parser-admissible;
- the strongest relations are concentrated in a signed network, especially slots 6–11: some pairs strongly co-occur and others strongly exclude one another;
- strongest primary edge `(8,10)` has mean held-out gain **0.76767 bits/token**, phi **+0.92378**, and remains family-wise significant after `K_other` conditioning.

#58A frozen classification:

> **`BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`**

The correct interpretation is not that #55 was false. slot3 and slot5 really are almost mutually exclusive in this representation. What is rejected is privileging that pair as a unique key: it is one edge inside a substantially stronger signed token-construction grammar.

See `experiments/slot35-dependency/REPORT_A.md`, `REPORT_B.md`, and `experiments/occupancy-graph/REPORT_A.md`.

## Content-relation program

The Phase65–68 object-local content program made several externally grounded image↔text tests possible, then returned null results under frozen representations.

Current accepted content state:

- Phase65A established a defensible localized pharmaceutical image↔label population; anchor readiness was a mapping result, not content detection.
- Phase66 explicit morphology/color ↔ attached-label structure: not supported.
- the same coarse morphology coding recovered a known-positive historical botanical image↔description relation, so the detector is not trivially incapable of finding any real relation.
- Phase67 visible leaf/root morphology ↔ adjacent body-paragraph surface: not supported.
- Phase67 formal-channel masking did not reveal a hidden morphology signal.
- Phase68 morphology ↔ residual lexical/edit1-family selection: strongly not supported.

The current evidence therefore does not support a simple surface-correlated mapping from visible plant morphology to nearby Voynich label/body form in the tested object-local populations.

This does not establish semantic absence, plant-name absence or cipher absence.

## Direct-music program — Issue #26

The bounded direct-music program A–E17 is complete.

Tested families included finite musical states, Ptolemaic/music-cosmology relations, Guidonian six-state interpretations, Nicholas Philip 1436, Sloane MS 351, León substitution, Porta, Öttingen, Kircher, Bacon biliteral and Friderici-style mechanisms.

Accepted bounded conclusion:

> **No tested, independently constrained direct-musical or music-cipher model provides held-out evidence that Voynich running text encodes music or readable plaintext through a musical state system.**

Three residuals remain useful outside a musical interpretation:

1. slot3×slot5 dependence — now subsumed into the broader #58A occupancy grammar;
2. STA-family order effect — real order contains exploitable sequence structure, but genuine Latin order is not specific;
3. a six-state morphology/dependency factor — static structure survives, literal Guidonian interpretation does not.

See `experiments/issue26-music/RESEARCH_SUMMARY.md`.

## Historical real-cipher control lane

A Phase72 source-audit branch exists for real historical ciphertext controls. It is **not yet integrated into main and is not current accepted science**.

Its source-only work found that the open benchmark contains useful real-cipher material, but the available public page records do not provide two independent historical-practice collections with externally established message-entry boundaries. No Phase72 Voynich S1/S2/S3/H62 scientific score has been authorized.

Until that branch is reconciled against current main, treat it as source-development work rather than accepted result state.

## Current interpretation limits

Do not infer any of the following:

- the manuscript is meaningless;
- the manuscript has no semantic content;
- A1 is the historical generator;
- the manuscript uses or does not use a cipher in general;
- any slot has a semantic meaning;
- the signed occupancy graph is itself a cipher table;
- direct music is impossible under every conceivable encoding;
- a negative morphology test falsifies plant names or all plant-related content;
- the manuscript is deciphered.

## Active frontier

Issue #58A moves the structural frontier from one selected edge to the **complete signed occupancy grammar**.

The next plan-first phase must test whether that graph is stable across externally defined manuscript strata rather than being an aggregate mixture. In particular:

1. freeze register/Currier/section metadata and token-position strata before target scoring;
2. test graph-level stability / interaction rather than chasing individual #58A top edges post hoc;
3. preserve physical-leaf separation and multiplicity-aware inference;
4. independently test whether the graph survives a representation/transcription change only when that mapping can be fixed without using #58A outcomes;
5. only after structural stability is established ask whether the graph can constrain an invertible surface-transform or decoding family.

The umbrella Issue #58 required register/Currier/token-position tests, but #58A did not preregister their exact definitions before its first reveal. They therefore cannot be retrofitted into #58A as confirmatory science; they belong to a separately frozen #58B.

A parallel external-source lane may continue seeking real historical cipher corpora with genuine message boundaries, but no Voynich comparison should be run until the external population and boundary semantics are frozen.

## Reproducibility / repository state

Issue #55 first-reveal provenance and Issue #58A first-reveal provenance are preserved beyond Actions artifact retention. #58A stores the exact raw-result hash and a deterministic gzip archive under `experiments/occupancy-graph/first-reveal/`.

Historical reproducibility debts from earlier phases remain documented in `REPRODUCIBILITY_AUDIT.md` and phase-specific reports.
