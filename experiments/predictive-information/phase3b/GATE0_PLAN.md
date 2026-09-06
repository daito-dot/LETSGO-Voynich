# Issue #107 / Issue #88 Phase 3B — observable metadata Gate 0

Date: 2026-09-06
Status: **FROZEN BEFORE ANY PHASE-3B PREDICTIVE SCORE**

## Purpose

Audit whether independently defined IVTFF metadata can disentangle the Currier-associated PREV_PARAS strength difference found in Phase 3A.

This is a score-free metadata/support gate. It may license a later factor but may not evaluate prediction.

## External semantics

Per the IVTFF format authority:

- `$I`: illustration type — A astronomical, B biological, C cosmological, H herbal, P pharmaceutical, S marginal-stars, T text-only, Z zodiac;
- `$H`: Lisa Fagin Davis writing hand — 1–5, or `@` when text tags change the value within the page;
- `$C`: legacy Currier hand — secondary audit/control;
- `$L`: Currier language/text-section label already frozen by Phase 3A.

Page variables set to `@` are unresolved before their first corresponding text tag. A text tag applies on its own line and forward until changed or the page ends.

## Resolution rules

For I/H/C/L separately:

1. read the page-header variable literally;
2. page start resets prior-page state;
3. if the header value is not `@`, it is the resolved page value unless an illegal tag is encountered;
4. if the header value is `@`, resolved state begins `UNSET` and changes only through `<@X=v>` tags;
5. tags on a line apply to the full line before token metadata is assigned;
6. duplicate conflicting tags for one variable on one line are invalid;
7. a text tag for X when page `$X` is not `@` is reported as a conformance violation;
8. missing header variable remains `MISSING` and is not imputed;
9. the Phase-3A Currier fallback (`f57v -> B`) remains the page-level `$L` authority for the Currier cross-tab. The line-level raw L resolution is audited separately and must be compared against that authority.

No missing H/I/C value may be inferred from imagery, page name, neighbouring pages, comments or prediction.

## Population mapping

Reconstruct the same P-locus paragraph/line/token population as the frozen parser and assert:

- every token-bearing source P line maps to the expected parsed `document:pN` and line index;
- visible-token count on every mapped line matches the parsed item;
- parser-accepted flags are taken from the frozen token parser result;
- total visible/accepted counts match the current corpus;
- corrected source-order authority verifies;
- frozen physical-leaf fold identity is unchanged.

## Required outputs

For I/H/C/L:

- raw page-header distribution including MISSING and `@`;
- pages and sequences of text-tag changes;
- conformance violations;
- resolved visible/accepted-token, item, document and leaf counts per level;
- leaves containing more than one resolved level;
- accepted-token support by level and frozen fold;
- unresolved (`MISSING`/`UNSET`/other unsupported) population.

Cross-tabs, using parser-accepted tokens:

- L × I;
- L × H;
- L × C;
- I × H;
- L × I × H.

Each cell reports accepted tokens, unique items and unique numeric leaves, plus the number of frozen folds with nonzero accepted support.

## Identifiability rule

For each candidate factor X in priority order H, I, C, consider only resolved non-`@`/non-MISSING/non-UNSET levels.

A level x is cross-Currier usable iff:

- L=A and L=B both occur at that level;
- each L×x cell has parser-accepted tokens in >=4/5 frozen folds;
- the level spans >=2 numeric physical leaves.

A candidate factor is `CROSS-CURRIER IDENTIFIABLE` iff at least two levels are cross-Currier usable.

If multiple candidates qualify, license the first by the pre-frozen priority:

1. H (Davis writing hand)
2. I (illustration/domain)
3. C (legacy Currier hand)

The Gate result must report every factor/level, not only the licensed one.

If no factor qualifies, classification is `NO ADEQUATELY CROSSED OBSERVABLE FACTOR` and predictive Phase 3B remains blocked pending a new support-preserving design.

## Firewall

- no held-out code length;
- no model fitting or hyperparameter selection;
- no S1/S2/H62/R1 or Issue #84 target;
- no image access;
- no proposed plaintext/semantics;
- no latent state;
- no predictive outcome used in identifiability/licensing;
- no post-audit reordering of H/I/C priority.
