# Issue #115 Phase 4B — IT2a P1/P2 first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL — FULL REPLICATION**

## Scientific head

The first IT2a P1/P2 target reveal was executed from PR #117 at the exact pre-result scientific head:

- commit: `c134560f071a89f77c751878f3f096ce6cb2ac63`
- workflow run: `34024979238`
- conclusion: `success`
- artifact ID: `9986755320`
- artifact digest: `sha256:9969915558dec9880c5a980f697759cb5357e92cdd5fcfcb693abcb7f4d1c0e4`
- `phase4b_it2a_first_reveal.json` SHA-256: `3e9651c733a956b7507a71d169555de1904fe11924fc08b30a3a548b5b29be29`

No IT2a P1/P2 output was inspected before this scientific head was committed and the PR-triggered workflow started.

## Authority reproduced before fitting

The scorer reproduced the merged #116 Gate authority before fitting any model:

- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- fold identity `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`
- REAL_SPACE hash `465c93d24b7b96e5d48d7e31d524f700beff849c9fae49a302a7f4ba0d62f675`, n=27,436
- MID_TOKEN hash `c8c75745d4878f9695868e3797cd23c82ed6eb1aa047dd49194482778c53ad75`, n=24,239
- P2 hash `5a74abbbedc46b7dca38e5afbec5707e72a1c67f9becbb4843e7be0ee52c7505`, n=23,379.

## IT2a frozen classification

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

### P1 reset contrast

- REAL_SPACE mean A: `+2.5542140893 bits/event`
- MID_TOKEN mean A: `-5.5384008981 bits/event`
- pooled D_RESET: `+8.0926149875 bits/event`
- fold D_RESET: `+7.8298223019`, `+7.7521161469`, `+8.3497099413`, `+8.1799800972`, `+8.2844882593`
- positive folds: `5/5`
- P1: **PASS**.

### P2 exact-cut challenge

Observed minus one-atom-left shift:

- pooled `-7.9682686460 bits/event`
- folds `-7.9683959258`, `-8.0150261914`, `-7.9019846828`, `-8.0980176125`, `-7.8516592167`
- observed wins `5/5`.

Observed minus one-atom-right shift:

- pooled `-5.2794501281 bits/event`
- folds `-4.9513692542`, `-5.2007349115`, `-5.3986014268`, `-5.5911729548`, `-5.1716777987`
- observed wins `5/5`.

Both P2 sides: **PASS**.

## Frozen cross-transcription replication label

> **VISIBLE-SPACE PRODUCTION BOUNDARY REPLICATES ACROSS ZL3b/IT2a**

No magnitude-agreement threshold was part of the pass rule. Descriptively, however, the independently fitted IT2a effects are close to the frozen ZL3b effects:

| metric | ZL3b | IT2a | IT2a / ZL3b magnitude |
|---|---:|---:|---:|
| P1 D_RESET | +8.81191 | +8.09261 | 0.918 |
| P2 observed-left | -8.50180 | -7.96827 | 0.937 |
| P2 observed-right | -5.47660 | -5.27945 | 0.964 |

The closeness is descriptive only and did not determine replication status.

## OOV diagnostic

Training atom inventories were 26–27 atom types. P2 OOV fraction was zero in folds 0,2,3,4 and `0.0000222` in fold1. The replication is therefore not an OOV artifact.

## Currier diagnostic — non-authoritative

Same unconditioned IT2a models:

- Currier A: D_RESET `+7.12504`; P2 left `-7.38328`; right `-4.35113`.
- Currier B: D_RESET `+8.49239`; P2 left `-8.22591`; right `-5.64258`.

The direction reproduces in both regimes.

## Claim boundary

The result supports literal certain spaces as a **transcription-lineage-robust raw-shape production/construction boundary under the tested ZL3b and IT2a EVA/IVTFF representations**.

It does not establish that the bounded units are natural-language words, semantic units, syllables, cipher groups or historically intended conceptual units. It does not identify plaintext, language, cipher family, author, hoax/artificial generation, historical mechanism or latent semantic state.

Refs #66, #88, #112, #115, #116, #117.
