# OGH-A — minimal occupancy-generation rule for the replicated R1 topology: first-reveal report

Status: **FIRST REVEAL COMPLETE — FROZEN CLASSIFICATION `COMPACT CONSTRUCTION GRAMMAR SUFFICIENT` (Issue #68 gate), REPLICATED ON BOTH SKELETONS**

Plan authority: `PLAN_A.md` (frozen before executable). Implementation: `IMPLEMENTATION_A.md`. Exact provenance and hashes: `first-reveal/PROVENANCE.md`, `first-reveal/SHA256SUMS.txt`. Aggregate SHA-256 `6cabec85dcb4e49ca412df3468b544d7e427dacfb398379cb48248df7fa7a788`. Every number below is copied from `first-reveal/ogh_a_aggregate.json` and the per-job JSONs in `first-reveal/results/`.

## 1. Question

Issue #72 localized the Naibbe/Voynich R1 resemblance to the corpus-level distribution of parsed 12-slot occupancy signatures. OGH-A asked, on the manuscript itself:

> What is the minimal rule over 12-slot occupancy signatures that, sampled independently token by token into the manuscript's own line skeleton, reproduces the replicated complete-66 R1 residual topology?

Seven models were frozen as a nested ladder (Section 5 of the plan): G0 independent slot Bernoulli; G1 uniform over parser-admissible signatures; G2 maximum-entropy marginals on the admissible set; G3 marginals + occupied-slot count; G4 a left-to-right construction grammar conditioned on the last occupied slot; G5 full pairwise maximum entropy (non-promoting second-order control); G6 empirical signature resampling (non-promoting ceiling). Each was fitted on four physical-leaf folds and generated into the fifth, on both the ZL3b and the IT2a skeleton, with three seeded realizations; every corpus was scored with the unchanged Issue #68 R1 procedure against the frozen ZL3b and IT2a target vectors.

## 2. Frozen result

Primary arm (ZL3b skeleton, realization 0):

| model | free params | E | W | r vs ZL3b | signs | r vs IT2a | signs | R1 (Issue #68 gate) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| G0 independent Bernoulli | 12 | 1.172 | 0.096 | 0.094 | 34/66 | 0.088 | 33/66 | fail |
| G1 admissible uniform | 0 | 0.904 | −0.083 | 0.093 | 39/66 | 0.063 | 38/66 | fail |
| G2 maxent marginals | 12 | 1.768 | 0.462 | 0.025 | 37/66 | 0.039 | 38/66 | fail |
| G3 maxent marginals + count | 23 | 3.257 | 0.312 | 0.058 | 38/66 | 0.020 | 37/66 | fail |
| **G4 last-occupied-slot grammar** | 78 | 3.128 | 0.972 | **0.917** | 62/66 | **0.933** | 63/66 | **PASS** |
| G5 pairwise maxent (control) | 78 | 3.221 | 0.987 | 0.951 | 63/66 | 0.948 | 64/66 | PASS |
| G6 empirical resampling (ceiling) | 611–643 | 3.249 | 0.990 | 0.967 | 64/66 | 0.965 | 65/66 | PASS |

Replication arm (IT2a skeleton, parameters fitted on IT2a training folds, realization 0):

| model | E | W | r vs ZL3b | signs | r vs IT2a | signs | R1 |
|---|---:|---:|---:|---:|---:|---:|---|
| G0 | 1.145 | −0.014 | −0.207 | 28/66 | −0.194 | 27/66 | fail |
| G1 | 1.045 | 0.061 | 0.131 | 39/66 | 0.138 | 40/66 | fail |
| G2 | 1.976 | 0.417 | 0.024 | 36/66 | 0.031 | 37/66 | fail |
| G3 | 3.194 | 0.473 | 0.049 | 38/66 | 0.094 | 37/66 | fail |
| **G4** | 3.197 | 0.975 | **0.908** | 62/66 | **0.933** | 63/66 | **PASS** |
| G5 | 3.220 | 0.979 | 0.959 | 64/66 | 0.960 | 65/66 | PASS |
| G6 | 3.266 | 0.984 | 0.967 | 64/66 | 0.964 | 65/66 | PASS |

All passing models have every familywise maxT p-value at `1/1001`; all failing models fail the topology gate (and G0/G1 also the existence gate). The G0 sanity gate holds on both arms: G0 fails R1 and its residual energy lies inside the candidate test-null range, so the scorer and null behave as designed.

Frozen ordered classification (plan §7), realization 0, both arms:

> **`COMPACT CONSTRUCTION GRAMMAR SUFFICIENT`** — G1, G2 and G3 fail; G4 passes.

The pass/fail pattern is identical on the ZL3b and IT2a skeletons, so the verdict is **replicated across skeletons**. Realizations 1 and 2 are reported in Section 6; they do not change any class.

## 3. What each rung shows

**Parser admissibility is not the source of R1.** 4,077 of 4,095 non-empty signatures are emittable by `SlotParser(min)`, and the uniform-admissible model G1 has no residual graph at all. The grammar is in the manuscript, not in the representation.

**Marginals and occupied-slot count are not enough, and count alone manufactures a strong but wrong graph.** G3 has residual energy `E ≈ 3.2`, indistinguishable in magnitude from the manuscript's `3.23`, yet its 66-edge topology correlates only `0.02–0.09` with either reading and reproduces only `37–38/66` signs. This is exactly the Issue #75 Phase-A M1 finding under an independent harness: graph *existence* is cheap, graph *geometry* is not.

**The empirical signature inventory is sufficient and the two harnesses agree.** Cross-fitted resampling (G6) reaches `r = 0.967 / 0.965` on both arms, matching Issue #75's M+ banks (`0.964–0.966`) to the third decimal. Because G6 samples tokens i.i.d. into the line skeleton, it also re-confirms, for the manuscript itself, the Issue #72 FI conclusion that R1 does not require within-line or sequential organization of signatures.

**R1 is almost entirely a second-order property.** The full pairwise maxent G5, which matches only the 12 first moments and 66 second moments of the training signature distribution, recovers `r = 0.948–0.969` and `63–65/66` signs. Across the three realizations its median `T` is `0.001` below the G6 ceiling on the ZL3b arm (inside the Issue #75 tolerance of `0.0098`) and `0.012` below it on the IT2a arm. Whatever higher-order configuration information the inventory carries contributes at most about one hundredth of topology correlation. G5 is a labelled control, not a mechanism, because it spends one parameter per slot pair; but it fixes the target that any compact mechanism must reach.

**A 78-parameter sequential successor grammar passes R1.** G4 generates a token left to right; the probability of occupying slot `s` depends only on which slot was occupied most recently. Equivalently, it is a first-order Markov chain over the ordered sequence of occupied slots with a stop option. Fitted by counting (add-½, no tuning), it reaches `r = 0.917 / 0.933` (ZL3b arm) and `0.908 / 0.933` (IT2a arm) with `62–63/66` signs, `W ≈ 0.97`, `p = 1/1001` throughout. This exceeds the published Naibbe surface scored under the same gate in Issue #68 (`0.883 / 0.900`) and every model in the Issue #75 ladder to date (M2 `0.29`, M3 `0.59`, M4 `0.62`, M5 `0.73`; see Section 4). It also has the best cross-fitted held-out log-likelihood of any non-saturated model (`−5.04` nats/token vs `−5.12` for G5 with the same nominal parameter count).

The fitted grammar is readable. On ZL3b fold 0, for example: from slot 3 (gallows `t/k/p/f`) the next occupied slot is 6 (`e`-group) or 8 (`o/a`) with probability `0.37` each, or 4 (`ch/sh`) with `0.21`; from slot 8 the successor is 10 (`d/l/r/m/n`) with `0.59` or 9 (`i`-group) with `0.36`; slot 9 is followed by slot 10 with probability `1.00`; after slot 10 the token stops with probability `0.91`; slot 11 (final `y`) is reached from slots 3–7 with probability `0.90–0.98`. These are structural transition tendencies under the frozen 12-slot coordinate system. They are not letter meanings.

## 4. Relation to Issue #75

OGH-A was planned, implemented and frozen from post-Issue-#72 `main`. After the pre-reveal head was committed, the GitHub issue list showed that Issue #75 ("minimal generator of the replicated 12-slot residual token grammar", branch `issue75-minimal-occupancy-generator`, not yet on `main`) had already run Phases A–F0 on the same question during 2026-09-01. No OGH-A model, seed, gate or classification was changed after that discovery; this section only maps the two ladders onto each other.

| OGH-A | Issue #75 | relation |
|---|---|---|
| G0 independent Bernoulli (renormalized non-empty) | M0 non-empty main-effect maxent | same distribution family |
| G1 admissible uniform | — | new: representation-only control |
| G2 admissible maxent, marginals | ≈ M0 (differs only by the 18 inadmissible states) | near-duplicate |
| G3 admissible maxent, marginals + count | M1 (K distribution + conditional main effects) | same distribution family |
| G4 last-occupied-slot left-to-right grammar (78 params) | — | new compact class; distinct from M3 (K/R/S + nearest-neighbour chain, 21 params), M4 (+distance), M5 (two-mode mixture, 43 params), M6 (K/R/S-gated two-mode, 46 params) |
| G5 full pairwise maxent (78 params) | — | new second-order sufficiency control; #75 deliberately excluded an unrestricted pairwise fit as a *candidate*; OGH-A uses it as a labelled non-promoting control |
| G6 empirical signature resampling | M+ (MPLUS-A/B) | same |

Harness differences: #75 uses 31 realizations per family and a strict sufficiency criterion (`T = min(R_ZL3b, R_IT2a)` must lie within the q95 self-difference `0.0098` of the M+ centre); OGH-A uses 3 realizations, both skeletons (ZL3b and IT2a), and the Issue #68 R1 pass gate (`r ≥ .70`, signs `≥ 50/66`, familywise `p ≤ .01`, existence). Both use candidate-owned 1,000 reference + 1,000 test line-local nulls, the same parser, the same five physical-leaf folds and the same frozen target vectors. Issue #75 results at the time of writing: M0 median `T = −0.110`, M1 `−0.167`, M2 `0.287`, M3 `0.593`, M4 `0.623`, M5 `0.725`, M+ `≈ 0.965`; M6 target reveal pending.

OGH-A therefore contributes three things Issue #75 does not yet contain: an independent-harness replication of the Phase-A fork (G0/G3/G6 vs M0/M1/M+) on both skeletons; a direct answer to whether the topology is **second-order sufficient** (G5); and one more compact candidate class (G4) whose held-out predictive fit can be compared with the #75 ladder.

Under Issue #75's stricter criterion (median `T = min(r_ZL3b, r_IT2a)` within `0.0098` of the M+ centre), neither G4 nor G5 would be called sufficient: the OGH-A three-realization median gaps to G6 are reported in Section 6: `−0.064` (ZL3b arm) and `−0.062` (IT2a arm) for G4; `−0.001` and `−0.012` for G5. G4 is therefore clearly outside the tolerance, while the pairwise control is inside it on the ZL3b arm and marginally outside on the IT2a arm. The two criteria answer different questions. The Issue #68 gate asks whether a mechanism reproduces R1 as well as a serious cipher candidate must; the Issue #75 criterion asks whether it is statistically indistinguishable from memorizing the inventory. OGH-A's classification label is defined by the former, as frozen in the plan; the latter is reported alongside so that the two ladders can be read together.

## 5. Interpretation and limits

Supported:

- The replicated 66-edge R1 topology is a property of *which slot subsets co-occur* inside a token, not of slot prevalence, occupancy count, parser admissibility, or token placement.
- That property is, to within about `0.01` of correlation, second-order: pairwise slot couplings carry it; on the ZL3b arm the pairwise control is statistically indistinguishable from the empirical ceiling under the Issue #75 criterion.
- A compact, interpretable left-to-right successor grammar (78 counted probabilities) generates it well enough to pass the same R1 gate that the Issue #68 tournament applies to candidate mechanisms, on both independent readings and both skeletons, without any access to the target graph.

Not supported and not claimed:

- that G4 is the historical production rule, or that slots carry meaning;
- that G4 is sufficient under the Issue #75 M+-equivalence criterion;
- anything about plaintext, semantics, cipher tables, spaces as words, Naibbe, Latin, or decipherment;
- anything about R2 (recurrence), R3 (paragraph entry) or R4 (reversibility), which remain independent responsibilities.

Design limits: three realizations per model (Issue #75 uses 31); the first reveal ran locally rather than on GitHub Actions (the headline job ZL3b/G4/rep0 was then replayed on Actions run `33558417211` with byte-identical corpus and residual vector, see `first-reveal/PROVENANCE.md`); the IT2a arm inherits the ZL3b physical-leaf fold definition, as in #58D.

## 6. Stochastic sensitivity (realizations 1 and 2)

All 42 jobs completed (0 drops, 0 rerolls). Pass/fail is identical across all three realizations for every model on both arms. `T = min(r_ZL3b, r_IT2a)`; the last column is the Issue #75-style gap of the median T to the G6 median T.
#### ZL3b skeleton — primary realization (rep 0)

| model | params | E | W | p_exist | r ZL3b | signs ZL3b | r IT2a | signs IT2a | held-out LL | R1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| G0 independent Bernoulli | 12 | 1.1724 | 0.0960 | 0.0220 | 0.0937 | 34/66 | 0.0880 | 33/66 | -7.070 | fail |
| G1 admissible uniform | 0 | 0.9041 | -0.0828 | 0.8492 | 0.0931 | 39/66 | 0.0631 | 38/66 | -8.313 | fail |
| G2 maxent marginals | 12 | 1.7678 | 0.4617 | 0.0010 | 0.0252 | 37/66 | 0.0390 | 38/66 | -7.050 | fail |
| G3 maxent marginals+count | 23 | 3.2570 | 0.3125 | 0.0010 | 0.0576 | 38/66 | 0.0202 | 37/66 | — | fail |
| G4 last-occupied grammar | 78 | 3.1279 | 0.9724 | 0.0010 | 0.9173 | 62/66 | 0.9326 | 63/66 | -5.042 | **PASS** |
| G5 pairwise maxent (control) | 78 | 3.2208 | 0.9872 | 0.0010 | 0.9513 | 63/66 | 0.9483 | 64/66 | -5.119 | **PASS** |
| G6 empirical resampling (ceiling) | 611 | 3.2494 | 0.9899 | 0.0010 | 0.9674 | 64/66 | 0.9646 | 65/66 | — | **PASS** |

#### ZL3b skeleton — all three realizations (r ZL3b / r IT2a; T = min)

| model | rep0 | rep1 | rep2 | median T | gap to G6 median T |
|---|---|---|---|---:|---:|
| G0 | 0.094 / 0.088 | -0.281 / -0.271 | -0.161 / -0.120 | -0.1610 | -1.1256 |
| G1 | 0.093 / 0.063 | -0.009 / -0.000 | -0.013 / -0.001 | -0.0090 | -0.9735 |
| G2 | 0.025 / 0.039 | 0.047 / 0.048 | 0.082 / 0.070 | 0.0465 | -0.9180 |
| G3 | 0.058 / 0.020 | 0.052 / 0.024 | 0.080 / 0.018 | 0.0202 | -0.9444 |
| G4 | 0.917 / 0.933 ✓ | 0.901 / 0.925 ✓ | 0.900 / 0.921 ✓ | 0.9011 | -0.0635 |
| G5 | 0.951 / 0.948 ✓ | 0.966 / 0.963 ✓ | 0.969 / 0.966 ✓ | 0.9634 | -0.0011 |
| G6 | 0.967 / 0.965 ✓ | 0.965 / 0.962 ✓ | 0.967 / 0.966 ✓ | 0.9646 | +0.0000 |

#### IT2a skeleton — primary realization (rep 0)

| model | params | E | W | p_exist | r ZL3b | signs ZL3b | r IT2a | signs IT2a | held-out LL | R1 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| G0 independent Bernoulli | 12 | 1.1454 | -0.0143 | 0.0470 | -0.2067 | 28/66 | -0.1939 | 27/66 | -6.997 | fail |
| G1 admissible uniform | 0 | 1.0452 | 0.0609 | 0.2757 | 0.1307 | 39/66 | 0.1380 | 40/66 | -8.313 | fail |
| G2 maxent marginals | 12 | 1.9761 | 0.4173 | 0.0010 | 0.0240 | 36/66 | 0.0315 | 37/66 | -6.975 | fail |
| G3 maxent marginals+count | 23 | 3.1939 | 0.4728 | 0.0010 | 0.0490 | 38/66 | 0.0936 | 37/66 | — | fail |
| G4 last-occupied grammar | 78 | 3.1969 | 0.9748 | 0.0010 | 0.9075 | 62/66 | 0.9333 | 63/66 | -5.014 | **PASS** |
| G5 pairwise maxent (control) | 78 | 3.2196 | 0.9795 | 0.0010 | 0.9589 | 64/66 | 0.9600 | 65/66 | -5.090 | **PASS** |
| G6 empirical resampling (ceiling) | 629 | 3.2658 | 0.9845 | 0.0010 | 0.9666 | 64/66 | 0.9641 | 65/66 | — | **PASS** |

#### IT2a skeleton — all three realizations (r ZL3b / r IT2a; T = min)

| model | rep0 | rep1 | rep2 | median T | gap to G6 median T |
|---|---|---|---|---:|---:|
| G0 | -0.207 / -0.194 | -0.203 / -0.188 | -0.013 / -0.028 | -0.2025 | -1.1720 |
| G1 | 0.131 / 0.138 | 0.113 / 0.110 | 0.006 / -0.009 | 0.1097 | -0.8598 |
| G2 | 0.024 / 0.031 | 0.045 / 0.045 | 0.072 / 0.064 | 0.0446 | -0.9249 |
| G3 | 0.049 / 0.094 | 0.011 / -0.000 | 0.135 / 0.122 | 0.0490 | -0.9205 |
| G4 | 0.908 / 0.933 ✓ | 0.895 / 0.926 ✓ | 0.919 / 0.943 ✓ | 0.9075 | -0.0620 |
| G5 | 0.959 / 0.960 ✓ | 0.954 / 0.955 ✓ | 0.959 / 0.957 ✓ | 0.9572 | -0.0124 |
| G6 | 0.967 / 0.964 ✓ | 0.973 / 0.970 ✓ | 0.971 / 0.971 ✓ | 0.9695 | +0.0000 |

## 7. Consequences for the program

1. **Reframe the Issue #75 search.** The missing information in the K/R/S, nearest-neighbour, distance-coupled and two-mode families is well described by *pair-specific* second-order couplings, and a successor-conditioned sequential grammar captures most of it compactly. The next preregistered rung should start from G4 and ask what small extension closes the remaining `≈0.06` to the pairwise ceiling: for example a second-order successor context (last two occupied slots), or K/R/S-gating of the successor table. No individual target edge may be used to choose it.
2. **Use G4 as a frozen mechanistic comparator.** In future joint tournaments, G4's R1 performance (`≈0.92`) is the bar a candidate mechanism's *emission* stage must clear, at a cost of 78 counted parameters, before its R2/R3/R4 behaviour is interesting.
3. **Downgrade higher-order configuration hypotheses for R1.** Latent construction states or non-pairwise configuration rules can add at most `≈0.01` topology correlation for R1 and should be motivated by R2/R3/R4 or by held-out likelihood, not by R1.
4. **Keep the ceiling honest.** G6 and G5 remain non-promoting controls; neither is an explanation.
