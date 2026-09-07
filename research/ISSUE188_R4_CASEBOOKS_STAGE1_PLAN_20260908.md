# Issue #188 — R4 / Casebooks one-shot Stage1 plan

Date: 2026-09-08  
Parent: Issue #188 / Issue #172 Priority 1  
Base main: `002ec619903dd06415dc37c1859fa01d6d44dfad`  
Status: **FROZEN BEFORE ANY CASEBOOKS S1 SCORE**

## Question

Does the independently selected Casebooks medical/astrological record architecture reproduce the positive signed paragraph-entry direction of the Voynich S1 responsibility under the unchanged historical Phase62B/62C statistic?

This is external mechanism attribution, not semantic decoding or a provenance claim.

## Frozen authorities

### Casebooks

- external repository: `CasebooksProject/casebooks-data`
- commit: `9d42295d72b5ba8889575a32d79311cc72bce73a`
- Gate0 provenance: `experiments/issue188-r4-casebooks/ISSUE188_GATE0_PROVENANCE.md`
- Gate0 authority summary: `experiments/issue188-r4-casebooks/issue188_gate0_authority_summary.json`
- frozen Gate0 extractor/auditor blob: `9792e32a0cb86bd293491701625e8fe2d530aacd`

Gate0 admitted 1,082 structurally eligible paragraphs in 1,050 cases, with 51 source volumes having >=10 eligible paragraphs and both Forman/Napier practices independently supported. No Casebooks S1 was computed in Gate0.

### Historical S1

- implementation: `experiments/phase62/phase62b_n0.py`
- implementation blob: `e0ada366845c7a6c5a5dd75de91fe262b72a94b6`
- historical result: `experiments/phase62/phase62b_n0_results.json`
- historical result blob: `e798b3af89fd029660f9a90750985630c3d283ac`
- ZL3b source blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- ZL3b mirror repository: `matthewdgreen/cipher_benchmark`
- ZL3b mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`

Historical held-out Voynich fold S1 values are frozen as:

`[0.8061532394902311, 1.4591847522080983, 0.20470443416832568, 0.6808459396801555, 1.2290822859476285]`

with mean `0.8759941302988878`.

## Exact S1 replay

For each of the five historical physical-leaf folds:

1. parse ZL3b with historical Phase62B code;
2. use all non-held-out Voynich leaves as training;
3. compute the historical feature standard deviations from eligible training lines;
4. compute historical paragraph contrasts in the eight-dimensional line-feature space;
5. take the mean training contrast and normalize it to the fold direction;
6. verify the held-out Voynich projection reproduces the frozen historical fold S1 value;
7. project Casebooks paragraph contrasts using the same fold `sd` and direction.

No Casebooks value contributes to scaling, direction selection, feature choice, sign choice, or threshold choice.

The eight historical line features and line-0/line-2 minus pseudo-boundary contrast are unchanged. Positive projection is the historical Voynich direction.

## Frozen Casebooks extraction

Stage1 must import the frozen Gate0 extraction module and verify its git blob before use. It may not redefine paragraph boundaries, `<lb/>` lineation, diplomatic branch selection, translation/note exclusions, Letter/Mark tokenization, or structural eligibility.

Each eligible Casebooks paragraph becomes one historical Phase62 `Item`. Gate0 word tokens are converted to historical Phase62 Latin units with `latin_units`; no target-driven segmentation is introduced.

## Primary replication population

The primary source-volume population is fixed by the Gate0 support rule already declared before scoring:

> source volume has at least 10 structurally eligible paragraphs.

There are exactly 51 such volumes. The sorted volume-name list must hash to:

`25cc1b61569c4c5933f5b9293e47477107b163ab80bfae323dc5c55fe211dfcc`

when encoded as sorted names joined by newline with a trailing newline.

All other eligible paragraphs are retained for descriptive pooled and practice/hand summaries but do not enter the equal-volume primary mean.

## Primary statistics

For each primary volume and each of five Voynich folds:

- compute one S1 projection over that volume's eligible paragraphs;
- record volume mean across folds and positive-fold count.

A primary volume is `stable_positive` iff its five-fold mean is >0 and at least 4/5 fold projections are >0. It is `stable_negative` iff its mean is <0 and at most 1/5 fold projections are >0.

Compute equal-volume fold means across the 51 primary volumes, then their five-fold grand mean. No volume is weighted by paragraph count.

Separately compute pooled five-fold S1 for:

- practice `forman`;
- practice `napier`;
- exact hand set `#sforman`;
- exact hand set `#rnapier`;
- all eligible Casebooks paragraphs (descriptive only).

## Frozen external classification

### `VOYNICH_DIRECTION_REPLICATED`

All must hold:

1. equal-volume grand mean > 0;
2. equal-volume fold means are positive in at least 4/5 folds;
3. at least 60% of the 51 primary volumes are `stable_positive` (minimum 31);
4. both `forman` and `napier` practice means are >0;
5. each practice is positive in at least 4/5 folds.

### `WRONG_SIGN`

All must hold:

1. equal-volume grand mean < 0;
2. equal-volume fold means are positive in at most 1/5 folds;
3. at least 60% of the 51 primary volumes are `stable_negative` (minimum 31);
4. both `forman` and `napier` practice means are <0;
5. each practice is positive in at most 1/5 folds.

### `MIXED_OR_UNSTABLE`

Any result satisfying neither complete rule above.

These labels concern direction replication only.

## Magnitude compatibility

Report separately:

`ratio_to_voynich = equal_volume_grand_mean / 0.8759941302988878`

If and only if the direction classification is `VOYNICH_DIRECTION_REPLICATED`, label magnitude `R4_MAGNITUDE_COMPATIBLE` when the ratio lies in the historical `[0.5, 2.0]` band; otherwise label `DIRECTION_ONLY_OUTSIDE_MAGNITUDE_BAND`.

A wrong-sign or mixed result cannot be rescued by magnitude, pooled Casebooks, hand subsets, consultation classes, or post-hoc source selection.

## Secondary reporting

Report, without changing the primary classification:

- exact `#sforman` and `#rnapier` hand summaries;
- all-eligible pooled Casebooks S1;
- distribution of 51 volume means;
- positive/stable-positive/stable-negative volume counts;
- Forman-vs-Napier practice difference as a descriptive contrast only;
- consultation classes only as support labels, not as post-reveal subgroups for rescue.

## Firewall

After the first successful Casebooks S1 reveal:

- no source-volume threshold change;
- no paragraph/token repair;
- no sign reversal;
- no alternate target fold direction;
- no removal of Forman or Napier;
- no consultation-class rescue;
- no nearby S1 offset or feature variant.

A runtime/transport failure before any Casebooks S1 output may be repaired only if the scientific statistic and frozen population remain unchanged and the failure chronology is recorded.
