# Phase 62 — first fair N/C/G model-family tournament

Status: **frozen design before N0/B0 tournament scoring**.

Phase61C kept G/A1 structurally viable after exactly one local-family repair. Phase62 does not extend A1. It asks whether meaningful structured medieval text, with or without a bounded global recoding, can achieve comparable structural fit at lower target dependence / complexity.

## Scientific question

Compare:

- **N0** — source-native meaningful structured medieval text;
- **C0/B0** — the same text after a bounded, reversible, global, boundary-blind recoding;
- **G/A1** — the frozen Phase61C nonsemantic generator.

Which family places the same cross-representation structural targets in the Voynich regime most efficiently, and what extra machinery is required?

This is a mechanism-family comparison, not a language identification or decipherment test.

## Frozen inputs

### Voynich

- transcription: ZL3b/EVA v3b, 2025-05-13
- expected Git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`
- public reproducibility mirror: `matthewdgreen/cipher_benchmark`
- frozen mirror commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- path: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`

The external transcription is not redistributed by this repository.

### Medieval structured-text controls

- corpus: `HTR-United/CREMMA-Medieval-LAT`
- frozen commit: `292525969ad98380b398e6606a9c2a36d51913ae`
- representation: graphematic medieval Latin manuscript transcription

Source recovery and provenance are frozen in `CONTROL_RECOVERY.md`.

### Primary N0 panel

Before corpus-wide counts were inspected, the source audit committed the rule:

> include every immediate CREMMA manuscript directory with at least 5 eligible literal-pilcrow entries.

It yields:

1. BIS 193 — scholastic — 64 eligible entries;
2. CLM 13027 — medical — 39;
3. Mazarine 915 — scholastic — 38;
4. UBL 758 — ecclesiastical — 5.

All eligible entries are used. There is no manual semantic item selection.

**Replication/aggregation unit = manuscript, not entry.** The four manuscripts receive equal primary weight.

### Predeclared sensitivities

- H318 — medical/recipes — 4 eligible literal-pilcrow entries; excluded by the frozen >=5 primary rule but retained because it was already a Phase52 control.
- Arras 861 — literary — no literal-pilcrow eligible entries; retained for non-entry document/line-position sensitivity only.

Neither may enter/leave the primary estimate after results are seen.

## Source-native entry segmentation

A medieval item begins at a literal `¶` and extends until the next literal pilcrow in the same file or file end.

- line0 = post-pilcrow text on the marker's physical source line;
- later lines = following physical source lines until next marker/file end;
- primary eligibility = at least 3 item lines and >=5 usable tokens on line0 and line2;
- internal pseudo-boundaries = `j -> j+2`, `j>=1`, within the same item, both compared lines >=5 tokens.

No Latin wording/translation is used to create boundaries.

Voynich uses explicit ZL3b `<%>` paragraph markers and the audited physical-leaf grouping.

## Graphematic units

- Voynich: raw EVA characters;
- Latin: NFC grapheme units, attaching combining marks to the preceding base unit where applicable;
- punctuation/separators are not units;
- medieval abbreviation graphemes are retained, never expanded for the primary analysis.

## Sample-size-neutral core feature vector — 8D

Literal Voynich-specific `{k,t}` dimensions have no invariant cross-language analogue and are excluded. Local previous-10 continuity is also kept outside this vector because its intended window must not be truncated by the fixed-token sample-size control.

For **S1 and S3**, every eligible line is represented using exactly its **first five usable tokens**, with:

1. type-token ratio;
2. mean token length in graphematic units;
3. token-length SD;
4. unit inventory size;
5. unit entropy;
6. first-unit entropy;
7. last-unit entropy;
8. within-line edit-distance-1 token-family fraction.

The fixed-five representation prevents line token count from becoming a hidden discriminator. Source-native full-line versions are secondary sensitivities only.

## Primary structural scorecard

All families are judged on the same three dimensions.

### S1 — entry-specific generic projection

Within each outer Voynich physical-leaf fold:

1. learn 8D feature SDs and the mean real-entry-minus-internal-pseudo direction from **Voynich training leaves only**;
2. normalize that direction to unit norm;
3. score held-out Voynich entry deltas on it;
4. score external N0/C0 manuscript entry deltas on the same frozen Voynich scaling/direction;
5. average entries within each manuscript first, then average the four manuscripts equally.

Primary S1 quantity: external/model projection divided by the held-out Voynich projection.

Also report the full 8D mean delta, cosine to the Voynich direction, and source-standardized transition norm as diagnostics. They cannot replace S1 post hoc.

### S2 — local near-family activation beyond document inventory

S2 uses **full eligible physical lines**, not the five-token S1/S3 representation.

Observed statistic: fraction of token occurrences having at least one non-identical edit-distance-1 token among the preceding up-to-10 tokens on the same physical line.

Permutation null, separately within each manuscript/model realization:

- pool all tokens from the included physical lines;
- preserve the number of token slots in every line;
- randomly redistribute the existing document tokens across those slots;
- thereby preserve document vocabulary and exact line-token counts while destroying line-local family activation.

Use 100 deterministic null replicates.

Primary S2 quantity:

`locality_excess = observed_local_prev10 - median(null_local_prev10)`.

Compare model locality excess with the equivalently computed held-out Voynich value. Report raw observed and null distribution too.

### S3 — generic line-position grammar

Using the same fixed-five 8D features as S1, compute eta-squared for item/paragraph line-position groups:

- line0;
- line1;
- line2;
- line3+.

Primary S3 quantity: mean eta2 across 8 dimensions. Report max and per-dimension values as diagnostics.

## Secondary scorecard

Report but do not use to override S1–S3:

- full-line S1/S3 sensitivity;
- entry transition norm and direction cosine;
- raw local-prev10;
- edit1 token-type density;
- token/unit inventory sizes;
- manuscript heterogeneity and leave-one-manuscript-out sensitivity;
- H318 and Arras predeclared sensitivities.

Edit1 type density is a target-dependence diagnostic: it is independent for N0/C0 source vocabularies but **not** an independent A1 prediction because A1 is supplied the empirical Voynich token vocabulary.

## N0

N0 is unencoded source-native structured manuscript text under the frozen rules above.

- Voynich-tuned parameters: none;
- primary result: equal-manuscript aggregate across BIS193, CLM13027, Mazarine915, UBL758;
- all four individual manuscript results are reported;
- best-manuscript matching is not a primary result.

## C0/B0 — bounded boundary-blind reversible recodings

C0 begins from the exact N0 items. Every transform is global and token-internal. No transform may inspect manuscript identity, entry/paragraph position, line number, Voynich section, or Voynich boundary labels.

All encoded units are abstract symbols/tuples; arbitrary one-to-one renaming of those symbols is irrelevant to the generic structural scorecard.

### C0-0 — identity / monoalphabetic-equivalent

No structural change. Any one-to-one grapheme substitution is equivalent here.

### C0-1 — token reversal

Reverse graphematic unit order in every token. Fixed and reversible.

### C0-2 — positional allography, 2 classes

For token units `g_i`, encode each as `(g_i, class)` where:

- `I` if `i=0`;
- `N` otherwise.

Token boundaries are preserved. Decoding drops the class tag.

### C0-3 — positional allography, 3 classes

Encode each unit as `(g_i, class)` where:

- `I` if `i=0` (including singleton tokens);
- `F` if `i=len(token)-1` and `len(token)>1`;
- `M` otherwise.

Decoding drops the class tag. The rule is fixed, reversible and boundary-blind.

### C0-4 — non-overlapping digraph coding

From token start, encode exact unit pairs `(g_0,g_1)`, `(g_2,g_3)`, ... as single abstract units; an odd final source unit becomes a tagged singleton. Because each encoded unit contains its exact source unit(s), decoding is unique.

### C0 model selection

There are exactly five alternatives C0-0…C0-4.

For each outer Voynich physical-leaf fold:

- compute training-fold Voynich S1–S3 targets;
- calculate equal-manuscript C0 candidate aggregates;
- choose the single transform minimizing mean squared relative error over S1, S2 and S3 on training targets;
- evaluate that selected transform against held-out Voynich targets.

No continuous transform parameter and no Voynich-derived symbol/codeword table is fitted.

Any more expressive cipher becomes **C1** after C0 is frozen; it is not a repair inside Phase62C.

## Frozen G/A1 competitor

A1 remains exactly the Phase61C architecture. Its mechanism and selected fold parameters are frozen in:

- `../phase61/PLAN_C.md`
- `../phase61/IMPLEMENTATION_C.md`
- `../phase61/phase61c_results.json`

No A1 parameter is retuned.

Phase62 regenerates/rescores A1 using its already selected per-fold parameter pair and deterministic generator seeds, but evaluates the output on the new common 8D/S2 scorecard. This is evaluation under a common representation, not model repair.

## Outer isolation

Voynich outer split remains five physical-leaf folds; recto/verso stay together.

Per fold:

- S1 scaling/direction is learned from Voynich training leaves only;
- C0 transform choice sees training targets only;
- held-out leaves define final target values;
- N0 has no Voynich-tuned parameter;
- A1 is not retuned.

External manuscripts are replication units. Uncertainty is shown with manuscript-level results and leave-one-manuscript-out sensitivity rather than treating 146 entries as 146 independent documents.

## Complexity/dependence accounting — frozen before outcome

Do not collapse complexity to one arbitrary scalar penalty. Report a vector and use Pareto comparisons.

For each family record:

1. explicit Voynich boundary-aware mechanisms;
2. local/context state mechanisms and maximum memory;
3. Voynich-selected parameters/model choices;
4. number of transform alternatives searched;
5. whether empirical Voynich vocabulary/codebook is supplied;
6. target-derived codebook size in types and total graphematic units;
7. generation-time use of section/hand/page metadata;
8. reversibility to a candidate meaningful plaintext.

### Pre-result ledger

**N0**
- Voynich boundary mechanisms: 0
- Voynich-selected parameters: 0
- target vocabulary: no
- output already meaningful source plaintext

**C0**
- Voynich boundary mechanisms: 0
- one global boundary-blind transform choice
- alternatives searched: 5; model-choice cost conceptually at least `log2(5)` bits
- Voynich-derived mapping/codebook: none
- reversible to N0 source plaintext

**G/A1**
- explicit Voynich paragraph-entry mechanism: 1
- local-family mechanism: 1, maximum generator memory 10 tokens
- entry-strength and local-family parameter choices already selected in Phase61C
- supplied empirical Voynich prose vocabulary: yes, 8,295 observed token types in the Phase61C input
- candidate meaningful plaintext: none supplied

A1's target-vocabulary dependence remains explicit even if structural fit is strong.

## Frozen primary decision rules

The tournament may remain unresolved; no forced winner is required.

### N0 materially competitive

N0 is materially competitive if the equal-manuscript primary aggregate lies in `[0.5, 2.0]` of held-out Voynich for S1, S2 and S3 wherever the held-out denominator is positive and stable. If S2 Voynich excess is too close to zero for a stable ratio, use the predeclared relative-error score and report the sign rather than manufacturing a ratio.

### C0 explanatory value

C0 gains explanatory credit only if held-out transform selection materially improves joint S1–S3 error over N0 without boundary awareness, and the improvement is stable across a majority of Voynich folds and manuscript leave-one-out sensitivities.

Merely changing symbols is not evidence for ciphering.

### A1 materially competitive

Frozen A1 remains competitive only if its common-scorecard held-out results remain in the same broad regime on S1–S3. Failure is recorded without A1 repair inside Phase62.

### Exposed scores cannot finish the tournament

A family may become the leading **structural** family on S1–S3, but final promotion requires the frozen prospective discriminator below.

## Frozen prospective holdout H62-P1 — near-family recurrence distance profile

Repository search before freezing found no prior phase implementing this exact distance-profile test. The aggregate previous-10 statistic is exposed; the five-bin profile is not used to construct A1 or select C0.

### Exact computation

Within each Voynich paragraph or medieval source-native item separately, flatten physical lines to token order. Do not cross paragraph/item boundaries.

For each token occurrence, for each preceding-distance bin:

- B1: 1–2;
- B2: 3–5;
- B3: 6–10;
- B4: 11–20;
- B5: 21–40;

record whether at least one non-identical edit-distance-1 token occurs in that bin. The observed bin statistic is the mean indicator over token occurrences for which the full bin is available within the same paragraph/item.

Null:

- permute token order **within each paragraph/item**;
- preserve each paragraph/item token multiset and length;
- 100 deterministic replicates;
- `E_b = observed_b - median(null_b)` for each bin.

Signed normalized profile:

`P_b = E_b / sum_j(abs(E_j))`, when the denominator is nonzero.

Short-range concentration:

`C_short = (E_B1 + E_B2 + E_B3) / sum_j(abs(E_j))`.

Profile distance between a candidate and held-out Voynich:

`D_profile = sum_b abs(P_b(candidate) - P_b(Voynich))`.

Primary prospective comparison reports both `C_short` difference and `D_profile`; lower profile distance is better. Do not combine them into a new post-hoc weighted scalar.

### Mechanistic relevance

A1 explicitly reuses/mutates from a maximum recent window of 10 tokens, so it predicts that induced near-family excess should be disproportionately concentrated in B1–B3. N0/C0 may show lexical/morphological recurrence but have no hard 10-token generator window.

### Holdout isolation

Do **not** compute/reveal the Voynich H62-P1 profile until:

1. N0/C0/A1 S1–S3 results are complete;
2. the Phase62D structural ranking/unresolved set is written and committed;
3. an executable implementing exactly the H62-P1 definition above is committed without having evaluated Voynich H62-P1.

A contradictory H62-P1 result must be recorded before any architecture extension.

## Phase sequence

### Phase62A — source/design freeze

Complete when external provenance, source panel, common scorecard, C0 family, complexity ledger and H62-P1 are committed. **No N0/C0 tournament score belongs in 62A.**

### Phase62B — N0 baseline

Run N0 only. Record manuscript heterogeneity. Do not change C0/A1 based on N0 results.

### Phase62C — C0 and frozen-A1 common evaluation

Run the fixed C0 selection and re-score frozen A1.

### Phase62D — exposed-score structural decision

Compare N0/C0/A1 S1–S3 plus complexity/dependence. Commit a structural ranking or unresolved set.

### Phase62P / Phase63 — prospective reveal

Only after Phase62D is frozen, evaluate H62-P1 on held-out Voynich and competitors.

## Interpretation limits

- good N0 fit does not prove Latin or any specific language;
- good C0 fit does not identify a historical cipher;
- good A1 fit does not prove meaningless generation;
- structural equivalence is not semantic equivalence;
- content/decipherment promotion still requires independent content prediction.
