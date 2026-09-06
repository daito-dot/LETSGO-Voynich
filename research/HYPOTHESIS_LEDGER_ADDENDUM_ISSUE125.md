# Hypothesis ledger addendum — Issue #125

Date: 2026-09-06
Parent: Issue #88 / Issue #118 / Issue #121 / Issue #123

| Hypothesis / question | Status | Evidence / consequence |
|---|---|---|
| Issue #123 LINECONT2 gain is only a generic source-line-start vs line-interior onset distribution effect | **REJECTED as complete explanation** | POS2 captures a smaller robust component (`G_position=+0.00889185`, 5/5), but explicit previous-terminal identity adds `G_identity=+0.02026956`, 5/5 |
| Immediately previous token terminal identity predicts the next token onset within the same source line | **SUPPORTED — SMALL, ROBUST** | `G_identity` positive in all five outer folds after generic line-position onset is already modeled |
| EDGE2 introduced extra flexibility relative to Issue #123 LINECONT2 | **REJECTED / EXACT EQUIVALENCE** | max inner and outer token-logp difference EDGE2 vs LINECONT2 = `0.0`; parent G_line and weights reproduce exactly |
| The terminal-identity contribution is confined to one reported line-position stratum | **NOT SUPPORTED descriptively** | POS2→EDGE2 contribution is positive for ENTRY/BODY and FIRST/MIDDLE/FINAL strata |
| Generic hidden long sequence memory is needed to explain the L2 residual | **FURTHER WEAKENED** | a large share of the line-local gain is explained by one explicit observable edge: previous terminal → next initial |
| Terminal→initial edge strength transports across Currier A/B | **OPEN — NEXT TRANSPORT QUESTION** | should be tested prospectively using source-trained edge parameters / architecture without hand confounding |
| Material residual remains after adding the explicit edge directly to the observable core | **OPEN — NEXT CAPACITY QUESTION** | required before latent-state interpretation |
| Source line is a natural-language sentence / semantic clause | **NOT ESTABLISHED** | all current evidence is predictive production topology, not semantics |

## Working update

The economical structural hypothesis is now:

> Visible certain-space units are bounded construction episodes with compact internal grammar. Cross-unit structure is multiscale: a broadly transportable edit-near recurrence process, slower prior-inventory effects, generic line-position onset differences, and a small direct within-line terminal→initial edge. The direct edge is observable and local; the same short context resets at line breaks.

This remains a structural predictive model, not a decipherment or historical mechanism claim.
