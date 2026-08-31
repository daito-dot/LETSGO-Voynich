# Issue #64 / #58C first-reveal provenance

This directory permanently preserves the exact result of the preregistered Issue #58C target reveal.

## Scientific reveal identity

- repository: `daito-dot/LETSGO-Voynich`
- branch: `issue64-residual-token-graph`
- exact explicitly checked-out scientific head: `aa64f31942bc21f75695fcdf0065e3e7e922f687`
- PR authorizing first reveal: `#65`
- workflow: `Issue64 null-residual token-construction graph`
- workflow run ID: `33442306206`
- preflight job ID: `99653167521`
- target-first-reveal job ID: `99653243946`
- GitHub Actions artifact ID: `9776775160`
- artifact name: `issue64-residual-graph-aa64f31942bc21f75695fcdf0065e3e7e922f687`
- artifact ZIP digest reported by GitHub: `sha256:ed3c28b214ed78b9c19a67182eac7e867e51bc3e13ef4ee6c778ef329f9a7650`

The raw JSON contains GitHub's pull-request synthetic merge-context SHA `24b668f9e978f8464a12e674201dae46cd73ac5e` in its `github_sha` metadata field. The Actions checkout log explicitly records the actual scientific checkout as `aa64f31942bc21f75695fcdf0065e3e7e922f687`; that explicit checkout controls scientific head provenance.

## Plan-before-code provenance

- `PLAN_A.md` first-add commit: `88812f9772938f341473d622f4470d72990381a2`
- target executable first-add commit: `bb03304fa1f563d0da3c61a04191524a9901e7eb`
- preflight/workflow head: `aa64f31942bc21f75695fcdf0065e3e7e922f687`
- push preflight run: `33442255448`
- push preflight conclusion: success
- target on push: skipped

Opening PR #65 was the first authorized event capable of target reveal.

## Frozen external source

- source repository: `matthewdgreen/cipher_benchmark`
- source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- source file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- required Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

## Result integrity

Downloaded artifact contained exactly:

`issue64_residual_graph_results.json`

SHA-256 of the unmodified raw JSON:

`fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`

For compact permanent storage the exact bytes were compressed using deterministic gzip (`gzip -n -9`). SHA-256 of the deterministic gzip stream:

`666cfa3e211b097b30025a7947cf8bbb22e1bf24cae18a55d99017328b511d4f`

Because the GitHub connector used for this integration accepts UTF-8 text but not arbitrary local binary-file upload, the gzip stream is stored losslessly as ordered base64 text chunks:

`issue64_residual_graph_results.json.gz.b64.part00` ... `part07`.

Reconstruction:

```bash
cat issue64_residual_graph_results.json.gz.b64.part* | tr -d '\n' | base64 -d > issue64_residual_graph_results.json.gz
sha256sum issue64_residual_graph_results.json.gz
gzip -dc issue64_residual_graph_results.json.gz | sha256sum
```

Expected hashes:

- gzip: `666cfa3e211b097b30025a7947cf8bbb22e1bf24cae18a55d99017328b511d4f`
- decompressed raw JSON: `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`

## Frozen classification contained in the raw result

> `RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`

Family classifications:

- `REGISTER/SECTION RESIDUAL MODULATION`
- `LINE-POSITION RESIDUAL MODULATION`

This archive preserves the first reveal. Later reruns, descriptive analyses, reports, or follow-up designs must not replace it.