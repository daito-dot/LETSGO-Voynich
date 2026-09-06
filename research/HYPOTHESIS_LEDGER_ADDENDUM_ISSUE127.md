# Hypothesis ledger addendum — Issue #127 L4 Currier edge transport

Date: 2026-09-06
Parent: Issue #88 / Issue #104 / Issue #125

| Hypothesis / question | Status | Evidence / consequence |
|---|---|---|
| The native terminal→initial edge exists robustly in both Currier A and B | **SUPPORTED** | target-native oracle edge passes 5/5 in both targets; mean gain A `+0.0757422`, B `+0.1946842` bit/line-body target |
| Currier A/B differ mainly in useful scalar edge strength | **NOT SUPPORTED as primary explanation** | source-selected rho transfers bidirectionally when the target's own identity table is supplied; A rho `.81` works on B table, B rho `.92` works on A table, both 5/5 |
| One exact terminal→initial conditional table plus source-selected strength transports A↔B | **REJECTED** | exact source-table+source-rho transfer is negative 0/5 in both directions; A→B mean `-0.14636`, B→A `-0.19259` |
| Source identity table transports after target-only strength recalibration | **ASYMMETRIC UNDER UNMATCHED SUPPORT** | B→A passes 4/5, mean `+0.02728`; A→B fails 3/5, mean `+0.00684` |
| Missing previous-terminal classes explain cross-regime table failure | **REJECTED** | fallback only 2/15,217 A→B and 1/6,634 B→A targets |
| B→A-only table transport proves Currier-specific mapping | **NOT YET** | source support is strongly imbalanced: A 8,967 visible line-body edges vs B 19,049; B table may simply be estimated more precisely |
| Support-matched table transport preserves the directional asymmetry | **OPEN — NEXT CONFIRMATORY CONTROL** | prospectively match source-table estimation support before attributing table asymmetry to Currier regime |
| Rich latent state is needed to explain edge regime behavior | **NOT LICENSED** | observable identity table and estimation-support questions remain unresolved; no latent variable is required for the current tests |

## Working update

The L4 first reveal separates the direct edge into two properties:

> The **strength** of using a terminal→initial edge is broadly compatible across Currier A/B, but the literal conditional identity table does not exactly transfer. A weak B→A table signal survives target strength recalibration, whereas A→B does not pass the frozen stability gate. Because B provides roughly twice the source edge observations, that directional table asymmetry must be support-matched before it is interpreted as a true regime-specific mapping difference.

This is predictive mechanism evidence only. Currier is an observable manuscript regime, not a semantic state.
