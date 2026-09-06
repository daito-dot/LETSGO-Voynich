# Issue #112 Phase 4A — Gate 0 provenance

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE GATE 0 — PASS**

## Scientific head

The first complete support audit was run on PR #113 head:

- commit: `adfbb7e51d119dbc36fbef201f8f9101ac1ee2ad`
- workflow: `Issue112 Phase4A raw boundary Gate0`
- workflow run: `34024096077`
- conclusion: `success`
- artifact: `9986480597` (`issue112-phase4a-boundary-gate0`)
- artifact ZIP digest: `sha256:6c932a31cd228fdd7ae84df11295840ae8478721a1296f3f01bae7d22aa4ef87`
- `phase4a_boundary_gate0.json` SHA-256: `e736e1360aa3b0fc6fbdeb6fafb7beff5d48d4ce1102c340516c347e8f770c08`

## Source authority reproduced

- ZL3b Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- bytes: `411671`
- header: `#=IVTFF Eva- 2.0 M 5`

The workflow checked out `matthewdgreen/cipher_benchmark` at frozen commit `315f0cad4de3d021bd4185765c037cf2a28d341c` and independently verified both the Git blob and SHA-256 before running the audit.

## Frozen fold authority

The original five physical-leaf fold identity was reproduced using `phase62b_n0.parse_voynich + physical_leaf_folds` for membership only.

- numeric physical leaves: `99`
- fold identity SHA-256: `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`

No historical normalized token or SlotParser decision was used for Phase-4A event eligibility.

## Score-free Gate result

Eligible populations:

- REAL_SPACE: `21,363`
- MID_TOKEN: `21,313`
- P2 REAL_SPACE: `18,696`

By original physical-leaf fold:

| Fold | REAL_SPACE | MID_TOKEN | P2 REAL_SPACE |
|---:|---:|---:|---:|
| 0 | 3,685 | 3,682 | 3,240 |
| 1 | 4,171 | 4,224 | 3,675 |
| 2 | 4,717 | 4,616 | 4,176 |
| 3 | 4,623 | 4,591 | 4,016 |
| 4 | 4,167 | 4,200 | 3,589 |

All three support predicates are true in all five folds. Frozen Gate classification:

> **PASS — PROCEED TO PHASE-4A P1/P2 FIRST REVEAL**

## Event identities

- REAL_SPACE event identity SHA-256: `45d456d106c96f3085774bfe3f2b8a4ed1c1a1bc70ae135215ea590d0039752c`
- MID_TOKEN event identity SHA-256: `2e05e74a35d31391da976bb7a447694210a26e390397ecb738982cac4134b7af`
- P2 REAL_SPACE event identity SHA-256: `ccd7efe6ce35b74fb41e227893d2bd972c2c4db60f9ae2c3830b38da6c45209b`

The scoring implementation must reproduce these identities before computing P1/P2.

## Firewall confirmation

The authoritative JSON records:

- `predictive_scores_computed = false`
- `boundary_model_fitted = false`
- `slotparser_used_for_event_eligibility = false`
- `target_surface_metrics_used = false`
- `issue84_target_used = false`
- `semantic_or_image_context_used = false`
- `latent_state_fitted = false`

Therefore this Gate reveals support only. It does not reveal whether real spaces are favored by the future boundary model.

Refs #88, #112, #113.
