# Phase 65A anchor audit — independently grounded localized content candidates

Status: **COMPLETE — `M8-ANCHOR READY`**.

This audit applies the preregistered A1–A6 admission gates in `PLAN_A.md`. No new Voynichese content statistic was computed in Phase65A. The audit used manuscript layout/images, existing descriptive/transcription metadata, prior repository history and external historical/scholarly sources only.

## Result

At least one candidate population passes all frozen gates:

> **V1-P25 — 25 physically localized pharmaceutical plant-fragment ↔ adjacent-label pairs from f100v and the unambiguous lower two rows of f102v2.**

This is sufficient to open a separately preregistered Phase65B content-relation experiment.

The result does **not** mean that the labels have been shown to encode plant morphology, plant names or any semantic content. It means only that a clean test is now executable without inventing a semantic identification.

## Source/provenance record

| Source | Role in audit | What is accepted from it |
|---|---|---|
| Yale Beinecke, MS 408 collection page, `https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript` | manuscript authority / broad section identity | MS 408 is the Voynich manuscript; the relevant leaves belong to the pharmaceutical/herbs-and-roots illustrated material. No proposed reading is taken from Yale. |
| René Zandbergen, Quire 19, `https://www.voynich.nu/q19/index.html` | current folio/object counts and cross-reference numbering | f100v has 13 herb fragments and 13 plant-fragment labels; f102v2 has 19 herb fragments and 19 plant-fragment labels; other Quire-19 pages often have count mismatches or missing labels and are therefore not automatically one-to-one. |
| VIB/Stolfi f100v, `https://vib.tamagothi.de/index.php?id=f100v&show=page` | legacy object-row/label-locus geometry and independent descriptive notes | three f100v rows contain 4, 5 and 4 plant-label loci, with image-side descriptors such as leaf/root/inflorescence morphology. |
| VIB/Stolfi f102v2, `https://vib.tamagothi.de/index.php?id=f102v2&show=page` | legacy object-row/label-locus geometry and ambiguity warning | rows contain 7, 7 and 5 plant-label loci. The source explicitly warns that the **first three top-row labels may attach to the leaf at left rather than right**. Therefore the entire top row is excluded before any text metric. Rows 2 and 3 have no corresponding pairing warning in this source. |
| `phase3_visual_pair_results_ja.md` / `phase3_visual_pair_test.py` retained project evidence | contamination audit | prior Phase3 used f102r2 [3,1], f102v1 [2,3], f102r2 [3,2], f89v3 [3,4], f89v3 [1,5] (plus documented legacy-coordinate sensitivities), not f100v or f102v2. Phase3 asked whether visually matched Herbal↔Pharma pairs showed cross-page label-substring recurrence; it did not test local morphology↔own-label geometry. |
| University of Cologne teaching/research pages on Voynich botany, `https://voynichsc.uni-koeln.de/pages/06-botanik/` and 2026 course material | V3 named-species caution | published plant identifications are strongly contradictory; no consensus named-species population is imported as a primary anchor. |
| Zandbergen zodiac descriptions, `https://www.voynich.nu/illustr.html`, `q10/index.html`, `q11/index.html`, `q12/index.html`, `extra/labels.html` | V2 zodiac audit | zodiac diagrams usually contain 30 nymph/star/label units; Aries/Taurus are split into two 15-unit panels; 299 zodiac labels survive. This supports a degree-like interpretation as a candidate family but not a unique degree-number alignment. |
| al-Biruni, *The Book of Instruction in the Elements of the Art of Astrology*, Wright 1934; open bibliographic copy at `https://opendata.uni-halle.de/handle/1981185920/101870` | external historical degree-table existence | medieval degree-property tables exist independently of Voynichese. Their existence does not by itself determine which Voynich nymph is degree 1, direction of traversal or ring order. |

No source's proposed Voynichese plaintext is accepted as an anchor.

## V1 — localized image-object ↔ adjacent-label pairs

### Candidate V1-P25 population

The primary auditable population is fixed as follows.

#### f100v — 13 pairs

All three plant rows:

- row 1: `T.1–T.4` — 4 pairs;
- row 2: `M.1–M.5` — 5 pairs;
- row 3: `B.1–B.4` — 4 pairs.

Total: **13**.

The current Quire-19 description independently reports 13 herb fragments and 13 plant-fragment labels on f100v. The VIB layout records exactly 4/5/4 label loci in the three rows. It also records image-side morphology variation, for example a toothed-leaf/dark-root form, an inflorescence-or-berries/round-leaf form, and a dark-leaf/light-root form. These descriptions are used only to establish that the external visual target is nonconstant, not as hand-engineered text-correlated features.

#### f102v2 — 12 pairs

Retain only:

- row 2: `L2.1–L2.7` — 7 pairs;
- row 3: `L3.1–L3.5` — 5 pairs.

Total: **12**.

Exclude the complete top row `L1.1–L1.7` before any Phase65B score because the legacy source explicitly states that the first three labels may attach to the leaf at left rather than at right. We do not resolve that ambiguity by inspecting strings or by choosing the visually/textually favorable direction.

Combined V1-P25 total: **25 localized units**.

### Why not use more pharmaceutical units now

The audit deliberately does not maximize sample size. Several Quire-19 pages have fragment/label count mismatches or missing labels:

- f99r: 27 fragments / 30 plant-fragment labels;
- f99v: 20 / 21;
- f100r: 16 / 17;
- f101r: 29 fragments / no labels;
- f101v: 28 / 18;
- f102r1: 4 / 1;
- f102r2: 9 / 2.

Those pages may contain useful individual mappings, but importing them would require a new object-level mapping audit and adds ambiguity freedom. V1-P25 already clears A5, so they are not needed for the primary test.

### A1–A6 admission

| Gate | Verdict | Reason |
|---|---|---|
| A1 source independence | **PASS** | The external target can be constructed from text-blinded image crops of the physical plant fragments. No species name or Voynichese reading is needed. Object inclusion was chosen from layout/count/ambiguity evidence, not from string similarity. |
| A2 physical localization | **PASS** | Each retained unit is a specific fragment and its adjacent row-local label locus, below page/section level. |
| A3 mapping ambiguity | **PASS for restricted P25** | f100v has matching 4/5/4 row counts and no recorded pairing warning; f102v2 top row is discarded because of the explicit warning, leaving matching 7/5 lower-row loci with no corresponding warning. Phase65B must still verify crop geometry without reading text and reject any newly discovered ambiguous unit before reveal under a predeclared rule. |
| A4 content specificity | **PASS** | Plant-fragment image morphology varies in leaf outline, serration, root geometry, stem/inflorescence structure, fill/paint and overall form. A fixed image representation can therefore define a continuous/multivariate external target without naming species. |
| A5 prospective population | **PASS** | `n=25 >= 20`. More strongly, f100v (13) and f102v2 rows 2–3 (12) provide a natural physical-page holdout split, while row structure supports exact within-row label permutation. |
| A6 contamination control | **PASS with explicit qualification** | Phase3's five Pharma coordinates are on f102r2/f102v1/f89v3, not V1-P25. Phase3 tested cross-section substring recurrence in visually matched Herbal prose; Phase65B will test the relation between each local fragment's text-blinded visual morphology and its own adjacent label. Phase58's page-level visual tests were also coarser and did not test these object-local pairs. |

**V1-P25 admission: PASS.**

## Contamination disclosure

While auditing VIB layout, the source page incidentally displays Basic-EVA transcriptions beside the row loci. No candidate-wide text statistic, pairwise string distance, visual-text association, clustering or content score was computed in Phase65A, and no unit was admitted or rejected because its string looked favorable.

Because the strings were not literally hidden from the auditor, Phase65B must be especially conservative:

1. freeze the text representation from generic/pre-existing principles before computing any P25 visual-text association;
2. do not hand-select glyph/string features from the displayed labels;
3. freeze the visual representation independently of the label strings;
4. preserve the page/row holdout and exact permutation null before first result.

## V2 — zodiac / degree anchors

### V2a — central zodiac-sign identity

External sign identity is often visually clear and each sign has a localized diagram, but the population structure is insufficient for the frozen A5 class-design gate:

- most preserved signs have one diagram;
- Aries and Taurus alone are split into two 15-unit panels;
- treating each sign as a class therefore does not provide >=4 physically distinct units per class, and repeated-sign evidence is too sparse for the frozen repeated-identity rule.

**V2a: FAIL A5.**

### V2b — individual zodiac degree identity/properties

The diagrams usually have 30 nymph/star/label combinations and are plausibly related to degree astrology/paranatellonta. Medieval external sources such as al-Biruni provide degree-specific properties. This makes V2b scientifically interesting.

However, the required per-degree mapping is not presently fixed independently enough for a primary anchor. The manuscript does not provide unambiguous explicit degree numbers, and historical/research discussions differ over traversal start, ring order and clockwise/counter-clockwise assignment. A recent independent preprint reports a visually aligned al-Biruni-degree signal, but its degree shift/alignment is itself an inferred mapping and its own later analysis notes that a coarse 15+15 visual partition can match or exceed the fine degree-sex interpretation. That is useful prior art, not an independent physical numbering authority for this project.

Therefore Phase65A does not import a favorable rotation/shift/order after comparing visual attributes or Voynichese labels.

- A1: historical degree tables themselves pass independence;
- A2: nymph↔label localization is strong;
- **A3: FAIL for exact degree-number assignment under the current evidence**;
- A5 would otherwise be ample.

**V2b: NOT ADMITTED / secondary research opportunity pending an independently fixed numbering rule.**

This rejection is important: the audit does not use the attractive `30 figures = 30 degrees` structure as permission to optimize a circular alignment.

## V3 — independently named botanical objects

Specific species identifications would be highly interpretable if independently secure, but the frozen source-independence requirement is not met by the current literature survey.

The Yale collection description identifies broad illustrated domains, not plant species. University of Cologne's Voynich botany material explicitly notes that published plant-identification works strongly contradict one another. Tucker/Janick and related publications provide extensive specific identifications, but they form a particular contested Mesoamerican-origin program rather than a cross-source consensus population. Importing those names as ground truth would make the content test depend on a disputed identification system.

No >=20 or >=3×4 named-object population satisfying both independent support and exact physical localization was located under the frozen standard.

**V3: FAIL A1 / A5 as a primary named-object anchor.**

This does not assert that no individual Voynich plant is identifiable. It means only that Phase65A has not found a sufficiently independent named-species ground-truth population for a prospective test.

## Phase65A classification

> **`M8-ANCHOR READY`**

Reason: V1-P25 passes all frozen A1–A6 gates. V2 and V3 are retained as negative/secondary candidates rather than used to inflate the conclusion.

## What has actually advanced

Before this audit, the content lane was blocked because prior tests were broad page-level or relied on contested visual/name matches. V1-P25 creates a different bridge:

`physical fragment image` ↔ `adjacent isolated label`

with no requirement to know what either one is called.

This is valuable because it asks a falsifiable content-relation question without attempting decipherment:

> **Do labels attached to visually more similar plant fragments become more similar under a generic frozen string representation than expected under physically constrained label reassignment?**

A positive result would show a localized relation between external image content and label form. It would not by itself tell us the semantic dimension or plaintext.

A negative result would be narrower: it would reject the tested morphology↔label-form relation, not semantic content in general. Plant names can be semantically meaningful while being weakly related to visual similarity, and labels could encode properties other than morphology.

## Required next step

No P25 content statistic may be computed yet.

A separate `PLAN_B.md` must first freeze:

- exact P25 object crops and exclusion rule;
- a text-blind visual representation;
- a generic text representation chosen without P25 outcome inspection;
- f100v/f102v2 physical holdout role;
- within-row exact permutation null;
- primary statistic, sensitivity and pass/fail rule;
- source/model hashes and deterministic implementation details.

Only after that freeze is merged may Phase65B science reveal begin.
