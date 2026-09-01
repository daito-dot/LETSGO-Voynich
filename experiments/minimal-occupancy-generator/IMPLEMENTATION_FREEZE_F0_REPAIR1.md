# Issue #75 Phase F0 — repair-1 implementation freeze

Date: 2026-09-02  
Status: **FROZEN BEFORE COMPLETE REPAIRED F0 EXECUTION**

Attempt 1 aborted numerically and produced no authority. The permitted repair was frozen in `NUMERICAL_REPAIR_F0.md` before repair code.

Repair authority:

- failure record commit `16d8faf70a322cd567450e22e7be93ffedd2130f`
- numerical-repair plan commit `021b8420dcefe06ddbba9f6c0f101ab18310806b`
- stable runner commit `2874f57a201fd36f8289e5375551a240ef5f02d4`
- stable runner Git blob SHA-1 `865a9363533741f84b5c764a123124a6675ada43`

The original F0 scientific executable remains byte-for-byte frozen at commit `201a4d3a1ff4ef374f1ab3b0c2f8adf7f886e394` / blob `c1b9e8620c121124137d88f4dad233b6aa2f2834`.

The wrapper changes only the numerical implementation of the new F0 G2/G3 component normalization. It does not patch the frozen Phase-E module itself: `real_egen.fit_m5` continues to resolve its own original Phase-E module globals. Only lookups made by the imported F0 G2/G3 code through `f0.egen.component_logprob_and_mu` are redirected to the stable equivalent evaluator.

The repaired evaluator performs log-sum-exp normalization followed by explicit floating-point renormalization and corresponding log-probability adjustment. No clipping, bounds, model term, start, fold, threshold, or selection-rule change is introduced.

The repaired complete run must pass the same finite-difference gradient audits and exact nested M5 start checks before any result is accepted.
