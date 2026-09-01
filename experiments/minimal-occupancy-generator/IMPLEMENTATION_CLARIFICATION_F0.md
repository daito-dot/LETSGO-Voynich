# Issue #75 Phase F0 — implementation clarifications

Date: 2026-09-02  
Status: **FROZEN BEFORE FIRST F0 EXECUTABLE**

This note resolves implementation-level ambiguities in `PLAN_F0_TRAINING_LATENT_DIAGNOSTIC.md` without changing its scientific question, candidate families, parameter counts, support threshold, or architecture-selection rule.

## K/R/S standardization

For G2, descriptor coordinates are standardized separately inside each outer training population using token-weighted population moments:

- mean = arithmetic mean over outer-training tokens;
- standard deviation = population standard deviation (`ddof=0`) over outer-training tokens.

A coordinate with exactly zero standard deviation is represented by standardized value zero for every descriptor and its corresponding gate slope is initialized and kept at zero because its objective gradient is identically zero.

Held-out tokens never contribute to these means or standard deviations.

## Deterministic SHA directions

All F0 perturbation directions are produced by the same deterministic construction family used in Phase E: for each coordinate, take the first eight bytes of SHA-256 of a frozen namespace string, map the resulting unsigned integer to `(-0.5,0.5)`, and L2-normalize the vector.

Frozen namespaces:

- G2 component start `k=1..8`: `issue75:phaseF0:G2:component:init{k}:coord{j}`;
- G2 gate-slope start `k=1..8`: `issue75:phaseF0:G2:gate:init{k}:coord{j}`;
- G3 split start `k=1..8`: `issue75:phaseF0:G3:split:init{k}:coord{j}`.

No random-number generator is used.

## G2 start construction

Let the outer-training fitted M5 parameters be `(theta0, theta1, pi)` after the frozen Phase-E canonicalization.

- start 0: `(theta0, theta1, logit(pi), 0, 0, 0)`;
- starts 1..8: component parameters `(theta0 + 0.10*v_k, theta1 - 0.10*v_k)` and gate slopes `0.05*g_k`, with gate intercept remaining `logit(pi)`.

Any inactive zero-variance gate coordinate has slope exactly zero.

## G3 start construction

Let M5 weights be `(w0,w1)=(1-pi,pi)`.

- start 0 duplicates component 0 exactly: components `(theta0, theta1, theta0)` and weights `(w0/2, w1, w0/2)`;
- starts 1..4 split component 0 symmetrically by `±0.08*v_k`, preserving weights `(w0/2, w1, w0/2)`;
- starts 5..8 split component 1 symmetrically by `±0.08*v_k`, using components `(theta0, theta1+0.08*v_k, theta1-0.08*v_k)` and weights `(w0, w1/2, w1/2)`.

The three global weights are represented by two logits relative to component 0. Start 0 is therefore an exact distributional representation of the fitted M5 baseline.

## Optimization validity

Use analytic-gradient L-BFGS-B with the same numerical policy as frozen Phase E:

- `maxiter=2000`;
- `ftol=1e-12`;
- `gtol=1e-8`;
- `maxls=50`;
- a result is numerically converged when the optimizer reports success or final gradient infinity norm is `<=1e-6`;
- all values must be finite.

For G2, every gate probability over the complete frozen K/R/S descriptor support must satisfy `1e-8 < p < 1-1e-8`.

For G3, all three global mixture weights must exceed `1e-8`.

No invalid start is replaced or rerolled. Selection among valid starts remains outer-training conditional likelihood only, with the preregistered `1e-10` tie rule.

## Held-out score

Held-out score is the exact sum of `log P(x | K,R,S)` over every token in the physical leaf held out by the outer fold, divided by the held-out token count. The empirical descriptor probability `q(K,R,S)` is deliberately excluded because it is common to the candidate conditional generators and is not the mechanism under discrimination.

A held-out K/R/S class need not have occurred in the outer training population: the component exponential families define a normalized conditional distribution on every state in every frozen K/R/S class, and the G2 gate is defined from training-only standardization for the complete descriptor support.
