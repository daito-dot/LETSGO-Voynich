# Issue #75 Phase A preflight replay incident — floating fit metadata

Date: 2026-09-01  
Status: **PRETARGET REPLAY-GATE IMPLEMENTATION INCIDENT; SCIENTIFIC DESIGN UNCHANGED**

## Failed preflight

- workflow run: `33501362053`
- head: `7cf4c779acfcc90f180cf1e4fce02352737e3091`
- scientific mode: `--verify-only`

The preflight never computed pair Q, residual Z, or any target comparison.

## Failure

Several boundary cases failed in `build_exact_case` at:

`RuntimeError: deterministic M0/M1 fit no longer matches Stage A0 authority`

The scorer compared the entire serialized M0/M1 fit object from a new GitHub runner to the Stage A0 fit object using Python exact equality. That serialized object includes floating-point Newton parameters and model marginals.

Different GitHub hosted runners/regions can produce last-bit floating-point differences in linear algebra while satisfying the same moment equations far inside the frozen scientific tolerance. One boundary runner happened to match exactly; others did not. This gate therefore tested accidental hardware-level floating serialization identity rather than the preregistered scientific model.

## Correct authority hierarchy

For Phase A, the scientifically relevant replay gates are:

1. exact source/transcription and parser/fold population;
2. exact training empirical statistics (slot marginals and M1 `q_k`);
3. the frozen fit criterion: maximum absolute slot-marginal error `<=1e-10`;
4. exact model code/family/seed namespace;
5. most importantly, exact final generated occupancy-corpus SHA against Stage A0.

The Stage A0 fit achieved maximum marginal error `1.2705114738054135e-14`.

Literal bitwise equality of intermediate floating `lambda` values was never part of `PLAN_A.md` and is not a scientific requirement.

## Licensed repair

The scorer replay gate may be changed only as follows:

- require exact equality of empirical training target marginals and M1 `q_k` with Stage A0;
- require every regenerated M0/M1 fold fit to satisfy the original `<=1e-10` moment error;
- do not require bitwise equality of fitted floating `lambda` or model-marginal last bits across runners;
- continue to require **exact occupancy SHA equality** for the requested generated corpus before any pair Q, residual Z or target load.

If exact generated occupancy SHA fails after this repair, stop again. Do not loosen the corpus SHA, change a seed, reroll, or replace a case.

## Target firewall

The failed preflight used `--verify-only` and exited before:

- candidate pair-Q computation;
- candidate residual-Z computation;
- Issue58C target load;
- Issue58D target load;
- target correlation/sign calculation;
- T computation;
- positive-control calibration;
- Phase-A classification.

No target outcome was observed when making this repair.
