# Issue #72 — preregistered Naibbe R1 codebook/process decomposition

Status: **SUPERSEDED BEFORE ANY COUNTERFACTUAL R1 TARGET SCORE**

This historical plan was preregistered before the attempted Issue #72 first-reveal event. The first-reveal workflow run `33458765600` stopped in its chronology/firewall preparation step before any score job ran. GitHub Actions records `score=skipped` and `aggregate=skipped`; therefore no counterfactual 66-edge Q, residual-Z, E, W, topology, sign-agreement, p-value, or R1 class was revealed under this plan.

This plan is superseded prospectively because a subsequent criterion-validity audit identified causal-identification defects in the intervention meanings. It is retained as a historical design record only. **Do not execute it. Do not interpret any later test as if this plan were still normative.**

The superseding design must start from post-`research/RESEARCH_PROTOCOL.md` main and must separate criterion validity from statistical stringency.

## Why this plan was superseded

Two source-level facts prevent several intended interventions from being interpreted as one-factor causal ablations when the published encoder is simply rerun after a codebook change:

1. `UNAMBIGUOUS=True` rejects a proposed bigram according to emitted glyph strings and the global unigram/bigram collision catalog. Changing letter/state/table/glyph association can therefore change retry counts and accepted table-cell trajectories.
2. The published implementation uses the same global Python `random` stream for plaintext respacing, deck shuffling/table selection, retry-driven extra card draws, later deck reshuffles, and ciphertext space removal. A codebook intervention that changes a retry can therefore perturb downstream process choices unrelated to the nominated mapping change.

Consequently the old L/S/T/G rerun interventions mix direct emission-association effects with downstream process-trajectory effects. They may be valid as **total pipeline interventions**, but not as clean isolations of letter association, state specialization, or table allocation.

The old I control also cannot support its previous global causal label. It permutes the exact final token inventory produced by the full published pipeline. If that inventory retains R1, the result establishes only that the already-produced surface token multiset plus the retained layout is sufficient for the R1 statistic under that control. It does **not** identify whether the inventory arose from codebook structure, plaintext ordering, retry dynamics, table scheduling, or their interaction.

These are construct/identification defects, not failures of preregistration, null calibration, or multiple-comparison correction. Making the R1 gates harder would not fix them.

## Historical scientific question

The original question was:

> Is the already-observed Naibbe R1 match primarily carried by the emitted Voynich-like codebook/inventory, by particular codebook associations/state allocations, or by plaintext/encryption-process dynamics?

That question remains scientifically useful, but it requires a design in which the manipulated layer is actually identifiable.

## Historical common R1 statistic

The old plan intended to reuse Issue #68's R1 formalism:

- unchanged 12-slot `SlotParser(min)`;
- direct representation coverage gate `>=0.60`;
- all 66 unordered slot pairs;
- K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule-Q;
- candidate-owned 1,000 reference line-local nulls;
- independent 1,000 test line-local nulls;
- empirical mid-rank normal residual transform;
- residual energy `E=sqrt(mean(Z_e^2))`;
- fold reliability `W`;
- complete residual topology against frozen ZL3b #58C and IT2a #58D.

Those statistical procedures are not themselves invalidated. Their role must, however, be stated narrowly: they evaluate whether an emitted surface retains the replicated R1 token-construction constraint. They do not by themselves identify which upstream mechanism caused that surface property.

## Historical intervention families

The superseded design contained:

- P — within-line plaintext character-order shuffles followed by full rerun;
- L — global effective-letter association permutations followed by full rerun;
- S — state-allocation rotations followed by full rerun;
- T — table-allocation rotations followed by full rerun;
- G — global reachable-cell association permutations followed by full rerun;
- I — whole-token permutations of the exact published final surface.

The P intervention remains interpretable as a **total effect of plaintext-order perturbation through the entire published pipeline**, provided that wording is kept. It does not isolate plaintext order from its downstream retry/RNG consequences.

L/S/T/G require a trace-controlled emission design if they are to isolate emission-layer associations while holding the realized process path fixed.

I may remain a descriptive surface-sufficiency control but must not decide codebook-versus-process origin.

## Historical threshold note

The old `.90` / `.70` relative-effect bands and axis classes `R1_RETAINED`, `R1_MODULATED`, `R1_COLLAPSED` were prospectively fixed, but their numerical boundaries were pragmatic rather than empirically calibrated. Under `research/RESEARCH_PROTOCOL.md`, they would be T5-style decision bands and cannot be treated as inherently scientifically privileged merely because they are stringent.

The superseding design should prefer:

- the already-calibrated R1 constraint as an R1 surface-equivalence test;
- continuous effect sizes relative to the published surface;
- positive-control/replay variation where feasible;
- randomization or matched-control distributions for causal contrasts;
- no global causal label whose premises do not identify the claimed layer.

## First-reveal history

Attempted first-reveal run:

- run: `33458765600`;
- exact checked-out head: `afc04aaf597ae1042e62d204c1043dbff1df9999`;
- preparation job: `99704262365`;
- failure: chronology/firewall verification, before family exposure/scoring;
- score job: skipped;
- aggregate job: skipped.

Therefore the project remains target-unrevealed for Issue #72 counterfactual R1 decomposition.

## Superseding requirement

Before any new Issue #72 target score is allowed, the replacement plan must include a Criterion Validity Table under `research/RESEARCH_PROTOCOL.md` and must distinguish at minimum:

1. **published replay / positive control**;
2. **trace-controlled emission-association interventions** — process realization held fixed, emitted cell values reassigned;
3. **pipeline-total plaintext/process interventions** — rerun effects interpreted as total effects;
4. **surface-sufficiency controls** — explicitly descriptive, never promoted to upstream causal origin;
5. **matched negatives** that destroy the nominated dependency while preserving the relevant lower-order quantities.

The replacement plan must be committed before any counterfactual R1 target scoring.
