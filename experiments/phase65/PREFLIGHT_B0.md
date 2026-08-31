# Phase 65B0 source-only preflight audit

Status: **PASS — source identities frozen; no P25 content-relation statistic computed.**

Normative authority: `PLAN_B.md`.

## Exact execution provenance

- implementation branch: `phase65b-image-label-science`
- preflight head SHA: `1e6aa9824084dadec2bd43b65da9f7f47d3e1cbb`
- GitHub Actions workflow: `Phase65B source-only preflight`
- run: `33345560254`
- job: `99348878636`
- conclusion: `success`
- artifact: `9741863634`
- artifact name: `phase65b-source-preflight-1e6aa9824084dadec2bd43b65da9f7f47d3e1cbb`
- artifact ZIP SHA-256: `9104f0aec5829fff0c69e9bbd188d474353ce07d161feb1a5b05d80db058cd5a`
- generated `SOURCE_MANIFEST_B.generated.json` SHA-256: `71023a2c395ad95848697e866373541deb1beb02dfbfaaabcd21140293775a56`

The generated manifest was promoted to `SOURCE_MANIFEST_B.json` without changing scientific source identities or P25 locus selection.

## Frozen source identities

### Primary ZL3b transcription

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- byte size: `411671`
- SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`

The exact 25 preregistered P25 label loci were extracted only to freeze source strings and confidence flags. No pairwise text distance was computed.

### Independent IT2a transcription

- URL/final URL: `https://www.voynich.nu/data/IT2a-n.txt`
- IVTFF header: `#=IVTFF EvaT 2.0 M 3`
- byte size: `342104`
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

### DINOv2 external representation

- repository: `facebookresearch/dinov2`
- commit: `7764ea0f912e53c92e82eb78a2a1631e92725fc8`
- model: `dinov2_vits14`
- official weight byte size: `88283115`
- weight SHA-256: `b938bf1bc15cd2ec0feacfe3a1bb553fe8ea9ca46a7e1d8d00217f29aef60cd9`

The B0 workflow downloaded and hashed the weights but did **not** instantiate DINOv2 or compute any P25 embedding.

### Yale manuscript images

#### f100v source scan

- Yale image ID: `1006249`
- IIIF retrieval/final URL: `https://collections.library.yale.edu/iiif/2/1006249/full/full/0/default.jpg`
- dimensions: `7486 × 3715`
- byte size: `6794523`
- SHA-256: `72637b9770f40f7a8ff6b96a551e64775e88994ae69bafec0b43d48974364c33`
- note: this child image is the combined f100v + f101r scan; the crop freeze must isolate only the f100v page/object regions.

#### f102v2 source scan

- Yale image ID: `1006252`
- IIIF retrieval/final URL: `https://collections.library.yale.edu/iiif/2/1006252/full/full/0/default.jpg`
- dimensions: `2981 × 3795`
- byte size: `2576704`
- SHA-256: `8cdb1030d805b968932146124915cb0d86f7abf853167ffec028b59599820fad`

Both image downloads decoded successfully as RGB JPEGs.

## Frozen P25 locus consequence

The Phase65A row mapping was instantiated as:

- f100v `T.1–T.4` → `f100v.1–4`
- f100v `M.1–M.5` → `f100v.5–9`
- f100v `B.1–B.4` → `f100v.10–13`
- f102v2 `L2.1–L2.7` → `f102v2.10–16`
- f102v2 `L3.1–L3.5` → `f102v2.25–29`

The frozen Phase63B/65B confidence firewall excludes exactly one primary unit before any science:

- `L2.7 / f102v2.16`: source reading `to[d:?]?`, containing both an alternative reading and unreadable `?`.

Therefore the transcription-confidence population before crop-quality review is:

- f100v: `13/13` eligible;
- f102v2: `11/12` eligible (`L2=6`, `L3=5`);
- combined: `24/25` eligible.

This remains above the frozen coverage thresholds before crop review. No page pass/fail statistic has been computed.

## Anti-leak assertion

The successful manifest records all of the following as `false`:

- P25 visual↔text association computed;
- DINO embeddings computed;
- text distance computed;
- correlation computed;
- permutation statistic computed.

The workflow additionally asserted these flags after source retrieval.

> **SOURCE PREFLIGHT PASS: no P25 visual-text association, DINO embedding, text distance, correlation or permutation statistic was computed.**

## Next gate

The next operation is the text-blind crop freeze required by `PLAN_B.md`. Crop rectangles must be selected from the visible plant-fragment boundaries only, must exclude associated label glyphs, and may not be changed after any P25 association result is observed.
