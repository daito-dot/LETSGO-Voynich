# Issue #26E11D — León-style monoalphabetic solver calibration and locked validation

Status: **FROZEN BEFORE E11D EXECUTABLE / VALIDATION REVEAL**

Parent: `issue26-music-e11-leon-substitution` at exact-spec E11C head `a643c273fe08da116a24f21954cf1d507e73c729`.

## Why E11D exists

E11C's historically relevant question cannot yet be answered because its mandatory known-cipher positive control failed even after the frozen 24-letter Latin alphabet specification was restored.

Exact-spec E11C replay:

- true-key synthetic held-out CE: `2.8305081643 bits/char`;
- recovered-key held-out CE: `4.5930139959`;
- mean occurrence-weighted key accuracy: `0.03398`;
- positive control: **FAIL**.

Therefore E11C is `SOLVER INADEQUATE`, not a Voynich negative.

E11D is strictly **solver engineering outside the Voynich target**. It must establish that a monoalphabetic solver can recover known ciphers of the exact E11C dimensionality before any further Voynich decoding is permitted.

## Hard isolation from Voynich

E11D's executable/workflow must not download, parse, score, or inspect:

- ZL3b;
- STA1;
- any Voynich transcription;
- any E11C Voynich mapping/output;
- any folio-specific data.

The only scientific input is the same frozen external medieval-Latin CREMMA corpus:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- frozen normalization `j→i`, `v→u`;
- frozen 24-letter alphabet from E11C.

## Cipher dimensionality

Match the exact E11C search problem:

- plaintext alphabet size: 24;
- observed cipher symbols: 23;
- one plaintext letter is unused by each synthetic cipher;
- mapping is injective from 23 cipher symbols into 24 plaintext letters;
- no homophones, nulls, transposition, spaces, or polyalphabetic changes.

## Development control

The already-revealed failing E11C positive-control construction is explicitly a **development control** in E11D. Solver design may be improved using its known true key and score because this contains no Voynich information.

Development target construction:

1. load frozen normalized CREMMA;
2. select the 23 most frequent plaintext letters;
3. retain only runs over those 23 letters until approximately the E11C event count (`140,423` letters);
4. apply deterministic secret permutation seed namespace `Issue26E11C:PositiveKey:v1`;
5. use five deterministic run-index folds.

The solver should reach on this known development cipher:

- mean occurrence-weighted key accuracy >= `.95`;
- mean recovered held-out CE within `.05 bits/char` of the true-key held-out CE.

Failure on development is not a scientific reveal; solver parameters may be changed on E11D **before validation is opened**.

## Locked validation population

Validation is prospectively frozen now and must not be used to tune solver parameters after its first output.

Create exactly **12 independent validation ciphers**, `v00..v11`.

For each validation cipher:

1. rotate the CREMMA runs deterministically by validation index before taking the target event budget, so validation plaintext samples are not identical to the development sample;
2. choose the unused plaintext letter independently as the least frequent letter after a deterministic alphabet rotation by index;
3. generate an independent random injective key using seed `Issue26E11D:ValidationKey:v1:<index>`;
4. make five deterministic run-index folds after an index-specific cyclic fold offset;
5. fit on 4/5 and score untouched 1/5.

The solver never receives the true key. The evaluation wrapper retains it only to compute recovery metrics after fitting.

## Solver-v2 design freedom before validation reveal

The solver may use only information available to a normal cryptanalyst:

- cipher unigram frequencies;
- the frozen external Latin 4-gram language model;
- the known dimensions 23→24;
- deterministic random seeds.

It may use:

- frequency-ranked initialization;
- perturbed frequency starts;
- random starts;
- simulated annealing / hill climbing;
- deterministic steepest pair-swap descent;
- multiple restarts and temperature schedules.

It may **not** use synthetic true keys except for reporting development/validation recovery after optimization.

## Solver freeze rule

The first commit tagged/documented as `E11D_SOLVER_FREEZE` must contain exact:

- algorithm;
- restart population;
- seeds;
- temperature schedule(s);
- steps per restart;
- tie-breaking;
- scoring model.

After that freeze, the 12 validation results may be emitted once. No solver modification may be called E11D validation after seeing those results.

If validation fails, a new E11D2/E11D-next solver generation must be explicitly preregistered rather than silently retuning the failed validation.

## Validation pass criteria

E11D solver is **validated** only if all of the following hold on first locked validation reveal:

1. at least **11/12** validation ciphers have mean occurrence-weighted key accuracy >= `.95`;
2. at least **11/12** have mean recovered held-out CE within `.05 bits/char` of true-key held-out CE;
3. median validation occurrence-weighted key accuracy >= `.98`;
4. worst validation recovered-minus-true held-out CE <= `.15 bits/char`;
5. no validation cipher has mean occurrence-weighted key accuracy < `.85`.

Frozen classification:

- all pass: **`E11D SOLVER VALIDATED`**;
- otherwise: **`E11D SOLVER NOT VALIDATED`**.

## Consequence for Voynich

Only `E11D SOLVER VALIDATED` authorizes a later **new preregistered E11E** run that applies the frozen solver unchanged to the frozen STA-family Voynich population.

E11D itself must never emit a Voynich plaintext or Voynich score.

## Audit boundary

The failed E11C outputs, including isolated Latin-looking fragments, remain uninterpretable while the positive control fails. Solver calibration must not use them, choose parameters based on them, or optimize for their appearance.

Keep E11D on its own research branch. Do not merge to `main` without explicit user authorization.
