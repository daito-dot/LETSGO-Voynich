# Research roadmap

Last consolidated: 2026-09-01

This file controls current sequencing. Exact historical methods and results remain controlled by phase/issue-specific frozen plans and reports.

## Program objective

The project is not optimizing for the number of falsified hypotheses. The objective is to move from reproducible Voynich structure toward a constrained generative/transform account that can eventually be inverted and tested on unseen material.

For the current token-construction lane, read `research/TOKEN_CONSTRUCTION_PROGRAM.md` before interpreting the statistical milestones below.

## Completed milestones relevant to the current frontier

- **M1–M5:** paragraph-entry/local-recurrence mechanism program established A1/A1-R1 as the leading tested structural mechanism, with prospective H62 support, training-vocabulary robustness and independent-reading replication.
- **M6:** inventory-autonomy stress test was mixed; full autonomy failed on canonical ZL S3 while H62 remained strong.
- **M7:** published Naibbe provided a stronger C-family comparator but remained partial and did not rival A1 on sealed recurrence geometry.
- **M8:** localized content-anchor feasibility was established; Phase66–68 object-local morphology↔text tests were negative under frozen representations.
- **M9:** Phase69/70 demonstrated compatibility between strong local recurrence and exactly recoverable meaningful plaintext; recurrence alone cannot imply semantic absence.
- **M10:** Phase71 Alberti paragraph-boundary signal/reset failed in the opposite S1 direction.
- **M11:** Issue #26 bounded direct-music program closed with no supported tested direct-musical interpretation.
- **M12:** Issue #55A found cross-leaf slot3×slot5 dependence; Issue #55B reduced it to binary occupancy exclusion.
- **M13 / #58A:** all 66 binary slot pairs were audited. The selected slot3×slot5 edge is real but ranks 22/66; 22 edges survive global maxT with all five folds positive. Frozen classification: `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`.
- **M14 / #58B:** complete signed graph stability was tested across source-grounded Currier/section/line-position strata. Observed graph correlations and transfers were high, but the line-local marginal-preserving null generated similarly high whole-graph correlations. Frozen classifications: `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE` and `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`.
- **Decipherment threshold:** not reached.

## Current scientific object

The current lane concerns **space-delimited token internal construction**, not whole-sentence grammar.

Visible spaces are treated only as observed delimiters; they are not assumed to be proven linguistic word boundaries.

The 12-slot representation shows strong occupancy constraints. The open question is now whether a **non-trivial residual interaction system**, after removing lower-order occupancy prevalence, is shared across the manuscript.

## Active frontier — null-residual token-construction graph

#58B exposed a limitation of raw graph comparison: complete 66-edge correlation remains near `0.95` even in line-local null populations that destroy same-token cross-slot pairings while retaining line×slot marginal occupancy.

Therefore the next phase must not ask the same raw-similarity question again.

### Primary next question

> After estimating and removing each edge's expected association under the frozen line-local occupancy null, does a graph-level residual interaction signal exist? If it exists, is the signed residual pattern stable across the already frozen Currier/section/position strata?

### Required plan-first design

Before any new target reveal, freeze at least:

1. the exact residual representation for all 66 edges;
2. the null-reference estimator for edge-wise expected Q and scale;
3. an independent null-test ensemble so the same simulations are not used both to define and validate residuals;
4. a graph-level **residual-existence gate**;
5. residual cross-stratum similarity/transfer statistics that are interpreted only if existence survives;
6. family-wise correction across all predeclared graph-level tests;
7. five physical-leaf folds or a justified prospectively frozen replacement;
8. the same external Currier/section/position contrasts unless a new source audit independently justifies a change;
9. parser `min` primary and `max` non-promoting sensitivity unless changed prospectively for a representation-specific reason;
10. exact stop rules preventing edge selection or threshold tuning after reveal.

### Preferred null separation

A strong design is to use deterministic split null ensembles, for example:

- **1,000 reference nulls:** estimate each stratum×edge null expectation and robust scale;
- **1,000 test nulls:** independently generate the null distribution of residual graph existence and residual transfer statistics using the reference parameters only.

The exact counts and robust-scale rule must be frozen before target scoring. The principle — independent estimation versus validation — is mandatory unless a stronger non-circular construction is preregistered.

### Decision branches

#### Residual graph exists and transfers across strata

- promote a manuscript-wide token-internal construction mechanism as a strong surface constraint;
- then prioritize representation/transcription invariance;
- use only the stable residual constraints prospectively to restrict reversible generative/inverse models.

#### Residual graph exists but materially changes across strata

- move to a hierarchical or multiple-generator token-construction model;
- do not force one manuscript-wide inverse transform.

#### No residual graph survives

- downgrade the current 66-edge graph from “deep grammar candidate” to a lower-order occupancy architecture under this representation;
- do not keep mining individual #58A/#58B edges;
- move to a different independently motivated structural representation or inverse constraint.

#### Residual result is inconclusive

- record power/representation limits;
- do not rescue the result by selecting top edges, changing strata or loosening thresholds.

## Why this frontier matters to decipherment

This lane answers a prerequisite to inversion:

> **Are we trying to invert one token-generation mechanism across the manuscript, or multiple/hierarchical mechanisms?**

Passing the residual-stability test would not decipher the manuscript, but it would provide a substantially stronger and less prevalence-driven generative constraint for later reversible-transform work.

## Parallel source lane — real historical ciphertext

The Phase72 source-development branch is not accepted current science and should not be merged wholesale into main.

Before any historical-cipher S1 comparison:

1. fix source authority and availability;
2. fix genuine message/document boundaries externally;
3. freeze preprocessing and exact comparison statistic;
4. only then authorize Voynich comparison.

Do not substitute physical page starts for message starts after seeing metadata.

## Deferred lanes

### Reversible surface-transform grammar

Reversible/inverse work remains first-class, but the token-construction component should now be constrained by the outcome of the residual-existence/stability phase rather than by raw #58A edge strengths.

Do not assign functions or meanings to slots before a stable residual structure is established.

### Content

Phase66–68 morphology-correlated object-local work is stopped for the current populations/representations. Reopen only with a materially new independently grounded content variable.

### Direct music

Issue #26 remains closed. Reopen music-specific interpretation only with a genuinely new independently fixed historical/manuscript-local constraint before target scoring.

### A1 extension

Do not add A2 merely to repair known S1/S3/profile residuals. New mechanism terms require independent motivation and a new frozen test.

## Repository-maintenance rules

Before starting new science:

1. current `main` is the descriptive source of truth;
2. check current PRs/issues/branches;
3. permanently archive completed first reveals before relying on expiring Actions artifacts;
4. ensure `research/STATUS.md`, `ROADMAP.md`, `RESUME.md`, `research/NEXT_RESEARCH_FRONTIER.md` and `research/TOKEN_CONSTRUCTION_PROGRAM.md` agree on the object and frontier;
5. preserve negative/inconclusive results and raw-result hashes;
6. never relabel a post-reveal redesign as the same confirmatory hypothesis;
7. close completed research issues only after authoritative integration reaches main.