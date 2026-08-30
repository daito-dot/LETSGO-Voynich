# Phase 62C — C0 + frozen A1 common-score result

Status: **complete**.

This report interprets the exact result in `phase62c_c0_a1_results.json` under the frozen `PLAN.md` / `IMPLEMENTATION_C.md` rules and the later reproducibility constraints recorded in `research/AUDIT_PHASE51_61C_20260830.md`.

H62-P1 was not computed or revealed in Phase62C.

## Reproducibility / authority

The original Phase62C GitHub Actions run used the frozen implementation from PR #7 and produced artifact:

- workflow run: `33313019008`
- artifact: `9732584331`
- artifact ZIP SHA-256: `fe555431c6472b26663a23c842a0c37f70963ca524d7c1759cec6e2799fc4594`

After the independent Phase51–61C audit was merged to `main`, PR #7 was merged without modifying its frozen scientific implementation. Current-main dependency identity was then checked by Git blob SHA:

- `experiments/phase62/phase62b_n0.py`: `e0ada366845c7a6c5a5dd75de91fe262b72a94b6` both at Phase62C execution ancestry and current main;
- `experiments/phase61/phase61c_joint_model.py`: `4213e87b7cf519372a84694fe297dcb3f14e0d66` both before and after audit integration;
- `experiments/phase62/phase62c_c0_a1.py`: `de6eb1b829ef43fcc23cb3ba85d3640a2e9b7c87` at the frozen Phase62C head and current main.

The container available during final recording could not reach GitHub directly, so a fresh local clone/re-run was not possible there. This does not substitute for replay. The recorded result is instead tied to the exact successful Actions artifact plus immutable code/input identities. The executable also recomputed Phase62B N0 internally and matched it exactly on S1/S2/S3 (`relative_discrepancy = 0`), passing the predeclared compatibility gate.

Pinned external inputs remain:

- ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`;
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`.

## Primary result

Across five Voynich physical-leaf folds:

| family | S1 | S2 | S3 | ratio to Voynich S1 | ratio S2 | ratio S3 |
|---|---:|---:|---:|---:|---:|---:|
| Voynich | 0.87599 | 0.04388 | 0.02827 | 1.000 | 1.000 | 1.000 |
| N0 | -0.85872 | 0.00585 | 0.02797 | -0.980 | 0.133 | 0.989 |
| selected C0 | -0.81672 | 0.01095 | 0.02421 | **-0.932** | **0.249** | **0.856** |
| frozen A1 | 0.54597 | 0.06634 | 0.01661 | **0.623** | **1.512** | **0.587** |

The frozen broad-regime interval is `[0.5, 2.0]` where the ratio is positive/defined.

- N0: S1 fail, S2 fail, S3 pass.
- C0: S1 fail, S2 fail, S3 pass.
- A1: S1 pass, S2 pass, S3 pass on the preregistered **ratio-of-means** rule.

## C0 — bounded reversible recoding

Every outer fold selected the same training-optimal transform:

> **C0-4: non-overlapping digraph coding**

This is notable because selection was performed from training Voynich targets only and the result was identical in all five folds.

Mean held-out joint relative MSE:

- N0: **3.03877**
- C0: **2.88836**

C0 improves N0 held-out joint MSE in **5/5 folds**.

Leave-one-manuscript-out fold-improvement counts:

- omit BIS193: 1/5;
- omit CLM13027: 5/5;
- omit Mazarine915: 5/5;
- omit UBL758: 4/5.

Thus 3/4 manuscript-omission conditions show majority fold improvement. C0 therefore satisfies the frozen criterion for **material explanatory improvement over N0**.

### C0 interpretation

Supported:

> A simple reversible boundary-blind recoding can move meaningful structured medieval text measurably toward the exposed Voynich joint scorecard.

Not supported:

> The tested low-complexity recoding family is sufficient for Voynich structure.

The best C0 still has:

- S1 opposite in sign to Voynich (`-0.932×`);
- S2 only about one quarter of Voynich (`0.249×`).

Therefore simple global reversible recoding receives real but limited explanatory credit. Any stronger cipher/shorthand proposal is a new **C1** model with additional complexity; it cannot be treated as a hidden repair to C0.

## Frozen A1 — common-score evaluation

A1 was not retuned for Phase62. The exact Phase61C fold-specific parameters and deterministic held-out seed scheme were reused.

Across-fold A1/Voynich ratios:

- S1 entry projection: **0.623**;
- S2 locality excess: **1.512**;
- S3 aggregate generic line-position eta2 mean: **0.587**.

All pass the frozen common-score broad-regime rule.

A1 held-out joint relative MSE by fold:

- fold0: 0.2091
- fold1: 0.2736
- fold2: 1.1925
- fold3: 0.4101
- fold4: 0.2650

Mean: approximately **0.4701**.

### Important heterogeneity

The Phase62C gate was explicitly the ratio of across-fold means, not “all three targets pass in every fold.” A1 does not satisfy that stronger unstated rule. Examples include:

- fold0: S1 ratio 0.476, S3 0.444;
- fold1: S1 0.349, S3 0.398;
- fold2: S1 2.764;
- fold3: S2 2.108;
- fold4: S3 0.364.

This heterogeneity must remain visible in later ranking and replication.

### Audit constraint on A1

The independent Phase61C audit remains binding. The aggregate eta2 pass does **not** mean that A1 reproduces the full multivariate line-position profile. In the post-hoc 11-coordinate decomposition, near-family eta2 coordinates are overproduced by about 6× while the aggregate excluding those coordinates is about 0.64× Voynich.

Therefore retain only:

> Frozen A1 remains materially competitive on the preregistered exposed Phase62 scalar S1–S3 scorecard without retuning.

Do not strengthen this to:

> A1 reproduces the full Voynich line-position grammar/profile.

## Complexity / target dependence

The exposed fit cannot be interpreted without the frozen dependence ledger.

### N0

- Voynich boundary mechanisms: 0
- Voynich-selected parameters: 0
- target vocabulary: no
- meaningful plaintext: yes

### C0

- Voynich boundary mechanisms: 0
- searched alternatives: 5
- Voynich-derived symbol/codebook: no
- reversible to meaningful source text: yes

### A1

- explicit Voynich paragraph-entry mechanism: 1
- explicit local-family mechanism: 1
- local memory: 10 tokens
- Phase61C parameters selected against Voynich training folds
- empirical Voynich token vocabulary supplied: yes, 8,295 types
- meaningful plaintext candidate: none

The Phase61C training-vocabulary-only audit showed that held-out-only token leakage does not drive A1's first-gate survival, but A1 still has substantially greater target dependence and mechanism cost than N0/C0.

## Phase62C decision

1. **N0 remains not jointly competitive** on the exposed common scorecard.
2. **C0 materially improves N0**, establishing limited explanatory value for simple boundary-blind reversible recoding, but C0 still fails the crucial S1/S2 broad-regime targets.
3. **Frozen A1 remains the strongest exposed scalar structural fit** among the tested N0/C0/A1 candidates.
4. This does **not** yet make G/A1 the overall mechanism-family winner because A1 carries higher target dependence, profile mismatch, fold heterogeneity and no semantic/historical grounding.
5. **H62-P1 remains sealed.** Phase62D must first freeze the exposed-score structural ranking / unresolved-set interpretation in a separate commit.

No A2, C1 or M0 is introduced here.