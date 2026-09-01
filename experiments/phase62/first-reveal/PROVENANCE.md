# Phase62C exact first-reveal provenance repair

Status: **PERMANENT EXACT FIRST-REVEAL ARCHIVE**

This archive was recovered during Issue #68 Stage 0, before any Issue #68 target candidate score existed.

## Original scientific execution

- workflow: `Phase62 C0+A1 pre-H62 evaluation`
- workflow run: `33313019008`
- job: `99261341362`
- branch head recorded by the original run: `899cfa1833d1d6d2faf53c8e3f9bdc92474dc148`
- PR merge checkout tree used by the run: `0f5f54d7d5f9f93e0413845fc9086067d3aa275d`
- source ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`

## Original Actions artifact

- artifact name: `phase62c-c0-a1-results`
- artifact ID: `9732584331`
- artifact ZIP SHA-256: `fe555431c6472b26663a23c842a0c37f70963ca524d7c1759cec6e2799fc4594`
- exact raw JSON SHA-256: `1bd44579b7a57d43ea52ddf9d5bf59acb936b3f6fe7b7346010685c50f10bfb2`
- permanent raw file: `phase62c_c0_a1_results_run33313019008.json`

## Difference from the later committed Phase62C result file

The repository file `experiments/phase62/phase62c_c0_a1_results.json` is **not byte- or semantic-identical** to the original first-reveal artifact. Its raw SHA-256 at this audit was:

`0518ffcebf4666c5b6a142054696c0bf092ee86428ef8282aba6537691eccbb4`

Exactly three numeric fields differ, all in the same non-primary leave-one-manuscript-out sensitivity cell:

`folds[2].C0_leave_one_manuscript_out.Mazarine915`

| field | exact first reveal | later committed record |
|---|---:|---:|
| `C0.S1` | -0.9238719297180421 | -0.8830522744522888 |
| `C0_joint_relative_mse` | 10.371319531604906 | 9.044530390532254 |
| `N0_joint_relative_mse` | 11.695085537263099 | 10.659921954292841 |

The Issue #68 provenance audit found:

- numeric difference count: `3`
- nonnumeric difference count: `0`
- primary scientific field mismatches: `[]`

In particular, the original first reveal and later committed record agree on all protected primary fields, including:

- source compatibility and frozen inputs;
- Voynich/N0/C0/A1 across-fold means;
- C0/A1 ratios to Voynich;
- selected C0 transform in every fold (`C0-4_digraph`);
- held-out C0 improvement count;
- LOMO fold-improvement counts (`1 / 5 / 5 / 4`);
- number of LOMO conditions with majority improvement (`3`);
- frozen C0 material-improvement decision;
- frozen A1 common-score competitiveness decision;
- Phase62C decision block.

Therefore this is a **first-reveal provenance/reproducibility defect, not a change in the accepted Phase62C scientific conclusion**.

## Later verification during Issue #68 Stage 0

- artifact-authority audit run: `33454247454`
- audit job: `99690680088`
- audit artifact ID: `9780853020`
- audit artifact ZIP SHA-256: `4de7e2bbc4efce90a4130f2e7a1150cba948850f913f3c08edb825739aebde3f`

The original first-reveal raw file is now the authority whenever an exact Phase62C first-reveal value is required. The later committed result file is retained as historical repository state and must not be silently presented as the exact first reveal.
