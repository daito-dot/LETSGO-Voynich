# Issue #72 V2 — Stage B unchanged-Naibbe positive-control calibration plan

Status: **PREREGISTERED BEFORE ANY NEW rep1–rep4 R1 SCORE**

Parent Stage A:

> `TRACE-IDENTIFIED INTERVENTION SET READY FOR TARGET DESIGN`

Read first:

- `research/RESEARCH_PROTOCOL.md`
- `STAGE_A_TRACE_AUDIT_PLAN.md`
- `STAGE_A_REPORT.md`
- `STAGE_A_PROVENANCE.md`

## 1. Why Stage B exists

The superseded V1 design used human-chosen relative-effect bands such as `.90` and `.70` to classify intervention outcomes.

Those bands were stringent but not empirically calibrated to the amount of R1 variation produced by the unchanged published Naibbe mechanism itself.

Under `research/RESEARCH_PROTOCOL.md`, the correct next question is:

> **How much does the complete R1 surface constraint vary across already-frozen stochastic realizations of the exact same published Naibbe mechanism?**

This is a positive-control / measurement-process calibration step. It is not a new mechanism tournament and it scores no Issue #72 intervention.

## 2. Frozen positive-control population

Use exactly the five historical published Naibbe cipher realizations already frozen in Phase64B before Issue #68 R1 existed:

`rep0, rep1, rep2, rep3, rep4`

For manuscript index `mi` in the existing Phase64B manuscript order, seed:

`6480000 + 100*mi + rep`

Thus:

| manuscript | rep0 | rep1 | rep2 | rep3 | rep4 |
|---|---:|---:|---:|---:|---:|
| BIS193 | 6480000 | 6480001 | 6480002 | 6480003 | 6480004 |
| CLM13027 | 6480100 | 6480101 | 6480102 | 6480103 | 6480104 |
| Mazarine915 | 6480200 | 6480201 | 6480202 | 6480203 | 6480204 |
| UBL758 | 6480300 | 6480301 | 6480302 | 6480303 | 6480304 |

No seed may be added, removed or replaced based on R1 performance.

### Why these five

This is not a convenience sample selected after Issue #68. It is the exact `CIPHER_REPS=5` seed family already used by Phase64B for the published Naibbe evaluation.

Therefore the family supplies an independently frozen stochastic-replay population for the unchanged mechanism.

## 3. Two-step Stage B firewall

### B0 — target-blind support freeze

Before new R1 scoring, generate all five published surfaces and freeze:

- exact per-manuscript surface SHA-256;
- exact pooled surface SHA-256 per rep;
- visible token count;
- unchanged `SlotParser(min)` accepted count and continuous coverage;
- ambiguity retry diagnostics.

Forbidden during B0:

- any slot-pair Q;
- residual Z;
- E or W;
- topology/sign against ZL3b or IT2a;
- R1 p-values.

### B1 — positive-control R1 calibration

Only after B0 surfaces are frozen may the R1 calibration scorer be committed/executed.

B1 scores the complete R1 geometry for all five unchanged-mechanism reps. It does **not** score EL/ES/ET/EG/PT/FI.

## 4. Criterion Validity Table

| Claim / role | Construct | Metric | Threshold / class | Source | Positive control | Negative / null | Failure meaning | Limit |
|---|---|---|---|---|---|---|---|---|
| Five surfaces are unchanged published Naibbe stochastic realizations | exact pinned algorithm/codebook/source with only historically frozen RNG seed changed | source/commit/config identities + surface SHA + seed | exact identity/invariants | **T1** | rep0 exact Issue #68 replay | any authority/config mismatch | surface cannot enter calibration | does not say R1 should be identical |
| 12-slot interface support is stable enough to compare reps | unchanged parser coverage as continuous measurement | visible, accepted, coverage | no hard cutoff in B0 | **T2-calibration input / descriptive** | rep0 `0.886370...` | none at B0 | no scientific rejection | parser can still select a subset |
| B1 measures ordinary R1 variability of unchanged Naibbe | complete candidate-owned residual topology under exact same R1 representation/scorer | E, W, Pearson vs both readings, sign agreement vs both readings | **no PASS/FAIL threshold in Stage B** | **T2** | all five frozen unchanged-mechanism reps | each rep's line-local null is calibration of residual coordinates, not a mechanism negative control | if variability is large, later equivalence threshold cannot be tight | five reps are a small empirical sample |
| Later intervention criterion may use the baseline variation | intervention deviation compared with frozen B1 distribution | to be defined only after B1 and before intervention scoring | not defined yet | must be **T2/T3**, not hardness-based T5 if avoidable | frozen B1 family | prospective intervention randomization family | only role-specific effect statements | calibration data are not intervention test data |

## 5. R1 calibration metric set

B1 must retain the full complete-graph representation and score each rep independently.

Primary continuous coordinates to freeze for later calibration:

1. direct parser coverage;
2. residual energy `E` over all 66 edges;
3. fold reliability `W` using the four CREMMA manuscript folds;
4. Pearson topology correlation against frozen pooled ZL3b #58C;
5. Pearson topology correlation against frozen pooled IT2a #58D;
6. sign agreement out of 66 against ZL3b;
7. sign agreement out of 66 against IT2a.

For later single-coordinate summaries, a prospective later plan may use a conservative worst-reading quantity such as:

`M_R = min(R_ZL3b, R_IT2a)`

and

`M_sign = min(sign_ZL3b, sign_IT2a)`

but Stage B itself does not convert these into an intervention threshold.

## 6. Null calibration in B1

Each rep must receive its own candidate-owned line-local residual calibration, because stochastic surfaces can differ in line/slot marginals.

Use the same scientific null operation as Issue #68:

- preserve generated physical line identity;
- preserve line length / accepted token count;
- preserve line × slot occupied counts;
- preserve manuscript fold labels;
- destroy same-token cross-slot pairing.

Reference null population:

`N_ref=1000`

This is sufficient for the residual-Z transform used for cross-rep calibration.

### No new confirmatory null p-value is required in Stage B

The purpose is to measure variation among known-positive unchanged-mechanism surfaces, not to repeatedly prove that each surface rejects a line-local null.

Therefore B1 need not generate a second `N_test=1000` family for p-values unless a later pre-reveal audit shows that an exact existing scorer cannot cleanly emit the needed coordinates without it.

Rep0's already-frozen full Issue #68 R1 test-null result remains historical confirmation that the published primary surface satisfies R1.

This halves unnecessary computation and avoids treating p-value hardness as the calibration objective.

## 7. Rep0 cross-check

B1 rep0 must reproduce, to numerical tolerance fixed in implementation before B1 run, the already-frozen Issue #68 continuous values obtainable from the same reference-calibrated pipeline.

At minimum:

- representation population identity;
- residual energy `E=3.1784043855151296` if the exact same residual transform is used;
- reliability `W=0.954726539114345`;
- ZL3b Pearson `0.8830282501011794`;
- IT2a Pearson `0.9000974100381157`;
- sign agreements `60/66` and `61/66`.

If B1 intentionally differs in a way that makes those exact values non-comparable, that difference must be discovered and frozen before any rep1–rep4 target values are exposed. Otherwise the implementation is not authorized.

## 8. Small-n limitation and escalation rule

Five historical reps are valuable because they are independently frozen, but `n=5` is too small to pretend that an empirical min/max is a precise population tolerance interval.

Therefore after B1:

- report the full five values, range, median and MAD/robust spread;
- do not call the observed minimum a universal pass threshold;
- do not score Issue #72 interventions until deciding whether the five-rep spread is sufficiently narrow/stable for the intended comparison.

### If five reps are too variable

A larger unchanged-mechanism calibration family may be prospectively defined in a **new calibration extension before intervention scoring**.

The extension must use target-independent seed generation and must be frozen before any new extended-rep R1 value is revealed.

Intervention results may never be used to decide whether more baseline reps are added.

## 9. No intervention access

Before the Stage-B calibration report is frozen, no R1 scorer may be run on:

- EL;
- ES;
- ET;
- EG;
- PT;
- FI;
- any V1 L/S/T/G/P/I counterfactual.

The Stage-A support diagnostics are already known and may be used only for representation/mechanical design, not R1 selection.

## 10. Stage-B outputs

B0 output:

> exact target-blind rep0–rep4 surface/support manifest.

B1 output:

> unchanged-mechanism R1 stochastic-variation table and calibration assessment.

Allowed B1 conclusions:

- `UNCHANGED-NAIBBE R1 VARIATION NARROW ENOUGH FOR INTERVENTION CALIBRATION`;
- `UNCHANGED-NAIBBE R1 VARIATION REQUIRES LARGER CALIBRATION POPULATION`;
- `POSITIVE-CONTROL CALIBRATION INCONCLUSIVE`.

The exact numerical rule for "narrow enough" is deliberately **not** a hidden hard threshold. The B1 report must justify the decision from the observed scale relative to the scientific contrast that a later intervention design can resolve, and any later intervention threshold must still be frozen before intervention scoring.
