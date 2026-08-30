# Phase 60C — transferable entry vocabulary / formal-role test

Status: frozen before execution.

## Target
Test P60-3 from the Phase60 narrative.

Phase60B identified a stable carrier pattern across three token representations: paragraph body recovery increases k/t-family mass, near-family/edit1 activation and local continuity, while entry lines have higher TTR and longer units/tokens.

## Prediction
If paragraph entry is a recurring formal role rather than a section-specific accident, token-family / affix / slot-role preferences learned in some manuscript sections should identify entry vs body lines in held-out sections after controlling simple length and frequency effects.

## Primary design
- Labels: genuine paragraph line0 = entry; line2 = body.
- Grouping: physical leaf; no line from a held-out leaf may enter training/model selection.
- Outer transfer: leave one major section H/B/P/S/T out entirely.
- Controls: line token count matching/weighting; token frequency and mean-length baseline; section-blind evaluation.
- Candidate structural predictors fixed before execution: k/t-family mass and balance, near-family/edit1 activation, local previous-10 continuity, token length distribution, TTR, first/last unit patterns, frequent prefix/suffix families, audited slot-role features where available.
- Compare against a nuisance-only baseline containing token count, mean length and broad frequency summaries.

## Hard falsification
P60-3 fails if held-out-section entry/body prediction collapses to nuisance baseline, if predictive token families reverse arbitrarily across sections, or if performance depends on a single section.

## Interpretation ceiling
Successful transfer establishes a manuscript-wide formal entry role. It does not establish headings, recipes, plaintext semantics, or cipher meaning.
