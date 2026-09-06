# Issue #104 / Issue #88 Phase 3A — Currier A/B transport contract

Date: 2026-09-06
Status: **FROZEN BEFORE PHASE-3A PREDICTIVE TRANSPORT SCORING**
Entry authority: `GATE0_PROVENANCE.md`

This file mirrors the already-frozen Issue #104 transport design in executable terms. It does not add model families or decision rules.

## Population

- Currier A/B labels are exactly the Gate-0 authority, including the one prereveal `f57v -> B` missing-`$L` fallback.
- UNKNOWN/OTHER documents are excluded.
- Gate 0 found no mixed A/B numeric physical leaves.
- The original five physical-leaf folds remain fixed.
- Corrected raw-source causal order is mandatory.

## Frozen mechanism family

Primary mechanism-only transport uses target-stratum emission/support:

1. `T_V2`: V2 fitted on target-stratum training leaves only.
2. `T_LOCAL(pi)`: exact edit-1 local mechanism with `H=40`, `tau=32`; only scalar `pi` varies.
3. `T_CORE(pi,alpha)`: LOCAL plus order-free `PREV_PARAS` edit-1 inventory; only scalar `alpha` varies.

`pi, alpha in {0.00,0.01,...,0.30}`. Exact ties choose the smaller value.

No H/tau/window, edit relation, paragraph pool, fold or grid may change after reveal.

## Source-transferred parameters

For each source stratum S in {A,B}:

- select one `pi_S` by summed 5-fold held-out literal-surface likelihood within S only;
- fix `pi_S`, then select one `alpha_S` by summed 5-fold held-out likelihood within S only.

No target-stratum token enters source parameter selection.

## Target oracle comparator

For each target outer fold f:

- select `pi_T,f` only from the other four target-stratum folds using nested inner validation;
- fix that pi, then select `alpha_T,f` from the same target-only inner-validation system;
- fit target V2/edit-1 support on target training leaves excluding f;
- score target fold f.

The target oracle is a comparator only. It does not select source-transferred parameters.

## Primary mechanism-only scores

For S -> T and each target outer fold:

- `T_V2`
- `T_LOCAL(source pi)`
- `T_CORE(source pi, source alpha)`
- `T_LOCAL(target-oracle pi)`
- `T_CORE(target-oracle pi, target-oracle alpha)`

Primary gains:

- `G_local_transfer = bits(T_V2) - bits(T_LOCAL(source pi))`
- `G_prev_transfer = bits(T_LOCAL(source pi)) - bits(T_CORE(source pi,source alpha))`
- `G_core_transfer = bits(T_V2) - bits(T_CORE(source params))`

Oracle penalties:

- `penalty_local = bits(T_LOCAL(source pi)) - bits(T_LOCAL(target oracle pi))`
- `penalty_core = bits(T_CORE(source params)) - bits(T_CORE(target oracle params))`

A directional component passes iff mean gain > 0 and it is positive in >=4/5 target outer folds.

Each component is classified separately as:

- `BIDIRECTIONAL TRANSPORT`
- `A->B ONLY`
- `B->A ONLY`
- `NO BIDIRECTIONAL TRANSPORT`
- `SUPPORT / FOLD INVALID`

No equivalence threshold is invented for oracle penalties; continuous values are reported.

## Secondary full-support diagnostic

Attempt a strict source-trained model with source V2, source exact-token vocabulary/edit-1 index and source `pi/alpha` scored on each target fold.

Report:

- finite code length if available;
- exact-token OOV fraction relative to source training vocabulary;
- local and PREV_PARAS context-availability rates if scoring is valid;
- degradation versus the mechanism-only target-support model.

If source emission/support yields non-comparable or non-finite literal probability, record `FULL-SUPPORT INCONCLUSIVE`. This diagnostic cannot overturn the primary mechanism-only classification.

## Firewall

- prediction-only literal-surface code length;
- corrected source order;
- no S1/S2/H62/R1 or Issue #84 target;
- no page imagery/plaintext/semantics;
- no hand/section/scribe conditioning;
- no latent state;
- no future target token;
- no post-reveal model/grid/pool expansion.