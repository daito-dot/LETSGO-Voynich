# Token-construction program addendum — Issue #75 Phase A

Status: **NORMATIVE PROGRAM UPDATE AFTER PHASE A**

Read with `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

## Program-level change

Issue #72 localized R1 to the corpus inventory of parsed 12-slot occupancy patterns rather than exact plaintext order or final token placement.

Issue #75 Phase A now identifies what information inside that inventory cannot be removed.

Three prospectively ordered controls were tested under five-fold cross-fitting and against both frozen ZL3b and independent IT2a target graphs:

1. **M0: slot marginals only** — failed strongly;
2. **M1: slot marginals + occupied-slot count K** — produced strong residual structure but the wrong complete-graph geometry;
3. **M+: empirical 12-bit signature resampling** — succeeded strongly in two independent positive-control banks.

Frozen classification:

`LOW_ORDER_MODELS_INSUFFICIENT_EMPIRICAL_PATTERN_STRUCTURE_REQUIRED`

## New scientific object

The research object is now narrower than “token grammar” in general.

The unresolved information is:

> **Which subsets of the 12 structural positions are permitted or preferred together inside one token, beyond individual slot prevalence and the total number of occupied positions?**

M1 shows why this distinction matters. Occupancy-count regulation alone creates large residual energy (`E≈3.25`) but a topology mildly anticorrelated with Voynich. Therefore a strong graph can be generated for trivial combinatorial reasons while still being the wrong graph.

The program should distinguish:

- **graph existence** — easy to generate from K constraints;
- **graph geometry** — requires configuration-specific information;
- **empirical-pattern memorization** — sufficient but non-explanatory;
- **compact configuration grammar** — current target.

## Revised mechanism-discrimination path

The next stage should not return to individual edge discovery or token placement.

It should prospectively bridge the gap between M1 and M+ with models that encode progressively more configuration information without directly fitting the frozen 66 edges.

Ordered next questions:

1. Can a small set of generic shape descriptors explain which 12-bit patterns occur?
2. If not, can a compact latent/state construction process generate the required pattern inventory?
3. How much information/complexity is required before topology approaches the empirical-signature positive control?
4. Does any compact occupancy generator also help independent responsibilities R2/R3/R4 when embedded in a reversible/generative mechanism?

A successful occupancy generator is not yet a decipherment mechanism. It becomes historically interesting only if it survives the independent joint scorecard.

## Current handoff statement

Future agents should begin this lane with:

> **Voynich tokens exhibit a replicated 12-slot residual occupancy grammar. The graph is not explained by individual slot frequencies or by the distribution of how many slots a token occupies: M0 and M1 are strongly wrong, while cross-fitted empirical complete-pattern resampling reproduces the graph at about R=.965 against both independent readings. The open problem is now to identify the smallest generic rule governing which slot subsets co-occur inside a token, without fitting the 66 target edges directly.**

Exact Phase-A method/result authorities:

- `experiments/minimal-occupancy-generator/PLAN_A.md`
- `experiments/minimal-occupancy-generator/REPORT_A.md`
- `experiments/minimal-occupancy-generator/stage-a0/`
- `experiments/minimal-occupancy-generator/stage-a-first-reveal/`
- `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE75_PHASE_A.md`
