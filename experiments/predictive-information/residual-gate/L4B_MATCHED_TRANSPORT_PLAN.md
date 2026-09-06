# Issue #130 — L4b support-matched Currier edge-table transport

Date: 2026-09-06
Status: **FROZEN BEFORE MATCHED PREDICTIVE REVEAL**
Parent: Issue #127

## Entry authority

The merged score-free Gate0 froze five outcome-blind source-event selections with exact previous-terminal context matching:

- Gate JSON SHA-256 `a0f48878506369aa9dff60e06b60be13d41d36dd1ceef3a40c4fc63825db66f5`;
- parent Issue #127 Gate0 SHA-256 `31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`;
- 20 shared previous-terminal classes;
- 8,728 selected visible source edge events per Currier regime per seed;
- exact A/B count equality separately for every retained previous-terminal class;
- five deterministic outcome-blind hash selections.

Only after this Gate is merged may current-initial outcomes be attached to the frozen selected loci.

## Question

Issue #127 first reveal found target-calibrated source-table transport `B→A ONLY`, but source support was strongly imbalanced (A 8,967 vs B 19,049 visible edge events).

L4b asks:

> **Does that directional table-transport asymmetry survive after source conditional-table estimation support is prospectively matched context by context?**

## Frozen populations and model

Reuse exactly:

- frozen ZL3b source;
- corrected source order;
- Phase 3A Currier A/B authority and `f57v -> B` fallback;
- original five physical-leaf folds;
- fixed `k=2`, additive `alpha=.01`;
- target-local POS2 factors from Issue #127;
- parser-accepted line-body current tokens as predictive scoring support;
- target-POS2 pooled line-body first-symbol fallback for source-unseen terminal contexts;
- rho grid `0.00,0.01,...,1.00`, ties to smaller rho.

No source POS2 emission/onset factor is imported into target.

## Reconstructing frozen matched source tables

For each Gate seed and source Currier regime:

1. rebuild the score-free event loci and reapply the exact Gate hash selection;
2. require the selected event-identity digest to equal the merged Gate digest;
3. only then attach each selected locus's current-initial raw-byte outcome from the frozen source corpus;
4. train `P(current_initial | previous_terminal)` using only those selected events;
5. fixed additive smoothing is `.01` over byte vocabulary size 257.

No sample selection may depend on current-initial outcome.

## Predictive comparison

Repeat only the already-authorized Issue #127 `SOURCE_TABLE_TARGET_RHO` comparison.

For each seed `r`, direction `S -> T`, and untouched target outer fold `f`:

- matched source conditional table = fixed for that seed/source regime;
- target POS2 factors are trained on target leaves outside outer fold `f`;
- source-table rho is selected using target inner folds `g != f` only:
  - target POS2 factors for inner `g` are trained outside `f,g`;
  - the same matched source table is used;
  - pool accepted line-body target likelihood over the four inner folds;
  - choose rho by maximum pooled likelihood, ties smaller rho;
- score target outer fold `f` once.

Primary fold gain:

`G_matched = bits(POS2_T) - bits(MATCHED_SOURCE_TABLE_TARGET_RHO)`.

No source-only rho and no exact source-strength transfer are part of L4b; those questions were already separated in Issue #127.

## Seed-level and overall stability

For each seed and direction:

- `seed_mean = mean(G_matched over 5 target outer folds)`;
- `seed_positive_folds = count(G_matched > 0)`;
- seed PASS iff `seed_mean > 0` and positive in at least `4/5` folds.

For each direction overall:

- `seed_passes = count(PASS seeds)`;
- `grand_mean = mean(all 25 seed × target-fold G_matched values)`;
- direction PASS iff `seed_passes >= 4/5` **and** `grand_mean > 0`.

No effect-size threshold, confidence interval gate or equivalence margin may be added after reveal.

## Frozen classification

`MATCHED_TABLE_TRANSPORT` is:

- `BIDIRECTIONAL` — A→B and B→A overall PASS;
- `A→B ONLY` — A→B passes, B→A fails;
- `B→A ONLY` — B→A passes, A→B fails;
- `NONE` — neither passes.

No other post-reveal class may be added.

## Frozen interpretation

- `B→A ONLY` persists: support imbalance does not explain the directional asymmetry; regime-specific conditional mapping becomes substantially more credible.
- `BIDIRECTIONAL`: original A→B failure was primarily compatible with source-table estimation support; shared cross-regime mapping is more plausible after matching.
- `A→B ONLY`: direction reverses under support control; first-reveal asymmetry was unstable and cannot support a regime-specific direction claim.
- `NONE`: the apparent B→A table transfer was not robust to support matching; universal literal table remains unsupported.

These are predictive mechanism statements only.

## Required diagnostics

Report without altering the class:

- matched-table selection digest and selected count for every seed/source;
- source previous-terminal context count and observed terminal→initial pair count after outcome attachment;
- target outer accepted support and source-context fallback rate;
- target-inner selected rho by seed/direction/outer fold;
- POS2 and matched mixed bits/token;
- all 25 gains per direction;
- seed-level means/positive folds/pass;
- grand mean, seed-pass count and overall direction pass.

## Firewall

L4b must not:

- change Gate-selected source events after outcome attachment;
- use current-initial outcomes in sampling/ranking;
- use target outer-fold tokens for rho selection;
- import source POS2 emission/onset factors into target;
- tune alpha, k, rho grid, fallback or classification after reveal;
- fit latent states;
- condition on writing hand, domain or semantics;
- score Issue #84 targets;
- infer plaintext, language, cipher family, author, hoax status or historical production mechanism.
