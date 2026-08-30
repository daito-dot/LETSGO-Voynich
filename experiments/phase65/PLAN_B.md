# Phase 65B plan — sealed local image↔label content-relation test

Status: **FROZEN BEFORE ANY V1-P25 VISUAL↔TEXT ASSOCIATION METRIC IS COMPUTED.**

Parent authority:

- `DECISION_65.md`
- `PLAN_A.md`
- `ANCHOR_AUDIT_A.md` (`M8-ANCHOR READY`)

## 1. Scientific question

> Among physically attached pharmaceutical labels, are labels on visually more similar plant fragments themselves more similar under a generic frozen string distance than expected under row-constrained reassignment?

This is a **content-relation** test, not a translation test.

No plant species identification, plaintext hypothesis, dictionary, proposed decipherment, Naibbe mapping or A1 parameter enters the test.

## 2. Frozen anchor population

Start from V1-P25 fixed in Phase65A.

### Page P1 — f100v, 13 mapped units

- row `T`: T.1–T.4 (4)
- row `M`: M.1–M.5 (5)
- row `B`: B.1–B.4 (4)

### Page P2 — f102v2, 12 mapped units

- row `L2`: L2.1–L2.7 (7)
- row `L3`: L3.1–L3.5 (5)

The complete f102v2 top row L1.1–L1.7 remains excluded because its physical assignment was externally flagged as ambiguous before Phase65B.

No other Pharma object may be added after outcome inspection to improve power or result.

## 3. Two-stage physical holdout

The pages have different roles fixed before association scores.

### Primary sealed test — P2 / f102v2 lower rows

The first scientific reveal is owned by f102v2 rows L2 and L3.

Before this reveal:

- f100v may be used only for **image/crop/model pipeline engineering that never combines its labels with its images**;
- no f100v visual↔text correlation, retrieval score or label-assignment statistic may be computed;
- no f102v2 visual↔text statistic may be computed.

### Independent page replication — P1 / f100v

After the f102v2 primary result has been archived, the exact frozen executable is run on f100v without parameter, representation, threshold or preprocessing changes.

This second page result is required regardless of whether the primary passes or fails.

## 4. Source freeze before science

Phase65B0 must produce source-only manifests before any association metric.

### Manuscript images

Canonical image authority:

- Yale Beinecke MS 408 catalog: `https://collections.library.yale.edu/catalog/2002046`
- Yale IIIF manifest: `https://collections.library.yale.edu/manifests/2002046` (or the institutionally equivalent `/manifests/oid/2002046` endpoint if required by the live service).

For the exact f100v and f102v2 image bytes used, record before science:

- IIIF/canvas/image-service identifiers;
- retrieval URL;
- pixel width/height;
- byte size;
- SHA-256.

If Yale changes the image bytes after freeze, scientific workflow must fail rather than silently accept replacement bytes.

### Primary transcription — ZL3b

Reuse the existing pinned reference source:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- `ZL3b-n.txt` Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`.

Phase65B0 must record the exact label loci/strings selected for P25 without computing a visual association.

### Independent-transcription sensitivity — IT2a / Takeshi Takahashi EvaT

Use the same canonical IT2a source lineage frozen in Phase63B:

- `https://www.voynich.nu/data/IT2a-n.txt`

Before science, record exact downloaded byte SHA-256, byte size and IVTFF header. If the source changes between manifest freeze and sensitivity execution, fail.

IT2a does not own the primary verdict; it tests whether a result is an artifact of one EVA-family reading.

## 5. Crop freeze and text blindness

The content-side image must not contain the associated label.

Create `CROP_MANIFEST_B.json` before science. For every retained unit record:

- page;
- row/locus/object ID;
- source image SHA-256;
- integer pixel crop rectangle `(x, y, width, height)`;
- whether any page edge/fold/other plant enters the crop;
- crop PNG SHA-256.

### Crop rule

Each crop must contain exactly one intended plant fragment and **no label glyphs**.

Crop rectangle is chosen from the visible fragment boundary alone. It may include surrounding parchment. It must not be shifted/resized after observing any label-distance result.

A unit is excluded before science if a text-blind crop audit finds any of:

1. associated label glyphs enter the crop;
2. a second plant fragment substantially overlaps the crop such that the intended object cannot be isolated;
3. the intended fragment is materially truncated by scan/page damage beyond what is inherent in the manuscript object itself;
4. the object↔label physical assignment is newly found to be ambiguous under the Phase65A A3 rule.

No exclusion may depend on the label string or DINO/text distance.

### Coverage firewall

After crop-quality and transcription-confidence exclusions, Phase65B may proceed only if:

- total retained P25 units >=20;
- primary f102v2 retains >=8 units total;
- each primary row retains >=4 units;
- f100v replication retains >=8 units total and each retained row used in the statistic has >=3 units.

Otherwise classify `M8-B1 BLOCKED_BY_INPUT_QUALITY` before content scoring.

## 6. Frozen visual representation

Primary visual representation = **Meta DINOv2 ViT-S/14, pretrained LVD-142M backbone, no fine-tuning**.

Exact code source:

- repository `facebookresearch/dinov2`
- commit `7764ea0f912e53c92e82eb78a2a1631e92725fc8`
- primary model entrypoint `dinov2_vits14`
- official weight URL `https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_pretrain.pth`.

Phase65B0 must download the weights, record SHA-256/size, and freeze that identity before science. The scientific workflow must verify it.

Rationale: DINOv2 is a fixed external self-supervised vision representation trained without Voynich labels or this experiment. ViT-S/14 is chosen as the smallest official standard backbone sufficient for a 25-image representation test; there is no model selection across DINO variants after seeing outcomes.

### Deterministic preprocessing

For each already-frozen plant crop:

1. decode as RGB;
2. pad to a square, centered, using constant RGB `(255,255,255)`; do not crop away content;
3. resize the full square to exactly `518 x 518` using bicubic interpolation;
4. convert channels to `[0,1]` float;
5. normalize with ImageNet mean `(0.485,0.456,0.406)` and std `(0.229,0.224,0.225)`;
6. inference mode, no augmentation;
7. representation = `model.forward_features(x)["x_norm_clstoken"]` (384-D for ViT-S/14);
8. L2-normalize the 384-D vector.

Primary visual distance:

`D_visual(i,j) = 1 - cosine(embedding_i, embedding_j)`.

No PCA, feature selection, fine-tuning, learned metric or page-specific normalization is allowed.

### Predeclared grayscale sensitivity

Repeat the same representation after deterministic luminance conversion of each crop and replication to three channels. This tests whether any result depends primarily on pigment/color rather than form. It does not own primary pass/fail.

## 7. Frozen text representation

Primary text source = pinned ZL3b Basic EVA.

The representation is deliberately generic and parameter-free.

### IVTFF confidence firewall

Reuse the Phase63B rule:

- exclude any label whose source representation contains `?` unreadable glyphs;
- exclude any label whose source representation contains `[ ... ]` alternative readings.

Do not choose a preferred uncertain reading.

### W1 primary segmentation

Interpret IVTFF label text using the Phase63B conservative-space convention:

- `.` = boundary;
- `,` = boundary;
- `<->` = boundary;
- `<~>` = boundary;
- comments/tags are removed;
- braces are structural only and enclosed glyph units remain;
- ASCII EVA letters canonicalized to lowercase;
- `@NNN;` remains one atomic glyph unit.

Represent a multi-token label as one glyph-unit sequence with one explicit boundary unit `|` between tokens.

### Primary text distance

`D_text(i,j) = Levenshtein(sequence_i, sequence_j) / max(len(sequence_i), len(sequence_j))`.

Both sequences are nonempty by input rule.

Levenshtein cost is exactly 1 for insertion, deletion or substitution. No Voynich-specific glyph weights, morphology, stems, prefix/suffix parse or learned edit costs are allowed.

### W2 segmentation sensitivity

As in Phase63B, uncertain comma spaces are removed without inserting a boundary; definite/drawing spaces remain boundaries. Recompute the same normalized Levenshtein statistic. W2 does not own primary pass/fail.

### Length-only diagnostic

Also report:

`D_len(i,j) = abs(len_i - len_j) / max(len_i, len_j)`.

This diagnostic asks whether any visual↔text relation is explainable by label length alone. It does not replace the primary distance.

### IT2a sensitivity

On independently transcribed IT2a label strings, apply the same confidence firewall, W1/W2 parsing and normalized Levenshtein distance. Missing/unusable IT2a units are reported; no unit is substituted from ZL to improve the IT result.

## 8. Primary statistic: stratified distance concordance

Never compare across rows in the primary statistic.

For each retained row separately:

1. take all unordered image pairs inside the row;
2. compute `D_visual` and `D_text` for those pairs;
3. compute Spearman rank correlation `rho_row` between the two distance vectors.

Combine row correlations with fixed pair-count weights:

`T = sum_r [ C(n_r,2) * rho_r ] / sum_r C(n_r,2)`.

For intact f102v2 this is 21 pairs in L2 + 10 in L3 = 31 pair observations for the weighted statistic.

Interpretation: positive T means visually close plant fragments tend to have textually close labels within the same physical row.

## 9. Exact row-constrained permutation null

The null is physical label reassignment **within each row only**.

For f102v2 intact rows:

- L2: `7!`
- L3: `5!`
- joint exact null: `7! * 5! = 604,800` assignments.

Enumerate every joint within-row assignment exactly. For each assignment, recompute the text-distance pairing and T with visual distances fixed.

If confidence/crop filtering reduces row sizes, enumerate the full Cartesian product of the retained row permutations exactly. Do not switch to Monte Carlo unless the exact space exceeds 5,000,000; under the frozen P25 sizes it does not.

One-sided exact p-value:

`p_exact = #{T_perm >= T_observed} / N_permutations`.

The identity assignment is part of the exact permutation space.

No asymptotic p-value owns any claim.

The same row-constrained exact procedure is used for f100v replication. With intact 4/5/4 rows the exact space is `4! * 5! * 4! = 69,120`.

## 10. Frozen pass/fail thresholds

A page **passes** its content-relation gate only if both:

1. `T_observed >= 0.20`;
2. `p_exact <= 0.05`.

The effect-size floor prevents promotion of a statistically unusual but substantively tiny concordance.

No threshold is changed after the f102v2 reveal.

## 11. Phase65B classification

Exactly one primary classification is assigned after both frozen page runs.

### `M8-B1 REPLICATED CONTENT RELATION`

- f102v2 primary passes; and
- f100v replication passes.

Interpretation:

> Under a fixed external visual representation and generic string metric, physically attached labels show a replicated local relation to plant-fragment visual morphology beyond row-constrained reassignment.

This advances the project from mechanism evidence to a genuine **content relation**. It does not identify plaintext, language, cipher key or historical mechanism.

### `M8-B1 PRIMARY-ONLY CONTENT RELATION`

- f102v2 primary passes;
- f100v replication fails.

Interpretation: localized relation is prospectively detected on the sealed primary page but does not independently replicate; retain as tentative/heterogeneous evidence.

### `M8-B1 REPLICATION-ONLY / NONCONFIRMATORY`

- f102v2 primary fails;
- f100v replication passes.

Interpretation: the predeclared primary test failed. The later page signal is secondary and cannot be promoted to confirmed content relation.

### `M8-B1 NO DETECTED MORPHOLOGY RELATION`

- neither page passes.

Interpretation is narrow:

> The tested visual-morphology ↔ generic-label-form relation was not detected under the frozen design.

This is **not** evidence that labels lack semantic content. Plant names, ingredients, quantities, properties or coded identifiers need not be morphologically close when the drawings are visually close.

### `M8-B1 BLOCKED_BY_INPUT_QUALITY`

Assigned before scoring if the frozen coverage/source/crop requirements fail.

## 12. Sensitivities and diagnostics — non-owners of primary verdict

Always report, without repairing the primary result:

- grayscale DINOv2 visual distance;
- ZL W2 segmentation;
- IT2a W1 and W2 where coverage permits;
- length-only text distance;
- per-row rho values;
- all retained/excluded unit IDs and exact exclusion reason;
- visual-distance and text-distance matrices;
- permutation distribution quantiles.

If a primary pass reverses under most sensitivities, retain the frozen classification but explicitly downgrade interpretation and diagnose the dependency.

## 13. Anti-leak / no-repair rules

Before the first f102v2 association reveal, prohibited:

- computing any P25 image↔label correlation under another image model to choose DINOv2;
- selecting among DINOv2 S/B/L/g or register variants by result;
- adjusting crop boxes based on label strings or association metrics;
- selecting a text metric because it scores better than normalized Levenshtein;
- choosing EVA glyph groups, prefixes/suffixes, stems or semantic guesses from P25 labels;
- rotating/reassigning object-label mappings;
- adding ambiguous f102v2 top-row units for power;
- adding other Pharma pages after seeing the primary result;
- fitting a visual-to-text mapping on f100v;
- changing `T >= 0.20` or `p <= 0.05` after reveal.

After f102v2 reveal and before f100v replication, **no scientific code or parameter may change**. Only provenance/documentation that cannot affect computation may be added.

## 14. Required execution chronology

1. merge Phase65A audit and this plan to main;
2. create a fresh Phase65B implementation branch from that main;
3. perform Phase65B0 source/model/image/crop/transcription preflight with science disabled;
4. freeze `SOURCE_MANIFEST_B.json`, `CROP_MANIFEST_B.json`, exact DINO weight hash and executable identity;
5. run a synthetic-only preflight proving parser, DINO path and exact permutation enumeration without reading P25 association outcomes;
6. authorize f102v2 primary first reveal only;
7. archive raw JSON + hashes + exact workflow/job provenance;
8. with no scientific changes, run f100v replication;
9. archive replication raw JSON + hashes;
10. write `REPORT_B.md`, update formal research state, exact-replay if feasible, then converge to main.

## 15. Claim boundary

Even the strongest possible Phase65B result would establish only that **label form covaries locally with an independently measured visual property of the attached drawing**.

It would not establish:

- that the labels are plant names;
- that similar strings share a specific morpheme or phonetic value;
- that N or C is true and G false;
- that A1 is the historical production mechanism;
- a translation or decipherment.

A replicated positive would, however, force future mechanism families to explain not only Voynichese-internal structure but also a prospective external image↔text relation at object resolution.
