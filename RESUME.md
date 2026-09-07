# RESUME — deterministic restart point

Last consolidated: 2026-09-07

## Resume here — Issue #148 is closed; Issue #151 is next

Do not reconstruct the project from old chat when GitHub contains a newer state.

Issue #148 has completed the cross-reading literal edge-table transport gate. The frozen classification is:

> **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**

Under the frozen common Basic-EVA representation, the BODY table `P(first_common_atom | previous_terminal_common_atom)` learned from either reading predicts the other reading's untouched physical-leaf fold:

- ZL3b→IT2a mean `G_transport = +0.15554823663346334 bit/token`, positive `5/5`;
- IT2a→ZL3b mean `G_transport = +0.13039023868507016`, positive `5/5`;
- transport retains `96.106%` and `97.580%` of the corresponding target-native edge gain;
- minimum previous-terminal context coverage is `0.99935469993547` and `0.9988499137435307`.

This promotes the same-line terminal→initial mechanism from architecture-only replication to a **bidirectionally transportable literal predictive mapping across ZL3b and IT2a under the common-EVA representation**.

The manuscript is not deciphered. ZL3b and IT2a are two readings of the same physical manuscript, not independent manuscripts. This result does not establish words, plaintext, language, cipher family, historical direction, authorship, artificiality/hoax or a production algorithm.

### First sentence a future agent should be able to say

> The tested short sequence residual beyond corrected B3 is closed by a compact observable same-line edge; that edge independently replicates on IT2a, remains robust under one common-EVA representation, and its literal previous-terminal→next-initial table transports in both directions between ZL3b and IT2a with about 96–98% retention of target-native gain. The next gate asks whether separate reading-native edge tables are still needed at all.

## Read in this order

1. `README.md`
2. `research/STATUS.md`
3. `ROADMAP.md`
4. Issue #151
5. Issue #148 and merged PR #150 for exact transport chronology
6. `research/PREDICTIVE_INFORMATION_PROGRAM.md`
7. `research/HYPOTHESIS_LEDGER.md`
8. `research/RESEARCH_PROTOCOL.md`
9. Issue-specific plans/provenance under `experiments/predictive-information/`

For exact historical numbers or methods, open the relevant frozen plan, report and first-reveal provenance. Superseded current-state snapshots are historical only.

## Authority hierarchy

1. phase/Issue-specific frozen plan + exact first-reveal artifact/provenance control historical method, hashes and frozen classification;
2. `research/STATUS.md` controls the current accepted high-level interpretation;
3. `research/PREDICTIVE_INFORMATION_PROGRAM.md` controls the Issue #88 program and latent-state licensing rule;
4. `research/HYPOTHESIS_LEDGER.md` controls current hypothesis status/history;
5. `research/RESEARCH_PROTOCOL.md` controls evidential discipline;
6. `ROADMAP.md` controls current sequencing;
7. old chats and archived snapshots are non-authoritative where later repository evidence conflicts.

## Current accepted state

### 1. Token-internal construction is compact

Issue #75 + OGH-A/B/C close the token-internal R1 generation lane.

- target-blind second-order occupied-slot successor grammar: 298 counted conditional probabilities;
- median topology agreement `T≈0.948` on ZL3b and `0.962` on IT2a;
- memoryless V2 code length `9.7089061 bits/token`;
- approximate information split: shape `~7.0`, values add `~2.7 bits/token`.

Do not reopen an occupancy-only R1 ladder without a new falsification reason.

### 2. Certain visible spaces are production/construction boundaries

Independent ZL3b and IT2a tests support exact visible cuts over nearby shifted cuts. This validates the tested production boundary, not a linguistic word interpretation.

### 3. Corrected observable predictive ladder

After source-order correction:

- B0 V2 `9.7089061`;
- B1 local `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688 bits/token`.

Longer-history gain is dominated by causal-prefix / prior-paragraph inventory rather than detailed long ordered memory.

### 4. The old flexible residual was small, real, and localized

- Issue #118: `G_context = +0.0178533 bit/token`, positive 5/5;
- Issue #121: same-order fixed-k2 residual `+0.0106322`, positive 5/5;
- Issue #123: line-local gain `+0.0291614`, positive 5/5; carrying context beyond line break `-0.0185292`, positive 0/5;
- Issue #125: generic position/onset `+0.00889185`; terminal→initial identity adds `+0.02026956`, both 5/5; EDGE2 and LINECONT2 are token-logp identical.

### 5. Issue #134 closes the residual after observable augmentation

- classification **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**;
- `G_residual=[0,0,0,0,0]`;
- augmented core mean `9.451900585480233` vs B3 `9.517268842963203`;
- gain over B3 `+0.06536825748296984`, positive 5/5;
- RESET and LINE challengers choose final `w=0` in every fold.

Authority: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.

No current residual-based license exists for a rich latent-state escalation.

### 6. The edge independently replicates and survives common representation

Issue #139 Takahashi/IT2a replication:

- classification **`INDEPENDENT EDGE REPLICATION PASSES`**;
- mean gain `+0.15211188542908544`, positive 5/5;
- run `34061721332`, artifact `9997679250`, result SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`.

Issue #145 common Basic-EVA dual-reading test:

- classification **`COMMON-EVA EDGE ROBUST IN BOTH READINGS`**;
- ZL3b mean `+0.1336232955274749`, positive 5/5;
- IT2a mean `+0.16184998339508744`, positive 5/5;
- EDGE2_COMMON equals full clean-run-contiguous k2 at token-logp level in all reading×fold cells;
- run `34062199123`, artifact `9997826217`, result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`.

### 7. Issue #148 shows the concrete common-EVA table is shared across readings

Authoritative run `34073660425` at pre-merge head `e08e682c9be91ee9cec97dedd66dd2dc3549eac1` completed all frozen assertions.

- classification **`COMMON-EVA LITERAL EDGE TABLE TRANSPORTS BOTH DIRECTIONS`**;
- ZL3b→IT2a fold gains `[0.16617550444405893, 0.13437428362215265, 0.16077057068791767, 0.1796534044981435, 0.13676741991504393]`, mean `+0.15554823663346334`, positive 5/5;
- IT2a→ZL3b fold gains `[0.13208421050786257, 0.10700594617669168, 0.12950827390527841, 0.1397962031635096, 0.14355655967200853]`, mean `+0.13039023868507016`, positive 5/5;
- target-native retention `0.9610642730420239` / `0.9758046916172639`.

Authority:

- Gate0 result SHA-256 `f324264b814ef02d8de70b804754750ec579f8a9e0d8dffb0f1575439867d1bf`;
- scorer blob `7847c0fea1dcfc4ace5752d0188d70e3739679d3`;
- run `34073660425`;
- artifact `10001309613`;
- ZIP digest `sha256:cfefd670b00ebb3eae3020a4b5308115ec9172b793ed1fe4b598928718f5c622`;
- result JSON SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`;
- PR #150 merged as `b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131`.

PR #150 also records the authority-repair chronology. Do not rewrite that history as a perfectly clean single attempt: run `34073482403` entered the scorer but aborted at a mis-copied Issue #145 authority constant and emitted no transport metric/classification; the existing frozen #145 artifact was then used to correct only the authority constants. No #148 scientific rule changed.

### 8. Currier A/B remains a separate regime question

Issue #130 support-matched literal table transport remains **B→A ONLY** under its frozen representation. #148 cross-reading bidirectional transport does not imply Currier universality or historical direction.

## Next scientific move — Issue #151

Issue #151 asks whether the two reading-native common-EVA edge tables can be collapsed into one table without losing reproducible held-out information.

Frozen shared table per outer fold:

`C_SHARED = 0.5 * C_ZL3b + 0.5 * C_IT2a`

using training leaves outside the untouched physical-leaf fold in **both** readings. The `0.5/0.5` weights are fixed to avoid making the same manuscript evidence artificially twice as sharp merely because two transcriptions are pooled.

Primary quantities:

- `G_shared[T] = bits(POS2_TARGET) - bits(EDGE2_SHARED)`;
- `G_specific[T] = bits(EDGE2_SHARED) - bits(EDGE2_NATIVE_T)`.

A reading-specific residual requires mean `G_specific > 0` and positive in at least 4/5 folds. The shared table must itself be useful in both readings or the consolidation is INVALID.

### First deliverable

**Score-free Gate0 only.** Freeze and audit:

- exact #145/#148 authorities;
- physical-leaf folds and zero held-out leaf use in either reading's shared-table training counts;
- exact target support reproduction;
- per-reading edge counts and context support;
- deterministic fractional `0.5/0.5` consensus arithmetic;
- finite support and target-free synthetic tests;
- no held-out shared-table likelihood, `G_shared`, `G_specific` or classification inspected.

## Do not

- reopen rich latent-state work after #134 without a new prospectively defined residual;
- tune #151 reading weights, normalization, exclusions, mapping, folds, smoothing or fallback after target reveal;
- treat ZL3b and IT2a as independent manuscripts;
- erase the distinct Currier A/B asymmetry from #130;
- reopen token-internal R1 ladders without a new falsification reason;
- treat visible spaces as proven natural-language words;
- infer plaintext, language, semantics, cipher identity, author, historical direction, hoax/artificial origin or historical production mechanism from predictive fit;
- call a non-reversible surface generator a decipherment;
- append another current resume beneath this file; replace it and archive superseded snapshots where appropriate.
