# Issue #55A — hypothesis-neutral slot3×slot5 dependency audit

Status: **PREREGISTERED — NO #55 TARGET REVEAL YET**

## Origin of the question

E10 tested a historical Sloane 351 5×5 cipher and obtained `NO READABLE SLOANE PLAINTEXT`. The decoded output was collapse-dominated and far from medieval Latin. That historical interpretation is closed.

One numerical observation was parked before the music-cipher program ended: the training-only Sloane fit selected the same complete slot3×slot5 axis/permutation key in 4/5 physical-leaf folds.

Issue #55 removes the historical cipher completely and asks only:

> Do the native five-state slot3 and five-state slot5 factors exhibit a manuscript-internal association that transfers across physical leaves beyond line-local marginal frequencies?

No Sloane table, music model, Latin language model, plaintext decoder, `con` abbreviation, or music-derived ordering is used anywhere in this audit.

## Frozen representation

Reuse the existing validated Zattera-style slot parser and the same frozen ZL3b transcription/blob already used in the parent experiments.

Primary parser policy: `min`.
`max` is a sensitivity only and cannot promote a primary failure.

For every successfully parsed visible token in the numerical physical-leaf universe used by `physical_leaf_folds`:

- slot3 state is one of `EMPTY,t,k,p,f`;
- slot5 state is one of `EMPTY,cth,ckh,cph,cfh`.

Encode both in the exact state order above. Do not reorder states by frequency or by any observed association.

Every parsed token contributes exactly one `(slot3, slot5)` pair.

## Physical-leaf cross-fitting

Use the existing five deterministic physical-leaf folds.

For each fold:

1. estimate all marginal and conditional probabilities from the other four folds only;
2. freeze them;
3. score the untouched held-out fold.

No parameter is selected on held-out data.

## Primary statistic — symmetric held-out predictive information gain

Let `S3` and `S5` be the two five-state factors.

From training counts estimate with Jeffreys smoothing `alpha=0.5`:

- `P(S5)` and `P(S5|S3)`;
- `P(S3)` and `P(S3|S5)`.

On the held-out fold compute base-2 log-loss improvements:

`G5 = CE_held[P(S5)] - CE_held[P(S5|S3)]`

`G3 = CE_held[P(S3)] - CE_held[P(S3|S5)]`

and

`Gsym = (G3 + G5) / 2` bits per parsed token.

`Gsym > 0` means that a slot3↔slot5 relation learned on other physical leaves improves prediction on unseen leaves in both directions on average.

Primary observed statistic:

- equal-weight mean `Gsym` across the five physical-leaf folds.

Also record occurrence-weighted pooled gain, `G3`, `G5`, and all fold values as diagnostics.

## Primary null — within-line pair destruction

Generate exactly **1,000 deterministic null populations**.

For every physical line independently:

1. keep the complete ordered slot3 sequence fixed;
2. take the slot5 states from the successfully parsed tokens on that same line;
3. shuffle those slot5 states without replacement;
4. pair the shuffled slot5 states back to the unchanged token positions.

This preserves exactly for every physical line:

- page, physical leaf, paragraph and line identity;
- number of parsed tokens;
- the complete slot3 sequence and slot3 frequency vector;
- the slot5 frequency vector;
- all line-level marginal composition.

It destroys only the exact within-token slot3↔slot5 pairing. No state moves between lines or folds.

Each null is refitted from scratch in the same five physical-leaf cross-fitting procedure.

Frozen seed namespace:

`Issue55A:WithinLineSlot5Shuffle:v1:<null_index>:<page>:<paragraph>:<line_index>`

Monte-Carlo upper-tail p-value with +1 correction:

`p = (1 + # null mean Gsym >= real mean Gsym) / 1001`.

## Strong sensitivity null — within-line cyclic misalignment

The primary permutation null preserves local marginals but destroys slot5 order. As a non-gating adversarial sensitivity, generate 1,000 deterministic within-line cyclic-shift nulls:

- for every line with at least two parsed tokens, rotate the slot5 sequence by a deterministic nonzero offset;
- leave slot3 fixed;
- singleton lines remain unchanged.

This preserves the slot5 sequence itself up to cyclic alignment as well as its line-local marginal frequencies. It tests whether the same-position pairing matters beyond line-level slot5 sequential structure.

Seed namespace:

`Issue55A:WithinLineSlot5Rotate:v1:<null_index>:<page>:<paragraph>:<line_index>`

Report the same upper-tail p-value. It does not rescue a primary failure.

## Secondary descriptive statistics

Record without additional significance claims:

- pooled 5×5 contingency table;
- slot3 and slot5 marginals;
- pooled empirical mutual information in bits/token;
- Cramér's V;
- conditional probability matrices `P(S5|S3)` and `P(S3|S5)`;
- fold-specific contingency tables and gains;
- exact number of lines/tokens movable under each null family;
- null q05/q50/q95/min/max for mean `Gsym`.

These are interpretation aids, not separate discovery tests.

## Frozen classification

A primary result is **`CROSS-LEAF SLOT3xSLOT5 DEPENDENCE`** only if all conditions hold for `min`:

1. all five held-out folds have `Gsym > 0`;
2. primary within-line-shuffle upper-tail `p <= .01`;
3. real equal-weight mean `Gsym` exceeds the primary-null median by at least **`.02 bits/token`**.

If condition 2 passes but condition 3 fails, classify:

**`STATISTICALLY DETECTABLE BUT SMALL SLOT3xSLOT5 DEPENDENCE`**.

Otherwise classify:

**`NO CROSS-LEAF SLOT3xSLOT5 DEPENDENCE BEYOND LINE MARGINALS`**.

The cyclic-shift sensitivity is reported separately and cannot promote the primary class.

## Interpretation boundary

Even a positive result establishes only a stable manuscript-native dependency between two slot factors. It does not establish:

- a 25-symbol cipher;
- plaintext;
- Sloane 351;
- music;
- a semantic meaning for either slot;
- direct causation between the slots.

If positive, the next experiment should ask what explains the dependency: token-position grammar, morphological compatibility, section effects, or a lower-dimensional latent token class. That follow-up must use a new plan-first branch.

If negative, the E10 4/5 fitted-key recurrence should be treated as an optimizer/table-frequency artifact rather than retained as a manuscript-native slot3×slot5 signal.
