# Issue #151 — shared common-EVA edge first-reveal provenance

Date: 2026-09-07
Status: **AUTHORITATIVE FIRST REVEAL COMPLETE**

Frozen classification:

> **`ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`**

## Chronology

The scientific chronology was clean and prospective:

1. Issue #151 frozen plan committed before Gate scoring;
2. score-free Gate0 first succeeded in run `34074227552` and computed no real shared-table target likelihood;
3. Gate0 PR #153 merged as `dea1fc30e9e426adaee290bd1cb357478edf96bf`;
4. scientific scorer committed afterward at `1c8f5fe432d60696dd0875e0a5c6082709599008`, scorer blob `2dcd68c8fa68080552a8b90a81e118568b35f8ef`;
5. **no Issue #151 target workflow existed when that scorer blob was frozen**;
6. first target workflow added afterward at `c8865c3f64e8c8991b0456e1dbe2bd6188a97fcf`;
7. first target run completed successfully without any model/threshold/weight repair.

## Authoritative first reveal

- Issue: #151
- PR: #154
- workflow: `Issue151 shared common-EVA edge first reveal`
- run: `34074437422`
- exact workflow head: `c8865c3f64e8c8991b0456e1dbe2bd6188a97fcf`
- conclusion: `success`
- scorer blob: `2dcd68c8fa68080552a8b90a81e118568b35f8ef`
- Gate0 result SHA-256: `bcc6c6bd5600ef9f74484807b51ef1db454613bae2bbd351d90f089c8693eea2`
- Gate0 script blob: `d5e3bd22501f8caebabc7c2728bc7f8d5cb59018`
- Gate0 provenance blob: `609ee5f208cfdb3739749d8d82e34d68e4803dd6`
- frozen plan blob: `e903bfbdd3742e578f784dc9c358f98f44ad42d2`
- Gate0 merge: `dea1fc30e9e426adaee290bd1cb357478edf96bf`
- artifact ID: `10001563139`
- artifact name: `issue151-shared-edge-first-reveal-c8865c3f64e8c8991b0456e1dbe2bd6188a97fcf`
- artifact ZIP digest: `sha256:7bc50522e382a5d93a2d60cd773d4c9886c0186891ae30954f594c88dcd87666`
- result JSON SHA-256: `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`

All workflow assertions passed, including exact Gate reproduction, frozen authority blobs, Issue #145 native-fold gain reproduction, Gate0 shared-table matrix identity/support reproduction, gain decomposition and frozen classification logic.

## Frozen model

For every target reading and untouched physical-leaf fold:

`C_SHARED(ctx,outcome) = 0.5*C_ZL3b(ctx,outcome) + 0.5*C_IT2a(ctx,outcome)`

using only training physical leaves outside that fold in both readings.

All non-edge factors remain target-native. Fixed `k=2`, `alpha=0.01`, `V=32`; no target-native fallback, scalar, temperature, calibration, interpolation or mixture.

Primary quantities:

- `G_shared = bits(POS2_TARGET) - bits(EDGE2_SHARED)`;
- `G_specific = bits(EDGE2_SHARED) - bits(EDGE2_NATIVE_TARGET)`.

A shared table is useful iff mean `G_shared > 0` and positive in at least 4/5 folds. A reading-specific residual is robust iff mean `G_specific > 0` and positive in at least 4/5 folds.

## ZL3b result

`G_shared` by fold:

`[0.13926437255780932, 0.11161234327340175, 0.13728247100496027, 0.14762436955488845, 0.1424451464797798]`

- mean `G_shared = +0.13564574057416792 bit/token`;
- positive `5/5`;
- shared table useful: **YES**.

`G_specific` (native over shared) by fold:

`[0.0009213986606688707, -0.0009043072432319832, 0.0009403071477347424, 0.0005215738462336361, -0.011591197644870377]`

- mean `G_specific = -0.002022445046693022 bit/token`;
- positive `3/5`;
- robust reading-specific residual: **NO**.

Reference target-native Issue #145 edge gain:

- mean `G_native = +0.1336232955274749`;
- shared/native gain ratio `1.0151354225976053`.

Thus the shared table is slightly better on mean held-out code length than the ZL3b-native table under this frozen test; this is a non-promoting diagnostic, not a new threshold.

## IT2a result

`G_shared` by fold:

`[0.17294643599508852, 0.14079586668107957, 0.16944697105456008, 0.18390397539769587, 0.1519496573817669]`

- mean `G_shared = +0.16380858130203818 bit/token`;
- positive `5/5`;
- shared table useful: **YES**.

`G_specific` (native over shared) by fold:

`[-0.0044496719055615586, -0.0013462909376045218, -0.003758599911728666, -0.003560035147692986, 0.003321608367834017]`

- mean `G_specific = -0.001958597906950743 bit/token`;
- positive `1/5`;
- robust reading-specific residual: **NO**.

Reference target-native Issue #145 edge gain:

- mean `G_native = +0.16184998339508744`;
- shared/native gain ratio `1.0121013166999817`.

Again, the shared table is slightly better on mean held-out code length than the IT2a-native table under the frozen test.

## Joint classification

Both shared-table usefulness prerequisites pass 5/5.

Neither reading has a robust native-over-shared residual.

Therefore the frozen class is exactly:

> **`ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`**

The mean reading difference in shared gain is `ZL3b - IT2a = -0.02816284072787026 bit/token`. The mean reading difference in native-over-shared residual is only `-0.00006384713974227907 bit/token`.

## Accepted interpretation

Under the prospectively frozen common Basic-EVA representation and physical-leaf held-out design, **one reading-balanced literal previous-terminal→next-initial table is sufficient for both ZL3b and Takahashi/IT2a**. Separate reading-native tables do not add robust held-out predictive information.

The fact that the shared table slightly outperforms each native table on average is consistent with variance reduction from pooling two noisy readings of the same underlying manuscript surface; it is not needed for the frozen classification and does not prove the population conditional tables are mathematically identical.

This strengthens the interpretation that the terminal→initial edge is a stable observable property of the manuscript surface rather than a transcription-lineage-specific mapping.

## Boundary of inference

This result does **not** establish:

- natural-language word boundaries;
- token-by-token semantic equivalence across readings;
- plaintext or meaning;
- language/cipher family;
- authorship or scribal causation;
- historical direction or production algorithm;
- artificiality/hoax;
- decipherment.

It also does not resolve the Currier A/B literal-table asymmetry from Issue #130, which used a different frozen representation/regime comparison. That is now the next high-information transport question.

Refs #88 #125 #130 #134 #139 #145 #148 #150 #151 #153 #154.