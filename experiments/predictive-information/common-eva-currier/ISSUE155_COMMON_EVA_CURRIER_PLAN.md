# Issue #155 — common-EVA support-matched Currier A↔B edge-table transport

Status: **FROZEN BEFORE CURRIER TRANSPORT SCORING**
Date: 2026-09-07
Parent: Issue #88
Entry result: Issue #151 / PR #154

## Entry authority

Issue #151 classification:

> **`ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`**

Authority:

- Issue #151 Gate0 merge `dea1fc30e9e426adaee290bd1cb357478edf96bf`;
- Issue #151 Gate0 result SHA-256 `bcc6c6bd5600ef9f74484807b51ef1db454613bae2bbd351d90f089c8693eea2`;
- Issue #151 Gate script blob `d5e3bd22501f8caebabc7c2728bc7f8d5cb59018`;
- Issue #151 Gate provenance blob `609ee5f208cfdb3739749d8d82e34d68e4803dd6`;
- Issue #151 first-reveal scorer blob `2dcd68c8fa68080552a8b90a81e118568b35f8ef`;
- Issue #151 first-reveal provenance blob `b599d7a3b4a2c749262231f711c6f14aa6a0cb0e`;
- Issue #151 first-reveal run `34074437422`;
- artifact `10001563139`, ZIP digest `sha256:7bc50522e382a5d93a2d60cd773d4c9886c0186891ae30954f594c88dcd87666`;
- result JSON SHA-256 `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`;
- PR #154 merge `5562f966a5469e9da26406c23f47d60c8c2db17f`.

Historical comparison: Issue #130 raw-byte support-matched Currier table transport classified `MATCHED_TABLE_TRANSPORT: B→A ONLY` (run `34029536188`, artifact `9988168421`, result SHA-256 `d2ae55675fb7613b4f5000ab81558099f2821ff245acacdcb5a6697e06f7249e`).

## Question

Does the earlier B→A-only literal Currier table asymmetry survive the stabilized common Basic-EVA representation, reading-balanced ZL3b/IT2a regime tables, deterministic context-by-context support matching, and independent evaluation in both reading lineages?

## Frozen Currier authority

Reuse Phase 3A exactly:

- `experiments/predictive-information/phase3a/currier_gate0_audit.py` blob `015ee2cda0de53e14d82302aea7e639570db7242`;
- Phase 3A Gate result SHA-256 `e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`;
- physical leaves classified as `A_ONLY`, `B_ONLY`, `MIXED_AB`, or `UNKNOWN_OTHER_ONLY_OR_PRESENT` from frozen ZL3b header/comment authority;
- only `A_ONLY` and `B_ONLY` leaves are eligible;
- the same physical-leaf Currier class is reused in IT2a; no IT2a text outcome can alter a label.

## Frozen representation and folds

Reuse Issue #145/#151 exactly:

- exact ZL3b and Takahashi/IT2a source identities;
- common Basic-EVA: 31 observed atoms plus END, model `V=32`;
- literal IVTFF certain-space segmentation;
- maximal contiguous clean runs, reset at source-line start and after each unclean segment;
- original five physical-leaf folds, SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- fixed `k=2`, `alpha=0.01`;
- unchanged SlotParser primary target;
- previous clean unit need not itself be SlotParser accepted.

## Reading-balanced Currier table

For outer fold `f`, Currier regime `R`, previous-terminal context `c`, and first-atom outcome `y`:

`C_R(c,y) = 0.5*C_ZL3b,R(c,y) + 0.5*C_IT2a,R(c,y)`

using only training physical leaves outside `f` in both readings.

The weights are fixed and untuned.

## Deterministic support matching

For each retained context:

`M_R(c) = Σ_y C_R(c,y)`

Retain contexts with positive mass in both A and B and define:

`m(c) = min(M_A(c), M_B(c))`

`C_R^MATCH(c,y) = C_R(c,y) * m(c) / M_R(c)`.

This freezes exact A/B effective-mass equality separately within every retained previous-terminal context while preserving each regime's training outcome proportions. The scaling depends only on context total mass, never on held-out or training current-first outcomes beyond the already accumulated count table. There is no stochastic subsampling seed.

Contexts absent from either regime are excluded from both matched tables. Future exact-context smoothing remains `alpha=0.01`, `V=32`; an unsupported target previous-terminal context receives the empty exact-context additive distribution. No target-native fallback is allowed.

## Frozen future target model

For target reading `T`, target Currier regime `R`, and outer fold `f`:

- `POS2_T,R`: all generic common-EVA factors trained target-reading/target-regime only on leaves outside `f`;
- `XEDGE2_S→R`: identical non-edge factors, with BODY first-atom probability replaced by the opposite Currier source-regime `C_S^MATCH` table.

No rho/mixture-strength calibration is part of the primary test.

## Primary quantity and stability

`G_transport[T,S→R,f] = bits(POS2_T,R) - bits(XEDGE2_S→R)`.

Within one target reading a direction passes iff mean gain >0 and positive in at least 4/5 outer folds.

A Currier direction is robust only if it passes independently in **both** ZL3b and IT2a.

## Frozen classes

Exactly one:

1. `COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: BIDIRECTIONAL`
2. `COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: A→B ONLY`
3. `COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: B→A ONLY`
4. `COMMON-EVA MATCHED CURRIER TABLE TRANSPORT: NONE`
5. `INVALID COMMON-EVA CURRIER TRANSPORT`

No equivalence margin, post-reveal threshold, rescue class, or historical-direction inference.

## Mandatory score-free Gate0

Before any real Currier transport probability or likelihood:

1. re-run and exact-hash the Issue #151 score-free Gate;
2. pin Issue #151 scorer/provenance/result authority;
3. re-run and exact-hash Phase 3A Currier authority;
4. freeze A_ONLY/B_ONLY physical-leaf sets and reuse them in both readings;
5. prove zero held-out physical-leaf use in any reading/regime training count;
6. audit target primary BODY support for every reading × regime × fold cell;
7. build training-only reading-balanced A/B tables;
8. retain only shared previous-terminal contexts and compute exact context match masses;
9. prove A/B matched effective mass equality separately for every retained context;
10. archive exact rational/fractional matched table identities;
11. audit target matched-context support without selecting on held-out current-first outcome;
12. require at least 300 primary BODY targets and at least 300 matched-context-supported primary BODY targets in every reading × regime × fold cell;
13. run a target-free synthetic test of reading consensus, context-mass matching and additive smoothing;
14. record that no real target transport probability, likelihood, bits/token, gain or classification was computed.

If authority or support fails, stop INVALID rather than changing the rule.

## Secondary non-promoting diagnostics after reveal

Allowed prospectively without changing class:

- target-regime native edge gain;
- source/native matched-table retention;
- matched-context coverage;
- matched context mass and positive cells;
- ZL3b vs IT2a directional difference;
- training-only A/B table divergence.

## Firewall

Do not alter Currier labels, common-EVA atomization, folds, `k`, `alpha`, reading weights, support-matching rule, exact-context fallback, or primary decision rule after target reveal. Do not condition the primary table on hand/section/domain, fit latent states, tune S1/S2/H62/R1, or infer words/plaintext/semantics/language/cipher/authorship/history/hoax/decipherment.

Refs #88 #104 #125 #127 #130 #134 #139 #145 #148 #151 #154 #155.
