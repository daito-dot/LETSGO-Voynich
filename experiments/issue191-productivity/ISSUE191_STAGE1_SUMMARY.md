# Issue #191 — Stage 1 productivity / open-vocabulary result

Date: 2026-09-08  
Issue: #191  
Parent: #172  
Scientific first reveal: Actions run `34169742362`

## Frozen decision

**`PRODUCTIVE_FORMS_PRESENT_BUT_FINITE_NULL_NOT_REJECTED`**

`R11_PRODUCTIVITY_PROMOTED = false`.

Both ZL3b and IT2a contain stable parser-accepted held-out new types in every physical-leaf fold. However, the preregistered exchangeable finite-observed-inventory control C2 is not rejected at the required `p <= 0.01` threshold in both primary statistics for both readings. Therefore the observed productivity cannot be promoted as a separately demonstrated mechanism responsibility.

This does **not** mean that novel forms are absent. It means that their held-out occurrence is not sufficiently different, under the frozen test, from what is expected when the complete finite observed type inventory and its frequency skew are preserved while token occurrences are reassigned exchangeably to folds.

## Primary result

| quantity | ZL3b | IT2a |
|---|---:|---:|
| visible tokens | 32,570 | 34,411 |
| parser-accepted tokens | 25,071 | 28,280 |
| rejected visible tokens | 7,499 | 6,131 |
| physical leaves | 99 | 99 |
| mean five-fold held-out new-type token rate | 0.070343 | 0.063814 |
| total fold-novel distinct-type incidence | 1,638 | 1,661 |
| all five folds nonzero | yes | yes |
| C2 mean-OOV p-value | 0.073926 | 0.003996 |
| C2 novel-incidence p-value | 0.254745 | 0.031968 |
| C3 V2 mean OOV | 0.069744 | 0.064116 |
| observed / V2 mean OOV | 1.008589 | 0.995280 |
| C3 nonzero in every rep and every fold | yes | yes |

The IT2a mean-OOV statistic alone rejects C2 at 0.01 (`p=0.003996`), but its novel-type-incidence statistic does not (`p=0.031968`). ZL3b rejects neither (`p=0.073926`, `p=0.254745`). The frozen promotion rule requires both statistics to pass in both readings, so the result is unambiguously non-promoting.

## Fold stability

### ZL3b

| fold | parsed tokens | new-type tokens | new-type token rate | novel distinct types |
|---:|---:|---:|---:|---:|
| 0 | 4,430 | 339 | 0.076524 | 327 |
| 1 | 4,810 | 364 | 0.075676 | 337 |
| 2 | 5,516 | 365 | 0.066171 | 339 |
| 3 | 5,447 | 347 | 0.063705 | 321 |
| 4 | 4,868 | 339 | 0.069638 | 314 |

### IT2a

| fold | parsed tokens | new-type tokens | new-type token rate | novel distinct types |
|---:|---:|---:|---:|---:|
| 0 | 4,976 | 350 | 0.070338 | 328 |
| 1 | 5,416 | 364 | 0.067208 | 336 |
| 2 | 6,261 | 376 | 0.060054 | 348 |
| 3 | 6,197 | 367 | 0.059222 | 336 |
| 4 | 5,430 | 338 | 0.062247 | 313 |

The qualitative presence of held-out novelty is therefore reading-stable. ZL3b and IT2a are alternate readings of the same manuscript, not independent manuscript evidence.

## What the novel types are made of

Annotations are non-exclusive and are counted on fold-novel distinct-type incidences.

| annotation | ZL3b | IT2a |
|---|---:|---:|
| total fold-novel distinct incidences | 1,638 | 1,661 |
| all component `(slot,value)` units already seen in training | 1,638 (100%) | 1,661 (100%) |
| known occupied-slot shape | 1,428 (87.18%) | 1,437 (86.51%) |
| new occupied-slot shape | 210 (12.82%) | 224 (13.49%) |
| surface Levenshtein distance 1 from a training type | 1,575 (96.15%) | 1,593 (95.91%) |
| parser-accepted innovation farther than edit distance 1 | 63 (3.85%) | 68 (4.09%) |

The strongest structural fact is that **every held-out novel canonical type uses only component units already observed in its training folds**. Most also reuse an occupied-slot shape already observed in training, and approximately 96% are one character edit away from an existing canonical surface.

Operationally, the new forms look like local recombinations / near-neighbour variants inside an already-established component system, not the arrival of new component symbols or a radically new shape inventory.

## Exact rarefaction expectation

Summed across the five folds, the expected number of training-unseen distinct types discovered at each without-replacement sample fraction is:

| held-out sample fraction | ZL3b | IT2a |
|---:|---:|---:|
| 10% | 173.93 | 177.87 |
| 25% | 430.25 | 439.45 |
| 50% | 845.76 | 861.70 |
| 75% | 1,247.81 | 1,268.31 |
| 100% | 1,638.00 | 1,661.00 |

This confirms a smooth continuing discovery curve within the finite held-out sample. It does not establish an infinite latent vocabulary.

## C2 — finite observed-inventory null

### ZL3b

Observed mean OOV: `0.0703427526`.

C2 null mean: `0.0692242390`; central 95% interval `[0.0677784603, 0.0707258785]`; `p=0.073926`.

Observed novel incidence: `1638`.

C2 null mean: `1631.699`; central 95% interval `[1615, 1649]`; `p=0.254745`.

### IT2a

Observed mean OOV: `0.0638138356`.

C2 null mean: `0.0619134165`; central 95% interval `[0.0605489348, 0.0633819837]`; `p=0.003996`.

Observed novel incidence: `1661`.

C2 null mean: `1642.385`; central 95% interval `[1624, 1661]`; `p=0.031968`.

Thus there is some evidence of physical-leaf localization in IT2a token-mass OOV, but it does not replicate across the alternate reading or across the second primary C2 statistic. Under the preregistered rule, this is insufficient for a separate productivity responsibility.

## C3 — frozen productive V2 control

V2 generates nonzero new types in every one of the 100 deterministic realizations of every fold in both readings.

### OOV magnitude

- ZL3b observed `0.0703428`; V2 mean `0.0697437`; 95% MC interval `[0.0668528, 0.0728919]`; observed/V2 `1.00859`.
- IT2a observed `0.0638138`; V2 mean `0.0641165`; 95% MC interval `[0.0610176, 0.0670073]`; observed/V2 `0.99528`.

### Novel distinct incidence

- ZL3b observed `1638`; V2 mean `1632.79`; 95% MC interval `[1564.475, 1708.1]`; observed/V2 `1.00319`.
- IT2a observed `1661`; V2 mean `1687.39`; 95% MC interval `[1618.425, 1759.575]`; observed/V2 `0.98436`.

### Structural composition

Observed and V2 structural shares are also close:

- known-shape share: ZL3b `0.87179` observed vs `0.86699` V2; IT2a `0.86514` vs `0.85850`;
- edit-distance-1 share: ZL3b `0.96154` observed vs `0.93327` V2; IT2a `0.95906` vs `0.93415`.

The frozen V2 token-internal generator therefore reproduces not only the overall held-out OOV magnitude but also novel distinct incidence and most of the coarse structural composition of the novel types.

## Mechanistic interpretation

Issue #191 asked whether productivity deserved a **separate** mechanism responsibility. The answer from this test is no.

The data clearly exhibit productive-looking legal-form novelty: each fold contains unseen canonical types, those types are assembled entirely from known units, and V2 generates a quantitatively matching novelty regime. But C2 shows that most of the key held-out novelty burden is compatible with the already-observed finite type inventory plus its frequency skew under exchangeable fold assignment.

The parsimonious current interpretation is therefore:

1. the manuscript has a strongly reusable component/slot system;
2. this system naturally produces many low-frequency legal-form combinations and near-neighbour variants;
3. the frozen V2 grammar already captures that behavior well;
4. the present evidence does not require a new R11 responsibility beyond the existing token-internal generative account.

This is a negative result for **separate-responsibility promotion**, not a negative result for generativity itself.

## Firewalls

This result does not prove:

- an infinite vocabulary;
- semantic word formation;
- natural language;
- a particular cipher family;
- authorship or scribal intent;
- independence of ZL3b and IT2a.

No retroactive #172 scorecard rescore is licensed by Issue #191.