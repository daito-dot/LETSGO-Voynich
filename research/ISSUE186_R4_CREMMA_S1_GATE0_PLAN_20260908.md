# Issue #186 — R4 / CREMMA signed paragraph-entry Gate0 plan

Date: 2026-09-08  
Parent: Issue #172 / near-term Priority 1  
Stage: **Gate0 only — score-free composability audit**

## Question

Can the already-frozen Phase62B/62C signed paragraph-entry statistic be replayed on the full externally classified CREMMA manuscript panel without changing the representation, boundary definition, target direction, or source membership?

Gate0 does **not** answer which class has positive or negative S1. It establishes the source and parser population that a later one-shot reveal is allowed to score.

## Authorities

Repository authority is current `main` at the start of Issue #186:

- base main: `224c0130016e533823df14df682a30ca668b88e6`
- roadmap: `research/NEAR_TERM_RESEARCH_ROADMAP_20260908.md`
- historical parser / S1 implementation: `experiments/phase62/phase62b_n0.py`
- historical implementation git blob: `e0ada366845c7a6c5a5dd75de91fe262b72a94b6`
- ZL3b source git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- ZL3b mirror repository: `matthewdgreen/cipher_benchmark`
- ZL3b mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- CREMMA repository: `HTR-United/CREMMA-Medieval-LAT`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`

The external checkout route is copied from the historical Phase62B GitHub Actions workflow. No new corpus transport is introduced for Issue #186.

## Frozen external population

The only class label is the `Type` field in the pinned CREMMA registry. All 21 registered manuscripts are included before any new S1 score is computed.

### Medic.

- `Egerton821` → `data/Egerton821`
- `H318` → `data/H318`
- `CLM13027` → `data/CLM13027`
- `Latin16195` → `data/Latin16195`
- `Phi_10a135` → `data/Phi_10a135`

### Schol.

- `WettF0015` → `data/WettF0015`
- `BIS-193` → `data/BIS-193`
- `Mazarine915` → `data/Mazarine915`
- `PalLat373` → `data/PalLat373`
- `CCCC-MSS-165` → `data/CCCC-MSS-165`

### Lit.

- `CCCC-MSS-236` → `data/CCCC-MSS-236`
- `LaurentianusPluteus33.31` → `data/LaurentianusPluteus33.31`
- `Arras-861` → `data/Arras-861`
- `Latin6395` → `data/Latin6395`
- `LaurentianusPluteus39.34` → `data/LaurentianusPluteus39.34`
- `Latin8236` → `data/Latin8236`

### Eccl.

- `UBL758` → `data/UBL758`
- `SBB_PK_Hdschr25` → `data/SBB_PK_Hdschr25`
- `BGO-511` → `data/BGO-511`

### Gramm.

- `LaurentianusPluteus53.08` → `data/LaurentianusPluteus53.08`
- `LaurentianusPluteus53.09` → `data/LaurentianusPluteus53.09`

No manuscript may be removed because of its eventual S1 value. A missing folder or parser failure is recorded as a Gate0 failure; zero S1-eligible items is a support outcome, not a reason to repair the source.

## Historical S1 contract reserved for Stage1

Stage1, if licensed, must replay the historical Phase62B/62C statistic unchanged:

- paragraph items begin at source pilcrow `¶` markers;
- item eligibility is historical `base_eligible` + `valid_pseudo_indices`;
- the same eight line features are used;
- the real paragraph-entry contrast is line 2 minus line 0, residualized by within-item pseudo-boundaries;
- feature scaling and each of five projection directions come only from the corresponding Voynich training leaves;
- positive projection is the historical Voynich direction;
- target mean remains `0.8759941302988878`;
- no class-specific direction, sign flip, tokenization, line offset, paragraph repair, rescaling, or manuscript subsetting is allowed.

None of those target-derived projections is computed in Gate0.

## Gate0 firewall

The Gate0 executable may import the historical Phase62B module only to reuse Latin parsing and support predicates. Immediately after import it must replace these score-producing functions with throwing stubs:

- `feature8`
- `training_sd`
- `item_contrast`
- `contrasts`
- `s1_projection`

Gate0 must not parse the ZL3b text. It may only verify the ZL3b git blob. This prevents construction of target folds, target feature scales, or projection directions during the composability audit.

Forbidden Gate0 outputs include:

- any new manuscript S1 value;
- any item contrast projected onto a Voynich direction;
- positive/negative S1 counts;
- class S1 means or medians;
- ratios to the Voynich target;
- any scientific R4 classification.

The output must contain the literal marker:

`NO ISSUE186 SCIENTIFIC S1 SCORE COMPUTED`

and `scientific_score_computed: false`.

## Allowed Gate0 outputs

For every frozen manuscript:

- source path;
- external `Type`;
- parse status;
- item count;
- base-eligible item count;
- S1-eligible item count, using only the structural eligibility predicate;
- physical-line count represented by parsed items;
- non-empty-line count;
- token count.

Class summaries may contain only counts of listed, parsed, and structurally eligible manuscripts. No S1-derived field is allowed.

## Gate0 validity

`gate0_valid = true` requires all of the following:

1. the historical Phase62B implementation git blob matches exactly;
2. the Phase62B embedded CREMMA and ZL3b authority constants match this plan;
3. the CREMMA checkout is exactly the pinned commit;
4. the ZL3b file has exactly the pinned git blob;
5. every one of the 21 frozen CREMMA folders parses without source/path error;
6. the score firewall is installed before the real external panel is audited;
7. no scientific S1 score is computed.

A manuscript with zero structurally S1-eligible items does not invalidate Gate0. It is retained as externally selected but non-composable for Stage1.

## Chronology after Gate0

If the pull-request Gate0 run succeeds:

1. archive the raw Gate0 JSON and provenance in the repository;
2. freeze its hashes/run identifiers;
3. only then add a separate Stage1 scorer that computes the one-shot external S1 reveal under Issue #186;
4. do not alter source membership, class labels, eligibility, S1 implementation, signs, or interpretation labels after seeing Stage1 values.

Historical S1 values already revealed for `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`, and the small H318 sensitivity remain disclosed history. The prospective protection here is complete externally fixed inclusion of the 21-manuscript registry population, not a claim that those historical rows are blinded.
