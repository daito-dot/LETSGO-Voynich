# Next research frontier — Issue #55C occupancy-graph specificity

Status: current frontier after Issue #55B integration.

## Why the frontier moves here

Issue #55A established a cross-leaf slot3×slot5 dependence. Issue #55B showed that the signal is almost entirely the binary fact that the two slots are not occupied together:

- full gain `0.0441774454 bits/token`;
- binary occupancy gain `0.0442150445`;
- subtype residual `-0.00003747`;
- residual-null p `0.26973`.

The result is therefore a morphotactic exclusion, not a rich 5×5 paired-state code.

The next question is specificity. slot3×slot5 was selected through the failed E10 Sloane path, so simply retesting the same pair would not provide an unseen confirmation.

## Primary next question

> Relative to the complete 12-slot occupancy graph, is the previously selected slot3×slot5 exclusion unusually strong, unusually transferable across physical leaves, or otherwise structurally distinctive?

## Required design

Before scoring:

1. freeze binary occupancy for all 12 parser slots;
2. define the full set of slot pairs and the same cross-leaf predictive statistic for every pair;
3. freeze a null preserving line-local slot occupancy rates and relevant token structure;
4. account explicitly for the previous selection of slot3×slot5;
5. freeze the exceptional-pair criterion and multiplicity correction;
6. predeclare register/Currier/token-position stratification or interaction tests;
7. report the full pairwise matrix, including negative and redundant relations.

Independent-transcription replication should be added only if the relevant slot states can be defined without choosing a mapping from the target outcome.

## What each outcome means

### Selected pair remains exceptional

Retain a specific slot3↔slot5 incompatibility and test whether it behaves like an alternative-construction constraint in a reversible surface grammar.

### Many pairs have comparable exclusion

Promote the object of study from one pair to the complete slot-occupancy grammar. The E10/#55 pair then becomes one example rather than a privileged code candidate.

### Pair is subset-specific

Narrow the claim to the relevant register/Currier/position domain. Do not describe it as manuscript-wide.

### Pair fails independent representation

Treat the effect as representation-specific until a more invariant construction is identified.

## Prohibited shortcuts

Do not:

- assign semantic meanings to `t/k/p/f` or `cth/ckh/cph/cfh` from the exclusion alone;
- return to Sloane/music interpretation without new external evidence;
- optimize which slot pairs to report after seeing the complete matrix;
- infer a cipher table from binary mutual exclusion;
- add an invertible-transform interpretation before structural specificity is established.

## Parallel external-source work

Real historical ciphertext controls remain useful, but the current source-development work has not yet supplied externally established message-entry boundaries sufficient for a fair S1 comparison. That lane remains source-only until the population and boundary semantics are fixed before Voynich scoring.
