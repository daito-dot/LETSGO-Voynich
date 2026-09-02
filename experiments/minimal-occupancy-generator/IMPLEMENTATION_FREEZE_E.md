# Issue #75 Phase E — M5-KRS-2MIX-CHAIN implementation freeze

Date: 2026-09-01  
Status: **TARGET-BLIND IMPLEMENTATION FROZEN BEFORE E0 EXECUTION**

## Chronology

- permanent Phase-D first-reveal evidence commit: `b9b7dea91e914c89e3f35647f87b29a0391127cc`;
- Phase-D report commit: `f3bc276bb76305ddb632d4b21077242cc58115ea`;
- Phase-D latent-frontier decision commit: `446bcc57103b0801ed50844fa509167517fee971`;
- initial Phase-E plan commit: `f7606bf9d89ff259577cca04c33894d0241eede1` — superseded before executable;
- **final normative Phase-E plan commit:** `b2ef72d19111445f164d68ded813f1f81e297af6`;
- **first Phase-E executable commit:** `e6eb4fd32a7428a152b6370562f29eb453e4f049`;
- the executable's direct parent is the final plan commit;
- no Phase-E generated population and no Phase-E target result exist at this freeze.

## Frozen model

Family: `M5-KRS-2MIX-CHAIN`.

Generation mechanism:

1. exact training-only empirical `(K,R,S)` descriptor distribution;
2. one global binary hidden state `Z` with mixing probability `pi`;
3. each hidden component uses only the Phase-C 21-parameter local grammar: 11 unary + 10 nearest-neighbor terms conditioned on `(K,R,S)`.

Nominal continuous parameters per cross-fit split:

`43 = 21 + 21 + 1`.

Forbidden flexibility remains zero:

- explicit nonadjacent pair parameters: `0`;
- generic distance parameters: `0`;
- named distant-pair parameters: `0`;
- complete-signature-specific parameters: `0`.

## Frozen fitting contract

- exact 4095 non-empty state enumeration;
- exact aggregated training conditional likelihood;
- analytic gradient;
- finite-difference gradient audit before fitting;
- SciPy L-BFGS-B, no parameter bounds, no regularizer/prior;
- exactly 9 deterministic starts;
- start 0 is the exact nested M3 baseline;
- starts 1..8 use SHA-256-derived 21-D directions fixed by `PLAN_E.md`;
- start selection uses training conditional likelihood only;
- M5 selected training likelihood may not fall below the M3 baseline beyond `1e-8`;
- component labels canonicalized only after selection and distribution invariance is audited;
- no target quantity participates in fitting or selection.

## E0 contract

The next authorized execution is target-blind Stage E0 only:

- 31 reps `0..30`;
- 25,071 generated signatures each;
- frozen physical folds and parser unchanged;
- generation namespace `issue75:phaseE:M5-KRS-2MIX-CHAIN:rep{r}:fold{f}:generate`;
- exact occupancy SHA frozen for every rep;
- all fit/start diagnostics frozen;
- all target-access fields false;
- no Q/Z;
- no target correlation/sign/T;
- no drops;
- no rerolls.

If target-blind E0 exposes an implementation or numerical defect, repair is allowed only while the final plan, model family, 43-parameter structure, start set, optimizer settings, training objective, generation namespace, and target firewall remain unchanged. Every failed pretarget attempt must remain documented and non-authoritative.
