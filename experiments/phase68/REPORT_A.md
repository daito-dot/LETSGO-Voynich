# Phase 68A — formal-residual lexical/family selection

Status: **CLOSED — NOT SUPPORTED**

## Question

Phase67C removed tokens directly compatible with the strongest established formal channels and still found no image relation in the remaining character surface. Phase68A moved one representational level higher:

> Do the sealed plant attributes predict which recurrent retained token identities or one-edit lexical neighborhoods are selected in the paired paragraph?

Two morphology-blind text lanes were frozen before association:

1. exact retained-token identity;
2. exact-or-edit1 neighborhoods around recurrent retained token anchors.

The four image characters remained unchanged: leaf composition, leaf arrangement, leaf margin, and root/subterranean architecture.

## Text feasibility

The lexical representation was not sparse enough to block the test:

- formal-mask retained tokens: **423**
- retained distinct token types: **279**
- exact recurrent vocabulary (document frequency >=2): **59**
- exact-token lane nonzero paragraphs: **14 / 14**
- edit1-anchor lane nonzero paragraphs: **14 / 14**

The workflow also verified that the edit-distance-1 function used by the Phase67/68 mask is source-identical to the historical Phase61C implementation.

## Primary result

Eight preregistered cells were tested: four image characters × two lexical lanes. The exact within-folio null reassigns complete paragraph representations across all **1,152** allowed assignments and uses the maximum RV across the eight cells.

The largest observed cell was:

- image character: `leaf_arrangement`
- text lane: `edit1_anchor_family`
- RV: **0.52020**

Family-corrected result:

- global exact p = **0.99392** (1,145 / 1,152 assignments at least as large)
- image coverage gate: pass

The result is not borderline. The observed maximum is far below the null distribution:

- null mean maxT: **0.60323**
- null 95th percentile: **0.67910**
- null maximum: **0.69934**

Even before family correction, no individual cell was close to significance. The smallest uncorrected cell p was **0.38542** for leaf arrangement × exact-token identity.

## Retention-fraction control

After residualizing lexical vectors on paragraph formal-mask retention fraction:

- winning cell: root/subterranean architecture × exact-token identity
- maxT: **0.50434**
- eight-way exact p: **0.84983**

This does not uncover hidden lexical selection.

## Decision

Phase68A is classified:

> **NOT SUPPORTED**

The combined object-local content program now has negative results at several distinct levels:

- image morphology -> attached short-label structure: null;
- image morphology -> immediate body character structure: null;
- leaf and root morphology separately -> body surface: null;
- image morphology -> character structure after masking entry/edit1-compatible formal tokens: null;
- image morphology -> exact retained lexical identity / edit1 lexical neighborhoods: null.

The positive external botanical control showed that the general image-to-description machinery can detect genuine morphology correspondence. The current Voynich negatives therefore should not be treated as a generic failure to measure images.

This is the stopping point for repeated representational tweaks on the same 14 Quire 19 object-local pairs. Continuing to change tokenization, morphology traits, or similarity metrics on this population would become post-hoc search rather than a clean prospective program.

The next frontier must change the scientific model. Live alternatives include:

1. **page/recipe-level content organization** rather than one illustration block -> one paragraph;
2. **nonlocal reference/indexing**, where labels or illustrations point elsewhere;
3. **meaningful plaintext transformed by shorthand/cipher/obfuscation**, so semantic relation is not expected to survive as local surface similarity;
4. content dimensions not represented by visible morphology, such as preparation, use, quantity, or process.

Given the independently strong A1-like formal layer and the current content nulls, the highest-value next test is a bounded meaningful-text + deliberate-obfuscation mechanism that makes prospective structural predictions rather than another local image/text correlation.

## Provenance

- GitHub Actions run: `33383915585`
- job: `99462131137`
- scientific head: `919f7a85fc3f14a13ec421970ee17106a80a58af`
- artifact ID: `9754810200`
- artifact SHA-256: `d8cec404ce38d7cc677d51267aaaa1460cd9c584bfcc81f5a2408afdfafc3029`
- result SHA-256: `e159fd20dd0225f91ec9cdc5381ed2288858f154a47d79ebe67cd24c6d762817`
