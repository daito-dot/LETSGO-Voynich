# Issue #139 — independent IT2a replication of the same-line terminal→initial edge

Date: 2026-09-06
Status: **FROZEN BEFORE ANY ISSUE #139 EDGE SCORE**
Parent: Issue #88; entry authority Issue #134 / PR #137
Architecture authority: Issue #125 / PR #126
Independent-source authority: Issue #66 Stage-A audit

## Question

Does the fixed same-source-line previous-terminal → next-initial predictive architecture from ZL3b survive on the independently frozen Takahashi/IT2a transcription when source handling, representation, folds, smoothing, target population, and decision rule are fixed before target scoring?

This is an architecture replication. It does not require literal ZL3b and IT2a conditional tables to be numerically equal.

## 1. Frozen independent source

Use only:

- URL: `https://www.voynich.nu/data/IT2a-n.txt`
- transcription: Takeshi Takahashi / `EvaT`
- IVTFF header: `#=IVTFF EvaT 2.0 M 3`
- raw byte size: `342104`
- raw line count: `5444`
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git-blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`

This source was independently frozen before Issue #139 in Phase63B and re-audited in Issue #66. The Issue #66 raw audit authority is:

- `experiments/occupancy-graph-independent-transcription/source-audit/issue66_source_audit.json`
- raw JSON SHA-256: `bed86e92fcb854b614dfb474cd3bab9e6fc1e5746399fc14bced9f8e4448eddf`
- repository blob SHA-1: `85c172c113927b91215463ee9297630580b57769`

No alternate IT2a mirror, revision, transcription, or target-driven source repair is allowed after reveal.

## 2. Frozen record / source-line mapping

Reuse the already-audited Phase63B W1 parser semantics in `experiments/phase63/phase63b_common.py`.

Only IVTFF loci matching the frozen locus parser and having a P-coded record are eligible. Physical leaf is the leading integer in the page locus (`fNN... -> NN`). Paragraph starts/ends are the IVTFF `<%>` / `<$>` markers. A source line for this replication is one parsed non-empty P-coded IVTFF locus appended as one `line` by the frozen W1 parser. The edge history is hard-reset before every such source line.

No edge may cross a source-line boundary, paragraph boundary via an empty line, page boundary, or physical-leaf boundary.

## 3. Frozen visible-boundary and uncertainty handling

Use Phase63B `tokenize_body(..., alphabet="EvaT", view="W1")` unchanged:

- remove paragraph markers `<%>` and `<$>`;
- treat `<->` and `<~>` as visible token boundaries;
- remove remaining inline IVTFF tags;
- remove ligature braces `{}` while preserving their contained glyph sequence;
- split W1 visible units on period, comma, whitespace, `<->`, and `<~>` boundaries;
- an uncertainty bracket `[...]` marks the containing token uncertain;
- any token containing a frozen uncertainty marker or `?` is excluded in full;
- retained EVA letter units are converted to the parser's already-frozen lowercase native form;
- no new glyph substitution, equivalence class, normalization, token merge, or token split is permitted.

The independently audited source counts that Gate0 must reproduce are:

- P-coded loci: `4118`;
- paragraphs: `772`;
- pages: `206`;
- physical leaves: `99`;
- clean visible tokens: `34411`;
- excluded uncertain/unreadable tokens: `80`.

Visible boundaries are production boundaries in this experiment. They are not asserted to be natural-language words.

## 4. Frozen outer folds

Reuse the exact Issue #66 / #58C physical-leaf fold authority. Gate0 must read the already-archived `fold_leaf_sets` from `issue66_source_audit.json` and require:

- exactly five folds;
- exactly 99 distinct physical leaves total;
- no leaf overlap between folds;
- IT2a observed leaf universe equals that 99-leaf authority exactly.

The already-audited clean-token support by fold is:

`[6102, 6692, 7528, 7484, 6605]`.

The already-audited primary-target support by fold is:

`[4976, 5416, 6261, 6197, 5430]`.

No fold shuffling, balancing, target-dependent exclusion, or alternate seed is allowed.

## 5. Frozen training and primary target population

### Training population

For each outer fold, train both POS2 and EDGE2 on **all clean visible W1 tokens** on the other four folds. This matches Issue #125: visible tokens contribute to the explicit onset/continuation expert whether or not the 12-slot parser accepts that token.

The immediately previous token used by EDGE2 is likewise the immediately previous **clean visible token** within the same source line; it is not required to be a scored/slot-accepted token.

### Primary scored population

Score a current clean visible token iff the unchanged Issue #125 `SlotParser` has at least one legal parse for that current token. This preserves the #125 scientific support rule while leaving the predictive representation literal.

Gate0 must reproduce the Issue #66 totals:

- primary scored tokens: `28280`;
- rejected current tokens: `6131`;
- direct coverage: `0.821830228705937`;
- fold scored counts: `[4976, 5416, 6261, 6197, 5430]`.

Parse multiplicity is not used to choose a token representation. Acceptance is only a fixed inclusion predicate. `min` versus `max` slot parses therefore cannot change POS2/EDGE2 probabilities.

No all-clean score may replace the primary after reveal. A broader all-clean analysis would require a separate preregistered sensitivity and cannot promote a failed primary result.

## 6. Frozen literal symbol representation

For every retained W1 token string `tok`, use exactly the Issue #125 Phase-1 byte representation:

`list(tok.encode("utf-8")) + [END_TOKEN]`

with:

- `END_TOKEN = 256`;
- `BOS = -1` only for left-padding a short k-context;
- outcome vocabulary size `V = 257` (`0..255` raw byte outcomes plus `END_TOKEN`).

No slot identity, EVA equivalence class, glyph class, Currier label, hand label, section label, or cross-transcription mapping enters the predictive symbol representation.

## 7. Frozen POS2 / EDGE2 architecture

Reuse Issue #125 without target-driven modification.

Global constants:

- `k = 2`;
- additive `alpha = 0.01`;
- source-line hard reset.

### POS2

For each token:

1. first symbol at line start: one pooled `LINE_START` first-symbol distribution;
2. first symbol in line body: one pooled `LINE_BODY` first-symbol distribution, ignoring previous-token identity;
3. second emitted symbol: conditional on current first symbol, with separate line-start and line-body tables; the outcome may be a raw byte or `END_TOKEN`;
4. third and later emitted symbols: the ordinary shared fixed-k2 source-line byte transition table, exactly as in Issue #125.

### EDGE2

Identical to POS2 except for exactly one factor:

- for the first symbol of a line-body token, condition on the immediately previous clean visible token's terminal raw byte within the same source line.

Line-start first-symbol, second-symbol, and all later continuation factors are definitionally the same as POS2.

No across-line edge, longer terminal history, first-two-glyph identity edge, latent state, Currier gate, hand gate, or section gate may be added.

## 8. Frozen smoothing and fallback

Every categorical probability uses the Issue #125 additive rule over `V=257`:

`p(sym | context) = (count(context,sym) + 0.01) / (count(context) + 0.01*257)`.

There is **no backoff or pooled fallback** for an unseen EDGE2 previous-terminal context. An unseen context therefore has its empty additive-smoothed distribution, i.e. `1/257` for every outcome. The same empty-context rule applies to an unseen line-start/body second-symbol context and to an unseen exact k2 continuation context.

This is intentionally stricter than the later Currier transport fallback used in Issues #127/#134; #139 replicates the original Issue #125 edge architecture.

## 9. Frozen held-out comparison

There is no tunable hyperparameter and therefore no inner-fold selection in the primary replication.

For each outer fold `f`:

1. train POS2 and EDGE2 on the other four physical-leaf folds;
2. score the untouched fold once on the frozen primary target population;
3. compute mean token code length for each model;
4. define

`G_identity_IT2a[f] = bits(POS2)[f] - bits(EDGE2)[f]`.

Primary stability rule, frozen from the Issue #88 program family:

- mean `G_identity_IT2a > 0`; and
- `G_identity_IT2a > 0` in at least `4/5` outer folds.

There is no minimum effect-size threshold and no post-reveal weighting.

## 10. Frozen classifications

Exactly one class is allowed after a valid first reveal:

1. `INDEPENDENT EDGE REPLICATION PASSES` — Gate0 valid and the primary stability rule passes.
2. `INDEPENDENT EDGE REPLICATION FAILS` — Gate0 valid and the primary stability rule fails.
3. `INVALID INDEPENDENT REPLICATION` — source/fold/line/boundary/support authority or faithful frozen representation cannot be established.

No fourth class may be introduced after target reveal.

## 11. Score-free Gate0 requirements

Before any Issue #139 POS2/EDGE2 probability is computed, Gate0 must verify at minimum:

- exact IT2a raw source identity;
- exact archived Issue #66 source-audit identity and fold sets;
- exact Phase63 W1 parser and SlotParser source-code blob identities used by this contract;
- all frozen population/fold counts above;
- train/test leaf disjointness for all five outer folds;
- every test fold has at least 300 primary scored tokens and at least 300 scored line-body tokens;
- every outer training complement has nonzero line-start and line-body support, at least two previous-terminal byte contexts, and at least two observed previous-terminal→first-byte pairs;
- every retained token has a nonempty UTF-8 byte sequence before `END_TOKEN`;
- no scientific edge probability, log likelihood, bits/token, `G_identity_IT2a`, or classification is computed.

A Gate failure maps only to `INVALID INDEPENDENT REPLICATION` and blocks scoring.

## 12. Firewall / chronology

The following must be true before first reveal:

1. this plan and Gate0 executable are committed;
2. Gate0 succeeds and its exact JSON authority is archived/merged;
3. the predictive scorer is committed separately after Gate0 authority exists;
4. the scorer and frozen classification rule are committed before its first target workflow run;
5. no IT2a edge score is inspected before the scientific scorer commit is fixed.

Forbidden target-driven choices include:

- symbol normalization or glyph equivalence;
- uncertainty exclusion changes;
- W1/W2 switching;
- physical-leaf fold changes;
- slot-parser repair or parse-choice filtering;
- smoothing changes or fallback addition;
- k/model-family expansion;
- Currier/hand/section conditioning;
- target-score-driven population narrowing;
- S1/S2/H62/R1 tuning;
- latent-state fitting.

## 13. Interpretation boundary

A pass would reduce the plausibility that the same-line terminal→initial architecture is merely a ZL3b-specific transcription artifact. It would not establish literal conditional-table equality across transcriptions, semantics, plaintext, language, cipher family, historical direction, author, hoax/artificial origin, or natural-language word boundaries.

A fail would downgrade manuscript-wide responsibility for this edge until representation/transcription sensitivity is audited prospectively. It may not be rescued by a secondary subgroup sign.

Refs #66 #88 #123 #125 #126 #134 #136 #137 #139.
