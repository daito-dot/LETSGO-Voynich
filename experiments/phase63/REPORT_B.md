# Phase 63B report — independent-transcription replication

Status: **completed; frozen strong replication criteria pass**.

This report interprets the exact first-reveal result in `phase63b_science_results.json`. Exact method authority remains `PLAN_B.md`, `IMPLEMENTATION_B.md`, `PARSER_AMENDMENT_B1.md`, the frozen executable `phase63b_science.py`, and the committed raw result.

## 1. Scientific question

Phase63B tested the highest-value remaining robustness objection after Phase63A:

> Are the strongest paragraph-entry / near-family recurrence findings, and the frozen A1-R1 mechanism advantage, artifacts of the ZL3b/EVA transcription and segmentation conventions?

This was an external representation/transcription challenge, not an A2 mechanism-development phase.

No A2, C1, M0, cross-alphabet mapping, post-result normalization, parameter repair or model retuning was allowed.

## 2. Chronology firewall

The result was revealed only after the following were committed:

1. exact independent source identities and hashes;
2. W1 primary and W2 sensitivity word-space rules;
3. source-native paragraph/line/physical-leaf parsing;
4. native v101 / EvaT glyph-unit handling;
5. the common five Phase62 physical-leaf folds;
6. GC-R1/R2 and IT-R1/R2/R3 metrics and pass/fail rules;
7. a parser-only B1 preflight with no edit1/features/S1/S2/S3/H62-P1/A1 computation;
8. the complete scientific executable and deterministic seed labels.

The initial strict parser preflight exposed only a ZL Eva- syntax compatibility issue (`'` and `0` inside frozen ZL tokens). `PARSER_AMENDMENT_B1.md` froze that correction before any Phase63B scientific metric was implemented or computed.

The parser freeze was merged to main at `af989f9ae22b3d4a2c6352551b13a2cdd144b190` before the scientific branch was created.

The first-reveal scientific head was:

`31746c4d318929b602b35c288e36e83001200509`

## 3. Frozen external sources

- **ZL3b** discovery/reference lineage: mirror blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.
- **GC2a** independent v101 transcription: SHA-256 `b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f`.
- **IT2a** independent EvaT transcription: SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`.
- **CREMMA medieval Latin controls:** commit `292525969ad98380b398e6606a9c2a36d51913ae`.

GC is the stronger **independent-alphabet observational** challenge because it stays in native v101 and is never converted to EVA. IT is the **independent-reading full-transfer** challenge because its native EvaT representation permits the frozen A1 machinery to be applied without inventing a v101→EVA mapping.

## 4. Preflight population identity

The scientific executable re-verifies the successful B1 parser-only population counts before calculating any scientific metric.

W1 primary:

| source | paragraphs | lines | tokens | types | base eligible | S1 eligible | leaves |
|---|---:|---:|---:|---:|---:|---:|---:|
| ZL3b | 740 | 4,115 | 34,360 | 6,895 | 597 | 436 | 99 |
| GC2a | 775 | 4,130 | 36,658 | 8,602 | 633 | 448 | 99 |
| IT2a | 772 | 4,117 | 34,411 | 7,069 | 602 | 440 | 99 |

Thus the replication is not driven by a tiny overlapping subset.

## 5. GC independent-alphabet observational replication

### GC-R1 — paragraph-entry specialization

Frozen W1 criterion: positive held-out real-minus-pseudo projection in at least 4/5 folds and positive mean; W2 must not reverse the mean sign.

W1 results:

- positive folds: **5/5**;
- mean projection: **1.00905**;
- median: **1.22629**;
- fold values: `1.22629 / 1.07212 / 0.26245 / 1.24581 / 1.23860`.

W2:

- positive folds: **5/5**;
- mean projection: **1.08374**.

**GC-R1 passes.**

The weaker fold2 effect is retained rather than repaired.

### GC-R2 — H62-P1 recurrence geometry

W1:

- positive `C_short` folds: **5/5**;
- mean `C_short`: **0.58781**;
- median: **0.56350**;
- fold values: `0.74045 / 0.59950 / 0.49087 / 0.56350 / 0.54473`.

W2:

- positive folds: **5/5**;
- mean `C_short`: **0.59868**.

Mean native-profile distance to strict-parser ZL under the same view:

- W1 `D_profile`: **0.45180**;
- W2 `D_profile`: **0.49456**.

**GC-R2 passes.**

This is important because edit-distance families were reconstructed directly in the independent v101 alphabet; no glyph conversion was introduced to make the result resemble EVA.

## 6. IT independent-reading observational replication

### IT-R1

W1:

- positive folds: **5/5**;
- mean projection: **0.77003**;
- median: **0.76769**;
- fold values: `0.69971 / 1.26037 / 0.15871 / 0.76769 / 0.96369`.

W2 is identical for R1 because IT2a contains no uncertain comma-space distinctions affecting this population.

**IT-R1 passes.**

### IT-R2

W1:

- positive `C_short` folds: **5/5**;
- mean `C_short`: **0.58501**;
- median: **0.56375**.

W2:

- positive folds: **5/5**;
- mean `C_short`: **0.59326**.

Mean profile distance to strict-parser ZL:

- W1: **0.33870**;
- W2: **0.32731**.

**IT-R2 passes.**

The same fold2 weakening in entry projection remains visible (`0.15871`) but does not change sign.

## 7. IT-R3 — frozen A1-R1 full transfer

This is the strongest Phase63B mechanism test.

For each fold, A1 receives only:

- IT training-leaf vocabulary;
- IT training-leaf edit1 neighbor graph;
- IT training paragraph-entry shape scores;
- IT held-out paragraph/line/token-count layout;
- the exact Phase61C parameter pair selected historically on ZL;
- the exact historical five generator seeds.

No IT result is used to retune the parameters.

### 7.1 Exposed common scorecard — W1 primary

IT target across-fold means:

- S1 `0.77003`
- S2 `0.04699`
- S3 `0.02657`

A1-R1 means:

- S1 `0.56769`
- S2 `0.07453`
- S3 `0.01719`

Ratio-of-means A1-R1 / IT:

- **S1 0.73723×**
- **S2 1.58617×**
- **S3 0.64696×**

All three pass the frozen aggregate `[0.5, 2.0]` gate.

W2 ratios are essentially the same: `0.73723 / 1.59123 / 0.64696`.

### 7.2 H62-P1 — W1 primary

| candidate | mean D_profile | median D_profile | mean |ΔC_short| |
|---|---:|---:|---:|
| N0 | 1.47727 | 1.47518 | 0.62192 |
| fixed C0-4 | 1.79735 | 1.75476 | 1.29206 |
| **A1-R1** | **0.83028** | **0.92972** | **0.07184** |

Fold wins for A1-R1:

- versus N0: `D_profile` **4/5**, `|ΔC_short|` **5/5**;
- versus fixed C0-4: **5/5 on both metrics**.

The only H62-P1 `D_profile` loss is fold2:

- N0 `1.19208`
- A1-R1 `1.24428`

A1 nevertheless has a far smaller fold2 `|ΔC_short|` (`0.11114` vs N0 `0.63816`). This failure is retained explicitly.

### 7.3 W2 sensitivity

A1-R1 remains the best tested candidate on the frozen aggregate diagnostics:

- mean `D_profile`: **0.85525**;
- mean `|ΔC_short|`: **0.08292**;
- versus N0: D wins **4/5**, C-short wins **5/5**;
- versus C0: **5/5 on both**.

The frozen IT-R3 criterion passes under **both W1 and W2**.

## 8. Important heterogeneity retained

Phase63B is a strong aggregate/external replication, not a universal fold-wise exact match.

In W1 IT-R3, individual exposed ratios include:

- fold1 S1 `0.424×`;
- fold2 S1 `3.927×`;
- fold3 S2 `2.230×`;
- fold0/fold1/fold4 S3 approximately `0.473 / 0.497 / 0.414×`.

The frozen criterion was explicitly **ratio-of-means**, not an all-fold `[0.5,2]` requirement. These deviations therefore do not retroactively fail Phase63B, but they remain evidence that A1 is not a complete generator.

## 9. Frozen Phase63B verdict

All preregistered primary components pass:

- GC-R1: **PASS**
- GC-R2: **PASS**
- IT-R1: **PASS**
- IT-R2: **PASS**
- IT-R3 W1 primary: **PASS**
- IT-R3 W2 sensitivity: **PASS**
- no W2 observational mean-sign reversal

Frozen classification:

> **STRONG REPLICATION — GC independent-alphabet observational effects and IT independent-reading observational/full A1-R1 transfer pass the frozen W1 criteria without W2 observational sign reversal.**

## 10. What Phase63B changes

Before Phase63B, a major live objection was that the strongest Phase60–63 effects could be consequences of ZL3b/EVA transcription, glyph splitting or word-space conventions.

Phase63B materially reduces that objection:

1. the paragraph-entry effect survives a separate v101 transcription in all five folds;
2. the short-range near-family recurrence geometry survives native v101 edit-distance construction in all five folds;
3. both effects also survive an independent EvaT reading;
4. frozen ZL-selected A1 parameters transfer to IT without retuning and still outperform N0/fixed-C0 on the preregistered H62 profile diagnostics.

The evidence for a real formal generation layer is therefore no longer confined to one transcription representation.

## 11. What Phase63B does not establish

Do not promote this result to any of the following:

- A1 is the historical production algorithm;
- Voynichese is meaningless;
- N or C families are falsified;
- all transcription uncertainty has been removed;
- A1 autonomously generates Voynich morphology;
- the manuscript has been deciphered.

Remaining A1 dependence is substantial:

- the architecture was discovered using Voynich/ZL evidence;
- parameters were historically selected on Voynich/ZL and merely frozen for this transfer;
- IT A1-R1 still uses IT training-side empirical vocabulary and morphology;
- true held-out layout/token counts are supplied;
- full line-position coordinate/profile mismatch and fold heterogeneity remain.

GC supplies the strongest independent-alphabet observational replication, but Phase63B deliberately does **not** transfer A1 into v101 through an invented cross-alphabet mapping.

## 12. Provenance

First scientific reveal:

- Actions run: `33334225091`
- job: `99318112772`
- first-reveal scientific head: `31746c4d318929b602b35c288e36e83001200509`
- artifact: `9738599590`
- artifact ZIP SHA-256: `4b9448e655d539528357ee4b51de1ebdea70003730c593f49c96bdbb4a6d9324`
- raw result JSON SHA-256: `77653133af22cd26141bc695a8ee6243cc3d924ba44a41a685cb148b9167db91`

The exact artifact was downloaded and hash-verified by a separate recording workflow before being committed as `phase63b_science_results.json`.

## 13. Next scientific decision

Phase63B closes M5 independent-transcription robustness positively.

The next frontier should **not** be an A2 repair pass. The next strategic gate must compare the remaining high-value objections on equal footing:

1. **G autonomy:** remove the empirical Voynich/IT token inventory and require morphology to be learned/generated from a lower-level rule;
2. **C1 competitive challenge:** give the cipher/shorthand family a separately frozen, historically or mathematically motivated model with explicit complexity cost;
3. **content bridge:** seek independently grounded object/paragraph mapping capable of unseen content prediction.

Phase64 should freeze which of these is the next highest-information test before seeing a new outcome.
