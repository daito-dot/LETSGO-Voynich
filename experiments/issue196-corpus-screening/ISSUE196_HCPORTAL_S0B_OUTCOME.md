# Issue #196 HCPortal S0-B — postcard population metadata outcome

Date: 2026-09-08  
Issue: #196  
PR: #197

## Scope

Score-free population metadata audit only. No attachment target, image pixel, ciphertext/plaintext content, R5 statistic, or Voynich data was accessed.

## First-reveal authority

- exact tested head: `9602e752253d60aa15618c29019fe0291fb9fc6f`
- Actions run: `34177152439`
- job: `101908722753`
- conclusion: `success`
- artifact: `issue196-hcportal-s0b`
- artifact ID: `10037660695`
- artifact ZIP SHA-256: `0aebfd85aaee0502c292fc16492bbc3f39591286e38e6517dc70980ace80df5d`
- raw `issue196_hcportal_s0b_results.json` SHA-256: `16a6714cfaaef4248788d58ff9c12fcc124a7c5fd881d96598d4ccd8455c5840`

## Frozen population result

The public HCPortal list transport was reproducibly paginated and double-fetched under the preregistered audit.

- public cryptograms received: `1,875`
- API-reported total: `1,875`
- exact `^pc_hcp_[0-9]+$` postcard population: `562`
- `solution.name = Not solved`: `551`
- `solution.name = Solved`: `11`
- records with non-null `cipher_key_id`: `0`
- records with image attachment: `562`
- records with text attachment: `4`
- records with link attachment: `0`

All four text-attachment records carry the self-describing `Solved` label. They are the complete preregistered `Solved x text/link` intersection:

| id | name | text title | text bytes | text lines | paired key |
|---:|---|---|---:|---:|---|
| 1324 | `pc_hcp_5` | `Solution` | 133 | 1 | no |
| 1473 | `pc_hcp_154` | `Solution` | 53 | 1 | no |
| 1510 | `pc_hcp_191` | `Solution` | 113 | 1 | no |
| 1789 | `pc_hcp_470` | `Solution` | 13 | 1 | no |

Every postcard has the `Cryptogram` data group with image items. Only these four add a `Transcriptions and solutions` group, and within the metadata exposed by S0-B each added machine-readable item is titled `Solution`; no machine-readable `Transcription` item appeared in the population metadata.

## S0-B classification

**`POPULATION_HAS_COMPOSABILITY_METADATA_CANDIDATES`**

This label follows the preregistered S0-B rule because nonempty text attachments exist. It is deliberately not a five-layer admission.

The metadata already makes the principal limitation visible: all 562 postcards have `cipher_key_id = null`, and the only four machine-readable text attachments are labeled `Solution`. A final score-free S0-C detail/schema inspection of all four predeclared records is nevertheless required before closing the HCPortal lane, because S0-B did not inspect detail endpoints or text content.
