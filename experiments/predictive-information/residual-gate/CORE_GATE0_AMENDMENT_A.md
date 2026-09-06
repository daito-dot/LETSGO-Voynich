# Issue #118 corrected-core Gate 0 — Amendment A

Date: 2026-09-06
Status: **FROZEN BEFORE ANY ISSUE #118 RESIDUAL MIXTURE SCORING**
Parent: Issue #118 / Issue #88

## Why this amendment exists

The original Gate 0 plan required the corrected Phase-1 authority JSON to reproduce byte-for-byte with SHA-256

`0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`.

The first Gate run (`34025442893`) never reached scientific reproduction because the new Gate workflow omitted the pre-existing `scipy` runtime dependency. No corrected authority JSON and no Issue #118 residual score were produced.

After repairing only that CI dependency, run `34025606759` completed the full corrected Phase-1 calculation. All printed scientific quantities matched the frozen authority, but the final whole-file SHA check failed. Because the workflow stopped before its later assertions/artifact step, a diagnostic-only amendment was then added. No `p_mix`, `G_any`, `G_context`, or other Issue #118 residual statistic existed at any point.

Diagnostic run `34025800793` archived the regenerated JSON and passed every explicit scientific-field assertion before intentionally retaining the original whole-file SHA gate.

## Exact old-vs-new JSON diff

Original authority artifact:

- run `34019919131`
- artifact `9985167291`
- original JSON SHA-256 `0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`.

Diagnostic regeneration:

- run `34025800793`
- artifact `9987037790`
- regenerated JSON SHA-256 `37fabb0856f9d27ee0c8860cf65ceb143ae91510b4c714d3af6d73bf93f5b7fd`.

A recursive typed JSON comparison found **exactly one differing scalar in the entire 715,312-byte JSON**:

`recency_selection.3.candidate_table[88].total_log_likelihood`

- original: `-131278.47048215955`
- regenerated: `-131278.47048215958`
- absolute difference: `2.9103830456733704e-11`.

The row identity is fixed and unchanged:

- outer fold `3`
- `H=40`
- `tau=64`
- `pi=.26`.

This is a **non-selected** B1 candidate. The selected fold-3 B1 candidate remains `H=40, tau=32, pi=.21` with log-likelihood `-131234.59121955265`; the discrepant row is approximately `43.87926` log-likelihood units worse. The discrepancy cannot alter the frozen selection.

There were **zero** non-float differences and zero other float differences. Classification, folds, fold hash, order authority, grids, all selections, B0–B4 output values, support counts, decision inputs, regression flags, firewalls, and interpretation-boundary fields were byte/value identical.

A repository compare from the original scientific head `fab8c77c32b35bddbe490d246feaba8500495578` to the pre-Gate current main showed no modifications to the corrected Phase-1 scorer or its imported Phase0 / Issue81 / SlotParser calculation code. The original and diagnostic workflows both use the same unpinned `numpy scipy` runtime family. The observed one-ULP-scale reduction difference is therefore treated as execution-level floating-point nondeterminism, not a model or authority change.

## Frozen narrow normalization rule

Gate 0 may now normalize **only** this exact scalar before checking the original full-JSON SHA.

Mechanical rule:

1. regenerate the corrected Phase-1 JSON normally;
2. require the row at `recency_selection.3.candidate_table[88]` to have exactly `H=40`, `tau=64`, `pi=.26`;
3. require its regenerated `total_log_likelihood` to differ from the original value `-131278.47048215955` by no more than `1e-9`;
4. replace only that scalar in an in-memory/file copy with the original authority value;
5. serialize with the exact original `indent=2`, `sort_keys=True`, `allow_nan=False`, terminal newline convention;
6. require the normalized file SHA-256 to equal the original authority SHA exactly;
7. retain all explicit B0–B3, B3-fold, byte-family selection/support and firewall assertions.

No other path, float, metadata field, candidate score, selection, support count, model output, or JSON byte may be normalized or tolerated. If any second difference appears, the normalized SHA will fail and Gate 0 remains invalid pending a new documented audit.

## Scientific consequence

This amendment does **not** weaken or change any Issue #118 model, target, hyperparameter grid, mixture rule, residual pass threshold, or interpretation. It repairs only an execution-level reproducibility requirement discovered before the residual scorer existed.

Issue #118 first reveal remains blocked until the amended Gate passes.
