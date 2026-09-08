# Issue #199 — DECODE Record 1564 acquisition correction

Date: 2026-09-08  
Parent: #194 / #196 / #172  
Base: `51722602e892bb03fa0c733547a10368a48041b1`  
Status: **SCORE-FREE TRANSPORT DIAGNOSTIC**

## Correction being tested

Issue #194 correctly recorded that its three frozen leaf URLs returned the same 17,947-byte PNG payload. It did **not** establish that DECODE's public Transcription, key_CT2, and decryption_CT2 documents are themselves identical or unavailable.

The acquisition mistake under test is that #194 treated the `filesrv/?file=...` href as a context-free file endpoint. The current record page must instead be the acquisition root of authority: establish the page/session, extract the current document hrefs from that page, then follow them as a browser navigation would.

## Probe only

The probe compares cold direct GET with record-page-session GET and browser-navigation GET. It records transport metadata and signatures only. No document content is scientifically parsed. No R5 or Voynich data is touched.

A successful textual route invalidates only the **acquisition stop** in #194; it does not automatically make Ramanacoil R5-composable. A new score-free structural Gate0 would still be required.

If no justified route yields the documents, the correct outcome is `DECODE_FILESRV_TRANSPORT_UNRESOLVED`, not `Ramanacoil non-composable`.
