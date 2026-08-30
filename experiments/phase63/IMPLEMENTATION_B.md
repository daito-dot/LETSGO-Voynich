# Phase 63B — independent-transcription implementation freeze

Status: **frozen before GC-R1/GC-R2/IT-R1/IT-R2/IT-R3 outcomes are computed**.

This file resolves parser/execution details left implicit by `PLAN_B.md`. It does not alter source selection, W1/W2 definitions, replication criteria or frozen A1 parameters.

## Source authority

Scientific execution must use exact files recorded in `SOURCE_MANIFEST_B.json`:

- GC2a SHA-256 `b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f`;
- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- ZL3b Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.

Any mismatch is fatal before scientific metrics.

## Generic P-locus parser

Only loci whose IVTFF locus type has generic type `P` are consumed.

Page and line order remain file order. Physical leaf is parsed from the folio page name.

### Paragraph state

For each page independently:

1. `<%>` starts a new paragraph on that physical line;
2. if another paragraph is still open on the same page, a new `<%>` closes it implicitly before opening the next;
3. the line containing `<%>` belongs to the new paragraph;
4. `<$>` closes the current paragraph **after** the current physical line is appended;
5. page change/file end closes any still-open paragraph;
6. P lines outside an open source-native paragraph are ignored rather than assigned to a guessed paragraph.

This preserves source-native paragraph decisions while tolerating historical files where `<$>` is less complete than `<%>`.

If more than one `<%>` occurs on one physical line, or one line would require splitting into multiple paragraph bodies, execution fails rather than inventing an intra-line mapping.

## Inline IVTFF parsing order

For each P-line body:

1. remove paragraph markers `<%>` / `<$>`;
2. convert `<->` and `<~>` to a dedicated word-boundary sentinel;
3. remove other `<...>` comments/tags without creating a token boundary;
4. protect every `@NNN;` sequence as one atomic glyph placeholder;
5. convert any bracketed uncertain reading `[ ... ]` to an uncertainty sentinel inside its containing token;
6. remove ligature braces `{` / `}` while retaining enclosed manuscript glyph units;
7. apply W1 or W2 word-space handling;
8. convert each surviving token string to native glyph units;
9. exclude the entire token if it contains the uncertainty sentinel or literal `?`.

Malformed/unclosed `@NNN;`, bracket or brace syntax is fatal rather than silently repaired.

## Word-space views

### W1 primary

Token boundaries:

- definite `.`;
- uncertain `,`;
- drawing-space sentinel from `<->` / `<~>`;
- ordinary whitespace in the file.

### W2 sensitivity

Token boundaries:

- definite `.`;
- drawing-space sentinel;
- ordinary whitespace.

An uncertain comma is deleted before splitting, thereby joining its left/right character sequences exactly as preregistered.

No later word-space variant is allowed inside Phase63B.

## Native glyph units

### Eva / EvaT

Applicable to ZL/IT:

- ASCII alphabetic glyphs become lowercase atomic units;
- `@NNN;` protected high-ASCII codes are atomic units;
- braces are structural only;
- any other non-whitespace, non-IVTFF structural character surviving parsing is fatal. This avoids silently reinterpreting unexpected EVA punctuation.

### v101

Applicable to GC:

- each surviving plain character is one atomic native glyph unit;
- ASCII case is preserved;
- digits/punctuation are preserved if they survive IVTFF structural parsing;
- `@NNN;` protected high-ASCII codes are atomic units;
- no v101→EVA conversion occurs.

## Scientific `Item` population

Every parsed source-native paragraph becomes a Phase62-compatible `Item`:

- `document` = page name;
- `leaf` = physical leaf number;
- `lines` = physical P lines containing at least one usable token after confidence filtering;
- empty-token physical lines are omitted from the scientific line array, matching the earlier ZL parser behavior.

The base population uses the already-frozen Phase62 eligibility:

- at least 3 usable lines;
- at least 5 tokens on line0 and line2.

S1 additionally requires at least one valid internal pseudo-boundary under the same Phase62 rule.

## Parser preflight gate before scientific execution

Before GC-R1/R2/IT-R1/R2/R3 code is committed/run, a parser-only preflight must record for each source × W1/W2:

- parsed paragraph count;
- parsed nonempty physical-line count;
- token count/type count;
- base-eligible paragraph count;
- S1-eligible paragraph count;
- physical leaves represented;
- paragraph-start locus count consumed;
- excluded uncertain/unreadable token count;
- token-count distribution summary.

The preflight may **not** build edit1 neighbors, calculate feature vectors, S1/S2/S3, H62-P1 or generate A1 text.

If the preflight shows a parser/syntax bug, parser fixes are permitted only before scientific implementation/results and must be recorded. Population counts themselves are not scientific pass/fail targets and cannot be used to change the already-frozen source/metric criteria.

## Common physical-leaf folds

Use the exact Phase62 fold membership stored in `SOURCE_MANIFEST_B.json`. All three sources contain all 99 common leaves, so no fold member is removed in the frozen current source versions.

Every source uses the same fold leaf numbers but its own source-native paragraphs/tokens.

## GC-R1 exact implementation

For each W view and fold:

1. training items = GC items outside held-out leaves;
2. held-out items = GC items on held-out leaves;
3. compute the Phase62 generic fixed-five 8D feature SD on training base-eligible lines;
4. compute each training S1 item contrast exactly as Phase62: `(line2-line0) - mean(internal j→j+2 pseudos)`, standardized by training SD;
5. training direction = normalized mean training contrast;
6. held-out scalar = projection of mean held-out S1 contrasts on the training direction.

The reported `real_minus_pseudo_projection` is this held-out scalar.

No ZL direction, sign choice or Procrustes alignment is permitted.

## GC-R2 / IT-R2 exact H62-P1 implementation

Reuse the committed Phase62P functions with the parsed native-unit tokens:

- exact five bins;
- base-eligible source-native paragraphs only;
- edit-distance-1 neighbor graph built within the evaluated transcription/fold item set;
- 100 deterministic within-item permutation nulls;
- E vector = observed minus null median;
- signed L1 normalization;
- `C_short` as frozen.

Deterministic null label must include transcription, W view and fold, e.g. `Phase63B:GC:W1:fold0`. No label is shared with ZL discovery tests because this is an external replication, not a paired Monte Carlo sensitivity.

Also recompute the strict-confidence ZL H62-P1 held-out profile under the same parser/view for descriptive cross-transcription `D_profile`; it does not own GC/IT observational pass/fail.

## IT-R1

Identical to GC-R1 except using IT/EvaT native units.

## IT-R3 full frozen A1-R1 transfer

### Paragraph representation

IT source-native parsed paragraphs are converted to Phase61-compatible `Paragraph` objects. Each token is serialized as its concatenated native EvaT glyph units. Since EvaT units here are lowercase single ASCII glyphs/high-ASCII placeholders and no cross-alphabet mapping is introduced, literal `k/t` semantics are inherited exactly from the existing A1 code.

High-ASCII atomic placeholders are serialized as unique private string tokens that remain one Python character-equivalent unit for the A1 edit/length machinery. If any IT high-ASCII glyph is present after confidence filtering, execution must use an explicit one-symbol surrogate table frozen by sorted code value; if none is present, no surrogate table is created.

### Frozen generator

For each fold/W view:

- output vocabulary = IT training-leaf token strings only;
- edit1 neighbor graph = IT training vocabulary only;
- entry shape scores = IT training source-native paragraphs only;
- held-out layout = IT held-out source-native paragraph/line/token counts;
- exact Phase61C parameter pair for that fold;
- five exact seed formulas used in Phase62C/P/63A;
- zero generated types outside IT training vocabulary.

### IT target score

Recompute IT W1/W2 held-out S1/S2/S3 targets using IT training scaling/direction.

S2 null labels are transcription/view/fold/replicate specific; exact deterministic labels are frozen in the executable before result.

### N0 / fixed C0 comparator under IT target

Use the same frozen four CREMMA manuscripts and equal-manuscript aggregation.

Re-tokenize Latin controls using the existing Phase62 representation. Score S1 with the IT training direction/SD. S2 remains source-native Latin locality excess. S3 remains source-native Latin line-position eta2.

C0 is **fixed to C0-4 non-overlapping digraph coding**, with no model selection on IT. It is scored against the IT target in every fold.

### H62-P1 comparator

Recompute N0 and fixed C0-4 H62-P1 using the exact Phase62P equal-manuscript E-vector aggregation. They are representation-independent Latin controls and may be cached across IT folds/views where identical.

A1-R1 H62-P1 uses the generated IT realization, exact frozen bins/null/normalization, average-E-then-normalize across the five generator realizations.

## Scientific result publication

One executable may produce all GC-R1/R2 and IT-R1/R2/R3 outcomes, but it must:

1. verify source hashes and preflight population identities before scientific calculation;
2. report W1 primary and W2 sensitivity separately;
3. preserve all fold-level results;
4. apply only the pass/fail rules already frozen in `PLAN_B.md`;
5. emit no adaptive mapping/model repair.

No A2/C1/M0 is allowed in Phase63B.