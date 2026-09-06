# Issue #115 Phase 4B — IT2a P1/P2 first-reveal plan

Date: 2026-09-06
Status: **FROZEN BEFORE IT2a P1/P2 SCORING**
Parent: Issue #88
Prerequisite: merged PR #116 score-free IT2a Gate 0

## Question

Does the ZL3b Phase-4A visible-space production-boundary result reproduce in the independent Takahashi/IT2a reading under the unchanged representation logic, model and pass rules?

## Frozen IT2a authority

Before model fitting, regenerate the merged Gate-0 authority and halt if any identity differs:

- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- IT2a Git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- fold identity `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`
- REAL_SPACE hash `465c93d24b7b96e5d48d7e31d524f700beff849c9fae49a302a7f4ba0d62f675`, count `27,436`
- MID_TOKEN hash `c8c75745d4878f9695868e3797cd23c82ed6eb1aa047dd49194482778c53ad75`, count `24,239`
- P2 REAL_SPACE hash `5a74abbbedc46b7dca38e5afbec5707e72a1c67f9becbb4843e7be0ee52c7505`, count `23,379`.

No event may be dropped or added after likelihood is available.

## Representation

Identical to Phase 4A and merged Phase-4B Gate:

- REAL_SPACE = literal IVTFF `.` only;
- same Basic-EVA atomizer and connected composites `cfh/ckh/cph/cth/ch/sh`;
- same complete-token exceptional-content exclusion;
- same midpoint pseudo-boundary;
- same P2 >=3-atoms-each-side population;
- same original five physical-leaf folds.

## Frozen predictive model

For outer fold f, train only on clean IT2a certain-space token sequences from the other four folds.

Second-order atom model:

`P(x_t | x_{t-2}, x_{t-1})`

with exactly:

- `(BOS,BOS)` token start;
- no STOP probability;
- training atom types plus one OOV bucket;
- held-out unseen atoms mapped to OOV as target and context;
- additive alpha `0.5`;
- no backoff/interpolation/order/smoothing search.

The ZL3b learned counts, parameters and target effect magnitudes are not transferred.

## P1

Same Phase-4A event score:

`A = bits(CARRY) - bits(RESET)`

where RESET predicts the first two atoms right of the cut from BOS contexts and CARRY uses the literal two atoms left of the cut.

`D_RESET = mean(A_REAL) - mean(A_MID)`.

Pass iff pooled `D_RESET > 0` and fold-specific D_RESET >0 in >=4/5 folds.

## P2

For each frozen P2 event, code the same atoms under:

- `L | R`
- `L[:-1] | L[-1:] + R`
- `L + R[:1] | R[1:]`.

Observed cut beats a shift iff `bits(OBSERVED)-bits(SHIFT) < 0`.

Each side passes iff the pooled mean is negative and fold-specific mean is negative in >=4/5 folds. P2 passes iff both sides pass.

## IT2a classification

Use the exact Phase-4A four valid-result classes:

- `SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY`
- `SPACE MARKS A RESET BUT EXACT CUT IS WEAK`
- `SPACE POSITION IS LOCALLY PRIVILEGED WITHOUT RESET EVIDENCE`
- `VISIBLE SPACE NOT SUPPORTED AS PRODUCTION BOUNDARY`.

Authority mismatch stops before fitting as `IT2A REPLICATION INVALID` rather than producing a scientific class.

## Cross-transcription replication label

Given the already frozen ZL3b class `SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY`:

- IT2a full class -> `VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a`
- IT2a reset-only or exact-cut-only -> `PARTIAL CROSS-TRANSCRIPTION BOUNDARY REPLICATION`
- IT2a unsupported class -> `CROSS-TRANSCRIPTION BOUNDARY REPLICATION FAILS`.

No magnitude-similarity requirement may be invented after reveal.

## Diagnostics

Non-authoritative only:

- OOV rates by fold;
- Currier A/B values from the same unconditioned models;
- continuous IT2a fold values;
- descriptive comparison to the already frozen ZL3b magnitudes only after the IT2a class is determined.

## Firewall

This reveal must not:

- tune any source/atomization/cut/model parameter against IT2a;
- import ZL3b fitted counts;
- select `.` versus `,` after scoring;
- use SlotParser eligibility;
- optimize magnitude agreement with ZL3b;
- infer natural-language wordhood, meaning, plaintext, language, cipher identity, authorship, hoax/artificial generation, historical mechanism or latent semantic state.

## Authority rule

The scientific scorer and workflow must be committed before any IT2a P1/P2 output is inspected. The first successful PR-triggered artifact at that scientific head is the authoritative first reveal. Later documentation commits must reproduce the JSON byte-for-byte.

Refs #66, #88, #112, #115, #116.
