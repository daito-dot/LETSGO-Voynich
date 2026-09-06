# Issue #127 L4 Currier edge transport first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL — SUPPORT-MATCHED FOLLOW-UP REQUIRED FOR CAUSAL INTERPRETATION OF ASYMMETRY**
Parent: Issue #88 / Issue #104 / Issue #125

## Frozen scientific head

`ca92553cae7fa3afb056f10f142b3f9902bf5ed0`

No A→B/B→A edge transport gain, rho, penalty or formal class was inspected before PR #129 was opened at this head.

## Workflow authority

- workflow run `34028942191`
- conclusion: **SUCCESS**
- artifact `9987979148`
- artifact ZIP digest `sha256:99f1d561c6871763027b8240e44ab220ded50e766c7e765d87f46d5926b459a3`
- result JSON SHA-256 `bf19cb3cd9e93d6e7b6391223f89ec85ed06fdf9d0344f8b1a9bb56192d2e2d7`
- merged Gate0 JSON SHA-256 reproduced: `31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`
- Phase 3A Currier authority SHA-256 reproduced: `e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`.

The run passed all target-outer non-selection, fixed-model, support and firewall assertions.

## Frozen mechanism-only design

Target-local POS2 supplies all target onset and within-token factors. Only `P(current_initial | previous_terminal)` is transported from the source Currier regime. Fixed `k=2`, `alpha=.01`.

Edge strength is a separate normalized interpolation:

`p_rho = (1-rho) p_POS2 + rho p_EDGE`, `rho=0.00..1.00`.

Source rho is selected by source-only five-fold CV. Target-calibrated rho is selected using target inner folds only; target outer folds are untouched.

Primary scoring support is parser-accepted line-body current tokens only.

## Source-only strengths

- Currier A: `rho_A = .81`
- Currier B: `rho_B = .92`

## Frozen formal classifications

- `TABLE_TRANSPORT`: **B→A ONLY**
- `EXACT_TRANSPORT`: **NONE**
- `SOURCE_STRENGTH_COMPATIBILITY`: **BIDIRECTIONAL**
- `TARGET_NATIVE_EDGE`: **A PASS / B PASS**

## A→B

### Native B edge

Target-native oracle gain:

- fold values `+0.2467066, +0.1578457, +0.1882025, +0.2173018, +0.1633646`
- mean `+0.1946842 bit/line-body-target`
- positive `5/5` — PASS.

Native B target-oracle rho is `.91,.91,.91,.91,.93`.

### Strength transport

Use target B identity table with source-A `rho=.81`:

- mean gain `+0.1900690`
- positive `5/5` — PASS.

Thus A's selected scalar strength is highly compatible with B once B's own identity map is supplied; its mean penalty relative to target oracle is only about `0.00462 bit/target`.

### Source A table with target B recalibration

Target-inner selected rho for the A table is `.16,.15,.16,.16,.13`.

Gain:

- `-0.0068166, +0.0192004, -0.0018108, +0.0041456, +0.0194657`
- mean `+0.0068369`
- positive `3/5` — FAIL.

### Exact source A table + source-A rho

- mean gain `-0.1463628`
- positive `0/5` — FAIL.

The large negative exact-transfer result arises because source-A rho `.81` is far larger than the target-calibrated useful weight for the A table on B (`~.13-.16`).

## B→A

### Native A edge

Target-native oracle gain:

- fold values `+0.0651432, +0.0709218, +0.0814479, +0.0604336, +0.1007645`
- mean `+0.0757422 bit/line-body-target`
- positive `5/5` — PASS.

Native A target-oracle rho is `.75,.75,.75,.80,.75`.

### Strength transport

Use target A identity table with source-B `rho=.92`:

- mean gain `+0.0745402`
- positive `5/5` — PASS.

Thus B's selected scalar strength is also compatible with A once A's own identity map is supplied; mean penalty relative to target oracle is only about `0.00120 bit/target`.

### Source B table with target A recalibration

Target-inner selected rho for the B table is `.21,.16,.19,.20,.18`.

Gain:

- `-0.0109814, +0.0666305, +0.0263885, +0.0212063, +0.0331749`
- mean `+0.0272838`
- positive `4/5` — PASS.

### Exact source B table + source-B rho

- mean gain `-0.1925913`
- positive `0/5` — FAIL.

Again, source-B rho `.92` is far larger than the target-calibrated useful weight for the B table on A (`~.16-.21`).

## Source-context support is not the failure mode

Fallback to target POS2 because a source terminal class was unseen is negligible:

- A→B: `2 / 15,217 = 0.0131%`
- B→A: `1 / 6,634 = 0.0151%`.

Thus the cross-regime degradation is not caused by missing previous-terminal classes.

## Current interpretation

The first-reveal result cleanly separates scalar strength from identity-table content:

1. the native terminal→initial edge exists robustly in both Currier regimes;
2. source-selected **strength** transfers bidirectionally when the target's own identity map is used;
3. the actual source conditional table does not transfer exactly at source strength in either direction;
4. after target strength recalibration, the B table carries a weaker but stable signal into A, while the A table does not meet the frozen A→B stability gate.

This makes a simple universal terminal→initial conditional table unsupported. The result is qualitatively different from Phase 3A LOCAL40, whose geometry and strength transported cleanly.

However, the **directional table asymmetry is not yet attributable solely to Currier mapping differences**, because source support is materially imbalanced: Gate0 observed 8,967 visible A line-body edges versus 19,049 B edges, and 6,634 versus 15,217 accepted edge targets. A smaller A table may simply be estimated less precisely than B.

Therefore the next licensed confirmatory control is support-matched table transport: train B source tables on prospectively matched source support comparable to A, and symmetrically control A/B estimation size, without changing target folds or revealed gain thresholds. Only after that control should the B→A-only table asymmetry be interpreted as regime-specific mapping.

## Firewall

No B3 model was refit or scored in L4; no latent state, hand/domain/semantic conditioning, Issue #84 target, plaintext, language or cipher claim was used. Currier remains an observable manuscript regime.
