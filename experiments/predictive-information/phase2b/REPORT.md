# Issue #96 / Issue #88 Phase 2B report — predictive dependence across line and paragraph boundaries

Date: 2026-09-06
Authority: `FIRST_REVEAL_PROVENANCE.md`
Classification: **MULTISCALE**

## Executive result

The earlier finding that Voynich prediction improves when the model can consult a long causal leaf prefix is **not well described as one uniform token-distance memory horizon**.

After the frozen LOCAL40 predictor is accounted for:

- extra same-line order-free inventory adds exactly `0`;
- current-paragraph inventory adds only `+0.00071 bit/token`;
- adding inventory from previous paragraphs on the same physical leaf adds `+0.04360 bit/token`, positive in 5/5 folds;
- actual lag/order inside the current paragraph does not survive matched randomization;
- actual lag/order among previous-paragraph sources survives only weakly: `+0.00061 bit/token`, positive in 4/5 folds.

The dominant slow predictive source is therefore **previous-paragraph token-family inventory**, not a smooth continuation of the same local recency mechanism.

## 1. What was tested

For every held-out target, all causal edit-1 source occurrences were split prospectively into observable structural pools:

1. earlier tokens in the same line;
2. earlier tokens in the current paragraph;
3. tokens in previous paragraphs on the same physical leaf;
4. their full causal leaf-prefix union.

All new models were conditional additions to the already frozen LOCAL40 probability. New scalar mixture weights were selected by nested held-out literal-surface likelihood only. Ordered controls used the already frozen `tau=128`; no distance/horizon parameter was reopened.

Matched random-lag controls preserved the exact source set, source-to-neighbour distributions, and recency-weight multiset while destroying which prior source received which lag weight.

## 2. Reference regressions

The implementation exactly reproduced the archived Phase-1 LOCAL40 and ORDERED128 code lengths and the Phase-2A LOCAL+LEAF_PREFIX_BAG selections/code lengths in every outer fold. This is important because the boundary result is measured as a decomposition of those already-established predictive effects rather than as a new model search.

## 3. Inventory localization

### Same line

`LOCAL + LINE_BAG = LOCAL40 = 9.5961811 bits/token`.

Every outer fold selected `alpha=0`. The preceding same-line inventory contains no additional order-free predictive information once the existing LOCAL40 recency model is present.

### Current paragraph

`LOCAL + CURR_PARA_BAG = 9.5954733 bits/token`.

Gain over LOCAL40:

> `+0.0007078 bit/token`, positive 4/5 folds.

This passes the frozen stability rule but is tiny. Selected mixture weights are only `.01-.02`.

### Previous paragraphs on the same physical leaf

`LOCAL + PREV_PARAS_BAG = 9.5439510 bits/token`.

The previous-paragraph-only model selects much larger mixture weights, `.23-.25` across all folds.

The primary sequential contrast, adding previous-paragraph information beyond the current-paragraph model, is:

> **`+0.0435981 bit/token`, positive 5/5 folds.**

This is roughly two orders of magnitude larger than the current-paragraph inventory increment.

A particularly informative diagnostic is that the previous-paragraph-only pool performs better than the full causal leaf-prefix bag (`9.5439510` vs `9.5518752 bits/token`). This means simply adding the current-paragraph source inventory to the slower previous-paragraph inventory does not help under this model; it dilutes the stronger predictor.

This should not be interpreted as an orthogonal causal decomposition, but it strongly argues against a single homogeneous inventory process operating identically across all preceding positions.

## 4. Order/lag localization

### Current paragraph

Matched random-lag is microscopically better than actual ordered lag in all five folds:

`G_order_within_para = -0.0000877 bit/token`, positive 0/5.

Thus Phase 2B finds no evidence that the exact source-to-lag association inside the current paragraph matters beyond LOCAL40 and the tested pool composition.

### Previous paragraphs

Actual source-to-lag association beats its matched randomized control by:

> `+0.0006074 bit/token`, positive 4/5 folds.

This is formally reproducible but extremely small, and one fold reverses. The main previous-paragraph effect is therefore inventory-like rather than precise long-range ordering.

## 5. What this says about the earlier tau=32 / tau=128 result

The earlier global recency fits used token distance and applied one decay law across a physical leaf. Phase 2B shows why that can be misleading as a mechanistic interpretation.

A distance-only model can partially exploit a structural fact that is better described as:

> **the set and frequencies of edit-1 token families already established in earlier paragraphs on the same physical leaf predict later tokens strongly.**

Once this boundary structure is exposed explicitly, extra current-paragraph inventory contributes almost nothing and current-paragraph lag order contributes nothing measurable.

So the current evidence no longer supports phrasing the main effect as “the manuscript looks back about 20–100 tokens with one common memory kernel.” The safer description is a combination of:

- short local recency captured by LOCAL40;
- a strong slower previous-paragraph/leaf inventory state;
- a very small residual cross-paragraph lag/order effect.

## 6. Formal MULTISCALE classification versus effect-size interpretation

The frozen classifier returns `MULTISCALE` because both:

- current-paragraph inventory passes at 4/5 folds;
- cross-paragraph inventory and cross-paragraph order pass.

But the effect sizes are highly asymmetric:

- current-paragraph inventory: `+0.00071 bit/token`;
- cross-paragraph inventory: `+0.04360 bit/token`.

Therefore the scientifically useful statement is not merely “both scales matter.” It is:

> **the dominant nonlocal predictive component crosses paragraph boundaries, while within-paragraph residual effects beyond LOCAL40 are negligible by comparison.**

## 7. Next frontier

The next attribution step should split `PREV_PARAS` without introducing external semantic labels.

The most informative prospective decomposition is:

- immediately previous paragraph versus older paragraphs;
- previous paragraphs on the same transcription side/page versus paragraphs carried across recto/verso within the same physical leaf;
- paragraph index within the side/leaf.

This matters because the current parser's `leaf` key collapses `f###r` and `f###v` to the same numeric physical leaf, while `document` retains the side identifier. A portion of the present previous-paragraph signal could therefore be a page-side state or a cross-side transport effect rather than a generic paragraph-history mechanism.

Only after this structural decomposition should Currier/section/scribe metadata be introduced and transport tested.

## 8. Claim boundary

Phase 2B does not identify topic, meaning, syntax, plaintext, cipher family, author, or latent state. It does not prove paragraph boundaries are semantic units or that visible spaces are words. It establishes a prospective held-out predictive localization under the current space-delimited representation.