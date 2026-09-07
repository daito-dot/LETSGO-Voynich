# Issue #188 — R4 / Casebooks score-free Gate0 plan

Date: 2026-09-08  
Parent: Issue #172, Priority 1  
Base main: `544a3ae97001ff4ea8c353bde805aee7a1157005`

## External authority

- repository: `CasebooksProject/casebooks-data`
- pinned commit: `9d42295d72b5ba8889575a32d79311cc72bce73a`
- population: every `cases/CASE*.xml` file at that commit
- external architecture: raw XML transcriptions of the medical/astrological case records of Simon Forman and Richard Napier, 1596–1634

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

### DTD transport rule

The first GitHub Actions attempt was terminated by the hosted runner while repeatedly resolving the same external entity DTD across the ~80,000 files. It produced no support result and no scientific score.

For Gate0 transport only, each XML byte stream is therefore made standalone before parsing:

1. remove the document's `DOCTYPE` declaration that references `../schema/entities.dtd`;
2. preserve the five XML predefined entities (`amp`, `lt`, `gt`, `quot`, `apos`);
3. replace every other named entity reference with one Private Use placeholder character;
4. parse the resulting XML as ordinary namespace-preserving XML;
5. count and report how many named entity references were replaced.

The placeholder is Unicode category `Co`, so it cannot become a Letter/Mark token. This is deliberately equivalent to treating unexpanded source entity glyphs as opaque non-letter symbols. No entity is expanded into normalized alphabetic text. This transport change is licensed only because the first run terminated before emitting any support/S1 result; it does not alter paragraph/line selection, token rules, admission thresholds, or the scientific representation after reveal.

## Structural S1 eligibility only

Gate0 computes no 8-feature vector and no projection. A paragraph is structurally eligible iff:

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

- every standalone-transformed case XML parses without fatal transport error;
- at least 100 structurally eligible paragraphs;
- at least 100 distinct cases contain a structurally eligible paragraph;
- at least 5 source volumes each contribute at least 10 eligible paragraphs;
- at least 2 hand-set strata each contribute at least 20 eligible paragraphs.

## Firewall

Gate0 must not parse ZL3b or IT2a, import Phase62 S1 feature/projection code, compute feature8/contrasts/fold directions/S1/signs/ratios/R4 classifications, or select files/paragraphs/tokenization/metadata strata based on S1 behavior.

Required output marker:

`NO ISSUE188 SCIENTIFIC S1 SCORE COMPUTED`

with `scientific_score_computed: false`.

## Stage1 if admitted

Only after Gate0 support/provenance is committed may a separate scorer be introduced. It must preserve this extraction exactly and replay the historical Phase62B/62C eight-feature S1 statistic/sign without candidate-specific rescue. Primary interpretation must include source-volume and hand-level replication, not only a pooled mean.
