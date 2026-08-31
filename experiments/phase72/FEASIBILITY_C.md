# Phase 72C — DECODE document/transcription surface discovery

Status: **SOURCE DISCOVERY ONLY — NO VOYNICH SCORE AUTHORIZED**

Date: 2026-08-31

## Motivation

Phase72A established that DECODE contains thousands of historical cipher records, but its public `/view/records/{id}` response does not expose transcription bodies for the ten non-private records in the 1400–1600 window. Phase72B established that the open benchmark subset has rich page transcriptions but not a valid two-source population of independently established message entries.

Before abandoning DECODE as a source of real message-level ciphertext, Phase72C audits the **public document/file surface** of the same external database.

No Voynich statistic is computed.

## Independent probes

The audit uses two source-only probe sets:

1. DECODE record IDs `1205` and `1206`, independently cited in the published study *Deciphering three diplomatic letters sent by Maximilian II in 1575* as DECODE records containing the historical cipher material/plaintext documents;
2. the ten objectively retained non-private 1400–1600 Cipher records from Phase72A: `939, 338, 347, 358, 344, 331, 1491, 1819, 345, 1379`.

The first set is a source-interface positive probe. It is not selected for Voynich similarity.

## Public API surface to audit

Pinned public Swagger authority exposes generic endpoints:

- `/api/list/{table}`
- `/api/view/{table}/{key}`
- `/api/file/{table}/{field}/{key}`
- `/api/file/{table}/{fn}`
- `/api/export/{type}/{table}/{key}`

The source audit may try a fixed list of plausible document tables before inspecting responses:

- `documents`
- `document`
- `record_documents`
- `recorddocuments`
- `document_types`
- `documenttypes`
- `files`

For each successful endpoint it may record only:

- HTTP status/content type;
- top-level JSON keys;
- first-record field names/types;
- IDs and foreign-key-looking fields;
- text/file field names and lengths/hashes;
- whether any object references the probe record IDs.

It may query `/view/{table}/{id}` only for IDs discovered from successful list responses or directly from record-detail foreign keys.

## Firewall

Phase72C may not:

- calculate S1/S2/S3/H62;
- compare any discovered transcription with Voynich;
- select records by Voynich similarity;
- alter the historical probes after inspecting Voynich outcomes;
- infer a Voynich cipher family.

## Feasibility result

Classify:

- `P72-DECODE-DOC READY` if the unauthenticated public API exposes machine-readable ciphertext transcriptions for at least one published real historical cipher probe and preserves source-native line/document boundaries;
- `P72-DECODE-DOC METADATA-ONLY` if document tables exist but no transcription body/file is publicly retrievable;
- `P72-DECODE-DOC BLOCKED` if document/file surfaces require authentication or cannot be joined to records from the public API.

This classification is source availability only. A READY result still requires a separately frozen population/statistic before any Voynich comparison.
