# Phase 60D — prospective recovery prediction

Status: frozen before execution.

## Target
Test P60-4 from `research/NARRATIVE_HYPOTHESIS_PHASE60.md`.

## Core question
Does the structural composition of a paragraph entry line predict the later body state of that same paragraph beyond section/page-level baselines?

## Primary endpoint
For eligible paragraphs with at least three usable lines, predict the standardized structural fingerprint of line2 from line0.

## Evaluation
- 5-fold outer CV grouped by physical leaf.
- Compare four models on identical held-out folds:
  1. global mean baseline;
  2. metadata baseline (section + Currier + hand where available);
  3. page-context baseline using only other paragraphs/lines on the same page and only when leakage-safe;
  4. metadata/page context + entry-line structural fingerprint.
- Primary statistic: held-out multivariate MSE and incremental R2/MSE reduction from adding entry-line state.
- Secondary statistic: predict the line0->line2 recovery vector rather than absolute line2 state.
- Report H/B/P/S/T separately.

## Hard falsification
P60-4 is weakened/rejected if entry-line features do not improve held-out prediction of their own paragraph body beyond nuisance/page baselines, or if any apparent gain is confined to one section.

## Interpretation ceiling
Success supports an initialization/state-carrying role for paragraph entry. It does not identify semantics, plaintext, headings, or cipher values.
