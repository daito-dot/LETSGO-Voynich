# Issue26E11D locked-validation operational amendment

Status: **FROZEN AFTER `E11D_SOLVER_FREEZE`, BEFORE VALIDATION EXECUTABLE / REVEAL**

`PLAN_E11D.md` already froze the 12-cipher validation concept, seed namespace, folds, and pass criteria before solver development. It intentionally did not spell out three low-level deterministic operations: the exact run-rotation offset, how the phrase “least frequent letter after deterministic alphabet rotation” selects the unused letter, and the exact event budget. This amendment resolves those ambiguities **before any validation executable exists or validation result is generated**.

It does not alter the frozen solver or validation thresholds.

## Frozen event budget

For every validation cipher, use exactly **140,423 plaintext characters**, matching the reconciled E11C numerical-leaf analysis event count.

A validation construction must fail rather than silently use a smaller budget.

## Frozen normalized Latin source

Use the exact same normalized CREMMA run list as `E11D_SOLVER_FREEZE`:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- 24-letter alphabet `abcdefghiklmnopqrstuwxyz`;
- normalization `j→i`, `v→u`.

Let `R` be the resulting ordered list of normalized runs and `N=len(R)`.

## Frozen run rotation

For validation index `i=0..11`, compute:

`shift_i = seed32("Issue26E11D:ValidationRuns:v1:<i>") mod N`

using the same SHA-256-first-32-bit `seed32` convention as the project.

Rotate the run list left by `shift_i` before any target-budget extraction:

`R_i = R[shift_i:] + R[:shift_i]`.

This makes the twelve plaintext windows deterministic and non-identical without inspecting their validation results.

## Frozen unused-letter rule

Compute **global frozen CREMMA unigram counts** for all 24 normalized letters once.

Create the base rarity order:

1. ascending global frequency (rarest first);
2. lexicographic letter as tie-break.

For validation index `i`, rotate this **rarity-ranked 24-letter list** left by `i` positions and choose its first element as the unused plaintext letter.

Equivalently, validation `i` omits the letter at rarity-rank `i` for `i=0..11`.

This operationalizes the parent plan's “least frequent letter after a deterministic alphabet rotation by index” while ensuring the locked battery exercises twelve distinct unused-letter positions. It uses only the external corpus and validation index, never a fitted or decoded validation result.

## Frozen 23-letter plaintext extraction

For each rotated run list `R_i`:

1. split every run at every occurrence of the validation's unused letter;
2. discard empty segments;
3. retain remaining segments in source order;
4. accumulate characters from those segments until exactly 140,423 characters are collected;
5. truncate only the final segment if necessary.

Segments shorter than four characters may remain in the encrypted population and in key-accuracy counts, but contribute no 4-gram terms, exactly as ordinary run boundaries do.

## Frozen hidden-key construction

For validation `i`:

- plaintext positions are the 23 alphabet letters other than the unused letter, in frozen alphabet order;
- initialize NumPy `default_rng(seed32("Issue26E11D:ValidationKey:v1:<i>"))`;
- shuffle those 23 plaintext indices once;
- assign the shuffled indices to cipher-symbol positions `0..22`;
- key position `23` stores the unused plaintext index.

The solver receives only encrypted symbol streams, not this true key.

## Frozen five-fold construction

After the 140,423-character retained run/segment list has been fixed, enumerate its segments `r=0,1,...` in extraction order.

Validation `i` assigns segment `r` to held-out fold:

`fold = (r + i) mod 5`.

For each fold:

- train FREQ-HILL on the other four folds;
- freeze the resulting key;
- compute occurrence-weighted decoded-letter accuracy on held-out observed symbols using the hidden key only in the evaluation wrapper;
- compute recovered held-out 4-gram CE and true-key held-out 4-gram CE.

Validation-cipher summary metrics are arithmetic means across its five folds, exactly as required by `PLAN_E11D.md`.

## Frozen validation classification

No change to `PLAN_E11D.md`:

`E11D SOLVER VALIDATED` only if all hold on the first reveal:

1. at least 11/12 validation ciphers have mean occurrence-weighted key accuracy >=`.95`;
2. at least 11/12 have mean recovered held-out CE within `.05 bits/char` of true-key held-out CE;
3. median validation occurrence-weighted accuracy >=`.98`;
4. worst validation recovered-minus-true held-out CE <=`.15 bits/char`;
5. no validation cipher has mean occurrence-weighted accuracy <`.85`.

Additionally, any final-score implementation discrepancy >`1e-10` under `E11D_SOLVER_FREEZE` produces `VALIDATION IMPLEMENTATION FAILURE` and no scientific pass/fail inference.

After this amendment, no further validation-population, solver, seed, scoring, or threshold changes are permitted before the first validation reveal.
