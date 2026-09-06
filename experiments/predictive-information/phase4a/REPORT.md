# Issue #112 Phase 4A — visible-space production-boundary test

Date: 2026-09-06
Status: **ZL3b FIRST REVEAL COMPLETE**

## Result

Frozen classification:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

Under the prospectively frozen raw-EVA second-order model, literal certain spaces behave very differently from deterministic within-token pseudo-boundaries on unseen physical leaves, and the exact observed cut is substantially better than moving the reset one atom left or right.

This validates the visible-space unit as a strong statistical construction/reset unit for the current predictive-information program. It does **not** establish that it is a natural-language word.

## Design

The experiment deliberately avoided the 12-slot parser when defining boundary events.

Gate 0 froze:

- exact ZL3b / IVTFF Eva-2 source;
- literal `.` certain spaces only;
- raw Basic-EVA shape atoms with fixed longest-match connected composites;
- complete exclusion of locally uncertain/exceptional transcription rather than repair;
- one deterministic MID_TOKEN cut at `floor(n_atoms/2)`;
- original five physical-leaf folds;
- exact event identities before any likelihood was computed.

The support Gate passed with:

- REAL_SPACE `21,363`
- MID_TOKEN `21,313`
- P2 REAL_SPACE `18,696`

all nonzero by thousands in each held-out fold.

The first-reveal model was then fixed to a single second-order atom model with token-start BOS context, additive alpha `0.5`, training-fold atom vocabulary + OOV, no STOP probability and no model selection.

## P1 — does a real space act like a reset?

For the first two atoms right of each candidate cut, define:

`A = bits(CARRY left context) - bits(RESET to BOS)`.

Positive A means resetting predicts the right side better than carrying the literal two-atom left context.

Pooled held-out results:

- REAL_SPACE mean A: **`+2.73865 bits/event`**
- MID_TOKEN mean A: **`-6.07325 bits/event`**
- contrast `D_RESET`: **`+8.81191 bits/event`**

By fold:

| Fold | REAL A | MID A | D_RESET |
|---:|---:|---:|---:|
| 0 | +2.71820 | -5.83794 | **+8.55614** |
| 1 | +2.69120 | -5.76732 | **+8.45852** |
| 2 | +2.77800 | -6.19696 | **+8.97496** |
| 3 | +2.99910 | -6.04853 | **+9.04763** |
| 4 | +2.47075 | -6.47829 | **+8.94904** |

Frozen rule required pooled `D_RESET > 0` and positive in at least 4/5 folds.

Result: **5/5 — PASS**.

The sign is informative in both arms, not only in the contrast. At real spaces the model prefers a reset; at deterministic internal cuts it strongly prefers carrying the within-token context.

## P2 — is the exact observed cut locally privileged?

For each stricter REAL_SPACE event, the same adjacent-token atom sequence was coded under three candidate cuts:

- observed `L|R`;
- one atom left;
- one atom right.

No STOP probability was used, so every candidate codes the same atoms exactly once and differs only in the reset position.

### One atom left

Observed minus shifted code length:

- pooled **`-8.50180 bits/event`**
- fold range `-8.75338` to `-8.29801`
- observed lower in **5/5 folds**.

### One atom right

Observed minus shifted code length:

- pooled **`-5.47660 bits/event`**
- fold range `-5.83150` to `-5.06124`
- observed lower in **5/5 folds**.

Both frozen P2 sides pass.

## Replication inside the primary corpus

The effect is not concentrated in a single physical-leaf partition. All three primary signs replicate in every outer fold:

- P1 real-vs-mid reset contrast: 5/5;
- P2 versus left shift: 5/5;
- P2 versus right shift: 5/5.

Held-out OOV is negligible, with P2 atom OOV fractions at or below `0.000126` in every fold and zero in two folds.

## Currier diagnostic

Without conditioning or retuning the model, the same direction appears in both Currier regimes:

| Diagnostic | Currier A | Currier B |
|---|---:|---:|
| P1 D_RESET | +8.01298 | +9.15433 |
| P2 observed-left | -7.67176 | -8.84943 |
| P2 observed-right | -4.61678 | -5.80593 |

This is non-authoritative but useful: the visible-space reset phenomenon is not obviously a Currier-B-only artifact.

## What changed scientifically

Before Phase 4A, all predictive-information work used the visible-space-delimited unit while explicitly withholding the claim that the space was the true production boundary.

That threat to construct validity is now substantially reduced for ZL3b.

The data support a sharper statement:

> A literal certain space is a strong, reproducible discontinuity in the raw transcription-shape construction process. The short context that predicts atoms inside a visible unit should be reset at the manuscript space, and the reset is tightly localized to the observed cut.

This makes the earlier token-level results easier to interpret as properties of genuine construction units rather than artifacts of an arbitrary editorial split.

It also makes the working picture suggested before this test more plausible: a visible unit may correspond to one bounded output/construction episode. That remains an interpretation, not an identified historical mechanism.

## What is still not established

This result does not imply that the units are:

- words of a natural language;
- semantic concepts;
- syllables;
- cipher code groups;
- independent generative draws;
- the intended units of the manuscript's author.

A natural-language word boundary, a cipher-group boundary, a formal-notation boundary and an artificial generator boundary could all create a comparable statistical reset.

No plaintext, meaning, language, cipher identity, author or historical mechanism has been recovered.

## Next falsification step

The ZL3b class is valid, but a strong manuscript-level claim should not rest on one transcription lineage. The predeclared next step is to freeze an independent IT2a/Takahashi raw-atom mapping and repeat **the same** event logic, second-order model, alpha, folds, P1/P2 metrics and classification without changing thresholds in response to this result.

If IT2a reproduces the reset and exact-cut effects, visible space can be treated as a transcription-robust production boundary for subsequent predictive work. If it does not, the discrepancy becomes a transcription/representation problem that must be resolved before stronger interpretation.

Exact provenance: `FIRST_REVEAL_PROVENANCE.md`.

Refs #88, #112, #113, #114.
