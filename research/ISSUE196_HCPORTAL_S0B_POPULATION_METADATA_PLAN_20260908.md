# Issue #196 — HCPortal S0-B population metadata audit

Date: 2026-09-08  
Status: **FROZEN BEFORE HCPORTAL LIST PAYLOAD REVEAL / SCORE-FREE**

## Trigger

S0-A showed that publication-fixed `pc_hcp_135` / record 1454 is reproducibly accessible through the public HCPortal API, but exposes only two images, no `cipher_key_id`, and no inline/link transcription or plaintext. The schema nevertheless exposes structured `solution`, `cipher_key_id`, and `datagroups`, so a population-level preservation audit is licensed before inspecting any additional record contents.

## Question

Does the HCPortal cryptographic-postcard population contain a metadata-defined subpopulation with enough **externally recorded source assets** to justify detailed five-layer Gate-0 inspection?

No ciphertext, image pixels, transcription text, plaintext text, or R5 statistic is inspected in S0-B.

## Frozen population identity

Retrieve the current public cryptogram list from:

`https://api.hcportal.eu/api/cryptograms?detailed=1&per_page=100&page={page}`

Use every paginated public record returned by the API. The postcard population is fixed as records whose `name` matches exactly:

`^pc_hcp_[0-9]+$`

This identity is fixed from HCPortal's published naming convention and the HistoCrypt-2026-cited `pc_hcp_135`, before the population list is inspected.

Do not subset by ciphertext appearance, symbol statistics, language, date, or expected R5 behavior.

## Transport audit

- Fetch page 1 twice and require byte identity before trusting pagination metadata.
- Read `last_page` / equivalent paginator metadata from the returned JSON; abort rather than invent a page count if pagination cannot be determined.
- Fetch every page `1..last_page` twice with the exact same URL parameters and require byte identity per page.
- Cap at 100 pages as an implementation safety bound. Hitting the cap is `INVALID_TRANSPORT` rather than silent truncation.
- Archive page URL, bytes, SHA-256, current/last-page metadata, and record count only; raw population payloads are Actions-ephemeral and are not committed to the repository.

## Allowed metadata fields

For each `pc_hcp_` record S0-B may inspect and aggregate only:

- `id`, `name`;
- category/subcategory names;
- date, language, availability metadata;
- `state.id/title/show`;
- `solution.id/name` **as a status/label only**;
- whether `cipher_key_id` is null/non-null, plus the ID for future source lookup;
- `datagroups[].description`;
- each data item's `type`, `title`;
- whether each item has a non-empty `text`, `link`, or `image` field;
- host/path metadata for links/images, without fetching the target;
- field-name/schema summaries.

S0-B must not archive attachment text itself. For a non-empty text field it may record only UTF-8 byte count, line count, whitespace/newline flags, and SHA-256.

## Required outputs

Report:

1. total public cryptograms;
2. total `pc_hcp_` postcard records;
3. distribution of `solution.name` values;
4. count and share with non-null paired `cipher_key_id`;
5. counts with image/text/link attachment fields;
6. distributions of data-group descriptions and item `type`/`title`;
7. intersections, without interpreting them as sufficient:
   - paired key × any text attachment;
   - paired key × any link attachment;
   - each solution-label value × paired key;
   - each solution-label value × text/link attachment;
   - each solution-label value × paired key × text/link attachment.
8. IDs/names of records in each nonempty **metadata intersection** only if the intersection rule above was fixed before reveal. S0-B may list the full membership of those predeclared intersections; it may not rank them.

## No positive solution label is frozen yet

The exact vocabulary of `solution.name` has not been inspected. S0-B therefore reports every label verbatim and symmetrically. It does **not** decide which label means solved.

After S0-B reveal, a later S0-C plan may use the self-describing label semantics, but that filter must be committed before any candidate record detail endpoint is fetched.

## Decision

- If no postcard has either a paired key or a text/link attachment, HCPortal postcard population is `SOURCE_METADATA_INSUFFICIENT` for Priority 3 and screening moves to Mary Stuart.
- If potentially useful intersections exist, classify `POPULATION_HAS_COMPOSABILITY_METADATA_CANDIDATES` and freeze S0-C selection using only revealed metadata labels before fetching any candidate details.
- S0-B never emits `ADMIT_FOR_PROSPECTIVE_R5_GATE0`; only a later detailed five-layer inspection may do that.

## Firewall

No attachment download. No image inspection. No ciphertext/text content. No token counts derived from content. No terminal/initial statistic. No R5. No Voynich access. No ranking by cipher behavior.
