# Issue26E11E — validated-solver León/STA family substitution re-analysis

Status: **COMPLETED — `LATIN-LIKE BUT KEY-UNSTABLE`**

## Question

After E11D validated the frozen FREQ-HILL monoalphabetic solver on 12/12 independently constructed 23-symbol Latin substitutions (60/60 held-out folds perfect), E11E re-analysed the externally defined 23-family STA representation of Voynich under the same fixed León-style manuscript-wide one-to-one Latin substitution model.

E11E is a validated-solver re-analysis, not a pristine first-ever target reveal: E11C had previously exposed a target run using an invalid solver, but those target outputs were declared non-authoritative and were not used to develop or select the E11D solver.

## Preregistration and provenance

- E11D validated solver report parent: `e7e14388c9407816b6a9d8bccb58e13c34fc1df9`
- E11E plan first commit: `d89c66e3903ce4d97ee97c8da68ecc2d26c156bc`
- E11E executable first commit: `fc5f653bd7ea407ae139811dcef91009bff05b55`
- reveal workflow/head: `f67a9f5fd503fd57558919fefcea18be250c1674`
- Actions run: `33386685707`
- job: `99470787198`
- artifact: `9755848260`
- raw JSON SHA-256: `7cd3e50c40a88430ef1e8657175c0d2a49985f9180e391542be7ffa8d2e8e39f`
- artifact ZIP SHA-256: `b049cb00a2c579125d5cb0c4e2011cff7788efd3ff22d698254021196738dd1f`.

The workflow verified the exact official STA1 target and frozen CREMMA commit before execution.

## Target population audit

The reconciled population reproduced exactly:

- numerical-leaf source lines: **4,119**
- numerical-leaf STA-family events: **140,423**
- numerical physical leaves: **99**
- scoring segments: **4,865**
- excluded special Rosettes population: **11 `fRos` lines / 166 events**.

All 23 frozen STA families were present. No family was split, merged, deleted, or target-selected.

## Solver implementation audit

PASS.

For every fold, the frozen FREQ-HILL solver's final score agreed exactly with both the independently explicit 24-letter scorer and the shared scorer:

- maximum discrepancy: **0**.

Thus E11E is not blocked by the failure that invalidated E11C.

## External Latin baseline

Under the E11-specific normalization/model frozen before E11E:

- mean five-fold medieval-Latin self CE: **3.6903904874 bits/char**
- Latin top-five-character fraction: **0.4932494650**.

This baseline differs from some other Issue26 plaintext probes because the E11 source/model normalization is its own previously frozen family-specific representation. The E11E comparison is only to this matched E11 baseline.

## Primary held-out result

Frozen classification:

> **`LATIN-LIKE BUT KEY-UNSTABLE`**

Observed pooled held-out metrics:

- pooled Voynich→Latin CE: **3.6860993911 bits/char**
- Latin baseline CE: **3.6903904874**
- CE difference target − Latin baseline: approximately **−0.00429 bits/char**
- pooled top-five-character fraction: **0.7746166938**
- mean pairwise occurrence-weighted key stability: **0.6219935481**
- exact complete-key recurrence: **1/5**
- distinct exact whole-token CREMMA matches length >=6: **1** (`distin`)
- folds with any >=6 exact whole-token match: **1/5**.

Frozen gates:

| gate | result |
|---|---|
| pooled CE <= Latin + .50 | **PASS** |
| weighted key stability >= .90 | **FAIL** |
| identical complete key >=3/5 | **FAIL** |
| top-five <= Latin + .15 | **FAIL** |
| >=10 distinct exact whole-token words >=6 | **FAIL** |
| >=6-word hits across >=3 folds | **FAIL** |

Therefore the low held-out CE alone cannot be called plaintext evidence.

## Fold results

| fold | train CE | held CE | unused letter | accepted swaps |
|---:|---:|---:|:---:|---:|
| 0 | 3.62347 | 3.64944 | w | 13 |
| 1 | 3.78618 | 3.77973 | y | 13 |
| 2 | 3.63518 | 3.59941 | w | 12 |
| 3 | 3.74616 | 3.73543 | y | 16 |
| 4 | 3.61811 | 3.66690 | k | 13 |

A few high-frequency assignments recur — most notably family `A→i` in all five folds — but the complete mapping changes substantially. The pairwise frequency-weighted agreement of only 0.622 is far below the frozen 0.90 stability requirement.

## What the decoded text looks like

Representative held-out continuous sequences:

- `qiuinitisinitiodisdinirnenitindissi`
- `ninirininitiautiodininerinrinsip`
- `nitimiileittidineit`
- `tdeinciqisuisrissimss`
- `nisiseierisiatisisaeiminti`
- `tuisiquiiutiiiiaiinisniuisistdisi`.

Original token boundaries do not rescue readability. Examples:

- `qiuin itis in itio dis dini rnen i tin dissi`
- `nitimi ileit tid ineit`
- `tdein ciqis uis ris simss`
- `nisisei erisi atis is aei minti`.

Only one distinct exact whole-token CREMMA word of length >=6 appears (`distin`, fold 2). This is far below the preregistered readability requirement.

## Interpretation

E11E produces the first result in the historical music-cipher plaintext series where the held-out character 4-gram CE itself reaches the matched Latin self-baseline. That numerical fact should be retained.

It is **not sufficient for a plaintext claim** because three independent warning signals are strong:

1. the fitted key is unstable across physical-leaf folds;
2. decoded character mass is much more concentrated than medieval Latin (top five 77.5% vs 49.3%);
3. token-level lexical readability is almost absent.

The immediate competing explanation is that the 23-family Voynich stream has frequency/local-order structure that allows a flexible monoalphabetic optimizer to achieve a low Latin 4-gram score without identifying a stable decipherment.

## Required next falsification

Do **not** rescue E11E by moving directly to homophones, polyalphabetic keys, family-member splitting, or manual interpretation.

First test whether E11E's low CE depends on genuine Voynich family order rather than family frequencies and the optimizer itself:

> Give frequency- and segment-length-preserving order-shuffled STA-family nulls the **same complete FREQ-HILL fitting freedom**, and ask whether the real E11E sequence achieves unusually low held-out CE and/or unusually high cross-fold key stability relative to those fully refitted nulls.

This follow-up should be separately preregistered before execution. If real order is ordinary under those refitted nulls, the apparent Latin-like CE is a fitting/frequency effect. If real order is strongly exceptional, only then is a more specific León-like follow-up warranted.

## Scope of any negative

Even if the next null audit explains the CE, the result only bears on the externally defined 23-family manuscript-wide monoalphabetic Latin substitution representation. It does not test family-member distinctions, historically attested homophony, nulls/polygraphs, non-Latin plaintext, or non-textual musical/procedural use.

No merge to `main` is authorized.
