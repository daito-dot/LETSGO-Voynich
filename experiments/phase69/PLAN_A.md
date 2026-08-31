# Phase 69A — meaningful plaintext with context-adaptive homophonic obfuscation

Status: **FROZEN BEFORE FIRST C2-LH1 VOYNICH SCORE**

Date: 2026-08-31

Hypothesis ID: **P69-C2-LH1**

## 1. Question

The current evidence creates a specific tension:

- A1-like short-range formal recurrence has genuine prospective and replication support;
- a serious meaningful-text cipher, published Naibbe C1-E0, is substantially better than simple C0 but fails specifically on paragraph-entry S1 and previous-10 / H62 short-range recurrence;
- Phase66–68 found no direct local mapping from pharmaceutical image morphology to attached-label, nearby body-character, formal-residual character, or formal-residual lexical structure.

One live explanation is that meaningful plaintext is present but a deliberate surface encoder actively chooses among equivalent ciphertext realizations in a context-dependent way.

Phase69A asks:

> Can meaningful plaintext carried by a reversible homophonic code acquire the A1-like short-range recurrence geometry when the encoder deliberately prefers a valid homophone one edit away from recent ciphertext?

This is a mechanism-compatibility test. It does not claim that this exact procedure was historically used.

## 2. Historical grounding and explicit novelty charge

Historically grounded ingredients:

- fifteenth-century northern Italian diplomatic ciphers used homophonic substitution, including several substitution options for plaintext letters;
- nomenclators and nulls were used in historical cipher practice to make reading/solution harder;
- recent historical-cryptology work documents both the spread of monoalphabetic systems and use of more complex systems in fifteenth-century Italy.

Relevant sources include:

- Greshko, M. A. (2025), *The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext*, Cryptologia, DOI 10.1080/01611194.2025.2566408. The article specifically notes 1435 Modena and 1450 Mantua precedents with multiple substitution options.
- Vito, M. (2025), *A Florentine 'polyalphabetic' cipher in the 15th century*, HistoCrypt 2025, https://hdl.handle.net/10062/109755.
- Megyesi et al., work on historical cipher-key instructions/nomenclatures, documenting homophones, nomenclators and null practices from the fifteenth century onward.

**Not historically established:** choosing a homophone because its ciphertext form is edit-distance 1 from a recently written ciphertext token. That is the new P69-C2-LH1 mechanism and must be charged as an explicit complexity term. A positive result cannot be described as evidence that a known historical cipher used this exact rule.

## 3. Fixed external base cipher

Reuse the exact published Naibbe v2 source authority from Phase64B:

- repository: `greshko/naibbe-cipher`
- commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`
- `naibbe_v2.py` blob: `b566ad82e4b6ff0782ecdddebf77718dac44f292`
- `references/naibbe_tables.csv` blob: `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`
- `README.md` blob: `486782221285186c0f78dd9474b676e067cd4bea`

Reuse the same 23 effective plaintext letters after the Phase64B B3 drop-only interface projection. No medieval grapheme expansion or favorable transliteration is added.

Reuse published Naibbe parameters that define plaintext segmentation and output presentation:

- `RESPACING = 17`
- 78-card table weights: alpha 28, beta1 14, beta2 11, beta3 11, gamma1 7, gamma2 7
- `SPACE_REMOVAL_RATE = 0.03`
- ambiguity-safe bigram requirement

The published codebook is target-aware and remains a major complexity/dependence charge.

## 4. Fixed meaningful plaintext panel

Reuse exactly the Phase62/64 equal-weight CREMMA panel at commit `292525969ad98380b398e6606a9c2a36d51913ae`:

1. BIS193
2. CLM13027
3. Mazarine915
4. UBL758

Preserve source item and physical line boundaries exactly as the existing parser does.

## 5. Plaintext segmentation

For each cleaned physical line, remove spaces as published Naibbe does and segment into one- or two-letter plaintext units with the published probability rule:

- if one character remains, emit a one-character unit;
- otherwise emit one character when `r < 17/36`, two characters otherwise.

A dedicated deterministic segmentation RNG is used so C2-LH0 and C2-LH1 receive **identical plaintext unit sequences** in every manuscript/realization.

This isolates the effect of context-adaptive homophone selection.

## 6. Candidate ciphertext set

For every plaintext unit, enumerate all valid realizations from the fixed published codebook.

### One-character plaintext unit

Six candidates, one unigram glyph from each published table, subject to codebook existence.

Candidate weight = the published 78-card weight of that table.

### Two-character plaintext unit

Enumerate all 36 prefix-table × suffix-table combinations.

Keep only candidates satisfying the published ambiguity rules:

1. combined glyph string is not any published unigram glyph;
2. no other prefix/suffix code pair produces the same combined glyph string.

Candidate weight = `weight(prefix_table) * weight(suffix_table)`.

If a plaintext unit has no valid candidate, the model is `BLOCKED`; do not repair the codebook or ambiguity rule.

## 7. Paired model arms

### C2-LH0 — weighted homophone control

For each plaintext unit, select one valid ciphertext candidate randomly in proportion to the fixed candidate weights.

C2-LH0 has no recent-ciphertext preference. It exists to isolate effects caused merely by replacing Naibbe's shuffled-deck sampling with independent weighted candidate sampling.

### C2-LH1 — local adaptive homophone selection

Maintain the previous **10 emitted raw ciphertext tokens within the same source item**, crossing physical line boundaries within that item and resetting only at the next source item.

For current plaintext unit:

1. enumerate its valid candidates;
2. define the eligible local subset as candidates having Levenshtein distance **exactly 1** from at least one of the previous 10 emitted raw ciphertext tokens;
3. if the subset is nonempty, sample from that subset in proportion to the original candidate weights;
4. otherwise sample from the complete valid candidate set in proportion to the original candidate weights;
5. append the selected raw ciphertext token to the previous-10 history.

The edit1 definition is exactly the Phase61/62 relation:

- equality does not count;
- one insertion, deletion or substitution counts;
- length difference greater than one does not count.

No similarity score other than exact edit1 is considered. No Voynich token, fold target or score is consulted during selection.

## 8. Output respacing

After all raw ciphertext tokens on each physical line are generated, apply the published 3% adjacent-space removal rule.

C2-LH0 and C2-LH1 use paired respacing RNG seeds. Because they have the same number of raw units per line, they receive the same sequence of space-drop decisions.

Both are scored in the primary published-style respaced view. Raw-token outputs are retained as a frozen sensitivity and decoder audit but cannot rescue a failed primary arm.

## 9. Deterministic seeds

For manuscript index `m` in the frozen order and realization `r in 0..4`:

`base = 6900000 + 100*m + r`

Use:

- segmentation RNG seed = `base`
- LH0 selection RNG seed = `base + 10000`
- LH1 selection RNG seed = `base + 20000`
- paired output-space RNG seed = `base + 30000`

Exactly five realizations per manuscript. No realization is selected on Voynich score.

## 10. Reversibility audit

Before any Voynich metric is accepted:

- construct the inverse raw-token catalog implied by the exact published codebook and ambiguity rules;
- every selected raw ciphertext token must uniquely decode to the plaintext one- or two-character unit that produced it;
- audit all emitted raw units in all arms/realizations;
- required exact decode accuracy = **1.000**.

If any raw emitted token is ambiguous or decodes incorrectly, Phase69A is `BLOCKED / REVERSIBILITY FAILURE`.

The published 3% space removal is presentation noise; the reversibility audit is performed on the pre-space-removal raw token sequence, exactly as Phase64B retained a raw-token view.

## 11. Mechanism utilization audit

Report for C2-LH1:

- total emitted raw tokens;
- count/fraction with at least one edit1 candidate available against previous 10;
- count/fraction for which the selected token is edit1 to previous 10;
- opportunity and selected-hit rates by manuscript and realization.

By construction selected-hit count should equal opportunity count. Any mismatch is an implementation failure.

## 12. Voynich scoring authority

Reuse the exact frozen Phase62/63 scorecard and authorities through the Phase64B adapter:

- S1 paragraph-entry projection;
- S2 previous-10 near-family excess;
- S3 aggregate line-position eta2;
- H62-P1 five-bin recurrence-excess profile;
- `D_profile` and `|ΔC_short|`;
- same five physical-leaf Voynich folds;
- same N0, fixed C0 and A1-R1 comparison authorities.

No score definition or target is changed.

## 13. Aggregation

For each arm:

1. score each realization within manuscript;
2. average the five realization metrics/profile excess vectors within manuscript;
3. average four manuscripts equally;
4. evaluate the aggregate against the five held-out Voynich fold targets.

This matches the external replication hierarchy used in Phase64B.

## 14. Predeclared causal mechanism prediction

Because P69-C2-LH1 was motivated by C1-E0's locality failure, the first question is whether the new local selector actually changes the intended geometry.

C2-LH1 passes the **local-adaptation mechanism check** only if, in the primary respaced view, all are true relative to C2-LH0:

1. aggregate S2 is strictly higher;
2. mean H62 `|ΔC_short|` is strictly lower;
3. mean H62 `D_profile` is strictly lower.

Report the same three comparisons against the already sealed published C1-E0 result, but those comparisons are descriptive because C1-E0 differs in sampling mechanism as well as local adaptation.

If LH1 does not beat LH0 on all three, classify `LOCAL ADAPTATION DID NOT PRODUCE THE PREDICTED STRUCTURE` regardless of any isolated score.

## 15. Full structural gate

For direct comparability with Phase64B, C2-LH1 is in the broad structural regime only if the same existing gates pass:

### Exposed gate

Equal-manuscript ratio-of-means must lie in `[0.5, 2.0]` for all:

- S1
- S2
- S3

### H62 viability vs N0/C0

Same Phase64B conditions:

- lower mean D than N0 and C0;
- lower mean |ΔC_short| than N0 and C0;
- at least 3/5 strict fold wins on each diagnostic against each baseline.

### A1-R1 rivalry

Use the exact Phase64B rival rule. No new weighted combined score is allowed.

## 16. Interpretation categories

### `C2-LH1 STRUCTURALLY VIABLE MEANINGFUL-TEXT OBFUSCATION MODEL`

Requires local-adaptation mechanism check + exposed gate + H62 viability.

### `C2-LH1 H62 RIVAL TO A1-R1`

Requires structural viability plus every existing A1 rivalry criterion.

### `C2-LH1 LOCALITY-ONLY PARTIAL`

Local-adaptation mechanism check passes and S2/H62 materially move toward Voynich, but full exposed/H62 structural viability fails, especially if S1 remains absent.

### `C2-LH1 NOT COMPETITIVE`

The local mechanism check fails or no substantive structural advantage survives.

Because the model was designed after seeing C1-E0's locality failure, even `STRUCTURALLY VIABLE` is **developmental mechanism evidence**, not an independent prospective confirmation.

## 17. Complexity/dependence ledger

Mandatory report:

- meaningful source plaintext: yes;
- raw codeword reversibility: required 100%;
- externally published target-shaped Naibbe codebook: yes, substantial;
- published homophonic candidate inventory/weights: yes;
- explicit previous-10 ciphertext state: **yes, new**;
- edit1-aware context selection: **yes, new**;
- paragraph/line-position-specific tuning: no;
- page/section/hand metadata: no;
- Voynich score used for parameter selection within Phase69: no;
- model chosen after Phase64 C1 failure: yes; adaptation debt explicitly charged.

## 18. Claim boundary

A strong result would establish only that a bounded meaningful-plaintext homophonic encoder can coexist with, or reproduce part of, the A1-like formal recurrence when it is given an explicit recent-ciphertext obfuscation rule.

It would **not** show that:

- Voynichese is Naibbe;
- this context-adaptive rule is historically attested;
- the plaintext is Latin or Italian;
- any particular illustration has been decoded;
- a decipherment key has been found.
