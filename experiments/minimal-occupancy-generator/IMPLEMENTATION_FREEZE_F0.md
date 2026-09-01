# Issue #75 Phase F0 — implementation freeze

Date: 2026-09-02  
Status: **FROZEN BEFORE FIRST F0 EXECUTION**

## Chronology

Normative F0 plan:

- commit `dc780cbe985e424dc3953003d05e682b8a492694`
- file `experiments/minimal-occupancy-generator/PLAN_F0_TRAINING_LATENT_DIAGNOSTIC.md`

Implementation clarification:

- commit `431ff0e328d1c3cd065bba53fa4438780490fa92`
- file `experiments/minimal-occupancy-generator/IMPLEMENTATION_CLARIFICATION_F0.md`

First F0 executable:

- commit `201a4d3a1ff4ef374f1ab3b0c2f8adf7f886e394`
- file `experiments/minimal-occupancy-generator/phase75f0_training_latent_diagnostic.py`
- Git blob SHA-1 `c1b9e8620c121124137d88f4dad233b6aa2f2834`

The executable was committed only after both F0 normative documents.

## Frozen implementation properties

The executable:

- reuses the exact frozen 12-slot state space, parser, five physical folds, and Phase-E M5 fitting implementation;
- refits M5 independently on each outer training population;
- fits G2 and G3 only to the same outer training population;
- evaluates model selection only by exact held-out conditional occupancy log likelihood `log P(x|K,R,S)`;
- does not generate Monte Carlo corpora for F0;
- does not compute pair-Q, residual-Z, a 66-edge correlation, sign agreement, or a topology score;
- has no explicit nonadjacent, generic-distance, named distant-pair, or signature-specific parameter in G2/G3;
- uses exactly nine frozen deterministic starts for each richer family/fold;
- contains an analytic-vs-central-finite-difference gradient audit for both new objective functions on outer fold 0;
- checks exact nested likelihood equality at start 0 against the refitted M5 baseline;
- forbids rerolls and random restarts;
- applies the preregistered five-fold predictive-support and architecture-selection rules mechanically after all held-out likelihoods are available.

## Frozen numerical policies

- exact enumeration over all 4095 non-empty 12-slot states;
- analytic-gradient L-BFGS-B;
- maximum 2000 iterations;
- `ftol=1e-12`;
- `gtol=1e-8`;
- `maxls=50`;
- numerical convergence accepted on optimizer success or final gradient infinity norm `<=1e-6`;
- finite-difference gradient-audit tolerance `2e-5` under max absolute/scaled error;
- start likelihood tie tolerance `1e-10`;
- nested-distribution numerical tolerance `1e-7`;
- every G2 descriptor gate probability and every G3 global mixture weight must remain strictly above the frozen `1e-8` floor (and below `1-1e-8` for the binary G2 gate).

## Frozen support law

A richer family is supported over M5 only when:

- all five held-out fold gains are positive; and
- median gain is at least `0.01 nat/token`.

If both G2 and G3 satisfy that rule, G2 remains preferred unless G3 beats G2 in at least four of five held-out folds and has median direct gain at least `0.01 nat/token`.

No implementation or threshold change is authorized after the first F0 execution based on its result.
