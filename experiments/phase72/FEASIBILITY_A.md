# Phase 72A — real historical ciphertext feasibility audit

Status: **NO VOYNICH SCIENTIFIC SCORE AUTHORIZED**

Date: 2026-08-31

## Pre-science source-schema amendment

The first source-only audit parsed **7,959** DECODE records but returned zero candidates because the pinned Decode2LOD RDF snapshot stores controlled vocabulary fields as numeric IDs rather than display labels: for example `hasRecordType` is predominantly `"1"` / `"2"`, not the strings `Key` / `Cipher`. No Voynich score was computed in that run (`scientific_metrics_called=false`).

Before any scientific score, the source parser is therefore corrected at the interface layer only:

- DECODE web record `4417` and other independently displayed cipher records establish record-type ID **`2 = Cipher`**;
- DECODE web record `205` and `1439` independently display **Key**, establishing **`1 = Key`**;
- Phase72 keeps only record-type ID `2` (or a literal display value containing `cipher/crypt` if a future compatible snapshot exposes labels);
- the 1400–1600 date window and privacy criterion are unchanged;
- all corrected candidates must still be reported, and no candidate is ranked or chosen using Voynich outcomes.

The original zero-candidate result is retained as a source-schema compatibility failure, **not** as `P72-EXT UNDERPOWERED`. Correcting a controlled-value decoding mismatch is allowed because Phase72A is explicitly a no-score source audit and no Voynich statistic has been revealed.

## Why this frontier

Phase69–70 showed that meaningful plaintext can carry much of the Voynich short-range recurrence structure under a reversible surface encoder. Phase71 then showed that one explicit near-period Alberti message-initial reset/signal mechanism does not reproduce the Voynich paragraph-entry S1 direction; the primary S1 projection is opposite-signed in 5/5 folds.

The next question should therefore use **real historical ciphertext practice**, not another target-shaped synthetic encoder.

Phase72A is only a feasibility/source audit:

> Does the public DECODE/DECRYPT collection contain enough independently dated, machine-readable historical ciphertexts with usable message/line boundaries to support a prospective external test of the Voynich paragraph-entry statistic?

No Voynich S1/S2/S3/H62 value may be computed in this phase.

## Independent source authorities

Primary metadata snapshot:

- `Glottocrisio/Decode2LOD@1ab5dac5da1fbb65b3b851b31e21f2257f715c6d`
- `populated_decryptontology.ttl` Git blob `943f1f4896ad004e5292a8348737706f09c9b729`

The Decode2LOD implementation documents the public DECODE REST API base:

`https://de-crypt.org/decrypt-web/api`

and endpoints:

- `/list/records`
- `/view/records/{record_id}`

DECODE is an external historical-cipher collection maintained by the DECRYPT project. The database papers describe ciphertexts, keys, transcriptions, decryptions/cleartext and metadata as separate collection fields.

## Metadata-first rule

The candidate historical population must be formed without inspecting any Voynich score.

Initial feasibility window is deliberately broad:

- `start_year` from **1400 through 1600 inclusive**;
- record type = decoded DECODE **Cipher** controlled value (`2` in the pinned RDF snapshot), or an equivalent literal `cipher/crypt` display label;
- key-only records are excluded;
- public/non-private record where metadata exposes the flag.

The audit must report all matching records, not hand-pick attractive examples.

## What the audit may inspect

For every metadata-matching record, Phase72A may inspect external-source metadata and DECODE record detail only to determine:

- record ID/name/year/country/city/holder;
- record type;
- cipher-family metadata;
- symbol-set metadata;
- number of pages;
- public/private status;
- status/decryption metadata;
- presence and machine-readable size/shape of transcription or cleartext fields;
- presence of line/page/message structure in the external transcription;
- source links/record links.

The audit may record field names, scalar metadata, text lengths and hashes. It may archive full external record-detail JSON as a source artifact because this is independent of Voynich outcomes.

## What the audit may not do

Before a later `PLAN_B.md` freezes a prospective real-cipher population and statistic, Phase72A may not:

- compute S1, S2, S3 or H62 on any external ciphertext;
- compare any historical ciphertext representation with Voynich;
- rank records by Voynich similarity;
- choose cipher families because they appear Voynich-like;
- alter date/family/source filters after seeing a Voynich score;
- infer a Voynich cipher or plaintext.

## Feasibility success criterion

Classify `P72-EXT READY` only if the objective external audit identifies at least:

- **10** public historical ciphertext records in the 1400–1600 window;
- spanning at least **2** independently identified cipher-family/source groups or archives;
- with machine-readable ciphertext transcription;
- and at least **5** records with enough explicit source structure to define a message entry plus internal pseudo-entry control without manually inventing boundaries.

If the database has machine-readable ciphertext but not reliable boundaries, classify `P72-EXT TRANSCRIPTION READY / BOUNDARY BLOCKED`.

If fewer than 10 usable transcribed records exist after the corrected source schema, classify `P72-EXT UNDERPOWERED`.

These are source-availability classifications only, not scientific results about Voynich.

## Next-stage firewall

If feasibility is successful, `PLAN_B.md` must freeze, **before any external-cipher S1 computation**:

1. exact record IDs and source hashes;
2. exact transcription parser;
3. exact boundary definition;
4. inclusion/exclusion rules;
5. unit representation for historical cipher symbols;
6. control stratification by record/cipher family/date if required;
7. primary statistic and multiplicity correction;
8. pass/fail thresholds.

Only after that freeze may a real historical ciphertext S1 comparison be revealed.
