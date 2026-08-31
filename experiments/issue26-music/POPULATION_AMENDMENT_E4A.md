# Issue #26E4A — pre-executable population clarification

Status: **FROZEN BEFORE E4 EXECUTABLE / SCIENTIFIC REVEAL**

This amendment corrects one wording error in `PLAN_E4.md` discovered while auditing the already-committed E/E2/E3 implementation before writing the E4 executable.

## What the first PLAN_E4 wording said

Section 4 described the population as if only individual paragraphs satisfying the `>=3 lines` and `line1/line3 >=5 visible tokens` rule were counted, and Section 5 used the shorthand “all eligible” ZL token types/occurrences.

## What the existing frozen E/E2/E3 implementation actually does

`issue26e_core.py::physical_leaf_folds()` uses that paragraph rule only to determine the **physical-leaf universe**. Once a physical leaf is admitted to the universe, `count_matrix()` and the E2/E3 training-type loops count **all running-text (`P`) paragraphs on that admitted leaf**, including paragraphs that would not independently satisfy the leaf-admission rule.

E3’s exact E2-C replay constants therefore refer to this leaf-level population boundary.

## Correct E4 rule

E4 must preserve the existing population exactly:

1. parse running-text (`P`) paragraphs;
2. determine admitted physical leaves from paragraphs satisfying the existing `>=3 lines`, `line1 >=5 tokens`, `line3 >=5 tokens` criterion;
3. form the same five physical-leaf folds / their union;
4. after a leaf is admitted, include **all running-text paragraphs and normalized visible tokens on that leaf** in type fitting, count matrices, parse-coverage denominators and held-out scoring.

For ZL topology discovery, “all eligible ZL token types/occurrences” means all parsed types/occurrences on the **union of admitted ZL physical leaves**, not only tokens inside the qualifying paragraph that caused a leaf to be admitted.

For IT2a evaluation, use the exact hard-frozen E2/E3 leaf memberships and the same all-running-paragraphs-on-admitted-leaf behavior.

## Why this is not an outcome-driven change

This clarification was made:

- before `phaseE4_nonmusic_mechanism.py` existed;
- before any E4 generic topology was fit;
- before any E4 IT2a comparison was calculated;
- solely to make E4 reproduce the already frozen E2/E3 population and replay gate.

This amendment supersedes only the conflicting population wording in Sections 4–5 of `PLAN_E4.md`. All other frozen E4 rules remain unchanged.
