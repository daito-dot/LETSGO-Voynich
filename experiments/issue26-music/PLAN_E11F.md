# Issue26E11F — fully refitted STA-family order-null audit

Status: **FROZEN BEFORE E11F EXECUTABLE / NULL REVEAL**

Parent target result: E11E at `1442cdcaa819ed2b0e24eea9c66bc51e40800eaa`.

## Motivation

E11E used the independently validated FREQ-HILL substitution solver and produced an unusual mixed result:

- pooled held-out CE `3.6860993911 bits/char`, essentially equal to the matched E11 Latin self-baseline `3.6903904874`;
- but complete-key recurrence only `1/5`;
- mean pairwise occurrence-weighted key stability only `.6219935481`;
- pooled top-five decoded-character fraction `.7746166938` versus Latin `.4932494650`;
- only one distinct exact whole-token CREMMA match length >=6 (`distin`).

Frozen classification was `LATIN-LIKE BUT KEY-UNSTABLE`.

Before increasing model flexibility, E11F tests the most direct competing explanation:

> Does the low held-out Latin 4-gram CE depend on the actual ordering of STA families, or can the same family frequencies and segment lengths obtain similarly low CE after order is destroyed and the complete substitution key is refit from scratch?

## Frozen target and solver

Reuse E11E exactly:

- official ZL3b STA1 SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`;
- 23 family order `A B C D E F G H J K L M N P Q R S T U V W X Z`;
- numerical-leaf analysis population 4,119 lines / 140,423 family events;
- five physical-leaf folds;
- frozen CREMMA model and 24-letter normalization;
- E11D-validated `FREQ-HILL` solver with no changes.

The real E11E statistics are replayed by running the same code path and must reproduce within `1e-12`:

- pooled held CE `3.6860993911494533`;
- weighted key stability `0.6219935480654878`;
- exact full-key recurrence `1`.

If replay fails, classify `E11F REPLAY FAILURE` and do not interpret nulls.

## Primary null family

Generate exactly **200 deterministic order nulls**.

For null index `n=0..199`, independently for every E11E scoring segment:

1. take that segment's exact sequence of 23 STA-family indices;
2. shuffle the indices uniformly without replacement **within that segment only**;
3. preserve the segment's exact family multiset, length, leaf, page, locus, source line, and segment identity;
4. preserve the original token-length vector and repartition the shuffled sequence into those same token lengths for diagnostics only.

Seed namespace:

`Issue26E11F:SegmentShuffle:v1:<n>:<source_line>:<segment_index>`

The null therefore preserves exactly:

- global family frequencies;
- per-segment family frequencies;
- every segment length;
- all physical-leaf/fold assignments;
- token counts and token lengths;
- the complete solver dimensionality.

It destroys only within-segment family order / local sequential structure.

No symbol may move between segments or folds.

## Full refit requirement

Every null receives the **entire E11E pipeline from scratch**:

For each of five folds:

1. construct training sequences from the shuffled 4/5 training leaves;
2. recompute the frequency seed (it should be numerically identical because unigram counts are preserved, but the implementation must not reuse the target final key);
3. run the complete frozen FREQ-HILL optimization on shuffled training 4-grams;
4. freeze that null-specific key;
5. score the shuffled held-out fold;
6. compute all five null keys' cross-fold stability.

No E11E fitted key is supplied to a null. No null is allowed less fitting freedom than the target.

## Primary statistics

For the real target and every null compute:

1. pooled held-out CE, weighted by held-out scored 4-gram count;
2. mean pairwise occurrence-weighted key stability using the same fixed global family weights as E11E;
3. exact complete-key recurrence across five folds.

Primary significance test:

- lower-tail CE p-value: `(1 + #{null_CE <= real_CE}) / 201`.

Secondary descriptive comparisons:

- null median / q05 / minimum CE;
- real minus null-median CE;
- upper-tail key-stability p-value `(1 + #{null_stability >= real_stability}) / 201`;
- null median / q95 / maximum stability;
- distribution of exact-key recurrence.

## Frozen interpretation

### `ORDER-SPECIFIC LATIN-LIKENESS RESIDUAL`
Only if all hold:

1. real lower-tail CE `p <= .01`;
2. real CE is at least `.10 bits/char` below null median;
3. real weighted key stability exceeds null median;
4. real is not formally low-diversity relative to E11E's already-frozen absolute diagnostics (no reinterpretation of token readability).

This would justify a new separately preregistered follow-up, but still would not establish plaintext because E11E keys are absolutely unstable and token readability is poor.

### `ORDER-SPECIFIC BUT KEY-UNSTABLE`
If CE gates 1 and 2 pass but stability gate 3 fails.

### `LATIN-LIKE CE EXPLAINED BY REFITTED ORDER NULLS`
If real CE does not satisfy both CE gates 1 and 2.

### `E11F REPLAY FAILURE`
If exact E11E replay fails before null interpretation.

## Boundaries

- Do not alter the number of nulls after reveal.
- Do not select favorable leaves, families, or segments.
- Do not preserve selected n-grams in nulls post hoc.
- Do not move directly to homophones, polyalphabetic keys, family-member splits, or manual semantic reading on an E11F negative.
- A positive E11F still requires an independent new prediction; it does not retroactively make E11E a decipherment.
- Keep E11F on its research branch and do not merge to main without explicit authorization.
