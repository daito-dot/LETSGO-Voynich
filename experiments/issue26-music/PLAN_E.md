# Issue #26 experiment E — Guidonian 20-locus × 6-vox slot-lattice test

Status: **FROZEN BEFORE EXECUTABLE / SCIENTIFIC REVEAL**

Issue: #26

Base main: `4d4ca6ef3bc38ddefa43978d9569d4d565314e25`

Slot provenance is separately frozen in `SLOT_PROVENANCE_E.md` and controls the fresh parser validation gate.

## Question

Does a sequence-blind factorization of Voynich token-internal slot structure contain the specific combinatorial lattice expected if one six-state channel behaves like the six Guidonian `voces` while the remaining morphology identifies the twenty positions of the medieval gamut?

This is intentionally narrower than “Voynich is music.” A positive result would establish only held-out structural compatibility with one historically motivated two-channel coding architecture.

## Historical target fixed before Voynich evaluation

The medieval Guidonian gamut combines twenty pitch loci with the six solmization `voces` `ut re mi fa sol la`. The allowed voice set varies by locus because natural, hard and soft hexachords overlap. The target lattice used here is fixed as:

1. Γ: `{ut}`
2. A: `{re}`
3. B: `{mi}`
4. C: `{fa,ut}`
5. D: `{sol,re}`
6. E: `{la,mi}`
7. F: `{fa,ut}`
8. G: `{sol,re,ut}`
9. A: `{la,mi,re}`
10. B: `{fa,mi}`
11. C: `{sol,fa,ut}`
12. D: `{la,sol,re}`
13. E: `{la,mi}`
14. F: `{fa,ut}`
15. G: `{sol,re,ut}`
16. A: `{la,mi,re}`
17. B: `{fa,mi}`
18. C: `{sol,fa}`
19. D: `{la,sol}`
20. E: `{la}`

Consequences fixed before evaluation:

- 20 locus rows;
- row-degree profile: `1,1,1,2,2,2,2,3,3,2,3,3,2,2,3,3,2,2,2,1`;
- six vox columns;
- every vox occurs in exactly seven loci;
- 42 allowed locus×vox cells in total.

The primary historical basis is the traditional Guidonian gamut/hand tradition: twenty pitches designated through combinations of the six voces, with overlapping hexachords. No Voynich sequence outcome is used to construct this lattice.

## Frozen Voynich source

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- expected git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`

Population:

- running paragraph loci only (`P` in locus code);
- visible normalized alphabetic EVA tokens;
- only tokens having at least one legal **single-unit** parse under the freshly implemented 12-position Zattera table;
- primary parser policy = `min` earliest-valid;
- sensitivity = `max` latest-valid.

All parse coverage is reported. Unparseable or multi-unit-required tokens are excluded rather than force-fit.

## Physical-leaf holdout

Reuse the Issue26A / Phase62 physical-leaf rule exactly:

1. parse Voynich paragraphs;
2. an item is base-eligible when it has at least three lines and lines 1 and 3 each contain at least five visible tokens;
3. collect the eligible physical leaf numbers in ascending order;
4. folds are `leaves[i::5]` for `i=0..4`.

All token-type clustering and all lattice mappings are fitted on training leaves only. Scientific scoring uses held-out leaves only.

## Candidate vox channel

The candidate six-state channel is **Zattera slot 10**, with states:

`EMPTY, d, l, r, m, n`

Slot 10 is selected solely because the independently published slot table gives exactly six states including empty. No alternative slot or grouping may be selected after reveal and called experiment E.

## Candidate locus representation

For each legal parsed token, completely remove slot 10.

Represent the remaining slots `0..9,11` by a binary categorical one-hot vector. Each possible non-empty slot value has its own feature; the empty state of each slot also has its own feature. No sequence position, neighboring token, line position, paragraph position, section, hand or target music statistic enters this vector.

For each physical-leaf fold:

- fit on unique normalized token **types from training leaves only**, each type weight 1;
- if a token type has several legal parses, primary uses its `min` parse and sensitivity its `max` parse;
- deterministic `k=20` Euclidean k-means on the binary vectors;
- no feature standardization;
- first centroid = lexicographically smallest token type;
- subsequent centroids = training type maximizing distance to its nearest existing centroid, ties lexicographically;
- Lloyd updates until assignments stop or 100 iterations;
- empty cluster is replaced by the training type farthest from its currently assigned centroid, ties lexicographically;
- held-out types use nearest frozen centroid; ties smallest cluster index.

The cluster numbers have no pitch interpretation until the training-only lattice assignment below.

## Training-only mapping to the Guidonian lattice

For a fold, form training occurrence counts `C[c,s]` for 20 morphology clusters `c` and six slot-10 states `s`.

For the fixed Guidonian binary lattice `G[r,v]`, choose mappings using **training occurrences only**:

1. enumerate all `6! = 720` bijections from the six observed slot-10 states to the six voces;
2. for each vox mapping, find the one-to-one assignment of the 20 morphology clusters to the 20 Guidonian locus rows maximizing training occurrence mass in allowed cells (Hungarian assignment);
3. select the globally maximal training score;
4. ties are resolved lexicographically by the six-state vox permutation and then the cluster→row assignment.

The selected mapping is then frozen for held-out scoring.

## Primary held-out score

For every held-out parsed token occurrence, map its morphology cluster and slot-10 state through the frozen training mapping.

`A = allowed held-out occurrences / all held-out parsed occurrences`

This is an out-of-sample admissibility accuracy, not a melody score.

## Degree-matched non-Guidonian null

The important null is not a random 20×6 matrix. Null lattices must have the **same combinatorial capacity** as the Guidonian lattice.

For each fold generate exactly **100** deterministic non-Guidonian binary matrices by degree-preserving bipartite double-edge swaps starting from `G`:

- all 20 row degrees remain exactly equal to the corresponding Guidonian row degrees;
- all six column degrees remain exactly 7;
- total allowed cells remains 42;
- matrices identical to `G` are rejected;
- duplicate matrices within the fold are rejected;
- deterministic SHA-256-derived seeds from `Issue26E:<policy>:fold:<f>:null:<j>`;
- for each candidate matrix perform 5,000 attempted double-edge swaps and retain only a changed degree-valid matrix.

Every null lattice receives the **same training optimization freedom** as `G`: all 720 six-state↔column assignments and the optimal 20-cluster↔row Hungarian assignment are fitted on training occurrences, then frozen and scored on the same held-out fold.

This tests the *specific pattern of Guidonian allowed cells*, not merely its row/column sparsity.

## Fold and global statistics

For fold `f`:

- `A_G[f]` = held-out Guidonian accuracy;
- `A_N[f,j]` = held-out accuracy for null lattice `j`;
- fold rank and empirical `p_fold = (1 + #{j: A_N[f,j] >= A_G[f]}) / 101`.

Global statistic:

- `mean_G = mean_f A_G[f]`;
- pair null index across folds: `mean_N[j] = mean_f A_N[f,j]`;
- `p_global = (1 + #{j: mean_N[j] >= mean_G}) / 101`.

Also report per-fold null median and 95th percentile and `mean_G - median_j(mean_N[j])`.

## Primary decision gate (`min` parser)

`NARROW GUIDONIAN SLOT-COMPATIBILITY` only if **all** hold:

1. mean held-out single-unit parse coverage >= `0.60`;
2. `p_global <= 0.05`;
3. `A_G` exceeds the fold-specific null median in at least `4/5` folds.

Otherwise primary classification is `NOT SUPPORTED`.

The 0.60 coverage floor is only an interpretability gate; falling below it cannot be called positive evidence.

## Predeclared `max`-parser sensitivity

Repeat the complete clustering/mapping/null procedure using latest-valid parses.

For robustness of a primary positive result require:

- same sign of global advantage (`mean_G > median mean_N`), and
- sensitivity `p_global <= 0.10`.

A primary failure is not rescued by a positive sensitivity.

## Interpretation boundary

If positive, retain only:

> one independently selected six-state Voynich slot channel and a sequence-blind twenty-class representation of the remaining token morphology generalize to the specific Guidonian admissibility lattice better than equally sparse degree-matched non-Guidonian lattices under identical training mapping freedom.

Do **not** infer a melody, note names, instrument, composer, plaintext or historical authorship.

If negative, retain only that this specific `slot10 = vox / remaining morphology = gamut locus` model is weakened. Other tablature, duration, multi-voice or intermediate-cipher models remain logically possible but require new preregistered constraints.

## Non-negotiable anti-overfitting rules

After reveal do not:

- choose a different Voynich slot as the six-state channel;
- merge/split slot-10 states;
- change `k=20`;
- reorder or modify the Guidonian allowed-pair lattice;
- choose a different parser policy as primary;
- use token sequence to create the 20 morphology classes;
- tune mappings on held-out leaves;
- compare only against unoptimized null lattices;
- retune the null degree profile;
- call a post-hoc alternative `Issue26E`.
