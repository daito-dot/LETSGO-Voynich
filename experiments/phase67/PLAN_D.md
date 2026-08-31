# Phase 67D — image morphology -> formal-residual lexical-family selection

Status: **FROZEN BEFORE LEXICAL-FAMILY MORPHOLOGY↔TEXT ASSOCIATION**

Date: 2026-08-31

## Motivation and sequential status

Phase67C removed paragraph line-0 tokens and all non-line0 tokens directly compatible with the established preceding-10 edit1 formal channel. The remaining 423/685 cleaned tokens still showed no image relation when represented by character n-grams.

A distinct live model remains: semantic/content information may be carried primarily by **which lexical/token family is selected**, while the detailed character realization of those families is shaped by formal Voynichese processes.

Phase67D therefore changes the text representation, not the image hypotheses or block population:

> Do the sealed image morphology distributions predict which edit1 lexical families are selected among the Phase67C retained innovation tokens?

This test is adaptive, because it follows the observed Phase67A–C nulls. Any positive result is a candidate only and requires independent replication.

## Frozen population and inputs

Reuse unchanged:

- `BLOCK_MANIFEST_A.json`
- `TEXT_TABLE_A.json`
- `IMAGE_ANNOTATION_A.json`
- `ROOT_ANNOTATION_B.json`
- the exact Phase67C formal mask: paragraph line0 masked; non-line0 token masked when it is non-identical Levenshtein distance 1 from any previous ten cleaned folio tokens; every cleaned token still enters history.

No image state, paragraph boundary, cleaning rule, mask rule, or ten-token history rule may change.

## Primary lexical-family representation

Let `V` be the sorted set of all distinct `INNOVATION_RETAINED` token types across the 14 frozen paragraphs.

For each paragraph and each vocabulary type `v in V`, define the closed edit1-family count:

`c_v = number of retained token occurrences t in the paragraph for which (t == v) OR lev1(t, v)`.

Thus exact identity and one-edit relatives count as membership in the same local lexical neighborhood. No distance weighting or fitted parameter is used.

Convert the paragraph's `c_v` vector to proportions by dividing by `sum_v c_v`, then apply the Hellinger transform `sqrt(p)`. A paragraph with zero retained tokens receives an all-zero vector.

This representation deliberately allows overlapping families; it does not impose arbitrary connected-component clustering on the dense Voynich edit1 graph.

## Image predictor family

Exactly the four already sealed characters from Phase67C:

1. leaf composition
2. leaf arrangement
3. leaf margin
4. root/subterranean architecture

Use the same Hellinger state-distribution vectors and per-character usable-block rules as Phase67A–C.

## Folio control and statistic

For each image character separately:

- keep its usable blocks;
- retain only folios with at least two usable blocks;
- subtract folio means from both image and lexical-family vectors;
- compute the normalized RV coefficient.

Primary family statistic:

`T = max(RV_leaf_composition, RV_leaf_arrangement, RV_leaf_margin, RV_root_architecture)`.

## Exact null

Permute complete lexical-family paragraph vectors among blocks within folio only.

Enumerate all:

`4! * 3! * 2! * 1! * 2! * 2! = 1,152`

assignments, identity included. Recompute all four RVs and the four-way maximum.

Primary exact p-value:

`p = count(T_perm >= T_obs) / 1152`.

## Coverage gate

A candidate requires:

1. global exact p <= 0.05;
2. winning character >=8 centered usable blocks;
3. >=3 contributing folios.

If it passes, the classification is only:

`CANDIDATE LEXICAL-FAMILY IMAGE↔BODY ASSOCIATION — INDEPENDENT REPLICATION REQUIRED`.

## Retention nuisance control

Use the exact Phase67C retained-token fraction for each paragraph.

For every image character:

- compute retention-only RV between centered image matrix and centered retention fraction;
- residualize the centered lexical-family text matrix on centered retention fraction with no intercept;
- compute residualized image↔text RV;
- repeat the full 1,152 exact null and a four-way residual maxT.

If primary p<=0.05 and the primary winner's retention-only p<=0.05, require residualized global p<=0.05 and its coverage gate; otherwise classify `TEXT-RETENTION CONFOUNDED`.

## Frozen secondary: exact-token identity

As a stricter sensitivity, repeat the same analysis with a paragraph vector over exact retained token types only:

- coordinate = retained occurrence count of exactly that vocabulary type;
- convert to proportions;
- Hellinger transform;
- same folio centering, four image characters, 1,152 exact null, maxT and retention control.

This exact-token representation is secondary and cannot rescue a failed primary closed-edit1-family test.

## Falsification rule

Primary global p>0.05 => `NOT SUPPORTED`.

Do not tune neighborhood radius, family weight, vocabulary filtering, image character set, retention rule, or null after reveal.
