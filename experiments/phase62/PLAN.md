# Phase 62 — first fair N/C/G model-family tournament

Status: **frozen design before N0/B0 tournament scoring**.

Phase61C kept G/A1 structurally viable after exactly one local-family repair. Phase62 does not extend A1. It asks whether meaningful structured medieval text, with or without a bounded global recoding, can achieve comparable structural fit at lower target dependence / complexity.

## Scientific question

Among the currently viable families,

- **N0** — source-native meaningful structured medieval text;
- **C0/B0** — the same text after a bounded, reversible, global, boundary-blind recoding;
- **G/A1** — the frozen Phase61C nonsemantic generator;

which family places the same cross-representation structural targets in the Voynich regime most efficiently, and what extra machinery is required?

This phase is a **mechanism-family comparison**, not a semantic identification or decipherment test.

## Frozen inputs

### Voynich

Primary transcription:

- ZL3b/EVA v3b, 2025-05-13
- expected Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- reproducible public mirror: `matthewdgreen/cipher_benchmark`
- frozen mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`

The external transcription is not redistributed by this repository.

### Medieval structured-text controls

External corpus:

- `HTR-United/CREMMA-Medieval-LAT`
- frozen commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- graphematic medieval Latin manuscript transcriptions

The source-recovery audit and rationale are frozen in `CONTROL_RECOVERY.md`.

### Primary N0 panel

The primary panel was selected by an objective corpus-wide rule committed before its counts were inspected:

> all immediate CREMMA manuscript directories with at least 5 eligible literal-pilcrow entries under the frozen Phase62 enumeration rule.

Resulting manuscripts:

1. BIS 193 — scholastic — 64 eligible entries;
2. CLM 13027 — medical — 39;
3. Mazarine 915 — scholastic — 38;
4. UBL 758 — ecclesiastical — 5.

All eligible entries are used. There is no manual semantic sub-selection inside these manuscripts.

**Replication/aggregation unit is manuscript, not entry.** Manuscripts receive equal primary weight so BIS193 cannot dominate by entry count.

### Predeclared sensitivities

- H318 — medical/recipes — 4 eligible literal-pilcrow entries; excluded from the primary >=5 rule but retained as a Phase52-preexisting sensitivity.
- Arras 861 — literary — no literal-pilcrow eligible entries; retained for non-entry line-position/document sensitivity only.

Neither sensitivity can be promoted into or removed from the primary panel after tournament results are seen.

## Entry segmentation

For structured medieval controls, a source-native item begins at a literal `¶` marker and extends until the next literal pilcrow in the same file or file end.

- line0 = post-pilcrow text on the marker's physical transcription line;
- later lines = following physical transcription lines until the next marker/file end;
- primary entry eligibility = at least 3 item lines and at least 5 usable tokens on line0 and line2;
- internal pseudo-boundaries are `j -> j+2`, `j>=1`, within the same item and with >=5 tokens on both compared lines.

No Latin wording or semantic interpretation is used to create boundaries.

Voynich paragraphs continue to use the explicit ZL3b `<%>` paragraph markers and the audited physical-leaf grouping.

## Cross-representation token units

Primary comparison is graphematic and representation-neutral:

- Voynich raw EVA token characters are units;
- medieval Latin tokens are NFC grapheme units, with combining marks attached to the preceding base unit where applicable;
- punctuation/separators are not token units;
- medieval abbreviation graphemes are retained, not expanded.

## Primary common feature vector — 9D

Literal Voynich-specific `{k,t}` dimensions are excluded from the primary N/C/G tournament because they have no invariant cross-language analogue.

For each line, use:

1. type-token ratio;
2. mean token length in graphematic units;
3. token-length SD;
4. unit inventory size;
5. unit entropy;
6. first-unit entropy;
7. last-unit entropy;
8. within-line edit-distance-1 token-family fraction;
9. local previous-10 edit-distance-1 fraction.

### Sample-size-neutral primary representation

To prevent line-token-count artifacts from becoming model-family evidence, the **primary 9D score uses exactly the first five usable tokens of every eligible line**.

Source-native full-line values are retained only as a sensitivity / continuity analysis.

This fixed-five rule is frozen before N0/C0 scores are inspected.

## Primary structural scorecard

All families are evaluated on the same three dimensions.

### S1 — entry-specific generic projection

Within each outer Voynich physical-leaf fold:

1. learn feature SDs and the 9D real-entry-minus-internal-pseudo direction using **Voynich training leaves only**;
2. score held-out Voynich entries on that direction;
3. score every external manuscript/model output on the same frozen direction and scaling;
4. aggregate external entries within manuscript first, then aggregate manuscripts equally.

Primary quantity: model / held-out-Voynich entry projection ratio.

Also report the full 9D vector, cosine to the Voynich direction, and source-standardized transition norm. These are secondary diagnostics and cannot replace S1 after results are seen.

### S2 — local near-family activation beyond document inventory

Report the raw within-line previous-10 near-family fraction and a locality excess relative to a deterministic permutation null that:

- pools tokens within each manuscript/document realization;
- preserves the number of tokens in every physical line;
- randomly redistributes the document's existing tokens across line/token slots;
- therefore preserves the document vocabulary and line-length layout while destroying local lexical-family activation.

Use 100 deterministic null replicates per manuscript/model realization.

Primary S2 quantity: observed minus null-median local-prev10 fraction, compared with the equivalently computed held-out Voynich value.

### S3 — generic line-position grammar

Compute eta-squared for each of the nine common features across item/paragraph line-position groups:

- line0;
- line1;
- line2;
- line3+.

Primary quantity: mean eta2 over the nine dimensions. Report max and per-dimension eta2 as diagnostics.

## Secondary scorecard

These are reported but cannot override the frozen S1–S3 decision:

- source-native full-line S1–S3;
- entry transition norm;
- entry-direction cosine;
- edit1 token-type density;
- number of token types / graphematic units;
- manuscript-to-manuscript heterogeneity;
- predeclared H318 and Arras sensitivities.

Edit1 type density is especially important as a **target-dependence diagnostic**: it is independent for raw N0/C0 source vocabularies but is not an independent A1 prediction because A1 is supplied the empirical Voynich token vocabulary.

## N0

N0 is the unencoded source-native structured manuscript text under the fixed extraction/feature rules above.

No parameter is tuned to Voynich.

Primary family aggregation:

- calculate each metric per manuscript;
- give BIS193, CLM13027, Mazarine915 and UBL758 equal weight;
- report all manuscript values individually;
- do not select the best matching manuscript as the primary N0 result.

## C0/B0 — bounded boundary-blind recoding family

C0 starts from the exact N0 items and may use only the following **predeclared reversible transforms**. All operate independently inside each token and cannot inspect document, entry, paragraph, line number, Voynich section, or Voynich boundary labels.

### C0-0 — identity / monoalphabetic-equivalent

No structural recoding. Any one-to-one grapheme renaming is structurally equivalent on the generic scorecard and is represented by identity.

### C0-1 — token reversal

Reverse graphematic unit order within every token. This is a fixed reversible transposition and tests whether edge orientation rather than document grammar explains mismatch.

### C0-2 — positional allography, 2 classes

Replace each graphematic unit `g` by an abstract reversible pair `(g, class)`, where class is:

- initial;
- non-initial.

The mapping is global and token-position-conditioned only.

### C0-3 — positional allography, 3 classes

Replace each unit by `(g, class)` with classes:

- initial;
- medial;
- final/singleton (singleton is deterministically distinguishable within the encoded unit definition if needed for reversibility).

No line/entry state is available.

### C0-4 — non-overlapping digraph coding

Encode token units left-to-right into reversible non-overlapping pairs, with a final singleton unit when token length is odd. Each encoded unit contains its exact source unit(s), so decoding is unique.

### C0 model selection

The family contains exactly five alternatives C0-0…C0-4.

Within each outer Voynich physical-leaf fold, select one transform using Voynich **training** targets only, minimizing equal-weight mean squared relative error over S1, S2 and S3 after manuscript-level equal weighting.

Evaluate the selected transform against held-out Voynich targets. The held-out fold cannot choose the transform.

No transform parameters beyond the five-class choice are fitted to Voynich.

A later, more expressive cipher is **C1**, not a repair inside C0, and may be proposed only after C0 is frozen and interpreted.

## Frozen G/A1 competitor

A1 is the exact Phase61C architecture and selected per-fold parameters already frozen in:

- `../phase61/PLAN_C.md`
- `../phase61/IMPLEMENTATION_C.md`
- `../phase61/phase61c_results.json`

No A1 parameter or mechanism may be retuned for Phase62.

For the fair tournament, regenerate/re-score frozen A1 outputs on the new common 9D fixed-five scorecard using its frozen selected parameter pair and deterministic seeds. This is **evaluation under a new common representation, not model repair**.

## Outer split and target isolation

Voynich outer folds remain physical-leaf folds; recto/verso stay together.

Within each fold:

- the 9D direction/scaling is learned on training leaves only;
- C0 transform choice uses training targets only;
- held-out leaves provide the Voynich target values used for final fold evaluation;
- N0 has no Voynich-tuned parameters;
- A1 remains frozen from Phase61C.

External manuscripts are independent source documents, not token-level folds. Their uncertainty is represented by manuscript-level values and leave-one-manuscript-out sensitivity rather than pretending 146 entries are independent documents.

## Complexity accounting — frozen before outcome

Do **not** reduce scientific interpretation to one arbitrary scalar penalty. Report a complexity/dependence vector and use Pareto comparisons.

For every family record:

1. number of explicit Voynich boundary-aware mechanisms;
2. number of local/context state mechanisms and maximum memory;
3. number of Voynich-selected discrete/continuous parameters;
4. number of transform/model alternatives searched;
5. whether an empirical Voynich token vocabulary/codebook is supplied;
6. size of any target-derived codebook in types and total graphematic units;
7. whether section/hand/page metadata are used at generation time;
8. whether the output process is reversible to a meaningful plaintext candidate.

### Pre-result complexity ledger

**N0**
- Voynich boundary mechanisms: 0
- Voynich-selected parameters: 0
- target vocabulary: no
- reversible plaintext: already plaintext

**C0**
- Voynich boundary mechanisms: 0
- global boundary-blind transform only
- searched alternatives: 5 (model-choice cost at least `log2(5)` bits conceptually)
- no Voynich-derived symbol/codeword table
- reversible to N0 plaintext by construction

**G/A1**
- explicit Voynich paragraph-entry mechanism: 1
- local-family mechanism with memory 10: 1
- selected entry-strength and local-family parameters from Phase61C
- empirical Voynich prose vocabulary supplied: yes, 8,295 observed token types in the Phase61C input
- no meaningful plaintext output supplied

A1's supplied target vocabulary must remain visible in interpretation even if its structural score is strong.

## Primary comparison / falsification rules

This tournament does **not** require one family to be declared a winner.

### N0 materially competitive

N0 is materially competitive if its equal-manuscript aggregate lies in the broad Voynich regime `[0.5, 2.0]` on all three positive primary target ratios where a ratio is defined, without selecting a favorable manuscript post hoc.

### C0 materially improves N0

C0 is retained as an explanatory cipher/recoding family only if held-out transform selection improves joint S1–S3 fit over N0 without adding boundary awareness and the gain is stable across most Voynich folds / manuscript leave-one-out sensitivities.

If C0 does not improve N0, simple boundary-blind reversible recoding receives no explanatory credit merely for obscuring symbols.

### A1 remains materially competitive

Frozen A1 remains competitive if its common 9D fixed-five held-out score stays in the broad regime on S1–S3. Failure here is recorded; A1 is not repaired inside Phase62.

### No winner by exposed score alone

Even if one family dominates S1–S3, it becomes only the **leading structural family**. A final mechanism-family promotion requires the prospective holdout below.

## Frozen prospective holdout — H62-P1

This statistic is **not used for N0/C0 selection or A1 construction**.

### Near-family recurrence distance profile

For each token occurrence in continuous prose/item order, determine whether an edit-distance-1 related token occurs at preceding distance bins:

- 1–2 tokens;
- 3–5;
- 6–10;
- 11–20;
- 21–40.

Report the excess over a document/paragraph-layout-preserving token permutation null in each bin and the normalized five-bin profile.

Primary discriminator:

> the ratio of short-range excess `(1–10)` to longer-range excess `(11–40)`, together with a preregistered profile distance to Voynich.

Why this is discriminative:

- A1 contains an explicit maximum local-family memory of 10 tokens and therefore makes a mechanistic prediction about where excess should decay;
- N0/C0 can show lexical/morphological recurrence but do not contain a hard 10-token generator window;
- the aggregate previous-10 statistic was exposed, but this five-bin distance profile was not used to construct A1 or select C0.

### Holdout isolation

Do **not** inspect the Voynich H62-P1 profile until:

1. N0/C0/A1 S1–S3 results are complete;
2. the structural family ranking is written and committed;
3. the exact H62-P1 computation and distance metric are executable and committed.

If the H62-P1 profile contradicts the leading family, record the contradiction before any architecture extension.

## Phase sequence

### Phase62A — source/design freeze

Complete when:

- external provenance recovered;
- primary panel fixed;
- common scorecard fixed;
- C0 transform family fixed;
- complexity ledger fixed;
- prospective H62-P1 frozen.

No tournament score belongs in Phase62A.

### Phase62B — N0 baseline

Run N0 only. Record manuscript heterogeneity and common-scorecard results. Do not alter C0/A1 based on N0 output.

### Phase62C — C0 and frozen-A1 evaluation

Run fixed C0 transform selection and re-score frozen A1 under the common scorecard.

### Phase62D — exposed-score tournament decision

Compare N0/C0/A1 S1–S3 plus complexity/dependence vector. Freeze a structural ranking or unresolved set.

### Phase62P / Phase63 — prospective discriminator

Only after Phase62D is frozen, reveal/evaluate H62-P1 on Voynich and competitors.

## Interpretation limits

- A good N0 score does not prove Latin or any specific language.
- A good C0 score does not identify a historical cipher.
- A good A1 score does not prove meaningless generation.
- Structural equivalence is not semantic equivalence.
- Meaning/content promotion still requires independently grounded content prediction.
