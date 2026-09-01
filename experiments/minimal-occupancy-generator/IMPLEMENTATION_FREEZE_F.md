# Issue #75 Phase F — generator implementation freeze

Date: 2026-09-02  
Status: **FROZEN BEFORE F1 TARGET-BLIND GENERATION / NO PHASE-F TARGET RESULT**

## Chronology

Training-only architecture decision:

- F0 authority commit `fd1446d474208b9e2f17e3fd4df5249e133c2bd3`
- F0 authority SHA-256 `999d9990449875708019ad71aa3a1d253afad19edada88cb45eb4204349887c6`
- selected family `M6-KRS-GATED-2MIX-CHAIN`

Phase-F normative plan:

- commit `eb4ee10d9874d2aace564a7f6a8464ccd4a677fc`
- file `experiments/minimal-occupancy-generator/PLAN_F.md`

First Phase-F executable:

- commit `e8fc51c54e8617943ebd1685e950a0ba74758ed1`
- file `experiments/minimal-occupancy-generator/phase75f_generator_support.py`
- Git blob SHA-1 `33a7b688bea07c8524a33d20348eb2eae4429ca1`

The Phase-F executable was committed after the complete plan.

## Frozen implementation behavior

The executable performs **no Phase-F fitting**.

For each of the five outer physical folds it:

1. verifies the exact frozen F0 authority SHA;
2. reconstructs the unchanged ZL3b source occupancy dataset and physical folds;
3. reconstructs outer-training K/R/S empirical `q(d)`;
4. verifies training-derived K/R/S standardization against the F0 frozen means/SDs/active coordinates;
5. reads the exact frozen G2 component vectors and geometry-gate coefficients from F0;
6. evaluates both local-chain components with the already-frozen Phase-F0 stable normalization policy;
7. builds the full 4095-state probability

   `q(d) * [(1-g(d))*p0(x|d) + g(d)*p1(x|d)]`;

8. audits full normalization and descriptor-mass reconstruction;
9. uses the frozen Phase-F sampling namespace to generate exactly reps `0..30`.

The generator contains:

- two latent local-chain components;
- 46 frozen free continuous parameters/fold inherited from F0;
- zero Phase-F optimizer starts because no refit occurs;
- zero explicit nonadjacent parameters;
- zero generic-distance parameters;
- zero named distant-pair parameters;
- zero signature-specific parameters.

## Frozen sampling namespace

`issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{r}:fold{f}:generate`

The 31 generated occupancy SHA identities produced by the first complete F1 execution become the pretarget candidate authority. They may not be dropped, rerolled, or regenerated under a different namespace after target access.

## Target firewall

This executable imports no target R1 scorer/reference loader and records all target-access fields false.

Before target access the F1 workflow must additionally verify:

- plan-before-code chronology;
- exact F0 authority SHA;
- exact source blob;
- exact 31-case population;
- unique occupancy SHA for all 31 reps;
- no drops/rerolls;
- all target-access flags false.
