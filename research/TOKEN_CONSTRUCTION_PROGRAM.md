# Token-construction program — purpose, object, and decision path

## Program update — OGH-C closes the token-internal chapter

A parsed Voynich token carries ≈ `9.7` bits under the best compact memoryless grammar (`7.0` shape, ≈ `2.7` values). A complete memoryless token generator reproduces none of the cross-token responsibilities (S1, S2, S3 ≈ 0.03× Voynich; raw H62 excess ≈ 1/10). The lane's object moves from token-internal construction to **cross-token memory** (`REPORT_C.md`). Frozen G4/G7A/V2 remain as emission-stage comparators.

## Program update — OGH-B closes the R1 generation lane

The target-blind selected second-order successor grammar (G7A, 298 counted probabilities) reproduces the replicated 66-edge R1 topology to within `0.01–0.02` of inventory memorization on both readings (`REPORT_B.md`). R1 is henceforth a cheap necessary condition on a candidate mechanism's emission stage, not a discriminator. The lane's next object is the **value** filling each occupied slot and the cross-token responsibilities R2/R3.

## Program update — OGH-A identifies a compact second-order successor grammar behind R1

After Issue #72 (R1 lives in the occupancy-signature inventory) and Issue #75 Phases A–F0 (low-order and local-chain families insufficient), OGH-A establishes:

- R1 is **second-order sufficient to within ≈0.01** (pairwise maxent control `r 0.948–0.969` vs empirical ceiling `≈0.965`);
- a **left-to-right successor grammar** with 78 counted conditional probabilities (occupy slot `s` with a probability that depends only on the last occupied slot) passes the Issue #68 R1 gate on both readings and both skeletons (`r 0.91–0.93`, `62–63/66` signs), the first compact, interpretable token-construction rule to do so;
- parser admissibility, slot prevalence and occupancy count do not generate the topology.

The lane's object is therefore now: **the successor grammar of occupied structural positions inside one space-delimited token**, and how much of the remaining `≈0.06` correlation gap a minimal extension recovers. The grammar is structural; it assigns no meaning to slots and says nothing about R2/R3/R4.

Authorities: `experiments/occupancy-generation-hierarchy/PLAN_A.md`, `REPORT_A.md`, `research/HYPOTHESIS_LEDGER_ADDENDUM_OGH_A.md`.

## Program update — Issue #68 changes the evidential role of the token-construction graph

The core empirical finding remains accepted:

> Voynich space-delimited tokens, under the frozen 12-slot representation, exhibit a strong non-null residual construction graph that replicates across independent ZL3b and IT2a readings.

Issue #68 adds a crucial mechanism-control result:

> Published target-aware Naibbe C1-E0 also passes the complete-66 R1 residual constraint very strongly (`r=.883` vs ZL3b, `.900` vs IT2a; `60/66` and `61/66` signs; familywise `p=1/1001`).

Therefore the program must distinguish **existence of the token-construction rule** from **identification of the historical process that produced it**.

Current responsibility hierarchy:

- **R1 token construction:** strong, replicated output-grammar constraint; no longer sufficient alone to rule out reversible cipher families.
- **R2 short-range recurrence geometry (H62):** dynamic/local-family responsibility not automatically implied by R1; Naibbe fails the frozen joint gate.
- **R3 signed paragraph-entry S1:** currently the hardest tested structural discriminator; Naibbe is wrong-sign in all five frozen comparisons.
- **R4 inverse closure:** source-side requirement for a claimed decoder; published Naibbe closes uniquely/exactly on only `1167/1778` primary lines under the frozen rule.
- **R5 access/complexity:** protects against target-guided repair.

The token-construction program should now ask **what layer R1 lives in**: codebook inventory, codebook association, encryption/generation process, or an interaction among them. The next phase must decompose that question prospectively at complete-graph level.

Do not reinterpret R1 PASS as evidence for Naibbe historical identity, Latin plaintext, or encryption. Conversely, do not discard R1 because a target-aware cipher can reproduce it. Its role is now precisely defined as one constraint in a joint falsification system.

Status: normative orientation for the token-construction research lane.

This document exists so that a future researcher or agent can recover **why this lane is being run** before reading individual statistics. Phase-specific frozen plans, first-reveal artifacts, and reports remain authoritative for exact methods and numbers.

## One-sentence purpose

> Determine which internal construction constraints of Voynich **space-delimited tokens** are reproducible enough across manuscript strata and independent readings to become prospective restrictions on later reversible/generative/inverse models.

## What the object is

The object is **not sentence grammar** and it is not yet a claim about natural-language words.

We use `space-delimited token` deliberately because the manuscript's visible spaces have not been established as natural-language word boundaries.

For the established representation, a parsed token is described through a frozen 12-slot construction. Each slot can be occupied or empty. The program has asked:

- which slots tend to co-occur;
- which slots tend to exclude one another;
- which dependencies remain after controlling for simpler occupancy structure;
- whether the residual dependency system is shared across manuscript strata;
- whether that system survives an independent manuscript reading lineage rather than being a peculiarity of ZL3b.

A relation such as `slot3 occupied -> slot5 unusually absent` is a **token-internal construction constraint**. It is not, by itself, a meaning assignment, plaintext-letter relation, or cipher table.

## Why this matters to decipherment

A candidate decipherment/generative model should not be allowed to explain arbitrary token forms after the fact. It should prospectively reproduce manuscript-level surface constraints that have already survived independent controls.

The token-construction lane initially asked:

> **How many token-generation systems are we trying to invert?**

Then:

> **Which token-internal constraints survive lower-order controls?**

After #58D, the operative question becomes:

> **Which reversible/generative mechanisms can satisfy those replicated constraints together with the other strongest Voynich constraints without post-hoc repair?**

The structural signature still does not tell us whether the underlying information is natural language, ciphered text, artificial text, or another structured source.

## What has been established

### Issue #55

A selected slot3×slot5 relation was real, but #55B showed that essentially all measured dependence reduced to the binary fact that the two slots are almost never occupied together.

> `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`

This established a token-internal occupancy constraint, not a semantic interpretation.

### Issue #58A

The selection-aware complete-graph audit tested all `C(12,2)=66` slot pairs instead of privileging slot3×slot5.

> `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

Twenty-two edges qualified under the frozen family-wise primary rule. The object therefore moved from one selected pair to the **complete signed occupancy graph**.

### Issue #58B

Observed complete signed graphs looked highly similar across Currier/section/line-position strata, but the exact line-local marginal-preserving null also generated correlations near `0.95`.

> `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`

> `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

This showed that raw graph similarity was contaminated by lower-order slot prevalence / line-local occupancy architecture.

### Issue #58C / #64

#58C calibrated every one of the 66 conditional edges against its own line-local occupancy-null distribution, using separate 1,000-reference and independent 1,000-test null ensembles.

> **`RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`**

Pooled ZL3b:

- `E_ALL = 3.23155`;
- independent test-null maximum `1.28318`;
- `p_exist_ALL = 1/1001`;
- `W_ALL = 0.94471`.

All seven planned strata independently contained the residual structure. Currier-B section comparisons and interior/final were stable; Currier A/B and line-initial comparisons were related but modulated; none met the materially different-grammar gate.

The lower-order explanation exposed by #58B was therefore insufficient.

### Issue #58D / #66

#58D prospectively challenged #58C with the independent Takeshi Takahashi / IT2a reading.

Stage A froze the source before science and showed:

- exact historical/current IT2a bytes;
- 99/99 physical leaves shared with #58C;
- 34,411 clean tokens;
- 28,280 accepted by the unchanged 12-slot parser;
- 82.18% coverage.

IT2a then received an independent line-local residual calibration.

Frozen result:

> **`INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE`**

Independent IT2a residual existence:

- `E_IT_ALL = 3.21363`;
- test-null maximum `1.25891`;
- `p_exist_IT = 1/1001`;
- `W_IT_ALL = 0.95377`.

Direct complete-graph ZL3b↔IT2a replication over **all 66 edges**:

- pooled Pearson `0.98845`;
- pooled sign agreement `65/66`;
- both maxT p-values `1/1001`.

All eight planned groups meet the frozen strong cross-reading topology class:

- Pearson `0.97031–0.99548`;
- sign agreement `64/66–66/66`;
- all maxT p-values `1/1001`.

Within IT2a, the same broad family result reappears:

> `REGISTER/SECTION RESIDUAL MODULATION`

> `LINE-POSITION RESIDUAL MODULATION`

The secondary exact ordering of historically stable vs modulated contrast sets did not pass its `.05` gate (`p=.08791`). Broad geometry replicates; every fine ranking does not.

## Current working interpretation

The strongest supported token-construction statement is now:

> **Within a common EVA/IVTFF representational framework, Voynich space-delimited tokens exhibit a manuscript-level internal construction signature that survives independent ZL3b and Takahashi/IT2a readings. A broad residual core is shared across manuscript strata with measurable modulation rather than an exactly uniform token grammar.**

The complete residual topology is no longer merely a ZL3b-specific descriptive statistic. It is sufficiently cross-reading replicated to become a **prospective surface-generation rejection criterion**.

This is not a claim that the 12-slot representation is uniquely historical. It is the strongest tested structural coordinate system so far for this object.

## What remains uncertain

### Representation independence is not absolute

IT2a and ZL3b are distinct reading lineages but share an EVA/IVTFF ecosystem. #58D therefore does not prove alphabet/publishing-pipeline independence.

GC2a/v101 remains a useful future robustness lane if a coarser, independently motivated cross-alphabet invariant can be preregistered without tuning to the observed residual graph.

### The historical mechanism is unknown

The residual graph says how viable surface outputs are constrained. It does not tell us what historical operation generated those constraints.

That is now the high-value problem.

## Next scientific move

Do **not** continue discovering or retesting individual occupancy edges merely because they are available.

The next frontier should be a plan-first **constrained reversible/inverse model tournament**.

Before any candidate target outcomes are inspected, freeze a common scorecard requiring models to reproduce, on held-out material:

1. cross-reading replicated residual token-construction structure from #58C/#58D;
2. accepted A1/H62 short-range near-family recurrence geometry;
3. the difficult signed S1 paragraph-entry specialization;
4. any additional manuscript-level constraints selected prospectively;
5. exact reversibility/decodability where the model family claims a reversible encoding;
6. explicit complexity and degrees-of-freedom cost.

Candidate families should be allowed to fail. A mismatch must not automatically generate a new repair parameter inside the same confirmatory test.

The practical purpose is to turn accumulated structural knowledge into **mechanism discrimination**.

## Decision path from here

### A bounded reversible mechanism satisfies the joint held-out scorecard

Promote that family to a serious inverse/decoding candidate and require unseen prediction or recoverable content under separately frozen tests.

### A mechanism reproduces easy structure but fails S1 or replicated token construction

Reject or sharply narrow that mechanism family rather than repairing it post hoc.

### No tested bounded family satisfies the joint constraints

Use the pattern of independent failures to identify what architectural ingredient is missing, then preregister a genuinely new mechanism family.

### Cross-alphabet robustness becomes a specific live objection

Open a separate plan-first GC2a/v101/coarser-invariant lane. Do not mix cross-alphabet mapping search into the inverse tournament after seeing mechanism results.

## Interpretation boundaries

This lane must not silently become any of the following:

- a proof that spaces are true word boundaries;
- sentence-level syntax analysis;
- semantic assignment to slots;
- a plaintext alphabet or cipher-table inference;
- evidence for or against all ciphers;
- evidence that the manuscript is meaningless;
- identification of one historical generator;
- decipherment.

## Handoff rule for future agents

Before continuing this lane, state the research object and current result in plain language:

> **We are studying how one space-delimited Voynich token is internally assembled, not whole-sentence grammar. The non-trivial slot-to-slot construction signature survives lower-order controls and an independent Takahashi reading: the full ZL3b↔IT2a residual graph correlates about 0.988 with 65/66 signs agreeing. The next task is no longer to find another local rule; it is to use the replicated rule set, together with recurrence and paragraph-entry constraints, to reject or retain prospectively defined reversible/generative mechanisms.**

Then read, in order:

1. this file;
2. `research/STATUS.md`;
3. `experiments/slot35-dependency/REPORT_B.md`;
4. `experiments/occupancy-graph/REPORT_A.md`;
5. `experiments/occupancy-graph-stability/REPORT_A.md`;
6. `experiments/occupancy-graph-residual/REPORT_A.md`;
7. `experiments/occupancy-graph-independent-transcription/REPORT_A.md`;
8. `experiments/occupancy-graph-independent-transcription/first-reveal/PROVENANCE.md`;
9. `research/NEXT_RESEARCH_FRONTIER.md`;
10. the frozen plan for the next inverse/mechanism phase.

Do not let the mechanics of a local statistic replace the program-level question.