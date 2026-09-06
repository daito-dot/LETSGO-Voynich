# Issue #139 — independent IT2a terminal→initial edge first-reveal provenance

Date: 2026-09-07
Status: **INDEPENDENT EDGE REPLICATION PASSES**

This document archives the first successful target-scoring run under the prospectively frozen Issue #139 contract. It adds provenance only; it does not change source handling, folds, target population, representation, smoothing, model family, pass rule, or interpretation boundary.

## Chronology

### Merged score-free authority

Issue #139 Gate0 was merged before the scientific scorer existed:

- Gate0 PR: #143
- Gate0 merge: `12b2b79de65ab1ac510cb3b8aad5386dcb180249`
- Gate0 run: `34061441684`
- Gate0 artifact: `9997590970`
- Gate0 result JSON SHA-256: `b97fe44633b088a97e86d5e08a74e9688647b8bb5eeeb7a44a43c98887b80fea`
- Gate0 disposition: `PASS — PROCEED TO SEPARATELY COMMITTED FROZEN IT2A EDGE SCORER`

### Scorer freeze before target reveal

The scientific scorer was committed separately after the Gate merge and before any target run:

- scorer commit: `bb5d2cf56f2cb40eba99dd209aa8da187172d379`
- scorer file: `experiments/predictive-information/independent-edge/issue139_it2a_edge_first_reveal.py`
- scorer Git blob SHA-1: `6e8cdeb4ffeed4d75a0b8ac5f0e67ab0cf836c79`

The next commit added only the workflow:

- initial workflow commit: `1e420f8fc27f603fb6c630e27be5d339fa85c55a`

The scorer blob remained unchanged at `6e8cdeb4ffeed4d75a0b8ac5f0e67ab0cf836c79` throughout first reveal.

### Pre-target transport failure

The first workflow run did **not** reveal the target:

- run: `34061614164`
- head: `1e420f8fc27f603fb6c630e27be5d339fa85c55a`
- conclusion: `failure`
- failed step: `Assert merged Gate ancestry and frozen scorer blob`
- IT2a retrieval: skipped
- scorer self-test: skipped
- `Run frozen independent first reveal`: skipped
- result artifact: none

Cause: `actions/checkout` used its shallow default, so the already-merged Gate commit was unavailable to `git merge-base --is-ancestor`. No IT2a target data were loaded and no predictive score was computed.

A transport-only workflow commit added `fetch-depth: 0`:

- transport fix commit: `8deebb3ebca22da84375d1f30413feb078b7bfc2`
- scientific scorer blob after fix: unchanged at `6e8cdeb4ffeed4d75a0b8ac5f0e67ab0cf836c79`

No scientific parameter or implementation changed.

## Authoritative first successful target reveal

- PR: #144
- workflow: `Issue139 IT2a edge first reveal`
- run: `34061721332`
- scientific/workflow head: `8deebb3ebca22da84375d1f30413feb078b7bfc2`
- conclusion: `success`
- artifact ID: `9997679250`
- artifact name: `issue139-it2a-edge-first-reveal-8deebb3ebca22da84375d1f30413feb078b7bfc2`
- artifact ZIP digest: `sha256:1043ce3a54c47f1c87b0070f52e0a0693660bb26dcbc3a7de4c78a4ea074cec1`
- result JSON: `issue139_it2a_edge_first_reveal.json`
- result JSON SHA-256: `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`

The workflow re-established before scoring:

- exact Gate0 result SHA-256 `b97fe44633b088a97e86d5e08a74e9688647b8bb5eeeb7a44a43c98887b80fea`;
- exact IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- exact IT2a Git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`;
- exact Issue #125 architecture blob `5b4bead22ed301cba88300af97cef654610648ab`;
- exact Gate script blob `e5571c92ad8c4ef437b73dac7a246eec3cf2a887`;
- exact Gate provenance blob `47af1106f55effa2adb309ec085d3101334680d8`.

## Frozen primary result

Primary definition:

`G_identity_IT2a = bits(POS2) - bits(EDGE2)`

Frozen pass rule:

- mean `G_identity_IT2a > 0`; and
- positive in at least `4/5` untouched physical-leaf folds.

Observed fold results:

| fold | scored targets | scored line-body | POS2 bits/token | EDGE2 bits/token | G_identity_IT2a |
|---:|---:|---:|---:|---:|---:|
| 0 | 4,976 | 4,393 | 10.0370286958 | 9.8765935376 | +0.1604351582 |
| 1 | 5,416 | 4,824 | 9.9496988507 | 9.8260884631 | +0.1236103876 |
| 2 | 6,261 | 5,545 | 9.7755304034 | 9.6202087137 | +0.1553216897 |
| 3 | 6,197 | 5,517 | 9.8468703451 | 9.6729033895 | +0.1739669556 |
| 4 | 5,430 | 4,832 | 9.9601852348 | 9.8129599988 | +0.1472252361 |

Aggregate:

- mean POS2: `9.913862705954429 bits/token`;
- mean EDGE2: `9.761750820525345 bits/token`;
- mean `G_identity_IT2a`: `+0.15211188542908544 bit/token`;
- positive folds: `5/5`;
- frozen rule: PASS.

Frozen classification:

> **`INDEPENDENT EDGE REPLICATION PASSES`**

## Architecture checks

The broader source-line-contiguous k=2 model was evaluated only as the preregistered implementation-equivalence check for the Issue #125 factorization.

- `EDGE2_LINECONT2_max_abs_token_logp = 0.0` in every fold;
- every scored line-body target used a previous-terminal context observed in that fold's training complement;
- unseen previous-terminal contexts among scored line-body targets: `0` in all five folds;
- target support reproduced Gate0 exactly: `[4976, 5416, 6261, 6197, 5430]`;
- line-body target support reproduced Gate0 exactly: `[4393, 4824, 5545, 5517, 4832]`.

No support repair, post-reveal smoothing change, fallback addition, glyph normalization, fold regrouping, subgroup selection, or model-family expansion occurred.

## Interpretation

This result materially reduces the plausibility that the same-line previous-terminal→next-initial predictive edge identified in ZL3b is merely a ZL3b reading/transcription artifact. The same frozen architecture improves held-out prediction strongly and consistently in the independently frozen Takahashi/IT2a reading lineage under the common EVA/IVTFF framework.

It does **not** establish that literal conditional tables or effect magnitudes are identical across transcriptions. It also does not establish natural-language wordhood, semantics, plaintext, language, cipher family, authorship, historical production mechanism, or hoax/artificial origin.

The accepted responsibility is narrower: a compact same-source-line edge architecture linking the previous visible unit's terminal identity to the next visible unit's initial identity is independently predictive across the two reading lineages tested.

Refs #66 #88 #123 #125 #134 #139 #143 #144.
