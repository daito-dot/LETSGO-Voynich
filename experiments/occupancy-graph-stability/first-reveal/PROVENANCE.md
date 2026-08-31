# Issue #62 / #58B first-reveal provenance

This directory permanently preserves the exact result of the preregistered Issue #58B target reveal.

## Scientific reveal identity

- repository: `daito-dot/LETSGO-Voynich`
- branch: `issue62-occupancy-graph-stability`
- exact scientific first-reveal head: `ebc794567574e20eac82df6a856d5ea4dd72b9cb`
- workflow: `Issue62 signed occupancy graph stability`
- workflow run ID: `33437742982`
- preflight job ID: `99638198622`
- target-first-reveal job ID: `99638298655`
- GitHub Actions artifact ID: `9775074050`
- artifact name: `issue62-graph-stability-ebc794567574e20eac82df6a856d5ea4dd72b9cb`
- artifact ZIP digest reported by GitHub: `sha256:ef02c4e7333cef13a9a4793a6bdc0a91996feb416bd32756e7254ea33c6f329f`

Both workflow jobs completed successfully. Preflight verified plan-before-executable ordering, exact source identity, parser/syntax/self-tests and frozen population reproduction before target scoring.

## Frozen external source

- source repository: `matthewdgreen/cipher_benchmark`
- source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- source file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- required Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

## Result integrity

Downloaded artifact contained exactly:

`issue62_graph_stability_results.json`

SHA-256 of the unmodified raw JSON:

`45024fd1d15b2d2484ffc26657ccc8007fd6a04dc3ed1b53b243f77ba455f8a0`

For permanent repository storage the exact bytes were compressed using deterministic gzip (`gzip -n -9`). SHA-256 of the stored gzip file:

`ce75f676885f44d69f59fed733744da7cdfe3a446ac4d4e1423592667a063102`

Decompressing `issue62_graph_stability_results.json.gz` must reproduce raw SHA-256 `45024fd1d15b2d2484ffc26657ccc8007fd6a04dc3ed1b53b243f77ba455f8a0`.

## Frozen classifications contained in the raw result

- `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`
- `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

This archive preserves the first reveal. Later descriptive analyses, reports, or follow-up designs must not alter or replace it.