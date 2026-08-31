# Issue26E11D DEV3 — Voynich-blind robustness development battery

Status: **FROZEN BEFORE DEV3 EXECUTABLE — DEVELOPMENT DATA ONLY**

DEV2 identified excessive starting temperature as the dominant failure in E11C/DEV1: the frequency seed was exactly correct and `T0=.50` destroyed it, while `.020/.005/.001` preserved it. DEV3 asks whether conservative search also works when frequency initialization is deliberately imperfect.

This is the final development battery before any candidate solver freeze. It is not the locked validation defined in `PLAN_E11D.md`.

## Information firewall

DEV3 may access only:

- this repository branch;
- frozen CREMMA medieval Latin at `292525969ad98380b398e6606a9c2a36d51913ae`.

The workflow must assert absence of ZL3b, STA1 and `external/cipher-benchmark`.

No Voynich target data, E11C target mapping/output, target score, folio data, or locked E11D validation result may be loaded.

## Cipher dimensionality

Exactly the E11C dimensionality:

- 24 normalized Latin plaintext letters (`j→i`, `v→u`);
- 23 observed cipher symbols;
- exactly one plaintext letter unused;
- injective monoalphabetic mapping;
- character 4-gram objective from the frozen external Latin corpus.

## Six development cases

Use six known-key development ciphers, with deliberately different unused plaintext letters in this fixed order:

`q, x, z, y, k, w`

For each case:

1. retain normalized CREMMA runs over the other 23 letters;
2. take the first **40,000** retained characters in deterministic corpus order;
3. generate an independent random injective 23→24 key using seed `Issue26E11D:Dev3Key:v1:<unused>`;
4. encrypt the retained plaintext;
5. keep the true key only for post-optimization development diagnostics.

If any case has fewer than 40,000 retained characters, DEV3 must fail rather than silently lower the population.

These are development cases and do not use the locked validation seed namespace or its rotation/fold construction.

## Frozen candidate solvers

Every candidate starts from information available to a normal cryptanalyst: observed cipher unigram counts and frozen external-Latin unigram/4-gram statistics.

The 24-key representation includes an explicit unused-key position, so swaps may exchange an observed symbol's plaintext letter with the currently unused plaintext letter.

### Candidate A — `FREQ-HILL`

- frequency-ranked 24-position initialization;
- deterministic steepest pair-swap descent under the exact 4-gram objective;
- all `24 choose 2` swaps evaluated via the already-audited incremental delta kernel;
- stop when no improvement >`1e-12`.

### Candidate B — `T020`

- four deterministic starts:
  - exact frequency seed;
  - frequency seed with one deterministic random swap;
  - frequency seed with two deterministic random swaps;
  - frequency seed with three deterministic random swaps;
- 60,000 proposals/start;
- geometric `T0=.020` to `T1=.00005`;
- deterministic steepest pair-swap finalizer;
- seed namespace `Issue26E11D:Dev3:T020:<unused>:<start>`;
- choose lowest final training CE; ties lexicographic key.

### Candidate C — `T005`

Identical to B except `T0=.005` and seed namespace `Issue26E11D:Dev3:T005:<unused>:<start>`.

### Candidate D — `T001`

Identical except `T0=.001` and seed namespace `Issue26E11D:Dev3:T001:<unused>:<start>`.

No random-from-scratch starts are used because DEV2 showed that the relevant failure mode is destruction of a strong frequency initialization, not lack of exploration from arbitrary keys.

## Mandatory implementation audits

For every case/candidate:

- report direct full-score CE from an independent explicit 24-letter scorer;
- report shared/incremental solver CE;
- absolute discrepancy must be <=`1e-10`;
- report exact key accuracy and occurrence-weighted key accuracy.

## Development comparison

For each candidate aggregate across all six cases:

- mean and worst occurrence-weighted key accuracy;
- number of cases with weighted accuracy >=`.95`;
- mean and worst CE excess over true key;
- number of exact recovered keys.

A candidate is **development-robust** only if all six cases satisfy:

- occurrence-weighted key accuracy >=`.95`;
- recovered CE excess <=`.05 bits/char`.

If multiple candidates are development-robust, prefer in this fixed order:

1. `FREQ-HILL` (least stochastic freedom);
2. `T001`;
3. `T005`;
4. `T020`.

This preference is frozen before results and is not based on fit.

## Consequence

- If at least one candidate is development-robust, record the result and create a separate `E11D_SOLVER_FREEZE` document containing the preferred candidate's exact algorithm **before** any locked validation executable is created.
- If none is robust, validation remains unopened and a new development generation is required.

DEV3 cannot authorize a Voynich reveal. Only the subsequently frozen solver passing the one-time 12-cipher locked validation in `PLAN_E11D.md` can authorize E11E.
