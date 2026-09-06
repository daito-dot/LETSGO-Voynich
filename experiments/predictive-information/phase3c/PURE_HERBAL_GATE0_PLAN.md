# Issue #109 / Issue #88 Phase 3C — pure-Herbal Gate 0

Date: 2026-09-06
Status: **FROZEN BEFORE ANY PHASE-3C PREDICTIVE SCORE**
Entry authority: Issue #107 / Phase 3B score-free metadata audit

## Purpose

Construct a domain-matched Currier A/B population without altering token distances or paragraph histories.

Phase 3B identified Herbal (`I=H`) as the only illustration level with substantial A/B support in all five frozen folds. Phase 3C therefore tests only whether a **pure Herbal leaf** population can be formed prospectively. No prediction is computed in this Gate.

## Conservative pure-leaf rule

A numeric physical leaf is eligible for `A_HERBAL` or `B_HERBAL` iff **every visible parsed-P token row on that numeric leaf** satisfies both:

1. frozen Phase-3A Currier authority is exactly the same label L (`A` or `B`);
2. resolved Phase-3B illustration value is exactly `I=H`.

Thus eligible leaves contain:

- no opposite Currier label;
- no UNKNOWN/OTHER Currier token row;
- no non-Herbal illustration token row;
- no unresolved illustration row.

This rule is intentionally stricter than filtering only scored/accepted tokens. The full visible leaf is retained or excluded as a unit so LOCAL40 token distances and previous-paragraph histories are not shortened by deleting intervening non-Herbal material.

## Required score-free outputs

For A_HERBAL and B_HERBAL report:

- eligible numeric leaves;
- items;
- visible tokens;
- parser-accepted tokens;
- accepted-token support in each original physical-leaf fold;
- excluded leaves by reason, including observed Currier and I level sets.

Hard invariants:

- frozen ZL3b source hash;
- corrected source order valid;
- Phase-3B metadata mapping remains exact (`32,570` visible / `25,071` accepted);
- Phase-3B Gate result remains `NO ADEQUATELY CROSSED OBSERVABLE FACTOR`;
- Herbal remains the sole cross-Currier usable I level from the prior support-only audit.

## Gate rule

PASS iff:

- at least one eligible A_HERBAL and B_HERBAL leaf exists;
- each of the original five frozen folds has >0 parser-accepted target tokens for A_HERBAL;
- each of the five folds has >0 accepted target tokens for B_HERBAL;
- all source-order/metadata mapping invariants pass;
- no predictive code length/model fit is computed.

If any target fold is empty, STOP. Do not regroup folds after seeing scores because no scores are permitted in Gate 0.

## Consequence if PASS

A later, separately committed scorer may repeat exactly the Phase-3A target-support V2 + LOCAL40 + PREV_PARAS transport family on these pure-Herbal leaves only, under Issue #109's already-frozen decision rules.

No hand conditioning, H/tau/window search, history-pool change, token deletion inside eligible leaves, or latent state is licensed.