# Issue #72 — preregistered Naibbe R1 codebook/process decomposition

Status: **PREREGISTERED — NO COUNTERFACTUAL R1 TARGET SCORE REVEALED**

Parent accepted scientific state:

- main `ce49de68a3bd308b9432f5904b5368fc4c6f9c8f`;
- Issue #68 published Naibbe R1 PASS;
- Issue #68 global result `NO TESTED FAMILY JOINT-CONSTRAINT COMPETITIVE`;
- Naibbe R2/R3/R4 remain frozen failures and are **not** being repaired here.

Stage-A authority:

- `SOURCE_AUDIT_PLAN.md`;
- `SOURCE_AUDIT_IMPLEMENTATION.md`;
- `SOURCE_AUDIT_MECHANICAL_FIX.md`;
- permanent target-blind machine audit under `source-audit/`;
- `source-audit/TARGET_ELIGIBLE_AXES.txt` defines the only axes allowed to enter target preflight.

No counterfactual 66-edge Q, residual-Z, energy, reliability, target correlation/sign agreement, R1 p-value or per-edge difference was available when this plan was committed.

## 1. Scientific question

> **Is the already-observed Naibbe R1 match primarily carried by the emitted Voynich-like codebook/inventory, by particular codebook associations/state allocations, or by plaintext/encryption-process dynamics?**

The published Naibbe result is already observed and is used only as a frozen reference. It is not treated as a new unseen candidate.

## 2. Common frozen R1 statistic

Every scored counterfactual uses the same R1 formalism as Issue #68:

- unchanged 12-slot `SlotParser(min)`;
- direct representation coverage gate `>=0.60`;
- all 66 unordered slot pairs;
- K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule-Q;
- candidate-owned 1,000 reference line-local nulls;
- independent 1,000 test line-local nulls;
- empirical mid-rank normal residual transform;
- residual energy `E=sqrt(mean(Z_e^2))`;
- fold reliability `W`;
- complete residual topology against both exact frozen ZL3b #58C and IT2a #58D pooled references.

Per-realization full R1 PASS requires exactly the frozen Issue #68 gates:

1. representation support already passed before R1 scoring;
2. at least four valid reliability folds;
3. `W >= .50`;
4. familywise `p_exist,maxT <= .01`;
5. for **both** ZL3b and IT2a:
   - Pearson `>= .70`;
   - correlation familywise `p_maxT <= .01`;
   - sign agreement `>=50/66`;
   - sign familywise `p_maxT <= .01`.

No selected edge can promote an intervention.

## 3. Stage-A eligibility rule

The only axes that may be scored are the exact nonempty lines committed in:

`source-audit/TARGET_ELIGIBLE_AXES.txt`

and only if their Stage-A machine record reports:

- deterministic generation completed;
- claimed causal invariant passed;
- direct parser coverage `>=0.60`;
- no target-dependent remapping.

An axis omitted from that file is `STAGE_A_SUPPORT_INELIGIBLE` and receives no R1 score.

This source-support selection happened before any counterfactual R1 quantity existed.

## 4. Primary deterministic intervention families

A single arbitrary counterfactual is insufficient. Each support-eligible axis receives the complete family below.

All intervention RNGs are local SHA-256-derived RNGs and do not consume the published encryption RNG before `encrypt_manuscript` reseeds it.

### P — plaintext-order family, 5 realizations

Purpose: test whether normalized plaintext sequence/bigram order is necessary.

For `r=0..4`, within every effective plaintext line preserve exact character multiset and length while shuffling character order.

- `r=0` is the exact Stage-A P0 intervention:
  `issue72:P:pilot0:{manuscript}:{item_id}:{line_index}`
- `r=1..4`:
  `issue72:P:family:{r}:{manuscript}:{item_id}:{line_index}`

After this intervention use the unchanged published encryption process/codebook and original realization-0 encryption seed.

Changed ambiguity retries/deck trajectory are treated as causal downstream effects of changed plaintext order, not held fixed.

### L — global effective-letter association family, 5 realizations

Purpose: test whether the published plaintext-letter ↔ glyph association is necessary.

For each `r`, construct one fixed-point-free permutation of the 23 effective letters and reuse it identically across every table/state mapping.

- `r=0`: exact Stage-A L0 label
  `issue72:L:pilot0:global-effective-letter-permutation`
- `r=1..4`:
  `issue72:L:family:{r}:global-effective-letter-permutation`

For every table×state pool the reachable glyph-value multiset must remain exactly unchanged.

### S — state-allocation family, both non-identity rotations

Purpose: test unigram/prefix/suffix specialization.

Use both nonidentity cyclic rotations of the frozen state order `[unigram,prefix,suffix]`:

- `S1`: shift +1; exact Stage-A S0 pilot;
- `S2`: shift +2.

Each table+effective-letter three-value multiset is preserved exactly.

### T — table-allocation family, all five non-identity cyclic rotations

Purpose: test which glyph values receive the published unequal table-selection probabilities.

Frozen table order:

`[alpha,beta1,beta2,beta3,gamma1,gamma2]`

Use shifts `+1,+2,+3,+4,+5`.

`T1` is the exact Stage-A T0 pilot.

Each state+effective-letter six-value multiset is preserved exactly; the published table-selection weights and RNG algorithm remain unchanged.

### G — global effective-cell association family, 5 realizations

Purpose: destroy structured letter/state/table association while preserving the complete reachable glyph-value multiset.

Operate on the 414 reachable cell instances in exact frozen state×table×effective-letter key order.

- `r=0`: exact Stage-A G0 label
  `issue72:G:pilot0:global-effective-cell-permutation`
- `r=1..4`:
  `issue72:G:family:{r}:global-effective-cell-permutation`

Duplicate glyph strings are permuted as cell instances. The 54 unreachable j/k/w cells remain fixed because they still participate in the published collision catalog; this fact must be retained in interpretation.

### I — exact published-token inventory family, 5 realizations

Purpose: upper-bound test of whether R1 is already carried by the emitted token inventory rather than plaintext/cipher lookup dynamics.

Start from the exact Issue #68 published primary rep0 surface. Preserve:

- exact complete whole-token multiset;
- every item/line token count;
- manuscript/item/line layout.

Permute whole token instances globally, then refill the exact line slots.

- `r=0`: exact Stage-A I0 label
  `issue72:I:pilot0:published-primary-token-instance-permutation`
- `r=1..4`:
  `issue72:I:family:{r}:published-primary-token-instance-permutation`

I is explicitly an **upper-bound inventory control**, not a neutral historical model.

## 5. Family support preflight before any R1 reveal

Before any counterfactual pair-Q is calculated, construct **all planned realizations** for every Stage-A-eligible axis and freeze:

- canonical surface SHA-256;
- visible/accepted token counts;
- direct parser coverage;
- ambiguity retries where applicable;
- claimed intervention invariants.

### Axis all-or-none rule

An axis proceeds to R1 only if **every planned realization**:

- generates successfully;
- preserves its nominated invariant;
- has direct parser coverage `>=0.60`.

Otherwise the entire axis is:

`FAMILY_SUPPORT_INELIGIBLE`

and none of its realizations receives an R1 pair/residual score.

This prevents selecting only favorable support realizations.

The exact list of target-scored axes/realizations and every primary surface SHA must be permanently archived before target code is authorized to calculate R1.

## 6. Candidate-owned finite-null namespaces

For every scored axis `A` and realization `r`, use disjoint namespaces:

Reference null replicate `n=0..999`:

`issue72:{A}:{r}:reference-null:{n}`

Independent test null replicate `n=0..999`:

`issue72:{A}:{r}:test-null:{n}`

Line ordering follows the same frozen manuscript → existing item → line → accepted-token ordering used in Issue #68.

No null calibration from published Naibbe, another counterfactual, ZL3b or IT2a may normalize a realization.

## 7. Familywise protection across the complete new counterfactual family

Let `C` be the set of **all realizations from all axes that passed the all-or-none support preflight**.

The set `C` is frozen before R1 and cannot shrink after a bad target result.

### Residual existence maxT

For test-null replicate index `n`, take:

`M_E[n] = max_{c in C} E_null[c,n]`

Each observed realization energy is evaluated against `M_E`.

### Topology maxT

For each test-null replicate `n`, compute every scored counterfactual null graph against both frozen target readings.

Correlation max:

`M_R[n] = max_{c in C, t in {ZL3b,IT2a}} R(Z_null[c,n], Z_target[t])`

Sign max:

`M_A[n] = max_{c in C, t in {ZL3b,IT2a}} sign_agreement(Z_null[c,n], Z_target[t])`

Every observed candidate↔target correlation/sign statistic is evaluated against these same family maxima.

No per-axis familywise reset is allowed.

## 8. Frozen published-Naibbe reference strength

The already-observed Issue #68 published primary reference is not included in the new maxT family.

Frozen published minimum topology across the two readings:

`B = min(0.8830282501011794, 0.9000974100381157) = 0.8830282501011794`

For each counterfactual realization `c`, define:

`M_c = min(R_c,ZL3b, R_c,IT2a)`

and relative topology:

`REL_c = M_c / B`.

This is descriptive/effect-size structure frozen before the counterfactual reveal. It does not replace the full R1 PASS gates.

## 9. Axis-level retention classes

For an axis with `N` planned/scored realizations, define:

- `FULL_PASS_COUNT` = number of realizations satisfying the complete familywise R1 PASS;
- `STRONG_COUNT` = number satisfying complete R1 PASS **and** `REL_c >= .90`;
- `MEDIAN_REL` = median `REL_c` across all axis realizations.

Threshold for family majority:

`Q = ceil(2N/3)`.

Axis class:

### `R1_RETAINED`

iff:

- `STRONG_COUNT >= Q`; and
- `MEDIAN_REL >= .90`.

### `R1_COLLAPSED`

iff:

- `FULL_PASS_COUNT = 0`; and
- `MEDIAN_REL < .70`.

### `R1_MODULATED`

otherwise, provided the full axis family was support-eligible and scored.

These `.90` / `.70` relative-effect bands are frozen prospectively and must not be changed after reveal.

## 10. Causal interpretation of each axis

- **P RETAINED**: within-line plaintext sequence/bigram order is not necessary for R1 under this architecture.
- **P COLLAPSED**: plaintext order and its downstream encryption trajectory materially matter.
- **L COLLAPSED**: global effective-letter association materially matters.
- **S COLLAPSED**: state specialization materially matters.
- **T COLLAPSED**: table allocation under unequal published weights materially matters.
- **G COLLAPSED**: structured cell association beyond the global reachable inventory materially matters.
- **I RETAINED**: the exact emitted-token inventory plus preserved line token-count layout is sufficient to reproduce R1 under the test, strongly downgrading R1 as evidence about plaintext/encryption dynamics.

`MODULATED` means the nominated component affects R1 strength but is neither clearly unnecessary nor clearly sufficient/necessary under the frozen effect bands.

## 11. Global decomposition classification

A definitive global class requires:

- I support-eligible and scored;
- P support-eligible and scored;
- at least one of L/S/T/G support-eligible and scored.

Otherwise:

`R1 DECOMPOSITION INCONCLUSIVE`

### `R1 IS PREDOMINANTLY CODEBOOK/INVENTORY-EMBEDDED`

if **I = `R1_RETAINED`**.

Because I removes plaintext/codebook lookup association while holding the exact published whole-token inventory and line token-count layout, this class has priority over the other axes. Other axis results are retained as secondary modulation evidence.

### `R1 DEPENDS MATERIALLY ON CODEBOOK ASSOCIATION/STATE STRUCTURE`

if:

- I = `R1_COLLAPSED`;
- P = `R1_RETAINED`; and
- at least one support-scored axis among L/S/T/G = `R1_COLLAPSED`.

### `R1 DEPENDS MATERIALLY ON ENCRYPTION/PLAINTEXT PROCESS`

if:

- I = `R1_COLLAPSED`; and
- no support-scored L/S/T/G axis is `R1_COLLAPSED`; and
- either P = `R1_COLLAPSED` **or** P = `R1_RETAINED`.

Interpretation differs by P:

- P COLLAPSED → plaintext sequence/process trajectory is implicated;
- P RETAINED → source order is unnecessary but the dynamic encryption schedule beyond static inventory is implicated.

### `R1 ORIGIN IS MIXED`

if:

- I = `R1_COLLAPSED` and both P and at least one L/S/T/G axis are `R1_COLLAPSED`; or
- I = `R1_MODULATED`; or
- the scored codebook/process axes show only modulation patterns that do not meet the clearer classes above.

### `R1 DECOMPOSITION INCONCLUSIVE`

if support completeness is insufficient for the required comparisons or a target execution/provenance failure prevents fair familywise evaluation.

No result may be reclassified by examining individual edge identities.

## 12. R2/R3/R4 boundary

This decomposition does **not** rescore counterfactual R2, R3 or R4 for promotion.

Published Naibbe remains frozen:

- R1 PASS;
- R2 FAIL;
- R3 FAIL;
- R4 FAIL;
- overall `NOT COMPETITIVE`.

A counterfactual preserving R1 cannot become a decipherment candidate in this phase.

## 13. Preflight firewall

Before first target reveal, code may:

- reconstruct every planned counterfactual surface;
- verify all support/invariant rules and exact SHA identities;
- freeze the scored family `C`;
- synthetic-test Q/residual/maxT aggregation code on synthetic arrays only;
- verify exact frozen #58C/#58D target authorities.

It may **not**, for any real counterfactual surface:

- compute any pair Q;
- compute residual Z/E/W;
- compare to ZL3b/IT2a;
- compute R1 p-values;
- inspect per-edge differences.

## 14. First-reveal protocol

After:

1. this plan is committed;
2. family-support preflight is permanently archived;
3. target scorer implementation is committed later;
4. synthetic target preflight passes with real scoring skipped;
5. exact target head is frozen;

one explicit auditable first-reveal event may score the complete frozen counterfactual family.

The exact raw per-realization artifacts, aggregate result, head/run/job IDs, null arrays and SHA-256 provenance must be permanently archived before interpretation.

No axis, realization, threshold, seed, codebook intervention, parser rule or null namespace may change after that event.

## 15. Interpretation boundary

Even `PROCESS` or `CODEBOOK ASSOCIATION` dependence would not identify Naibbe as the historical Voynich mechanism.

`INVENTORY-EMBEDDED` would not make the manuscript R1 result false; it would relocate its evidential role toward output-token grammar.

The objective is to locate the replicated R1 rule in the generative stack before using it to rank future inverse models.
