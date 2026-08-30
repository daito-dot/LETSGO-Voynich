# Phase 64B plan — published Naibbe external C1 challenge

Status: **FROZEN BEFORE IMPLEMENTATION / RESULT REVEAL**

Hypothesis ID: **P64-C1-E0**

Source authority: `C1_SOURCE_AUDIT_B.md`

## 1. Question

Phase64A shows that A1's core H62 recurrence geometry survives severe removal of explicit empirical vocabulary membership, while strict full autonomy fails only on canonical ZL aggregate S3.

The highest-value unresolved mechanism objection is now family-comparison fairness:

> **Can an independently published, reversible meaningful-text cipher reproduce the same held-out entry/locality and post-publication H62 recurrence geometry without importing A1's explicit previous-10 local-family reuse rule?**

Phase64B tests the exact published Naibbe v2 mechanism as **C1-E0**.

This is an external challenger evaluation, not an attempt to optimize Naibbe against this repository.

## 2. Frozen external implementation

Repository:

`greshko/naibbe-cipher`

Commit:

`f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`

Required blobs:

- `naibbe_v2.py`: `b566ad82e4b6ff0782ecdddebf77718dac44f292`
- `references/naibbe_tables.csv`: `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`
- `README.md`: `486782221285186c0f78dd9474b676e067cd4bea`

The workflow must verify all three before execution.

No later Naibbe variant is eligible. In particular, explicit reuse/locality variants are excluded.

## 3. Plaintext panel

Reuse the exact equal-weight Phase62 N0 panel from frozen CREMMA commit:

`292525969ad98380b398e6606a9c2a36d51913ae`

Manuscripts:

1. BIS193
2. CLM13027
3. Mazarine915
4. UBL758

The Phase62 source-native item/line segmentation is unchanged.

For each existing N0 item line, reconstruct the cipher input line by joining its parsed token strings with one ASCII space in original token order. Naibbe's own frozen `clean_line()` then performs its published alphabet projection, including dropping unsupported nonalphabetic/medieval graphemes and mapping `W/J/K` as in the source code.

Do not invent expansions for abbreviation graphemes that Naibbe does not support. Report character-retention diagnostics.

## 4. Document structure preservation

Naibbe is applied line by line in the original item order.

- source item/paragraph boundaries are preserved;
- physical line boundaries are preserved;
- source word boundaries are **not** preserved, because published Naibbe deliberately removes spaces and resegments the plaintext character stream;
- the cipher cannot inspect item identity, line number, paragraph position or Voynich fold.

Each encrypted line becomes one output physical line. Empty outputs, if any, remain empty and are handled by the existing scorecard eligibility rules; they are not padded or repaired.

## 5. Primary published-output view

The primary C1-E0 view is the exact published respaced output:

1. `clean_line()`
2. `encrypt_naibbe()`
3. `respace_line()` with published `SPACE_REMOVAL_RATE = 0.03`
4. split the resulting line on ASCII spaces into output tokens.

All published defaults remain unchanged:

- `RESPACING = 17`
- `USE_78_CARD_DECK = True`
- 78-card weights `28/14/11/11/7/7`
- `SPACE_REMOVAL_RATE = 0.03`
- `UNAMBIGUOUS = True`
- `MAX_BIGRAM_RETRIES = 10000`

No default is selected against Voynich folds.

## 6. Frozen raw-token sensitivity

For the same stochastic encryption stream, retain the pre-`respace_line()` encrypted token sequence as a secondary sensitivity.

Important implementation rule:

> `respace_line()` must still be called on every line in the published sequence even when recording the raw-token sensitivity, so the global random-number consumption and all later line encryptions remain exactly paired with the primary published-output stream.

The raw-token view cannot rescue a failed primary C1-E0 result. It only isolates the effect of the published 3% ciphertext-space removal.

## 7. Stochastic replication

Exactly five cipher realizations are run per manuscript.

Manuscript order is frozen as the four-item list above, indexed `0..3`.

Seed for manuscript `m`, realization `r`:

`6480000 + 100*m + r`

For each manuscript/realization:

1. call Python global `random.seed(seed)` once before the first item;
2. process every item and line in source order;
3. do not reseed at item or line boundaries.

This follows the original script's use of Python global randomness while making the evaluation reproducible.

## 8. Published-codebook permutation control

Naibbe's concrete glyph strings are Voynich-target-aware. To distinguish `cipher mechanism + Voynich-shaped codeword inventory` from the specific plaintext-to-codeword assignment, Phase64B includes a frozen **mapping-permutation control**.

### 8.1 What is preserved

For each of the three states independently:

- preserve the exact multiset of effective published glyph strings;
- preserve six-table structure and the published table-weight deck;
- preserve Naibbe's plaintext segmentation, prefix/suffix composition, ambiguity checks and respacing;
- preserve output alphabet and codeword length/morphology distribution.

### 8.2 What is broken

Within each state, deterministically permute the glyph values across the effective `(table, plaintext-letter)` cells reachable after `W/J/K` normalization.

This breaks the published letter/table-to-glyph assignment while keeping the target-shaped glyph inventory.

### 8.3 Permutation seeds

Five mapping controls:

`6490000 + p`, `p in {0,1,2,3,4}`

Use a dedicated `random.Random(seed)` object for the mapping permutation so it cannot alter the cipher's global random stream.

Each permutation is evaluated using the same five manuscript cipher seeds as the published mapping.

No permutation is selected by Voynich score. Primary control quantities are equal averages over the five frozen permutations.

## 9. Voynich fold/scoring authority

Reuse exact committed Phase62/63 authorities:

- ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- five physical-leaf folds;
- S1 8D training SD/direction learned from Voynich training leaves only;
- S2 previous-10 near-family excess with 100 deterministic nulls;
- S3 fixed-five aggregate 8D line-position eta2;
- H62-P1 five-bin recurrence-excess profile, `D_profile`, and absolute `C_short` difference;
- N0 and fixed C0 comparison authorities;
- Phase63A canonical A1-R1 as the current lower-target-dependence G comparator.

C1-E0 does not see Voynich training targets because no parameter or variant is selected. Voynich folds only provide fold-specific S1 projection directions and held-out targets/comparisons.

## 10. Aggregation

External replication unit remains manuscript.

For each Voynich fold and each view:

1. compute S1/S2/S3 for each of 5 cipher realizations within each manuscript;
2. average realizations within manuscript;
3. average the four manuscripts equally.

For H62:

1. compute signed excess vector `E` for each manuscript/realization;
2. average the five realization `E` vectors within manuscript;
3. average the four manuscript `E` vectors equally;
4. normalize only after this equal-manuscript/equal-realization aggregation;
5. compare the resulting profile to each held-out Voynich fold.

The permutation control adds an outer equal average over the five fixed mapping permutations after the same manuscript/realization aggregation.

No entry is treated as an independent replication unit.

## 11. Exposed scorecard pass

Published C1-E0 is in the broad Voynich structural regime only if the equal-manuscript ratio-of-means lies in `[0.5, 2.0]` for **all three**:

- S1
- S2
- S3

where the held-out denominator is positive/stable, exactly as in prior phases.

No raw-token or permutation sensitivity can replace this primary published-output result.

## 12. H62 viability against N0/C0

Published C1-E0 passes the existing C-family H62 challenge only if all are true:

1. lower mean `D_profile` than N0;
2. lower mean `D_profile` than fixed C0;
3. lower mean `|ΔC_short|` than N0;
4. lower mean `|ΔC_short|` than fixed C0;
5. at least 3/5 strict fold wins on D against each baseline separately;
6. at least 3/5 strict fold wins on C-short error against each baseline separately.

Strict comparison epsilon = `1e-12`; ties are not wins.

## 13. Does C1-E0 rival A1-R1?

Reuse the original H62 prospective-leader logic as a direct challenger rule.

C1-E0 is an H62 **rival/leader over A1-R1** only if the same candidate simultaneously has:

1. lower mean `D_profile` than A1-R1;
2. lower median `D_profile` than A1-R1;
3. strict D wins in at least 3/5 folds;
4. lower mean `|ΔC_short|` than A1-R1;
5. strict C-short wins in at least 3/5 folds.

No weighted combined score is invented.

Failure to beat A1 does not automatically falsify C1 if it still survives the broad exposed/H62 N0-C0 gate; it means the external C challenger is viable but not the leading tested mechanism on the frozen prospective geometry.

## 14. Codebook-specificity diagnostic

The published codebook assignment receives assignment-specific explanatory credit only if, relative to the equal permutation control:

- its mean H62 `D_profile` is lower;
- its mean H62 `|ΔC_short|` is lower;
- its exposed joint relative MSE over S1/S2/S3 is lower.

This diagnostic is descriptive and cannot rescue the primary gate.

Interpretation:

- if published ≈ permuted, fit mainly comes from the Voynich-shaped glyph inventory/algorithm rather than the specific plaintext mapping;
- if published materially outperforms permutation, the plaintext-to-codeword assignment contributes additional structure.

## 15. Complexity/dependence ledger

C1-E0 must be reported with:

- meaningful source plaintext: **yes**, four frozen Latin manuscripts;
- reversible candidate cipher: **yes in the published Naibbe construction**, subject to its documented ambiguity-avoidance rules;
- Voynich boundary-aware mechanism: **0**;
- explicit previous-10/local-family state: **0**;
- published stochastic state: shuffled homophonic table deck + one/two-character segmentation;
- target-derived concrete codebook: **yes, substantial**;
- effective reachable codebook cells after normalization: 414;
- published scalar/model defaults searched by this project: **0**;
- Phase64B model alternatives selected on Voynich: **0**;
- post-encryption space-drop parameter: fixed published 0.03;
- direct section/hand/page metadata: **0**.

This complexity vector is mandatory even if C1-E0 scores strongly.

## 16. Frozen classifications

### `C1-E0 STRUCTURALLY VIABLE`

Primary published-output exposed gate passes and H62 viability against both N0/C0 passes.

### `C1-E0 H62 RIVAL TO A1-R1`

Requires structural viability plus every direct A1-R1 challenger condition in §13.

### `C1-E0 PARTIAL`

At least one exposed or H62 criterion fails, but the model materially improves on N0/C0 in a documented subset.

### `C1-E0 NOT COMPETITIVE`

Fails to achieve broad exposed regime and does not pass the H62 N0/C0 viability rule.

No classification authorizes a historical-identification or decipherment claim.

## 17. Interpretation freeze

If C1-E0 is structurally viable or rivals A1-R1:

> A published reversible meaningful-text cipher can reproduce a materially larger part of the currently discriminative Voynich structure than C0. The C family must remain live, with explicit target-codebook complexity charged.

If C1-E0 fails H62 despite broad distributional fit:

> The published Naibbe construction demonstrates that Voynich-like ciphertext marginals are insufficient for the prospectively validated recurrence-distance geometry in its original no-reuse form.

If published mapping ≈ permutation control:

> Any fit is dominated by the supplied Voynich-shaped codeword inventory/algorithm rather than evidence that meaningful plaintext structure is being transferred through the specific mapping.

If published mapping beats permutation:

> The specific plaintext-to-codeword assignment contributes measurable structure beyond the target-shaped glyph inventory, but target-aware codebook design remains a major complexity cost.

## 18. Explicit non-claims

Regardless of outcome, Phase64B cannot establish:

- that the Voynich Manuscript was encrypted with Naibbe;
- that meaningful plaintext exists underneath Voynichese;
- that semantics are absent;
- that the entire C family is accepted/rejected;
- that A1 is historical;
- decipherment.

## 19. Reveal chronology

1. commit source audit;
2. commit this plan;
3. merge design-only freeze to main;
4. implement an adapter without changing the external pinned algorithm;
5. commit executable/workflow before any Phase64B metric is computed;
6. first science run from frozen head;
7. preserve artifact/hash before result documentation;
8. record negative/positive result without adding reuse or retuning Naibbe.
