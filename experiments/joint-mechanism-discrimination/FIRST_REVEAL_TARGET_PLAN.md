# Issue #172 — historical-anchor calibration first-reveal target plan

Status: **FROZEN TARGET DESIGN — NO ISSUE #172 R1–R8 CANDIDATE TARGET SCORE MAY BE COMPUTED FROM THIS COMMIT**

Parent: Issue #172.
Target-plan branch base: post-Stage0 main `53961dbe3a72ebb1c026079987d9a194ad0f0935`.
Stage0 plan blob: `638e212e22aaa313fd85ab80103528ce4cfada9f`.
Stage0 manifest blob: `ce72238107e95f3ed88152a943041d3a827ae945`.
Accepted Stage0 checker blob: `396b0ae7245015bc199f52a139cee20713afb54a`.
Authoritative Stage0 Gate result SHA-256: `76080227ad683d620a4888da05f8aef9a1dba0453125e740279dcbdcf9c28a10`.

This file is the separate target plan required by the Stage0 chronology firewall. It is committed before the Issue #172 target scorer. Historical target results and historical candidate failures already frozen before Issue #172 may be reproduced as authority checks. No new Issue #172 candidate R1–R8 score is licensed by this commit.

## 1. Purpose

The first reveal is a **historical-anchor calibration tournament**. It asks how the frozen #68 anchors fare against the larger post-#88 R1–R10 structural contract. It does not introduce a new mechanism family and does not repair a historical candidate.

The roster remains exactly:

1. `N0` — `CONTROL / NULL`, non-promoting;
2. `C0-4` — `CONTROL / NULL`, exact structured-reversible control, non-promoting;
3. `A1/A1-R1` — `SURFACE GENERATOR ONLY`, promotion-eligible as a surface mechanism only;
4. `Naibbe C1-E0` — `REVERSIBLE TRANSFORM / DECODER CANDIDATE`, promotion-eligible only if R9 also passes;
5. `OBSERVABLE-CORE REPLAY` — target-derived positive control, non-promoting by construction.

No A2, Naibbe locality repair, alternate Naibbe view, replacement codebook, new latent state, selected edge, target-derived seed choice, candidate-specific threshold, or post-reveal representation change is allowed inside this reveal.

## 2. Frozen candidate identities

### A1/A1-R1 primary surface

Use the exact historical Phase62/63 A1 mechanism and the already frozen `rep0` primary seed in each of the five historical physical-leaf folds:

| fold | seed | canonical surface SHA-256 |
|---:|---:|---|
| 0 | 6195200 | `be20405db3d8ee240b70f5b00bbbcba785f2af1b84bdcec849330162870bd142` |
| 1 | 6295200 | `a62c1ed31ef1d2fde42c858e137ffd49e998743b3ddc54ede132ea8c0606890b` |
| 2 | 6395300 | `173b991e9a2374f1c0b545e91b478e6312d0b93cd3340c43c10ad5e807786cf0` |
| 3 | 6495300 | `ec2c06bb6ac3aca33eb09aa7386d8f84ea1b55710c689e0b89d246c8899e0c15` |
| 4 | 6595200 | `c17bbcd9d68718c8823798b27d97db46fb060c635a46f340b748d5d28b1e6927` |

Pooled canonical surface SHA-256: `4ce8eaad33414feb4351825a228a1a865480c31bb41bf9e467c3b76fc6dc6fd3`.

The historical direct SlotParser(min) support `12650/32570 = 0.3883942278170095` is a frozen pre-Issue172 authority fact. It remains an R2 representation failure; no remapping or parser-policy change is licensed.

A1 preserves the historical Voynich held-out item/leaf/line/token-count layout. Those structural identities may be used by scoring adapters exactly where Stage0 already permits layout/scoring metadata. Held-out token identities remain forbidden inputs to generation/fitting.

### Naibbe C1-E0 primary surface

Use pinned public Naibbe commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`, the published primary respaced view, and realization 0 for the four frozen CREMMA manuscripts:

| manuscript | seed | canonical surface SHA-256 |
|---|---:|---|
| BIS193 | 6480000 | `fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805` |
| CLM13027 | 6480100 | `da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77` |
| Mazarine915 | 6480200 | `2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d` |
| UBL758 | 6480300 | `5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89` |

Pooled canonical surface SHA-256: `47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`.

The historical direct SlotParser(min) support `29759/33574 = 0.886370405671055` is frozen. The historical normalized-stream unique decoder closure `1167/1778 = 0.656355455568054` is also frozen and remains an R9 failure. No ambiguity rescue or side-information augmentation is allowed.

Naibbe preserves its source item/line/token hierarchy. It does **not** preserve a Voynich leaf, Currier, section, or paragraph identity. Such target metadata may not be overlaid onto Naibbe merely to make a responsibility evaluable.

## 3. Evaluation folds and causal order

Different responsibilities may use separate frozen arms. They are never pooled into one omnibus score.

### A1

Where a responsibility requires five held-out folds, use the exact five historical physical-leaf folds already inherited by the generated A1 items. Do not regroup leaves.

For causal-order R8, use the corrected Voynich source-order adapter already frozen by Issue #100: raw page-header first occurrence followed by numeric `:pN` paragraph order. Generated A1 items retain the corresponding target-side structural identity. No future token may enter any history feature.

### Naibbe

Historical Phase62/64 responsibilities retain their existing historical source-side/fold mappings unchanged.

For new candidate-surface responsibilities that require a five-fold train/held-out evaluation but do not require Voynich-specific metadata, define one score-free evaluation partition before scoring:

1. take all Naibbe source items in fixed manuscript order `BIS193, CLM13027, Mazarine915, UBL758`;
2. within each manuscript retain the exact parser/source order already emitted by `phase62b_n0.parse_latin_manuscript`;
3. concatenate the item sequence;
4. assign item at zero-based concatenated index `i` to evaluation fold `i mod 5`;
5. every line/token inherits its item fold.

This partition is an evaluation adapter only. Naibbe generation is not refit by these folds. Gate0 must verify nonzero score-free support in all five folds for every newly evaluated arm before the scorer is accepted.

For R8 Naibbe causal order, retain the same fixed manuscript order and native source item order above. Treat each source item as one candidate-native paragraph episode. This is a separate candidate arm; it is not described as Voynich physical page order. The metric remains previous-item/paragraph causal inventory beyond LOCAL40, with no future access.

## 4. R1 — visible-space production boundary

Replay the Phase4A/4B raw/common-EVA production-boundary test without SlotParser filtering.

### Candidate boundary serialization

Every generated visible token boundary in the candidate hierarchy is serialized as one certain boundary equivalent to the primary IVTFF `.` boundary. No uncertain or inferred boundary category exists in the generated candidate surface.

Atomization is frozen to the Phase4 score-free rule: deterministic longest match for `cfh`, `ckh`, `cph`, `cth`, then `ch`, `sh`; remaining lowercase Basic-EVA letters are single atoms. Any exceptional/unresolved material makes the complete affected event ineligible; material may not be deleted and rejoined.

`MID_TOKEN` remains the deterministic `floor(n_atoms/2)` cut with at least two atoms on each side.

P2 remains exactly:

- `OBSERVED = L | R`
- `SHIFT_LEFT = L[:-1] | (L[-1:] + R)`
- `SHIFT_RIGHT = (L + R[:1]) | R[1:]`

with `len(L), len(R) >= 3`, each segment coded from `(BOS,BOS)`, no STOP probability, and the same second-order additive-alpha `0.5` atom model fitted only on training folds.

### R1 hard gate

R1 PASS requires all of:

1. pooled `D_RESET > 0`;
2. `D_RESET > 0` in at least 4/5 held-out folds;
3. `OBSERVED - SHIFT_LEFT < 0` pooled and in at least 4/5 folds;
4. `OBSERVED - SHIFT_RIGHT < 0` pooled and in at least 4/5 folds.

No effect-size ratio to the Voynich target is introduced after reveal. R1 remains a production-boundary responsibility, not a linguistic-word claim.

## 5. R2 — token-internal complete-66 construction

Use the frozen Issue #68 complete-66 candidate-owned residual gate exactly as re-hosted by Stage0.

- SlotParser policy `min`;
- coverage >=0.60;
- >=4 valid reliability folds;
- median reliability >=0.50;
- residual-existence maxT p <=0.01;
- against each frozen target vector ZL3b and IT2a: Pearson >=0.70, Pearson maxT p <=0.01, sign agreement >=50/66, sign maxT p <=0.01.

Historical authority may be carried forward only when candidate identity, scorer identity and target-vector identities match exactly. Otherwise the scorer must abort rather than silently recompute under a modified definition.

Frozen consequences before this new target reveal:

- A1: R2 **FAIL** at the representation gate because primary direct coverage is below 0.60. No Issue172 repair is allowed.
- Naibbe: the unchanged historical #68 complete-66 R1 result is the replay authority for this exact responsibility. Gate0 must verify exact result/provenance identities before it may be carried as the Issue172 R2 disposition.

For a stochastic surface candidate, Stage0's all-three-preregistered-realizations requirement remains controlling. A known primary-realization representation failure is sufficient to fail A1 R2; later realizations cannot rescue it.

## 6. R3 — local near-family / H62 recurrence

Use the exact Phase62/64/Issue81 surface-metric functions and exact edit-1 relation. The target remains held-out Voynich, not the Issue81 X2 candidate.

For the immutable primary candidate surface compute, under the historical arm mapping:

1. aggregate S2 and held-out target S2;
2. H62-P1 `abs_excess_sum` and the corresponding held-out target raw magnitude;
3. only if the raw gate passes, mean `D_profile` and mean `abs_C_short_diff` against the frozen A1-R1 comparator means.

R3 PASS iff:

- S2 ratio in `[0.5, 2.0]`;
- raw H62 magnitude >=0.5 times held-out target raw magnitude;
- mean `D_profile <= 0.7665018009178945`;
- mean `abs_C_short_diff <= 0.11767986235112631`.

Those comparator numbers are the already frozen Issue81 A1-R1 authority, not Issue172 candidate output.

No weighted rescue is permitted.

## 7. R4 — signed paragraph-entry specialization

Use the exact historical S1 projection and candidate/target fold mapping from Phase62/64.

R4 PASS iff:

- aggregate candidate S1 has the same sign as the held-out Voynich target; and
- candidate/target mean ratio is in `[0.5, 2.0]`.

Wrong sign is an automatic failure. Historical exact S1 results may be carried forward after identity checks because the candidate surfaces and metric are unchanged.

## 8. R5 — same-line terminal→initial edge and line-break reset

Use the exact common-Basic-EVA mapping and held-out likelihood definitions from Issues #123/#125/#145.

For each candidate's five-fold surface arm:

1. fit the frozen baseline and same-line previous-terminal edge expert on four training folds only;
2. score the held-out fold;
3. fit/score the frozen beyond-line continuation expert under the same reset semantics.

Because each candidate emits one Basic-EVA surface rather than two transcription readings, it receives **one immutable candidate common-EVA edge result**. That single result is compared to both frozen reading targets; it is never separately tuned to ZL3b and IT2a.

R5 PASS requires:

- candidate common-EVA edge gain positive in >=4/5 folds;
- candidate mean gain lies in `[0.5,2.0]` times `0.1336232955274749` **and** in `[0.5,2.0]` times `0.16184998339508744`;
- beyond-line continuation is not robust positive, i.e. it is not simultaneously mean>0 and positive in >=4/5 folds.

The two target-ratio conditions are conjunctive; no average across readings is allowed.

## 9. R6 — reading-stable common-EVA base edge

R6 is primarily a sharing/access constraint.

A1 and Naibbe each emit one common-EVA candidate surface and contain no Issue172 reading-specific parameterization. Therefore the candidate edge model fitted in R5 is the only candidate shared-edge table permitted. It is compared unchanged to both target-reading reference bands.

R6 PASS requires all of:

1. R10 records `per_reading_tuning=false`;
2. exactly the same candidate parameterization and fitted common-EVA edge table is used for both target-reading comparisons;
3. the shared candidate edge usefulness condition from R5 is positive in >=4/5 folds and falls within both frozen reading ratio bands;
4. no reading-specific candidate table or post-hoc reading repair exists.

A candidate cannot create a second reading-specific table after seeing a mismatch. Since the historical anchors do not contain a reading-specific empirical edge table, no native-over-shared numerical residual is invented for them.

## 10. R7 — Currier-conditioned global next-initial bias

Use the exact #158 gain definition, #161 global-vs-context-interaction factorization, and #167 training-only Jeffreys sparse-support ranking/K ladder `[1,2,4,8,16]`.

### A1

A1 preserves frozen Voynich item/leaf layout. Currier may therefore be attached **for scoring only** from the frozen target-side metadata. Currier is not supplied to A1 generation or parameter fitting.

A1 produces one common-EVA surface. For each Currier regime, its single candidate gain is compared conjunctively against both reading-specific #158 target bands.

R7 PASS for A1 requires:

1. candidate Currier gain positive in >=4/5 folds for A and >=4/5 for B;
2. A-regime mean lies within `[0.5,2.0]` of both `0.0632767341` and `0.0678261662`;
3. B-regime mean lies within `[0.5,2.0]` of both `0.1012061293` and `0.1045681122`;
4. no Currier×previous-terminal interaction is robust under the #161 rule in the candidate arm;
5. under the exact #167 training-only ranking, K=16 suffices and no K<=8 suffices.

### Naibbe

Naibbe has no preserved Voynich Currier identity and no independently declared endogenous regime channel. Its manifest access is `SCORING_ONLY_METADATA`, not permission to fabricate target Currier labels for unrelated source items.

Therefore Naibbe's frozen R7 disposition is **`FAIL_NO_CURRIER_COMPARABLE_CHANNEL`**. No manuscript-ID-as-Currier proxy, target-layout overlay, inferred cluster, or new latent state may be introduced in this reveal. No numerical R7 target score is computed for Naibbe.

This is a substantive missing-responsibility failure, not an excuse to grant new target side information.

## 11. R8 — slower causal-prefix / previous-paragraph inventory

Use the exact LOCAL40 and inventory feature definitions from the corrected Issue #100 authority. Future tokens are forbidden.

A1 uses the corrected frozen Voynich causal order preserved by its target-side layout.

Naibbe uses the candidate-native causal source hierarchy frozen in Section 3. This is a separate surface arm and is reported explicitly as source-native. It may not be relabeled as Voynich physical order.

For either evaluable candidate arm, R8 PASS requires:

- previous-paragraph/item inventory gain beyond LOCAL40 positive in >=4/5 folds;
- mean gain in `[0.02072935, 0.0829174] bit/token`;
- same-line inventory beyond LOCAL40 is not robust positive under the same mean-positive and >=4/5 criterion.

No increase in local Markov order may substitute for the previous-paragraph feature.

## 12. R9 — recoverability

R9 applies as a promotion requirement only to decoder-role candidates.

- A1 is `SURFACE GENERATOR ONLY`; R9 is `NOT_APPLICABLE` and A1 can never be promoted as a decoder.
- Naibbe remains under the exact published decoder and Phase64B normalized recoverable-stream definition. PASS requires 100% unique exact recovery. The frozen authority `1167/1778` is below 100%, so Naibbe R9 is already **FAIL**. No ambiguity-set, source-length, RNG-seed, removed-space-mask, vocabulary, or message-length-scaling side information may rescue it.

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

If a historical parameter count cannot be represented as one scalar count without hiding a table, report the table dimensions/counts explicitly and mark the scalar field accordingly; do not collapse it to an invented one-number penalty.

Automatic R10 failure remains exactly the Stage0 rule: held-out target identity/statistic used for fitting, per-held-out-item fitting, post-reveal view/seed/representation selection, or a new codebook/repair selected from Issue172 performance.

Historical target-aware access remains charged and visible:

- A1: training-side empirical Voynich vocabulary/edit-family/entry-shape dependencies plus true held-out layout counts, fixed before Issue172;
- Naibbe: fixed public Voynich-target-aware codebook/algorithm, fixed before Issue172;
- OBSERVABLE-CORE REPLAY: target-derived positive control and therefore ineligible for promotion.

## 14. Controls

`N0` and `C0-4` remain historical controls and are not forced through incompatible common-EVA target arms. They are never promotion-eligible.

`OBSERVABLE-CORE REPLAY` is used only as a scorer-sensitivity control. It may consume the frozen #88 target-derived structures because that access is its declared purpose. It cannot be used to select thresholds, candidate repairs or mechanism families, and it cannot receive a joint-competitive class.

## 15. Overall classification

R10 failure has priority and yields `OVERFIT / EXCESS-TARGET-ACCESS`.

An authority/support/adapter failure that prevents a predeclared responsibility from being evaluated without changing its definition yields `INVALID / NON-COMPARABLE`. A preregistered structural or missing-channel failure such as A1 R2 coverage or Naibbe R7 does not become INVALID merely because it is fatal to joint promotion.

For a valid promotion-eligible surface mechanism:

- `JOINT-STRUCTURAL COMPETITIVE` iff R1–R8 all PASS and R10 PASS;
- `PARTIAL STRUCTURAL MODEL` iff R10 PASS, the licensed arms remain comparable, at least one of R1–R8 passes, and the R1–R8 conjunction fails;
- `NOT COMPETITIVE` iff R10 PASS but no substantive R1–R8 responsibility passes, or the mechanism is outside the required surface domain without a licensed comparable arm.

A decoder-role candidate additionally requires R9 PASS for decoder promotion. A decoder candidate with structural adequacy but R9 failure is not a decoder closure result.

Controls/nulls are never promoted regardless of their scorer-sensitivity result.

No averaging across R1–R8 is used.

## 16. Gate0 before scorer freeze

After this target-plan commit and before any Issue172 target scorer is committed, a score-free Gate0 must verify at minimum:

1. exact plan/Stage0/manifest blobs and branch ancestry;
2. exact A1 and Naibbe primary surface identities and historical source commits;
3. exact historical R2 carry-forward authorities and R9 authority;
4. deterministic five-fold candidate evaluation assignments;
5. R1 event support is nonzero in all five evaluation folds for both candidate surface arms;
6. R5 common-EVA same-line and beyond-line event support is nonzero in all five folds;
7. A1 scoring-only Currier A/B support is adequate in each historical fold for the frozen #158/#161/#167 adapters;
8. Naibbe receives no Currier mapping and is fixed to `FAIL_NO_CURRIER_COMPARABLE_CHANNEL`;
9. R8 causal order is deterministic, acyclic and future-free under each candidate arm;
10. the exact historical scorer modules for R1–R8 import and pass synthetic/self checks;
11. R10 accounting fields can be populated from candidate authority without target scores;
12. no file, log or artifact contains a new Issue172 candidate R1–R8 scientific score or overall candidate classification.

Gate0 may report counts, hashes, support sizes, fold membership hashes, access metadata and synthetic values. It may not report real-candidate likelihood gains, boundary scores, recurrence scores, S1/S2/H62 scores, edge gains, Currier gains, R8 gains, target correlations, p-values, R1–R8 pass/fail results beyond the already frozen historical/architectural dispositions stated in this plan, or an Issue172 overall class.

If Gate0 fails, repair may address transport, provenance, support implementation or an ambiguity in this already frozen design only. It may not use a candidate scientific score to change the design.

## 17. Chronology firewall from this point

Required order is now:

1. this target plan is committed on the fresh post-Stage0 branch;
2. score-free Gate0 checker is committed and run;
3. exact-head Gate0 passes and its artifact/result digest is frozen;
4. the scientific target scorer is committed **alone** in the next scientific-code commit and its blob is frozen;
5. the target workflow is added in a later commit;
6. exactly one first target reveal is performed;
7. first-reveal raw bytes, SHA-256, head, run/job/artifact IDs and scorer blob are permanently archived before interpretation or source-of-truth updates.

No candidate/scorer threshold or candidate definition may change after step 4 based on target performance.

## 18. Interpretation firewall

This tournament tests whether historical mechanism anchors reproduce a structural production contract. A structural pass does not establish natural-language words, plaintext, semantics, a language/cipher family, authorship, historical mechanism/direction, artificiality/hoax, or decipherment. Exact inverse closure is necessary for decoder promotion and still would not by itself establish historical truth.
