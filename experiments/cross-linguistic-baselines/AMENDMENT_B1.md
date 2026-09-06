# Issue #84 Phase B — prereveal interface amendment B1

Status: **FROZEN BEFORE ANY PHASE-B CANDIDATE HAS BEEN SCORED**

Parent authorities:
- `PLAN_B.md` at `b991b948f8bb4d5041ed2e6d348eef4d91feca84`
- notation amendment `AMENDMENT_B0.md`

## Correction

The first implementation of `phase84b.py` contained an implementation-only preflight assertion that expected `6 × 3 × 26 = 468` concrete entries in Naibbe's published `placeholder_to_glyph` CSV mapping.

The pinned published CSV and the already-frozen Phase64B adapter show that only the **23 effective letters** `a…z` excluding `j`, `k`, `w` have concrete table cells. The correct concrete mapping size is therefore:

`len(TABLES) × len(STATES) × len(EFFECTIVE_LETTERS) = 6 × 3 × 23 = 414`.

The executable shall replace the literal `6 * 3 * 26` assertion with the exact expression above, using the already-frozen `phase64b_naibbe.EFFECTIVE_LETTERS` definition.

This is an external-interface compatibility correction only. It changes no source corpus, candidate family, parameter, seed, generated ciphertext, statistic, target interval, candidate center, decision rule, surface/R1 policy, or interpretation rule.

No Phase-B candidate score has been produced or inspected before this amendment. The preflight workflow is expressly score-free.
