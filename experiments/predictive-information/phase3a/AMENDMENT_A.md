# Phase 3A Amendment A — resolve missing `$L` from same-source Currier comment

Date: 2026-09-06
Status: **FROZEN AFTER SCORE-FREE GATE-0 ATTEMPT AND BEFORE ANY PHASE-3A PREDICTIVE SCORE**
Applies to: `GATE0_PLAN.md`, Issue #104

## Trigger

The first score-free Gate-0 run (`34021103420`, head `48097faeb249c1ab761100f88653fe594b3b4be1`) computed no predictive code length and no surface target statistic.

It found exactly one metadata-consistency exception:

- `f57v` page header has no `$L` field;
- the adjacent comment in the same frozen ZL3b source says `Currier's language B, hand 2 (???)`;
- all 196 other checked A/B comment/header pairs agree;
- A and B retain nonzero parser-accepted support in all five frozen physical-leaf folds;
- no mixed A/B numeric physical leaf was found under the original header-only mapping.

The first audit JSON SHA-256 printed before the post-audit gate assertion was:

`5d5416fb0e87ee8fcdf7b2f3c1be3c88b0602da85de923382905d27efd8fc114`

No predictive scorer exists in this branch at the time of this amendment.

## Amended metadata authority

For Phase 3A Currier labels only:

1. if page-header `$L` is exactly `A` or `B`, that value is authoritative;
2. if and only if `$L` is **missing**, and the comments immediately adjacent to that same page header contain exactly one unambiguous `Currier's language A` or `Currier's language B` label, use that same-source comment as a fallback;
3. if `$L` is present with any value other than A/B, do not replace it from comments;
4. if `$L=A/B` conflicts with an adjacent Currier comment, FAIL;
5. if a missing `$L` page has conflicting/multiple A/B comments, FAIL;
6. otherwise label the page `UNKNOWN_OTHER` and exclude it from A↔B scoring.

This fallback is not generalized to hand, section, scribe or any other metadata field.

## Why this is admissible

The trigger is a source-metadata omission discovered by a score-free audit. The fallback label comes from the same frozen transcription source and predates this research program. No held-out likelihood, S1/S2/H62/R1, Issue #84 target or semantic outcome was consulted.

The amendment therefore repairs metadata transport/authority, not model fit.

## Stopping rule

This is the only Phase-3A Currier-label fallback rule. No further manual page-by-page relabeling is allowed after the next Gate-0 run.

If the amended Gate 0 still finds a conflict or an empty A/B target fold, Phase-3A predictive scoring remains blocked.