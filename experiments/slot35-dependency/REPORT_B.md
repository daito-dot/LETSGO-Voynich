# Issue #55B — occupancy-versus-subtype decomposition

Status: **COMPLETED — `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`**

## Question

Issue #55A established a reproducible cross-leaf slot3×slot5 dependence, but the pooled 5×5 table was dominated by near-mutual exclusion. #55B asked whether any stable subtype-level association remains after the binary EMPTY/nonEMPTY interaction is modeled explicitly.

The test remained hypothesis-neutral: no Sloane table, music ordering, Latin model, plaintext decoder or semantic interpretation was used.

## Frozen design

The preregistered design reused the exact #55A population, five physical-leaf folds, ZL3b source, parser and state order.

- slot3 states: `EMPTY,t,k,p,f`
- slot5 states: `EMPTY,cth,ckh,cph,cfh`
- primary parser policy: `min`
- `max`: sensitivity only
- Jeffreys smoothing: `alpha=0.5`
- subtype nulls: 1,000 deterministic within-line shuffles preserving every token-level EMPTY/nonEMPTY occupancy pattern and line-local subtype frequencies

The primary decomposition compared:

1. full five-state held-out predictive gain;
2. binary occupancy held-out predictive gain;
3. residual full-state gain beyond an occupancy-only conditional model.

The parser-admissibility audit separately tested all 24 nonempty canonical slot3×slot5 pairs.

## First-reveal provenance

- plan commit: `5cf723eec1df82f3d55dd02e39458afe97d4d273`
- executable commit: `0849607d580889baf8469128f6f41543c43f69c4`
- workflow/reveal head: `cd724664fec4145c129789478c3b4f0473f3c829`
- Actions run: `33394659964`
- job: `99496194136`
- artifact: `issue55b-slot35-cd724664fec4145c129789478c3b4f0473f3c829`, ID `9758969505`
- artifact ZIP SHA-256: `0411671f38515dcd1be0c434bb2e3068ae1c4db53a0c941cb212e95702b63ba6`
- raw JSON SHA-256: `46dbd7a40b8585f97063ba60b38f0e98f4801ff6e8e7d9c882de13b6762d77d0`

The workflow verified that the plan predated the executable and pinned the ZL3b mirror to commit `315f0cad4de3d021bd4185765c037cf2a28d341c`, blob `2a4533ab9bdfa85db9bad602d590978953055df1`.

## Population

Primary `min` and `max` produce the same slot3/slot5 population:

- visible tokens: **32,570**
- parsed tokens: **25,071**
- parse coverage: **0.7697574455**
- physical lines with parsed tokens: **4,082**
- movable lines: **3,953**
- movable tokens: **24,942**

## Primary result

The decomposition is decisive.

| quantity | value |
|---|---:|
| mean full five-state gain | `0.0441774454 bits/token` |
| mean binary occupancy gain | `0.0442150445 bits/token` |
| occupancy fraction of full gain | `1.0008510918` |
| mean subtype residual gain | `-0.0000374707 bits/token` |

The binary occupancy model therefore reproduces essentially all of the #55A cross-leaf predictive gain. The fraction slightly exceeding 1 is numerical/model-estimation variation, not evidence of extra information.

Residual fold values were:

- fold0: `+0.000427436`
- fold1: `+0.000946533`
- fold2: `-0.000446047`
- fold3: `-0.000444750`
- fold4: `-0.000670526`

Only 2/5 folds are positive.

## Occupancy-preserving subtype null

Across 1,000 deterministic subtype-shuffle nulls:

- median residual gain: `-0.0000960919`
- q05: `-0.0001968607`
- q95: `-0.0000199179`
- maximum: `0.0000067826`
- upper-tail count: `269/1000`
- +1 corrected p: **`0.2697302697`**
- real advantage over null median: `0.0000586212 bits/token`

The preregistered subtype-residual gates fail. There is no stable evidence that the exact `t/k/p/f` identity predicts `cth/ckh/cph/cfh` identity beyond occupancy.

## Parser-admissibility audit

All **24/24** nonempty canonical slot3×slot5 combinations are admitted by the frozen parser with the intended two occupied slots and all other slots empty.

Therefore the observed near-exclusion is not a hard parser impossibility.

## Rare co-occupancy

Only three observed parsed tokens have both slots nonempty:

- f57r, `tcfhy`: slot3=`t`, slot5=`cfh`
- f80v, `tchcthy`: slot3=`t`, slot5=`cth`
- f107v, `qopchcfhy`: slot3=`p`, slot5=`cfh`

These identities were preregistered as descriptive output and carry no separate significance claim.

## Classification

Frozen result:

> **`DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`**

#55A remains a real cross-leaf structural result, but its interpretation is narrowed: the predictive relation is a binary morphotactic exclusion, not evidence for a rich 5×5 paired-state code.

The original E10 Sloane recurrence therefore must not be used as evidence for a 25-cell cipher, Sloane plaintext, music or subtype-level correspondence.

## Current structural interpretation

The strongest supported statement is:

> slot3 and slot5 act as alternative token-construction channels that are almost never occupied simultaneously, and this occupancy relation transfers across physical leaves beyond line-local marginal frequencies.

The current experiment does not identify why the exclusion exists. Plausible structural explanations include alternative morphographic constructions, token-class competition or register/position-conditioned word formation. Those explanations remain untested.

## Next test boundary

A follow-up should not search semantic labels for slot3 or slot5. The useful next questions are whether the exclusion:

1. is exceptional among the 12 slot positions or one instance of a broader occupancy graph;
2. survives independent transcription/representation where the relevant states can be defined without circular remapping;
3. changes by manuscript register, Currier class or token position after those factors are frozen before scoring.

Any such follow-up should be plan-first and should treat the present slot3×slot5 result as the selection event rather than as an unseen discovery target.
