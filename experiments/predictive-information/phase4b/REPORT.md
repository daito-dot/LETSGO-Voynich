# Issue #115 Phase 4B — independent IT2a visible-space replication

Date: 2026-09-06
Status: **COMPLETE — FULL CROSS-TRANSCRIPTION REPLICATION**

## Result

The visible-space production-boundary result from ZL3b reproduces under the independent Takahashi/IT2a reading with no retuning.

Frozen IT2a class:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

Frozen cross-transcription class:

> **VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a**

## Why this is a stronger result than Phase 4A alone

Phase 4A could still have been a property of one transcription lineage: exact glyph reading, uncertain-character decisions, or the ZL-specific rendering could in principle have created an artificial reset at spaces.

Phase 4B repeated the same raw-shape test on a separately produced Takahashi reading represented as EvaT. The source, event population and model were independently reconstructed. No ZL3b fitted model was transferred and no threshold or mapping was changed in response to the ZL3b result.

The same three signs survive in all five physical-leaf folds:

1. real spaces prefer resetting short raw-glyph context relative to deterministic internal cuts;
2. moving the real reset one atom left makes coding worse;
3. moving it one atom right makes coding worse.

## P1 — reset contrast

IT2a pooled held-out values:

- REAL_SPACE reset advantage `+2.55421 bits/event`
- MID_TOKEN reset advantage `-5.53840 bits/event`
- D_RESET `+8.09261 bits/event`
- positive `5/5` folds.

The sign decomposition reproduces the ZL3b pattern: a reset helps at real spaces and strongly hurts inside a token.

## P2 — exact cut

Observed space versus one-atom-left shift:

- `-7.96827 bits/event`
- observed wins `5/5` folds.

Observed space versus one-atom-right shift:

- `-5.27945 bits/event`
- observed wins `5/5` folds.

Thus the phenomenon is not merely a broad boundary region. The observed cut is locally sharply privileged in both readings.

## Cross-transcription comparison

Magnitude agreement was not a pass criterion, but the independently obtained effects are strikingly close:

| metric | ZL3b | IT2a |
|---|---:|---:|
| P1 D_RESET | +8.81191 | +8.09261 |
| P2 observed-left | -8.50180 | -7.96827 |
| P2 observed-right | -5.47660 | -5.27945 |

IT2a magnitudes are about 92%, 94% and 96% of ZL3b respectively. This similarity is descriptive and was not used to promote the result.

## Scientific consequence

The most defensible current statement is now stronger than “spaces were a convenient tokenization”:

> **Literal certain spaces mark a reproducible, transcription-lineage-robust discontinuity in the local construction process. Within a visible unit, raw glyph context carries strongly; at a visible space, resetting that context is strongly preferred, and the reset is tightly localized to the observed cut.**

This makes it reasonable for the predictive-information program to continue treating the visible-space-delimited unit as a genuine **construction/production unit**, even while refusing to call it a natural-language word.

This result also fits the broader empirical picture:

- token interiors follow a compact construction grammar;
- short cross-token edit-near recency acts between these bounded units;
- slower paragraph-history effects exist above them;
- therefore at least three distinct structural scales are now experimentally separated: **inside-unit construction, between-unit local recurrence, and paragraph-scale inventory/history**.

The boundary result matters because it prevents those scales from being dismissed as artifacts of an arbitrary tokenizer.

## What it does not tell us

The bounded units may still be any of several kinds:

- natural-language words or morpheme-like groups;
- cipher code groups;
- formal notation units;
- steps emitted by a generative procedure;
- another historically specific unit not represented by modern linguistic categories.

Phase 4B does not distinguish those possibilities. In particular, it does not prove semantics, natural language, encryption, artificial generation or meaninglessness.

## Program consequence

The original Phase-4 construct-validity threat is now substantially closed for the tested EVA/IVTFF lineages. The next program step should not be arbitrary re-tokenization search.

The higher-value question is now:

> **After accounting for the validated bounded unit, compact token-internal grammar, LOCAL40 recency and paragraph inventory, how much held-out predictive information remains, and is any remaining signal explainable by additional observable structure before latent-state modeling?**

Any latent-state phase should still require a prospectively demonstrated residual beyond the currently validated observable mechanisms.

Exact run/artifact/result authority is recorded in `IT2A_FIRST_REVEAL_PROVENANCE.md`.

Refs #66, #88, #112, #115, #116, #117.
