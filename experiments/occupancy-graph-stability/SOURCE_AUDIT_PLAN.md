# Issue #58B — source / stratum audit plan

Status: **FROZEN SOURCE AUDIT — NO #58B OCCUPANCY-EDGE TARGET SCORING AUTHORIZED**

Parent: Issue #62, follow-up under umbrella Issue #58.

Current accepted main at branch creation: `ab6a8cc18566545f964e9d89d11e72e64842d49a`.

## Purpose

Issue #58A established a broad signed 66-edge binary slot-occupancy graph, but the exact register/Currier/token-position tests required by umbrella Issue #58 were not frozen before #58A's first reveal.

This audit exists only to determine which **externally defined strata have adequate population support** for a later preregistered #58B target test.

It must not score, rank, visualize, select or otherwise inspect occupancy dependence between slot pairs.

## Frozen source

Reuse the same source as #58A without alteration:

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- required Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

Reuse the current-main `experiments/issue26-music/issue26e_core.py` parser/population logic and the same deterministic `physical_leaf_folds`.

The audit may instantiate `SlotParser` solely to count whether visible tokens are parseable under the primary `min` policy. It must not emit slot occupancies, pair counts, phi, mutual information, predictive gain or any function of pairwise slot relation.

## External metadata authority

ZL3b is IVTFF. Its page headers contain page variables. The current IVTFF format definition (file format 2.0.1, document issue 2.0.2 dated 2025-07-08) defines:

- `$L = A/B`: Currier language of the page or text section;
- `$I`: illustration type / manuscript section (`A`, `B`, `C`, `H`, `P`, `S`, `T`, `Z`);
- `$H`: writing hand (Lisa Fagin Davis hand in modern IVTFF files);
- `$C`: Currier hand.

For #58B primary stratification, this audit evaluates only `$L` and `$I` as candidate external page-level strata. `$H` and `$C` are counted descriptively to expose possible confounding but are not automatically promoted to #58B targets.

If `$L` or `$I` is unset, `@`, or modified by an in-text tag on any analyzed page, the audit must report it explicitly. The later target plan must not silently guess or back-fill that assignment.

## Analysis population

Mirror #58A exactly:

1. use `issue26e_core.parse_voynich`;
2. keep the physical-leaf universe produced by the existing five `physical_leaf_folds`;
3. use only paragraph (`P`) running-text loci admitted by that parser;
4. count every visible token in that universe;
5. mark a token parsed iff `SlotParser.pick(token, "min")` succeeds.

No edge-level quantity is permitted.

## Frozen token-position categories

Position is defined from the **visible-token order on the physical line before parser failures are removed**.

Mutually exclusive categories:

- `singleton`: line contains exactly one visible token;
- `initial`: first visible token on a line of length >= 2;
- `final`: last visible token on a line of length >= 2;
- `interior`: all remaining visible tokens.

This definition is outcome-independent and must not be changed after the source-audit counts are seen merely to improve balance.

The later target plan may designate `singleton` sensitivity-only if population support is poor, but it must preserve the above definition.

## Required audit outputs

Produce deterministic JSON containing only population / metadata information:

1. exact source Git blob and parser validation status;
2. total visible tokens, parsed tokens, parse coverage, analyzed paragraph count, analyzed physical-line count and unique physical leaves;
3. fold-level visible / parsed counts;
4. page-header counts and analyzed-token counts for every observed `$L`, `$I`, `$H`, `$C` value, including missing / `@`;
5. for `$L` and `$I`, visible / parsed counts and unique leaves by each of the five frozen folds;
6. parsed and visible token counts for all `$L × $I` combinations;
7. visible / parsed counts and fold support for `singleton`, `initial`, `interior`, `final`;
8. counts of analyzed data lines containing any in-text `$L` or `$I` tag override;
9. counts of analyzed pages whose page-level `$L` or `$I` is missing or `@`;
10. a machine-readable list of candidate strata meeting each predeclared support screen below.

## Predeclared population-support screens

These screens select only on **sample support**, never on occupancy outcomes.

For a page-level `$L` or `$I` stratum to be eligible for a later confirmatory graph test, require all:

- at least `1,000` parsed tokens total;
- at least `100` parsed tokens in every one of the five frozen physical-leaf folds;
- at least `10` unique physical leaves total;
- no unresolved page-level `@` semantics for that stratum.

For a token-position category to be eligible for a later confirmatory graph test, require:

- at least `1,000` parsed tokens total;
- at least `100` parsed tokens in every frozen fold.

These thresholds are frozen before seeing the audit counts. Passing them does **not** imply the category must become a primary hypothesis; it only makes it technically eligible. The #58B statistical plan must be separately committed before any occupancy-edge scoring.

## Explicitly prohibited audit outputs

Do not compute or emit:

- any of the 66 pair contingencies;
- phi / odds ratio / co-occupancy ratio;
- mutual information;
- held-out predictive gain;
- edge rank;
- the #58A top-edge subset;
- graph correlations or graph distances between strata;
- any target p-value or null distribution.

If the audit implementation contains any such calculation, the audit is invalid and must not be used to freeze #58B strata.

## Stop rule

After the source audit, inspect only population support and metadata quality. Then commit a separate `PLAN_A.md` defining the actual #58B graph-level hypotheses, statistics, nulls, multiplicity and classification gates **before** any target-scoring executable or workflow is run.
