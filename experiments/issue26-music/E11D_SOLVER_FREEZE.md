# Issue26E11D_SOLVER_FREEZE — monoalphabetic substitution solver

Status: **FROZEN BEFORE LOCKED VALIDATION EXECUTABLE / REVEAL**

This document fixes the exact solver generation that will be applied to the one-time 12-cipher validation battery already preregistered in `PLAN_E11D.md`.

No locked validation output has been generated or inspected before this freeze.

## Selection basis

Voynich-blind development history:

- E11C / DEV1 failed because an excessively hot annealing start (`T0=.50`) destroyed strong frequency initialization.
- DEV2 independently verified the 24-letter score implementation and incremental swap delta, and showed `.020/.005/.001` preserve the known key while `.50` collapses.
- DEV3 tested six independent 23→24 substitutions with unused letters `q,x,z,y,k,w`. `FREQ-HILL`, `T001`, `T005`, and `T020` all achieved occurrence-weighted accuracy 1.0 and CE excess 0.0 in all six cases.
- `PLAN_E11D_DEV3.md` froze the preference order `FREQ-HILL > T001 > T005 > T020` if multiple candidates were development-robust.

Therefore the validation solver is **FREQ-HILL**.

## Frozen alphabet and language model

Plaintext alphabet, in exact index order:

`abcdefghiklmnopqrstuwxyz`

Properties:

- 24 letters;
- normalize `j→i`, `v→u`;
- exact frozen CREMMA corpus: `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- character 4-gram model;
- additive smoothing `alpha=0.1`;
- physical/external text run boundaries are not crossed.

## Frozen key representation

- 23 observed cipher-symbol positions indexed `0..22`;
- one explicit unused plaintext-letter position indexed `23`;
- the key is a permutation of all 24 plaintext-letter indices;
- positions `0..22` decode observed cipher symbols;
- position `23` stores the currently unused plaintext letter;
- swaps may involve position `23`, so the solver can change which plaintext letter is unused.

## Frozen initialization — frequency ranked

For each training population independently:

1. count occurrence frequency of the 23 observed cipher symbols;
2. rank symbols by descending count, tie by lower cipher-symbol index;
3. compute normalized plaintext-letter unigram frequencies from the frozen external CREMMA model population;
4. rank all 24 plaintext letters by descending external frequency, tie lexicographically;
5. map cipher rank 1..23 to plaintext rank 1..23;
6. place plaintext rank 24 in unused key position 23.

No random initialization, no true-key information, and no validation-specific tuning is permitted.

## Frozen optimization — deterministic steepest pair-swap descent

Starting from the frequency-ranked key:

1. evaluate all `24 choose 2 = 276` key-position swaps under the exact frozen 4-gram training objective;
2. evaluate CE change with the incremental swap-delta kernel audited in DEV2/DEV3;
3. choose the single swap with the greatest CE decrease;
4. accept only an improvement strictly greater than `1e-12`;
5. repeat until no eligible improving swap remains.

Tie behavior is deterministic:

- iterate `i=0..22`, `j=i+1..23`;
- update the best swap only on a strictly smaller delta;
- therefore the first lexicographic pair among exact ties is retained.

A safety cap of 100 accepted swaps is fixed; development required far fewer. If the cap is reached in validation, report it and use the capped key exactly; do not extend the search after reveal.

## Frozen scoring audits

For each validation fit:

- compute the final training CE through the incremental/shared implementation;
- independently recompute final CE with an explicit 24-letter full scorer;
- require absolute discrepancy <=`1e-10`;
- if this implementation audit fails, classification is `VALIDATION IMPLEMENTATION FAILURE`, not solver failure or success.

## Explicit exclusions

The locked validation solver uses **none** of:

- simulated annealing;
- stochastic restarts;
- random starts;
- perturbations;
- dictionary matching for key choice;
- Voynich data;
- synthetic true keys during optimization;
- post-validation retuning.

The true validation key is available only to the evaluation wrapper after fitting, solely to compute the preregistered recovery metrics.

## Validation authority

The validation population, seeds, rotations, folds, and pass/fail criteria remain exactly those frozen earlier in `PLAN_E11D.md`.

After the first validation output:

- this solver definition may not be modified and called the same E11D validation;
- if it fails, any new solver must be a newly preregistered generation;
- only `E11D SOLVER VALIDATED` may authorize a later separately preregistered E11E Voynich run.

Keep this research branch unmerged unless explicitly authorized.
