# Issue #58B source / stratum audit report

Status: **COMPLETE — POPULATION SUPPORT ONLY; NO OCCUPANCY-EDGE TARGET SCORES REVEALED**

## Provenance

- parent main at branch creation: `ab6a8cc18566545f964e9d89d11e72e64842d49a`
- source-audit plan first-add: `fd9893d70acacc95a4579eb43d05e9ac20916766`
- source-audit implementation first-add: `c42db3ab7938af08a7566ac3acb6b41504bfc15c`
- workflow head: `a72d4b423f7cad32ac417557de3ddfc633a0ac67`
- GitHub Actions run: `33436370960`
- job: `99633692794`
- artifact ID: `9774539949`
- artifact name: `issue62-source-audit-a72d4b423f7cad32ac417557de3ddfc633a0ac67`
- artifact ZIP SHA-256: `c3c90084748ce73bc5378ee5efd3790efcafdbaca5b5df334ac2bb6d18c41f50`
- exact raw audit JSON SHA-256: `afce5aba288145d1122bff9184e97a4573e8ec527823db9db2613fd668378259`
- deterministic archived gzip SHA-256: `cb64e1322e50ce43c83a2049761dd8726a08eaf88462a3a3251e25b24e82a3b6`
- frozen ZL3b source Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

The exact audit JSON is preserved as `source-audit/issue62_source_audit.json.gz` using deterministic `gzip -n -9`.

The workflow explicitly emitted scope:

`population_and_external_metadata_only_no_occupancy_pair_scoring`

No 66-edge contingency, phi, odds ratio, predictive gain, graph correlation, rank, target p-value or target null was computed in this audit.

## Population reproduction

The audit exactly reproduced #58A's token population invariant:

- visible tokens: **32,570**
- parsed under primary `min` policy: **25,071**
- parse coverage: **0.7697574455**
- analyzed paragraphs: **736**
- analyzed physical lines: **4,119**
- analyzed pages: **206**
- unique physical leaves: **99**

The 4,119 line count includes all analyzed paragraph lines containing visible tokens. #58A's `4,082` line count was the narrower count of lines retaining at least one successfully parsed token; this is not a population discrepancy.

## Currier language `$L`

Predeclared eligibility required >=1,000 parsed tokens total, >=100 in every frozen fold and >=10 unique leaves.

| `$L` | parsed | fold parsed | leaves | eligible |
|---|---:|---|---:|:---:|
| A | 7,700 | 1881 / 1820 / 1761 / 1288 / 950 | 54 | yes |
| B | 17,021 | 2447 / 2964 / 3668 / 4159 / 3783 | 40 | yes |
| missing | 350 | 102 / 26 / 87 / 0 / 135 | 5 | no |

Ten analyzed pages have missing `$L` metadata:

`f65v, f67r1, f67r2, f67v2, f68r1, f68r2, f68v2, f68v3, f69r, f70r2`.

No analyzed page has `$L=@`, and no analyzed data line contains an in-text `$L` override.

## Illustration / section `$I`

| `$I` | parsed | fold parsed | leaves | eligible |
|---|---:|---|---:|:---:|
| A | 178 | 66 / 0 / 0 / 0 / 112 | 2 | no |
| B | 4,936 | 999 / 941 / 1116 / 1191 / 689 | 10 | **yes** |
| C | 483 | 36 / 26 / 60 / 79 / 282 | 6 | no |
| H | 7,996 | 1613 / 1604 / 1772 / 1603 / 1404 | 64 | **yes** |
| P | 1,608 | 301 / 543 / 433 / 218 / 113 | 6 | no: leaf support |
| S | 8,174 | 1269 / 1696 / 2135 / 1917 / 1157 | 13 | **yes** |
| T | 1,696 | 146 / 0 / 0 / 439 / 1111 | 5 | no |

No analyzed page is missing `$I`, no page has `$I=@`, and no analyzed data line contains an in-text `$I` override.

Eligible section values are therefore exactly **B, H, S**.

## Token-position support

Frozen categories were defined from visible-token order before parser failures.

| position | parsed | fold parsed | eligible |
|---|---:|---|:---:|
| initial | 2,915 | 536 / 547 / 653 / 616 / 563 | yes |
| interior | 19,556 | 3398 / 3765 / 4303 / 4290 / 3800 | yes |
| final | 2,585 | 492 / 497 / 552 / 540 / 504 | yes |
| singleton | 15 | 4 / 1 / 8 / 1 / 1 | no |

`singleton` is therefore excluded from confirmatory #58B positional comparisons. It may remain a descriptive count only.

## Critical `$L × $I` confounding structure

The audit revealed strong page-level confounding between Currier language and section. This is metadata/population information, not an occupancy-graph outcome.

Parsed-token cross-populations:

| population | parsed | leaves | fold parsed |
|---|---:|---:|---|
| L=A, I=H | 5,520 | 47 | 1434 / 851 / 1328 / 1070 / 837 |
| L=A, I=P | 1,608 | 6 | 301 / 543 / 433 / 218 / 113 |
| L=A, I=S | 426 | 1 | 0 / 426 / 0 / 0 / 0 |
| L=A, I=T | 146 | 1 | 146 / 0 / 0 / 0 / 0 |
| L=B, I=B | 4,936 | 10 | 999 / 941 / 1116 / 1191 / 689 |
| L=B, I=C | 338 | 2 | 0 / 0 / 0 / 79 / 259 |
| L=B, I=H | 2,449 | 16 | 179 / 753 / 417 / 533 / 567 |
| L=B, I=S | 7,748 | 12 | 1269 / 1270 / 2135 / 1917 / 1157 |
| L=B, I=T | 1,550 | 4 | 0 / 0 / 0 / 439 / 1111 |

Two outcome-independent overlap designs are particularly clean:

1. **Currier comparison within Herbal only:** `I=H`, compare `L=A` vs `L=B`. Both groups independently pass the support screen in all five folds.
2. **Section comparison within Currier B only:** `L=B`, compare `I=B`, `I=H`, `I=S`. All three groups independently pass the support screen in all five folds and have >=10 physical leaves.

This avoids interpreting a simple section composition difference as a Currier effect, or vice versa.

## Hand metadata

`$H` and `$C` were counted only as descriptive confound checks. They are not promoted to primary #58B factors by this audit.

Modern `$H` parsed support is spread mainly across hands 1–3; `$C` has substantial missingness and several small groups. Introducing them now as additional target dimensions would substantially enlarge the search family without being required by Issue #58. They remain deferred unless a later separately frozen question independently motivates them.

## Consequence for the target plan

The #58B target plan should therefore be frozen around three externally defined families:

- Currier A vs B **within `I=H`**;
- section B/H/S **within `L=B`**;
- line position initial/interior/final, with singleton excluded by the predeclared support rule.

The target statistic must operate on the complete 66-edge signed graph. No individual #58A edge may be promoted to a confirmatory target because its score is already known.
