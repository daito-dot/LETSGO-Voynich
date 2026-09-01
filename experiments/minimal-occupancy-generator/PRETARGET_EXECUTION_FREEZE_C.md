# Issue #75 Phase C — recovered pretarget execution freeze

Date: 2026-09-01  
Status: **PRETARGET EXECUTION FROZEN / FIRST M3 TARGET ACCESS NOT YET PERFORMED**

## Scientific purpose

This document closes the recovered target-blind preparation chain for the preregistered `M3-KRS-CHAIN` model. After this commit, no Phase-C model, scorer, aggregation law, generated population, null construction, target statistic, or decision threshold may change before first reveal.

## Phase-B license authority

M3 is licensed only by the permanently recovered Phase-B result:

- Phase-B first reveal run: `33504481315` — success
- scientific head: `693f627910f5775406da410ec4d7157a161021e4`
- Phase-B aggregate SHA-256: `f0c5e9e210f3cf9bd0fa9c9b818c0ee61649a906b051998346db1583c60fb566`
- classification: `M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED`
- `gap_M2=-0.6777560206049392`
- no-material-loss: `false`

## Prospective Phase-C plan authority

The exact M3 plan text was versioned before executable implementation inside the conditional preregistration workflow at:

- normative preregistration source commit: `837d9b904a6fa75e5e50554477a3277c527c4a94`

The generator was added in its immediate child:

- generator commit: `32d2f8c99a9c9cf608af8b393f597412556c6f5d`

The original preregistration run failed at the then-broken Phase-B license gate and did not materialize `PLAN_C.md`. After Phase B was recovered, the original historical preregistration job was rerun without changing its workflow definition. It materialized the already-versioned plan text at:

- materialized `PLAN_C.md` commit: `615e60debc9ba9da024b91c86ae717b9ad03e460`

The recovered C0 workflow verified byte-for-byte equality between current `PLAN_C.md` and the plan extracted from the preimplementation commit `837d9b...`.

## Frozen executable authorities

- generator implementation: `32d2f8c99a9c9cf608af8b393f597412556c6f5d`
- candidate-owned R1 scorer: `77bcf3b8c4a56ac55eba8bffa775998f39a412d8`
- Phase-C aggregation law: `ad92c4f08d27da38157dc1bc581328416115a48f`
- target reference loader remains `experiments/joint-constraint-tournament/target68.py`, frozen blob expected by first reveal: `e94a24fbdfbb922099407313f23a1b87859130b6`
- Phase-A positive-control aggregate SHA-256: `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

No target-edge loss, selected nonadjacent edge, or complete-signature lookup parameter is permitted.

## Frozen M3 model

`M3-KRS-CHAIN` retains the training-only empirical `(K,R,S)` descriptor distribution and models the conditional occupancy pattern with:

`P(x | K,R,S) ∝ exp(Σ h_s x_s + Σ J_s x_s x_{s+1})`

with:

- 11 free unary position parameters;
- 10 free nearest-neighbor occupied-pair parameters;
- 21 free continuous parameters per cross-fit training split;
- explicit nonadjacent pair interaction parameters: `0`;
- empirical complete-signature-specific parameters: `0`.

## C0 generated-population authority

Recovered target-blind C0:

- workflow run: `33508138601` — success
- generation head: `1b3d1208e2a8d87649aa0489822f0ed6e6399dcd`
- permanent C0 repository commit: `cf2c1905a6255db41b3a41aa6ab2002566095dd7`
- C0 metadata commit: `38fe7a05f5b16a6acc59c1df170a6481c093d26a`
- generator authority SHA-256: `1ff4469f57a84093b8c5d6463bb276a8de6fc108eed666bf63c9c7dacbf622a6`
- artifact ID: `9800460088`
- artifact digest: `sha256:27cb7c4081f654a2d6e51e3fca00b88b9483e5b050a373f0134b29ea6424d4cc`
- cases: `31/31`
- drops: `0`
- rerolls: `0`
- maximum reported fit error: `1.3403167464787202e-12`
- target loaded: `false`
- pair Q computed: `false`
- residual Z computed: `false`
- target correlation computed: `false`

## Exact-replay preflight authority

Recovered boundary preflight:

- workflow run: `33508315635` — success
- head: `35a99c2f47cb5eef0e9c0c997004c435d85ce471`
- reps: `0` and `30`
- both exact C0 occupancy SHA replays: `true`
- target loaded: `false`

Artifacts:

- rep0 ID `9800524703`, digest `sha256:3d41f5d67e71b3bbfac24cb7c06ec92b0eea1bb81de4182e8ad70773d51b0c7c`
- rep30 ID `9800525631`, digest `sha256:a7d8f152a221003ec3df93a19360df66bfba06a29d2486b5a71569f7193e6e48`

## Candidate-owned null smoke authority

Recovered rep0 smoke:

- workflow run: `33508396294` — success
- head: `3f886b35a27c21e544e7be1960054bbbae7e9bf0`
- artifact ID: `9800602822`
- artifact digest: `sha256:cc41b89b27022e97589d4d15ae7fad61ebec289e5031647920867702607e8463`
- `N_ref=1000`
- `N_test=1000`
- candidate Q computed: `true`
- candidate residual Z computed: `true`
- Issue58C/ZL3b target vector loaded: `false`
- Issue58D/IT2a target vector loaded: `false`
- target correlation computed: `false`
- `T` computed: `false`

Target-blind implementation diagnostics only:

- `E=3.1410916241254005`
- `p_exist=0.000999000999000999`
- `W=0.9452895476573187`

These values are not model-selection or tuning criteria.

## Prior failed Phase-C attempts

The premature historical Phase-C runs are non-authoritative. In particular:

- original C0 run `33506051989` failed at license/chronology verification before corpus generation;
- original first-reveal run `33506588721` failed in authorization;
- its `score` job was skipped;
- its `aggregate` job was skipped.

Therefore the number of Phase-C M3 target scores observed before this freeze is exactly `0`.

## Frozen target comparison and decision

For each rep `r=0..30`:

- compute the unchanged candidate-owned complete 66-edge residual vector;
- compare separately against frozen ZL3b and IT2a target vectors;
- report `R_ZL3b`, `R_IT2a`, sign agreement, E, p_exist, W;
- define `T[r]=min(R_ZL3b,R_IT2a)`;
- reuse the exact 31 paired Phase-A `T_plus_center[r]` values;
- define `D_M3[r]=T_M3[r]-T_plus_center[r]`;
- define `gap_M3=median(D_M3)`.

Primary tolerance is unchanged:

`delta_plus_q95 = 0.009768313008182594`

Decision:

- if `gap_M3 >= -0.009768313008182594`: `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_SUFFICIENT` and stop the R1 complexity ladder;
- otherwise: `M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED` and only a separately preregistered next frontier is licensed.

No case may be dropped or rerolled. ZL3b and IT2a may not be averaged. No post-reveal model modification is permitted.

## Authorization

A new recovered first-reveal workflow may now be committed. Its commit becomes the scientific first-reveal head. Target access is authorized only after that workflow re-verifies every authority above.
