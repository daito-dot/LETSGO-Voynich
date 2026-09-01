# Issue #72 — counterfactual family-support preflight implementation freeze

Status: **FROZEN BEFORE FAMILY-PREFLIGHT EXECUTABLE AND BEFORE ANY COUNTERFACTUAL R1 SCORE**

Authority:

- `PLAN_A.md`;
- target-blind Stage-A machine audit under `source-audit/`;
- `source-audit/TARGET_ELIGIBLE_AXES.txt`.

This note fixes only construction/support mechanics. It does not change any target statistic, intervention family, seed namespace, support gate, R1 gate or outcome classification.

## 1. Axis selection

Read exact nonempty axis codes from:

`source-audit/TARGET_ELIGIBLE_AXES.txt`

Allowed values are only `P0/L0/S0/T0/G0/I0`, mapped to target axis names `P/L/S/T/G/I`.

No axis absent from the Stage-A eligibility file may be generated for target promotion.

## 2. Published primary authority

Reconstruct the exact Issue #68 published rep0 surfaces first and require the same four per-manuscript and pooled SHA-256 identities already frozen in Issue #68.

All counterfactuals must start from the same frozen source/codebook authority.

## 3. Family realization construction

### P

Five realizations `r=0..4`.

- r0 uses exact Stage-A P0 per-line label.
- r1..r4 use the exact `PLAN_A.md` family labels.

For every source line, assert source-effective length and character multiset are exactly preserved.

### L

Five global 23-letter fixed-point-free permutations.

- r0 uses exact Stage-A L0 label.
- r1..r4 use exact plan family labels.

Use the Stage-A deterministic derangement algorithm unchanged. Assert every table×state reachable glyph multiset is exactly preserved.

### S

Two state rotations, shifts +1 and +2. Shift +1 must reproduce Stage-A S0 exactly.

### T

Five table rotations, shifts +1..+5. Shift +1 must reproduce Stage-A T0 exactly.

### G

Five 414-cell-instance permutations.

- r0 uses Stage-A G0 label.
- r1..r4 use the exact plan family labels.

Assert the complete reachable 414-value multiset is exactly preserved.

### I

Five global whole-token-instance permutations over the exact published primary rep0 output.

- r0 uses Stage-A I0 label.
- r1..r4 use the exact plan family labels.

Assert exact global token multiset and every item/line token-count layout are preserved.

## 4. Codebook/collision-catalog consistency

For L/S/T/G counterfactual encryption, the published encoder's derived `unigram_glyphs` and `bigram_catalog` must be rebuilt from the intervention codebook before encryption and restored afterward.

It is not sufficient to swap only `placeholder_to_glyph`, because ambiguity retries depend on those derived collision structures.

The preflight must assert that target-blind Stage-A realization-0 surface SHA-256 is reproduced for every Stage-A-eligible mapped axis.

## 5. Support all-or-none rule

For every planned realization report:

- canonical surface SHA-256;
- visible tokens;
- accepted tokens;
- direct `SlotParser(min)` coverage;
- generation diagnostics / ambiguity retries where applicable;
- invariant checks.

Axis is target-authorized iff **every** planned realization:

- completes;
- passes all declared invariants;
- has coverage >= `0.60`.

Otherwise none of that axis's realizations may receive R1 scoring.

## 6. Permanent family freeze output

Before target scorer code exists, preflight must permanently archive:

- exact Stage-A machine audit SHA;
- exact target-authorized axis list;
- exact target realization IDs;
- every realization surface SHA-256;
- coverage and retry diagnostics;
- deterministic intervention metadata sufficient to reconstruct each surface;
- explicit `counterfactual_R1_scored=false` and all forbidden R1 quantities false.

The later target executable must abort before pair-Q calculation if a regenerated surface differs from these SHA identities.

## 7. R1 firewall

This family-support preflight must not import/call pair/residual target code on real surfaces.

Forbidden until the later explicit target reveal:

- pair Q;
- residual Z/E/W;
- target correlations/sign agreements;
- R1 p-values;
- per-edge differences.
