# Issue #26E4 — non-musical slot-mechanism audit

Status: **FROZEN BEFORE E4 EXECUTABLE / SCIENTIFIC REVEAL**

Base main at freeze: `ee1ca8376885e0711cb2dc46239ef63f1abba317`

Operational delivery rule for this branch: **do not merge to `main` without explicit user authorization**. E4 may be implemented, executed, reported, and reviewed on this branch / a draft PR, but branch completion is not permission to merge.

## 1. Why E4 exists

E3 falsified the stronger interpretation that the surviving E/E2 signal identifies the full Guidonian 20×6 row-neighborhood lattice. Once the complete labeled six-column pair-intersection matrix is fixed, two non-Guidonian higher-order alternatives equal or beat Guidonian on held-out IT2a.

The surviving object is therefore a **six-state second-order pair geometry**, not a demonstrated musical code.

E4 asks the next mechanism-level question:

> Can a purely non-musical, capacity-matched 20×6 slot-dependency topology learned from Zattera-parsed Voynich morphology in ZL transfer to the independent IT2a transcription as well as the Guidonian pair geometry?

If yes, the replicated E/E2/E3 signal is parsimoniously explainable as a property of the token grammar itself. If no, the labeled pair geometry retains an out-of-sample advantage over this explicit non-musical mechanism competitor, while still not becoming a musical decipherment.

## 2. Positive and negative claim boundary

A positive E4 non-musical result may support only:

> a generic slot-dependency topology learned without musical semantics reproduces the previously observed cross-transcription compatibility.

It may **not** establish what the manuscript means, how it was generated historically, or that Zattera slots are the author’s intended units.

A Guidonian win may support only:

> this particular capacity-matched generic slot model does not explain the surviving pair-geometry signal.

It may **not** by itself restore literal `ut/re/mi/fa/sol/la`, pitch, melody, or Guidonian-hand interpretation.

## 3. Frozen sources

### ZL discovery source

Use the same ZL3b source as E/E2:

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- required Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`

### IT2a prospective evaluation source

Use the same independent Takeshi Takahashi EvaT transcription as E2/E3:

- canonical distribution: `https://www.voynich.nu/data/IT2a-n.txt`
- required SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

No E4 topology may be fit using IT2a.

## 4. Frozen parser and population

Reuse `issue26e_core.py` without semantic changes.

Primary parser policy is **`max` / latest-valid only**, because E2-C and E3 localized the strongest prospective fixed-map signal under that policy.

Population:

- running paragraph loci only (`P` in locus code);
- normalized alphabetic EVA tokens;
- only paragraphs satisfying the existing physical-leaf eligibility rule: at least three lines and at least five visible tokens in line 1 and line 3;
- parsed-token scoring only, with visible-token parse coverage always reported.

Fresh-parser validation signatures from `SLOT_PROVENANCE_E.md` remain a hard pre-science gate.

## 5. Frozen representation

Candidate six-state channel remains Zattera **slot 10 including empty** in raw state order:

`EMPTY, d, l, r, m, n`

The remaining slots `0..9,11` are represented exactly as E/E2/E3:

- categorical one-hot per slot including empty;
- no sequence, neighbor, line-position, paragraph-position, section, hand, illustration, music or target-lattice information;
- deterministic Euclidean `k=20` clustering on unique normalized token types with equal type weight.

### ZL topology-discovery clustering

For discovery of the non-musical candidate topology, fit one deterministic `k=20` model to **all eligible parsed ZL token types** under `max`.

Then count all eligible parsed ZL token occurrences into a `20 cluster × 6 raw slot10 state` occurrence matrix `C_ZL`.

No IT2a data are used in this step.

## 6. Frozen generic non-musical topology learner

Learn a binary `20×6` matrix `M_ZL` from `C_ZL` only.

`M_ZL[c,s]=1` means that the generic non-musical model allows raw slot10 state `s` for ZL residual-morphology cluster `c`.

The learner has **exactly the same cell budget and degree profile as Guidonian**:

- 20 rows;
- six columns;
- row-degree multiset: four rows of degree 1, ten rows of degree 2, six rows of degree 3;
- every column degree exactly 7;
- total allowed cells exactly 42.

The primary objective is to maximize ZL allowed occurrence mass:

`sum_c sum_s C_ZL[c,s] * M_ZL[c,s]`.

This learner is explicitly **non-musical**:

- it does not receive `ut/re/mi/fa/sol/la` names;
- it does not receive the Guidonian lattice;
- it does not receive Guidonian pair intersections, overlap histogram, row neighborhoods or ordering;
- it receives only ZL slot-morphology counts plus the capacity constraints above.

### Deterministic optimization rule

Implement the binary optimization with a frozen numerical stack (`numpy==2.2.6`, `scipy==1.16.1`, SciPy HiGHS MILP).

Variables:

- `x[c,s] ∈ {0,1}` for the 120 cluster-state cells;
- `y[c,d] ∈ {0,1}` for row degree category `d∈{1,2,3}`.

Constraints:

1. each cluster chooses exactly one degree category;
2. `sum_s x[c,s] = sum_d d*y[c,d]`;
3. exactly `4/10/6` clusters have degree `1/2/3`;
4. every state column has exactly seven allowed clusters.

First solve the integer primary objective alone and record its optimum integer occurrence score.

Then solve again with an equality constraint fixing that primary score exactly and a deterministic SHA256-derived secondary linear objective whose total range is less than `1e-4`; this secondary objective is tie-breaking only and cannot trade one occurrence of primary score for another topology.

The executable must assert that the chosen solution attains the first-stage integer optimum and all degree invariants.

After fitting, discard ZL cluster identities and freeze only the **sorted multiset of 20 raw-state row neighborhoods**. This sorted row multiset is the transferable non-musical topology `T_ZL`.

## 7. Frozen Guidonian comparator in raw-state coordinates

Use the E2-C prospective six-state mapping, already frozen before IT inspection:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`

index tuple in raw-state order and `ut,re,mi,fa,sol,la` column order:

`(0,3,4,1,2,5)`.

Reindex the Guidonian matrix into raw-state columns once before IT scoring:

`G_raw[:,s] = GUIDO[:, fixed_map[s]]`.

No six-state permutation is searched in E4.

## 8. Prospective IT2a evaluation

Reuse the exact five physical-leaf folds from E2/E3.

For each fold:

1. fit deterministic `k=20` residual-morphology clustering on IT training token types only;
2. construct training and held-out `20×6` raw-state count matrices;
3. for `G_raw`, fit **only** the one-to-one `20 cluster → 20 row` assignment on training counts using the existing deterministic Hungarian/lexicographic rule;
4. for `T_ZL`, fit **only** the same one-to-one `20 cluster → 20 row` assignment on training counts;
5. freeze both assignments and score held-out parsed occurrences.

Thus the two models receive the same IT adaptation freedom: **row assignment only**. Neither may change its six columns or row-neighborhood topology on IT.

Primary fold score:

`A = allowed held-out parsed occurrences / held-out parsed occurrences`.

Report for each fold:

- parse coverage;
- `A_G` Guidonian raw-column accuracy;
- `A_M` non-musical ZL-topology accuracy;
- `Δ = A_G - A_M`.

Global primary summaries:

- `mean_G = mean_f A_G[f]`;
- `mean_M = mean_f A_M[f]`;
- `delta_mean = mean_G - mean_M`;
- number of folds where `M >= G`;
- number of folds where `G > M`.

## 9. Frozen classification

### Primary falsification criterion

Classify:

**`NON-MUSICAL SLOT TOPOLOGY MATCHES/BEATS GUIDONIAN`**

iff both are true:

1. `mean_M >= mean_G`;
2. `M >= G` in at least **3/5 folds**.

Otherwise classify:

**`GUIDONIAN PAIR GEOMETRY RETAINS ADVANTAGE AGAINST E4 GENERIC MODEL`**.

### Predeclared near-match diagnostic

Separately, without changing the primary classification, label the result a **near match** if:

- `mean_M >= mean_G - 0.005`.

The 0.5 percentage-point band is diagnostic only; it cannot convert a primary Guidonian win into the non-musical classification.

## 10. Pair-geometry diagnostics after topology is frozen

After `T_ZL` is learned, report without gating:

- its labeled `6×6` column-intersection matrix in raw-state coordinates;
- the corresponding `G_raw` pair-intersection matrix;
- off-diagonal L1 distance between the two pair matrices;
- whether they are exactly equal;
- overlap-histogram comparison;
- row-neighborhood multiplicities.

Also compare `T_ZL` against the three E3 exact-pair alternatives only descriptively. No E4 model may be selected from those alternatives.

These diagnostics ask whether a non-musical ZL learner independently recovers the same second-order geometry that E3 isolated.

## 11. Integrity replay gates

Before E4 classification is accepted, the executable must assert:

1. parser validation signatures pass;
2. ZL3b Git blob SHA matches the frozen value;
3. IT2a SHA-256 matches the frozen value;
4. `G_raw` IT2a held-out fold accuracies reproduce E3/E2-C within `1e-12`:
   - `0.835597`
   - `0.802178`
   - `0.870536`
   - `0.848460`
   - `0.811799`
   using full-precision frozen values from the prior raw/replay implementation where available;
5. mean `G_raw` reproduces `0.8337140490` within the stored full-precision tolerance.

If exact full-precision fold constants differ from the rounded report values, the executable must obtain and freeze the exact constants from the already committed E3 implementation/result before first E4 reveal; it must not weaken the replay tolerance after observing E4.

## 12. Anti-overfit / forbidden changes after reveal

After first E4 reveal do not:

- alter slot10 or its six raw states;
- change parser policy from `max`;
- change `k=20`;
- change the row-degree or column-degree constraints;
- let the generic topology inspect IT2a;
- search six-state permutations;
- tune the non-musical topology on IT heldout leaves;
- switch from occurrence objective to a different objective because of outcome;
- add Guidonian pair information to the generic learner;
- change the primary classification threshold;
- relabel a post-hoc variant as E4.

Any scientifically material post-reveal change requires a new experiment label.

## 13. Interpretation ladder

If the non-musical topology matches/beats Guidonian, the direct-music interpretation of E/E2 is further weakened: a generic slot-dependency structure learned without music semantics is sufficient to reproduce or exceed the transferable compatibility.

If Guidonian retains an advantage, the result says only that this explicit capacity-matched generic learner is insufficient. Because E3 already showed the higher-order Guidonian lattice is not identified, such a result would justify a broader family of non-musical six-category controls before returning to music-specific sequence predictions.

Under neither outcome may E4 authorize melody extraction or literal pitch naming.
