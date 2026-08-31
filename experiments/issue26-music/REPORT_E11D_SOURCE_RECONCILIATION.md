# Issue26E11D — STA source reconciliation report

Status: **COMPLETED — POPULATION DIFFERENCE RESOLVED**

This report corrects one provisional explanation in `REPORT_E11C.md`. E11C remains `SOLVER INADEQUATE` and makes no Voynich inference.

## Question

Corrected E11B source audit:

- 4,130 running-text physical lines;
- 140,589 first-reading STA events.

E11C result metadata:

- 4,119 source running-text lines;
- 140,423 family events.

The initial suspicion was that E11C's more specific locus regex excluded 11 source lines. E11D tested the source-to-analysis pipeline without running a Latin model or plaintext decoder.

## Frozen source

- official ZL3b STA1 file
- SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`.

## Stage 1 provenance and result

- audit-plan/workflow head: `931391882348ed9e12853342c81074087f3d5d6f`
- Actions run `33382946609`
- job `99459159798`
- artifact `9754448726`
- artifact ZIP SHA-256 `8fbfd083aba4983b9d5d28ecfe9ef93a16cdf61da0fad0b75bdc952277295b64`.

The generic E11B running-text locus regex and the E11C locus regex were both applied to every exact frozen source line.

Observed:

- generic lines: **4,130**
- generic events: **140,589**
- E11C-regex matched lines: **4,130**
- matched events: **140,589**
- unmatched lines: **0**
- unmatched events: **0**.

Therefore the hypothesis that the locus regex itself drops the 11 lines / 166 events was false.

## Stage 2 provenance and result

The next audit traced the already-frozen E11C numerical-leaf eligibility rule after successful locus matching.

- workflow/head: `612cc3546f8be2ce2d12c4aa828d277c8e9c2237`
- Actions run `33383624777`
- job `99461236795`
- artifact `9754700216`
- artifact ZIP SHA-256 `779b0535ede4bf7ea5e406d7741855b41703923b672ad60764c6fdfeb277bbdb`.

Observed:

- source-running-text lines: **4,130**
- source events: **140,589**
- locus-regex matches: **4,130 / 140,589**
- numerical-leaf eligible: **4,119 / 140,423**
- numerical-leaf ineligible: **11 / 166**
- the eligible counts match E11C metadata exactly.

All 11 ineligible lines are on the special Rosettes locus `fRos`:

- `<fRos.39,@Pb>` — 14 events
- `<fRos.40,+Pb>` — 12
- `<fRos.137,@Pb>` — 14
- `<fRos.138,*Pb>` — 24
- `<fRos.139,@Pb>` — 14
- `<fRos.140,+Pb>` — 16
- `<fRos.141,+Pb>` — 15
- `<fRos.142,@Pb>` — 13
- `<fRos.143,+Pb>` — 18
- `<fRos.144,+Pb>` — 18
- `<fRos.145,+Pb>` — 8.

Total: **11 lines / 166 events**.

## Resolution

> **The E11B/E11C count difference is not missing data. It is exactly the special `fRos` Rosettes population that cannot enter E11C's numerical physical-leaf five-fold assignment.**

The two counts describe two legitimate but different populations:

- **4,130 / 140,589** = broad source-level running-text audit, including `fRos`;
- **4,119 / 140,423** = E11C five-fold analysis population restricted to records with a numerical physical leaf.

Future León/STA cross-validation must state this eligibility boundary explicitly rather than calling the difference a parser loss. `fRos` may be reported separately descriptively, but it must not be silently inserted into numerical-leaf folds or assigned to an arbitrary fold.

## Authority correction

Where `REPORT_E11C.md` says that “E11C's locus parser excludes 11 lines / 166 events,” that diagnosis is superseded.

The authoritative interpretation is now:

1. E11C remains scientifically inconclusive because its mandatory positive control failed;
2. the source parser sees the complete 4,130 / 140,589 population;
3. the 11 / 166 difference is entirely `fRos` numerical-leaf ineligibility;
4. the valid five-fold numerical-leaf analysis population is therefore 4,119 / 140,423;
5. no future León/STA Voynich reveal is authorized until a substitution solver passes a prospectively locked synthetic validation battery.

## Next step

Population reconciliation is complete. Solver engineering remains isolated from Voynich under `issue26-music-e11d-solver-validation`. The development solver must first demonstrate reliable recovery on known synthetic monoalphabetic substitutions; only then may its parameters be frozen and the locked validation battery opened.
