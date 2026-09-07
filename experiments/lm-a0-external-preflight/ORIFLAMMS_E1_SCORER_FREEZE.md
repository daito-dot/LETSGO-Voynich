# ORIFLAMMS E1 scorer freeze

Date: 2026-09-07
Parent: Issue #180 / Issue #172
State: **FROZEN BEFORE E1 EFFECT REVEAL**

## Frozen inputs

- E1 scientific/selection plan: `research/LM_A0_EXTERNAL_E1_ORIFLAMMS_SELECTION_PLAN_20260907.md`
- frozen roster commit: `f370ed68982df9bfc56e68b30b519f247d8cd66e`
- frozen roster Git blob: `9a465e23e1efa78c9de504650f699e844a1daf5f`
- roster size: 23 manuscripts
- ORIFLAMMS authority commit: `93de4af4a470aea3f3b23c2e8bafcfa2161c5438`
- word authority SHA-256: `d1ff8102e8c81f36d45a31143f9294cf5c061d55d879aed44244c858f65018e4`

## Post-roster structure audit

Structure-only workflow run `34121652545` inspected the fixed 23 manuscripts after roster freeze and computed no effect statistic.

It found:

- 484 physical `<lb>` milestones;
- 90 `lb break="no"` boundaries;
- all 90 nonbreaking boundaries occur inside words represented as `seg/lb/seg`;
- ordinary word forms include literal text and one or more `choice` children;
- valid `choice` elements can occur under formatting wrappers but remain descendants of a corpus `w` token.

This permits the preregistered E0-style compatibility rule without text-driven inference: a word spanning `lb break="no"` is excluded and both physical lines adjacent to that split are excluded.

## Frozen scorer

Scorer: `experiments/lm-a0-external-preflight/oriflamms_e1_scorer.py`

Scorer freeze commit: `5298c0ea5983992867d544906a719bef7c7eaf49`

Frozen representation decisions:

1. use only corpus body `<p>` content;
2. ordinary `<lb>` defines a physical line transition;
3. a word containing internal `<lb>` is excluded, and both adjacent physical lines are excluded;
4. a word containing `<del>` is excluded as editorially ambiguous;
5. every valid `choice` in a word is rendered with `abbr` for the surface form and `expan` for the expanded form;
6. words with unresolved/malformed choices, `expan=ERROR`, render failure, or empty normalized forms are excluded and counted;
7. normalization is Unicode NFC + casefold + trimming of leading/trailing non-letter/non-mark characters only;
8. no `u/v`, `i/j`, spelling, lemma, morphology or language normalization is permitted;
9. primary strata are manuscript × normalized expanded lexical form;
10. the null is exact within-stratum hypergeometric exchangeability;
11. FINAL1 is primary and FINAL2 is the frozen sensitivity;
12. manuscript-level sign replication is evaluated exactly as specified in the E1 plan.

No manuscript may be added or removed after effect reveal.

## Target-free preflight

Synthetic-only workflow run `34121851428` completed successfully against the frozen scorer. The synthetic fixture exercises:

- physical line construction;
- internal `break="no"` exclusion;
- abbreviation/expansion branch rendering;
- mixed abbreviated/unabbreviated lexical strata;
- exact hypergeometric scoring.

Result: `SYNTHETIC_E1_PREFLIGHT_OK`.

No ORIFLAMMS FINAL1/FINAL2 effect was computed by the synthetic workflow.

## Reveal license

The next and only licensed operation in E1 is a single execution of the frozen scorer on the pinned ORIFLAMMS authority and frozen 23-manuscript roster. Any runtime failure before result emission may be repaired only if the repair is transport/parser-only and leaves the scientific population, representation, statistic and thresholds unchanged, with provenance recorded before rerun.

After a successful reveal, the E1 classification is determined mechanically by the already-frozen gate. A failed or opposite-direction result may not be rescued by changing the roster, positional window, normalization, abbreviation subtype, script subset or null.
