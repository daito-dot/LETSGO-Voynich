# Issue #172 — Stage 0 authority / compatibility plan

Status: **FROZEN DESIGN — NO ISSUE #172 JOINT CANDIDATE TARGET SCORE MAY BE COMPUTED FROM THIS COMMIT**

Parent: Issue #172.
Base authority: post-#88 closeout main `a1001cefaab1d3f7f1ef808af3f4614fe8bf7f3b`.

## 1. Purpose

Issue #172 is a mechanism-discrimination program. Stage 0 freezes the replay authority, representation boundaries, candidate roles, access accounting, numerical hard gates, and target-free preflight before any new joint reveal.

The tournament does **not** force all historical responsibilities onto one token population. Where historical definitions use different representations or populations, the candidate is passed through a frozen arm-specific adapter and the responsibility remains a separate hard gate. No weighted omnibus score may hide a failed responsibility.

Stage 0 itself may reproduce hashes, supports, source authorities, historical results, and synthetic checks. It may not compute a new candidate's R1–R8 scientific target result.

## 2. Compatibility classes

Every responsibility is assigned one of four frozen replay classes.

- `DIRECT_REPLAY`: exact historical metric and population can be rerun unchanged on a candidate-produced surface or probability law.
- `FROZEN_ADAPTER`: candidate output must be projected through a pre-existing historical adapter/parser; that adapter cannot be changed after candidate output is seen.
- `SEPARATE_ARM`: the responsibility is valid but lives on a distinct reading/population. It remains a hard gate and is not pooled with another arm.
- `ACCESS_CONSTRAINT`: the responsibility is primarily a candidate parameter-sharing, recoverability, or target-access rule rather than a surface statistic.

`NON_COMPOSABLE` is reserved for an authority that cannot be applied without changing its scientific definition. A non-composable responsibility remains visible; it is never silently replaced.

## 3. Frozen authority matrix

### R1 — visible-space production boundary

Authority: Phase 4A/4B, Issues #112/#115, PRs #116/#117.

IT2a authoritative first reveal:

- scientific head `c134560f071a89f77c751878f3f096ce6cb2ac63`;
- run `34024979238`;
- artifact `9986755320`;
- ZIP digest `sha256:9969915558dec9880c5a980f697759cb5357e92cdd5fcfcb693abcb7f4d1c0e4`;
- result JSON SHA-256 `3e9651c733a956b7507a71d169555de1904fe11924fc08b30a3a548b5b29be29`;
- classification `VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a`.

Frozen target facts: ZL3b observed-cut `D_RESET=+8.8119054250 bits/event`; IT2a `+8.092615` with 5/5 positive folds. Frozen one-atom-left/right shifted cuts are negative in both readings with 5/5 directionality.

Representation/population: raw/common EVA boundary events, independent of SlotParser acceptance.

Replay class: `SEPARATE_ARM + DIRECT_REPLAY`.

Hard gate for a candidate surface arm:

1. observed-cut pooled `D_RESET > 0` and positive in >=4/5 folds;
2. left-shift and right-shift observed-minus-shift contrasts have the frozen negative direction and that direction in >=4/5 folds each;
3. the same immutable candidate parameterization is used for ZL3b and IT2a arms where the candidate is reading-comparable.

No claim of natural-language wordhood follows from R1.

### R2 — token-internal construction

Authority: OGH-A/B, PRs #77/#79.

Frozen files:

- `experiments/occupancy-generation-hierarchy/PLAN_B.md`, blob `8768a8a795224fd90dd976435ac0f6699dc106ad`;
- `experiments/occupancy-generation-hierarchy/REPORT_B.md`, blob `ecdbd8f1136b7c7f7aba42c6a5eac7c08df6ba54`;
- first-reveal aggregate SHA-256 `b6bb8c3e124e9adb3d7af38c58d28c4cdc3e404f5059525c4128c9762ef204be`.

Accepted compact comparator: G7A second-order occupied-slot successor grammar, 298 counted probabilities. Frozen result `SUCCESSOR GRAMMAR NEAR-SUFFICIENT`; median `T=0.9481` on the ZL3b skeleton and `0.9617` on the IT2a skeleton, with empirical ceilings `0.9646/0.9695`.

Candidate hard gate is the already-frozen Issue #68 complete-66 topology gate, as re-hosted by Issue #81:

- SlotParser(min) coverage >=0.60;
- >=4 valid reliability folds;
- reliability >=0.50;
- existence maxT p <=0.01;
- against both frozen ZL3b and IT2a complete-66 targets: Pearson >=0.70, maxT p <=0.01, sign agreement >=50/66, sign maxT p <=0.01.

For stochastic surface generators, all three fixed preregistered realizations must pass. G7A/ceiling values remain non-promoting compactness diagnostics; a candidate is not required to equal the empirical inventory ceiling.

Representation/population: 12-slot SlotParser occupancy signatures and five physical-leaf folds.

Replay class: `FROZEN_ADAPTER + SEPARATE_ARM`.

### R3 — local near-family / H62 recurrence

Authority: frozen Phase62/64 definitions, carried unchanged into Issue #81 / PR #82.

Frozen plan: `experiments/cross-token-memory/PLAN_A.md`, blob `3c020804c050fc7aa449d6a1ede091f755929ca3`.

Issue #81 first reveal authority:

- run `33612699253`;
- stage1 SHA-256 `b7c3de603c2bed9a26ae9cc896bea69c88ff0f58bba1bab6b170cbda8032e584`;
- final SHA-256 `98aaabefec0409763f07e41badba3aff10027cc59b68cdcd73c66e2927ebb68e`.

The target is not the X2 candidate result. The target remains the historical S2 and H62-P1 held-out Voynich fingerprint under `phase64b_naibbe.output_metrics / evaluate_aggregate` and the exact edit-1 relation.

Frozen hard gate:

1. aggregate S2 / held-out Voynich S2 in `[0.5,2.0]`;
2. H62 `abs_excess_sum >= 0.5 *` held-out Voynich raw magnitude;
3. only after the raw gate, mean `D_profile` and mean `abs_C_short_diff` are each no worse than frozen A1-R1 means.

Replay class: `FROZEN_ADAPTER + SEPARATE_ARM` on the Phase62/64 ZL3b surface population.

### R4 — signed paragraph-entry specialization

Authority: same frozen Phase62/64 S1 projection and Issue #81 plan above.

Frozen hard gate:

- candidate aggregate S1 has the same sign as held-out Voynich;
- candidate/target mean S1 ratio is in `[0.5,2.0]`.

Wrong sign is an automatic failure and cannot be rescued by another responsibility.

Replay class: `DIRECT_REPLAY + SEPARATE_ARM` on the Phase62/64 ZL3b paragraph/line population.

### R5 — same-line terminal→initial edge and line-break reset

Authority: Issues #123/#125 plus common-representation replication #145.

Issue #123 authority:

- scientific head `87aee03e60e2eab72987eb0cc2bf8c4b992632a0`;
- run `34027611090`;
- artifact `9987613395`;
- result SHA-256 `dfdfca650a15f1d47bd7124898bc8483a139ce47bb17a2c2802a0d2e946dea55`;
- same-line `G_line=+0.0291614 bit/token`, 5/5;
- beyond-line `G_beyond_line=-0.0185292`, 0/5 positive.

Issue #125 authority:

- scientific head `8a3cd11543bc8ccbd7aacfa47486048d1b75cb5f`;
- run `34028083557`;
- artifact `9987750791`;
- result SHA-256 `f329b01a4645b4510bb8b2d5f6a1f194f01395bf707c4870195c3ea6f55f6b45`;
- generic position gain `+0.00889185`, 5/5;
- previous-terminal identity gain `+0.02026956`, 5/5;
- EDGE2 and LINECONT2 token log probabilities are exactly equivalent.

Common-EVA Issue #145 authority:

- scorer blob `ce8a167c607fbcf2807f567439ab6837471f4f07`;
- run `34062199123`;
- artifact `9997826217`;
- ZIP `sha256:d5d4aca2c8620e98753899b7ff675daba9739c19a0e818998fdc8c5da5acc5b8`;
- result SHA `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`;
- ZL3b common-EVA edge gain `+0.1336232955`, 5/5;
- IT2a `+0.1618499834`, 5/5.

Hard gate:

1. common-EVA edge gain is positive in >=4/5 folds in each reading and its mean lies in `[0.5,2.0]` times the corresponding frozen target mean;
2. a beyond-line continuation expert must not show a robust positive gain under the Issue #123 rule (not both mean>0 and >=4/5 positive).

Replay class: `FROZEN_ADAPTER + SEPARATE_ARM`.

### R6 — one reading-stable common-EVA base edge

Authority: Issue #151.

- Gate0 merge `dea1fc30e9e426adaee290bd1cb357478edf96bf`;
- first-reveal merge `5562f966a5469e9da26406c23f47d60c8c2db17f`;
- run `34074437422`;
- scorer blob `2dcd68c8fa68080552a8b90a81e118568b35f8ef`;
- artifact `10001563139`;
- ZIP `sha256:7bc50522e382a5d93a2d60cd773d4c9886c0186891ae30954f594c88dcd87666`;
- result SHA `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`;
- classification `ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`.

Frozen observed shared gains: ZL3b `+0.1356457406`, 5/5; IT2a `+0.1638085813`, 5/5. Neither reading has a robust native-over-shared residual.

R6 is primarily a parameter-sharing/access gate:

1. a candidate may not tune a separate reading-specific repair after seeing either reading;
2. the same immutable candidate parameterization must be used on both arms;
3. shared-edge usefulness must be positive in >=4/5 folds in both readings;
4. if the candidate itself contains an empirical edge table, reading-specific-over-shared residual must not be robust under the #151 rule.

Replay class: `ACCESS_CONSTRAINT + SEPARATE_ARM`.

### R7 — Currier-conditioned global next-initial bias

Authority: Issues #158/#161/#167.

Issue #158:

- Gate0 merge `ca77b7030dec12778ffdeb1d04bee0b30fb00b65`;
- scorer blob `e7a70a10dd7b663f3482993b0adfa8f804816158`;
- run `34076400927`;
- artifact `10002205049`;
- ZIP `sha256:ff54c0e617745cc747db6913a9f56d6f1d09bfa0ce9df7cd8c5e532d08c67462`;
- result SHA `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`;
- classification `CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`.

Frozen mean `G_Currier`: A/ZL3b `+0.0632767341`; A/IT2a `+0.0678261662`; B/ZL3b `+0.1012061293`; B/IT2a `+0.1045681122`.

Issue #161:

- Gate0 merge `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`;
- scorer blob `d24149977770118505f2147c5aa2bb727631906f`;
- run `34077382499`;
- artifact `10002558153`;
- ZIP `sha256:844c990a764a88d22e5b1099031cae68db1fa2e2820ba68d4778c6864240170b`;
- result SHA `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`;
- classification `NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`;
- accepted factorization: one shared terminal→initial base table + Currier-specific global next-initial bias.

Issue #167:

- Gate0 merge `bb56158e907d7253758cc5a0d8bc4dfa2606f1c7`;
- scorer blob `5e67cecc312b431791c6623d1077ac46533fce0a`;
- workflow head `148faf934a917239d2059a8215de48a799b89b48`;
- run `34079999067`;
- artifact `10003436653`;
- ZIP `sha256:f7b698cc44c914e54baa83228823bbb67d6b1b72b759974177e3795baa91a41b`;
- result SHA `a532136b821d3c42f7b340729961da438f1f7cbd9bf20afb73408261d8d7befd`;
- classification `CURRIER OUTCOME BIAS SPARSE SUPPORT: K=16 SUFFICES`.

Hard gate:

1. candidate `G_Currier` is positive in >=4/5 folds in all four reading×Currier cells and mean gain lies in `[0.5,2.0]` times the corresponding frozen #158 mean;
2. no Currier×previous-terminal interaction is robust in the same regime independently in both readings under #161's rule;
3. under the exact #167 training-only Jeffreys ranking and K ladder, K=16 suffices and no K<=8 suffices.

Currier access is separately charged as `ENDOGENOUS_STATE`, `EXOGENOUS_CURRIER_SIDEINFO`, or `SCORING_ONLY_METADATA`. These are not equivalent.

Replay class: `FROZEN_ADAPTER + ACCESS_CONSTRAINT + SEPARATE_ARM`.

### R8 — slower causal-prefix / previous-paragraph inventory

Only corrected source-order authority is valid for exact quantitative use.

Issue #100 correction rule: raw page-header first-occurrence order + numeric `:pN` paragraph order, with unchanged physical-leaf folds.

Corrected Phase 2B authority:

- run `34020290736`;
- scientific head `4bbd0a994dcc7307038b1b16c7726cffca5f3f65`;
- artifact `9985268839`;
- ZIP `sha256:0bb01973eb1d9a278b4160d16cbd9c33f332943c3ec0f0c4bac5737a0dd19920`;
- result SHA `d0ffb426ca268cea3c6c4090aaaac48f260dd4832e8806fbf20419f6f638c014`;
- same-line inventory beyond LOCAL40 `0`, 0/5;
- current-paragraph inventory `+0.0005153`, 4/5 but tiny;
- previous-paragraph inventory `+0.0414587 bit/token`, 5/5;
- previous-paragraph actual-lag residual `+0.0043079`, 5/5.

Phase 2C authority further shows OLDER given PREV1 `+0.0367964`, 5/5, and cross-side inventory given same-side `+0.0237448`, 5/5; these remain diagnostics for Stage 1.

Hard gate uses one deliberately compact replay summary:

1. corrected previous-paragraph inventory gain beyond LOCAL40 is positive in >=4/5 folds;
2. its mean lies in `[0.5,2.0] * 0.0414587`, i.e. `[0.02072935,0.0829174] bit/token`;
3. same-line inventory beyond LOCAL40 must not itself pass the same mean-positive / >=4/5 rule.

This prevents a higher local Markov order from masquerading as the accepted slow-history responsibility.

Replay class: `FROZEN_ADAPTER + SEPARATE_ARM` on corrected ZL3b causal order.

### R9 — reversibility / recoverability

Policy authority: Issue #68 Stage 0 and `experiments/joint-constraint-tournament/PLAN_A.md`.

Candidate role is fixed before scoring as exactly one of:

- `CONTROL / NULL`;
- `SURFACE GENERATOR ONLY`;
- `REVERSIBLE TRANSFORM / DECODER CANDIDATE`.

For a decoder candidate, the inverse target must be declared before target scoring. A primary exact decoder gate requires **100% exact recovery of the declared normalized recoverable stream** under its frozen side-information firewall. If the historical architecture claims exact structured reversibility, exact round-trip equality is required on every frozen audit item.

Ambiguous truth-containing alternatives, unresolved markers, many-to-one reconstruction, or message-length-scaling side information do not count as decoder closure.

A surface generator is exempt from R9 but can never be promoted as a decoder.

Replay class: `ACCESS_CONSTRAINT`.

### R10 — target-information and complexity accounting

Every candidate record must expose, before scoring:

- primary role;
- trainable scalar count;
- empirical table dimensions / observed context count;
- state count and transition-table dimensions;
- empirical vocabulary dependence;
- target token identity access;
- line/paragraph/page layout access;
- Currier/section/folio/scribe metadata access;
- target-derived lookup tables/codebooks;
- external corpus/plaintext assumptions;
- inverse side information;
- candidate-specific repair rules;
- per-reading tuning permission (default `false`);
- held-out item fitting permission (always `false` for a valid candidate).

Automatic `OVERFIT / EXCESS-TARGET-ACCESS` if held-out target identities/statistics are used for fitting, if per-held-out-item parameters are fit, if representation/view/seed is selected after target reveal, or if a new codebook/repair table is selected from Issue #172 performance.

Historical target-aware access fixed before Issue #172 remains visible and charged but is not retroactively called a protocol violation.

Replay class: `ACCESS_CONSTRAINT`.

## 4. Frozen first-tournament roster

The first #172 reveal is a **historical-anchor calibration tournament**. It does not invent a new mechanism family.

1. `N0` — `CONTROL / NULL`; exact historical source-native control; not eligible for joint promotion.
2. `C0-4` — `CONTROL / NULL`; exact structured-reversible control anchor; no boundary side information; not eligible for joint promotion.
3. `A1/A1-R1` — `SURFACE GENERATOR ONLY`; frozen historical mechanism, frozen empirical training dependencies and held-out layout access; no decoder.
4. `Naibbe C1-E0` — `REVERSIBLE TRANSFORM / DECODER CANDIDATE`; pinned public architecture from Issue #68, **without repair**.
5. `OBSERVABLE-CORE REPLAY` — `CONTROL / NULL`; target-derived #88 positive-control pipeline used only to verify scorer sensitivity. Its target-derived tables make it ineligible for mechanism promotion by construction.

Historical frozen failures remain failures. In particular:

- A1 direct 12-slot coverage `0.388394 < 0.60` remains a frozen R2 representation failure unless the exact candidate output under the unchanged adapter independently differs; no remapping is allowed.
- Naibbe historical normalized-stream unique closure `1167/1778 = 0.656355` remains a frozen R9 failure under the unchanged public decoder; no ambiguity/side-information rescue is allowed.

The calibration tournament is valuable even if no historical anchor can be joint-competitive: it establishes the new R1–R10 failure vector and validates the battery before an independently motivated new candidate family enters a later preregistered phase.

## 5. Train/test and reading rules

- Keep historical five physical-leaf folds wherever the historical responsibility uses them.
- Keep CREMMA/source-side folds for a historical decoder audit where that is the frozen authority; do not pretend those are Voynich physical-leaf folds.
- ZL3b and IT2a are readings of the same physical manuscript. Held-out physical leaves must be excluded from both reading training contributions whenever a shared model/table is fitted.
- No target token identity, target statistic, or candidate failure vector may enter hyperparameter/model/representation selection.
- Candidate parameterization is immutable across ZL3b/IT2a unless separate reading parameters were part of the architecture before this tournament; such parameters must be declared and charged, and R6 cannot pass through post-hoc reading repair.
- Currier labels may be used for scoring without being candidate input. If candidate generation/fitting consumes Currier labels, record `EXOGENOUS_CURRIER_SIDEINFO`. If the mechanism emits its own regime state without target Currier input, record `ENDOGENOUS_STATE`.
- No future token may enter R8 causal history.
- No rerolls. Any stochastic candidate uses a frozen seed namespace and fixed realization count declared before target scoring.

## 6. Overall frozen classifications

Access failure has priority.

### `OVERFIT / EXCESS-TARGET-ACCESS`

R10 fails, regardless of structural scores.

### `INVALID / NON-COMPARABLE`

An authority, support, normalization, representation, or adapter failure prevents the predeclared responsibility from being evaluated without changing its definition. A preregistered representation-coverage failure is a scientific responsibility failure, not INVALID.

### `JOINT-STRUCTURAL COMPETITIVE`

For a promotion-eligible surface mechanism: R1–R8 all pass and R10 passes. No averaging or compensation is allowed.

For a decoder-role candidate, promotion additionally requires R9 PASS. A decoder that passes R1–R8 but fails R9 is a structurally adequate surface/encoding model, not a decoder.

### `PARTIAL STRUCTURAL MODEL`

R10 passes, the candidate is valid/comparable on its licensed arms, at least one of R1–R8 passes, and the full R1–R8 conjunction fails.

### `NOT COMPETITIVE`

R10 passes but no substantive structural responsibility passes, or a candidate is structurally outside the required surface domain without a licensed comparable arm.

Controls/nulls are never promoted to `JOINT-STRUCTURAL COMPETITIVE` even if they validate scorer sensitivity.

## 7. Stage-0 target-free preflight requirements

Before a future Issue #172 target workflow exists, a checker must verify at minimum:

1. this plan blob and a machine-readable authority manifest are exact-pinned;
2. every referenced repo file exists and its blob SHA matches the manifest;
3. frozen source hashes / fold hash / corrected-order adapter authority are reproduced;
4. ZL3b/IT2a shared training has zero held-out physical-leaf leakage;
5. the R1 boundary event counts and R2 complete-66 target vector dimensions reproduce historical authority;
6. R3/R4 metric functions and R8 corrected source-order adapter import/execute under synthetic or authority-only inputs;
7. common-EVA inventory is exactly 32 outcomes and #145/#151 clean-run reset semantics are reproduced;
8. Currier A_ONLY/B_ONLY support and #167 K ladder/ranking construction are reproduced without candidate target scoring;
9. historical Naibbe/A1 role/access/recoverability metadata is exact-pinned;
10. no file or log contains new Issue #172 candidate R1–R8 target likelihoods/statistics/classifications.

If any authority check fails, Stage 0 fails. Do not alter the scientific family to make the check pass.

## 8. Chronology firewall

Required order:

1. commit this plan;
2. commit machine-readable authority/access manifest;
3. commit target-free Stage0 checker and workflow;
4. obtain exact-head green Gate0 artifact and pin its digest/result hash;
5. merge/accept Stage0;
6. only then create a fresh post-merge branch for the separate target plan;
7. commit target plan before scorer;
8. commit scorer alone and freeze blob;
9. add workflow in a later commit;
10. first target reveal once.

No new Issue #172 candidate target score is licensed before step 5.

## 9. Interpretation firewall

Structural competition does not establish natural-language word boundaries, plaintext, semantics, language/cipher family, authorship, historical mechanism/direction, artificiality/hoax, or decipherment. Exact inverse closure is necessary for decoder promotion but is not sufficient to establish historical truth.