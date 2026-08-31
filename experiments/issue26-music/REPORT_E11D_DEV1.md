# Issue26E11D — solver development pass 1

Status: **DEVELOPMENT FAILED — VALIDATION NOT OPENED — NO VOYNICH INFERENCE**

E11C's mandatory synthetic positive control failed, so E11D isolates substitution-solver engineering from all Voynich target data. This report records the first stronger development attempt; it is not a scientific Voynich result.

## Development configuration

Branch: `issue26-music-e11d-solver-validation`.

Executable: `phaseE11d_solver_dev.py`.

Frozen external source available to this job:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae` only.

The workflow explicitly asserted that no ZL3b/STA/cipher-benchmark target input was present.

Solver:

- 24 normalized Latin letters (`j→i`, `v→u`);
- 23 cipher symbols plus one unused plaintext letter;
- character 4-gram likelihood;
- 12 starts per fold: 1 frequency, 7 frequency-perturbed, 4 random;
- 100,000 annealing swaps per start;
- `T0=.50`, `T1=.00010`;
- final deterministic steepest pair-swap descent.

## Provenance

- executable/workflow head: `ee3578ede5586e466565de179a39171c294bd5f6`
- Actions run `33382967604`
- job `99459224546`
- artifact `9754635822`
- raw JSON SHA-256 `4865f4d76bd9b0cbb06e38a8be1e469fb4506cdbb5c60fbfb5393dc5f1fd83ed`
- artifact ZIP SHA-256 `148087f3927e9617872a2081a3015587482f549c79b49fcaad62457feeb6239d`.

## Result

Development gate: **FAIL**.

Across five folds:

- true-key mean held CE: **2.8305081643 bits/char**
- recovered-key mean held CE: **4.5931609451 bits/char**
- mean occurrence-weighted key accuracy: **0.0419383**.

Per-fold weighted accuracies:

- fold0 `.03398`
- fold1 `.03398`
- fold2 `.03398`
- fold3 `.03398`
- fold4 `.07376`.

The recovered objective is nearly identical across folds and remains far from the known true key. Increasing the original E11C annealing budget therefore did not solve the synthetic substitution.

## Interpretation

This does **not** weaken or support the León/Voynich hypothesis. The solver has still not demonstrated basic competence on a known plaintext-generated substitution.

The near-constant recovered CE around `4.593` is sufficiently suspicious that the next step is implementation/search diagnosis rather than a blind increase in restarts.

Potential causes to distinguish on synthetic data only:

1. frequency initialization is already informative but annealing destroys it;
2. frequency initialization itself is poor on the chosen retained-run population;
3. the incremental swap objective disagrees with direct full scoring;
4. the 24-letter wrapper/shared compiled kernels have an implementation mismatch;
5. the search landscape requires a different substitution-solving strategy.

## Next development step

Before any locked validation is opened, compare on the same known synthetic cipher:

- raw frequency seed;
- deterministic steepest pair-swap descent from that seed;
- existing annealing result;
- direct full-score recomputation after every diagnostic stage;
- exact and occurrence-weighted key accuracy, available only because this is development data.

No Voynich input/output may be used for this diagnosis.
