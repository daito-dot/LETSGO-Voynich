# Phase 66B — prospective attribute↔label association test

Status: **FROZEN BEFORE FIRST IMAGE↔TEXT ASSOCIATION**

## 1. Question

Do the independently sealed botanical morphology and normalized color measurements carry object-level information about the independently sealed structural representation of their physically attached Voynich labels?

This is a global dependence test. It does not search freely over individual morphology↔glyph pairs.

## 2. Chronology

- primary page: `f102v2` (11 retained objects; rows L2=6, L3=5)
- replication page: `f100v` (13 retained objects; rows T=4, M=5, B=4)
- primary must be run and archived first;
- replication must be run regardless of primary outcome;
- no scientific code, weights, thresholds, eligibility rules, or text features may change between primary and replication.

## 3. Frozen image representation

Three image feature groups are used, each with equal group weight so that the larger color feature count cannot dominate morphology.

### I1 morphology

Exactly the three Phase66A eligible characters:

- `leaf_composition`
- `leaf_arrangement`
- `leaf_margin`

For each character and object pair: distance 0 if both observed and equal, 1 if both observed and different, missing if either state is U. I1 pair distance is the mean over observed eligible characters. If no character is jointly observed for a pair, I1 is missing for that pair.

### I2 Color-B binary presence

Exactly the binary clusters passing `COLOR_REPORT_B.md`: C1 and C2.

Pair distance is normalized Hamming distance across the two presence bits.

### I3 Color-B continuous area

Exactly C1, C2, C3 area fractions, because all three passed the frozen continuous eligibility rule.

For each cluster, area fractions are min-max scaled using the frozen 24-object image-side population only. Pair distance is mean absolute scaled difference across C1/C2/C3.

### Composite image distance

`D_image = mean(available I1, I2, I3)`.

I2 and I3 are always available. Therefore every pair has a composite distance. No imputation of U morphology states is permitted.

## 4. Frozen text representation

Use `TEXT_PLAN_A.md` exactly. Composite `D_text` is the equal-weight mean of five text-distance groups: glyph length, first glyph, last glyph, retained unigram-presence Jaccard distance, retained bigram-presence Jaccard distance.

## 5. Primary statistic

Within each physical row, enumerate all unordered object pairs and compute Spearman correlation between `D_image` and `D_text`.

Page statistic:

`T = pair-count-weighted mean of row Spearman rho values`.

A positive T means objects more similar in frozen image attributes tend to have labels more similar in frozen text structure.

If a row has undefined Spearman correlation because either distance vector is constant, that row is excluded and its pair count is not used. If fewer than two physical rows are usable on f102v2, primary is `BLOCKED` before interpretation. For f100v replication, at least two rows must be usable.

## 6. Exact null

Hold all image measurements fixed. Permute complete label identities among objects **within each physical row** and recompute the entire text-distance matrix and T.

This preserves page and row structure while breaking object-level image↔label attachment.

Enumerate the full row-restricted permutation space:

- f102v2: `6! × 5! = 86,400`
- f100v: `4! × 5! × 4! = 69,120`

The identity permutation is included.

Exact one-sided p-value:

`p = count(T_perm >= T_observed) / N_permutations`.

## 7. Frozen pass rule

Primary passes only if both:

- `T >= 0.20`, and
- exact one-sided `p <= 0.05`.

The same threshold applies to replication.

The T>=0.20 requirement is a practical-effect firewall and deliberately matches the magnitude convention used in Phase65B, while the predictor representation and scientific hypothesis are different.

## 8. Multiplicity

There is exactly one confirmatory global statistic per page. Therefore no additional within-page multiplicity correction is required for the primary claim.

Individual feature-pair associations may be computed only after the global primary result is sealed and are secondary/explanatory. They cannot convert a failed global test into a pass.

## 9. Classification

- primary pass + replication pass: `M8-B2 REPLICATED ATTRIBUTE-LABEL RELATION`
- primary pass + replication fail: `M8-B2 PRIMARY-ONLY ATTRIBUTE-LABEL RELATION`
- primary fail + replication pass: `M8-B2 REPLICATION-ONLY / NONCONFIRMATORY`
- primary fail + replication fail: `M8-B2 NO DETECTED ATTRIBUTE-LABEL RELATION`
- provenance/input/statistic validity failure: `M8-B2 BLOCKED`

## 10. No-repair rule

After the primary result is revealed and before replication, do not:

- alter morphology eligibility;
- alter Color-B clusters, white balance, masks, or eligibility;
- add/remove/reweight text features;
- change row structure;
- change T threshold or p threshold;
- switch transcription authority;
- inspect secondary feature associations to redesign replication.

## 11. Synthetic preflight

Before reading the real cross-modal statistic, the executable must pass synthetic tests demonstrating:

1. independence produces no forced positive signal;
2. a constructed aligned image/text distance structure produces positive T and a low exact p where combinatorially achievable;
3. label permutation is restricted to physical rows;
4. identity permutation is included;
5. exact permutation counts are 86,400 and 69,120 for the real row sizes;
6. U morphology handling follows Section 3 without imputation.

Synthetic data must not use the real P25 label strings.

## 12. Claim boundary

Even replicated support would establish only a local prospective statistical relation between frozen depicted attributes and frozen label structure in these pharmaceutical fragments. It would not establish plant names, historical taxa, plaintext, semantics, language identity, cipher family, or a decipherment key.
