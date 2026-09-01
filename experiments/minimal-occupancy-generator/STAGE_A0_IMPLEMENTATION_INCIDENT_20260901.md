# Issue #75 Phase A0 implementation incident — M1 deterministic solver

Date: 2026-09-01  
Status: **PRETARGET NUMERICAL IMPLEMENTATION INCIDENT; SCIENTIFIC DESIGN UNCHANGED**

## Failed run

- workflow: `Issue75 Phase A0 target-blind occupancy generator authority`
- run: `33500769086`
- head: `f0bba25a6fcebf660bcc0535b2113d058923127e`
- conclusion: `failure`

The run passed:

- plan-before-code chronology;
- exact ZL3b source authority;
- frozen dependency installation;
- Python compilation.

It failed during target-blind fitting/generation before any generated population was frozen.

## Exact failure

`phase75a_generator_support.py` raised:

`RuntimeError: M1 deterministic line search failed at iteration 6`

inside `_newton_fit_m1`.

The original implementation accepted a damped Newton update only when the floating-point convex objective was **strictly** smaller than the previous objective. Near the moment-matching solution, objective differences can fall below floating-point resolution even while a small residual moment error remains. This turns a numerical stopping/line-search detail into an unnecessary hard failure.

## Target firewall

This run remained fully pretarget.

The failed path occurs inside `fit_models(d)` before:

- any of the 124 scientific corpora are frozen;
- any pair Q is computed;
- any residual Z is computed;
- any Issue58C or Issue58D target vector is loaded;
- any model-to-target correlation, sign agreement, T statistic, positive-control calibration or Phase-A classification is computed.

No target outcome was available when diagnosing this failure.

## Licensed repair

The scientific M1 family remains exactly the preregistered model:

- empirical training-only `q_k=P(K=k)`;
- conditional distribution `P(x|K=k) ∝ exp(sum_s lambda_s x_s)`;
- `lambda_0=0`;
- 11 free slot main effects;
- no slot-pair interaction parameters;
- exact 4095-state expectation/covariance;
- deterministic zero initialization;
- frozen `1e-10` maximum marginal-error requirement.

The repair may change only the numerical Newton damping/acceptance rule so that it directly seeks reduction in the moment residual rather than requiring a strictly resolvable floating-point decrease in the convex objective.

Permitted implementation change:

1. compute the Newton direction from the same exact conditional covariance;
2. backtrack deterministically over powers of two;
3. accept the first step that reduces the maximum absolute 12-slot moment error;
4. keep the original objective as a diagnostic/secondary monotonicity check rather than the sole acceptance criterion;
5. retain the exact same convergence tolerance, state space, model, source data and parameterization.

No fit may be manually repaired, dropped or rerolled.

## Scientific commitments unchanged

This incident does not modify:

- `PLAN_A.md` scientific question;
- M0/M1/M+ family definitions;
- training/held-out folds;
- generator seed namespaces;
- 31 realizations per family/bank;
- 124-case complete population;
- target firewall;
- candidate-owned null construction;
- target vectors;
- positive-control calibration;
- ordered Phase-A decision rule.

A successful rerun must still satisfy the original maximum absolute marginal error `<=1e-10` for every M0/M1 fold fit before any target scorer is implemented or used.
