# Issue #196 HCPortal S0-A — record 1454 outcome

Date: 2026-09-08  
Issue: #196  
PR: #197

## Scope

Score-free source/schema inspection only. No R5, adjacency, transition, or Voynich statistic was computed.

## Authority

- publication-fixed record: HCPortal ID `1454`, `pc_hcp_135`
- endpoint: `https://api.hcportal.eu/api/cryptograms/1454`
- exact tested head: `c3d7c359e1f96be9cb773202994f18a5b9256af6`
- Actions run: `34176958887`
- job: `101908161621`
- conclusion: `success`
- artifact: `issue196-hcportal-s0a`
- artifact ID: `10037577592`
- artifact ZIP SHA-256: `305cad14d4c21cfa9b42df6f2a1e08cf006f1ff08e09b719dd56af1779e874b9`
- raw result SHA-256: `dc6554b1dee716ef8a6416e953f2cb4672d40f2412b2c5016de99fdc4bd8820b`

The endpoint was fetched twice in the same run. Both payloads were byte-identical:

- bytes: `1962`
- SHA-256: `686a4b2a6e648015fb4d937f65e184777ec496bf96bef031df9d89489d3f5e2b`

## Structural result

Record metadata:

- ID/name: `1454 / pc_hcp_135`
- date: `1907-12-09`
- category: `Substitution`
- availability metadata: `Private collection`
- `cipher_key_id = null`
- top-level `solution` exists but is a two-field object (`id`, `name`), i.e. a structured solution/status field rather than plaintext content.

Attachments:

- one data group, `Cryptogram`;
- two attachment items;
- both are images (`Picture side`, `Address side`);
- zero inline text items;
- zero link items;
- original image URLs are served from `api.hcportal.eu/media/...`.

Therefore record 1454 itself does not expose the five layers needed for a clean R5 source-attribution experiment through its current structured API record. In particular it supplies no paired key and no machine-readable transcription/plaintext attachment.

## Decision

S0-A classification remains `NEEDS_SCORE_FREE_SOURCE_INSPECTION`, but **record 1454 is not an admissible R5 corpus item on its own**.

The API transport is reproducibly available and the record schema contains structured `solution`, `cipher_key_id`, and attachment data. Per the frozen plan, the next licensed step is a **population metadata/schema audit of the HCPortal postcard collection** before viewing/selecting additional record contents.

The population audit must use only preservation metadata and may not select records by ciphertext behavior.
