# Issue #172 — historical-anchor calibration first-reveal target plan

Status: **FROZEN TARGET DESIGN — NO ISSUE #172 R1–R8 CANDIDATE TARGET SCORE MAY BE COMPUTED FROM THIS COMMIT**

Parent: Issue #172.
Target-plan branch base: post-Stage0 main `53961dbe3a72ebb1c026079987d9a194ad0f0935`.
Stage0 plan blob: `638e212e22aaa313fd85ab80103528ce4cfada9f`.
Stage0 manifest blob: `ce72238107e95f3ed88152a943041d3a827ae945`.
Accepted Stage0 checker blob: `396b0ae7245015bc199f52a139cee20713afb54a`.
Authoritative Stage0 Gate result SHA-256: `76080227ad683d620a4888da05f8aef9a1dba0453125e740279dcbdcf9c28a10`.

This is the separate target plan required by the frozen Stage0 chronology. Historical target results and historical candidate failures already frozen before Issue #172 may be reproduced as authority checks. No new Issue #172 candidate R1–R8 score is licensed by this commit.

This revision corrects the chronology text of the immediately preceding target-plan commit. The scientific roster, surfaces, hard gates, access rules, and candidate definitions are unchanged. The frozen Stage0 chronology controls: after this plan, the next scientific-code commit is the scorer alone; the workflow is added only afterward; the first target workflow is the single reveal.

## 1. Purpose and roster

The first reveal is a **historical-anchor calibration tournament**. It asks how the frozen #68 anchors fare against the larger post-#88 R1–R10 structural contract. It introduces no new mechanism family and repairs no historical candidate.

Frozen roster:

1. `N0` — `CONTROL / NULL`, non-promoting;
2. `C0-4` — `CONTROL / NULL`, exact structured-reversible control, non-promoting;
3. `A1/A1-R1` — `SURFACE GENERATOR ONLY`, promotion-eligible only as a surface mechanism;
4. `Naibbe C1-E0` — `REVERSIBLE TRANSFORM / DECODER CANDIDATE`, decoder promotion additionally requires R9;
5. `OBSERVABLE-CORE REPLAY` — target-derived positive control, non-promoting by construction.

Forbidden in this reveal: A2, Naibbe locality repair, alternate Naibbe view, replacement codebook, new latent state, selected edge, target-derived seed choice, candidate-specific threshold, post-reveal representation change, or any repair chosen from the Issue #172 failure vector.

## 2. Frozen candidate identities

### A1/A1-R1

Use the exact historical Phase62/63 A1 mechanism and frozen `rep0` primary seed in each physical-leaf fold:

| fold | seed | canonical surface SHA-256 |
|---:|---:|---|
| 0 | 6195200 | `be20405db3d8ee240b70f5b00bbbcba785f2af1b84bdcec849330162870bd142` |
| 1 | 6295200 | `a62c1ed31ef1d2fde42c858e137ffd49e998743b3ddc54ede132ea8c0606890b` |
| 2 | 6395300 | `173b991e9a2374f1c0b545e91b478e6312d0b93cd3340c43c10ad5e807786cf0` |
| 3 | 6495300 | `ec2c06bb6ac3aca33eb09aa7386d8f84ea1b55710c689e0b89d246c8899e0c15` |
| 4 | 6595200 | `c17bbcd9d68718c8823798b27d97db46fb060c635a46f340b748d5d28b1e6927` |

Pooled canonical surface SHA-256: `4ce8eaad33414feb4351825a228a1a865480c31bb41bf9e467c3b76fc6dc6fd3`.

Historical direct SlotParser(min) support is `12650/32570 = 0.3883942278170095`. This is a frozen R2 representation failure. No remapping or parser-policy change is licensed.

A1 preserves the historical Voynich held-out item/leaf/line/token-count layout. Those structural identities may be used only by scoring adapters where Stage0 permits layout/scoring metadata. Held-out token identities remain forbidden inputs to generation or fitting.

### Naibbe C1-E0

Use pinned public Naibbe commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`, the published primary respaced view, and realization 0:

| manuscript | seed | canonical surface SHA-256 |
|---|---:|---|
| BIS193 | 6480000 | `fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805` |
| CLM13027 | 6480100 | `da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77` |
| Mazarine915 | 6480200 | `2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d` |
| UBL758 | 6480300 | `5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89` |

Pooled canonical surface SHA-256: `47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`.

Historical direct SlotParser(min) support is `29759/33574 = 0.886370405671055`. Historical normalized-stream unique decoder closure is `1167/1778 = 0.656355455568054`; this remains a frozen R9 failure. No ambiguity rescue or side-information augmentation is allowed.

Naibbe preserves its source item/line/token hierarchy. It does not preserve a Voynich leaf, Currier, section, paragraph, folio, or scribe identity. Target metadata may not be overlaid onto Naibbe merely to make a responsibility evaluable.

## 3. Evaluation folds and causal order

Responsibilities remain separate arms; they are never pooled into one omnibus score.

### A1

Where five held-out folds are required, use the exact historical physical-leaf folds inherited by generated A1 items. Do not regroup leaves.

For R8 use corrected Issue #100 order: raw page-header first occurrence followed by numeric `:pN` paragraph order. A1 retains the corresponding target-side structural identity. No future token may enter a history feature.

### Naibbe

Historical Phase62/64 responsibilities retain their existing source-side/fold mappings unchanged.

For new candidate-surface responsibilities that require five-fold train/held-out evaluation but do not require Voynich-specific metadata, freeze this evaluation-only partition:

1. manuscript order `BIS193, CLM13027, Mazarine915, UBL758`;
2. within each manuscript, exact parser/source order emitted by `phase62b_n0.parse_latin_manuscript`;
3. concatenate items;
4. zero-based item index `i` goes to fold `i mod 5`;
5. every line/token inherits its item fold.

Naibbe generation is not refit by these evaluation folds.

For R8 Naibbe causal order, retain the same manuscript and native item order. Each source item is one candidate-native paragraph episode. Report this arm explicitly as source-native; do not describe it as Voynich physical order.

## 4. R1 — visible-space production boundary

Replay the Phase4A/4B raw/common-EVA production-boundary test without SlotParser filtering.

Candidate boundaries are serialized as certain visible boundaries equivalent to the primary IVTFF `.` boundary. There is no uncertain/inferred boundary category in generated candidate surfaces.

Atomization is fixed to deterministic longest match `cfh`, `ckh`, `cph`, `cth`, then `ch`, `sh`; remaining lowercase Basic-EVA letters are single atoms. Exceptional/unresolved material makes the complete affected event ineligible; material may not be deleted and rejoined.

`MID_TOKEN` is `floor(n_atoms/2)` with at least two atoms on both sides.

P2 remains:

- `OBSERVED = L | R`
- `SHIFT_LEFT = L[:-1] | (L[-1:] + R)`
- `SHIFT_RIGHT = (L + R[:1]) | R[1:]`

with `len(L),len(R) >= 3`, each segment coded from `(BOS,BOS)`, no STOP probability, and the frozen second-order additive-alpha `0.5` atom model fitted only on training folds.

R1 PASS requires all of:

1. pooled `D_RESET > 0`;
2. `D_RESET > 0` in at least 4/5 held-out folds;
3. `OBSERVED - SHIFT_LEFT < 0` pooled and in at least 4/5 folds;
4. `OBSERVED - SHIFT_RIGHT < 0` pooled and in at least 4/5 folds.

No post-reveal effect-size ratio to the target is added.

## 5. R2 — token-internal complete-66 construction

Use the frozen Issue #68 complete-66 candidate-owned residual gate exactly as re-hosted by Stage0:

- SlotParser policy `min`;
- coverage >=0.60;
- >=4 valid reliability folds;
- median reliability >=0.50;
- residual-existence maxT p <=0.01;
- against each frozen target vector ZL3b and IT2a: Pearson >=0.70, Pearson maxT p <=0.01, sign agreement >=50/66, sign maxT p <=0.01.

Historical authority may be carried forward only when candidate identity, scorer identity, and target-vector identities match exactly. Otherwise abort as non-comparable rather than silently changing the definition.

Frozen pre-Issue172 dispositions:

- A1: R2 `FAIL` at representation gate because direct coverage is below 0.60; no repair.
- Naibbe: unchanged historical #68 complete-66 result is the replay authority after exact identity/provenance verification.

For stochastic surface candidates, Stage0's all-three-preregistered-realizations requirement remains controlling. A known primary-realization representation failure is sufficient to fail A1 R2; later realizations cannot rescue it.

## 6. R3 — local near-family / H62 recurrence

Use exact Phase62/64/Issue81 surface-metric functions and exact edit-1 relation. The target is held-out Voynich, not the Issue81 X2 candidate.

For the immutable primary surface compute:

1. aggregate S2 and held-out target S2;
2. H62-P1 `abs_excess_sum` and held-out target raw magnitude;
3. only if the raw gate passes, mean `D_profile` and mean `abs_C_short_diff` against frozen A1-R1 comparator means.

R3 PASS iff:

- S2 ratio in `[0.5,2.0]`;
- raw H62 magnitude >=0.5 times held-out target raw magnitude;
- mean `D_profile <= 0.7665018009178945`;
- mean `abs_C_short_diff <= 0.11767986235112631`.

No weighted rescue is permitted.

## 7. R4 — signed paragraph-entry specialization

Use exact historical S1 projection and candidate/target fold mapping from Phase62/64.

R4 PASS iff aggregate candidate S1 has the same sign as held-out Voynich and candidate/target mean ratio is in `[0.5,2.0]`. Wrong sign is an automatic failure. Historical exact S1 results may be carried forward only after identity checks.

## 8. R5 — same-line terminal→initial edge and line-break reset

Use exact common-Basic-EVA mapping and held-out likelihood definitions from Issues #123/#125/#145.

For each candidate five-fold surface arm:

1. fit frozen baseline and same-line previous-terminal edge expert on four training folds only;
2. score held-out fold;
3. fit/score frozen beyond-line continuation expert under the same reset semantics.

Each candidate emits one Basic-EVA surface, so it receives one immutable candidate common-EVA edge result. That result is compared to both frozen reading targets and is never separately tuned by reading.

R5 PASS requires:

- edge gain positive in >=4/5 folds;
- candidate mean lies in `[0.5,2.0]` times `0.1336232955274749` and independently in `[0.5,2.0]` times `0.16184998339508744`;
- beyond-line continuation is not robust positive, i.e. not simultaneously mean>0 and positive in >=4/5 folds.

The reading-ratio conditions are conjunctive.

## 9. R6 — reading-stable common-EVA base edge

R6 is primarily a sharing/access constraint. A1 and Naibbe each emit one common-EVA surface and contain no Issue172 reading-specific parameterization. The R5 candidate edge model is therefore the only candidate shared-edge table permitted.

R6 PASS requires:

1. R10 records `per_reading_tuning=false`;
2. exactly the same candidate parameterization and fitted common-EVA edge table is used for both target-reading comparisons;
3. shared candidate edge usefulness from R5 is positive in >=4/5 folds and within both frozen reading ratio bands;
4. no reading-specific candidate table or post-hoc reading repair exists.

No native-over-shared numerical residual is invented for historical anchors that contain no reading-specific empirical edge table.

## 10. R7 — Currier-conditioned global next-initial bias

Use exact #158 gain definition, #161 global-vs-context-interaction factorization, and #167 training-only Jeffreys sparse-support ranking with K ladder `[1,2,4,8,16]`.

### A1

A1 preserves Voynich item/leaf layout. Currier may therefore be attached for scoring only from frozen target-side metadata; Currier is not supplied to A1 generation or fitting.

A1 produces one common-EVA surface. For each Currier regime, its single candidate gain is compared conjunctively against both reading-specific #158 target bands.

R7 PASS for A1 requires:

1. candidate Currier gain positive in >=4/5 folds for A and >=4/5 for B;
2. A mean lies within `[0.5,2.0]` of both `0.0632767341` and `0.0678261662`;
3. B mean lies within `[0.5,2.0]` of both `0.1012061293` and `0.1045681122`;
4. no Currier×previous-terminal interaction is robust under #161;
5. under exact #167 training-only ranking, K=16 suffices and no K<=8 suffices.

### Naibbe

Naibbe has no preserved Voynich Currier identity and no independently declared endogenous regime channel. `SCORING_ONLY_METADATA` is not permission to fabricate target Currier labels for unrelated source items.

Naibbe R7 is therefore frozen as `FAIL_NO_CURRIER_COMPARABLE_CHANNEL`. No manuscript-ID proxy, target-layout overlay, inferred cluster, or new latent state is allowed. No numerical R7 target score is computed for Naibbe.

This is a substantive missing-responsibility failure, not an INVALID adapter failure.

## 11. R8 — slower causal-prefix / previous-paragraph inventory

Use exact LOCAL40 and inventory feature definitions from corrected Issue #100 authority. Future tokens are forbidden.

A1 uses corrected frozen Voynich causal order preserved by target-side layout. Naibbe uses the candidate-native source hierarchy frozen in Section 3 and is reported explicitly as source-native.

For either evaluable candidate arm, R8 PASS requires:

- previous-paragraph/item inventory gain beyond LOCAL40 positive in >=4/5 folds;
- mean gain in `[0.02072935,0.0829174] bit/token`;
- same-line inventory beyond LOCAL40 is not robust positive under the same mean-positive and >=4/5 rule.

No increase in local Markov order may substitute for the previous-paragraph feature.

## 12. R9 — recoverability

R9 is a promotion requirement only for decoder-role candidates.

- A1 is `SURFACE GENERATOR ONLY`; R9 is `NOT_APPLICABLE`, and A1 can never be promoted as a decoder.
- Naibbe remains under exact published decoder and Phase64B normalized recoverable-stream definition. PASS requires 100% unique exact recovery. Frozen authority `1167/1778` is below 100%, so Naibbe R9 is already `FAIL`. No ambiguity-set, source-length, RNG-seed, removed-space-mask, vocabulary, message-length-scaling, or other new side information may rescue it.

## 13. R10 — target-information and complexity accounting

Issue172 fits no new candidate-family parameter. For every candidate report separately:

- `issue172_trainable_scalars` (must be 0 for these historical anchors);
- historical trainable/empirical parameter count reconstructed from pinned code where defined;
- empirical table dimensions and observed context count;
- state count and transition-table dimensions;
- empirical vocabulary dependence;
- target token identity access;
- layout access;
- Currier access;
- section/folio/scribe access;
- target-derived lookup tables/codebooks;
- external corpus/plaintext assumptions;
- inverse side information;
- candidate-specific repair rules;
- per-reading tuning;
- held-out item fitting.

If a historical parameter count cannot be represented as one scalar without hiding a table, report table dimensions/counts explicitly rather than inventing a one-number penalty.

Automatic R10 failure remains the Stage0 rule: held-out target identity/statistic used for fitting, per-held-out-item fitting, post-reveal view/seed/representation selection, or a new codebook/repair selected from Issue172 performance.

Historical target-aware access remains charged and visible:

- A1: training-side empirical Voynich vocabulary/edit-family/entry-shape dependencies plus true held-out layout counts, fixed before Issue172;
- Naibbe: fixed public Voynich-target-aware codebook/algorithm, fixed before Issue172;
- OBSERVABLE-CORE REPLAY: target-derived positive control and ineligible for promotion.

## 14. Controls and overall classification

`N0` and `C0-4` remain historical controls and are not forced through incompatible common-EVA target arms. They are never promotion-eligible.

`OBSERVABLE-CORE REPLAY` is used only as scorer-sensitivity control. It may consume frozen #88 target-derived structures because that is its declared purpose. It cannot select thresholds, candidate repairs, or mechanism families, and cannot receive a joint-competitive class.

R10 failure has priority and yields `OVERFIT / EXCESS-TARGET-ACCESS`.

An authority/support/adapter failure preventing a predeclared responsibility from being evaluated without changing its definition yields `INVALID / NON-COMPARABLE`. A preregistered structural or missing-channel failure such as A1 R2 coverage or Naibbe R7 is a scientific failure, not INVALID.

For a valid promotion-eligible surface mechanism:

- `JOINT-STRUCTURAL COMPETITIVE` iff R1–R8 all PASS and R10 PASS;
- `PARTIAL STRUCTURAL MODEL` iff R10 PASS, licensed arms remain comparable, at least one of R1–R8 passes, and the conjunction fails;
- `NOT COMPETITIVE` iff R10 PASS but no substantive R1–R8 responsibility passes, or the mechanism is outside the required surface domain without a licensed comparable arm.

A decoder-role candidate additionally requires R9 PASS for decoder promotion. A structurally adequate decoder candidate with R9 failure remains a surface/encoding model, not a decipherment result.

No averaging across R1–R8 is used.

## 15. Scorer preflight assertions

The scorer-only commit must contain deterministic score-free assertions that execute before any candidate target score is computed. These assertions are part of the scorer, not a new Gate0 phase or separate checker commit. Failure aborts the single reveal before scientific scoring.

Before scoring, assert at minimum:

1. exact Stage0 plan/manifest/checker authority blobs and branch ancestry;
2. exact target-plan blob loaded by the scorer;
3. exact A1 and Naibbe primary surface identities and historical source commits;
4. exact historical R2 carry-forward and R9 authorities;
5. deterministic five-fold candidate evaluation assignments;
6. nonzero R1 event support in all five evaluation folds for both candidate surface arms;
7. nonzero R5 common-EVA same-line and beyond-line event support in all five folds;
8. A1 scoring-only Currier A/B support sufficient for the frozen #158/#161/#167 adapters;
9. Naibbe has no Currier mapping and remains fixed to `FAIL_NO_CURRIER_COMPARABLE_CHANNEL`;
10. R8 causal order is deterministic, acyclic, and future-free under each candidate arm;
11. exact historical scorer modules import and pass synthetic/self checks;
12. R10 accounting fields are populated from frozen candidate authority before scientific scoring.

These assertions may expose hashes, counts, support sizes, fold membership hashes, access metadata, and synthetic values. They must not be used to modify any scientific threshold, candidate surface, seed, representation, or access rule.

## 16. Chronology firewall

The frozen Stage0 chronology controls. Required order from this revision onward:

1. this corrected target plan is committed on the fresh post-Stage0 branch;
2. the scientific target scorer is committed **alone** in the next scientific-code commit and its blob is frozen;
3. the target workflow is added in a later commit;
4. exactly one first target workflow is performed;
5. first-reveal raw bytes, SHA-256, exact head, run/job/artifact IDs, scorer blob, and workflow head are permanently archived before interpretation or source-of-truth updates.

There is no new post-target-plan Gate0 commit. Stage0 Gate0 is already the accepted authority/preflight gate required by the frozen plan. The scorer's own score-free preflight assertions are runtime abort conditions inside the single reveal, not an additional selection stage.

No candidate/scorer threshold or candidate definition may change after step 2 based on target performance.

## 17. Interpretation firewall

This tournament tests whether historical mechanism anchors reproduce a structural production contract. A structural pass does not establish natural-language words, plaintext, semantics, a language/cipher family, authorship, historical mechanism/direction, artificiality/hoax, or decipherment. Exact inverse closure is necessary for decoder promotion and still would not by itself establish historical truth.
