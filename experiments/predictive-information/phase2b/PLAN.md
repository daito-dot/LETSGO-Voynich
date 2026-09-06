# Issue #96 / Issue #88 Phase 2B — line/paragraph boundary localization

Date frozen: 2026-09-06
Parent program: Issue #88
Implementation issue: #96
Entry authority: Phase 2A / Issue #94 / PR #95
Status: **PREREGISTERED BEFORE PHASE-2B OUTER SCORING IMPLEMENTATION**

## Governing question

> At what observable document scale do the causal-prefix inventory effect and the surviving order-sensitive effect live: within the current line, elsewhere in the current paragraph, or across previous paragraphs on the same physical leaf?

This phase directly tests whether the apparent memory horizon is effectively uniform or an aggregate of distinct document-scale regimes.

## Population and firewall

Reuse the frozen ZL3b source, five physical-leaf folds, V2 literal-surface scoring, parser support and exact edit-distance-1 training-vocabulary neighbour relation from Phases 0–2A.

For each target, only preceding visible tokens on the current physical leaf are causal context. The parser's existing line records and `<%>` paragraph/item boundaries are the only new structural authority.

Unavailable to model selection/classification: S1/S2/H62/R1, Issue #84 target ranges, Currier/section/scribe labels, page imagery, proposed plaintext, semantic labels and future tokens.

## Disjoint causal source pools

At every target split the preceding eligible source occurrences into:

- `LINE`: earlier tokens in the same line;
- `PARA_PRIOR_LINES`: earlier tokens in the same paragraph/item but earlier lines;
- `PREV_PARAS`: tokens in earlier paragraph/items on the same physical leaf.

Define compound pools:

- `CURR_PARA = LINE union PARA_PRIOR_LINES`;
- `LEAF_PREFIX = CURR_PARA union PREV_PARAS`.

All pools contain only occurrences with at least one training-vocabulary exact edit-1 neighbour, exactly as in Phase 2A.

## Frozen base and regression authorities

For outer fold f:

`LOCAL40` uses H=40, tau=32 and the already frozen pi values:

`.21, .21, .20, .21, .21` for folds 0..4.

Required Phase-1 outer code-length regression:

`9.7455321345, 9.6543793895, 9.4455240875, 9.4785097013, 9.6569602881`.

`ORDERED128` diagnostic uses the exact Phase-1 A2 reference H=ALL, tau=128, pi=.30 with expected outer code lengths:

`9.7049938528, 9.6121495322, 9.3878142898, 9.4172539561, 9.6240585636`.

`LEAF_PREFIX_BAG` must reproduce Phase-2A A5. Its frozen nested rho values are:

`.20, .21, .20, .20, .21`.

Expected A5 outer code lengths:

`9.7094750841, 9.6155597839, 9.3832763858, 9.4223777902, 9.6286869561`.

No reference parameter is reselected for the regression gate.

## Pool distributions

For each pool, let Q_bag be the equal-occurrence average of the same source-to-edit1-neighbour distributions used by Phase 2A.

Let Q_order use actual source lag d with frozen weight exp(-d/128). No tau or history-length search is permitted.

For random-lag controls, preserve the exact eligible source set, source-to-neighbour distributions and recency-weight multiset at every target, but prospectively permute weights across source occurrences. Use exactly five fixed randomizations 0..4. Namespace includes only phase/pool/randomization/leaf/position and never target identity. No rerolls.

## Conditional models on LOCAL40

All new boundary-localization models use the frozen LOCAL40 probability as their base.

For bag/ordered component Q:

`P = (1-alpha) P_LOCAL + alpha Q`

when the pool is available, else exactly P_LOCAL.

For each new bag or ordered model, alpha is selected independently by nested literal-surface likelihood on the outer-training population from `0.00..0.30` step `.01`, exact tie -> smaller alpha.

For each random-lag model, alpha is selected by the arithmetic mean inner-validation log likelihood over all five fixed randomizations; outer score is the arithmetic mean bits/token over those same five randomizations. No seed selection.

## Inventory models

Fit:

- `LINE_BAG`;
- `CURR_PARA_BAG`;
- `PREV_PARAS_BAG`;
- `LEAF_PREFIX_BAG` regression.

Primary inventory contrasts:

- `G_line_inventory = bits(LOCAL40) - bits(LINE_BAG)`;
- `G_within_para_inventory = bits(LOCAL40) - bits(CURR_PARA_BAG)`;
- `G_cross_para_inventory = bits(CURR_PARA_BAG) - bits(LEAF_PREFIX_BAG)`;
- `G_prev_para_inventory = bits(LOCAL40) - bits(PREV_PARAS_BAG)` diagnostic.

The sequence LOCAL40 -> CURR_PARA_BAG -> LEAF_PREFIX_BAG is the primary boundary localization. Effects are not reported as orthogonal causal shares.

## Order models

Fit, conditional on LOCAL40:

- `CURR_PARA_ORDERED128`;
- `CURR_PARA_RANDOM_LAG`;
- `PREV_PARAS_ORDERED128`;
- `PREV_PARAS_RANDOM_LAG`;
- `LEAF_ORDERED128_LOCALBASE` diagnostic.

Primary order contrasts:

- `G_order_within_para = bits(CURR_PARA_RANDOM_LAG) - bits(CURR_PARA_ORDERED128)`;
- `G_order_cross_para = bits(PREV_PARAS_RANDOM_LAG) - bits(PREV_PARAS_ORDERED128)`.

Required diagnostics:

- ordered-vs-bag for CURR_PARA and PREV_PARAS;
- LEAF_ORDERED128_LOCALBASE vs LEAF_PREFIX_BAG;
- all selected alpha values and fixed-randomization per-seed code lengths.

## Stability and classification

A contrast passes iff mean > 0 and positive in at least 4/5 outer folds. This is a preregistered stability rule, not a p-value.

Define:

- `WITHIN := G_within_para_inventory passes OR G_order_within_para passes`;
- `CROSS := G_cross_para_inventory passes OR G_order_cross_para passes`.

Classification:

- `MULTISCALE` iff WITHIN and CROSS;
- `PREDICTIVE DEPENDENCE CROSSES PARAGRAPH BOUNDARIES` iff CROSS and not WITHIN;
- `PREDICTIVE DEPENDENCE LOCALIZES WITHIN PARAGRAPH` iff WITHIN and not CROSS;
- `BOUNDARY ATTRIBUTION INCONCLUSIVE` otherwise;
- `MODEL / SUPPORT INVALID` if reference regression, probability normalization, source-pool partition, randomization invariant or causal-prefix discipline fails.

Always state separately whether inventory and/or order supports each scale.

## Secondary state diagnostics

After primary models are frozen, summarize primary per-token code-length gains descriptively by:

- paragraph `ENTRY` = first line vs `BODY` = later lines;
- LINE4 = `SINGLE`, `FIRST`, `MIDDLE`, `FINAL`.

These summaries never change model selection or classification. No state-specific tau/alpha is fitted in Phase 2B.

## Interpretation boundary

A cross-paragraph result means predictive information survives an explicit paragraph production boundary under this representation. It does not identify topic, semantics, syntax or a literal memory mechanism.

A within-paragraph result means a paragraph boundary is a useful localization scale; it does not prove that paragraphs are semantic units.

Any state-specific horizon model, Currier/section/scribe attribution or transport test requires a subsequent preregistration.