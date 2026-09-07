# Issue #191 Stage 1 first-reveal provenance

Date: 2026-09-08  
Issue: #191  
Parent: #172  
PR: #193

## Scientific first reveal

The first reveal is permanently identified by:

- final prereveal plan commit: `5e80d48cababb94a346dce4d1e34a910ec22ae65`
- preregistered scorer commit: `67310515ba1778f5e8ceb844087665324354c513`
- first-reveal workflow / exact tested head: `f6292dcb28242c2353f5b85f4a02d4e52067b126`
- workflow run ID: `34169742362`
- job ID: `101887636004`
- conclusion: `success`
- artifact name: `issue191-productivity-stage1-first-reveal`
- artifact ID: `10035428581`
- artifact ZIP SHA-256: `fcc399fa9c7671086a05e013ecabd8cf43c77936aba01bcb3d72df082c7fa560`
- raw `issue191_stage1_results.json` SHA-256: `1cafbb568e278ee2d4ae9863b62d6a228eeeed656ad90464edba90f1efa455f0`
- raw result size: `292460` bytes

GitHub's artifact metadata independently reports digest `sha256:fcc399fa9c7671086a05e013ecabd8cf43c77936aba01bcb3d72df082c7fa560`, matching the downloaded ZIP.

Archive-only commits after `f6292dcb...` do not replace this scientific first reveal.

## Frozen outcome

- `outcome_label = PRODUCTIVE_FORMS_PRESENT_BUT_FINITE_NULL_NOT_REJECTED`
- `label_resolution = FROZEN_LABEL`
- `r11_promoted = false`

Promotion-gate vector:

```text
observed_nonzero_every_fold: ZL3b=true, IT2a=true
C2 both primary tests p<=0.01: ZL3b=false, IT2a=false
C3 nonzero every rep/every fold: ZL3b=true, IT2a=true
observed/V2 mean OOV ratio: ZL3b=1.0085887943776193, IT2a=0.9952797098403523
ratio within [0.5,2.0]: ZL3b=true, IT2a=true
```

The sole promotion failure class is C2: the finite observed-inventory null is not rejected under both frozen primary statistics in both readings.

## Exact primary scientific values

### ZL3b

- support: visible `32570`, parsed `25071`, rejected `7499`, physical leaves `99`
- parsed folds: `[4430,4810,5516,5447,4868]`
- observed mean five-fold OOV: `0.07034275261192202`
- total fold-novel distinct incidence: `1638`
- C2 mean-OOV p: `0.07392607392607392`
- C2 novel-incidence p: `0.2547452547452547`
- C3 V2 mean OOV: `0.0697437379872232`
- observed/V2 mean OOV: `1.0085887943776193`
- C3 strong nonzero gate: `true`

### IT2a

- support: visible `34411`, parsed `28280`, rejected `6131`, physical leaves `99`
- parsed folds: `[4976,5416,6261,6197,5430]`
- observed mean five-fold OOV: `0.06381383564931845`
- total fold-novel distinct incidence: `1661`
- C2 mean-OOV p: `0.003996003996003996`
- C2 novel-incidence p: `0.03196803196803197`
- C3 V2 mean OOV: `0.06411648405808905`
- observed/V2 mean OOV: `0.9952797098403523`
- C3 strong nonzero gate: `true`

## Structural checks

Every fold-novel distinct canonical type in both readings uses only `(slot,value)` units present in its training folds:

- ZL3b: `1638 / 1638`
- IT2a: `1661 / 1661`

Known occupied-slot-shape counts:

- ZL3b: `1428 / 1638`
- IT2a: `1437 / 1661`

Character-level edit-distance-one counts:

- ZL3b: `1575 / 1638`
- IT2a: `1593 / 1661`

These annotations are non-exclusive as preregistered.

## Authority statement

The run passed all exact source, repository-code, parser, support, fold, deterministic-control, generated-reparse, and numerical-finiteness admission gates before interpretation. ZL3b and IT2a remain alternate readings of one manuscript and are not counted as independent manuscript evidence.

The full machine-readable authority is the immutable Actions artifact identified above. `ISSUE191_STAGE1_SUMMARY.md` is a human-readable derivative and does not supersede the artifact.