# Issue #72 Stage A — mechanical audit fix record

Status: **RECORDED BEFORE ANY COUNTERFACTUAL R1 SCORE**

The first Stage-A source-audit workflow reached the target-blind audit executable and failed before producing an audit artifact.

Failure source:

- the Stage-A wrapper attempted to read `diag["primary_tokens"]`;
- the already frozen Phase64B `encrypt_manuscript` interface actually emits `diag["primary_cipher_tokens"]`.

This is a wiring error in the new Stage-A audit code only. It does not change:

- any source or codebook authority;
- P0/L0/S0/T0/G0/I0 intervention definitions;
- any deterministic seed or permutation label;
- the 0.60 representation-support gate;
- published Naibbe primary surfaces;
- any R1 statistic or threshold.

At the time of this correction:

- no Issue #72 `PLAN_A.md` target plan existed;
- no Issue #72 target scorer existed;
- no counterfactual 66-edge Q vector had been computed;
- no residual-Z, energy, reliability, topology, p-value, or per-edge diagnostic had been computed.

The correction is implemented by `source_audit72_runtime_fix.py`, which changes only the diagnostics key name while leaving the frozen audit/intervention logic untouched.
