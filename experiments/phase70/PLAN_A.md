# Phase 70A — can the frozen A1 formal layer sit over reversible meaningful plaintext?

Status: **FROZEN BEFORE FIRST PHASE70 SCIENTIFIC SCORE**

Date: 2026-08-31

Hypothesis ID: **P70-SC1**

## 1. Purpose

Phase69 established a nontrivial result: meaningful Latin plaintext encoded with a fully reversible homophonic code can acquire a very Voynich-like H62 short-range recurrence profile when recent ciphertext constrains homophone choice. However, the deliberately all-or-nothing Phase69 selector overproduced exposed S2 by about 6.2x and did not generate the paragraph-entry register.

The Phase69 blinded routing decision forbids tuning that selector after seeing the result.

Phase70 therefore does **not** repair Phase69 as an independent cipher hypothesis. It asks a different, narrower compatibility question:

> If the already-frozen A1 entry/local parameters are used as a surface-selection layer, can a semantically constrained, uniquely reversible homophonic encoding of meaningful plaintext still inhabit the same broad structural regime?

This is an **A1-semantic-compatibility construction**. It is allowed to reuse historical A1 training-side information precisely because it is not being presented as an independently discovered cipher explanation.

A positive result would show constructively that the strongest current formal mechanism is compatible with recoverable meaningful plaintext underneath. It would not establish that this composite is historically correct.

## 2. No Phase69 tuning

Phase70 may not choose or fit any new local-strength, history-length, edit-distance, entry-strength or shape-feature parameter from Phase69 outcomes.

Reuse exactly the Phase61C selected fold parameters:

| fold | entry strength | local-family probability |
|---:|---:|---:|
| 0 | 0.5 | 0.2 |
| 1 | 0.5 | 0.2 |
| 2 | 0.5 | 0.3 |
| 3 | 0.5 | 0.3 |
| 4 | 0.5 | 0.2 |

Authority: `experiments/phase61/phase61c_results.json`.

The A1 shape definition and edit1 relation are reused source-identically from `phase61c_joint_model.py`.

## 3. Meaningful plaintext and reversible codebook

Reuse Phase69 without change:

- four equal-weight CREMMA medieval Latin manuscripts: BIS193, CLM13027, Mazarine915, UBL758;
- CREMMA commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- published Naibbe v2 source at `greshko/naibbe-cipher@f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`;
- same 23-letter effective plaintext projection;
- same ambiguity-safe valid ciphertext-candidate catalog;
- same published table/card weights;
- same 17/36 plaintext one-character segmentation probability;
- same 3% adjacent ciphertext-space removal;
- raw selected ciphertext token must decode uniquely to the plaintext unit that produced it.

No codeword is created, deleted or remapped in Phase70.

## 4. Five fold-specific compatibility constructions

A1 is a cross-fitted mechanism. Therefore Phase70 creates one external meaningful-plaintext construction for each of the five already-frozen Voynich physical-leaf folds.

For fold `f`:

1. use only the Phase61/62 Voynich **training leaves** for that fold to learn the historical A1 line-entry shape log-odds;
2. use the historical selected `entry_strength_f` and `local_p_f` from Phase61C;
3. encode the same external Latin panel with those frozen training-side formal parameters;
4. score that fold-specific external construction only against the corresponding held-out Voynich fold target.

No held-out Voynich outcome is used to choose the fold parameters.

## 5. Candidate weighting

For a current plaintext unit, let `C` be its fixed valid Naibbe ciphertext candidates and `w(c)` the published candidate weight.

### SC0 paired semantic control

SC0 samples from `C` proportional only to `w(c)`. It has no A1 entry/local selection.

### SC1 frozen A1-constrained semantic surface

For the first physical line of each plaintext item:

`weight_entry(c) = w(c) * exp(entry_strength_f * shape_log_odds_f(shape(c)))`

where the shape is exactly Phase61C:

`(contains k or t, min(length,8), first glyph, last glyph)`.

For candidate shapes absent from the fold's Voynich training counts, use the same add-one-smoothed log-odds construction as Phase61C. The support includes the fixed SC1 candidate shapes; this changes only a common smoothing denominator and introduces no held-out information.

For all later physical lines in the same plaintext item:

1. draw one Bernoulli activation with probability `local_p_f`;
2. if activated and at least one candidate in C has edit distance exactly 1 from any of the previous ten emitted raw ciphertext tokens, sample from only that local candidate subset proportional to the original `w(c)`;
3. otherwise sample from all C proportional to `w(c)`.

The previous-ten history crosses physical lines inside an item and resets at the next plaintext item. This is a conservative paragraph-local analogue because the external corpus has paragraph/pilcrow items but no defensible mapping to Voynich physical leaves.

No Phase69 all-or-nothing local rule is reused.

## 6. Paired randomness

For fold f, manuscript index m and realization r=0..4:

`base = 7000000 + 100000*f + 100*m + r`

Use:

- segmentation seed = `base`
- SC0 candidate-selection seed = `base + 10000`
- SC1 candidate-selection seed = `base + 20000`
- SC0/SC1 paired output-space seed = `base + 30000`
- SC1 local-activation seed = `base + 40000`

Exactly five realizations per manuscript per fold.

SC0 and SC1 therefore receive identical plaintext segmentation and identical space-removal decisions. No realization is selected by Voynich fit.

## 7. Reversibility and utilization gates

Before structural interpretation:

- SC0 raw decode accuracy must equal 1.000;
- SC1 raw decode accuracy must equal 1.000;
- every SC1 local activation/opportunity/selection event must be internally consistent;
- report entry candidate-weight concentration and local opportunity/activation/hit rates per fold/manuscript/realization.

Any decode failure -> `BLOCKED / REVERSIBILITY FAILURE`.

## 8. Frozen scorecard

Use the exact existing Phase62/63 authorities:

- S1 paragraph-entry projection;
- S2 previous-10 near-family excess;
- S3 aggregate line-position eta2;
- H62-P1 five-bin recurrence-excess profile;
- `D_profile`;
- `|ΔC_short|`.

For each fold, the candidate is the SC0 or SC1 construction generated with that fold's training-side A1 parameters. Compare only to that same fold's held-out Voynich target.

Across folds:

- compute ratio-of-means for S1/S2/S3 using the five fold-specific candidate values and the five held-out targets;
- compute mean/median H62 D and mean C-short error;
- use the same N0/C0 viability comparisons.

A1-R1 is a **reference ceiling/comparator**, not a rival in Phase70, because SC1 explicitly borrows A1's formal parameters.

## 9. Primary compatibility gate

SC1 establishes **constructive semantic compatibility with the broad A1 regime** only if all are true:

1. reversibility gate passes;
2. S1 ratio-of-means in `[0.5,2.0]`;
3. S2 ratio-of-means in `[0.5,2.0]`;
4. S3 ratio-of-means in `[0.5,2.0]`;
5. mean H62 D lower than both N0 and C0;
6. mean H62 C-short error lower than both N0 and C0;
7. at least 3/5 strict fold wins against each N0/C0 baseline on both H62 diagnostics.

This is the same broad structural regime used previously; no easier compatibility threshold is introduced.

## 10. Causal A1-surface check

SC1 must also improve on paired SC0 in the intended directions:

- S1 absolute error to target ratio 1 is lower;
- S2 absolute error to target ratio 1 is lower;
- mean H62 D is lower;
- mean H62 C-short error is lower.

If the broad regime passes without all four paired improvements, classify `COMPATIBILITY PASS BUT A1-SURFACE CAUSALITY UNCLEAR`.

## 11. Classification

### `P70-SC1 REVERSIBLE SEMANTIC COMPATIBILITY DEMONSTRATED`

All primary compatibility and paired causal checks pass.

Allowed interpretation:

> A recoverable meaningful plaintext can be carried through a fixed homophonic code while the already-supported A1 entry/local surface selectors remain sufficient to place the ciphertext in the broad held-out Voynich structural regime.

### `P70-SC1 PARTIAL COMPATIBILITY`

A1-surface causally improves the meaningful-text control but full broad regime fails.

### `P70-SC1 NOT COMPATIBLE UNDER THIS CONSTRUCTION`

No clean causal improvement or major gates fail.

## 12. What Phase70 cannot establish

Even a full pass does not show:

- the Voynich manuscript contains the tested Latin texts;
- Naibbe is the historical cipher;
- A1 is an encryption algorithm;
- the historical author used edit1-aware homophone selection;
- any glyph/string has been translated;
- any illustration has been identified or decoded.

The result would answer only a logical/mechanistic question: whether the formal evidence currently favoring A1 is compatible with an underlying meaningful and exactly recoverable message.
