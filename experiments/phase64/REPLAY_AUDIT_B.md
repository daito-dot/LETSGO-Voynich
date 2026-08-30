# Phase 64B replay audit — published Naibbe C1

Status: **EXACT-BYTE REPLAY CONFIRMED**.

This audit concerns reproducibility only. It does not change the frozen Phase64B candidate, scorecard, pass/fail rules, scientific result, classification or interpretation.

## First successful scientific reveal authority

Exact scientific head:

`1e80c41f0e502a7dacb593723dbf9d81f9f84add`

Actions provenance:

- run `33338000172`
- job `99328325145`
- artifact `9739776686`
- artifact name `phase64b-first-reveal`
- artifact ZIP SHA-256 `f8534605b0c6b2396341d47d54b7d4280632ba14eb30ae7f34b8208921dab378`
- archived raw JSON SHA-256 `f88954c2efa2ec69e4bee0cd6fb1c70b49f08b1f44206c7f70bd540ad538d35d`

The exact artifact bytes were hash-verified and committed as `phase64b_science_results.json` before result interpretation was synchronized into the research-state documents.

## Replay diagnostic

A clean diagnostic replay was run from the exact first-reveal scientific head, not from later result-documentation commits.

Actions provenance:

- diagnostic head `1d3046fb6b3f9c8f2a5c290131534ba1dc672cec`
- run `33339140111`
- job `99331437730`
- artifact `9740114679`
- artifact name `phase64b-replay-diagnostic`
- diagnostic artifact ZIP SHA-256 `d91cadd5440d181236280269cdc757f3cd6e465f77553632df30b3dc1776bd08`

The replay pinned and verified:

- project scientific head `1e80c41f0e502a7dacb593723dbf9d81f9f84add`;
- ZL3b mirror commit `315f0cad4de3d021bd4185765c037cf2a28d341c` and ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- CREMMA commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- Naibbe commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2` and the exact pinned Python/table/README blobs;
- `PYTHONHASHSEED=0`;
- `numpy==2.5.2`;
- `pandas==3.0.5`.

No scientific executable was modified for the replay.

## Exact comparison result

Archived first reveal:

`f88954c2efa2ec69e4bee0cd6fb1c70b49f08b1f44206c7f70bd540ad538d35d`

Clean replay:

`f88954c2efa2ec69e4bee0cd6fb1c70b49f08b1f44206c7f70bd540ad538d35d`

Audit output:

- raw-byte identical: **true**
- nonnumeric differences: **0**
- numeric differences: **0**
- maximum absolute numeric difference: **0.0**
- frozen classification equal: **true**
- primary evaluation exact-JSON equal: **true**
- canonical hashes equal at 15, 14, 13, 12, 11 and 10 decimal places.

Thus the clean replay is not merely verdict-stable or machine-precision-equivalent: it reproduces the archived first-reveal JSON byte-for-byte under the exact frozen head and dependency versions.

## Conclusion

> **Phase64B first-reveal scientific output is exact-byte reproducible under its frozen code, source identities, seeds, environment and dependency versions.**

The authoritative scientific classification remains `C1-E0 PARTIAL`; the replay does not upgrade, weaken or reinterpret that result.
