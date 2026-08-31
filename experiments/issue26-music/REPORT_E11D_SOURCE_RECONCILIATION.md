# Issue26E11D — STA source reconciliation report

Status: **COMPLETED — DESCRIPTIVE PARSER AUDIT ONLY**

This report corrects one provisional explanation in `REPORT_E11C.md`. E11C remains `SOLVER INADEQUATE` and makes no Voynich inference.

## Question

Corrected E11B source audit:

- 4,130 running-text physical lines;
- 140,589 first-reading STA events.

E11C result metadata:

- 4,119 source running-text lines;
- 140,423 family events.

The initial suspicion was that E11C's more specific locus regex excluded 11 source lines. E11D tested that hypothesis directly without running a Latin model or plaintext decoder.

## Frozen source

- official ZL3b STA1 file
- SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`.

## Provenance

- audit-plan/workflow head: `931391882348ed9e12853342c81074087f3d5d6f`
- Actions run `33382946609`
- job `99459159798`
- artifact `9754448726`
- artifact ZIP SHA-256 `8fbfd083aba4983b9d5d28ecfe9ef93a16cdf61da0fad0b75bdc952277295b64`.

## Result

The generic E11B running-text locus regex and the E11C locus regex were both applied to every exact frozen source line.

Observed:

- generic lines: **4,130**
- generic events: **140,589**
- E11C-regex matched lines: **4,130**
- matched events: **140,589**
- unmatched lines: **0**
- unmatched events: **0**.

Therefore:

> **The hypothesis that the E11C locus regex itself drops the 11 lines / 166 events is false.**

The E11C population discrepancy is introduced later in the analysis pipeline, after raw locus matching. Candidate locations include record construction, folio/leaf eligibility, fold-universe construction, or subsequent filtering; these must be reconciled against the frozen E11B population before a new Voynich substitution reveal.

## Authority correction

Where `REPORT_E11C.md` says that “E11C's locus parser excludes 11 lines / 166 events,” read that sentence as a provisional diagnosis superseded by this E11D source audit.

The underlying facts remain unchanged:

1. E11C is scientifically inconclusive because its mandatory positive control failed;
2. its analysis metadata also differs from the E11B source audit;
3. the mismatch is **not caused by the locus regex**;
4. do not change E11B expected counts to fit E11C;
5. no future León/STA Voynich reveal is valid until the exact analysis-population transformation is documented and preregistered.

## Next step

Solver work is isolated in `PLAN_E11D_SOLVER_CALIBRATION.md` and uses no Voynich plaintext/scoring. In parallel, a source-to-analysis population reconciliation must explain exactly which 11 lines / 166 events are removed and why, before a future E11E plan is frozen.
