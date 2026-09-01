# Issue #72 V2 — Stage A trace audit report

Status:

> **`TRACE-IDENTIFIED INTERVENTION SET READY FOR TARGET DESIGN`**

This report is target-blind with respect to every new Issue #72 counterfactual R1 quantity.

No counterfactual slot-pair Q, residual Z, residual energy E, reliability W, target topology, sign agreement, R1 p-value, or selected-edge diagnostic was computed.

## 1. Provenance

Stage-A workflow:

- run: `33462299547`;
- job: `99714832939`;
- exact branch head: `df8cdf10e9fb7a6812567c6d954eb9313f39eb09`;
- parent main: `98a04953aabe9e228a17fa5808adf506a0833362`;
- plan first-add: `0d8a3803e7c9b959718686d497087718e130a252`;
- implementation first-add: `b7b86a84d5469a1a77bb2c0f689427aff149deec`;
- workflow first-add: `df8cdf10e9fb7a6812567c6d954eb9313f39eb09`.

Actions artifact:

- artifact ID: `9783599640`;
- artifact ZIP SHA-256: `97a7c146f8aeb2a1bb55df0ad657258f4db9f63c02da80c5a99197d2ec4630c8`;
- exact Stage-A JSON SHA-256: `a8d82a6e9fbc391ab532734af424bf6c6b7241d5a36deeb1248dba53d5775392`;
- exact Stage-A JSON bytes: `24,988`;
- manifest SHA-256: `da7028a72f01c9a3d4fd7a67b3ad7212b7d75cf6ad265bce3e2c816adab1c6a0`.

The workflow explicitly recorded:

`counterfactual_R1_target_scored=false`

## 2. Exact baseline replay established

The instrumented implementation was run independently from the historical Phase64B implementation at the same frozen realization-0 seed for each manuscript.

For every manuscript:

1. instrumented primary output = historical primary output exactly;
2. instrumented raw output = historical raw output exactly;
3. trace-only primary re-render = instrumented primary exactly;
4. trace-only raw re-render = instrumented raw exactly;
5. ambiguity-retry count = historical implementation exactly;
6. frozen Issue #68 primary surface SHA-256 reproduced exactly.

| manuscript | seed | primary SHA-256 | raw SHA-256 | ambiguity retries | primary 12-slot coverage |
|---|---:|---|---|---:|---:|
| BIS193 | 6480000 | `fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805` | `06e71ba2bf0470ca1f432b9eecbfcb137c4debe3383d0f5d4b06e7af3c25233e` | 401 | 0.886129 |
| CLM13027 | 6480100 | `da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77` | `533e706fe3b00fede8eeffe3352cab78e9ba9b2f38d1987b6b1ddbd7096dcc21` | 471 | 0.889907 |
| Mazarine915 | 6480200 | `2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d` | `cb51281201b3f39eb2f6b604b591290ba515d6c0f952b33268e442b5335d97ef` | 320 | 0.883625 |
| UBL758 | 6480300 | `5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89` | `f31ce1d2d40f6acec4bf19ee17d8cec9c0776c11e71866e88b70783df1cc8ed8` | 99 | 0.879965 |

Pooled frozen primary surface:

`47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`

This is the exact Issue #68 primary surface identity.

Therefore the accepted-event trace is an exact realized-process authority for the frozen published rep0 execution rather than an approximate reimplementation.

## 3. Permanent trace identities

The full traces are deterministically regenerable from the pinned source, exact code, exact seeds and the Stage-A executable. Their compressed artifact identities are:

| manuscript | deterministic gzip SHA-256 | raw canonical trace JSON SHA-256 | raw JSON bytes |
|---|---|---|---:|
| BIS193 | `e2a8f10489b2977fa8042db1c81c7235fffe55bdfc37ca74b60bc083536a9913` | `c3a0158bd0b4d161d30cfbe601af2fb7fe90fa2ae340e6473db73f60b14d47c7` | 5,510,747 |
| CLM13027 | `129f8fb4be68fc3747af0514be3e860cf909e4f90819bcb11e088b6b8403c87b` | `1bbc6aec641e15edbe8f5a7f3a934365648d4a56caefeb14afa260cf496252fd` | 4,717,490 |
| Mazarine915 | `e09f12a63dad7d7814e1b4a44f31ad8188dbd41c7a9ebe80fba736304c9d788a` | `b3c18102de365de67c4c5a0cd027bff2a8d51d352866ca4fb1fd1e90f9cda0d8` | 3,291,422 |
| UBL758 | `c9d9cc9dba16341a2608119f4af6b209c0051b6cb53345be301d8782e7e7ccfb` | `e840ff0cefc244276caaa6d81030d90f20ad474e656b7276da877b62adf0eaff` | 1,004,896 |

Trace schema:

`issue72-v2-naibbe-accepted-event-trace-v1`

## 4. Fixed-path emission pilots

All four fixed-path pilots keep the realized segmentation, source-letter trace, selected table/state schedule, retry history, and final output join mask fixed. Only the declared codebook value association is changed.

There are `34,577` pre-output-spacing encryption events. The fixed-path pilots alter nearly every emitted event, so they are nontrivial interventions.

| pilot | direct 12-slot coverage | accepted / visible | changed-event fraction | bigram ambiguity-admissible fraction |
|---|---:|---:|---:|---:|
| EL — effective-letter value reassignment | **0.853845** | 28,667 / 33,574 | 1.000000 | 0.975876 |
| ES — state-value reassignment | **0.530708** | 17,818 / 33,574 | 1.000000 | 0.945450 |
| ET — table-value reassignment | **0.866146** | 29,080 / 33,574 | 0.993232 | 0.973321 |
| EG — global effective-cell value permutation | **0.561565** | 18,854 / 33,574 | 0.996905 | 0.848612 |

Bigram-event support totals:

- fixed trace bigram events: `17,617`.

Legality diagnostics:

| pilot | admissible | unigram collision | alternative-bigram collision |
|---|---:|---:|---:|
| EL | 17,192 | 246 | 179 |
| ES | 16,656 | 58 | 903 |
| ET | 17,147 | 281 | 189 |
| EG | 14,950 | 68 | 2,599 |

### Interpretation

EL and ET preserve most of the direct 12-slot interface support and most fixed-path bigrams remain valid under the corresponding modified full codebook.

ES and EG reduce parser coverage substantially. This is scientifically informative but is **not a Stage-A FAIL**, because no 0.60 hard gate exists here. It means any later R1 comparison must confront the possibility that these interventions alter the representation itself rather than merely moving within the same representation.

The ambiguity-admissibility fraction is diagnostic only. A counterfactual is not repaired or selected based on this number.

## 5. PT total-pipeline plaintext-order pilot

PT shuffles effective plaintext character order within each line while preserving that line's exact character multiset and length, then reruns the unchanged pinned published pipeline.

Pooled direct parser coverage:

**0.885656**

This is very close to the published primary surface's pooled coverage (`29,759 / 33,574 = 0.886370`).

Per-manuscript PT coverage:

- BIS193: `0.884724`;
- CLM13027: `0.886792`;
- Mazarine915: `0.885616`;
- UBL758: `0.885579`.

PT changed the retry trajectory as expected:

- BIS193: 518 retries vs published 401;
- CLM13027: 512 vs 471;
- Mazarine915: 329 vs 320;
- UBL758: 127 vs 99.

This confirms why PT must be interpreted as a **total upstream perturbation through the complete pipeline**, not as an isolated direct plaintext-order effect.

No R1 conclusion follows yet.

## 6. FI final-surface sufficiency pilot

FI globally permutes the exact `33,574` complete published primary token instances while preserving:

- the exact whole-token multiset;
- manuscript/item/line token counts.

Distinct complete tokens in the frozen primary population: `7,146`.

FI pooled direct parser coverage:

**0.886370405671055**

This is exactly the same as baseline because the complete-token multiset is unchanged.

This is not evidence for a codebook origin. It establishes only that FI is a clean test of whether the already-produced complete token inventory plus the retained line layout is sufficient for R1 after token-to-position pairing is randomized.

## 7. Criterion-validity conclusions from Stage A

### A. Exact trace authority: VALIDATED FOR ROLE

The trace is exact enough to support fixed-realization counterfactual re-emission.

### B. EL/ES/ET/EG: VALIDATED AS FIXED-PATH STRUCTURAL ABLATIONS

They isolate emitted lookup-value association conditional on the exact realized rep0 path.

They are **not** automatically valid historical Naibbe ciphertext families, because the ambiguity rule is not rerun.

### C. PT: VALIDATED AS A TOTAL-PIPELINE INTERVENTION

It answers whether changing plaintext order has a total downstream effect on R1 through the entire published algorithm.

It does not estimate a direct effect holding mediators fixed.

### D. FI: VALIDATED AS A FINAL-SURFACE SUFFICIENCY CONTROL

It cannot identify whether the final inventory was caused by codebook structure, plaintext dynamics, table scheduling, retries, or their interactions.

### E. 12-slot coverage: DESCRIPTIVE / INTERFACE SUPPORT ONLY AT STAGE A

The old 0.60 hard cutoff is not inherited as a scientifically privileged boundary.

## 8. Stage-A scientific conclusion

> **Issue #72 can proceed, but only with role-specific contrasts. A single global `codebook versus process origin` label is not causally identified by the available interventions.**

The next step is not to make the R1 gates harder. The next step is to empirically calibrate what counts as ordinary R1 variation under the unchanged published Naibbe mechanism, then preregister intervention comparisons against that calibrated reference.

A natural positive-control family already exists prospectively from Phase64B: published Naibbe cipher realizations `rep0..rep4` under the historically frozen seeds. Scoring those unchanged-mechanism realizations before scoring any Issue #72 intervention can provide a T2 measurement/process-variation reference for the later target criterion.
