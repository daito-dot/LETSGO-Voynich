# Issue #188 — R4 / Casebooks score-free Gate0 plan

Date: 2026-09-08  
Parent: Issue #172, Priority 1  
Base main: `544a3ae97001ff4ea8c353bde805aee7a1157005`

## External authority

- repository: `CasebooksProject/casebooks-data`
- pinned commit: `9d42295d72b5ba8889575a32d79311cc72bce73a`
- population: every `cases/CASE*.xml` file at that commit
- external architecture: the Casebooks Project's raw XML transcriptions of the medical/astrological case records of Simon Forman and Richard Napier, 1596–1634

No Casebooks S1 score may be computed during Gate0.

## Frozen diplomatic extraction

Scientific items are only TEI paragraphs under `<text>/<body>`.

Physical lines are the main paragraph text segmented by descendant `<lb/>` markers in XML source order. A first `<lb/>` at the beginning of a paragraph starts line 0 rather than creating an empty pre-line. Non-whitespace text before the first `<lb/>` is retained and audited as a leading-text anomaly.

The retained surface is diplomatic rather than normalized:

- any subtree whose `decls` contains `#translation` is excluded;
- `<note>` subtrees are excluded because Casebooks uses them for margin/chart or other spatially separate note streams;
- `<reg>`, `<corr>`, and `<expan>` are excluded;
- within `<choice>`, select exactly one source-bearing branch using precedence `orig` > `sic` > `abbr`; if none exists, select the first child that is not `reg`, `corr`, or `expan`;
- visible contents of `del`, `add`, `unclear`, `hi`, `foreign`, `g`, `rs`, and ordinary inline elements remain in source order;
- no editorial translation is substituted for source Latin;
- no expansion of abbreviation glyphs or numeral/planetary symbols is invented.

Tokenization is the historical Phase62B Latin-control policy in definition: NFC normalize; a token is a maximal sequence of Unicode categories Letter or Mark; lowercase; combining marks remain attached to their preceding unit. Numerals and non-letter symbols do not become tokens.

## Structural S1 eligibility only

Gate0 computes no 8-feature vector and no projection. It only asks whether a paragraph could later be scored by the unchanged historical S1 geometry.

A paragraph is structurally eligible iff:

1. it has at least three retained physical lines;
2. line 0 and line 2 each have at least five tokens;
3. there exists at least one pseudo-boundary index `j` in `1 .. len(lines)-3` such that line `j` and line `j+2` each have at least five tokens.

This is the exact support logic of historical `base_eligible + valid_pseudo_indices`, stated without importing the target scorer.

## External replication metadata

Before scoring, report support by:

- source volume from `altIdentifier[@type='fn_number']/idno/@n`;
- hand set from `handNotes/handNote/@sameAs`;
- practice from `cb:practice/@name`;
- consultation class from `textClass/catRef/@target`.

These labels are descriptive authorities only. They cannot be altered after Gate0 based on later S1 values.

## Gate0 admission rule

Stage1 is licensed only if all are true:

- every case XML parses without fatal source/schema-transport error;
- at least 100 structurally eligible paragraphs;
- at least 100 distinct cases contain a structurally eligible paragraph;
- at least 5 source volumes each contribute at least 10 eligible paragraphs;
- at least 2 hand-set strata each contribute at least 20 eligible paragraphs.

The purpose is to ensure that a later result can be replicated beyond one pooled notebook or one writer stratum.

## Firewall

Gate0 must not:

- parse ZL3b or IT2a;
- import Phase62 S1 feature/projection code;
- compute `feature8`, training standard deviations, paragraph contrasts, fold directions, S1, sign counts, ratios to Voynich, or any R4 classification;
- select files, paragraphs, tokenization, source volumes, or hands based on S1 behavior.

Required output marker:

`NO ISSUE188 SCIENTIFIC S1 SCORE COMPUTED`

with `scientific_score_computed: false`.

## Stage1 if admitted

Only after Gate0 support/provenance is committed may a separate scorer be introduced. It must preserve this extraction exactly and replay the historical Phase62B/62C eight-feature S1 statistic/sign without candidate-specific rescue. Primary interpretation must include source-volume and hand-level replication, not only a pooled mean.
