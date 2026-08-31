# Phase 67A coverage / observability control freeze

Status: **FROZEN BEFORE IMAGE ANNOTATION AND PRIMARY ASSOCIATION REVEAL**

The main plan already requires a missingness/observability control. This note fixes the exact residualization procedure implemented in `run_phase67a.py` before any Phase67 image state table exists.

For each morphology character separately:

1. use the same blocks and same within-folio centering as the primary RV statistic;
2. let `Xc` be the centered Hellinger morphology-state vector and `Cc` the centered scalar non-`U` coverage fraction;
3. regress every column of `Xc` on `Cc` with no intercept (the intercept is already removed by within-folio centering):
   `beta = (Cc^T Cc)^-1 Cc^T Xc` when `Cc^T Cc > 0`;
4. define `Xres = Xc - Cc beta`; if coverage has zero centered variance, use `Xres = Xc`;
5. compute the same normalized RV between `Xres` and centered paragraph text;
6. repeat this for every within-folio paragraph permutation;
7. form a second three-character family statistic `T_res = max(RV_res,c)` and its exact maxT p-value over all 2,304 assignments.

Decision rule is frozen as follows:

- if the primary global maxT test is positive and its winning character's coverage-only p-value is > 0.05, classify as `DETECTED` if the ordinary coverage gate passes;
- if the primary winner's coverage-only p-value is <= 0.05, require the coverage-residualized global maxT test to pass `p <= 0.05` and its winning character to pass the same coverage gate; then classify as `DETECTED AFTER COVERAGE RESIDUALIZATION`;
- otherwise classify the apparent primary result as `MORPHOLOGY / OBSERVABILITY CONFOUNDED`;
- a primary p-value <= 0.05 with failed ordinary coverage gate remains `UNDERPOWERED / COVERAGE-LIMITED`.

This control is not allowed to change the image states, paragraph population, n-gram representation, folio strata, or primary statistic.