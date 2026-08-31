# Phase 72B — open real-historical-cipher benchmark feasibility

Status: **NO VOYNICH SCIENTIFIC SCORE AUTHORIZED**

Date: 2026-08-31

## Pre-science source-path amendment

The first Phase72B source-only audit parsed all **905** manifest records but reported zero usable transcriptions because manifest paths such as `sources/copiale/transcriptions/...` are relative to the repository's `benchmark/` directory, not the repository root. The run recorded 102 declared transcription paths as missing, with the path prefix mismatch visible directly in the audit. No Voynich score was computed (`scientific_metrics_called=false`).

Before any scientific score, path resolution is therefore corrected deterministically:

1. if `<repo>/<declared_path>` exists, use it;
2. otherwise use `<repo>/benchmark/<declared_path>`;
3. if neither exists, retain the record in the missing-path audit.

No record/date/source/rights/eligibility criterion changes. The first zero-record result is retained as a source-interface compatibility failure, not as evidence that the benchmark is genuinely underpowered.

## Why a second source audit is necessary

Phase72A's corrected DECODE audit found 2,267 cipher records dated 1400–1600 in the pinned metadata snapshot, but **2,257 are explicitly marked private ciphertext**. Only ten records satisfy the frozen non-private filter, and their public record-detail responses expose metadata only, not machine-readable ciphertext transcription. The public unauthenticated DECODE surface is therefore underpowered for the intended real-cipher boundary test.

This is a source-availability result, not a Voynich result. No S1/S2/S3/H62 score has been computed in Phase72.

Phase72B audits a different independently curated source: the public `matthewdgreen/cipher_benchmark` repository, whose manifest explicitly distinguishes historical vs synthetic records and points to canonical diplomatic transcriptions where redistribution is permitted.

## Pinned source authority

- repository: `matthewdgreen/cipher_benchmark`
- commit: `729aad62d12483c549e64a2541d4f9255538c8cf`
- manifest: `benchmark/manifest/records.jsonl`
- manifest Git blob: `9dfedda0597185eda64e8166535fa1d0aa0898f5`
- schema Git blob: `f07533cce267bb17110c8a3327385d7e586eee20`

The schema explicitly exposes:

- source/source_record_id;
- historical date range;
- `synthetic` flag;
- rights class;
- cipher family;
- diplomatic/canonical transcription path;
- original manuscript page;
- word-boundary status.

## Objective feasibility population

Audit **all** manifest records satisfying:

1. `synthetic` is false or absent/false;
2. `rights_class == "open"`;
3. a canonical or diplomatic transcription file is declared;
4. the declared transcription file exists under the deterministic repository/`benchmark/` path rule above;
5. the record has a historical upper date bound at or before **1900** when a parseable bound is present.

The broad 1900 cutoff is a source-feasibility screen only. No later scientific population may be chosen by Voynich similarity.

The audit must report every passing record grouped by external `source` and `source_record_id`.

## Boundary feasibility

The intended later statistic needs a source-native entry plus internal comparison positions. Phase72B therefore records, without scoring:

- number of nonempty transcription lines;
- whitespace-token counts per line;
- whether the manifest says word boundaries are preserved;
- manuscript-page identifier;
- number of pages/records sharing the same `source_record_id`;
- whether the record is objectively the first page in its source-record group under manifest/page order;
- whether the first page has at least three nonempty lines and at least five whitespace tokens in line 1 and line 3;
- whether at least one internal `j -> j+2` comparison with the same line-token eligibility exists.

These checks mirror only the **availability requirements** of the existing entry statistic; they do not calculate a Voynich direction or any S1 score.

## Feasibility classes

`P72-BENCH READY` requires:

- at least **20** historical first-page/source-record entries with canonical/diplomatic transcription;
- at least **2** independent source collections;
- at least **10** entries satisfying the frozen line/token eligibility shape;
- at least **2** source collections contributing eligible entries.

If >=20 historical entries exist but fewer than 10 satisfy line/token shape, classify:

`P72-BENCH TEXT READY / ENTRY-SHAPE BLOCKED`.

If fewer than 20 historical first-page/source-record entries exist after the corrected path rule, classify:

`P72-BENCH UNDERPOWERED`.

## Firewall

No Phase72B code may import the Voynich scorer or compute S1/S2/S3/H62.

If `P72-BENCH READY`, a later `PLAN_C.md` must freeze **before any real-cipher vs Voynich score**:

1. exact record IDs;
2. exact source-record entry rule;
3. exact transcription choice (canonical vs diplomatic);
4. exact symbol/token representation;
5. exact handling of line breaks and word boundaries;
6. source-stratified null/control if required;
7. primary statistic and pass/fail rule;
8. multiplicity correction for any source-family arms.
