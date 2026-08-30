# Phase 62C — C0 + frozen A1 implementation freeze

Status: frozen before C0/A1 common-score outcomes are inspected.

This note resolves execution details for the Phase62C stage already specified in `PLAN.md`. It does not change the C0 transform family, A1 architecture, source panel, common S1–S3 scorecard, or sealed H62-P1.

## Scope firewall

Phase62C may compute only:

- C0-0…C0-4 training-fold selection and held-out evaluation;
- frozen Phase61C A1 re-generation/re-scoring under the Phase62 common S1–S3 scorecard;
- comparison with the already recorded N0 baseline.

Forbidden:

- C1 or any additional recoding;
- A2 or any A1 retuning;
- M0;
- computing or revealing H62-P1.

The executable must contain no H62-P1 implementation.

## Reuse of Phase62B definitions

`phase62c_c0_a1.py` imports the frozen Phase62B parser, graphematic representation, base/S1 eligibility rules, fixed-five 8D feature function, S1 contrast logic, S2 null, S3 eta2, and input verification.

This prevents Phase62C from silently redefining the common scorecard after seeing N0.

## C0 transforms — executable unit encoding

All transforms preserve token and physical-line boundaries and operate independently inside each token.

### C0-0 identity

Return the original graphematic-unit tuple unchanged. This also represents any one-to-one monoalphabetic rename, which is structurally equivalent on the generic scorecard.

### C0-1 token reversal

Reverse the graphematic-unit tuple.

### C0-2 two-class positional allography

Each source unit `g_i` becomes one encoded abstract unit:

- `A2:I:g_i` for `i=0`;
- `A2:N:g_i` otherwise.

The prefixes are structural tags, not additional units. Token length in encoded units therefore equals source token length.

### C0-3 three-class positional allography

Each source unit becomes:

- `A3:I:g_i` if `i=0` (including singleton tokens);
- `A3:F:g_i` if `i=len(token)-1` and token length >1;
- `A3:M:g_i` otherwise.

Again, each tagged source unit is one encoded unit.

### C0-4 non-overlapping digraph coding

Read from token start:

- each adjacent pair becomes one abstract encoded unit `D:<exact pair>`;
- an odd final source unit becomes one tagged singleton encoded unit `S:<unit>`.

The exact source unit strings are length-delimited inside the encoded-unit identifier so the representation is injective/reversible even if unusual Unicode units occur.

## C0 training target and selection

For each outer Voynich physical-leaf fold:

1. learn S1 feature SD and normalized direction from Voynich training paragraphs exactly as Phase62B;
2. compute **training** Voynich S1, S2 and S3 using the same scorecard;
3. transform all four primary medieval manuscripts independently under each C0 candidate;
4. compute each candidate's equal-manuscript S1, S2, S3;
5. selection loss is equal-weight mean squared relative error over S1–S3:

`mean(((candidate_k - train_target_k) / max(abs(train_target_k), 1e-9))^2)`;

6. choose the smallest loss; exact ties are broken by fixed order C0-0, C0-1, C0-2, C0-3, C0-4;
7. evaluate only the selected transform against the held-out Voynich fold.

No held-out statistic participates in transform choice.

## C0 explanatory-value decision

For each fold compute the held-out joint relative MSE of:

- N0 / C0-0;
- selected C0.

C0 counts as a material improvement over N0 only if **all three** are true:

1. selected C0 has lower held-out joint MSE than N0 in at least 3 of 5 Voynich folds;
2. mean held-out joint MSE across five folds is lower for selected C0 than N0;
3. for at least 3 of the 4 leave-one-manuscript-out conditions, the mean five-fold selected-C0 joint MSE is lower than the corresponding N0 joint MSE.

This fixes the meaning of “stable across a majority of folds / manuscript leave-one-out sensitivities” before the result.

Separately report whether selected C0's across-fold S1/S2/S3 ratios all fall in `[0.5,2.0]`; this broad-regime report cannot substitute for the improvement criterion above.

## Frozen A1 regeneration

Phase62C loads the exact Phase61C generator implementation from:

`../phase61/phase61c_joint_model.py`

It does not reimplement or modify the generator.

Frozen fold-specific Phase61C selected parameters:

- fold0: entry strength 0.5, local-family p 0.20;
- fold1: 0.5, 0.20;
- fold2: 0.5, 0.30;
- fold3: 0.5, 0.30;
- fold4: 0.5, 0.20.

For each fold:

1. verify that Phase61 and Phase62 physical-leaf test sets are identical;
2. learn Phase61 entry-shape scores from the same Voynich training leaves as the frozen generator;
3. regenerate five held-out A1 realizations using the exact Phase61C held-out seed formula;
4. convert generated string tokens to the Phase62 graphematic token representation without altering token/line/paragraph layout;
5. score every realization under the **Phase62** S1–S3 definitions;
6. average S1, S2 and S3 over the five realizations.

No A1 parameter is selected or changed in Phase62C.

## A1 broad-regime decision

Across folds, calculate the ratio of mean A1 score to mean held-out Voynich score for S1, S2, S3.

Frozen A1 common-score gate:

- A1 remains materially competitive on exposed Phase62 structure only if every defined ratio lies in `[0.5,2.0]`.

Failure is recorded without repair.

## A1 target-dependence record

Regardless of score, report explicitly:

- empirical Voynich token vocabulary supplied: yes;
- Phase61C input vocabulary size: 8,295 types;
- explicit boundary-aware entry mechanism: yes;
- explicit local-family mechanism: yes;
- maximum local generator memory: 10 tokens;
- meaningful plaintext candidate: none.

These costs are not converted into a post-hoc scalar penalty in Phase62C.

## N0 reference

Phase62C recomputes the identity/N0 candidate under the exact same executable path used for C0 so operational differences cannot explain apparent improvement. The committed Phase62B result remains the scientific N0 authority; a compatibility check compares the recomputed held-out N0 S1–S3 means with `phase62b_n0_results.json` and aborts the Phase62C verdict if relative discrepancy exceeds:

- S1: 1e-6;
- S2: 1e-6;
- S3: 1e-6.

## Phase62C output

Report:

- selected C0 transform per fold and training loss;
- every candidate's training S1–S3 and loss;
- held-out N0 and selected-C0 S1–S3, ratios, joint MSE;
- C0 fold-improvement count and leave-one-manuscript-out stability;
- frozen A1 held-out S1–S3 and ratios;
- broad-regime status for C0 and A1;
- complexity/dependence record.

Do not declare the final N/C/G structural ranking inside the implementation. Phase62D owns that decision and must be committed before prospective H62-P1 reveal.