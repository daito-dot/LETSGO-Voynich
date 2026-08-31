# Issue #26E3 — structured-null specificity challenge

Status: **FROZEN BEFORE E3 EXECUTABLE / E3 SCIENTIFIC REVEAL**

Issue: #26

Base main: `73dc7e2cedec45f95122045b71bafad7395f510a`

Issue26E2 established a strong replicated result for the specific Guidonian 20-locus×6-vox admissibility lattice, including prospective ZL→IT transfer of a six-state slot10→vox mapping. E3 attacks the strongest remaining nuisance explanation before any melody-level analysis:

> Does the result identify the *specific Guidonian row-neighborhood geometry*, or would a non-musical six-column lattice with the same low-order overlap structure fit equally well because Voynich token morphology is itself an ordered combinatorial grammar?

No new music mapping is fitted in E3.

## Frozen source and population

Use only the independent IT2a / Takeshi Takahashi EvaT transcription:

- canonical source: `https://www.voynich.nu/data/IT2a-n.txt`
- accepted Phase63B / E2 SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

The workflow must fail before science if the canonical bytes do not match.

Reuse exactly the five E/E2 physical-leaf folds. No rebalancing is allowed.

## Frozen Voynich representation

Reuse merged `issue26e_core.py` unchanged:

- fresh Zattera 12-slot parser and validation gate;
- **max/latest-valid parser only** for E3;
- slot10 state order `EMPTY,d,l,r,m,n`;
- remove slot10 and represent slots `0..9,11` by the same categorical one-hot vector;
- sequence-blind deterministic `k=20` clustering on unique IT training token types;
- fit clusters separately inside each training fold exactly as E2;
- held-out metric remains `A = allowed parsed occurrences / parsed occurrences`.

The six slot10-state→column mapping is frozen prospectively from E2 and may not be optimized:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`

index tuple `(0,3,4,1,2,5)` in the existing state/vox orders.

For Guidonian and every E3 null matrix, fit **only** the 20 cluster→20 row bijection on IT training occurrences by the same optimal assignment procedure. Then freeze that row mapping and score the held-out fold.

## What is actually discriminative after row fitting

Because cluster→row labels are freely fitted on training data, the physical ordering of the 20 gamut rows is not itself evidence in E/E2. The relevant matrix object is the **multiset of six-column neighborhoods carried by the 20 rows**.

E3 therefore preserves progressively more of that object.

## Frozen Guidonian invariants

The merged Guidonian matrix has:

- 20 rows, six columns, 42 allowed cells;
- row-degree multiset: four degree-1, ten degree-2, six degree-3 rows;
- every column degree = 7;
- pairwise column intersection matrix, in vox order `ut,re,mi,fa,sol,la`:

```
[[7,2,0,4,3,0],
 [2,7,2,0,4,3],
 [0,2,7,2,0,4],
 [4,0,2,7,2,0],
 [3,4,0,2,7,2],
 [0,3,4,0,2,7]]
```

Across the 15 off-diagonal column pairs, the overlap histogram is exactly:

- overlap 0: 5 pairs
- overlap 2: 5 pairs
- overlap 3: 2 pairs
- overlap 4: 3 pairs

These invariants are computed from the historical Guidonian lattice only, with no Voynich outcome used.

## E3-A — exact pair-matrix alternative tournament

This is the strongest low-order-moment challenge.

Restrict candidate 20×6 binary matrices to all of the following:

1. row degrees only 1, 2 or 3;
2. exactly 4 degree-1, 10 degree-2, 6 degree-3 rows;
3. all six column degrees exactly 7;
4. the **entire labeled 6×6 pairwise column intersection matrix is exactly identical to Guidonian**.

A complete combinatorial enumeration was performed before the E3 executable and before any E3 Voynich score. The method enumerates all weak compositions of the six degree-3 rows over the `C(6,3)=20` possible triple neighborhoods; the fixed pair intersections then determine all degree-2 counts, and the fixed column degrees determine all degree-1 counts.

There are exactly **four** feasible row-neighborhood multisets, one Guidonian and **three non-Guidonian alternatives**.

The complete frozen enumeration is `E3_EXACT_PAIR_ALTERNATIVES.json` with expected SHA-256:

`8debd0aabeba75d15e73f0819e0466028324138c5360b9d8856af2f99774cbfa`

All four candidates receive identical training-only row assignment freedom and the same fixed six-state column mapping.

E3-A passes only if:

- Guidonian has strictly highest across-fold mean held-out accuracy among all four candidates; and
- against each of the three alternatives separately, Guidonian wins strictly in at least 3/5 held-out folds.

Ties count against Guidonian. There is no significance claim from four candidates; this is an exhaustive adversarial tournament.

If any exact-pair alternative matches or beats Guidonian in mean held-out accuracy, the E2 fixed-map signal is not specific beyond second-order column geometry.

## E3-B — pair-overlap-histogram-matched structured null

E3-A holds the labeled pair matrix fixed and leaves only triple/higher row-neighborhood choices. E3-B asks whether the Guidonian arrangement of which column pairs receive overlap 0/2/3/4 is itself special.

The frozen catalog `E3_STRUCTURED_NULLS.json` contains exactly 100 distinct non-Guidonian row-neighborhood multisets. Every catalog matrix has:

- 20 rows / six columns / 42 cells;
- row-degree multiset exactly `1×4, 2×10, 3×6`;
- all column degrees exactly 7;
- pairwise overlap **histogram** exactly `0×5, 2×5, 3×2, 4×3`;
- a labeled pair-overlap vector different from the Guidonian vector;
- a row-neighborhood multiset different from Guidonian;
- no duplicate row-neighborhood multiset in the catalog.

The catalog was generated before the scientific executable by deterministic random assignments of the fixed overlap multiset to the 15 labeled column pairs, followed by an integer-feasibility solve over all size-1/2/3 row neighborhoods. No Voynich text or score enters catalog generation.

Expected catalog SHA-256:

`dd32a66b93d7250a3244b14cfc496d4a760cbdca826bbc1bbdf3e792e1ae273d`

Generation label:

`Issue26E3:pair-histogram-catalog:v1`

The frozen catalog required 1,805 candidate pair assignments to obtain 100 distinct feasible nulls. This attempt count is descriptive provenance, not a scientific metric.

For each fold, fit the row assignment of each of the 100 catalog matrices on the same IT training counts and score the same held-out occurrences.

Global paired null:

- `mean_G = mean_f A_G[f]`
- `mean_N[j] = mean_f A_N[f,j]`
- `p_global = (1 + #{j: mean_N[j] >= mean_G}) / 101`

E3-B passes if:

1. `p_global <= 0.05`;
2. Guidonian mean accuracy exceeds the median of `mean_N`;
3. Guidonian exceeds the fold-specific catalog median in at least 4/5 folds.

## Frozen E3 classification

- **`GUIDONIAN-SPECIFIC BEYOND PAIR GEOMETRY`**: E3-A and E3-B both pass.
- **`PAIR-GEOMETRY SUFFICIENT / GUIDONIAN NOT SPECIFIC`**: E3-A fails, regardless of E3-B.
- **`STRUCTURED-NULL CHALLENGE NOT SURVIVED`**: E3-A passes but E3-B fails.

No E3 result licenses melody extraction. Even a full E3 pass only narrows the surviving hypothesis from generic sparse/overlap geometry toward the specific Guidonian row-neighborhood multiset.

## Next-step firewall

Do not use Voynich outcomes to:

- reorder the six voces;
- change the frozen ZL→IT slot10 map;
- choose alternative row-degree or overlap constraints;
- drop an exact-pair alternative;
- select only favorable catalog matrices;
- change k=20 or the parser policy;
- fit pitch order or melody.

Only after E3 is revealed and recorded may a new plan consider sequence-level Guidonian mutation constraints.
