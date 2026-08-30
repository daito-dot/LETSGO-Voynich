# Phase 62B — N0 implementation freeze

Status: frozen before N0 score evaluation.

This note resolves implementation details left implicit in `PLAN.md`. It does not change the Phase62 scientific design and does not evaluate C0, A1, or H62-P1.

## Scope

Phase62B computes **N0 only**: unencoded source-native structured medieval Latin controls against the common S1–S3 scorecard.

Forbidden in this phase:

- evaluating or selecting C0 transforms;
- regenerating/re-scoring A1;
- computing the Voynich H62-P1 distance profile;
- changing primary manuscript membership after seeing N0 results.

## Input verification

Voynich input must be the pinned `matthewdgreen/cipher_benchmark` file with Git blob SHA-1:

`2a4533ab9bdfa85db9bad602d590978953055df1`

CREMMA checkout must be exactly:

`292525969ad98380b398e6606a9c2a36d51913ae`

Primary medieval manuscripts are fixed:

- `BIS-193`
- `CLM13027`
- `Mazarine915`
- `UBL758`

H318 is a predeclared sensitivity only.

## Medieval item parser

Within each source file:

1. a literal `¶` starts a new item;
2. text before a pilcrow on that physical line belongs to the preceding item, if any;
3. text after the pilcrow is line0 of the new item;
4. following physical source lines are appended until the next pilcrow or file end;
5. if multiple pilcrows occur on one physical line, each marker closes the preceding item and starts the next item from the following same-line segment.

No text is joined across source files.

Base item eligibility for S2/S3:

- at least 3 physical item lines;
- line0 has at least 5 usable tokens;
- line2 has at least 5 usable tokens.

S1 additionally requires at least one valid internal pseudo-boundary `j -> j+2`, `j>=1`, with both compared lines containing at least 5 usable tokens. Thus an item may contribute to S2/S3 but not S1.

## Voynich paragraph parser

Use P-coded prose lines only. Explicit `<%>` starts a paragraph. Recto and verso sharing the same folio number remain in the same physical-leaf outer fold.

The same base/S1 eligibility distinction is used as above.

## Token and graphematic-unit representation

### Voynich

A usable token is the lowercase alphabetic EVA string after the existing ZL3b markup-cleaning rule. Graphematic units are individual EVA characters.

### Medieval Latin

A usable token is a maximal Unicode NFC Letter/Mark sequence. Within a token, a graphematic unit is one base Letter plus immediately following combining Mark code points. An isolated leading Mark, if encountered, is retained as its own unit rather than discarded.

All edit-distance calculations operate on graphematic-unit tuples, not Python code-point string distance.

## Fixed-five 8D features for S1/S3

For every line with at least 5 tokens, use exactly the first 5 tokens and compute:

1. TTR;
2. mean graphematic token length;
3. token-length SD;
4. graphematic unit inventory size;
5. graphematic unit entropy;
6. first-unit entropy;
7. last-unit entropy;
8. within-line fraction of tokens having a non-identical edit-distance-1 token elsewhere among the same five tokens.

No full-line token count enters these primary features.

## S1 exact implementation

For each Voynich outer physical-leaf fold:

1. derive feature SDs from all >=5-token lines in base-eligible **training** paragraphs; zero SD becomes 1;
2. for each S1-eligible training paragraph, compute:
   - real delta `(line2 - line0) / SD`;
   - every valid internal pseudo delta `(line[j+2] - line[j]) / SD`, `j>=1`;
   - paragraph contrast = real delta minus mean pseudo delta;
3. training direction = mean paragraph contrast, normalized to unit L2 norm;
4. held-out Voynich S1 = mean held-out paragraph contrast projected onto the training direction;
5. for each medieval manuscript, compute item contrasts using the **same Voynich training SD and direction**, then average items within that manuscript;
6. N0 S1 = equal mean of the four manuscript means.

No medieval manuscript contributes to direction/scaling estimation.

## S2 exact implementation

Included lines are all non-empty physical lines belonging to base-eligible paragraphs/items.

Observed local-prev10 fraction:

- for every token occurrence, inspect only preceding tokens on the **same physical line**;
- use up to 10 preceding tokens;
- success if at least one is a non-identical edit-distance-1 neighbor;
- denominator includes every token occurrence in the included lines.

Null separately for each held-out Voynich fold and each medieval manuscript:

- collect the exact token multiset from included lines;
- preserve each line's exact token-slot count;
- shuffle the pooled tokens and refill the line slots;
- 100 deterministic replicates;
- use the median null fraction.

`S2 = observed - null_median`.

For N0, compute S2 per manuscript and equal-average manuscripts. Do not pool tokens across manuscripts.

## S3 exact implementation

Use fixed-five 8D features from lines in base-eligible paragraphs/items. Position groups are `0`, `1`, `2`, `3+` by item-relative physical line index.

Eta-squared is computed separately for every feature using all available groups in that dataset. S3 is the mean of the eight eta-squared values.

N0 S3 is calculated per manuscript and then equal-averaged.

## Edit-distance neighbor implementation

For each dataset vocabulary, construct exact edit-distance-1 neighbor sets at graphematic-unit level using:

- same-length one-unit substitution signatures;
- one-unit insertion/deletion relationships.

Identical tokens are never neighbors. This same relation is used in S1 feature 8 and S2.

## Outer folds and deterministic null seeds

Voynich physical leaves are sorted numerically and assigned to five folds by `leaves[i::5]`, matching the Phase61 convention.

Null seeds are fixed from manuscript/fold identifiers and replicate index. Results are deterministic under the pinned inputs and executable.

## Primary N0 decision output

For each fold report:

- held-out Voynich S1, S2, S3;
- each manuscript S1, S2, S3;
- equal-manuscript N0 S1, S2, S3;
- N0/Voynich ratio where denominator is positive and numerically stable;
- S1/S2/S3 relative error regardless of ratio.

Across folds report:

- mean Voynich targets;
- mean N0 targets;
- ratio of means where valid;
- mean fold ratios;
- leave-one-manuscript-out aggregates;
- per-manuscript heterogeneity.

N0 is labelled materially competitive only according to the already frozen rule in `PLAN.md`; the raw result is retained regardless.

## Sensitivities

H318 is computed and reported separately but never included in the primary four-manuscript aggregate.

Arras861 has no eligible literal-pilcrow items and therefore has no primary N0 S1–S3 result; it remains reserved for later non-entry document sensitivity.

## Prospective holdout firewall

The Phase62B executable must contain **no implementation of H62-P1** and must not emit any 1–2 / 3–5 / 6–10 / 11–20 / 21–40 recurrence-distance statistics.