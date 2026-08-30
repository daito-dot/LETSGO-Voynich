# Phase 57 plan — residual robustness gate

Status: pre-execution plan. Frozen before robustness testing.

## Objective

Determine whether the Phase56D cross-fitted paragraph residual is a stable manuscript property or an artifact of token-unit definition, matched-window length, incomplete structural prediction, or resampling choices.

No semantic/content/cipher interpretation is permitted during this phase.

## Frozen tests

### 57A — representation sensitivity
Recompute matched paragraph fingerprints and residual structure under at least three token representations:
1. Phase56 collapsed EVA-unit representation;
2. raw EVA character representation;
3. conservative composite representation using only the longest established multi-character units (`cth/ckh/cph/cfh/ch/sh`).

Compare residual-subspace alignment, reliability, and broad-label leakage.

### 57B — window-length sensitivity
Repeat matched fingerprints at feasible fixed body-token windows (target 15, 20, 30, 40 tokens, with eligibility reported separately). Test whether leading residual axes and page/paragraph relationships persist rather than appearing only at one estimator scale.

### 57C — richer leakage-safe structural prediction
Compare the Phase56 metadata+page-context baseline against predictors that may legitimately encode known structure without using the target paragraph itself:
- section / Currier / hand / paragraph ordinal;
- other paragraphs on same page-side;
- opposite page-side on same physical leaf where available;
- adjacent physical leaves under exact metadata matching;
- paragraph length/line-count descriptors computed independently of target token identity where safe.

All evaluation grouped by physical leaf. Hyperparameter/model selection must remain inside training folds.

### 57D — residual stability
For each accepted perturbation/model:
- split-half reliability;
- cross-fitted residual variance;
- top-k residual-subspace principal angles;
- section/Currier/hand eta2 leakage;
- same-page / same-leaf / adjacent-leaf residual similarity;
- stability of paragraph-entry trajectory after nuisance prediction.

## Frozen hypotheses

### H57-1 — representation-stable residual
A substantial residual subspace remains aligned across reasonable token-unit definitions.

Falsified if the dominant residual directions rotate arbitrarily or disappear when representation changes.

### H57-2 — scale-stable residual
Residual structure persists across matched window lengths rather than depending on one 20-token estimator.

Falsified if reliability/alignment collapses outside the original window length.

### H57-3 — not merely omitted local state
Richer leakage-safe physical/page context does not explain away most of the reliable residual.

Falsified if held-out residual variance collapses once same-leaf/adjacent context is added.

### H57-4 — residual broad-label neutrality
Leading residual structure remains only weakly associated with section/Currier/hand after cross-fitting.

Falsified if stronger nuisance models reveal that the residual was mainly unmodeled broad metadata structure.

## Gate decision

Only if H57-1/2/3 survive sufficiently and H57-4 remains acceptable may the residual become the target of renewed semantic/content/cipher tests.

Failure is informative: if residual structure is representation- or scale-specific, return to structural modeling rather than interpret it.
