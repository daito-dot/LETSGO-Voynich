# Phase 63B — independent transcription / segmentation replication

Status: **source/design freeze before replication metrics are computed**.

Phase62P supplied genuine prospective structural support for A1 and Phase63A showed that the advantage survives removal of held-out-only token types. The next major dependency is the transcription/segmentation lineage itself.

Phase63B asks whether the strongest structural findings survive independent human readings of the manuscript rather than another repair to A1.

## Scientific question

> Are paragraph-entry specialization and short-range near-family recurrence robust to independent transcription decisions, and does the frozen A1-R1 mechanism transfer when the independent transcription uses a compatible EVA-family alphabet?

This is an **external representation replication**, not a new model-selection phase.

## Frozen transcription panel

### Primary independent observation replication — GC2a / Glen Claston v101

Source:

- canonical public distribution: `https://www.voynich.nu/data/GC2a-n.txt`
- header currently identifies `IVTFF v101 2.0` and original file `voyn101.txt`;
- transcriber: Glen Claston (GC);
- alphabet: **v101**, independently devised by Claston;
- Claston independently transliterated the whole manuscript and intentionally used a different glyph granularity from EVA, including distinctions that earlier alphabets collapse.

Rationale:

GC is the strongest available transcription-dependence challenge because both the human transcription and the alphabet/glyph segmentation differ from ZL/EVA.

Limitation:

The modern GC2a file has been converted to the common IVTFF locus/page framework. Thus page/locus reconciliation and file-format standardization are shared infrastructure; glyph readings, word-space decisions and source-native paragraph definitions remain independent transcription decisions.

### Secondary full-model replication — IT2a / Takeshi Takahashi EvaT

Source:

- canonical public distribution: `https://www.voynich.nu/data/IT2a-n.txt`
- header currently identifies `IVTFF EvaT 2.0`;
- underlying transcriber: Takeshi Takahashi;
- alphabet: EVA/EvaT family.

Rationale:

IT is a different human transcription lineage while retaining an EVA-compatible alphabet. This makes it suitable for a **full frozen A1-R1 transfer test** without inventing a post-hoc v101↔EVA glyph mapping.

Limitation:

The IT file is the historical Takahashi transcription as incorporated/standardized in the Landini-Stolfi/modern IVTFF lineage rather than a raw untouched original file. Treat it as independent reading evidence with shared later formatting infrastructure, not fully independent digital provenance.

### ZL reference

ZL remains the discovery/reference transcription only:

- pinned mirror commit `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`;
- exact `ZL3b-n.txt` Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`.

ZL is not used to tune GC/IT parsing after results.

## Phase63B0 — source audit before science

Before any replication metric is calculated, run a source-only audit that records for GC2a, IT2a and pinned ZL3b:

- byte SHA-256 and Git-blob SHA-1;
- byte size and IVTFF header/version text;
- total page headers;
- P-coded text loci;
- source-native `<%>` paragraph starts and `<$>` paragraph ends;
- physical leaves represented by P-coded prose;
- P-locus ID overlap across transcriptions;
- paragraph-start locus overlap across transcriptions;
- counts of high-ASCII `@NNN;`, uncertain readings `[ ]`, unreadable `?`, definite `.` spaces, uncertain `,` spaces, drawing-interruption spaces, and ligature notation;
- all raw non-reserved alphabet characters observed in P-coded text.

**No S1/S2/S3, edit-distance, H62-P1, entry/pseudo contrast or A1 result may be computed in Phase63B0.**

The audit output becomes `SOURCE_MANIFEST_B.json` and its hashes are then fixed as the only admissible Phase63B inputs.

If the live canonical source changes between the audit and scientific execution, the scientific workflow must fail rather than silently use the newer file.

## Frozen population and page/leaf mapping

Use only generic `P` paragraph-text loci from the IVTFF files.

Use each transcription's **own source-native paragraph markers** `<%>` / `<$>`. Do not copy ZL paragraph starts into GC or IT. IVTFF explicitly permits transcribers to define paragraphs differently.

Physical leaf identity is taken from the common folio page name (e.g. `f1r`, `f1v` → leaf 1). Recto/verso remain on the same physical-leaf side of every split.

Replication fold population rule, fixed before source counts:

> Start from the exact five Phase62 ZL physical-leaf fold sets and retain only physical leaves having usable P-coded prose in **all three** ZL/GC/IT sources.

A leaf remains assigned to its original Phase62 fold. No reassignment is permitted to improve balance after source inspection.

Source-native paragraphs within those common leaves may differ between transcriptions.

## Frozen IVTFF text interpretation

### Shared syntax

The parser follows IVTFF 2.0 semantics:

- `.` = definite apparent word space;
- `,` = uncertain apparent word space;
- `<->` and `<~>` = drawing interruption that implies a word space;
- `<%>` / `<$>` = source-native paragraph start/end;
- `<!...>` and `<@...>` = comments/tags, not manuscript glyphs;
- `@NNN;` = one high-ASCII manuscript glyph unit;
- `{...}` = ligature notation containing manuscript glyph units; braces themselves are not glyphs;
- `[a:b:...]` = uncertain alternative reading; the first option is the IVTFF-defined most likely reading;
- `?` = one unreadable manuscript character.

### Confidence firewall

Primary replication excludes any **token** whose source representation contains:

- `?` unreadable characters;
- `[ ... ]` uncertain alternative readings.

This rule applies identically to ZL, IT and GC before any outcome is seen. Such tokens remain counted in source-audit diagnostics but do not enter scientific features/edit-distance calculations.

### Word segmentation — two frozen views

Because apparent word-space judgment itself differs between transcribers, freeze both views before outcomes.

**W1 — conservative-space primary**

Treat all IVTFF word-space symbols as token boundaries:

- `.`
- `,`
- `<->`
- `<~>`

**W2 — definite-space sensitivity**

Treat only definite/drawing spaces as token boundaries:

- `.`
- `<->`
- `<~>`

For `,`, remove the comma without a boundary, joining the adjacent character sequences. This approximates the previous ZL analysis convention and tests sensitivity to uncertain-space decisions.

A claimed transcription-robust phenomenon must not depend on choosing W1 versus W2 after seeing results. Primary decisions use W1; W2 is a predeclared sensitivity and any reversal is reported.

## Frozen native glyph units

### Eva / EvaT (ZL and IT)

- basic ASCII alphabetic characters are glyph units;
- ASCII case is canonicalized to lower case because EVA capitalization is a ligature-connection convention rather than a different basic glyph identity;
- each `@NNN;` high-ASCII sequence is one atomic glyph unit;
- braces used for ligature notation are removed while their enclosed glyph units are retained.

### v101 (GC)

- every plain v101 ASCII character not serving current IVTFF syntax is one atomic native glyph unit;
- **case is preserved** because v101 uses separate ASCII assignments for distinctions within its alphabet;
- digits and punctuation that belong to v101 are real glyph units, not stripped;
- each `@NNN;` sequence is one atomic glyph unit;
- current IVTFF reserved syntax is parsed structurally before glyph extraction.

This deliberately does **not** convert GC/v101 into EVA.

## Primary GC replication targets

GC is used to test observational structure that does not require an EVA-specific k/t mapping.

### GC-R1 — paragraph-entry specialization

Use the generic representation-neutral **8D fixed-five-token** feature vector from Phase62:

1. TTR;
2. mean native-unit token length;
3. token-length SD;
4. native-unit inventory size;
5. native-unit entropy;
6. first-unit entropy;
7. last-unit entropy;
8. within-line edit-distance-1 token-family fraction.

For every outer fold:

1. learn training feature SD and real-entry-minus-internal-pseudo direction from GC training leaves only;
2. compare held-out real paragraph entry transitions against held-out internal pseudo-boundaries;
3. no ZL direction is imported.

A GC paragraph must satisfy the same fixed-five eligibility on both compared lines. Internal pseudo-boundaries remain `j -> j+2`, `j>=1`, inside the same source-native paragraph.

**Frozen GC-R1 replication criterion:**

- held-out real-minus-pseudo projection is positive in at least 4/5 folds;
- across-fold mean real-minus-pseudo projection is positive;
- W2 sensitivity may change magnitude but must not reverse the across-fold mean sign.

No magnitude equality to ZL is required because v101 has different glyph granularity.

### GC-R2 — H62-P1 recurrence geometry

Use the exact Phase62P five distance bins and within-item permutation-null logic, but edit distance is computed in native v101 glyph units.

Primary population = base-eligible source-native GC paragraphs on the common-leaf fold population.

**Frozen GC-R2 replication criterion:**

- `C_short > 0` in at least 4/5 held-out folds;
- across-fold mean `C_short > 0`;
- W2 sensitivity retains positive across-fold mean `C_short`.

Also report L1 profile distance to the corresponding ZL held-out fold profile recomputed under the same strict-confidence W1/W2 parser, but no post-hoc distance threshold owns the primary pass/fail because v101 changes glyph granularity.

## Why full A1 is not forced onto GC

The current A1 entry mechanism contains an EVA-specific token-shape feature: whether a token contains literal `k` or `t`. v101 uses a different alphabet and intentionally different glyph segmentation.

Phase63B will **not invent a v101 equivalent of EVA k/t after seeing GC data**.

Therefore GC owns the strongest independent-alphabet observational replication, not full A1 model replication. A later cross-alphabet A1 test requires a pre-existing externally grounded glyph mapping or an architecture whose entry feature is alphabet-invariant.

## Secondary IT full A1-R1 replication

IT/EvaT permits the existing A1 shape definition without an invented alphabet mapping.

### IT-R1 — source-native entry specialization

Run the same generic 8D training-fold real-vs-pseudo test as GC. Criterion:

- positive held-out real-minus-pseudo projection in at least 4/5 folds;
- positive across-fold mean;
- W2 does not reverse across-fold mean sign.

### IT-R2 — source-native H62-P1

Compute H62-P1 using IT source-native paragraphs and native EvaT units.

Criterion:

- `C_short > 0` in at least 4/5 folds;
- positive across-fold mean;
- W2 does not reverse across-fold mean sign.

### IT-R3 — frozen A1-R1 transfer

Generate using:

- IT training-leaf-only vocabulary;
- IT training-side edit1 neighbor graph and entry shape scores;
- source-native IT held-out paragraph/line/token-count layout;
- exact Phase61C fold parameter pairs (`.5/.20`, `.5/.20`, `.5/.30`, `.5/.30`, `.5/.20`);
- exact existing five seed formulas;
- no retuning.

Recompute N0 and **fixed C0-4 digraph** against the IT training direction/target. Do not rerun C0 model selection.

Frozen IT-R3 replication criterion under W1:

1. A1-R1 S1/S2/S3 ratio-of-means are each within `[0.5,2.0]` of IT held-out targets;
2. A1-R1 has lower mean H62-P1 `D_profile` than N0 and fixed C0-4;
3. A1-R1 has lower mean absolute `C_short` difference than N0 and fixed C0-4;
4. A1-R1 beats both baselines in at least 3/5 folds on each H62-P1 metric.

W2 is a predeclared sensitivity; failure under W2 does not overwrite W1 primary status but materially weakens transcription robustness and must be explicit.

## No cross-transcription retuning

Forbidden before recording Phase63B outcomes:

- changing paragraph starts to match ZL;
- mapping GC glyphs to EVA based on outcome;
- changing edit distance to improve agreement;
- dropping source-native uncertain spaces after seeing W1;
- changing A1 parameters for IT;
- choosing a new C0 transform on IT;
- dropping physical leaves/folds because they disagree;
- replacing GC with IT as primary because GC fails;
- replacing these replication criteria after inspection.

## Interpretation

### Strong replication

If GC-R1/R2 and IT-R1/R2/R3 all pass under W1, with no W2 sign reversal of the observational effects:

> the entry/local-recurrence mechanism is robust to an independent glyph/transcription lineage, and the frozen A1-R1 advantage transfers to an independent EVA transcription.

### Partial replication

If GC observational effects survive but IT A1-R1 transfer fails, the manuscript structure is transcription-robust but the specific A1 parameterization/entry mechanism is not fully portable.

If IT passes but GC fails, the result suggests dependence on EVA-style glyph/word segmentation and must weaken claims of transcription independence.

### Failure

If the primary GC observational effects fail or reverse, the current strongest mechanism narrative is materially transcription-dependent. Record that before adapting representation or model architecture.

## Phase63B0 stop point

The immediate next action is **source audit only**. Do not implement or run GC-R1/GC-R2/IT-R1/IT-R2/IT-R3 until exact GC2a/IT2a hashes, source coverage and syntax inventory are committed in `SOURCE_MANIFEST_B.json`.