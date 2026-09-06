# Current-status addendum — Issue #127 L4 Currier edge transport

Date: 2026-09-06

This addendum supersedes the `STATUS.md` frontier statement that Currier transport of the compact terminal→initial edge is still untested. Exact provenance is in `experiments/predictive-information/residual-gate/L4_CURRIER_TRANSPORT_PROVENANCE.md`.

## New accepted result

The native explicit terminal→initial edge is robust in both Currier regimes:

- target A native edge: `+0.0757422 bit/line-body-target`, positive `5/5`;
- target B native edge: `+0.1946842`, positive `5/5`.

Source-only selected edge strengths are:

- A `rho=.81`;
- B `rho=.92`.

When these source strengths are applied to the **target's own identity table**, strength compatibility is bidirectional and positive `5/5` in both targets. Thus a simple scalar-strength difference is not the main reason cross-regime edge transport fails.

The identity tables behave differently:

- exact source table + source strength: fails `0/5` in both directions;
- source table + target-inner strength recalibration: B→A passes `4/5`, A→B fails `3/5`.

Fallback for source-unseen previous-terminal classes is negligible (<0.02% in both directions), so missing terminal classes do not explain the failure.

## Current interpretation

The compact line-local edge is manuscript-wide as a **mechanism family**, but a single literal terminal→initial conditional table is not supported as universal by the first transport reveal. Useful scalar strength is broadly compatible; conditional mapping is the unstable component.

However, B has roughly twice A's source edge observations (19,049 vs 8,967 visible line-body edges; 15,217 vs 6,634 accepted edge targets). Therefore the apparent B→A-only table transport cannot yet be attributed to a true Currier mapping asymmetry. A prospectively support-matched transport control is required next.

No latent-state, semantic, language, cipher or historical-mechanism claim follows.
