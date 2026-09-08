# Issue #199 — DECODE Record 1564 acquisition correction outcome

Date: 2026-09-08  
Refs: #199 #194 #196 #172

## Result

**Acquisition status: `DECODE_FILESRV_TRANSPORT_UNRESOLVED`.**

The correction probe confirms that Issue #194 fixed authority at the wrong layer when it treated the three visible `filesrv/?file=...txt` leaf hrefs as self-sufficient downloadable document authorities.

Starting instead from the live Record 1564 page, the probe:

1. fetched the public record page first;
2. extracted the current visible `Transcription [transc]`, `key_CT2 [key]`, and `decryption_CT2 [dec]` hrefs from that HTML;
3. established a cookie jar and record-page Referer;
4. tested cold GET, session GET, and browser-navigation-style GET twice each.

All nine request classes returned the same response:

- HTTP 200;
- `Content-Type: image/png`;
- `Content-Disposition: inline; filename="forbidden.png"`;
- 17,947 bytes;
- PNG dimensions 986 × 568;
- SHA-256 `1e47167c4db694fe06f61f4c5650ac54eff2ce3ee2eff9dea78c7f15aa55b606`.

Therefore the identical payload observed in #194 was not a transcription/key/decryption payload. It was the site's explicit forbidden response image.

## Authority

First correction run:

- workflow run: `34179251164`
- job: `101914775076`
- tested head: `f56245faecb79a1ade79e70c997d6a1679a0fb84`
- result JSON SHA-256: `10e73ff31fec418e8303accc8eb1b4ec7d79142c59ba930b8a1d5df99d729a92`
- artifact: `10038307432`
- artifact ZIP SHA-256: `b988edc6316112a1c469588d2d31a2e47e498eaa98036e988ba2f21c1ae8ac76`

No R5 statistic, Voynich statistic, or cipher-content score was computed.

## Correction to interpretation

The valid statement from #194 is:

> the exact unauthenticated/direct DECODE document transport used there did not retrieve the three public document payloads.

The invalid stronger statement is:

> Ramanacoil itself is non-composable or permanently unavailable for Priority 3.

Accordingly, Ramanacoil should remain **unresolved / acquisition-blocked**, not scientifically rejected. The #196 corpus screening may retain Dee as an independently promising candidate, but must not treat #194 as evidence that Ramanacoil has been eliminated on preservation/composability grounds.

## Next acquisition rule

Do not guess query parameters or bypass site controls. A future Ramanacoil attempt must use an externally documented access route, e.g. an official DECODE/DECRYPT API, export mechanism, public corpus release, or author-provided transcription/key/decryption package. Only after the actual three payloads are reproducibly obtained should a fresh score-free structural Gate 0 be run.
