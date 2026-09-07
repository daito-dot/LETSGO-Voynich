# Issue #161 — outcome-only Currier factorization first-reveal provenance

Date: 2026-09-07
Status: **SCIENTIFIC FIRST REVEAL COMPLETE**

Frozen classification:

> **`NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`**

## Frozen chronology

- score-free Gate0 merged in PR #163 at `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`;
- post-Gate branch created from that exact merge;
- scientific scorer committed before any target workflow at `ecfa604519f1469eac289b9d200f9eedd6a24ddb`;
- frozen scorer blob `d24149977770118505f2147c5aa2bb727631906f`;
- first-reveal workflow added afterward at `fe1437e9a6985026b1fb9a19d7cb672c79effebd` and pins the scorer blob exactly;
- no Issue #161 target result was available when the outcome multiplier, class set, support rule, or 4/5 pass rule were frozen.

## Authoritative first reveal

- workflow: `Issue161 outcome-only Currier factorization first reveal`
- run: `34077382499`
- exact workflow head: `fe1437e9a6985026b1fb9a19d7cb672c79effebd`
- conclusion: `success`
- artifact ID: `10002558153`
- artifact ZIP digest: `sha256:844c990a764a88d22e5b1099031cae68db1fa2e2820ba68d4778c6864240170b`
- result JSON SHA-256: `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`

The workflow passed merged-Gate authority checks, exact source verification, target-free synthetic self-test, scientific scoring, foldwise Issue #158 reproduction, frozen classification assertions, and artifact upload.

## Reproduced authority

The scorer reproduced:

- Issue #161 Gate result SHA-256 `32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94`;
- Gate script blob `00e5bddc0484b9472bb4fce9dadb89dd52bf578f`;
- Gate provenance blob `67e91ba26a76898f679a5182828ab3e9f512d49a`;
- frozen plan blob `68cb29a11cb147c8ecd9e70b3349a4102744e0ed`;
- Gate merge `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- Issue #158 `G_Currier` exactly fold-by-fold within `1e-12` in all 20 reading × regime × fold cells.

For every cell, the decomposition identity also holds within `1e-12`:

`G_outcome + G_interaction = G_Currier`.

## Frozen comparison

For each reading `T`, Currier regime `R`, and outer fold:

- `EDGE_POOL`: exact Issue #158/#161 regime-neutral pooled edge;
- `EDGE_OUTCOME`: same edge plus the fixed training-only, context-invariant Currier next-initial multiplier `W_R(y)`;
- `EDGE_REGIME`: exact full target-regime matched edge.

Primary quantities:

`G_outcome = bits(EDGE_POOL) - bits(EDGE_OUTCOME)`

`G_interaction = bits(EDGE_OUTCOME) - bits(EDGE_REGIME)`.

`G_outcome` is the held-out information captured by the global Currier-specific next-initial bias. `G_interaction` is the residual requiring a Currier-specific previous-terminal × next-initial interaction after that global bias is supplied.

## Results

### Currier A — no context-specific residual

ZL3b:

- `G_outcome` by fold: `[+0.1207812891, -0.0260370441, +0.0822659591, +0.0832980295, +0.0815550380]`
- mean `G_outcome = +0.0683726543 bit/token`
- `G_interaction` by fold: `[-0.0143137700, -0.0042853384, -0.0232135309, +0.0049573617, +0.0113756762]`
- mean `G_interaction = -0.0050959203 bit/token`
- positive interaction folds `2/5` — FAIL
- reproduced mean Issue #158 `G_Currier = +0.0632767341`
- secondary outcome-capture ratio `1.0805338697`.

IT2a:

- `G_outcome` by fold: `[+0.1284535333, -0.0287675697, +0.0837136680, +0.0664269914, +0.1220427235]`
- mean `G_outcome = +0.0743738693 bit/token`
- `G_interaction` by fold: `[-0.0159951817, -0.0117848194, -0.0220055085, +0.0017102215, +0.0153367725]`
- mean `G_interaction = -0.0065477031 bit/token`
- positive interaction folds `2/5` — FAIL
- reproduced mean Issue #158 `G_Currier = +0.0678261662`
- secondary outcome-capture ratio `1.0965365358`.

Currier A therefore does not retain a robust context-specific residual in either reading. The context-invariant outcome factor slightly exceeds the mean gain of the full regime-specific table, so the negative residual is not evidence for an interaction of opposite sign; it means the fuller context-specific table does not improve held-out prediction over this lower-dimensional factorization under the frozen comparison.

### Currier B — weak ZL3b-only residual does not replicate

ZL3b:

- `G_outcome` by fold: `[+0.1211165700, +0.0885340022, +0.1112354582, +0.1060908904, +0.0429072711]`
- mean `G_outcome = +0.0939768384 bit/token`
- `G_interaction` by fold: `[+0.0243226024, +0.0007000749, +0.0098413648, +0.0126151268, -0.0113327145]`
- mean `G_interaction = +0.0072292909 bit/token`
- positive interaction folds `4/5` — PASS within ZL3b
- reproduced mean Issue #158 `G_Currier = +0.1012061293`
- secondary outcome-capture ratio `0.9285686456`.

IT2a:

- `G_outcome` by fold: `[+0.1197320924, +0.0864100464, +0.1140823484, +0.1097564738, +0.0467926623]`
- mean `G_outcome = +0.0953547247 bit/token`
- `G_interaction` by fold: `[+0.0303758645, -0.0013303030, +0.0116899524, +0.0116739340, -0.0063425102]`
- mean `G_interaction = +0.0092133875 bit/token`
- positive interaction folds `3/5` — FAIL within IT2a
- reproduced mean Issue #158 `G_Currier = +0.1045681122`
- secondary outcome-capture ratio `0.9118910409`.

The frozen rule requires the same Currier regime to pass independently in both readings. Currier B therefore does **not** qualify as a robust context-specific interaction. The small positive mean residual is similar across readings, but its fold-sign stability fails prospectively in IT2a.

## Cross-reading stability

Mean interaction differences are small:

- Currier A: `ZL3b - IT2a = +0.0014517829 bit/token`;
- Currier B: `ZL3b - IT2a = -0.0019840966 bit/token`.

The context-invariant outcome factor captures essentially all of the Currier-gate information in both transcription readings:

- A: about `108.1%` of the full mean Currier gain in ZL3b and `109.7%` in IT2a;
- B: about `92.9%` in ZL3b and `91.2%` in IT2a.

These ratios are secondary descriptive quantities, not separate pass criteria.

## Accepted interpretation

The frozen result supports the simpler predictive responsibility:

> **Under the common-EVA, reading-balanced, support-matched model family, the Currier A/B distinction in the same-line terminal→initial edge is adequately represented by a context-invariant Currier-specific bias over the next initial atom; no previous-terminal-specific Currier interaction survives the preregistered cross-reading robustness rule.**

Equivalently, the minimal live edge model can be compressed from separate Currier context×outcome tables to:

> **one shared terminal→initial base table + Currier-specific global next-initial bias.**

This substantially reduces the dimensionality assigned to Currier while retaining the established held-out predictive responsibility.

The result does **not** prove that previous-terminal context is irrelevant to the base edge itself; that base terminal→initial architecture remains strongly supported by earlier Issues. It says the **difference between Currier A and B** does not require a robust Currier×previous-terminal interaction under the frozen factorization.

## Interpretation boundary

This does not identify words, plaintext, semantics, language, cipher family, authorship, historical direction or mechanism, hoax/artificiality, or decipherment. It also does not prove that the frozen outcome multiplier is the unique or final low-dimensional parameterization of the Currier difference.

## Firewall

The artifact records all post-reveal change/tuning flags as false:

- no atom or context reselection;
- no multiplier change;
- no Currier relabeling;
- no support-match change;
- no alpha/smoothing/temperature/interpolation/fallback/mixture tuning;
- no hand/section/domain conditioning;
- no latent-state fit;
- no S1/S2/H62/R1 tuning;
- no semantic/cipher/historical inference.

Refs #88 #151 #155 #158 #161 #163 #164.
