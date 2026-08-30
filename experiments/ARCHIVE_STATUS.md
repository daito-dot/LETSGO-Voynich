# Experiment archive completeness

This file prevents a compact public summary from being mistaken for a complete raw archive.

## Current state

| Phase | Method/report | Code | Results | Archive status |
|---|---|---|---|---|
| 44 | public summary + frozen partition | partial | authoritative compact benchmark result | PARTIAL RAW ARCHIVE |
| 45 | interpretation in STATUS/ledger | not yet fully normalized | not yet fully migrated | PENDING RAW MIGRATION |
| 46 | public README + result summary | historical source exists locally | compact authoritative summary; historical raw JSON is large | PARTIAL RAW ARCHIVE |
| 47 | public README + decomposition summary | historical source exists locally | compact authoritative summary; historical raw JSON is large | PARTIAL RAW ARCHIVE |
| 48 | ledger/status + compact result | historical source exists locally | compact result migrated | PARTIAL RAW ARCHIVE |
| 49 | ledger/status + compact result | historical source exists locally | compact result migrated | PARTIAL RAW ARCHIVE |
| 50 | public README + compact result | historical source exists locally | compact result migrated | PARTIAL RAW ARCHIVE |
| 51 | public README + frozen public entrypoint | frozen spec recorded; historical implementation normalization pending | compact authoritative result migrated | REPRO SPEC COMPLETE / HISTORICAL CODE PARTIAL |
| 52 | public README | section-variance code migrated | matched-section + Latin pilot results migrated | ACTIVE / PARTIAL |

## Meaning of “authoritative compact result”

The compact JSON preserves the headline values and interpretation currently used by `research/STATUS.md` and `research/hypothesis-ledger.md`. It does **not** replace a historical raw result file when per-replicate rows are needed for reanalysis.

## Historical raw files still to migrate/normalize

High priority:

- Phase44 predictive/generator implementation and copy-locality scripts
- Phase45 paragraph state/boundary scripts and result files
- Phase46 plaintext-control implementation and raw result JSON
- Phase47 operation-decomposition implementation and raw result JSON
- Phase48–50 source scripts
- full Phase51 historical generator/falsification implementation
- remaining Phase52 raw section-variance result and expanded genre panel as it is produced

The local historical workspace remains necessary for exact re-execution until this table reaches COMPLETE. `RESUME.md` remains sufficient for research-state reconstruction.
