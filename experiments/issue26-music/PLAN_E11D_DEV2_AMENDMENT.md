# Issue26E11D DEV2 pre-execution amendment

Status: **FROZEN BEFORE DEV2 WORKFLOW / RESULT**

After writing the first DEV2 executable but before creating or running its workflow, code review found that the shared Numba `anneal_one` captures module-global `T0` at lazy compilation. Calling that single compiled kernel repeatedly after mutating `base.T0` would therefore not guarantee four genuinely different temperature trajectories in one process.

This is an implementation issue discovered before any DEV2 output existed.

Amendment:

- keep every DEV2 population, seed namespace, stage, metric and interpretation rule unchanged;
- keep the shared E11 kernel for the explicit incremental-delta audit and shared-full-score cross-check;
- for the four requested temperature trajectories, use a DEV2-local Numba implementation of the **same swap-delta / anneal / steepest-finalizer algorithm** with literal alphabet size 24 and `t0` passed as a function argument;
- `STEPS=100000`, `T1=.00005`, temperatures `.50/.020/.005/.001` remain unchanged;
- report direct full-score CE after each trajectory.

No validation data or Voynich data has been accessed. This amendment changes only how the already-frozen temperature comparison is implemented faithfully.
