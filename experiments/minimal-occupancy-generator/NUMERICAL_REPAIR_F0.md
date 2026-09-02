# Issue #75 Phase F0 — normalization-only numerical repair

Date: 2026-09-02  
Status: **FROZEN AFTER ATTEMPT-1 NUMERICAL ABORT / BEFORE COMPLETE F0 RESULT**

Attempt 1 (`33543350071`) produced no accepted F0 authority, no artifact, and no `stage-f0` evidence. Its only usable information is the mechanical exception recorded in `F0_EXECUTION_ATTEMPT1_FAILURE.md`.

## Repair scope

The mathematical conditional component distribution remains

`p(x | d, theta) = exp(F(x) theta) / sum_{x' in d} exp(F(x') theta)`.

For each K/R/S descriptor class, the repaired evaluation performs:

1. stable `logsumexp` of class logits;
2. `logp = logits - logsumexp(logits)`;
3. `p = exp(logp)`;
4. compute floating-point `s = sum(p)`;
5. explicitly renormalize `p <- p/s` and `logp <- logp-log(s)`;
6. use the renormalized `p` for exact feature expectations and the adjusted `logp` for likelihoods.

This removes only the inherited Phase-E `abs(sum(p)-1) <= 1e-12` abort during optimizer exploration. It does not clip probabilities, parameters, logits, gradients, responsibilities, or mixture weights.

## Invariants that may not change

The repair does not change:

- the 4095-state occupancy space;
- K/R/S classes;
- the five physical folds;
- the M5 baseline family or its frozen Phase-E fitting implementation;
- G2 architecture or 46-parameter count;
- G3 architecture or 65-parameter count;
- any deterministic start vector or perturbation amplitude;
- L-BFGS-B settings;
- the `1e-8` mixture-weight floor;
- the `0.01 nat/token` predictive-support threshold;
- the all-five-positive-fold requirement;
- the G2-vs-G3 parsimony/displacement rule;
- source transcription, parser, or token population;
- any topology-reference access rule.

The Phase-E M5 refit continues to call the original frozen Phase-E helper. The stabilized evaluator is used only by the new F0 G2/G3 objective and held-out likelihood code.

## Acceptance

The next complete F0 execution must still pass:

- the previously frozen analytic-gradient finite-difference audits;
- exact nested start-0 likelihood equality to M5 within `1e-7`;
- all start/population/weight checks;
- the exact frozen predictive-selection law.

If the repaired execution still fails mechanically, no partial fold values may be promoted into model selection.
