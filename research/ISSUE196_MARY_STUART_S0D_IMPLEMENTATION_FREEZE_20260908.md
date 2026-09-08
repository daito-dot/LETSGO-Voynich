# Issue #196 Mary Stuart S0-D — implementation freeze clarification

Date: 2026-09-08  
Status: **FROZEN BEFORE LOCATOR EXECUTABLE**

The following exact implementation rules are fixed before S0-D runs.

## Negative-screen sufficiency

`SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE` may be emitted only if all four channels below execute successfully:

1. pinned local CTTS tree/content audit;
2. Crossref DOI metadata retrieval;
3. Zenodo public API discovery;
4. GitHub public-code discovery across George Lasry's public repositories.

Publisher HTML access is useful but optional because automated publisher access may be blocked even when the open-access article is human-readable. Publisher failure is reported and does not by itself force `SOURCE_ACCESS_SCREEN_INDETERMINATE`.

If any of the four required channels fails, and no positive data artifact is independently located, emit `SOURCE_ACCESS_SCREEN_INDETERMINATE`.

## Data-like artifact rule

A candidate machine-readable corpus artifact must have a filename/path or explicit metadata role matching the Mary/Castelnau source identifiers and be data-like rather than article/image/software material.

Data-like extensions are frozen to:

- `.txt`, `.csv`, `.tsv`, `.json`, `.xml`, `.tei`, `.zip`, `.tar`, `.gz`, `.7z`, `.ctts`, `.dat`

Explicit role terms are:

- `transcription`, `transcript`, `ciphertext`, `cipher text`, `corpus`, `dataset`, `data`, `key`, `nomenclator`, `alignment`, `aligned`, `CTTS project`.

Excluded even when source terms are present:

- `.pdf`, `.html`, `.htm`, `.epub`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.tif`, `.tiff`, `.svg`;
- README/documentation prose;
- software source/binaries whose role is CTTS itself rather than Mary–Castelnau data;
- generic manuscript image/IIIF links;
- article/reference links.

A `.zip`/archive is only positive if its surrounding title/path/metadata explicitly identifies Mary–Castelnau corpus/transcription/key/alignment data; a generic software release archive is excluded.

## GitHub discovery

The pinned CTTS repository is audited locally and therefore does not require remote code search.

Remote GitHub code discovery is limited to `user:GeorgeLasry` and exactly these queries:

- `Castelnau`
- `"Mary Stuart"`
- `F38`
- `2988`
- `20506`

A code-search API hit is archived by repository/path/URL only plus bounded text-match context. It becomes a positive candidate only under the data-like artifact rule above.

## Zenodo discovery

Run exact public API searches for:

- the DOI `10.1080/01611194.2022.2160677`;
- exact normalized article title;
- `Mary Castelnau cipher`.

Archive returned record IDs, titles, DOI, resource type, and file names/links metadata. A paper-only record does not count.
