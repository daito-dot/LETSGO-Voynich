# Issue #58D / #66 — independent-transcription residual graph source audit plan

Status: **SOURCE/POPULATION AUDIT PREREGISTERED — NO #58D PAIR OR RESIDUAL TARGET SCORE AUTHORIZED**

Base main at branch creation:

`c777b81c9ef424429105dbcfd60532bdb9158362`

This file must predate the source-audit executable and any target replication plan/executable.

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

Primary candidate:

> **IT2a — Takeshi Takahashi reading, EVA transcription**

Canonical URL to audit:

`https://www.voynich.nu/data/IT2a-n.txt`

This choice is fixed on independent historical/project grounds, not on #58C graph agreement:

1. the repository's Phase63B source audit ranked IT2a first before #58C existed;
2. IT2a represents the Takeshi Takahashi reading lineage rather than the Zandbergen/Landini ZL reading lineage;
3. it remains in EVA conventions, giving a prospectively fair chance for the already frozen 12-slot parser to operate without inventing a new alphabet mapping after seeing results;
4. Phase63B previously used it as an independent-reading replication source without refitting the target recurrence mechanism.

Historical Phase63B audit identity, to be checked rather than blindly trusted:

- prior expected SHA-256: `78ce7677d6201d0f2c5c120ce769830672784adde458745e09e9dd0d12a94104`;
- prior expected line count: `5,444`;
- prior identity markers: `Takeshi Takahashi` and `Eva-` in the IVTFF header.

A changed current hash does **not** automatically authorize silently replacing the source. Any change must be reported and inspected as source-version drift before target authorization.

## 4. Secondary source audit only — GC2a

Comparator/fallback audit source:

`https://www.voynich.nu/data/GC2a-n.txt`

Historical Phase63B identity:

- prior SHA-256: `3c21f46003669c3417c485e0f6e0764fb4614646a2ed13eb8b1b88b23e2a1c1d`;
- prior expected line count: `5,444`;
- identity marker: `V101`.

GC2a is **not** authorized as the primary #58D exact 12-slot target by this plan. Its v101 alphabet is materially different from EVA and would require a mapping into the existing parser. Such a mapping could become a large outcome-dependent degree of freedom.

GC2a may replace IT2a only in a new separately frozen target plan after an objective source-audit failure of IT2a and a prospectively justified v101 compatibility layer. It may not be substituted because IT2a later gives an unfavorable graph result.

## 5. Independence standard

The audit must distinguish two kinds of independence:

### Reading-lineage independence

IT2a must be documented as deriving from the Takahashi reading lineage rather than the ZL reading lineage used for #58C.

### Publication/format independence

IT2a and ZL3b may share René Zandbergen's IVTFF publication/normalization ecosystem and EVA conventions. Therefore #58D must **not** claim complete publication-pipeline independence.

The intended replication claim, if successful, is narrower and accurate:

> independent manuscript reading lineage under a common EVA/IVTFF representational framework.

This limitation must remain visible in the eventual report.

## 6. Clean token and line parsing rules fixed before audit

The source audit uses the pre-existing Phase63B IVTFF token policy rather than inventing a #58D-specific cleanup rule:

1. ignore blank lines and header/comment lines beginning with `#`;
2. process IVTFF manuscript text lines beginning with `<f...>`;
3. split line identifier from text at the first whitespace;
4. tokenize text on `.` delimiters;
5. remove inline IVTFF comment/control fragments only by the already established outcome-independent source parser if required;
6. a candidate clean token for exact parser compatibility must match `[A-Za-z]+` after the fixed IVTFF cleanup;
7. do not normalize letters, merge glyph classes, or rewrite token strings to improve 12-slot parse coverage.

If the canonical source requires a materially different cleanup operation than the old Phase63B parser, Stage A must stop and document the mismatch before any target plan.

## 7. Frozen 12-slot parser compatibility audit

Use the current main version of:

`experiments/issue26-music/issue26e_core.py`

without changing its slot grammar.

Audit both:

- parser ambiguity policy `min` — primary compatibility population;
- parser ambiguity policy `max` — descriptive compatibility sensitivity only.

Permitted outputs are only population/coverage counts. Do **not** emit parser-derived pair occupancy relations.

For every clean IT2a token, record only whether the unchanged parser:

- accepts the token;
- rejects the token;
- has `min`/`max` ambiguity behavior relevant to population counts.

No slot-pair table, occupancy graph, Q statistic or residual statistic may be computed during Stage A.

## 8. Physical-leaf universe and folds

The audit must align IT2a pages to the already frozen #58C physical-leaf convention (`fNNr`, `fNNv` -> physical leaf number `NN`).

Use the same five deterministic physical-leaf folds as #58C for overlapping leaves.

Required outputs:

- all IT2a physical leaves represented in clean text;
- overlap with #58C/ZL3b analyzed physical-leaf universe;
- clean-token count on overlapping leaves;
- parser-min accepted-token count on overlapping leaves;
- accepted-token counts in each of the five frozen folds;
- leaves present only in IT2a or only in the #58C analyzed universe.

The target replication population must be restricted prospectively to the **shared physical-leaf universe** unless the later target plan gives a pre-reveal statistical reason to use a different population for the independent-existence question. Cross-reading graph comparison must never compare silently different physical-leaf populations.

## 9. Metadata / stratum audit

Where IT2a IVTFF metadata provide Currier language (`$L`) and illustration/section (`$I`) directly and consistently, reproduce population counts without pair scoring.

At minimum report support for the #58C group definitions if exact metadata are available:

- `AH`: Currier A within Herbal;
- `BH`: Currier B within Herbal;
- `BB`: section B within Currier B;
- `BS`: section S within Currier B;
- line initial;
- line interior;
- line final.

Do not import ZL3b Currier/section labels into IT2a on a token-by-token basis merely to force the same strata. Page-level externally defined metadata may be aligned only if its authority and rule are frozen in the audit report.

If exact stratum metadata are not sufficiently recoverable from IT2a, the later target plan must narrow the geometry-replication claim rather than fabricate labels.

## 10. Token-position labels

For each parsed physical line, define token position exactly as in #58B/#58C:

- `singleton`: only parsed token in the line;
- `initial`: first parsed token when at least two parsed tokens exist;
- `final`: last parsed token when at least two parsed tokens exist;
- `interior`: all other parsed tokens.

Stage A may report only counts by these labels.

## 11. Required source-audit outputs

The audit JSON/report must contain, for IT2a and GC2a where applicable:

1. retrieval URL and retrieval timestamp;
2. exact byte SHA-256;
3. exact byte size and line count;
4. header identity lines sufficient to confirm transcription identity;
5. comparison against historical Phase63B hashes/line counts;
6. count of manuscript text lines and unique page/leaf identifiers;
7. clean-token count under the frozen Phase63B token rule;
8. unchanged-parser accepted/rejected counts under `min` and `max`;
9. parser-min coverage overall and on shared #58C physical leaves;
10. shared physical-leaf count and frozen five-fold token counts;
11. metadata availability and support counts for planned #58C strata;
12. line-position support counts;
13. exact list/count of source-version or parsing deviations from the historical Phase63B assumptions;
14. an objective target-authorization disposition.

## 12. Objective target-authorization gates

IT2a is `AUTHORIZED_FOR_TARGET_PLAN` iff all are true:

1. current source identity is unambiguously IT2a/Takahashi EVA;
2. any hash/version change from Phase63B is understood and documented rather than unexplained;
3. the pre-existing clean-token parser works without a new outcome-dependent normalization;
4. unchanged 12-slot parser-min coverage on the shared physical-leaf universe is at least `60%` of clean tokens;
5. at least `80` #58C physical leaves overlap;
6. each of the five frozen physical-leaf folds contains at least `300` parser-min accepted IT2a tokens on the shared universe;
7. no target pair/residual score has been computed during Stage A.

The `60%`, `80 leaves`, and `300 tokens/fold` gates are frozen before audit output. They are deliberately support/compatibility gates, not effect-size gates.

If any required gate fails, disposition is:

`SOURCE/REPRESENTATION AUDIT DOES NOT AUTHORIZE EXACT IT2A TARGET`

If source identity is clear but one or more metadata strata are unsupported, the audit may still authorize **pooled residual-existence and cross-reading pooled-graph replication** while explicitly withholding unsupported stratum-geometry tests. That narrower authorization must be fixed in the audit report before target planning.

## 13. Strict Stage-A prohibitions

The source-audit executable/workflow must not calculate, print, persist, or inspect:

- any pairwise occupancy contingency table;
- any of the 66 Yule-Q values;
- any #58C residual Z values;
- any residual energy;
- any graph correlation or cosine/Spearman similarity;
- any edge sign agreement;
- any edge rank/magnitude comparison to ZL3b;
- any target empirical p-value;
- any alternative glyph normalization chosen because it improves graph agreement.

A population audit that accidentally reveals any of those quantities invalidates the clean source-selection stage and must be documented as such.

## 14. Sequence after source audit

If IT2a is authorized:

1. permanently archive the source-audit JSON/report and exact source hashes;
2. comment Issue #66 with the audit disposition;
3. commit the target replication `PLAN_A.md` **before** target executable code;
4. freeze IT2a-specific reference/test null calibration and cross-reading replication statistics;
5. run preflight that reproduces only the audited population before first reveal;
6. authorize target reveal only after plan-before-code verification.

If IT2a is not authorized, do not improvise. Record why and decide the next source/representation lane in a new plan-first step.