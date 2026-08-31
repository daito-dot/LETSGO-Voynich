# Issue #26E3 — structured-null specificity challenge

Status: **PAIR-GEOMETRY SUFFICIENT / GUIDONIAN NOT SPECIFIC**

E3 is a successful falsification of the stronger interpretation of E/E2.

The E2-C fixed-map signal replays exactly, and it remains extremely unusual relative to 100 structured nulls that match the Guidonian row-degree, column-degree and pair-overlap histogram. However, once the **entire labeled pairwise column-intersection matrix** is held exactly equal to Guidonian, two of the three possible non-Guidonian higher-order row-neighborhood alternatives match or beat Guidonian on held-out IT2a.

Therefore the current evidence does **not** identify the full Guidonian 20×6 admissibility lattice. The replicated signal is explainable at the level of its second-order six-state pair geometry.

## 1. Frozen question

Does the prospective E2 fixed map identify the specific Guidonian row-neighborhood multiset, or can non-musical six-column lattices with the same low-order overlap geometry reproduce the held-out result?

E3 changed no Voynich representation or state mapping:

- IT2a source and exact SHA unchanged;
- max/latest-valid Zattera parser unchanged;
- same five physical-leaf folds;
- same sequence-blind k=20 morphology clustering;
- same fixed six-state map `EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`;
- only cluster→row assignment fits on training leaves;
- held-out score remains allowed-occurrence accuracy.

The only substantive change from E2-C is a stronger family of null lattices frozen before the E3 scorer.

## 2. E2-C replay gate

E3 hard-asserted the previously revealed E2-C Guidonian result before accepting any new null comparison.

Replay:

- mean IT parse coverage: **0.8213154353**
- mean Guidonian held-out accuracy: **0.8337140490**
- fold accuracies: `0.835597 / 0.802178 / 0.870536 / 0.848460 / 0.811799`

All values match E2-C exactly within the frozen tolerance.

## 3. E3-B first — pair-overlap-histogram-matched structured null

The frozen 100-matrix catalog preserves much more than the earlier degree-only rewires:

- 20 rows / six columns / 42 cells;
- row-degree multiset `1×4, 2×10, 3×6`;
- every column degree exactly 7;
- pair-overlap histogram exactly `0×5, 2×5, 3×2, 4×3`;
- 100 distinct non-Guidonian row-neighborhood multisets;
- labeled pair-overlap pattern and higher-order neighborhoods differ from Guidonian.

The E2-C signal still dominates this family.

| quantity | result |
|---|---:|
| Guidonian mean A | **0.833714** |
| structured-null mean median | 0.723859 |
| structured-null mean q95 | 0.803825 |
| largest null mean | 0.827282 |
| Guidonian advantage over median | **+0.109855** |
| global empirical p | **0.009901** |
| fold median wins | **5/5** |

Per-fold Guidonian / structured-median / p:

- fold0: `0.835597 / 0.724830 / 0.009901`
- fold1: `0.802178 / 0.688503 / 0.019802`
- fold2: `0.870536 / 0.770568 / 0.009901`
- fold3: `0.848460 / 0.721022 / 0.019802`
- fold4: `0.811799 / 0.711266 / 0.039604`

**E3-B: PASS.**

This confirms that merely matching sparsity, degree profile and the distribution of pair-overlap strengths is not sufficient. Which six-state pairs receive which overlaps matters strongly.

## 4. E3-A — exact pair-matrix exhaustive tournament

E3-A is the decisive test.

Candidates were required to have:

- the same row-degree multiset;
- all six column degrees = 7;
- the **entire labeled 6×6 pairwise column intersection matrix exactly equal to Guidonian**.

A complete pre-science combinatorial enumeration found exactly four feasible row-neighborhood multisets: Guidonian plus three non-Guidonian alternatives. Thus this is an exhaustive tournament, not a sample of convenient alternatives.

Guidonian mean held-out accuracy:

**0.8337140490**

### Alternative 0

- mean A: **0.8340565063**
- Guidonian minus alternative: **−0.0003424573**
- Guidonian strict fold wins: **2/5**
- fold accuracies: `0.843987 / 0.807714 / 0.859853 / 0.842334 / 0.816394`

Alternative 0 slightly exceeds Guidonian in mean held-out accuracy.

### Alternative 1

- mean A: `0.8312548138`
- Guidonian minus alternative: `+0.0024592352`
- Guidonian strict fold wins: **3/5**
- fold accuracies: `0.838993 / 0.798487 / 0.860491 / 0.837498 / 0.820805`

Guidonian beats alternative 1 under the frozen criterion.

### Alternative 2

- mean A: **0.8354839822**
- Guidonian minus alternative: **−0.0017699332**
- Guidonian strict fold wins: **1/5**
- fold accuracies: `0.841191 / 0.805499 / 0.865115 / 0.849589 / 0.816026`

Alternative 2 exceeds Guidonian by about 0.177 percentage point and beats it in 4/5 folds.

**E3-A: FAIL.**

Because two exact-second-order alternatives equal or outperform Guidonian, no held-out preference for the Guidonian triple/higher-order row-neighborhood configuration remains after second-order column geometry is fixed.

## 5. Frozen classification

- E3-A exact pair-matrix specificity: **fail**
- E3-B overlap-histogram structured null: **pass**

Frozen classification:

**`PAIR-GEOMETRY SUFFICIENT / GUIDONIAN NOT SPECIFIC`**

Under the preregistration, E3-A failure controls the interpretation regardless of E3-B.

## 6. What survives from E/E2

E3 does not erase the replicated numerical facts from E/E2. It localizes them.

The strongest defensible surviving statement is now:

> A six-state factor in the Zattera token grammar, under a state correspondence frozen in ZL and transferred prospectively to IT2a, shows a highly reproducible compatibility with the **labeled second-order pair-overlap geometry** carried by the Guidonian six-vox lattice. That signal is much stronger than degree- or overlap-histogram-matched controls, but it does not distinguish the actual Guidonian higher-order 20-locus neighborhood system from all non-Guidonian systems having the same pairwise column intersections.

This is no longer sufficient to call the result “Guidonian slot compatibility” without qualification.

## 7. Consequence for the music hypothesis

This result **downgrades the music-specific interpretation sharply**.

The full Guidonian gamut is not identified. The surviving object is a six-state pairwise relationship matrix. Such a matrix could arise from a non-musical formal grammar, especially because Voynich tokens already exhibit constrained slot interactions.

Therefore:

- do not proceed to melody extraction;
- do not assign actual pitches to the 20 morphology clusters;
- do not interpret the fixed six state names literally as `ut/re/mi/fa/sol/la`;
- do not treat E2-C as a musical decoding success.

The next scientific question is instead whether the surviving six-state pair geometry is itself unusual relative to **non-musical slot grammars / generic six-category dependency systems**, or is a natural consequence of the Zattera morphology.

That next mechanism audit should be independent of music semantics. Only if the pair geometry remains distinctive after such controls would returning to music-specific sequence predictions be justified.

## 8. First-reveal provenance

- PR: `#33`
- scientific head: `785f71f97f6f255494c3883d15b97d0d222f68d5`
- Actions run: `33357288045`
- job: `99381761940`
- artifact: `9745529873`
- artifact ZIP SHA-256: `fb05e834ddb1dc7e8cb311a4a005d753d8ae6b4311882d8e5e60fc4a2c7d795e`
- raw JSON SHA-256: `dbc0dd982ec2cd8bdc15ac70f88b40e91b0f6e788edb4e44c20d812a607ef7c0`
- plan SHA-256: `a3705354bc1955f9d33cd443313efb7ef45a46b6542882a506064feace99b409`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`
- structured catalog SHA-256: `3ded6745d58701d1a1c38a38f268c57396afffbbbf0a681ec9b16bb09f1e47bd`
- exact-pair catalog SHA-256: `652e23fa08701a87e0aaab961f4a267f2389ccc19769eb31ed05e651c2bedfaf`
- E3 scorer SHA-256: `48b9a3b620932a5b39a77f170c5d6307377fdc3624a88b49aba4efdc6fa2cfa3`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
