# Predictive-information program — near-term research direction

Date: 2026-09-06
Authority issue: #88
Status: **NORMATIVE FOR THE NEXT RESEARCH CYCLE**

## Governing question

The current program-level question is:

> **What information makes the next Voynich space-delimited unit predictable, how much predictive information exists beyond the frozen memoryless V2 emission grammar, and where does that information reside?**

A prerequisite question remains explicit:

> **Is the visible-space-delimited unit the right production unit for this analysis, even if it is not a natural-language word?**

This replaces the premature framing "find the hidden state behind the generator" as the immediate research objective.

## Why this is the correct next level

Current results separate three things that must not be conflated:

1. **surface-statistic reproduction** — R1, S1, S2 and H62;
2. **predictive information** — actual held-out reduction in code length for unseen tokens;
3. **historical / semantic mechanism** — what information the writer actually used when producing the manuscript.

Issue #81 showed why this distinction matters. X2 near-family memory creates a large recurrence effect and recovers much of S2, but improves held-out surface prediction by only about `0.059 bit/token` and overshoots raw H62 by about `2.1x`. X3 paragraph ENTRY/BODY state separately recovers much of S1. A conspicuous recurrence statistic therefore need not imply a large cross-token information rate.

Issue #84 A-C also narrows the easy alternatives: the inter-token regime is robust across seven readings and is not jointly reproduced by the frozen 101-language panel, the frozen common reversible-operation representatives, or the ten historical recipe/herbal/account/liturgical source controls. This licenses mechanism discrimination, but not an assumption that a rich latent state exists.

## Near-term research sequence

### Phase 0 — close the already-licensed soft-memory question

Complete the independently motivated soft near-family / recency-kernel follow-up to Issue #81.

Selection rule:

- model and hyperparameter choice by training-only / nested held-out literal-surface likelihood;
- S1/S2/H62 target values unavailable to the selector;
- V2 emission grammar remains frozen;
- R1 remains a necessary surface condition.

Scientific role:

> Determine whether local S2/H62 geometry can be closed by a small target-blind local mechanism without the X2 raw-recurrence overshoot.

This is a **surface-closure experiment**, not identification of the historical generator.

Only a prospectively sufficient near-family component may later be composed with the already-supported X3 ENTRY/BODY state.

### Phase 1 — predictive-information budget

Measure the incremental held-out code-length gain beyond V2 as increasingly informative context is supplied.

Primary output:

> **held-out bits/token relative to frozen V2, reported as an incremental predictive-gain curve.**

Prospectively distinguish at least:

- V2 emission only;
- short local token history;
- recency / near-family history;
- observable line and paragraph position;
- folio / section / Currier / scribe metadata where an independent authority exists;
- longer token history;
- a separately frozen flexible sequence predictor used only as an empirical challenger for remaining predictable structure.

Do not call the flexible predictor an entropy bound. It is an empirical model-class ceiling only.

Decision fork:

- if strong challengers yield only a small additional held-out gain, then cross-token structure is statistically conspicuous but information-light and rich latent-state interpretation is not licensed;
- if large reproducible predictive gain remains, the current summary statistics miss substantial sequence structure and source attribution becomes the priority.

### Phase 2 — locate the predictive information

Partition predictive gain prospectively among:

A. **endogenous local history** — copy/mutate, near-family, recency/cache effects;

B. **observable document state** — line/paragraph position, folio, section, Currier class, scribe or other independently defined metadata;

C. **longer-range sequence context** — information not reducible to A/B;

D. **latent state** — only if A-C leave reproducible held-out predictive information;

E. **external input / content** — indirectly implicated when prediction depends on domain/section and does not transport as a universal production rule.

Use nested ablations and conditional code-length differences. Do not infer causal shares from one omnibus fitted model without ablation.

### Phase 3 — transport tests

A rule becomes more plausibly a manuscript-wide production mechanism only if it transports.

Where support permits, prospectively evaluate:

- Currier A -> Currier B and reverse;
- one section/domain -> held-out section/domain;
- one scribe -> held-out scribe;
- folio groups -> unseen folio groups.

Report:

- absolute held-out code length;
- degradation relative to within-stratum training;
- vocabulary/support mismatch separately from transition/mechanism mismatch.

Interpretation:

- strong transport with nearly unchanged parameters supports a content-independent production mechanism;
- material non-transport points toward content/external-state dependence, multiple production regimes, or representation mismatch.

### Phase 4 — boundary / segmentation validity

Visible spaces are not assumed to be natural-language word boundaries.

Before broad alternative-tokenization search, ask the narrower production-boundary question:

> **Do visible spaces mark a reproducible statistical reset or discontinuity relative to within-token construction?**

Any alternative segmentation must be defined by external or training-only criteria before target scoring. Target-guided boundary search is forbidden.

Possible outcomes:

- spaces are stable production boundaries without being language-like word boundaries;
- the main predictive effects survive reasonable boundary perturbations;
- the anomalies collapse under a prospectively motivated alternative segmentation, forcing reinterpretation of current token-level comparisons.

Phase 4 may move earlier if the boundary assumption becomes the dominant threat to validity.

## Licensing rule for latent-state work

A rich latent-state search is **not** licensed merely because hidden-state models can fit Voynich.

It becomes licensed only if all of the following hold:

1. Phase 1 finds material held-out predictive information beyond simple/local/observable-state models;
2. Phase 2 shows that the residual is reproducible and is not a vocabulary/support artifact;
3. latent architecture and state-count selection are frozen prospectively or selected by training-only likelihood/complexity criteria;
4. transport is measured rather than fitting only within the same strata.

Only then does the question become:

> **What does the required latent state correspond to?**

## Interpretation firewall

This program does not by itself license:

- plaintext or language identification;
- absence of meaning;
- hoax/artificial-text claims;
- a cipher key or historical cipher identity;
- treating spaces as proven word boundaries;
- semantic interpretation of latent states;
- treating a non-reversible generator as decipherment.

## Relationship to existing work

- Issue #81 remains authority for X0-X3 and the `~0.059 bit/token` X2 predictive gain. Its soft-memory follow-up is Phase 0 here.
- Issue #24 becomes one candidate local-history family inside Phase 0 / Phase 2A, not the program-level destination.
- Issue #84 Phase D remains downstream and should be read as a source-attribution / transport question once a sufficient memory model exists.
- R1 remains a necessary emission-stage constraint rather than the principal discriminator.

## Stopping rule for the next research cycle

Do not branch into new semantic, post-hoc cipher-composition, or rich latent-state hypotheses unless a result from this program prospectively licenses that branch.

Implementation order:

1. Phase 0 — soft near-family / recency closure;
2. Phase 1 — predictive-information budget;
3. Phase 2 — source attribution;
4. Phase 3 — transport;
5. Phase 4 — boundary validity, movable earlier if required for construct validity.

The purpose of this order is to prevent an increasingly accurate Voynich-like surface generator from being mistaken for progress on the inverse / decipherment problem.