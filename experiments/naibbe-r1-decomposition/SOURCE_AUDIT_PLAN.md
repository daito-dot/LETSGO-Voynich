# Issue #72 Stage A — Naibbe R1 source / architecture audit plan

Status: **PREREGISTERED BEFORE AUDIT EXECUTABLE AND BEFORE ANY COUNTERFACTUAL R1 SCORE**

Parent scientific authority:

`ce49de68a3bd308b9432f5904b5368fc4c6f9c8f`

Issue #68 already revealed that published Naibbe C1-E0 passes the complete-66 R1 constraint against both ZL3b and IT2a while failing R2/R3/R4.

The objective now is causal decomposition of that R1 success, not another fit contest.

## 1. Stage-A question

> **Which independently manipulable layers exist between Latin source text and emitted Voynich-like Naibbe tokens, and which counterfactual interventions can change one layer while preserving the others well enough for a fair complete-graph R1 test?**

Stage A is source/representation-only. It does not score any new counterfactual against the manuscript.

## 2. Exact source authority to re-audit

Naibbe:

- repository `greshko/naibbe-cipher`;
- commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`;
- encoder `naibbe_v2.py`, expected blob `b566ad82e4b6ff0782ecdddebf77718dac44f292`;
- codebook `references/naibbe_tables.csv`, expected blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`;
- decoder `decrypt_naibbe.py`, expected blob `b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b`.

Plaintext control authority remains the four frozen CREMMA manuscripts at:

`292525969ad98380b398e6606a9c2a36d51913ae`.

Issue #68 pretarget surface authority remains:

- BIS193 rep0 SHA `fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805`;
- CLM13027 `da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77`;
- Mazarine915 `2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d`;
- UBL758 `5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89`;
- pooled `47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`.

Stage A must reproduce these identities without computing pair associations.

## 3. Architecture layers to enumerate

Audit the exact published encoder call graph and identify these layers separately:

### L0 — source cleaning / effective alphabet

- `clean_line` behavior;
- source spaces/punctuation removal;
- `W→UU`, `J→I`, `K→C` behavior and where it occurs;
- Phase64B drop-only projection to the supported effective alphabet;
- effective reachable plaintext letters.

### L1 — plaintext sequence

- per-line normalized character sequence;
- character marginal counts;
- adjacent-character/bigram sequence as an **input object only**;
- no comparison to Voynich target statistics.

### L2 — plaintext segmentation

- exact mechanism deciding one- versus two-character plaintext units;
- `RESPACING` role;
- RNG call(s) and whether the decision depends on character identity or only position/randomness.

### L3 — table selection

- six published tables;
- exact 78-card weighting / selection mechanism;
- RNG call(s);
- dependence or independence from plaintext identity.

### L4 — state-specific lookup

- `unigram`, `prefix`, `suffix` states;
- how unigram and bigram plaintext units choose states;
- exact table × state × letter lookup interface.

### L5 — codebook inventory / association

For the 23 effective plaintext letters, report without R1 scoring:

- total reachable table × state × letter cells;
- distinct glyph strings overall;
- duplicate glyph strings and multiplicity;
- distinct counts by table and by state;
- overlap of glyph strings across states/tables;
- raw glyph-string length distributions;
- direct unchanged `SlotParser(min)` acceptance rate for individual reachable codebook cell values;
- direct parser acceptance by state/table.

Parser acceptance is an interface/support audit only. Do **not** calculate slot occupancy associations among cells.

### L6 — ambiguity/collision rejection

- exact `UNAMBIGUOUS` gate;
- which generated token combinations are rejected/retried;
- whether rejection depends on codebook values, plaintext identity, state/table or previous output;
- exact retry counter behavior.

### L7 — ciphertext spacing

- exact published 3% space-removal step;
- whether it concatenates whole already-encrypted tokens;
- RNG dependency;
- separation from codebook lookup.

## 4. Counterfactual causal axes to test for implementability

Stage A must decide whether each axis can be intervened on **without consulting any Issue #68 per-edge R1 pattern**.

### P — plaintext-order intervention

Desired causal change:

- destroy normalized plaintext sequence/bigram order;
- preserve each frozen source unit's character multiset and length as prospectively defined;
- leave codebook, segmentation algorithm, table selection, state lookup and output-spacing algorithm unchanged.

Audit whether this can be done before encoder segmentation with a separate deterministic intervention RNG namespace.

### L — letter-association intervention

Desired causal change:

- preserve plaintext sequence;
- preserve the exact glyph multiset available in each nominated table/state pool;
- break the published plaintext-letter → glyph association by a deterministic permutation of effective letter keys;
- leave segmentation/table/state logic unchanged.

Audit whether one **global effective-letter permutation reused across all table/state mappings** and/or independent within-pool permutations are cleanly implementable. Stage A may report both designs, but target PLAN_A must choose prospectively before scoring.

### S — state-allocation intervention

Desired causal change:

- preserve plaintext sequence, tables and each table+letter's three published glyph values;
- permute the assignment of those values among `unigram/prefix/suffix` states under a deterministic derangement/rotation;
- leave table selection and letter identity unchanged.

Audit whether this isolates state specialization cleanly without changing the global glyph inventory.

### T — table-allocation intervention

Desired causal change:

- preserve plaintext sequence and state identity;
- preserve each state+letter's six published table values;
- permute their table allocation under a deterministic table permutation;
- leave table-selection weights and RNG schedule unchanged.

Audit whether this isolates table-specific allocation cleanly.

### G — global-cell inventory intervention

Desired causal change:

- preserve the complete multiset of reachable codebook glyph values and the original process schedule;
- reassign glyph values across the full effective table×state×letter cell set using a deterministic permutation;
- destroy published letter/state/table association while preserving overall inventory exactly.

Audit whether this is mechanically valid and whether duplicate values create any representational ambiguity in defining a cell permutation.

### I — inventory-only emission control

Desired causal change:

- remove plaintext/cipher lookup dynamics while retaining a prospectively defined codebook-token sampling law and original line/token-count layout;
- ask whether the emitted-token inventory alone is sufficient for R1.

Stage A must **not** choose an empirical sampling law by looking at R1. It may enumerate outcome-independent options such as:

1. uniform reachable-cell sampling under the published state/table capacity;
2. sampling from the published primary output token histogram (not R1 edges), if used only as an explicit upper-bound inventory control;
3. a process-schedule replay in which plaintext lookup is replaced by a frozen source-marginal letter draw.

Target PLAN_A must choose at most one primary inventory-only definition before scoring.

## 5. Deterministic intervention family requirement

A single arbitrary random permutation is not sufficient evidence.

Stage A must identify an outcome-independent way to generate a small fixed family of deterministic intervention realizations, e.g. public SHA-256-derived permutations with predeclared labels/indices.

The later target plan must freeze:

- number of primary intervention realizations per axis;
- exact labels/seeds/permutation construction;
- whether the primary family statistic is median, minimum, maximum, pass-count or another prospectively defined aggregate;
- familywise correction across axes/realizations/readings.

Stage A may inspect only permutation validity/support, never R1 target performance.

## 6. Support screen allowed in Stage A

For a proposed intervention implementation, Stage A may generate candidate surfaces solely to audit:

- deterministic reproducibility / SHA identity;
- output token count and line count;
- encoder completion / retry failures;
- direct unchanged `SlotParser(min)` coverage;
- state/table/cell usage counts needed to prove the intervention preserved its nominated invariants.

Prospective support rule for target eligibility:

- surface generation completes under the frozen published algorithm;
- no hidden target-dependent remapping is required;
- direct parser coverage is at least `0.60`, inherited from Issue #68;
- the intervention preserves every invariant claimed by its causal definition.

An intervention failing this support screen is representation/invariant-ineligible. It may not be repaired after R1 reveal.

## 7. Strictly forbidden during Stage A

For every new intervention surface, do not compute or expose:

- 2×2 pair tables;
- any of the 66 Yule-Q values;
- `K_other`-conditional pair association;
- candidate residual-Z values;
- residual energy;
- cross-fold reliability based on residual graphs;
- correlation/sign agreement to ZL3b, IT2a or published Naibbe R1;
- R1 p-values;
- per-edge difference diagnostics.

No code path used in Stage A should import/call the pair/residual scoring functions on real intervention surfaces.

## 8. Stage-A outcome

Stage A ends with an architecture/source audit and a finite list of **causally interpretable, support-eligible intervention families**.

Only then may a separate `PLAN_A.md` choose the primary interventions and freeze the complete-graph R1 target statistics, nulls, familywise correction and outcome classification.

If no clean counterfactual separates codebook inventory from process dynamics, the correct Stage-A result is `DECOMPOSITION DESIGN NOT IDENTIFIABLE`, not an improvised R1 test.

## 9. Interpretation boundary

This phase cannot establish historical Naibbe use or plaintext even if process-specific effects are found.

Its sole purpose is to determine **where in the generative stack the already-observed R1 match is encoded**, so future inverse-model discrimination uses R1 at the correct evidential level.
