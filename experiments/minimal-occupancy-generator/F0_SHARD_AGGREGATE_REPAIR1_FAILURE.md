# Issue #75 Phase F0 — shard aggregate repair-1 failure

Date: 2026-09-02  
Status: **BASELINE-ONLY NUMERICAL AUDIT ABORT / NO F0 CLASSIFICATION**

Aggregate-only repair run:

- run `33550655259`
- execution head `c33cc588ccedf71eb29ace60f3eb3eace5c5befd`
- source scientific shards: exact ten artifacts from run `33548214504`
- no G2/G3 fitting was rerun
- no aggregate authority was uploaded or committed
- `stage-f0` was not created

The repair-1 reconciliation stopped on the redundant independently-refitted M5 baseline for outer fold 2:

- absolute training conditional log-likelihood difference: `1.0601914254948497e-05 nat` total;
- absolute held-out conditional log-likelihood difference: `0.0019000149659404997 nat` total;
- absolute held-out score difference: `3.4445521501780263e-07 nat/token`;
- absolute global-pi difference: `5.306937284066393e-08`.

The repair-1 held-out limits (`1e-3 nat` total and `1e-7 nat/token`) were therefore still tighter than independent hosted-runner optimizer reproducibility.

The observed held-out discrepancy is approximately 29,000 times smaller than the preregistered practical predictive-support threshold `0.01 nat/token`.

The reconciliation process aborted before invoking the model-selection aggregator. No G2/G3 five-fold support vectors or F0 classification were printed or accepted. Only these M5 baseline discrepancies may be used to define the next aggregate-only numerical audit.
