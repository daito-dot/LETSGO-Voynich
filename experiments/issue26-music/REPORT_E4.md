# Issue #26E4 — non-musical slot-mechanism audit

Status: **NON-MUSICAL SLOT TOPOLOGY MATCHES/BEATS GUIDONIAN**

E4 is a successful mechanism-level falsification of the remaining music-specific interpretation of the E/E2/E3 slot result.

A capacity-matched 20×6 topology learned from **ZL slot/morphology counts only**, with no Guidonian lattice, no music vocabulary, no Guidonian pair-overlap information and no IT2a information, transferred prospectively to the independent IT2a transcription **better than the Guidonian comparator**:

- mean Guidonian held-out accuracy: **0.8337140490**
- mean non-musical topology held-out accuracy: **0.8529061469**
- non-musical advantage: **+0.0191920979** (about **+1.92 percentage points**)
- non-musical topology matched or beat Guidonian in **4/5 folds**

Under the frozen E4 gate, the classification is therefore:

**`NON-MUSICAL SLOT TOPOLOGY MATCHES/BEATS GUIDONIAN`**

This does not prove a specific non-musical plaintext or historical mechanism. It does show that the previously surviving six-state structural signal is **not diagnostic of Guidonian/music structure** under this explicit generic slot-grammar competitor.

## 1. Why E4 was run

E/E2 found a reproducible association between:

- the six-state Zattera slot10 channel (`EMPTY,d,l,r,m,n`),
- sequence-blind twenty-class residual morphology,
- and the Guidonian 20×6 admissibility lattice.

E3 then showed that the **full Guidonian row-neighborhood system is not identified**. Two of the three exhaustive non-Guidonian alternatives sharing the exact same labeled 6×6 pair-intersection matrix equaled or exceeded Guidonian on held-out IT2a. E3 therefore localized the surviving evidence to second-order six-state pair geometry.

E4 asked the next falsification question:

> Can a purely non-musical, capacity-matched slot-dependency topology learned on ZL transfer to independent IT2a as well as the Guidonian pair geometry?

## 2. Chronology firewall

The E4 scientific order was preserved in repository history:

1. `PLAN_E4.md` committed first at `991a3997dfc7b89ca604b3458734fcade7d00ea1`;
2. a population wording inconsistency was discovered by auditing the already-frozen E/E2/E3 implementation and corrected **before the E4 executable existed** in `POPULATION_AMENDMENT_E4A.md`, commit `5ddb85257387248dfcfcbec018bc1c92eaf36883`;
3. `phaseE4_nonmusic_mechanism.py` was then committed at `9cff6c1cb611eedd0d70615f3dacec00e750b218`;
4. the first scientific reveal occurred only after the workflow commit, on scientific head `b7a39e8ba9f2ebd05990244f76cb740458b12118`.

The Actions chronology gate verified that both frozen documents are ancestors of the first executable commit.

### Pre-executable population clarification

The initial plan wording could be read as counting only paragraphs that independently satisfy the `>=3 lines`, `line1>=5 tokens`, `line3>=5 tokens` rule.

The frozen E/E2/E3 code actually uses that rule only to define the admitted **physical-leaf universe**. Once a leaf is admitted, all running-text (`P`) paragraphs on that leaf are counted.

E4 preserved that existing behavior. The clarification was made before any E4 topology was fit or any E4 IT score was calculated.

## 3. Frozen sources and parser

### ZL discovery source

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- required Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`

The first-reveal workflow downloaded this exact object and passed the blob-hash gate.

### IT2a prospective evaluation source

- canonical Takeshi Takahashi EvaT distribution
- required SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

The live canonical file passed the exact hash gate.

### Parser / representation

E4 reused `issue26e_core.py` unchanged:

- parser policy: **max / latest-valid**;
- candidate six-state channel: slot10 raw states `EMPTY,d,l,r,m,n`;
- residual morphology: categorical one-hot slots `0..9,11`, including empty states;
- deterministic Euclidean `k=20` clustering on unique normalized token types with equal type weight;
- no sequence, line-position, section, illustration or music information in the representation.

The frozen parser validation signatures all passed before science.

## 4. Non-musical topology learner

E4 learned one transferable binary `20×6` topology from ZL only.

The learner received:

- the ZL `20 residual-morphology clusters × 6 raw slot10 states` occurrence counts;
- a capacity constraint matching the Guidonian model.

It did **not** receive:

- `ut/re/mi/fa/sol/la` names;
- the Guidonian lattice;
- Guidonian pair intersections;
- Guidonian overlap histogram;
- Guidonian row neighborhoods or order;
- IT2a data.

Capacity was matched exactly:

- 20 rows;
- six columns;
- row-degree multiset `1×4, 2×10, 3×6`;
- every column degree = 7;
- 42 allowed cells.

The topology was optimized by frozen SciPy/HiGHS MILP to maximize ZL allowed occurrence mass. A second optimization fixed the integer primary optimum exactly and used only a deterministic SHA256-derived sub-`1e-4` objective to break primary-score ties.

Learner audit:

- ZL primary optimum allowed occurrences: **21874**
- secondary objective value: `3.393000000000001e-05`
- total secondary-weight range: `9.438e-05`

After learning, ZL cluster identities were discarded. Only the sorted multiset of raw-state row neighborhoods transferred to IT2a:

`[1,1,2,3,3,3,3,3,12,12,16,28,28,44,44,44,48,48,48,50]`

## 5. Guidonian comparator and matched IT adaptation

The comparator used the already-prospective E2-C state mapping:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`

index tuple:

`(0,3,4,1,2,5)`

No six-state permutation was searched in E4.

On each IT2a fold, both models received the same adaptation freedom:

- fit `k=20` on IT training token types only;
- fit only a one-to-one `20 IT clusters → 20 topology rows` assignment on training occurrences;
- freeze that assignment;
- score held-out leaves.

The non-musical topology itself was never refit on IT2a.

## 6. Exact E2-C / E3 replay gate

Before accepting the new comparison, E4 reproduced the previous Guidonian fixed-map result exactly:

- mean IT parse coverage: **0.8213154353321266**
- mean Guidonian accuracy: **0.8337140490098738**
- fold accuracies:
  - fold0 `0.8355972832600879`
  - fold1 `0.8021775235283263`
  - fold2 `0.8705357142857143`
  - fold3 `0.8484604223762695`
  - fold4 `0.8117993015989707`

All replay assertions passed within `1e-12`.

## 7. Primary E4 result

| fold | Guidonian | non-musical ZL topology | G − nonmusic |
|---:|---:|---:|---:|
| 0 | 0.835597 | **0.850779** | −0.015182 |
| 1 | 0.802178 | **0.847942** | −0.045765 |
| 2 | 0.870536 | **0.871971** | −0.001435 |
| 3 | **0.848460** | 0.844914 | +0.003547 |
| 4 | 0.811799 | **0.848925** | −0.037126 |
| **mean** | **0.833714** | **0.852906** | **−0.019192** |

Frozen gate:

1. `mean_nonmusic >= mean_Guidonian`: **PASS**
2. nonmusic `>=` Guidonian in at least 3/5 folds: **PASS (4/5)**

Frozen classification:

**`NON-MUSICAL SLOT TOPOLOGY MATCHES/BEATS GUIDONIAN`**

This is not merely inside the predeclared 0.5-percentage-point near-match band. The non-musical model exceeds Guidonian by about **1.92 percentage points on average**.

## 8. The generic topology did not simply rediscover Guidonian pair geometry

The result is stronger as a mechanism audit because the learned topology is structurally different from Guidonian.

Raw state order:

`EMPTY, d, l, r, m, n`

Generic learned pair-intersection matrix:

```text
7 5 0 0 0 0
5 7 0 0 1 1
0 0 7 7 2 3
0 0 7 7 2 3
0 1 2 2 7 4
0 1 3 3 4 7
```

Guidonian comparator in the same raw-state coordinates:

```text
7 4 3 2 0 0
4 7 2 0 2 0
3 2 7 4 0 2
2 0 4 7 2 3
0 2 0 2 7 4
0 0 2 3 4 7
```

Diagnostics:

- exact pair-matrix match: **false**
- off-diagonal upper-triangle L1 distance: **16**
- generic pair-overlap histogram: `0×6, 1×2, 2×2, 3×2, 4×1, 5×1, 7×1`
- Guidonian pair-overlap histogram: `0×5, 2×5, 3×2, 4×3`
- generic row-neighborhood multiset is not identical to Guidonian;
- it is also not identical to any of the three E3 exact-pair alternatives.

Thus E4 did not win by accidentally reconstructing the E3 Guidonian-equivalent pair matrix. A **different** non-musical dependency topology learned from ZL transferred better to IT2a.

## 9. Scientific interpretation

E4 materially changes the interpretation of the strongest positive evidence previously found under Issue #26.

The sequence of evidence is now:

1. E/E2: a real and independently replicated structural association exists under the six-state slot10 / twenty-class morphology setup;
2. E3: that association does not identify the full Guidonian lattice; it can be reduced to lower-order structural compatibility;
3. E4: even the remaining music-specific interpretation is not diagnostic, because a capacity-matched topology learned solely from non-musical slot/morphology statistics transfers **better** to independent IT2a.

The most parsimonious current explanation is therefore that E/E2 were detecting **stable token-grammar / slot-dependency structure**, not evidence requiring a Guidonian or musical coding system.

What E4 supports:

> Voynich token-internal morphology contains cross-transcription-stable six-state dependency structure. A generic capacity-matched topology learned from that structure in ZL predicts independent IT2a better than the Guidonian comparator used in E/E2.

What E4 does **not** support:

- a decipherment;
- a particular natural language;
- a particular cipher;
- a historical Zattera-like generating algorithm;
- literal `ut/re/mi/fa/sol/la` meanings;
- pitch, melody, rhythm, mode or instrument reconstruction;
- a universal proof that no part of the manuscript can contain music-related material.

For Issue #26 specifically, however, the strongest formerly positive direct-music evidence is now **mechanistically explained by a non-musical competitor** and should no longer be cited as affirmative evidence for a Guidonian/music encoding.

## 10. Consequence for the direct-music research direction

A–D were already negative or non-identifying. E/E2 supplied the only strong positive-looking structural result, E3 removed its Guidonian specificity, and E4 supplies a stronger non-musical explanation.

Therefore the current direct-music program should not proceed to:

- melody extraction;
- pitch-order fitting;
- duration inference;
- literal hexachord naming;
- post-hoc musical decoding.

Future work on music would require a **new independent observable** that makes a prediction not already explained by generic token grammar. The current slot-lattice path has reached a clean falsification boundary.

## 11. First-reveal provenance

- branch: `issue26-music-e4-nonmusic-mechanism`
- draft PR: `#34`
- scientific head: `b7a39e8ba9f2ebd05990244f76cb740458b12118`
- Actions run: `33361426447`
- job: `99393388693`
- artifact: `9746810603`
- artifact ZIP SHA-256: `c85ce2f3cef174fad9e745e9f2181b06f236607e90aa42642b3bc30a524091a9`
- raw JSON SHA-256: `994a386f708965a64f8a1c4bdee49a9276daead628e4c1766f6625eacf79b88a`
- plan SHA-256: `63914e43bb15de69fd5e2de1e1c53894a2ee6a0347d118c724cf1bd424a538ec`
- population amendment SHA-256: `07767817e63555422f95cc8e1221041ab1f479971644bfdacb7a62400fa55e88`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`
- E3 exact-pair catalog SHA-256: `652e23fa08701a87e0aaab961f4a267f2389ccc19769eb31ed05e651c2bedfaf`
- E4 script SHA-256: `dec13766d0647e8f33f13fee9579e4d2f41164bb381a811cc242fd1053854e42`
- ZL3b Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

The PR remains deliberately **unmerged**. Completion of E4 is not authorization to merge while parallel experiments are active.
