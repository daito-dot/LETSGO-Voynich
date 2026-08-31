# Phase 66A — morphology eligibility report

Status: **IMAGE SIDE SEALED; NO IMAGE↔TEXT ASSOCIATION COMPUTED**

Inputs: frozen Phase65 crop artifact `9742332663`; `ANNOTATION_A1.json`, `ANNOTATION_A2.json`, `ANNOTATION_A3.json`; automatic 2/3 modal aggregation in `MORPHOLOGY_TABLE_A.json`.

## Reproducibility audit

A2 and A3 are exact-state identical. A1 differs from their common primary-character states in only three object/field cells: `T.1 flower_or_inflorescence_visible`, `T.2 leaf_arrangement`, and `M.5 stem_branching_architecture`. Thus 381/384 primary object×field cells are unanimous across all three passes (99.22%); every cell has a 2/3 modal state.

Per-character three-pass unanimous agreement is 24/24 for all primary characters except:

- `flower_or_inflorescence_visible`: 23/24 = 0.9583;
- `leaf_arrangement`: 23/24 = 0.9583;
- `stem_branching_architecture`: 23/24 = 0.9583.

All primary characters therefore clear the frozen >=0.80 repeat-stability requirement. This does **not** imply independent-rater reliability: all three passes used the same GPT-5.6 Sol runtime, whose exact build pin is not exposed. That limitation remains part of the audit record.

## Frozen primary-character firewall

| character | non-U | aggregated state counts | eligibility |
|---|---:|---|---|
| leaf_visible | 22 | 1=20; 0=2 | FAIL — second state <4 |
| stem_axis_visible | 15 | 1=10; 0=5 | FAIL — <16 observable |
| root_or_subterranean_visible | 23 | 0=21; 1=2 | FAIL — second state <4 |
| flower_or_inflorescence_visible | 20 | 0=19; 1=1 | FAIL — second state <4 |
| fruit_or_seed_body_visible | 24 | 0=24 | FAIL — only one state |
| leaf_composition | 18 | simple=14; deeply_divided_uncertain_leaflet_status=4 | **ELIGIBLE** |
| leaf_arrangement | 19 | alternate=5; basal_or_rosette=6; opposite=2; single_or_insufficient_nodes=6 | **ELIGIBLE** |
| leaf_blade_shape | 15 | broad elliptic/ovate=2; orbicular=4; narrow lanceolate/elliptic=3; linear=2; lobed/divided=4 | FAIL — <16 observable |
| leaf_margin | 18 | serrate/dentate=3; entire=6; lobed/incised=6; crenate=3 | **ELIGIBLE** |
| leaf_apex | 13 | acute=7; rounded=5; mixed=1 | FAIL — <16 observable |
| leaf_base | 3 | attenuate/cuneate=3 | FAIL — <16 observable |
| venation_depiction | 4 | single-midvein=3; reticulate=1 | FAIL — <16 observable |
| stem_branching_architecture | 8 | lateral-branch=6; unbranched=2 | FAIL — <16 observable |
| root_subterranean_architecture | 2 | compact-storage-body-like=2 | FAIL — <16 observable |
| reproductive_architecture | 1 | spike/raceme-like=1 | FAIL — <16 observable |
| reproductive_symmetry | 1 | not_resolvable=1 | FAIL — <16 observable |

## Eligible character distribution checks

`leaf_composition`: simple occurs across f100v/T=4, M=3, B=3, f102v2/L2=3, L3=1; divided occurs M=1, B=1, L2=1, L3=1. Largest single-row share is 28.6% and 25.0% respectively.

`leaf_arrangement`: observations occur on both pages. Largest single-row share of any observed state is 60% (`alternate`, f100v/T=3 of 5), below the frozen 80% ceiling.

`leaf_margin`: observations occur on both pages. Largest single-row share is 66.7% (`serrate_or_dentate`, f100v/B=2 of 3), below the frozen 80% ceiling.

Therefore exactly three primary morphology characters cross the preregistered image-side eligibility firewall:

1. `leaf_composition`
2. `leaf_arrangement`
3. `leaf_margin`

No other primary character may own a Phase66 primary claim, even if it later appears associated with label structure.

## Scientific boundary

This report contains no Voynich label feature, no morphology↔label statistic, and no semantic interpretation. Phase66A establishes only that a frozen image-only measurement table exists and that three predefined morphology characters are sufficiently observable, variable, distributed, and repeat-stable to be candidates for a later prospective association test.

The next legal step is to freeze the text-side feature family and Phase66B association/null/multiplicity rules **without inspecting morphology↔text outcomes**. Only after that freeze may the first cross-modal statistic be computed.
