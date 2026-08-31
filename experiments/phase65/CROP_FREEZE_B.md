# Phase 65B1 text-blind crop freeze

Status: **PASS — crop rectangles, exact Yale source identities, crop PNG hashes and retained population are frozen before any P25 association statistic.**

Normative authority: `PLAN_B.md`.

## Exact execution provenance

- implementation branch: `phase65b-image-label-science`
- crop-spec/workflow head SHA: `aebc1b66410a1f28622e22223613e3a868c76f7b`
- GitHub Actions workflow: `Phase65B text-blind crop freeze`
- run: `33347087104`
- job: `99353155140`
- conclusion: `success`
- artifact: `9742332663`
- artifact name: `phase65b-text-blind-crop-freeze-aebc1b66410a1f28622e22223613e3a868c76f7b`
- artifact ZIP SHA-256: `5c0628c36a66a97fdf0c39d56d5cf830a456418b6c88c2e664b32ff08067e243`
- generated `CROP_MANIFEST_B.generated.json` SHA-256: `890dcd863dc555db3c2a4f6d4e6e826b1c79a4b46cbe6008f79c6cf483f11303`

The generated manifest is promoted to `CROP_MANIFEST_B.json` without changing crop rectangles, source identities, quality flags or crop hashes.

## Frozen crop rule

`CROP_SPEC_B.json` fixes one integer `(x, y, width, height)` rectangle for every transcription-confidence-eligible V1-P25 object. Rectangles were selected on the exact Yale scans frozen by Phase65B0 using visible drawing/layout geometry only.

The crop objective is a practical axis-aligned region that remains attributable to one intended plant fragment while stopping before associated label glyphs or a neighboring plant enters the rectangle. Because labels are physically adjacent to roots/stems, a crop need not contain the full drawing; label exclusion takes precedence. No rectangle was selected or revised using DINO embeddings, label strings, string distance, correlation, retrieval scores or permutation results.

## Result

No unit was newly excluded by crop quality. The pre-existing confidence exclusion remains:

- `L2.7 / f102v2.16` — excluded by the frozen transcription-confidence firewall before crop science.

Retained population:

- f100v: `13` = T `4` + M `5` + B `4`
- f102v2: `11` = L2 `6` + L3 `5`
- combined: `24/25`

All preregistered coverage-firewall conditions pass.

The Actions artifact contains all 24 PNG crops plus `crop-pngs.sha256`; the exact per-crop SHA-256 values are also stored in `CROP_MANIFEST_B.json`.

## Anti-leak state

At completion of B1:

- P25 visual↔text association computed: **false**
- DINO embeddings computed: **false**
- text distance computed: **false**
- correlation computed: **false**
- permutation statistic computed: **false**

The crop materialization executable itself contains no text parser, DINO path, string-distance function, correlation or permutation statistic.

## Next gate

Proceed to the synthetic-only implementation preflight required by `PLAN_B.md`. It must prove the parser, DINO forward path/preprocessing, normalized Levenshtein, Spearman aggregation and exact permutation machinery without computing any P25 image↔label association outcome. The first scientific reveal remains prohibited until that implementation/dependency identity is frozen and the synthetic preflight passes.
