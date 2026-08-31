# Phase 66C-D — illustrated image↔body categorical positive control

Status: **FROZEN BEFORE IMAGE-SIDE CONTROL CODING**

Parent control: `PLAN_C.md` / `BODY_AUDIT_C.json`.

## Why this test exists

The completed 24-entry body audit shows that genuine illustrated botanical prose often explicitly contains morphology, whereas the literal Latin binomial does not. This test asks whether the fixed image-side morphology categories used in Phase66 can recover those explicit prose properties in a known semantically related illustrated book.

This is intentionally a **categorical state-agreement test**, not a holistic visual-similarity or string-similarity test.

## Important blinding limitation

The same ChatGPT runtime has already inspected botanical prose for the 24 control species. Therefore the forthcoming image reading cannot be treated as blinded human/model annotation. The control is a detector-calibration exercise, not independent confirmatory evidence.

To limit discretionary bias:

- image coding must use only the already frozen Phase66A character/state vocabulary;
- no free-form taxon identification or "looks similar" score;
- no state may be invented outside the schema;
- `U` is mandatory when depiction is insufficient;
- no manual state changes after comparison with body coding;
- all 24 fixed species remain in the population.

## Control image source

Use the corresponding public-domain plates from Traill/FitzGibbon, *Canadian Wild Flowers* (1868) / *North American Wild Flowers* (1869). Plate reordering between editions is provenance only and does not alter the fixed 24 species.

Each illustrated species is treated as one object. Printed plate labels/known plate positions may be used only to locate the species region; they may not supply morphology.

## Primary characters

Exactly the same three Phase66A morphology characters that were eligible on the Voynich image side:

1. `leaf_composition`
2. `leaf_arrangement`
3. `leaf_margin`

Allowed states are exactly those already defined in `experiments/phase66/PLAN_A.md` and `ANNOTATION_SCHEMA_A.json`. No control-specific collapsing or new state is allowed.

## Body-side authority

Use the already sealed `BODY_AUDIT_C.json` evidence, but create a new state table only where the prose is directly mappable to a frozen Phase66 state.

A body state is `U` when prose does not explicitly provide enough information for one frozen state. Do not infer from taxon knowledge or images.

## Primary agreement statistic

For every species×character cell where both image and body state are non-U:

- agreement = 1 for exact same frozen state;
- agreement = 0 otherwise.

Primary statistic:

`A = total exact agreements / total jointly observed cells`.

Also report per-character A and coverage.

## Exact permutation null

Hold image states fixed. Permute the complete body-state triplets among the 24 species, preserving each prose description's three-character missingness/state pattern.

For each permutation recompute A over jointly observed cells.

Because 24! is intractable, use exactly 100,000 Monte Carlo permutations with NumPy `PCG64` seed `6603001`, plus the identity assignment as the observed configuration. Report the one-sided plus-one p-value:

`p = (1 + count(A_perm >= A_obs)) / (100000 + 1)`.

This null asks whether the correct image↔description pairing produces more exact categorical agreement than arbitrary reassignment of descriptions.

## Frozen practical-effect gate

This is a positive-control detector check, not a Voynich claim. The control is considered operationally successful if all are true:

1. at least 12 jointly observed species×character cells exist;
2. `A >= 0.60`;
3. Monte Carlo one-sided `p <= 0.05`.

The 0.60 gate is deliberately well above chance for the multistate schema but does not demand perfect historical illustration fidelity.

## Name-only negative control

The literal Latin binomials have no directly mapped primary body states under the sealed C1 rule (`0/24`). Therefore no analogous state-agreement statistic is defined for names. This absence is itself the negative-control result and must not be converted into states through Latin etymology.

## Interpretation

If the image↔body control passes while Latin-name state availability remains zero, then Phase65B/66B short-label string-similarity failures cannot be treated as evidence that an illustrated botanical document would lack morphology-linked semantics. They would specifically constrain simple surface-form coupling of short labels.

Failure of this control would instead show that the historical illustrations / fixed Phase66 schema / current coding process are too weak for the intended categorical detector.
