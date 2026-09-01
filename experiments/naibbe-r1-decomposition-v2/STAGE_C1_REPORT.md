# Issue #72 V2 — Stage C1 fixed-path association randomization report

## Status

**FIXED-PATH DIRECT-EMISSION ASSOCIATION EFFECTS LOCALIZED**

Stage C1 is complete and permanently frozen.

This report is interpretive metadata over the exact first-reveal authority. It does not replace the raw population.

Permanent raw authority:

- scientific first-reveal head: `200e664eaabc9c65774b9a46417a6b004ecf8e18`
- first-reveal workflow run: `33469456818`
- workflow conclusion: `success`
- first-reveal artifact ID: `9786807320`
- first-reveal artifact ZIP SHA-256: `ff8afdee9f54e7557c67152f22f120d0e385d30530b2ce604618dd6fe133e8cc`
- aggregate SHA-256: `ff46576e4f8bd015e7ad90689bb04b3984d43d3da3c98547ed09d58f58405f0c`
- permanent-freeze commit: `22d9a215982406695c89e97e222bb5c2fcb351af`
- permanent authority directory: `experiments/naibbe-r1-decomposition-v2/stage-c1/`
- exact assignment results: **124/124** = 4 axes × 31 prospectively fixed randomizations

The permanent authority directory contains:

- `stage_c1_aggregate.json`
- `individual/*.json` for all 124 assignments
- `SHA256SUMS.txt`
- `PROVENANCE.txt`
- `ARTIFACT_AUTHORITY.txt`
- `stdout.txt`

The permanent-freeze operation was **post-reveal transport only**. It did not regenerate, rerandomize, rescore, filter, or tune any scientific result.

---

## Scientific question

Conditional on Naibbe's already-realized segmentation, table, state, retry, and spacing paths, does the published assignment of Voynich-like glyph values to emission cells produce a systematically more Voynich-R1-like output than outcome-independent association-destroying reassignments?

This is a **fixed-realization conditional direct-emission** question. It is not a test of the complete historical Naibbe mechanism, the Latin plaintext hypothesis, or decipherment.

---

## Frozen intervention meanings

### EL — effective-letter association

Globally permute the 23 effective letters while reusing the same letter permutation across every table/state.

Preserves table×state value multisets and cross-table/state coordination by letter identity; destroys source-letter ↔ emitted-value association.

### ES — state-value association

Within each table×effective-letter, permute the three emitted values across unigram/prefix/suffix states.

Preserves the local three-value multiset; destroys state specialization.

### ET — table-value association

Within each state×effective-letter, permute the six emitted values across six table labels.

Preserves the state+letter six-value multiset and the realized table schedule; destroys table-value association.

### EG — global reachable-cell association

Globally permute all 414 reachable glyph-value instances among the 414 reachable emission cells.

Preserves the global reachable value multiset and fixed process path; destroys letter, state, table associations and their interactions. EG is therefore a broad association-destruction intervention, not a one-factor effect.

---

## Primary estimand

For each assignment and each target transcription, randomized and published-baseline outputs are aligned at identical final positions.

The primary comparison uses **common support**: positions parseable under the frozen SlotParser(min) in both the published baseline and randomized surface.

For each target:

`DELTA_R = R_randomized - R_baseline`

Interpretation:

- negative: association destruction made the same representable positions less Voynich-R1-like;
- near zero: little direct target-topology displacement;
- positive: reassignment improved target alignment.

No coverage gate was applied. No hard intervention threshold was applied. ZL3b and IT2a were not averaged.

The empirical non-loss rank quantity is

`(1 + count[DELTA_R >= 0]) / 32`.

It is reported as a finite prospective-randomization rank/evidence quantity and is **not promoted to a classical exact p-value or universal truth threshold**.

---

## Complete first-reveal result

| Axis | ZL3b median ΔR | IT2a median ΔR | Direction agreement across 31 assignments | ZL3b non-loss rank | IT2a non-loss rank |
|---|---:|---:|---|---:|---:|
| EL | -0.246725 | -0.253840 | **31 both-negative / 0 nonnegative / 0 mixed** | 0.03125 | 0.03125 |
| ES | -0.213530 | -0.233840 | **31 both-negative / 0 nonnegative / 0 mixed** | 0.03125 | 0.03125 |
| ET | -0.018601 | -0.043740 | 18 both-negative / 12 both-nonnegative / 1 mixed | 0.43750 | 0.40625 |
| EG | -0.334150 | -0.368101 | **31 both-negative / 0 nonnegative / 0 mixed** | 0.03125 | 0.03125 |

Mean ΔR values show the same ordering:

- EL: ZL3b `-0.253899`; IT2a `-0.264147`
- ES: ZL3b `-0.222793`; IT2a `-0.241729`
- ET: ZL3b `-0.024082`; IT2a `-0.034586`
- EG: ZL3b `-0.350429`; IT2a `-0.363318`

The full observed ΔR ranges were:

- EL: ZL3b `[-0.548612, -0.046218]`; IT2a `[-0.546975, -0.047446]`
- ES: ZL3b `[-0.458636, -0.012938]`; IT2a `[-0.480958, -0.035699]`
- ET: ZL3b `[-0.220364, +0.120729]`; IT2a `[-0.239124, +0.102279]`
- EG: ZL3b `[-0.621672, -0.156216]`; IT2a `[-0.636862, -0.143196]`

Thus every prospectively fixed EL, ES, and EG reassignment reduced common-support target alignment in both independent target readings. ET did not show this pattern.

---

## Representation context

Randomization changes parser coverage, especially for ES and EG. This is recorded separately from common-support topology rather than converted into a mechanism-failure gate.

| Axis | Median randomized full-parser coverage | Median common-support fraction |
|---|---:|---:|
| EL | 0.832419 | 0.776938 |
| ES | 0.584341 | 0.573500 |
| ET | 0.868974 | 0.813029 |
| EG | 0.545131 | 0.528372 |

Because the primary ΔR estimand is computed on identical jointly parseable positions, the EL/ES/EG topology displacement cannot be reduced to the statement that randomized outputs merely became less parseable. Coverage loss remains separate representational evidence and must not be ignored, but it is not the sole source of the observed common-support R1 loss.

---

## Scientific interpretation

### 1. Direct effective-letter association contributes strongly to R1

EL destroys the association between effective source-letter identity and emitted glyph values while preserving the fixed realized process path and table/state value inventories.

All 31 EL assignments displaced both target readings negatively, with median ΔR near `-0.25`.

Within the licensed fixed-path scope, this is strong evidence that Naibbe's published effective-letter ↔ emitted-value association contributes directly to the R1 topology resemblance.

### 2. Direct state specialization contributes strongly to R1

ES preserves each table×letter's three emitted values but reallocates them among unigram/prefix/suffix roles.

All 31 ES assignments displaced both target readings negatively, with median ΔR about `-0.21` to `-0.23`.

Within the licensed fixed-path scope, this is strong evidence that the allocation of glyph values by unigram/prefix/suffix state contributes directly to R1 resemblance.

### 3. Table-value association is not comparably localized by this experiment

ET is qualitatively different. Its effects are smaller, include both signs, and do not yield the unanimous negative displacement seen for EL/ES/EG.

Therefore Stage C1 does **not** support the claim that the specific table-label ↔ glyph-value allocation is a comparably strong direct source of R1 under the realized table schedule.

This is not evidence that tables are historically irrelevant. ET licenses only the narrower fixed-path direct-assignment statement.

### 4. Broad structured assignment beyond global inventory matters

EG preserves the complete global reachable value multiset but destroys its structured placement among all reachable cells.

All 31 EG assignments displaced both target readings negatively, and EG produced the largest median displacement of the four axes.

Therefore the R1 resemblance is not explained by global reachable glyph inventory alone. Structured placement across emission cells carries substantial R1-relevant information.

### 5. Current localization

The result supports the following mechanistic summary:

> Under fixed realized Naibbe process paths, the R1 resemblance depends strongly on structured emitted-value assignment, especially effective-letter identity and unigram/prefix/suffix state specialization; the specific allocation across table labels is much more exchangeable in this experiment.

A useful compact description is:

> **effective-letter × functional-state → emitted glyph value**

appears to be a major direct-emission scaffold for the observed Naibbe/Voynich R1 similarity.

This is a localization statement, not a decipherment claim.

---

## What Stage C1 does not establish

Stage C1 does **not** establish any of the following:

- that the Voynich Manuscript was generated by Naibbe;
- that Latin is the plaintext;
- that the tested Naibbe mechanism is historically competitive overall;
- that EL, ES, ET, and EG are independent additive causal factors;
- that five stochastic paths are five independent corpora;
- that common-support results describe positions rejected by the parser;
- that parser coverage is a historical-truth criterion;
- that `0.03125` is a universal significance boundary;
- that EG identifies one isolated factor;
- that final token inventory alone is insufficient;
- that plaintext order or the complete rerun pipeline is irrelevant.

Those last two questions remain deliberately outside Stage C1.

---

## Criterion-validity status

- Stage C1 intervention definitions: **VALIDATED FOR FIXED-PATH DIRECT-EMISSION ROLE**
- exact 124-assignment first-reveal population: **PERMANENTLY FROZEN AUTHORITY**
- common-support ΔR estimand: **VALIDATED FOR PAIRED REPRESENTABLE-POSITION ROLE**
- ZL3b and IT2a separate target readings: **VALIDATED FOR REPLICATION/ROBUSTNESS ROLE**
- B2 unchanged-Naibbe variation: **CALIBRATED FOR EFFECT-SIZE CONTEXT**
- parser coverage: **DESCRIPTIVE / REPRESENTATIONAL EVIDENCE; NOT A MECHANISM TRUTH GATE**
- rank-nonloss values: **FINITE RANDOMIZATION EVIDENCE; NOT A CLASSICAL HARD THRESHOLD**
- historical Naibbe/Latin/decipherment inference from C1 alone: **NOT AUTHORIZED**

---

## Next frontier

Stage C1 answers the fixed-path direct-emission association question. The remaining high-information decomposition should now move to the two preregistered responsibility classes that C1 intentionally does not answer:

1. **PT — full-pipeline total effect of within-line plaintext order**
   - preserve line length and character multiset;
   - shuffle effective plaintext order within line;
   - rerun the exact published pipeline;
   - asks whether ordered plaintext/process interaction contributes to R1 beyond the frozen-path direct assignment effect.

2. **FI — final-surface inventory/layout sufficiency**
   - permute complete produced tokens while preserving the prospectively declared line/layout structure;
   - asks how much R1 can survive from the final complete-token inventory plus layout alone;
   - cannot license inference about upstream codebook origin.

Only after PT and FI are frozen should Issue #72 make a broader statement about whether Naibbe's R1 resemblance is primarily attributable to codebook assignment, full-pipeline processing, or final-surface inventory/layout sufficiency.
