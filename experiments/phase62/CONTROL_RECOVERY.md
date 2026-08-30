# Phase 62A — external-control recovery audit

Status: descriptive/provenance audit completed before any Phase62 N0/B0 tournament score was computed.

## Why this audit was necessary

Phase59 established that source-native medieval item/section entries can reproduce part of the Voynich paragraph-entry transition. However, the Phase59 repository state preserved plans and result JSONs but not the exact extraction script or every item-level selection decision.

Phase62 therefore does **not** reconstruct missing historical subsets by choosing medieval entries that resemble Voynich. That would convert a historical development result into a post-hoc control.

Instead, this audit separates:

1. what can be recovered exactly from the historical record;
2. what cannot be recovered without guesswork;
3. a new objective source-selection rule that can be frozen before the N0/B0 tournament.

## External source freeze

Repository:

- `HTR-United/CREMMA-Medieval-LAT`
- frozen commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- corpus: graphematic medieval Latin manuscript transcriptions, 12th–16th century
- project license: CC BY 4.0 at the frozen repository state

The Phase62 repository does not redistribute the external corpus. CI checks out the exact external commit and verifies it before enumeration.

Recovery executable:

- `phase62a_recover_controls.py`

CI:

- `.github/workflows/phase62-control-recovery.yml`

Successful corpus-wide audit run:

- GitHub Actions run `33312150397`
- artifact `phase62-control-recovery`, artifact ID `9732307989`
- artifact ZIP SHA-256 `11d117ea8621968a6f5233599698eced1662bb4af99bc24dc2515a8707b81f6a`

## Frozen extraction rule for candidate enumeration

No Voynich statistic enters this rule.

- boundary marker: literal source-native pilcrow `¶` (U+00B6)
- tokenization: Unicode NFC maximal Letter/Mark sequences
- punctuation/separators discarded
- abbreviation graphemes retained; no abbreviation expansion
- entry line0: text following the source-native pilcrow on that physical transcription line
- line1/line2: next two physical source lines
- eligible entry: at least 5 usable tokens in line0 and line2

This rule is an enumeration rule. The Phase62 tournament plan separately controls score calculation and internal pseudo-boundary construction.

## Historical Phase59 subset recoverability

| historical Phase59 group | stored n | eligible under reconstructed generic rule | audit conclusion |
|---|---:|---:|---|
| H318 recipe context | 3 | 4 | exact historical item subset not recoverable from current repository metadata |
| CLM13027 39r treatment | 3 | 4 | page recoverable; exact 3/4 item selection not recoverable |
| CLM13027 41r–41v discussion | 9 | 34 | exact historical semantic sub-selection not recoverable |
| UBL758 ecclesiastical | 5 | 5 | effectively recoverable as all eligible literal-pilcrow entries |
| BIS193 scholastic | 5 | 64 | historical five-entry subset not recoverable |

### Consequence

Phase59 remains valid **historical development evidence** for the interpretation already recorded there. But its incompletely preserved H318/CLM/BIS item subsets must not become the sole prospective Phase62 control panel.

No missing historical subset will be reconstructed by maximizing similarity to the old Phase59/Voynich result.

## Phase52 pre-existing five-manuscript panel audit

Phase52 had independently established this document/genre pilot before the Phase62 tournament was conceived:

| manuscript | broad type | files | literal pilcrows | eligible entries |
|---|---|---:|---:|---:|
| Arras 861 | literary | 5 | 0 | 0 |
| CLM 13027 | medical | 5 | 53 | 39 |
| H318 | medical / recipes | 5 | 5 | 4 |
| UBL 758 | ecclesiastical | 15 | 10 | 5 |
| BIS 193 | scholastic | 6 | 98 | 64 |

Total eligible entries: **112**.

Arras861 remains useful as a general manuscript/line-position control but cannot contribute to the literal-pilcrow entry-primary test under this rule.

The large imbalance (e.g. BIS193 64 vs UBL758 5) means entries must **not** simply be pooled. Manuscript is the primary external replication unit and manuscript-level results receive equal interpretive weight.

## Corpus-wide objective structured-entry panel

Before the corpus-wide counts were inspected, the audit executable fixed this inclusion rule:

> include every immediate CREMMA `data/` manuscript directory with at least **5 eligible literal-pilcrow entries** under the frozen extraction rule.

No Voynich statistic or Phase59 similarity enters selection.

The resulting panel is:

| manuscript | broad type from CREMMA registry/README | eligible entries |
|---|---|---:|
| BIS 193 | scholastic | 64 |
| CLM 13027 | medical | 39 |
| Mazarine 915 | scholastic | 38 |
| UBL 758 | ecclesiastical | 5 |

Total: **4 manuscripts / 146 eligible entries**.

This is the primary Phase62 N0 entry panel because its inclusion rule is objective, corpus-wide, and frozen without reference to the Voynich tournament score.

### Pre-existing-panel sensitivity

H318 has 4 eligible entries and therefore misses the corpus-wide primary threshold. It remains admissible as a **named sensitivity analysis** because it was already a Phase52 medical/recipe pilot manuscript. It must not be silently added to or removed from the primary four-manuscript estimate depending on its Phase62 score.

Arras861 may likewise remain a non-entry document/line-position sensitivity control, but it has no eligible literal-pilcrow entries under the primary entry rule.

## Implications for Phase62 design

1. **Primary N0 entry replication unit = manuscript, not entry.**
2. **Primary structured-entry panel = BIS193, CLM13027, Mazarine915, UBL758.**
3. All eligible entries in each selected manuscript are used; no semantic/manual cherry-picking.
4. H318 is predeclared sensitivity only; Arras861 is non-entry sensitivity only.
5. Source-native boundaries are preserved.
6. N0/B0 scoring must use a cross-representation feature subset rather than Voynich-specific literal `{k,t}` features as primary dimensions.
7. B0 transforms must be global and boundary-blind so they cannot manufacture an entry register by inspecting entry position.
8. A1 remains frozen from Phase61C and receives no repair before the comparison.

## What this audit changes

It strengthens the control architecture relative to Phase59: the next comparison no longer depends on small hand-selected entry classes whose exact membership is partly lost. It will use an independently reproducible corpus-wide source rule and report between-manuscript heterogeneity directly.

It does **not** alter Phase59 numerical results or retroactively relabel them as prospective evidence.
