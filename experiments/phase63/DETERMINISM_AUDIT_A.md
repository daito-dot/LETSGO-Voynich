# Phase 63A — determinism / replay audit

Date: 2026-08-30

Status: **scientific verdict stable; bytewise JSON nondeterminism explained as machine-precision floating reduction noise**.

## Why this audit exists

The first frozen Phase63A run completed successfully and passed every preregistered robustness condition. Before persisting the result, a second clean GitHub Actions run was required to reproduce the first raw JSON SHA-256 exactly.

That bytewise digest check failed. The result was therefore **not** silently persisted or declared exact-replay certified. A third unchanged scientific run was captured for structural comparison.

## Runs

### First scientific run

- Actions run: `33315453851`
- job: `99267937410`
- artifact: `9733309531`
- artifact ZIP SHA-256: `d96a4362b16b77cafdf0addd031b9b5c1e293edbbe60d0aaedbd6f4a263ba60c`
- raw JSON SHA-256: `bcd05d1823e17b034c0abf984a0af9b0cb31b5a37bd9e604c327ab9aff1937a7`

Scientific verdict: all frozen R1/R2/R3 conditions pass.

### Second clean run

- Actions run: `33315570673`
- job: `99268270869`
- scientific executable completed successfully;
- exact first-run raw SHA check failed before persistence.

This triggered the audit rather than a result overwrite.

### Third unchanged scientific replay

- Actions run: `33315744714`
- job: `99268753900`
- replay artifact: `9733399839`
- replay artifact ZIP SHA-256: `a0f1951d1fa1392f485fb0d0b5c24a43b4e2440ae773a62c2231f553d896ad70`
- replay raw JSON SHA-256: `268ff3b65eacdb2611409a11a362007fa66bc4dc9d59ad15da5c237d3053262e`

Scientific verdict: again all frozen R1/R2/R3 conditions pass with the same printed aggregate values.

## Exact structural diff: first run vs third run

The two parsed JSON objects differ in **16 scalar values only**.

Every difference is in an S1 floating-point projection field:

- individual A1-R1 replicate S1 values;
- downstream fold mean S1 values;
- downstream fold S1 ratios.

Maximum absolute difference:

`2.220446049250313e-16`

Maximum observed relative difference is approximately `3e-16`.

No difference was found in:

- S2 values;
- S3 values;
- generated-type counts / training-vocabulary leakage audit;
- held-out coverage counts;
- every H62-P1 observed/null/excess/profile value;
- every H62-P1 candidate distance;
- every H62-P1 fold win;
- the R1/R2/R3 booleans;
- the final robustness verdict;
- any string/integer/discrete field.

Therefore the raw-byte mismatch is not evidence that stochastic generation changed across runs. The observed difference is confined to machine-precision floating-point reduction/projection arithmetic in S1, consistent with running the same NumPy calculation on different hosted-runner CPU environments.

## Canonical semantic digest

For audit only, both JSONs were recursively canonicalized by:

1. sorting object keys;
2. rounding floating-point values to 14 decimal places;
3. serializing compact UTF-8 JSON.

Both first and third runs then have the same SHA-256:

`cd53f47729c864badb5e8c747cfd9ad989de9c616ca54dd5bdcb83b075c33c74`

This canonical digest is a reproducibility diagnostic, not a change to any scientific metric or threshold.

## Correction to the initial suspicion

The first suspicion was Python set/hash iteration in the edit1 neighbor graph. Inspection of current `phase61c_joint_model.py` shows this is already canonicalized:

`out[w] = sorted(cand)`

Thus no neighbor-order repair is required and no scientific generator code is changed.

## Scientific consequence

Phase63A may be interpreted using the **first frozen scientific run** as historical result authority, with the third run as a clean semantic replay.

Allowed claim:

> Phase63A's pass/fail verdict and reported scientific values are reproducible to machine precision across clean hosted runners; byte-for-byte raw JSON identity is not portable because S1 floating reduction changes at approximately 1e-16.

Do not claim:

> every raw floating-point byte is platform-independent.

No parameter, model mechanism, target, metric, threshold or result is altered by this audit.

## Persistence rule

The repository result file should preserve the exact **first-run** JSON artifact, not replace it with a later replay. Its first-run raw SHA-256 remains the primary byte-level provenance identifier.

Future deterministic artifact checks involving floating-point JSON should use both:

- exact source/input/code identities;
- a documented numerical-tolerance or canonical-semantic comparison;

rather than requiring cross-CPU byte identity where the numerical algorithm does not guarantee it.