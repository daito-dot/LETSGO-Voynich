# Issue #191 — Productivity / open-vocabulary Stage 1 first-reveal plan

Date: 2026-09-08  
Issue: #191  
Parent: #172  
Base commit: `8c471182b108396c6405979238316c777e164def`  
Status: **FROZEN BEFORE STAGE-1 SCORER AND FIRST REVEAL**

Stage 0 is licensed by PR #192 / Actions run `34169112886`. This plan resolves the remaining implementation details needed to execute the already-preregistered Issue #191 measures without post-reveal choices.

## Scientific target

Test whether parser-accepted Voynich token forms exhibit stable held-out productivity beyond the frozen exchangeable observed-inventory control, and whether the magnitude is compatible with the already-frozen productive V2 grammar. This is an operational responsibility test, not evidence for an infinite vocabulary, semantics, language, cipher family, authorship, or decipherment.

## Exact source authorities

### ZL3b

Reuse the historical #115 / Phase58D source path exactly:

- repository: `matthewdgreen/cipher_benchmark`
- repository commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`

### IT2a

Reuse the historical #115 / Phase58D authority exactly:

- URL: `https://www.voynich.nu/data/IT2a-n.txt`
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- byte size: `342104`
- line count: `5444`
- first line: `#=IVTFF EvaT 2.0 M 3`

The workflow must fail before scoring on any source mismatch.

## Frozen repository code authorities

In addition to Stage-0 authorities, Stage 1 freezes:

- `experiments/issue191-productivity/issue191_stage0.py` Git blob `3bb6361f721e9cb8069846a79549652596aa287f` for rarefaction, edit-distance, deterministic C2 assignment, seed, annotation, and quantile helper semantics;
- `experiments/phase63/phase63b_common.py` Git blob `99cc6d49669c67432b4798b81c8250a17b3fbb38` for IT2a IVTFF W1 parsing;
- `experiments/occupancy-graph-independent-transcription/source-audit/issue66_source_audit_support_complete.json` Git blob `5de44d197ec60129d3df0bdcc95354b3dd38ba42`, with Phase58D-pinned raw SHA-256 `35ea31eb5d0a1f0484623ee8a29058f1c5bc339117e378b594f26c7c23aee0dc`;
- historical #115 Gate0 workflow Git blob `b715fced15212861618b03fbfe220030e5c5f8de` as source-acquisition precedent only.

All Stage-0 OGH/parser authorities remain frozen, especially `ogh_c.py` blob `742513b5ccfcd088e93b8e9480ac02cbc792e986`, `issue26e_core.py` blob `8bafba7f2bce4cf77c9001c729936c1ce619759b`, and Phase58D blob `161f721a325a53632f3d6d917ec5a27da48e2944`.

## Reading loaders and support gates

### ZL3b

Use `ogh_c.load_corpus(zl_path)` and its frozen `parse_voynich`, token cleaning, `SlotParser(min)`, and physical-leaf folds. For each fold, use only items on the frozen 99-leaf universe. Preserve source traversal order within fold.

Admission support must reproduce parser-accepted held-out counts exactly:

`[4430, 4810, 5516, 5447, 4868]`, total `25071`.

Visible-token support is reported from the same 99-leaf items; rejected tokens are not repaired or scored.

### IT2a

Use `phase63b_common.parse_ivtff(it_path, "IT2a", "W1")`, then the unchanged `SlotParser(min)`. Restrict only by the ZL-defined 99-leaf universe returned by `phase58d_independent_residual.frozen_folds_from_zl(zl_path)`. Do not align IT2a tokens to ZL3b tokens.

Preserve source traversal order within fold. Admission support must reproduce the frozen source-audit values exactly:

- visible/clean tokens: `34411`;
- parser-accepted tokens: `28280`;
- rejected tokens: `6131`;
- fold accepted counts: `[4976, 5416, 6261, 6197, 5430]`.

Any support or fold mismatch makes the run `INVALID` before scientific interpretation.

## Canonical representation

For both readings:

- canonical token type = ordered `((slot,value), ...)` sequence from `SlotParser(min)`;
- V2 integer representation = corresponding OGH-C `UNIT_INDEX[(slot,value)]` sequence;
- canonical surface = concatenation of canonical unit values;
- occupied shape = ordered tuple of occupied slots, equivalent to the 12-bit mask;
- parser-rejected visible tokens are support-only.

## Observed five-fold measures

For each held-out fold:

- training vocabulary = distinct canonical types in the other four physical-leaf folds;
- `NEW_TYPE` iff held-out canonical type is absent from training vocabulary;
- token-mass OOV/new-type rate = unseen held-out token occurrences / held-out parser-accepted token occurrences;
- novel distinct count = distinct held-out canonical types absent from training;
- novel distinct share = novel distinct count / all held-out distinct types.

Five-fold mean OOV is the unweighted arithmetic mean of the five fold OOV rates. Total novel-type incidence is the sum of fold-novel distinct counts; the same type novel in two folds counts twice because the training set differs.

## Rarefaction

Use the Stage-0 exact-without-replacement expectation at fractions `[0.10, 0.25, 0.50, 0.75, 1.00]`, with `n=max(1,floor(q*N))` capped at `N`.

For each fold/checkpoint:

- `all_distinct_expected` sums discovery probabilities over every held-out type;
- `training_unseen_distinct_expected` sums the same discovery probabilities only over types absent from that fold's training vocabulary;
- both use the full held-out parser-accepted token population `N` and the same sample size `n`.

This is an exact order-free expectation, not a Monte-Carlo growth curve.

## Structural novelty annotations

Annotations are computed on distinct fold-novel type incidences. They are non-exclusive. Report counts, shares, and the exact sorted-label intersection signature counts.

Use the five labels frozen in #191. `EDIT1_FAMILY_INNOVATION` is ordinary character-level Levenshtein distance exactly 1 on canonical surface strings. `OTHER_PARSER_ACCEPTED_INNOVATION` is its complement among parser-accepted novel types.

## C1 — closed V+ lookup

Report the deterministic construction fact `new_type_rate = 0` and `novel_distinct_count = 0` for resampling from the training canonical type set. Do not use C1 as a statistical null and do not generate unnecessary random samples.

## C2 — exchangeable finite observed-inventory null

For each reading:

1. concatenate accepted token occurrences as fold 0,1,2,3,4, preserving source order within each fold;
2. preserve that complete global canonical-type multiset and the exact five observed fold token counts;
3. for permutation `i=0..999`, call the Stage-0 deterministic assignment with namespace `Issue191:C2:<reading>:perm:<i>`;
4. assign the first `count[0]` ranked occurrence indices to fold 0, then fold 1, etc., exactly as Stage-0 `c2_fold_assignment` specifies;
5. calculate the unweighted mean five-fold OOV rate and summed fold-novel distinct-type incidence.

One-sided p-values are exactly `(1 + # null >= observed)/1001`. Equality is included in the upper tail.

## C3 — frozen productive V2 control

For each reading and physical fold:

1. fit the unchanged `ogh_c.V2Model` to that fold's actual training canonical integer sequences;
2. for each `rep=0..99`, initialize `numpy.random.default_rng(issue191_stage0.stable_seed("Issue191:C3:<reading>:fold:<f>:rep:<r>"))`;
3. sample exactly the observed held-out parser-accepted token count;
4. convert each sampled V2 integer sequence to its surface with `ogh_c.units_to_string`;
5. **reparse that generated surface through the unchanged `SlotParser(min)` and use the reparsed canonical type for all novelty scoring**. This prevents an alternative latent V2 parse from replacing the canonical identity. Any generated surface that becomes parser-rejected is an `INVALID` protocol failure;
6. score against the actual training vocabulary using the identical novelty/annotation code.

For each reading, replicate index `r` combines the five independently seeded fold realizations with the same `r` into one five-fold Monte-Carlo realization. For each of the 100 combined realizations report:

- unweighted mean five-fold OOV rate;
- summed fold-novel distinct-type incidence;
- known-shape share among all fold-novel distinct-type incidences;
- edit1 share among all fold-novel distinct-type incidences.

For each metric report the 100-realization mean, central 95% empirical interval using Stage-0 linear quantiles, and observed/V2-mean ratio when the denominator is nonzero. The observed structural shares use the same incidence denominator.

The #191 criterion “V2 produces nonzero novelty in every fold” is fixed here as: **every one of the 100 deterministic realizations has at least one generated new-type token in each of the five folds for that reading**. This is intentionally stronger than “at least one realization succeeds.”

## Outcome decision and precedence

First apply validity gates. Any source identity, parser authority, support, fold, deterministic-control, generated-reparse, or numerical-finiteness failure => `INVALID`.

Otherwise:

1. If held-out novelty is absent/collapses under the common parser/folds => `NO_HELDOUT_PRODUCTIVITY`.
2. If the qualitative stable-novelty result differs materially between readings, including any zero-novelty fold in one reading => `READING_UNSTABLE`.
3. If both readings have stable nonzero novelty but either C2 primary p-value fails `<=0.01` in either reading => `PRODUCTIVE_FORMS_PRESENT_BUT_FINITE_NULL_NOT_REJECTED`.
4. If both C2 tests pass in both readings and all five promotion gates in #191 hold => `R11_PRODUCTIVITY_PROMOTED`.

The frozen Issue #191 labels do not define a separate scientific category for the logically possible state “both C2 tests pass, but a C3 promotion condition fails.” If that state occurs, the scorer must not invent a post-hoc label: set `outcome_label = null`, `label_resolution = "NO_FROZEN_LABEL_APPLIES_C3_MISMATCH"`, and `r11_promoted = false`. Such a result may only be resolved by a separately preregistered future analysis; it cannot be repaired in this run.

## Promotion gates implemented literally

`R11_PRODUCTIVITY_PROMOTED` requires:

1. every fold in ZL3b and IT2a has observed OOV > 0;
2. C2 mean-OOV p <= 0.01 in both readings;
3. C2 novel-incidence p <= 0.01 in both readings;
4. frozen strong C3 nonzero-every-realization/every-fold criterion passes in both readings;
5. observed mean OOV / V2 mean OOV lies in `[0.5, 2.0]` in both readings.

No threshold, parser, source, fold, annotation, randomization, backoff, or category may change after the first Stage-1 reveal.

## First-reveal provenance

The first GitHub Actions run after the plan, scorer, and workflow are committed is the scientific first reveal. Record:

- exact prereveal plan/scorer/workflow commits;
- workflow run/job/artifact IDs;
- artifact ZIP SHA-256;
- raw result SHA-256;
- exact outcome label/resolution and gate vector.

A later rerun may be used only as a deterministic reproducibility check; it does not replace the first reveal.