# Issue #196 — HCPortal S0-C solved-text detail inspection

Date: 2026-09-08  
Status: **FROZEN BEFORE DETAIL ENDPOINT / TEXT-CONTENT INSPECTION — SCORE-FREE**

## Trigger

S0-B revealed exactly 562 `pc_hcp_` postcards, with self-describing solution labels `Solved` (11) and `Not solved` (551). No postcard has a paired `cipher_key_id`. Four records have a nonempty text attachment, and all four are in the `Solved` class. Their text item title is `Solution` in the S0-B metadata.

## Frozen S0-C population

Inspect **all and only** records satisfying the metadata predicate frozen from S0-B:

- `name` matches `^pc_hcp_[0-9]+$`;
- `solution.name == "Solved"` exactly;
- at least one nonempty `datagroups[].data[].text` attachment exists.

S0-B fixed the complete membership of this intersection as:

- `1324 / pc_hcp_5`
- `1473 / pc_hcp_154`
- `1510 / pc_hcp_191`
- `1789 / pc_hcp_470`

No ranking, favorable item choice, or R5-dependent selection is allowed.

## Frozen source access

For each ID, double-fetch:

`https://api.hcportal.eu/api/cryptograms/{id}`

Require byte identity within record. Do not fetch attachment links (S0-B found none) or image URLs. Image pixels remain outside S0-C.

## Allowed content inspection

S0-C may inspect the four detail JSON records to decide whether the five preservation layers are actually machine-readable. It may inspect:

- top-level field names and scalar metadata;
- `description`, `note`, and attachment text only for source-role identification;
- data-group descriptions and item `type/title`;
- whether any machine-readable field is an explicit ciphertext transcription, solution/plaintext, cipher key, mapping, lineation, or alignment;
- text byte count, line count, whitespace/newline structure, Unicode class summary, and bounded first/last 120 escaped characters for source-role audit;
- image/link metadata without downloading targets.

It must not compute symbol frequencies, adjacency, terminal/initial statistics, language-model scores, R5 gains, or Voynich comparisons.

## Five-layer definitions for this transport

1. `CIPHERTEXT_SYMBOLS = true` only if an explicit machine-readable ciphertext/transcription field or attachment is present. Images alone do not pass.
2. `PHYSICAL_LINES = true` only if that machine-readable ciphertext representation preserves at least two source lines, or a separately supplied external lineation field deterministically maps the transcription to source lines. Image layout alone does not pass.
3. `CIPHER_UNIT_BOUNDARIES = true` only if that ciphertext representation contains an explicit grouping channel coarser than atoms and not inferred from plaintext or image inspection.
4. `PLAINTEXT_LEXICAL_BOUNDARIES = true` if an explicit solution/plaintext text is present with at least two whitespace-separated alphabetic runs; no language correction is used.
5. `CIPHER_PLAINTEXT_ALIGNMENT = true` only if a supplied key/mapping/aligned transcription makes correspondence deterministic. `solution.name="Solved"` alone does not pass, and a plaintext solution next to an untranscribed image does not pass.

## Frozen outcome classes

- `ADMIT_FOR_PROSPECTIVE_R5_GATE0` only if at least one of the four records has all five layers externally present in the current reproducible API transport.
- `HCPORTAL_POSTCARDS_NO_MACHINE_READABLE_CIPHERTEXT` if none of the four has layer 1.
- `HCPORTAL_POSTCARDS_ALIGNMENT_INSUFFICIENT` if machine-readable ciphertext exists but no record has deterministic layer 5.
- `HCPORTAL_POSTCARDS_OTHER_LAYER_FAILURE` for another five-layer failure.
- `INVALID_TRANSPORT` for unstable/unreadable detail responses.

If more than one record passes all five, S0-C lists all passers; a later Gate-0 selection rule must be frozen separately. S0-C itself does not choose by R5 behavior.

## Consequence

Any non-admission outcome stops HCPortal postcards for the main Priority-3 lane and moves screening to the Mary Stuart/Castelnau source-access question. No OCR, manual image transcription, key reconstruction, or plaintext-to-image alignment is licensed as repair.
