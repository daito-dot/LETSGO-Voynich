# Issue26E11D DEV2 — synthetic substitution solver diagnosis

Status: **FROZEN BEFORE DEV2 EXECUTABLE — DEVELOPMENT DATA ONLY**

This is solver engineering after `REPORT_E11D_DEV1.md`. It is not the locked E11D validation and must not access Voynich data.

## Purpose

DEV1 increased the search budget but still recovered a known 23-symbol→24-letter substitution at only ~4.2% occurrence-weighted accuracy, with recovered CE near 4.593 bits/char versus true-key CE 2.831.

DEV2 distinguishes whether the failure comes from:

- poor frequency initialization;
- the stochastic annealing trajectory;
- the incremental swap-delta implementation;
- or a more fundamental objective/search problem.

## Information firewall

The job may access only:

- this repository branch;
- frozen CREMMA medieval Latin at `292525969ad98380b398e6606a9c2a36d51913ae`.

It must assert absence of ZL3b, STA1 and `external/cipher-benchmark` before execution.

No Voynich target data, E11C Voynich mapping, Voynich plaintext sample or Voynich score may be loaded or inspected.

## Diagnostic population

Normalize Latin exactly as E11D:

- 24 letters;
- `j→i`, `v→u`;
- same four CREMMA directories.

Take the 23 most frequent normalized Latin letters and retain same-alphabet runs. Use the first **70,000 retained characters** in deterministic corpus order. This is a development diagnostic size, not a future validation population.

Generate one known substitution using seed:

`Issue26E11D:Dev2KnownKey:v1`

The 23 observed cipher symbols map injectively to the 23 retained plaintext letters; the 24th plaintext letter is unused.

## Frozen diagnostics

Build the same additive-smoothed character 4-gram model from the full frozen CREMMA population.

Report the known true-key score and the following candidate stages.

### A. Frequency seed

Rank cipher symbols by occurrence frequency and normalized Latin letters by corpus frequency. Map ranks deterministically; the least-ranked Latin letter occupies the unused key position.

Report:

- full 4-gram CE;
- exact key accuracy across 23 observed symbols;
- occurrence-weighted key accuracy.

### B. Full-score steepest descent

Starting from the frequency seed, repeatedly test all `24 choose 2 = 276` key-position swaps by **direct full-score recomputation**, not the incremental delta kernel. Apply the single best improving swap; ties lexicographically. Stop when no improvement exceeds `1e-12` or after 100 accepted swaps.

Report CE/accuracy and accepted-swap count.

### C. Incremental-delta audit

At the original frequency seed, generate 200 deterministic candidate swaps with seed:

`Issue26E11D:Dev2DeltaAudit:v1`

For each, compare:

- CE change returned by the existing incremental `swap_delta` kernel;
- CE change from direct full-score recomputation after the same swap.

Report maximum and mean absolute discrepancy. A maximum discrepancy > `1e-10` is an implementation failure.

### D. Existing annealing behavior

From the exact same frequency seed run one deterministic trajectory for each `T0`:

- `.50` — DEV1 regime;
- `.020`;
- `.005`;
- `.001`.

Keep `T1=.00005`, 100,000 proposals and deterministic seed namespace `Issue26E11D:Dev2Anneal:v1:<T0>`.

After each anneal, use the existing deterministic steepest-swap finalizer and report direct full-score CE and key accuracy.

## Interpretation

This diagnostic may be used to choose the next development solver because the hidden key is intentionally known.

- If frequency seed is already high-accuracy and annealing degrades it, reduce/remove high-temperature randomization.
- If full-score steepest improves substantially while incremental annealing does not, investigate the incremental path.
- If incremental delta disagrees with direct scoring, fix implementation before any further tuning.
- If all local methods remain poor, move to a structurally different monoalphabetic-substitution solver.

No E11D locked validation data may be generated or opened from this experiment. No result from DEV2 permits a Voynich reveal.
