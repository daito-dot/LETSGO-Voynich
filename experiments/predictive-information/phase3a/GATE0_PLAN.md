# Issue #104 / Issue #88 Phase 3A — Currier A/B Gate 0

Date: 2026-09-06
Status: **FROZEN BEFORE ANY PHASE-3A PREDICTIVE SCORE**

## Purpose

Before testing Currier A↔B mechanism transport, establish that the stratum labels and target folds are externally/structurally defined and usable without consulting any predictive result.

## Authority

The sole Phase-3A stratum authority is the frozen ZL3b source page header. The IVTFF page header field `$L` is read literally:

- `$L=A` -> Currier A;
- `$L=B` -> Currier B;
- missing/other `$L` -> UNKNOWN/OTHER for this phase.

Adjacent source comments of the form `Currier's language A/B` are a consistency check, not an alternate classifier.

Corrected causal order remains `experiments/predictive-information/source_order_authority.py`.

No hand (`$H`), illustration/section (`$I`), Currier hand, scribe, image, semantic or proposed plaintext metadata is available to Phase 3A selection.

## Required score-free audit

Report:

1. exact `$L` distribution over source page headers;
2. all source-comment `$L` consistency checks and any mismatch;
3. parsed item, visible-token and parser-accepted-token counts by label;
4. numeric physical leaves that are A-only, B-only, mixed A/B, or unknown/other;
5. accepted-token/item/leaf counts for A and B in each frozen physical-leaf fold after exclusions;
6. corrected source-order verification;
7. frozen source/fold hashes.

## Exclusions frozen before scoring

- numeric physical leaves containing both A and B parsed documents are excluded entirely from A↔B transport;
- unknown/other-labelled documents do not enter A↔B scoring;
- all excluded populations remain reported.

## Gate rule

PASS only if:

- every parsed document resolves to one source page header;
- every available `Currier's language A/B` comment agrees with `$L`;
- corrected numeric paragraph and source page/panel order verify;
- every A target fold and every B target fold retains at least one parser-accepted token after the frozen mixed-leaf/unknown exclusions;
- no predictive code length or target surface statistic is computed.

If any target fold is empty, STOP and freeze a deterministic alternative fold plan before building a scorer.

If the gate passes, the next commit may implement exactly the transport model frozen in Issue #104. Gate outputs may determine only whether that already-frozen scorer is executable; they may not alter H/tau/edit relation/pool/grid/decision rules.