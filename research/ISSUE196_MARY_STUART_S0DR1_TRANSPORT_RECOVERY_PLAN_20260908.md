# Issue #196 — Mary Stuart / Castelnau S0-D-R1 transport-only recovery

Date: 2026-09-08  
Status: **FROZEN AFTER S0-D TRANSPORT FAILURE / BEFORE RECOVERY EXECUTION**

## Why one recovery is licensed

S0-D produced `SOURCE_ACCESS_SCREEN_INDETERMINATE`, not a scientific/source-access negative.

The only preregistered required-channel failures were transport failures:

- GitHub public code search: four of five exact `user:GeorgeLasry` queries returned HTTP 429; the fifth returned HTTP 200 with zero hits.
- Zenodo: the exact DOI query returned HTTP 500; the exact-title and `Mary Castelnau cipher` queries both returned HTTP 200 and no positive source-role artifact.

Pinned CTTS and Crossref both succeeded. Publisher HTML returned HTTP 403 but was explicitly optional.

S0-D-R1 may repair **only those two failed transports**. It may not change source identifiers, positive-candidate semantics, data-like extensions, public-source boundary, or R5/source-preservation criteria.

## Frozen GitHub recovery

Replace rate-limited GitHub code-search transport with exhaustive local inspection of George Lasry's currently public GitHub repositories.

### Repository population

Retrieve through the public GitHub REST API:

`GET https://api.github.com/users/GeorgeLasry/repos?type=owner&sort=full_name&direction=asc&per_page=100&page={p}`

- follow pages until a page returns fewer than 100 records;
- maximum 5 pages / 500 repositories; exceeding the cap is a transport failure;
- include every returned public repository, including archived repositories and forks if the endpoint returns them;
- no repository is selected or excluded by name/content;
- archive repository full name, fork flag, archived flag, default branch, and current default-branch head commit used for inspection.

This preserves the original frozen source boundary `user:GeorgeLasry` while avoiding the code-search endpoint. Searching a superset of owned public repository files can only make the locator more conservative against a false negative; it cannot create an R5-favorable selection because no R5 statistic is accessed.

### Checkout/scan

For every listed repository:

- clone the current default branch with `git clone --depth 1 --single-branch`;
- failure to clone any listed repository makes the GitHub recovery channel unsuccessful rather than silently skipping it;
- record `git rev-parse HEAD`;
- scan path names and text-like files up to 2 MB for **exactly the already-frozen identifiers**:
  - `Mary Stuart`
  - `Castelnau`
  - `Mary-Castelnau`
  - `F38`
  - `fr. 2988`
  - `2988 f.38`
  - `20506`
- matching is case-insensitive, with no stemming, synonym expansion, approximate matching, or new identifier;
- archive file path, matched frozen identifier, and at most 240 characters of context.

A hit is a positive candidate only under the already-frozen S0-D data-like artifact rule. README/article/software hits remain non-candidates.

## Frozen Zenodo recovery

Preserve the same three identifiers:

1. DOI `10.1080/01611194.2022.2160677`;
2. exact normalized article title `Deciphering Mary Stuart's lost letters from 1578-1584`;
3. `Mary Castelnau cipher`.

For each identifier, use this transport cascade fixed before execution:

1. original plain public API query `q=<identifier>`;
2. retry the identical URL up to three total attempts with fixed delays `5s`, then `15s` after HTTP 429 or 5xx;
3. only if all three identical attempts fail with HTTP 429/5xx, retry once with the **same identifier enclosed as an exact phrase** in the `q` value: `q="<identifier>"`;
4. for the DOI identifier only, if exact-phrase query also fails with HTTP 429/5xx, final fallback is `q=doi:"10.1080/01611194.2022.2160677"`.

These fallbacks change query syntax/transport only; the searched identifier text is unchanged. No new term is introduced.

Archive every successful record exactly as S0-D did: ID, title, DOI, resource type, and file metadata. Apply the unchanged data-like artifact rule.

## Unchanged successful channels

S0-D-R1 reruns the same:

- pinned `CrypToolProject/CTTS@d8b7d77b4e12e7a22d3980f8b5fb4e44c773287b` local audit;
- Crossref DOI audit.

This produces a self-contained recovery result rather than combining hidden state from two runs.

Publisher HTML remains optional and is not needed for R1 negative-screen sufficiency.

## Frozen final classification

Use the original S0-D rules unchanged:

- `PUBLIC_MACHINE_READABLE_MARY_CASTELNAU_SOURCE_LOCATED` if any unchanged-rule positive candidate is found;
- `SOURCE_NOT_REPRODUCIBLY_ACCESSIBLE` only if CTTS + Crossref + recovered GitHub + recovered Zenodo all succeed and no positive candidate exists;
- `SOURCE_ACCESS_SCREEN_INDETERMINATE` if any required channel still fails and no positive candidate exists;
- `INVALID` for source-identity/implementation failure.

Only a positive source candidate licenses a five-layer structural Gate 0. A negative result stops Mary–Castelnau for the main Priority-3 lane; no author contact, private data, image OCR, manual transcription, or expanded web search is licensed as a post-reveal rescue.
