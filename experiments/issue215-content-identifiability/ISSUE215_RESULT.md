# Issue #215 — page illustration-type identifiability gate

Parent: #172  
Stage: metadata-only identifiability gate  
Text/token/vocabulary feature access: **none**

## Decision

**`IDENTIFIABLE_FOR_HELDOUT_TEST`** under the thresholds frozen in Issue #215.

This licenses a separately preregistered inventory-composition test. It does **not** license choosing its textual feature representation after looking at content outcomes.

## Frozen source and execution

Page metadata source:

- repository: `noah-chelednik/voynich-data`
- commit: `472ef7366606a799fc8f1044c037e06b413f6ddd`
- path: `output/metadata/pages.jsonl`
- Git blob SHA-1: `f4ec667cd6b0e214eb755ccdc0c48d3d1c20d384`
- size: 112,121 bytes
- SHA-256: `cf4f60f1e2b2ace3789924d04765a83a005850a1dda3d7bfde6312931562ccf3`

Audit run:

- GitHub Actions run: `34233511565`
- scientific head: `25fa170651befc5b28ed637bf790aad462185a3b`
- artifact: `10058806692`
- artifact digest: `sha256:2d5be54e5b0e252ad6e9a2381d6dcb15b20a59fa53995aa915d74302576354e3`
- result JSON SHA-256: `8b80672300913b9cf238ffc98dbc30b9cfe1c16975c0f68f4981799fc1f8b18c`
- canonical result manifest SHA-256: `2076c324d8f2425ef21bdaaf9fd05dca29354965e0923070d601b0c3e193e5e3`

The workflow loaded only the pinned metadata JSONL. It did not load ZL3b token text, vocabulary, paragraph strings, image embeddings, or any content-association result.

## Gate counts

- all page records: **226**
- text-bearing records: **206**
- complete text-bearing records with illustration type + section + Currier + hand: **195**
- missing Currier among text-bearing pages: **11**
- unknown illustration-type codes: **0**

Complete cases by IVTFF `$I` illustration type:

| type | pages |
|---|---:|
| B | 19 |
| C | 2 |
| H | 127 |
| P | 16 |
| S | 25 |
| T | 6 |

Four classes have at least 8 complete pages.

There are 11 exact `(section, Currier, hand)` strata. Five contain at least two illustration types, with **106 pages** total. Mixed-stratum pages by illustration type:

- B: 19
- C: 2
- H: 63
- P: 16
- T: 6

Four illustration types contribute at least 4 pages in mixed strata. The mixed illustration↔stratum graph has a single connected component containing 5 illustration types and all 5 mixed strata.

All preregistered full-gate checks therefore pass.

## Important design warning discovered by the gate

The formal pass does **not** mean the full 195-page population is safely interpretable without conditioning.

Using the exact `(section, Currier, hand)` tuple alone and predicting the majority illustration type inside each tuple gives **92.3077% accuracy**. Illustration type is therefore still strongly confounded with the production metadata.

The five mixed strata are also highly uneven:

| section | Currier | hand | illustration counts |
|---|---|---|---|
| biological | B | 2 | B=19, T=1 |
| cosmological | B | 2 | C=2, T=3 |
| herbal_a | A | 1 | H=47, T=1 |
| herbal_b | B | 5 | H=6, T=1 |
| pharmaceutical | A | 1 | **H=10, P=16** |

Thus a later test must condition on the exact confounder stratum and must not present a naive manuscript-wide section/illustration classifier as content evidence.

## Prospectively useful stratum

Before any textual inventory feature was inspected, the metadata audit identifies one materially supported exact-confounder comparison:

**pharmaceutical / Currier A / Davis hand 1**

- 26 text-bearing pages
- H: 10 pages
- P: 16 pages
- 10 physical folios total
- H folios: `f87`, `f90`, `f93`, `f96`
- P folios: `f88`, `f89`, `f99`, `f100`, `f101`, `f102`

Within this stratum, section, Currier language and hand are fixed by construction. Each physical folio is also pure H or pure P in the pinned metadata, which permits folio-grouped validation/permutation without splitting recto/verso siblings across train/test.

This metadata fact is recorded now, before the first inventory-composition statistic, so a follow-up may freeze this exact 10-folio population without selecting pages from textual behavior.

## Interpretation

The gate answers only the design question:

> At least one externally labelled illustration contrast exists with enough within-confounder support to test page inventory composition without merely relearning section, Currier, or hand.

It does not show that text content differs by illustration type. It does not establish semantics or an image↔text causal relation.

The next step, if taken, must be a new issue that freezes the exact 10-folio H/P population, token/inventory representation, folio-grouped null/CV procedure, primary statistic, and stop rule before any text feature is computed.
