# ORIFLAMMS E1 roster provenance

Date: 2026-09-07
Parent: Issue #180 / Issue #172
Scientific state: **ROSTER FROZEN — NO E1 EFFECT STATISTIC COMPUTED**

## Frozen selection authority

Selection plan: `research/LM_A0_EXTERNAL_E1_ORIFLAMMS_SELECTION_PLAN_20260907.md`

External corpus:

- repository: `oriflamms/Dated-and-Datable-Manuscripts_LIRIS`
- pinned commit: `93de4af4a470aea3f3b23c2e8bafcfa2161c5438`
- `abbreviations.dtd` SHA-256: `dac3775b16878f596cd51391ef3fdbac6238205c057ac209585245009461f0b2`
- `mss-dates.xml` SHA-256: `5f5f3d4bab8bc04e180ca037ea50dec0c292dbb85a0097a2e10589b09fb64db7`
- `texts/mss-dates-w.xml` SHA-256: `d1ff8102e8c81f36d45a31143f9294cf5c061d55d879aed44244c858f65018e4`

## Schema/association recovery chronology

The first metadata extractor correctly read 102 metadata records but expected numbered child `<text>` nodes in the word-aligned authority and therefore found zero word documents. No effect statistic was computed.

A schema-only probe established that `mss-dates-w.xml` is a `teiCorpus` containing 102 immediate child `TEI` documents whose child `<text>` nodes do not retain the metadata `@n` value.

An association-only probe then showed that metadata and word authority have the same document count and that the sampled ordinal pairs have the same first-page IRHT image identifier apart from `.tif` versus `.png`.

The frozen recovery extractor (`oriflamms_e1_metadata_inventory_ordinal.py`) strengthened this to an all-document assertion: **all 102/102 ordinal pairs must share the same first-page IRHT image stem or the roster extraction aborts.** The successful run passed that assertion.

No abbreviation-position effect, p-value, FINAL1/FINAL2 score, or lexeme-specific result was computed during this recovery.

## Successful metadata-only run

- workflow run: `34121453209`
- workflow head: `53c1c42a287ac6462ca8964f774f6fa84d2b50d6`
- artifact ID: `10018334445`
- artifact ZIP SHA-256: `94137acab4a044957a7f0e0900963215ac4d03eca6fe832e4e208d659323a194`
- full metadata inventory SHA-256: `540944b4c6f3a4ed8446ee5cec6df739681f3756b12ce9158f699478a26fc00e`
- `effect_statistics_computed`: `false`
- metadata documents: 102
- word-aligned documents: 102
- first-page image-stem matches: 102/102

An earlier successful scientific roster extraction run (`34121301989`) produced the same inventory SHA-256 but placed the JSON one directory outside the artifact collection root. That was a transport-only defect. The path was corrected without changing roster logic and the metadata-only workflow was rerun.

## Frozen roster

The preregistered rule selected **23 manuscripts** whose complete declared date interval lies within 1375–1450 CE and that have unambiguous manuscript identity plus `lb`, `w`, and valid `choice/abbr/expan` structure.

The exact roster is now committed at:

`experiments/lm-a0-external-preflight/oriflamms_e1_frozen_roster.json`

Roster freeze commit:

`f370ed68982df9bfc56e68b30b519f247d8cd66e`

The roster includes manuscript dates from 1380–1400 through 1450 and multiple script classes including Rotunda, Textualis, Cursiva, Hybrida, Semitextualis, Humanistique and related forms.

## Firewall consequence

From commit `f370ed68982df9bfc56e68b30b519f247d8cd66e` onward, manuscripts may not be added to or removed from E1 because of abbreviation frequency, available power, line length, lexical composition, FINAL1/FINAL2 direction, or any observed effect.

The next licensed operation is parser/representation audit and scorer freezing against these 23 fixed documents. Only after that scorer is committed may the E1 effect be revealed.
