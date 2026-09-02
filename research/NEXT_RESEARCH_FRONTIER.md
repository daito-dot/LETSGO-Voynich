# Next research frontier — prospectively constrained reversible / inverse mechanism tournament

## CURRENT FRONTIER — after OGH-B: R1 is closed; move to slot values and cross-token responsibilities

OGH-B (`experiments/occupancy-generation-hierarchy/REPORT_B.md`) closed the gap OGH-A left: the target-blind selected second-order successor grammar (298 counted probabilities) reaches median `T = 0.948 / 0.962` on the ZL3b / IT2a skeletons, within `0.0165 / 0.0079` of the empirical-inventory ceiling (δ = 0.0098). Frozen decision `SUCCESSOR GRAMMAR NEAR-SUFFICIENT`. **No further R1 rung is licensed.**

The next plan-first question is:

> **How much information does a Voynich token carry beyond its slot shape, and does a complete memoryless token generator (shape + values) reproduce the cross-token constraints R2 and R3?**

Required shape: (1) value-level successor grammar fitted on training leaves, reported as held-out bits per token on both readings; (2) frozen R2/R3 scoring of the generated corpus with the Phase62/64 scorecards; (3) no target inspection during model definition. Everything below this line is the OGH-A-era frontier, retained for history.

## Previous frontier — after OGH-A: close the successor-grammar gap and re-enter the joint tournament

OGH-A (`experiments/occupancy-generation-hierarchy/REPORT_A.md`) and Issue #75 Phases A–F0 together resolve most of the post-#72 question "what generates the replicated R1 topology":

- not parser admissibility (4,077/4,095 signatures admissible, uniform fails);
- not slot marginals or occupied-slot count (strong residual energy, wrong geometry);
- yes, to within `≈0.01`, the **pairwise couplings** of the signature distribution (full pairwise maxent `r 0.948–0.969`);
- yes, to `r 0.91–0.93` on both readings and both skeletons, a **78-parameter left-to-right successor grammar** (next occupied slot conditioned on the last occupied slot), which passes the Issue #68 R1 gate that published Naibbe passed at `0.88–0.90`.

The next highest-value, target-blind question is therefore narrow:

> **Which minimal extension of the successor grammar closes the remaining `≈0.06` gap to the second-order ceiling, and does that grammar, embedded as the emission stage of a bounded reversible mechanism, help or hurt R2/R3/R4?**

Required shape of the next plan:

1. candidates: (a) second-order successor context (last two occupied slots), (b) K/R/S-gated successor tables (Issue #75 F0 direction), (c) unchanged G4 as anchor; select among (a)/(b) by cross-fitted held-out likelihood only;
2. score the selected family under both the Issue #68 gate and the Issue #75 M+-equivalence criterion, both skeletons, fixed realizations, no rerolls;
3. then carry the frozen grammar into a joint R1–R5 tournament as the emission-stage comparator; a mechanism whose emission stage cannot reach `r≈0.92` at ≤ 78 counted parameters is not competitive on R1.

Hard boundaries unchanged: no target-edge selection, no averaging of readings, no slot semantics, no repair of Naibbe R2/R3/R4.

Status: current frontier after OGH-A first reveal (2026-09-01).

## Previous frontier — after Issue #68: where does Naibbe's R1 match come from?


Issue #68 resolves the previous frontier. The manuscript's residual token-construction graph is real and transcription-robust, but it is **not unique to the manuscript or to A1-like generation**: published Naibbe C1-E0 reproduces it strongly while remaining a failed joint model.

The next highest-value question is therefore not another Voynich edge and not an immediate Naibbe repair.

> **Does Naibbe pass R1 because its homophonic/stateful encryption process generates the manuscript's construction grammar, or because its target-aware Voynich-like codebook/inventory already contains that grammar?**

Why this is now the frontier:

- R1 Naibbe vs ZL3b: `r=0.8830282501`, `60/66` signs.
- R1 Naibbe vs IT2a: `r=0.9000974100`, `61/66` signs.
- Naibbe residual existence/reliability are strong (`E=3.1784`, `W=.9547`, `p=1/1001`).
- Yet Naibbe R2, R3 and R4 all fail.
- Naibbe's concrete glyph codebook is explicitly target-aware, so R1 cannot yet be attributed to reversible encryption dynamics.

### Required next program shape

Start with a source/architecture audit and preregistration **before** counterfactual R1 scoring. Freeze a small family of controls that separates three causal components:

1. **published process + published target-aware codebook** — already observed Issue #68 reference;
2. **published process + codebook-association neutralization** — preserve prospective table/state/codebook capacity and glyph inventory while breaking the semantic/state-to-glyph association in a frozen outcome-independent way;
3. **inventory-only emission control** — preserve prospectively defined emitted-token/codebook marginals while removing plaintext/cipher dynamics, to ask whether the R1 graph is already an inventory property;
4. optionally, only if definable without using Issue #68 edge outcomes, a **non-target-aware codebook control** built from an external historical/synthetic authority.

The exact control construction must be frozen before executable scoring. Do not invent a neutralization after seeing which of the 66 edges Naibbe matches.

### Primary outcome

Use complete-graph residual existence and topology against both frozen ZL3b and IT2a references, with candidate/control-family maxT protection. Individual edges are diagnostic only after the family-level reveal and cannot promote a hypothesis.

### Interpretive gates

- **CODEBOOK/INVENTORY DOMINANT:** association-neutralized and/or inventory-only controls retain a comparably strong familywise R1 match. Then R1 is mainly an output-construction constraint and weak evidence about encryption process.
- **PROCESS/ASSOCIATION MATTERS:** published Naibbe remains strong while prospectively neutralized controls fail materially. Then the architecture/codebook interaction contains mechanism-specific structure worth deeper reversible-family testing.
- **INCONCLUSIVE:** support/representation/null reliability prevents a fair family comparison; do not repair controls after reveal.

### Hard boundary

This next phase does **not** try to make Naibbe pass R2, R3 or R4. Those failures remain frozen. The objective is to correctly interpret the surprising R1 success before using R1 to rank future inverse models.

Status: next plan-first frontier after successful Issue #58D independent-reading replication.

## Program-level purpose

Read `research/TOKEN_CONSTRUCTION_PROGRAM.md` first.

The project has spent many phases learning which Voynich surface properties are reproducible and which attractive explanations fail under held-out controls.

#58D crosses an important threshold: one major token-internal constraint is now portable across independent ZL3b and Takahashi/IT2a readings inside a common EVA/IVTFF framework.

The next high-information move is therefore **not another local structural discovery**.

It is to ask:

> **Which bounded reversible/generative mechanisms can satisfy the strongest already-established Voynich constraints simultaneously, on held-out material, without post-hoc repair?**

This is the transition from surface characterization toward mechanism discrimination and eventual inversion.

## Why the frontier moves here

### What #58C established

After edge-wise line-local null calibration:

> `RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`

ZL3b pooled residual energy was `3.23155` versus an independent test-null maximum `1.28318`, with `p=1/1001` and physical-leaf reliability `0.94471`.

### What #58D adds

IT2a/Takahashi independently reproduces the same object:

> `INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE`

Key evidence:

- IT2a residual energy `3.21363`;
- IT test-null maximum `1.25891`;
- `p_exist_IT = 1/1001`;
- `W_IT_ALL = 0.95377`;
- pooled ZL3b↔IT2a full-66-edge correlation `0.98845`;
- pooled sign agreement `65/66`;
- all eight planned cross-reading groups strongly replicate;
- independent test-null cross-reading correlation max `0.43199`;
- independent test-null sign-agreement max `47/66`.

Thus continuing to ask whether the ZL3b token graph is “real” has sharply diminishing information gain.

The cross-reading replicated structure should now be **used**, not merely measured again.

## Scientific object of the next phase

The next phase is not “solve the manuscript in one shot.”

It is a mechanism tournament with a common prospective scorecard.

A candidate mechanism is an explicit procedure capable of producing or transforming text-like input into a Voynich-like surface representation. Depending on family it may be:

- a reversible encoding/transform;
- a bounded shorthand/cipher-like transform;
- a structured generative mechanism used as a non-reversible comparator;
- a hybrid with explicitly declared state/memory.

Every candidate must declare before target scoring:

1. inputs available to the mechanism;
2. trainable parameters and where they are fitted;
3. state/memory available across tokens, lines and paragraphs;
4. whether exact reversal is claimed and how it is verified;
5. degrees of freedom / model-description cost;
6. which output constraints it is expected to reproduce.

## The joint constraint battery

The next plan must freeze an exact scorecard before candidate outcomes are inspected.

At minimum include the following independent responsibilities.

### C1 — cross-reading token-construction residual core

Candidate output must reproduce the **replicated token-internal construction signature**, not merely raw slot frequencies.

Do not use one selected edge.

The score should operate on the complete 66-edge residual representation or on a frozen lower-dimensional summary derived exclusively from the already completed #58C/#58D results before candidate outputs are inspected.

Candidate success should be compared with the empirical ZL3b/IT2a cross-reading tolerance, not an arbitrary visual notion of similarity.

### C2 — H62 short-range near-family recurrence geometry

Retain the prospectively successful H62-P1 geometry as a separate responsibility.

A candidate that matches token construction but loses the accepted short-range near-family recurrence profile is not a joint explanation.

### C3 — signed S1 paragraph-entry specialization

Retain S1 as a difficult discriminator.

Several otherwise plausible controls/mechanisms reproduce easier locality/line-position behavior but fail S1, sometimes with the wrong sign.

Do not average S1 away inside a large omnibus score.

### C4 — layout / line-position constraints

Use only the line-position quantities that remain scientifically informative after Phase62 and later refinements. Do not treat easy aggregate S3 as a strong discriminator merely because it is available.

### C5 — reversibility / recoverability when claimed

For any reversible family:

- exact decode of held-out transformed source must be tested;
- reversal must use only information the declared decoder would possess;
- hidden access to the original plaintext or target layout is forbidden unless explicitly part of the model and charged as complexity.

### C6 — complexity / freedom accounting

A candidate with enough paragraph-specific, section-specific or token-specific repair rules can imitate almost anything.

The tournament must therefore record and penalize at least:

- number/type of fitted parameters;
- size of learned symbol/code tables;
- state-space size;
- paragraph/section-conditioned rules;
- target-layout information supplied;
- training vocabulary or empirical token inventory supplied;
- any source-specific preprocessing chosen after target inspection.

The exact complexity score should be frozen before reveal.

## Candidate-family discipline

Do **not** start by adding terms to A1 until every residual disappears.

Do **not** construct a new cipher by inspecting the complete Voynich scorecard and adding one repair for each failed metric.

Instead, the next issue should first freeze a small set of **architecturally distinct candidate families** chosen for independent historical/mathematical reasons.

At least retain baseline anchors so gains are interpretable:

- source-native structured plaintext / N0-type baseline where applicable;
- bounded boundary-blind reversible recoding / C0-type baseline;
- the strongest serious previously tested C-family comparator where it can be replayed fairly;
- A1/A1-R1 as a structural-generation comparator, while explicitly charging its empirical dependencies and noting that it is not yet a historical reversible decoder.

Any genuinely new candidate family should be specified before its Voynich target score is known.

## Training / held-out separation

The next plan must state exactly what can be learned from training leaves and what is sealed on held-out leaves.

Preferred default:

- reuse stable physical-leaf folds when scientifically compatible;
- fit candidate parameters only on training leaves / source-side training data;
- evaluate the joint Voynich constraint battery on held-out leaves;
- where a candidate transforms external plaintext, keep plaintext-source selection independent of Voynich target fit.

If a different split is scientifically required, freeze it before candidate scoring and explain why.

## Multi-constraint decision logic

The next tournament should avoid one weighted average that lets a spectacular result on an easy metric hide a sign failure on S1.

Prefer responsibility gates.

A candidate can be classified roughly as:

### `JOINT-CONSTRAINT COMPETITIVE`

Only if it passes all preregistered hard responsibilities, including token-construction core, H62, and S1, under acceptable complexity/reversibility conditions.

### `PARTIAL STRUCTURAL MODEL`

If it passes a meaningful subset but fails at least one hard responsibility.

### `OVERFIT / EXCESS-COMPLEXITY`

If apparent fit requires complexity or target access beyond the frozen allowance.

### `NOT COMPETITIVE`

If it fails the primary structural responsibilities despite adequate support.

Exact numerical gates must be frozen in the next issue plan; the labels above define responsibility boundaries, not post-hoc thresholds.

## Critical distinction: generator vs decoder

The project currently has evidence for **surface-generation constraints**, not a decoded plaintext.

A non-reversible generator can teach us what architecture reproduces the surface, but it cannot by itself decipher the manuscript.

Therefore every candidate must be labeled as one of:

- `surface generator only`;
- `reversible transform / decoder candidate`;
- `control / null`.

Do not let an excellent non-reversible generator silently become a “decipherment.”

## What a successful tournament changes

### One reversible family becomes joint-constraint competitive

Then freeze it further and demand stronger inverse evidence:

- unseen-token or unseen-paragraph prediction;
- exact decode/re-encode closure;
- independent content or historical consistency tests;
- robustness to transcription/representation changes.

### A non-reversible generator alone is competitive

This would clarify the production architecture but not solve the inverse problem. Use it to derive new constraints on what a reversible mechanism must emulate.

### All bounded candidates fail

This is useful evidence if the failures are structurally distinct.

Do not immediately add a universal repair model. Identify which responsibility separates the families and preregister the next architectural hypothesis.

## Secondary robustness lane — GC2a/v101

#58D is an independent reading-lineage replication but not a wholly independent alphabet/publication representation.

A future GC2a/v101 lane could test a **coarser representation-invariant token-construction object**.

However, v101→EVA mapping search must not be mixed into the inverse tournament because it creates a large outcome-dependent degree of freedom.

Open that lane separately if/when the remaining representation objection becomes decision-relevant.

## Prohibited shortcuts

Do not:

- call visible delimiters proven words;
- convert token construction into sentence syntax without a new program;
- choose only the strongest #58C/#58D edges for model evaluation;
- tune a candidate until it passes each revealed failure and call the same phase confirmatory;
- hide S1 sign failure inside a weighted omnibus score;
- call an irreversible generator a decoder;
- infer semantics from structural fit alone;
- give candidate models hidden access to held-out target statistics;
- use model complexity without charging it;
- claim decipherment from surface reproduction.

## Repository sequence

1. finish integrating #58D first-reveal archive, report and accepted-state documents to `main`;
2. close Issue #66 only after post-merge main verification;
3. create a new issue for the joint-constraint mechanism tournament from post-#58D main;
4. document the **constraint battery and candidate-family eligibility before implementing candidate scoring**;
5. audit exact replayability of reused A1/C0/C1 baselines;
6. freeze common train/test populations, complexity accounting and outcome classes;
7. only then implement and run the first tournament reveal;
8. preserve failures without post-hoc repair.

## One-line handoff

> **The token-construction signature has now survived an independent reading. Stop searching for another local edge. Use the replicated 66-edge constraint, H62 recurrence geometry, and S1 paragraph-entry signal as a frozen multi-responsibility test that candidate reversible/generative mechanisms must jointly survive.**
