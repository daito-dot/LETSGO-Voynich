# Current research status

Last consolidated: 2026-08-31

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

### slot3 × slot5 morphotactic exclusion — Issue #55

Issue #55 followed a residual from the failed Sloane 351 music-cipher experiment while removing all Sloane, music, Latin and plaintext assumptions.

#55A found real cross-leaf predictive dependence between the native five-state slot3 and slot5 factors:

- equal-fold mean symmetric gain: **0.04417745 bits/token**;
- all 5 held-out folds positive;
- within-line pair-destruction p: **1/1001 ≈ 0.000999**;
- real advantage over null median: **0.041131 bits/token**.

#55B then decomposed that dependence. The result is decisive:

- full five-state gain: **0.04417745**;
- binary EMPTY/nonEMPTY gain: **0.04421504**;
- occupancy fraction: **1.00085**;
- subtype residual: **-0.00003747 bits/token**;
- subtype-residual null p: **0.26973**;
- only 2/5 residual folds positive;
- all 24 canonical nonempty slot3×slot5 combinations are syntactically admitted by the parser.

Frozen classification:

> **`DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`**

The surviving claim is structural: slot3 and slot5 behave as almost mutually exclusive token-construction channels across physical leaves. This is not evidence for a 25-cell code, Sloane 351, music, plaintext or semantic subtype correspondence.

See `experiments/slot35-dependency/REPORT_A.md` and `REPORT_B.md`.

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

1. slot3×slot5 dependence — now narrowed by #55B to binary occupancy exclusion;
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
- slot3 or slot5 has a semantic meaning;
- direct music is impossible under every conceivable encoding;
- a negative morphology test falsifies plant names or all plant-related content;
- the manuscript is deciphered.

## Active frontier

The immediate structural frontier is to determine what the newly confirmed slot3/slot5 occupancy exclusion actually represents without reusing the failed musical interpretation.

The next experiment should be plan-first and should treat slot3×slot5 as a **selected pair**, not as an unseen discovery target. Useful discriminators are:

1. compare the selected pair with the complete 12-slot occupancy graph under multiplicity-aware controls;
2. test whether the exclusion is stable across manuscript register/Currier/position rather than generated by one subset;
3. replicate the structural relation under an independent transcription or independently defined representation where possible;
4. only after structural specificity is established, ask whether the exclusion can constrain an invertible surface-transform family.

A parallel external-source lane may continue seeking real historical cipher corpora with genuine message boundaries, but no Voynich comparison should be run until the external population and boundary semantics are frozen.

## Reproducibility / repository state

Issue #55 first-reveal provenance is now preserved in the corresponding reports. The old #55 working branches diverged substantially from current main and should not be merged wholesale; the authoritative integration copies only the frozen plans, executables, reports and provenance needed for the result.

Historical reproducibility debts from earlier phases remain documented in `REPRODUCIBILITY_AUDIT.md` and phase-specific reports.
