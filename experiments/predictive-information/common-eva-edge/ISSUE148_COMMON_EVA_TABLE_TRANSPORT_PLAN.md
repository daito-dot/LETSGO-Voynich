# Issue #148 — bidirectional common-EVA literal edge-table transport

Date: 2026-09-07
Status: **FROZEN BEFORE ANY ISSUE #148 CROSS-TABLE TARGET SCORE**
Parent: Issue #88
Entry authority: Issue #145 / PR #147

## Question

If the BODY first-atom conditional table `P(next_initial_atom | previous_terminal_atom)` is learned from one transcription lineage on four physical-leaf folds, does that exact source table improve prediction in the other lineage on the untouched fifth fold when every non-edge factor remains target-native?

This is a literal predictive-table / learned-strength transport test. It does not test historical direction, semantics, plaintext or authorship.

## 1. Frozen entry authority

Issue #145 established under one common target-blind representation:

- ZL3b mean `G_common = +0.1336232955274749 bit/token`, positive 5/5;
- IT2a mean `G_common = +0.16184998339508744 bit/token`, positive 5/5;
- joint class `COMMON-EVA EDGE ROBUST IN BOTH READINGS`.

Authority:

- Issue #145 Gate0 merge `692b141ac8457f4026ae482a4a8ae79a4f0fef50`;
- Gate0 result SHA-256 `563573e81c931133aaa9877bcf79a57a40ebb3e2a946183cac3f6e922d65eb48`;
- Gate0 script blob `80585066e746f42ac10554aaaeece793682a0b84`;
- Gate0 provenance blob `e98d2fffac1d2500623a7f8660343ead67218332`;
- Issue #145 scientific scorer blob `ce8a167c607fbcf2807f567439ab6837471f4f07`;
- Issue #145 first-reveal provenance blob `1cbb43381c57726ecc3a5b5dc5e8efc0c7b732f6`;
- first-reveal result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`;
- PR #147 merge `26ccaa527fc4e1026d031e4773b819137a678f69`.

## 2. Frozen representation / folds / population

Reuse Issue #145 without any change:

- exact ZL3b and Takahashi/IT2a source authorities;
- exact Phase4A/4B Basic-EVA representation;
- literal IVTFF `.` certain-space segmentation;
- 25 Basic-EVA single atoms + `cfh, ckh, cph, cth, ch, sh`;
- 31 common atom outcomes + `END_TOKEN`, `V=32`;
- maximal contiguous clean runs;
- reset at source-line start and immediately after every unclean segment;
- original five physical-leaf folds, identity SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- fixed `k=2`, additive `alpha=0.01`;
- primary held-out current token must be accepted by the unchanged SlotParser;
- previous clean token need not be SlotParser-accepted;
- no edge or k2 context may cross an unclean segment.

## 3. Frozen models

For target reading `T`, source reading `S`, outer fold `f`:

### POS2_TARGET

Train all generic and continuation factors only on target-reading leaves outside `f`:

1. target pooled START first-atom factor;
2. target pooled BODY first-atom factor;
3. target START/BODY second-atom factors;
4. target clean-run k2 continuation.

### EDGE2_TARGET

The Issue #145 target-native edge reference, trained only on target-reading leaves outside `f`.

### XEDGE2_S→T

Identical to `EDGE2_TARGET` except exactly one factor:

- replace target-native BODY first-atom conditional table with the **literal source-reading training table** `P_S(first | previous_terminal)` learned from source leaves outside the same fold `f`.

All target START/second/continuation factors remain target-native. The primary target population remains target-native.

The source table is inserted with its raw source counts and fixed `alpha=0.01`. There is no source-to-target scalar adjustment, temperature, calibration, mixture weight, interpolation or target-native fallback.

If a previous-terminal context is unseen in the source training table, use the frozen empty exact-context additive distribution `1/32` for every first-atom outcome.

## 4. Frozen score-free Gate0

Before any Issue #148 cross-table target likelihood exists, Gate0 must reproduce Issue #145 score-free authority and verify for each direction/fold:

- source-training physical leaves are disjoint from target-test leaves;
- target primary and target primary run-body counts reproduce Issue #145;
- source clean/run-body training support is nonzero;
- source previous-terminal context set has at least 2 contexts;
- source previous-terminal→first-atom training support has at least 2 observed pairs;
- target held-out primary run-body events with a source-supported previous-terminal context >= 300;
- total target held-out primary run-body events >= 300;
- supported + unsupported target run-body counts exactly equal the frozen target run-body count.

Gate0 may inspect **only previous-terminal identity** on target held-out events for cross-support coverage. It must not inspect or aggregate the held-out current first atom for any transport decision.

Gate0 may summarize source-training outcome support because source training leaves are not target test leaves. It must not compute any categorical probability, target log likelihood, bits/token, `G_transport`, retention ratio, table divergence or scientific classification.

Gate failure maps only to `INVALID CROSS-READING TABLE TRANSPORT` and blocks scoring.

## 5. Frozen primary

For each direction/fold:

`G_transport[S→T,f] = bits(POS2_TARGET)[T,f] - bits(XEDGE2_S→T)[T,f]`.

Direction PASS iff:

- mean `G_transport > 0`; and
- positive `G_transport` in at least 4/5 untouched target folds.

Exactly one valid class:

1. `COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`
2. `COMMON-EVA LITERAL EDGE TABLE TRANSPORTS ZL3B→IT2A ONLY`
3. `COMMON-EVA LITERAL EDGE TABLE TRANSPORTS IT2A→ZL3B ONLY`
4. `COMMON-EVA LITERAL EDGE TABLE TRANSPORTS NEITHER DIRECTION`
5. `INVALID CROSS-READING TABLE TRANSPORT`

No fourth scientific rescue path beyond these frozen classes.

## 6. Frozen non-promoting diagnostics

The scorer may report without affecting classification:

- target-native Issue #145 `G_common` reproduced per fold;
- transport retention `mean G_transport / mean G_common_target` when target-native mean > 0;
- `G_transport - G_common_target` per fold;
- target held-out previous-terminal context coverage under the source training table;
- source/target training-table descriptive disagreement computed from training leaves only;
- directional difference between mean transport gains.

No diagnostic may trigger refitting or class changes.

## 7. Chronology firewall

1. commit this plan and a score-free Gate0 executable;
2. run Gate0 before any Issue #148 target probability code exists;
3. archive and merge the successful Gate0 authority;
4. create a new branch from that merge;
5. commit the scientific cross-table scorer separately;
6. record its blob SHA before any target workflow exists/runs;
7. add workflow later and take the first successful scoring run as authority.

Forbidden after reveal:

- atom remapping;
- source/target event alignment by held-out outcome similarity;
- support matching based on current first atom;
- `k`, `alpha`, temperature, scalar strength or mixture tuning;
- target-native fallback inside the transported table;
- Currier/hand/section-conditioned transport fits;
- latent-state fitting;
- S1/S2/H62/R1 tuning;
- semantic/cipher/historical-direction inference.

## 8. Interpretation boundary

A bidirectional PASS would establish that the literal common-EVA terminal→initial predictive mapping learned on one reading lineage transfers to the other under physical-leaf holdout. It would license a later consensus-table / transcription-robust compact-core consolidation.

A one-direction PASS would be predictive asymmetry only, analogous in logic to Issue #130, and would not identify historical direction.

A dual FAIL would preserve cross-transcription architecture robustness from Issue #145 while rejecting one universal literal table.

Refs #88 #125 #130 #139 #145 #148.
