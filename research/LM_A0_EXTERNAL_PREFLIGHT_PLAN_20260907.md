# LM-A0 external scribal preflight — frozen E0 plan

Date: 2026-09-07
Parent: Issue #180 / Issue #172
Related exploratory Voynich discriminator: Issue #179
Status: **FROZEN EXTERNAL E0 PLAN — NO VOYNICH TARGET ACCESS**

## Purpose

LM-A0 is the only architecture family carried forward by the Issue #172 architecture-selection gate, and only to external preflight. The present E0 test asks a narrow question in a non-Voynich medieval manuscript:

> Holding the underlying expanded lexical form fixed, is scribal abbreviation choice enriched at a physical manuscript-line ending?

A positive result would establish only that a line-scoped/context-sensitive scribal rendering effect exists in an external manuscript sample. It would not show that Voynich uses the same mechanism, and it would not license a joint R1-R10 target score.

## Frozen external authority

Repository: `michaelscho/transpy`

- repository commit: `7487dd18adb2bbb7194f3f4d32c03e04ac084626`
- source file: `new_file.xml`
- source blob: `b6addd83de208dc97e2013f45978a8d333b02a4f`
- TEI id: `bdd-bamberg-sb-c-6`
- manuscript: Bamberg, Staatsbibliothek, Can. 6
- content: *Decretum Burchardi*, Book 07

The file identifies itself as a working TEI conversion from Transkribus and says `Working files, not ready for circulation.` Therefore E0 is a feasibility/preflight sample, not sufficient external authority for LM-A1 promotion.

The same TEI contains physical `<lb>` elements with `facs="x,y,w,h"` geometry and `<choice><abbr>…</abbr><expan>…</expan></choice>` abbreviation markup. The conversion code and BDD workflow independently establish that manuscript lines and abbreviation/expansion representations are preserved in the data path.

## No-effect-peeking chronology

Before this plan was committed:

- the source schema and several example snippets were inspected only to establish feasibility and define parsing rules;
- no count, effect size, line-final enrichment statistic, p-value, or candidate score was computed;
- no Voynich target statistic was computed.

After this file is committed, the E0 extraction/scoring implementation may be written once against the frozen rules below.

## Population

Primary population:

- descendants of the TEI `div[@type='book'][@n='07']`;
- ordinary body text only;
- exclude `fw` page headers/footers and other running furniture;
- exclude editorial-only material where it can be identified structurally;
- physical lines are defined only by source `<lb>` boundaries, never by sentence punctuation or reconstructed syntax.

### Boundary exclusions

For the primary analysis, exclude:

1. every `<choice>` that itself spans an `<lb>`;
2. both physical lines adjacent to an `<lb break='no'>`, because the boundary splits one lexical item and would create an artificial line-final/line-initial token fragment;
3. empty/markup-only lines;
4. lines for which token order cannot be reconstructed deterministically from TEI document order.

The number of exclusions must be reported before the effect statistic.

## Representation

For every physical line, construct two aligned lexical views:

1. **surface view**: `<abbr>` content for a `choice`, literal text otherwise;
2. **expanded view**: `<expan>` content for a `choice`, literal text otherwise.

Inline formatting tags such as `hi` do not create tokens. Punctuation elements do not count as lexical tokens.

### Lexical normalization

For matching underlying expanded forms only:

- Unicode NFC;
- casefold;
- strip leading/trailing non-letter marks;
- retain internal alphabetic Unicode characters and combining marks belonging to them;
- do **not** normalize `u/v`, `i/j`, morphology, spelling, lemmas, or editorial expansions across distinct strings.

The normalization function must be frozen in code before results are printed.

### Abbreviation outcome

An occurrence is `abbreviated=1` only when it is represented by a TEI `choice` with both `abbr` and `expan` and the normalized rendered `abbr` differs from the normalized rendered `expan`.

A literal non-`choice` occurrence of the same normalized expanded form is `abbreviated=0`.

Malformed `choice` elements and `expan=ERROR` are excluded and counted.

## Primary predictor

`FINAL1 = 1` when the lexical occurrence is the final complete lexical token on its physical manuscript line, otherwise `0`.

The primary test is restricted to normalized expanded lexical forms that have at least one abbreviated and at least one unabbreviated occurrence in the eligible population. No minimum frequency is chosen after seeing the effect.

## Primary statistic and exact null

For each eligible lexical form `i` freeze:

- `n_i`: eligible occurrences;
- `a_i`: abbreviated occurrences;
- `f_i`: FINAL1 occurrences;
- `x_i`: abbreviated FINAL1 occurrences.

Primary observed statistic:

`X = sum_i x_i`

Under the null, abbreviation labels are exchangeable **within each expanded lexical form** while preserving `n_i`, `a_i`, and `f_i`. Therefore each stratum follows the corresponding hypergeometric null. Convolve the per-stratum hypergeometric distributions exactly where computationally practical; otherwise use a fixed-seed permutation with at least 100,000 draws and report that the result is Monte Carlo rather than exact.

Report:

- `X`;
- null expectation `E[X] = sum_i a_i f_i / n_i`;
- standardized `(X-E[X])/sqrt(Var[X])` where variance is defined;
- one-sided enrichment p-value `P(X_null >= X_obs)`;
- two-sided tail result as a descriptive sensitivity.

The directional hypothesis is **line-final enrichment**, so the preregistered confirmatory p-value is one-sided.

## Frozen sensitivity

Repeat the same construction with:

`FINAL2 = 1` for either of the final two complete lexical tokens on a physical line.

This is a sensitivity only. It may not rescue a failed primary.

## Specificity / diagnostics

Report without changing the primary decision:

- raw abbreviation rate in FINAL1 vs non-FINAL1;
- number of eligible lexical strata;
- total eligible abbreviated/unabbreviated occurrences;
- top contributing lexical strata by absolute deviation from their null expectation;
- page distribution of eligible occurrences;
- line-length distribution;
- an analogous `FIRST1` statistic as a non-gating positional diagnostic.

Do not select a better positional window, tokenization, lexical normalization, manuscript subset, or abbreviation subtype after seeing E0.

## E0 classification

`E0_POSITIVE_FEASIBILITY` only if:

1. primary `FINAL1` statistic is in the enrichment direction;
2. preregistered one-sided p <= 0.05;
3. FINAL2 sensitivity has the same direction.

Otherwise classify `E0_NO_EXTERNAL_SUPPORT_ON_THIS_SAMPLE` unless extraction/authority failure requires `E0_INVALID_OR_INDETERMINATE`.

No E0 outcome by itself promotes LM-A0 to LM-A1 because the authority is one working file from one manuscript/book.

## Replication gate before LM-A1

Even after `E0_POSITIVE_FEASIBILITY`, LM-A0 can be promoted only after a separately frozen E1 uses final/manually corrected external data and at least one independent manuscript/scribe population. The E1 plan must be committed before its effect is inspected.

If E1 does not replicate the line-conditioned effect under lexical control, LM-A0 is not promoted as the next Voynich mechanism candidate.

## Relation to Issue #179

The Voynich image-interruption discriminator remains sealed. E0/E1 concern ordinary external manuscript lineation and scribal abbreviation choice only. No Voynich illustration geometry, transcription, R5 score, or target label is used here.

A successful external replication would justify freezing a minimal LM-A1 architecture first; only after that may a separate Issue #179 target plan define same-height illustration interruptions versus actual next-line transitions.
