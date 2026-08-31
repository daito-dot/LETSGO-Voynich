# Issue #58D / #66 — independent-transcription residual graph source audit plan

Status: **SOURCE/POPULATION AUDIT PREREGISTERED — NO #58D PAIR OR RESIDUAL TARGET SCORE AUTHORIZED**

Base main at branch creation:

`c777b81c9ef424429105dbcfd60532bdb9158362`

This file predates the source-audit executable and any target replication plan/executable.

## 1. Program object

Read `research/TOKEN_CONSTRUCTION_PROGRAM.md` first.

The object is the internal construction of **one space-delimited Voynich token** under the established 12-slot representation. This is not sentence-level grammar, and visible spaces are not assumed to be proven natural-language word boundaries.

#58C established, under ZL3b + the frozen 12-slot parser, a broad residual token-internal interaction system beyond line-local slot prevalence, with a shared core and measurable stratum modulation.

The purpose of #58D is to determine whether that result is **manuscript-real rather than transcription/representation-specific**.

## 2. Frozen ZL3b result being replicated

Do not recompute or tune the reference result during this source audit.

- integrated #58C main commit: `c777b81c9ef424429105dbcfd60532bdb9158362`;
- #58C first-reveal raw SHA-256: `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`;
- frozen overall classification: `RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`.

This source audit may read #58C only for source-universe metadata such as physical-leaf folds and frozen population labels. It must not read individual residual edge values, signs, ranks, energies or cross-stratum graph correlations for any source-selection decision.

## 3. Primary independent reading fixed before target scoring

Primary exact-parser candidate:

> **IT2a — Takeshi Takahashi independent reading in `EvaT`**

Canonical URL to audit:

`https://www.voynich.nu/data/IT2a-n.txt`

This choice is fixed on pre-#58C project grounds, not on #58C graph agreement. Phase63B had already established that:

- GC2a/v101 is the stronger **independent-alphabet observational** challenge;
- IT2a/EvaT is the independent reading compatible with frozen EVA-family mechanism transfer without inventing a GC↔EVA mapping.

That same pre-existing compatibility fact makes IT2a the cleaner exact 12-slot replication target here. This does not make IT2a fully representation-independent: it remains inside an EVA/IVTFF publication framework.

### Exact historical Phase63B authority

The committed Phase63B `SOURCE_AUDIT_B.md` and `SOURCE_MANIFEST_B.json` are the authority:

- source: IT2a;
- lineage/alphabet: Takeshi Takahashi / `EvaT`;
- bytes: `342,104`;
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- Git-blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`;
- line count: `5,444`;
- header: `#=IVTFF EvaT 2.0 M 3`;
- provenance line: `# Extracted from LSI_ivtff_0d.txt`;
- version line: `# Version 2a of 02/02/2023 modified 25/06/2025`.

The first draft of Issue #66 / this plan contained an incorrect old IT2a SHA-256 and called the alphabet `Eva-`. Those were documentation errors discovered and corrected **before any #58D source-audit executable or any #58D pair/residual target score existed**. They have no authority over Phase63B's committed source manifest.

A changed current hash does **not** automatically authorize silently replacing the source. Any drift must be reported and understood before target authorization.

## 4. Secondary source audit only — GC2a

Comparator/fallback audit source:

`https://www.voynich.nu/data/GC2a-n.txt`

Historical Phase63B authority:

- lineage/alphabet: Glen Claston / `v101`;
- bytes: `314,916`;
- SHA-256: `b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f`;
- Git-blob SHA-1: `8417a644fbd9c11cdaf85224f29cafee9ba1bdb0`;
- line count: `5,822`;
- header: `#=IVTFF v101 2.0 M 6`.

GC2a is **not** authorized as the primary #58D exact 12-slot target by this plan. Its distinct v101 alphabet would require a mapping into the current EVA-derived slot grammar. Such a mapping is a large avoidable degree of freedom.

GC2a may replace IT2a only in a new separately frozen target plan after an objective source-audit failure of IT2a and a prospectively justified v101 compatibility layer. It may not be substituted because IT2a later gives an unfavorable scientific result.

## 5. Independence standard

The audit must distinguish two kinds of independence.

### Reading-lineage independence

IT2a derives from the Takahashi reading lineage rather than the ZL reading lineage used for #58C.

### Publication/format independence

IT2a and ZL3b share an EVA/IVTFF ecosystem. Therefore #58D must **not** claim complete publication-pipeline or alphabet independence.

The intended replication claim, if successful, is narrower:

> independent manuscript reading lineage under a common EVA/IVTFF representational framework.

This limitation must remain visible in the eventual report.

## 6. Frozen source parsing policy for Stage A

Do not invent a #58D-specific cleanup rule.

For IT2a, use the pre-existing Phase63B IVTFF parser semantics from `experiments/phase63/phase63b_common.py` / B1 compatibility where available in repository history:

- process P-coded IVTFF loci;
- respect source-native physical pages/leaves and line boundaries;
- use the W1 primary space view: both definite `.` and uncertain `,` spaces are boundaries;
- remove current IVTFF inline control tags by the established parser;
- exclude tokens containing uncertain-reading placeholders or `?` rather than repairing them;
- preserve native `EvaT` letter units exactly; no glyph-class merging or transliteration repair.

For direct compatibility with the current 12-slot parser, serialize only clean EvaT letter tokens exactly as read and call the unchanged current-main `SlotParser`.

Stage A may count accepted/rejected/ambiguous tokens. It may not calculate any pairwise occupancy relation.

For GC2a, Stage A may audit identity/coverage/native inventory, but the current EVA-derived `SlotParser` is not to be force-applied through an invented v101→EVA mapping.

## 7. Frozen 12-slot parser compatibility audit

Use the current main version of:

`experiments/issue26-music/issue26e_core.py`

without changing `SLOTS` or `SlotParser`.

Audit:

- parser ambiguity policy `min` — primary compatibility population;
- parser ambiguity policy `max` — population sensitivity only.

Permitted outputs are population/coverage counts only.

For every clean IT2a token, record only whether the unchanged parser:

- accepts the token;
- rejects the token;
- has more than one legal parse;
- yields the same or a different selected parse under `min` vs `max`.

No slot-pair table, occupancy graph, Q statistic or residual statistic may be computed during Stage A.

## 8. Physical-leaf universe and folds

Align IT2a pages to the frozen #58C physical-leaf convention (`fNNr`, `fNNv`, including split page suffixes, -> physical leaf number `NN`).

Use the exact five #58C physical-leaf folds, restricted to overlap.

Required outputs:

- IT2a physical leaves represented in P-coded clean text;
- overlap with the #58C/ZL3b analyzed physical-leaf universe;
- clean-token count on overlapping leaves;
- parser-min accepted-token count on overlapping leaves;
- accepted-token count in each frozen fold;
- leaves present only in IT2a or only in #58C.

The eventual cross-reading graph comparison must use a prospectively fixed shared physical-leaf universe. It must not silently compare different manuscript populations.

## 9. Metadata / stratum audit

Where the current IT2a IVTFF source supplies page-level Currier language (`$L`) and illustration/section (`$I`) metadata under the same IVTFF semantics, Stage A may reproduce **counts only** for the #58C groups:

- `AH`: Currier A within Herbal;
- `BH`: Currier B within Herbal;
- `BB`: section B within Currier B;
- `BS`: section S within Currier B;
- line initial;
- line interior;
- line final.

Do not import ZL3b token labels to manufacture support. If current IT2a does not independently expose adequate page-level metadata, the later target plan must narrow the geometry claim.

## 10. Token-position labels

For each physical line, position is defined on the **clean visible IT2a token sequence before 12-slot parse rejection**, matching the #58B/#58C concept that position belongs to the source line rather than to parser success:

- `singleton`: only clean visible token in the line;
- `initial`: first clean visible token when at least two exist;
- `final`: last clean visible token when at least two exist;
- `interior`: all other clean visible tokens.

Stage A may report counts only.

## 11. Required source-audit outputs

For IT2a, and for GC2a where applicable, the audit JSON/report must contain:

1. retrieval URL and retrieval timestamp;
2. exact byte SHA-256 and Git-blob SHA-1;
3. exact byte size and line count;
4. header identity lines;
5. comparison against exact historical Phase63B authority;
6. P-coded loci/pages/physical leaves;
7. clean-token count under the frozen source parser;
8. unchanged 12-slot parser accepted/rejected/ambiguous counts for IT2a;
9. parser-min coverage overall and on shared #58C leaves;
10. shared physical-leaf count and five frozen-fold accepted-token counts;
11. metadata availability and support counts for planned #58C strata;
12. line-position support counts;
13. exact source-version/parsing deviations;
14. objective target-authorization disposition;
15. explicit `scientific_pair_or_residual_metrics_computed: false`.

## 12. Objective target-authorization gates

IT2a is `AUTHORIZED_FOR_TARGET_PLAN` iff all are true:

1. current source identity is unambiguously IT2a/Takahashi `EvaT`;
2. any hash/version change from Phase63B is understood and documented rather than unexplained;
3. the pre-existing Phase63B source parser works without a new outcome-dependent normalization;
4. unchanged 12-slot parser-min coverage on the shared physical-leaf universe is at least `60%` of clean tokens;
5. at least `80` #58C physical leaves overlap;
6. each of the five frozen folds contains at least `300` parser-min accepted IT2a tokens on the shared universe;
7. no target pair/residual score has been computed during Stage A.

The `60%`, `80 leaves`, and `300 tokens/fold` gates were fixed before audit output. They are support/compatibility gates, not scientific effect-size gates.

If a required gate fails, disposition is:

`SOURCE/REPRESENTATION AUDIT DOES NOT AUTHORIZE EXACT IT2A TARGET`

If pooled gates pass but one or more metadata strata are unsupported, Stage A may authorize pooled residual-existence and pooled cross-reading graph replication while prospectively withholding unsupported stratum-geometry tests.

## 13. Strict Stage-A prohibitions

The source-audit executable/workflow must not calculate, print, persist, or inspect:

- pairwise occupancy contingency tables;
- any of the 66 Yule-Q values;
- #58C residual Z values;
- residual energy;
- graph Pearson/Spearman/cosine similarity;
- edge sign agreement;
- edge rank/magnitude comparison to ZL3b;
- target empirical p-values;
- alternative glyph normalization selected because it improves graph agreement.

Accidental production of any of those invalidates the clean source-selection stage and must be documented.

## 14. Sequence after source audit

If IT2a is authorized:

1. permanently archive the source-audit JSON/report and exact source hashes;
2. comment Issue #66 with the audit disposition;
3. commit target replication `PLAN_A.md` **before** target executable code;
4. freeze IT2a-specific reference/test null calibration and cross-reading replication statistics;
5. run a preflight that reproduces only the audited population before first reveal;
6. authorize target reveal only after plan-before-code verification.

If IT2a is not authorized, do not improvise. Record why and decide the next source/representation lane in a new plan-first step.