# LM-A0 external E1 — ORIFLAMMS selection and replication plan

Date: 2026-09-07
Parent: Issue #180 / Issue #172
Prior external result: `E0_NO_EXTERNAL_SUPPORT_ON_THIS_SAMPLE`
Status: **FROZEN E1 SELECTION PLAN — METADATA INVENTORY MAY RUN; EFFECT SCORING MAY NOT RUN UNTIL THE E1 ROSTER IS COMMITTED**

## Purpose

E0 tested a preregistered line-final abbreviation-enrichment prediction on one 11th-century working TEI file from Bamberg Can. 6. The observed effect ran opposite to the preregistered direction.

E1 does **not** reverse the prediction. It asks whether the unchanged prediction replicates in a substantially larger, independently curated corpus with dated manuscripts closer to the Voynich manuscript's early-15th-century physical context.

The external corpus is ORIFLAMMS, *Dated and Datable Manuscripts*.

## Frozen corpus authority

Repository:

- `oriflamms/Dated-and-Datable-Manuscripts_LIRIS`
- commit: `93de4af4a470aea3f3b23c2e8bafcfa2161c5438`
- metadata/source TEI: `mss-dates.xml`, blob `d09ef1bae7c9acce7f9a0fa312c3bbbffed0fa60`
- word-aligned TEI: `texts/mss-dates-w.xml`, blob `961292d08d1e0ef3bceac4c813ff7319b8e26352`
- character/coordinate TEI: `texts/mss-dates-c.xml`, blob `dbfbdc39a79c7d3afad4e1d559c5c71d1ac67adf`

The public dataset documentation states that the corpus contains dated manuscript transcriptions, preserves abbreviated and expanded forms in TEI, and provides line/word alignment and image coordinates. E1 uses only repository-pinned data.

## Selection firewall

Before any E1 abbreviation-position effect is computed, perform one metadata-only inventory.

The inventory may inspect only:

- manuscript identifier;
- declared dating attributes (`when`, `notBefore`, `notAfter`);
- script metadata;
- language metadata if present;
- boolean presence/absence of physical line markup (`lb`), lexical word markup (`w`), and abbreviation/expansion markup (`choice` with `abbr`/`expan`);
- ability to associate a transcription block with one manuscript identifier.

The inventory must **not** report:

- abbreviation counts or rates;
- line-final counts;
- FINAL1/FINAL2 effects;
- lexeme-specific abbreviation behavior;
- any p-value or candidate score.

## Frozen E1 roster rule

A manuscript enters the E1 candidate roster if and only if all of the following are true:

1. its dating can be represented by a closed interval `[earliest, latest]` from the metadata;
2. the full declared interval is contained in **1375–1450 CE**, i.e. `earliest >= 1375` and `latest <= 1450`;
3. the transcription has physical `lb` markup;
4. it has lexical `w` markup or another deterministic word segmentation already supplied by the corpus;
5. it has at least one structurally valid `choice/abbr/expan` annotation;
6. manuscript identity is unambiguous.

No manuscript may be added or removed because its abbreviation rate, lexical inventory, line length, FINAL1/FINAL2 effect, or statistical power looks favorable.

### Date conversion

- `date[@when=YYYY]` -> `[YYYY, YYYY]`.
- `date[@notBefore=YYYY][@notAfter=YYYY]` -> `[notBefore, notAfter]`.
- if only one open-ended bound is present, the manuscript is not roster-eligible for E1.
- if multiple dating statements apply to one transcription and cannot be reduced deterministically to one manuscript-level interval without historical interpretation, mark `DATE_AMBIGUOUS` and exclude from confirmatory E1.

## Minimum replication support

After the metadata-only roster is frozen:

- if fewer than **3 independent manuscripts** are eligible, E1 is classified `E1_INDETERMINATE_INSUFFICIENT_MANUSCRIPTS` and no confirmatory effect test is run;
- otherwise every eligible manuscript enters the confirmatory test.

No sample-size threshold based on abbreviation counts may be introduced after the inventory.

## Unchanged scientific prediction

The primary prediction remains exactly the E0 prediction:

> Holding normalized expanded lexical form fixed within manuscript, abbreviation is enriched when an occurrence is the final complete lexical token on a physical manuscript line.

E1 does not adopt E0's observed negative direction.

## Primary representation

Use the corpus-supplied manuscript and physical-line boundaries.

For each lexical occurrence:

- surface realization comes from `abbr` when a valid `choice/abbr/expan` exists, otherwise the corpus surface word;
- expanded lexical form comes from `expan` for an abbreviation choice, otherwise the literal lexical form;
- normalization remains Unicode NFC + casefold + removal of leading/trailing non-letter material only;
- do not normalize `u/v`, `i/j`, morphology, spelling, lemmas, or language-specific variants.

Malformed or unresolved annotations are excluded and counted under a frozen parser audit, not silently repaired.

## Boundary exclusions

Preserve the E0 logic where representable:

- exclude a lexical item spanning a physical line boundary;
- exclude both adjacent physical lines when a corpus marker explicitly identifies a word split or non-breaking line division;
- exclude running headers/footers and non-body furniture where the corpus distinguishes them structurally;
- do not infer semantic sentence or clause boundaries.

If ORIFLAMMS markup cannot represent one of these E0 exclusions exactly, the implementation must record the incompatibility before effect scoring. It may not invent a text-driven substitute.

## Primary statistic

Stratify by **manuscript x normalized expanded lexical form**.

Within every mixed stratum with at least one abbreviated and one unabbreviated occurrence, freeze:

- `n`: eligible occurrences;
- `a`: abbreviated occurrences;
- `f`: FINAL1 occurrences;
- `x`: abbreviated FINAL1 occurrences.

Primary pooled statistic:

`X = sum x`

Null: abbreviation labels are exchangeable within each manuscript x expanded-form stratum while preserving `n`, `a`, and `f`.

Use exact hypergeometric convolution where computationally practical. If exact support is too large, use a fixed-seed Monte Carlo null with at least 1,000,000 draws and label it explicitly as Monte Carlo.

Report:

- observed `X`;
- exact/null expectation;
- variance and z where defined;
- one-sided enrichment p-value `P(X_null >= X_obs)`;
- descriptive two-sided tail result.

## Manuscript-level replication diagnostic

For every eligible manuscript, compute the same observed-minus-expected FINAL1 direction using only its own strata.

This diagnostic is frozen before effect reveal. It prevents a single large manuscript from being treated as cross-manuscript replication.

## FINAL2 sensitivity

As in E0, repeat the same construction for the final two complete lexical tokens (`FINAL2`).

FINAL2 is a sensitivity and cannot rescue a failed FINAL1 primary.

## E1 classification

`E1_REPLICATED_EXTERNAL_SUPPORT` requires all of:

1. at least 3 eligible independent manuscripts;
2. pooled FINAL1 observed > expected;
3. pooled one-sided enrichment p <= 0.05;
4. at least two-thirds of informative manuscripts have manuscript-level observed > expected;
5. pooled FINAL2 observed > expected.

If at least 3 manuscripts are eligible but any of conditions 2–5 fails:

`E1_NO_REPLICATION`

If extraction/authority incompatibility prevents the frozen representation:

`E1_INVALID_OR_INDETERMINATE`

## Consequence

- `E1_REPLICATED_EXTERNAL_SUPPORT` would justify drafting a minimal LM-A1 architecture from **external** evidence. It would still not license Voynich target scoring until a separate target plan is frozen under #172/R10.
- `E1_NO_REPLICATION` rejects promotion of LM-A0 as currently operationalized. Do not invert the mechanism or add a cache/layout repair after reveal.
- `E1_INDETERMINATE_INSUFFICIENT_MANUSCRIPTS` returns the program to architecture selection without using #179 target data.

Issue #179 remains sealed throughout E1 selection and scoring.
