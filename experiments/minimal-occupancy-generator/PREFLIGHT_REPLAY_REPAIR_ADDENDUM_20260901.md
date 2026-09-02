# Issue #75 Phase A — preflight replay-gate repair addendum

Date: 2026-09-01  
Status: **PRETARGET IMPLEMENTATION REPAIR FROZEN; SCIENTIFIC DESIGN UNCHANGED**

The target-blind preflight run `33501362053` exposed a replay-gate implementation error documented in `PREFLIGHT_REPLAY_INCIDENT_20260901.md`.

The scorer repair is frozen at:

- scorer original add/freeze commit: `21e7bbc176e593ef9fa025113fb17799ca500d8e`
- replay incident commit: `cae1873d824e0e4c5e99cd3068c5cfed5a787438`
- replay-gate repair commit: `11cbcab12e9c02e5002bc286a132b9a8a9f267aa`

The repaired scorer retains the exact original scientific scorer after the replay gate. The only change is how the regenerated M0/M1 fit is authorized before exact corpus SHA comparison.

The repaired gate now requires:

1. exact frozen source/parser/fold population;
2. exact training empirical target marginals for every M0/M1 cross-fit fold;
3. exact training empirical `q_k` for every M1 cross-fit fold;
4. regenerated and frozen fit errors each `<= 1e-10`;
5. exact family/rep generation code and seed namespaces;
6. **exact final generated occupancy SHA** matching the Stage A0 case authority.

It no longer requires bit-for-bit equality of intermediate floating Newton `lambda` values or last-bit model-marginal serialization across GitHub hosted runners.

This is an authority correction, not a relaxation of the scientific corpus identity. Exact generated-corpus SHA remains mandatory before any pair Q, residual Z or target load.

At this addendum point no Issue #75 target score has been computed. The failed preflight used `--verify-only`; all target-access fields remained false.

The next licensed action is a rerun of the same eight target-blind preflight boundary cases. Any exact occupancy-SHA mismatch must stop the phase again; it may not be repaired by changing a seed, rerolling, replacing a case, or loosening corpus identity.
