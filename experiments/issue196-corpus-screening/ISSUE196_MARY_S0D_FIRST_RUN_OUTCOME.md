# Issue #196 Mary Stuart / Castelnau S0-D — first-run outcome

Date: 2026-09-08  
Issue: #196  
PR: #197

## Frozen first-run classification

**`SOURCE_ACCESS_SCREEN_INDETERMINATE`**

No positive machine-readable Mary–Castelnau corpus/transcription/key/alignment candidate was found in this run, but the preregistered negative-screen sufficiency rule was not met because two discovery channels had transport failures.

No R5 score, ciphertext statistic, manuscript OCR, or Voynich data was accessed.

## First-run authority

- exact tested head: `b9c0165e1e8bc77b9b5d638a5ffe7ca506ee17be`
- Actions run: `34177645626`
- job: `101910140368`
- artifact: `issue196-mary-stuart-s0d`
- artifact ID: `10037813716`
- artifact ZIP SHA-256: `985c9cddf33af062e22c5264c5885605ea0a6ee2de3ae5264b510ea60dc9af45`
- raw `issue196_mary_s0d_results.json` SHA-256: `a8db15e10e1cbe7be977821a18f05e680a3b401c0e31e84ab0a9ead862aaf78a`

## Required channel status

| channel | success | result |
|---|---|---|
| pinned CTTS | yes | exact commit, no source-relevant data path |
| Crossref | yes | article DOI/title confirmed; only PDF similarity-checking link |
| GitHub GeorgeLasry discovery | no | 4/5 frozen code searches HTTP 429 |
| Zenodo discovery | no | exact DOI query HTTP 500; other two frozen queries succeeded |
| publisher HTML | no, optional | HTTP 403 |

The frozen negative classification required CTTS + Crossref + GitHub + Zenodo all to execute successfully. Therefore no negative source-access conclusion is licensed yet.

## CTTS findings

Pinned authority:

`CrypToolProject/CTTS@d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b`

- source-identifier path hits: `0`;
- bounded text hits: `2`;
  - README: states that CTTS was used to decipher the Mary Stuart letters and links the article;
  - `spanishKeep.txt`: unrelated ordinary Spanish prose containing the surname Castelnau.

Neither is machine-readable Mary–Castelnau corpus data under the preregistered data-like artifact rule.

## Crossref findings

DOI identity was stable and correct. Crossref exposes the publisher PDF as an `unspecified` content link intended for similarity checking. No dataset/transcription relation is present in the Crossref relation metadata.

## GitHub transport failure

Frozen queries against `user:GeorgeLasry`:

- `Castelnau` -> HTTP 429
- `"Mary Stuart"` -> HTTP 429
- `F38` -> HTTP 429
- `2988` -> HTTP 429
- `20506` -> HTTP 200, zero hits

This is a discovery-transport failure, not evidence that the four failed queries have no matches.

## Zenodo transport failure

Frozen queries:

- DOI `10.1080/01611194.2022.2160677` -> HTTP 500
- exact normalized article title -> HTTP 200, 25 returned records
- `Mary Castelnau cipher` -> HTTP 200, 25 returned records

The 50 successfully returned records were unrelated publications/data objects under the frozen source-role/data-like rule; no positive candidate was emitted. The failed DOI query prevents declaring the whole Zenodo channel successful under the original sufficiency rule.

## Publisher transport

Both automated full-article attempts returned HTTP 403. The publisher channel was explicitly optional in the preregistration and does not by itself affect negative-screen sufficiency.

## Consequence

Do **not** score R5 and do not call Mary–Castelnau publicly unavailable yet.

A single S0-D-R1 recovery is licensed only to repair the two failed discovery transports while preserving:

- the exact frozen source identifiers/search terms;
- the same public-source boundary;
- the same data-like artifact rule;
- the same positive-candidate semantics;
- no new host/category/corpus search.
