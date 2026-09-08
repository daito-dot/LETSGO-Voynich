# Issue #196 Mary Stuart / Castelnau S0-D-R1 — final source-access outcome

Date: 2026-09-08  
Issue: #196  
PR: #197

## Frozen classification

**`SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE`**

No public machine-readable Mary–Castelnau corpus/transcription/key/alignment artifact was located under the preregistered source boundary after the one licensed transport-only recovery.

No R5 score, ciphertext statistic, manuscript OCR, or Voynich data was accessed.

## Recovery authority

- exact tested head: `000fbfcfd7be17ac68e29a920ec75ac89790d659`
- Actions run: `34177943841`
- job: `101910988111`
- conclusion: `success`
- artifact: `issue196-mary-stuart-s0dr1`
- artifact ID: `10037900007`
- artifact ZIP SHA-256: `1f704041fe253cdf82b8875e5cfd19c26d32226d75c2079b27145e2c92e3b4ee`
- raw `issue196_mary_s0dr1_results.json` SHA-256: `7871f3514be17362f36699495ba7b4b728b5bfc0111f67cb9a6fffdbecf4ec26`

## Required channels

All four preregistered required channels succeeded in R1:

- pinned CTTS: `true`
- Crossref: `true`
- GeorgeLasry public GitHub repositories: `true`
- Zenodo: `true`

Positive candidates: `0`.

## GitHub recovery

The public owner-repository endpoint returned exactly two George Lasry repositories, and both current default branches were cloned and scanned exhaustively with the seven frozen identifiers:

- `GeorgeLasry/sigabajf` @ `bbf6b42f05d1b8b35067d1e8d4ada2929db1ff33`
- `GeorgeLasry/Sturgeon` @ `03819e287e1250a0df3cf90e81d5f7444f0f1b72`

Source-relevant path hits: `0`.

Two content hits occurred in Sturgeon for the frozen identifier `F38`, both inside unrelated encoded/test strings in Java source:

- `src/Depth.java`
- `src/Scenario.java`

They fail the frozen data-like artifact rule and are not Mary–Castelnau source candidates.

## CTTS

The pinned CTTS authority again produced only:

- README prose stating that CTTS was used for the Mary Stuart work;
- unrelated Spanish corpus prose containing the surname Castelnau.

No data-bearing source path was found.

## Crossref

The DOI identity is stable. Crossref exposes only the publisher PDF link and no dataset relation.

## Zenodo recovery

The only failing first-run query, exact DOI `10.1080/01611194.2022.2160677`, returned HTTP 500 on all three frozen plain retries but succeeded with the preregistered exact-phrase fallback. The other two frozen identifiers succeeded on their first plain requests.

- DOI: `500, 500, 500, quoted -> 200`
- exact article title: `200`
- `Mary Castelnau cipher`: `200`

The combined returned records contained no artifact passing the unchanged Mary–Castelnau source-role/data-like rule.

## Interpretation boundary

This does **not** imply that the authors' CTTS transcription/key database no longer exists, nor that a private or author-supplied copy could not support a clean attribution experiment. It establishes that the scholarly working dataset is not reproducibly available through the prospectively frozen public channels used by this program.

Per the S0-D stop rule, no author contact, private share, manual image transcription, OCR, or expanded post-reveal web search is used as a rescue.

## Consequence

Stop the Mary Stuart / Castelnau lane for the main Priority-3 source-attribution program. Move to the preregistered DECRYPT/HistoCrypt shared-task paired-source screen, still score-free and still requiring all five preservation layers before any R5 computation.
