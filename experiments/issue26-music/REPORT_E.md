# Issue #26 experiment E — Guidonian slot-lattice first reveal

Status: **NARROW GUIDONIAN SLOT-COMPATIBILITY**

This is the first positive direct-music-family result in Issue #26. The interpretation boundary is deliberately narrow: it is a held-out structural compatibility result for one historically constrained 20×6 coding lattice, **not** evidence that the manuscript has been musically decoded.

## Frozen question

Can the independently selected six-state Zattera slot-10 channel (`EMPTY,d,l,r,m,n`), together with a sequence-blind 20-cluster representation of the other 11 slots, predict the specific allowed-pair lattice of the Guidonian gamut on held-out physical leaves better than equally sparse non-Guidonian lattices receiving the same training optimization freedom?

The frozen target has:

- 20 gamut loci;
- 6 voces `ut re mi fa sol la`;
- 42 allowed locus×vox cells;
- the exact Guidonian row-degree profile;
- column degree 7 for every vox.

For every physical-leaf fold, both Guidonian and null lattices were allowed to optimize all `6!` slot-state↔vox bijections plus the optimal 20-cluster↔20-locus assignment **on training leaves only**. Each of 100 null lattices preserved every row degree and every column degree exactly.

## Parser provenance

The historical Phase01–02 parser source was not recovered from current public GitHub. `SLOT_PROVENANCE_E.md` therefore froze a fresh implementation from the independently published Zattera 12-position inventory and a validation gate against preserved legacy signatures.

A dry-run before the executable was committed found one provenance-table error: the legacy `dain/daiin = 0-8-9-10` evidence was earliest-valid only, while the table-implied latest-valid parse is `7-8-9-10`. The correction commit `fd2f26a0ab013e1371450773df343453653e2f74` predates both executable files and any scientific computation. The workflow verifies this ordering.

All corrected parser assertions passed.

## Primary result — earliest-valid (`min`) parser

Mean held-out single-unit parse coverage: **0.769423**.

| quantity | result |
|---|---:|
| mean Guidonian held-out accuracy | **0.850966** |
| median paired-null mean accuracy | 0.841250 |
| 95th percentile paired-null mean | 0.846882 |
| Guidonian advantage over null median | **+0.009717** |
| global empirical p | **0.009901** |
| folds above own null median | **5 / 5** |

Per-fold results:

| fold | Guidonian A | null median | null q95 | fold p |
|---:|---:|---:|---:|---:|
| 0 | 0.824605 | 0.813093 | 0.829582 | 0.108911 |
| 1 | 0.855094 | 0.846778 | 0.859262 | 0.158416 |
| 2 | 0.832306 | 0.821338 | 0.834164 | 0.099010 |
| 3 | 0.863411 | 0.850009 | 0.862943 | 0.059406 |
| 4 | 0.879417 | 0.872638 | 0.884614 | 0.118812 |

No individual min-policy fold is conventionally significant on its own. The frozen global result is driven by a **small advantage in the same direction on all five physically separated folds**, not by one extreme fold.

Among the 100 paired global null replicates, none reached the Guidonian mean; the finite Monte-Carlo p is therefore `(0+1)/(100+1)=0.009901`. The observed Guidonian mean also exceeds the 95th percentile of the paired-null means.

## Predeclared sensitivity — latest-valid (`max`) parser

The parseable-token population is the same; ambiguous tokens receive their latest-valid slot assignment.

| quantity | result |
|---|---:|
| mean parse coverage | 0.769423 |
| mean Guidonian held-out accuracy | **0.843903** |
| median paired-null mean | 0.818613 |
| 95th percentile paired-null mean | 0.826641 |
| Guidonian advantage | **+0.025290** |
| global empirical p | **0.009901** |
| folds above own null median | **5 / 5** |

Every max-policy fold also passes its own 100-null comparison at `p <= 0.039604`:

`0.029703 / 0.029703 / 0.009901 / 0.029703 / 0.039604`.

Thus every preregistered primary and robustness condition passes.

## Frozen classification

- primary mean coverage >= 0.60: **pass**
- primary global p <= 0.05: **pass**
- primary null-median wins >= 4/5: **pass, 5/5**
- max sensitivity same-sign advantage: **pass**
- max sensitivity p <= 0.10: **pass**

Frozen verdict: **`NARROW GUIDONIAN SLOT-COMPATIBILITY`**.

## Post-reveal mapping-stability diagnostic — non-gating

The fitted slot10-state→vox map was not required to be the same across folds in the frozen test; each mapping was learned from training leaves only. Its stability is therefore a useful diagnostic, not part of the confirmatory evidence.

For the primary min parser, the six-state map forms three fold patterns: one shared by folds 0/4, one by 1/2, and a third in fold 3. It is **not globally stable**.

For the max-parser sensitivity, one slot10→vox map recurs unchanged in **4/5 folds**:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`

Fold 1 differs. This 4/5 recurrence is potentially interesting but was discovered after reveal and cannot upgrade the frozen claim. It instead supplies an explicit prediction for a later independent-transcription replication if such a replication is frozen before inspection.

## Interpretation

Retain only:

> Under a frozen fresh implementation of the published 12-position Zattera grammar, the unique six-state slot-10 factor plus a sequence-blind 20-class representation of the remaining token morphology generalizes to the specific Guidonian 20-locus×6-vox admissibility lattice better than 100 degree-matched non-Guidonian lattices under identical training mapping freedom. The effect is small under the primary parse policy but consistent across all five held-out physical-leaf folds and stronger under the predeclared latest-valid sensitivity.

This is substantially more specific than the earlier generic “music-like sequence” tests because the six-state channel, twenty-state counterpart and allowed-pair matrix are all externally constrained.

It does **not** establish:

- that slot 10 literally names `ut/re/mi/fa/sol/la`;
- that the 20 morphology classes are notes in pitch order;
- that Voynich lines are melodies;
- duration, rhythm, mode, instrument or polyphony;
- plaintext or decipherment;
- historical use of the Guidonian hand by the manuscript author.

## Why immediate replication is required

The primary effect is only about **+0.97 percentage point** over the matched-null median. Therefore the next high-information checks are not melody extraction. They are:

1. increase degree-matched Monte-Carlo resolution without changing the model;
2. reproduce the frozen architecture on the independently maintained IT2a/EvaT transcription;
3. test whether the post-reveal 4/5 max-parser slot10→vox mapping predicts IT rather than being refit freely;
4. only if those survive, test sequence-level Guidonian constraints such as mutation/hexachord transitions.

## First-reveal provenance

- PR: `#31`
- scientific head: `86bd3336cd7241127f99e75584ba0e75e15355f9`
- Actions run: `33355884461`
- job: `99377833117`
- artifact: `9745117683`
- artifact ZIP SHA-256: `69c8660d27c2aa039a20e7d1b15b307719caacbe6e1f39e91eb5eafe892d9c12`
- raw JSON SHA-256: `b0bb3b7cf77ca09955ac99fc41ed95d9aee406962f5973396568f3d7554eef9d`
- slot provenance SHA-256: `aebbd7b42736794229bd40e7b1e4012f044486221efeb8d5833e7e6e93cc5f51`
- plan SHA-256: `a9ccf4c993ca0ca5e5b4f64ca0aac1f5d71c8a6d370dedcbfde00154e492726d`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`
- executable SHA-256: `51bbd8026b78772a4aeed7981bf56ff7385bd36d1e21ad7b2bec4c98d03f18a0`
