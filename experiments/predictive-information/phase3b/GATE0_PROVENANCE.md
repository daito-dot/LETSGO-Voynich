# Issue #107 Phase 3B — observable metadata Gate 0 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE METADATA/SUPPORT AUDIT**
Parent: Issue #88

## Purpose

This Gate asks whether pre-existing IVTFF hand/domain metadata are sufficiently crossed with Currier A/B to support a prospective conditional-transport test of the Phase-3A PREV_PARAS strength difference.

No predictive probability, code length, S1/S2/H62/R1, Issue #84 target, imagery, plaintext/semantics or latent state is available to the audit.

## Frozen authority and resolution

- source: frozen ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- corrected causal order: `source_order_authority.py`;
- Currier A/B: merged Phase-3A `$L` authority;
- `$I`: IVTFF illustration type;
- `$H`: Lisa Fagin Davis writing hand;
- `$C`: legacy Currier hand.

The Gate prospectively resolves legal page-header `@` values using `<@X=v>` line text tags. One page (`f115r`) contains the only observed H-tag sequence; it switches H=2/H=3. No tag conformance violation was found.

## Authoritative workflow

- run: `34021902892`
- scientific head: `715e7231b8267c91daecae8de8747a56447581c9`
- conclusion: `success`
- artifact: `issue107-phase3b-metadata-gate0`
- artifact ID: `9985775083`
- artifact digest: `sha256:d02fa51aae15072f5dd451558119e5fef75375d01a2180c39c98449d901cdebd`
- result JSON SHA-256: `8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717`

## Mapping and conformance gates

The source-level metadata scanner exactly reconstructs the current parsed population:

- visible tokens expected/scanned: `32,570 / 32,570`;
- parser-accepted tokens expected/scanned: `25,071 / 25,071`;
- line-mapping mismatches: 0;
- metadata tag conformance violations: 0;
- raw resolved L vs Phase-3A Currier authority mismatches: 0;
- corrected numeric paragraph order: valid;
- corrected raw page/panel order: valid.

## Raw page-header distributions

### Davis writing hand `$H`

- H1: 113 pages
- H2: 46
- H3: 33
- H4: 26
- H5: 7
- `@`: 1

### Illustration type `$I`

- A: 8
- B: 19
- C: 10
- H: 129
- P: 16
- S: 25
- T: 7
- Z: 12

### Legacy Currier hand `$C`

- C1: 86
- C2: 45
- C3: 6
- C4: 8
- C5: 6
- X: 6
- Y: 2
- missing: 67

## Frozen identifiability result

Gate classification:

> **NO ADEQUATELY CROSSED OBSERVABLE FACTOR**

No factor satisfies the preregistered requirement of at least two levels that each occur in both Currier A and B with >=4/5-fold support on both sides.

### `$H` Davis hand

No hand level is cross-Currier usable.

The dominant confounding is almost complete:

- H1: A `7,274` accepted tokens / 5 folds; B `0`;
- H2: A `0`; B `8,422` / 5 folds;
- H3: A `426` / 1 fold / 1 leaf; B `8,050` / 5 folds;
- H5: A `0`; B `549` / 4 folds.

Thus the current corpus cannot distinguish Currier-associated PREV strength from writing-hand effects by a properly crossed H-conditioned test.

### `$C` legacy Currier hand

No C level is cross-Currier usable; the main levels are fully separated:

- C1: A `5,141`, B `0`;
- C2: A `0`, B `7,360`;
- other C levels are similarly one-sided/sparse.

### `$I` illustration/domain

Exactly one level is well crossed:

- `I=H` (Herbal): A `5,520` accepted tokens across 47 leaves / 5 folds; B `2,449` across 16 leaves / 5 folds.

All other informative I levels are Currier-asymmetric or too sparse:

- Biological B: A `0`, B `4,936` / 5 folds;
- Pharmaceutical P: A `1,608` / 5 folds, B `0`;
- Stars S: A `426` / 1 fold, B `7,748` / 5 folds;
- Text-only T: A `146` / 1 fold, B `1,550` / 2 folds;
- Cosmological C: A `0`, B `338` / 2 folds.

Because only one I level crosses adequately, `$I` cannot be used as a multi-level factor to estimate an independent domain effect under the frozen rule.

## Leaf mixing

- Currier L: 0 mixed leaves;
- legacy hand C: 0 mixed leaves;
- Davis hand H: 1 mixed leaf (`f115`, H2/H3 via text tags);
- illustration I: 7 numeric leaves contain more than one illustration level.

## Consequence

The Gate does **not** license a multilevel H/I/C conditional predictor.

However, the audit identifies one prospectively usable matched-domain subset that was not selected by prediction: `I=H` (Herbal) has substantial Currier A and B support in all five frozen folds.

A new, separately frozen experiment may therefore ask whether the Phase-3A A/B PREV_PARAS strength difference persists **within the common Herbal domain only**. This is a support-preserving matched-domain test, not a fitted illustration-state model.

No hand-conditioned causal interpretation is licensed because H and Currier are not adequately crossed.