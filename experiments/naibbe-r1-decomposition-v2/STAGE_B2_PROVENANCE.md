# Issue #72 V2 Stage B2 — exact aggregate provenance

Status: **PERMANENT RAW AUTHORITY PROMOTED**

## Scientific execution

- Stage B2 scoring run: `33466133615`
- exact scientific head: `1799e4d20266406f4e26d93bde8ab770db17ee02`
- all `rep5..rep24` score jobs: PASS
- 25-rep aggregate job: PASS
- aggregate artifact ID: `9784965611`
- aggregate artifact ZIP SHA-256: `8b13008d5720be82051fd73a22042350aecfaae1aea5156652680bd87c370ab7`

Exact aggregate raw file inside that artifact:

- file: `stage_b2_calibration.json`
- size: `157,852` bytes
- SHA-256: `2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147`

## Permanent repository authority

A manual base64/chunk transport attempt was abandoned after verification showed that manual text copying was not a sufficiently reliable carrier for this 157 kB scientific artifact.

No scientific computation depended on that failed transport.

Instead, GitHub Actions itself downloaded artifact `9784965611` through the repository Actions API, verified the exact raw size/SHA and scientific firewall, and committed the raw bytes directly into the repository.

Promotion:

- promotion workflow run: `33467222754`
- promotion-source head: `5a67d768593248a732fdc27d7faf5866561a4086`
- resulting bot commit: `61fe9d903d9d8d2dc587fef6c1a96dcc4c5a79af`

Permanent file:

`archive/stage_b2_calibration.json`

Required identity:

- size `157,852`
- SHA-256 `2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147`

The promotion workflow also removed the failed manual B2 chunk transport and its verification workflow so there is only one repository raw authority.

## Upstream authorities embedded in B2

- Stage B1 raw SHA-256: `b37d285b25d17623fa19910ff3f8f4586846bb8f19825c3dbdd6e8b19bb2e31d`
- Stage B2a raw SHA-256: `1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c`
- B2 population: exactly `rep0..rep24`, no result-based drops
- complete pairwise unchanged residual-topology comparisons: `300`

## Scientific firewall

The raw B2 aggregate records:

- `hard_intervention_threshold_derived=false`
- `worst_positive_is_fail_cutoff=false`
- `gaussian_tail_used_as_truth_region=false`
- `issue72_intervention_surface_loaded_or_generated=false`
- `issue72_intervention_R1_computed=false`

Therefore the entire 25-realization positive-control distribution was fixed and observed before any EL/ES/ET/EG/PT/FI R1 intervention result.
