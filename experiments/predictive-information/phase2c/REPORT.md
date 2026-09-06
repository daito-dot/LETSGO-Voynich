# Issue #98 Phase 2C — corrected previous-paragraph decomposition

Date: 2026-09-06
Status: **AUTHORITATIVE RESULT**
Parent: Issue #88

## Question

After source-order correction, Phase 2B established that the dominant slow predictive source is previous-paragraph edit-1 token-family inventory on the same numeric physical leaf, with a smaller previous-paragraph order/lag residual.

Phase 2C asks two narrower questions:

1. Is the previous-paragraph signal concentrated in the immediately preceding paragraph or distributed across older paragraphs?
2. Is it confined to the same transcription page/panel, or does predictive inventory survive across page/panel boundaries within the same numeric physical leaf?

The experiment is prediction-only and uses corrected causal source order.

## Formal classifications

Temporal topology:

> **TEMPORAL MULTISCALE**

Page/panel topology:

> **CROSS-SIDE TRANSPORT SURVIVES**

These labels describe predictive localization only. They do not establish syntax, topic, semantic page state or content transport.

## Temporal inventory decomposition

Conditional held-out gains:

- immediately preceding paragraph, conditional on older paragraphs: `+0.0070407 bit/token`, positive `5/5` folds;
- older paragraphs, conditional on the immediately preceding paragraph: **`+0.0367964 bit/token`**, positive `5/5` folds.

Both pass the frozen stability rule, hence `TEMPORAL MULTISCALE`. The magnitude is strongly asymmetric: the older accumulated paragraph inventory contributes roughly five times the conditional gain of PREV1.

Mean code lengths:

- LOCAL40: `9.5943670 bits/token`;
- PREV1-only bag: `9.5815945`;
- OLDER-only bag: `9.5518388`;
- jointly selected PREV1+OLDER model: `9.5447981`;
- corrected all-previous-paragraph bag regression: `9.5443611`.

The split joint model is not materially better than the unsplit ALL_PREV bag. Its value is attribution: both temporal pools are predictive, with older accumulated inventory dominant.

## Page/panel inventory decomposition

Conditional held-out gains:

- previous paragraphs on the same document/page-panel, conditional on cross-panel history: `+0.0205711 bit/token`, positive `5/5`;
- previous paragraphs on earlier page/panels of the same numeric physical leaf, conditional on same-panel history: **`+0.0237448 bit/token`**, positive `5/5`.

Cross-panel inventory therefore survives prospectively, and same-panel inventory also remains independently predictive.

Mean code lengths:

- same-panel-only bag: `9.5658477`;
- cross-panel-only bag: `9.5626740`;
- jointly selected same+cross panel model: **`9.5421029`**;
- unsplit ALL_PREV bag: `9.5443611`.

Unlike the temporal split, the page/panel split modestly improves over the unsplit previous-paragraph bag. The nested selectors consistently allocate substantial mass to both components:

- SAME_SIDE weights: `.14,.14,.13,.13,.13`;
- CROSS_SIDE weights: `.16,.16,.17,.17,.17`.

Thus the previous-paragraph inventory is not merely a within-panel phenomenon under this representation.

CROSS_SIDE context is available for about `50.83%` of scored positions. On positions where it exists, the joint side model saves about `0.04786 bit/token` relative to the same-side-only model; this restricted statistic is diagnostic only and does not enter classification.

## Order/lag localization

Matched random-lag controls localize the smaller order-sensitive residual:

- PREV1 actual lag vs random lag: `-0.0002645 bit/token`, positive `1/5` — FAIL;
- OLDER actual lag vs random lag: **`+0.0057373`**, positive `5/5` — PASS;
- SAME_SIDE_PREV actual lag vs random lag: `+0.0001767`, positive `3/5` — FAIL;
- CROSS_SIDE_PREV actual lag vs random lag: **`+0.0022930`**, positive `4/5` — PASS.

Therefore the corrected Phase-2B order residual does not localize to the immediately preceding paragraph. It is associated mainly with older paragraph history and, more weakly, with cross-panel history.

The restricted-to-cross-context order diagnostic is slightly negative (`-0.0002245 bit/token`) and is not the primary statistic; the whole-population matched-model contrast above is the preregistered decision quantity.

## Working structural picture

The predictive hierarchy is now more specific:

1. compact token-internal V2 construction;
2. stable short local edit-1 recency (`H=40,tau=32`);
3. slower paragraph-scale token-family inventory;
4. within that slower inventory, **older accumulated paragraphs dominate over PREV1**;
5. both same-panel and cross-panel previous history contribute independently;
6. the smaller actual-order residual is concentrated in OLDER and CROSS_SIDE pools, not PREV1/current-panel-local order;
7. observable line/paragraph position remains an independent predictor from corrected Phase 1.

This is inconsistent with a simple interpretation in which the writer only references the immediately preceding paragraph or a single fixed-length token window. It is more consistent, at the predictive-model level, with a slowly varying page/folio-scale inventory or observable/external production state plus a smaller recency/order component.

## Next licensed step

Proceed to independently defined manuscript strata and transport tests rather than fitting a rich latent state.

The next experiment should ask whether the corrected local + paragraph-inventory mechanism transports with stable parameters across independently authoritative strata such as Currier A/B, section/domain and scribe where metadata authority and support are sufficient.

Required separation:

- within-stratum fit vs cross-stratum transport;
- support/vocabulary mismatch vs mechanism mismatch;
- universal production rule vs observable document-state dependence.

No latent-state interpretation is licensed yet.

## Provenance

See `FIRST_REVEAL_PROVENANCE.md`.

Authoritative successful run: `34020713068`; artifact ID `9985408973`; result JSON SHA-256 `16cad5206cafc5ae1a856427c705afddfc591e2e706962de8bae326d32c1f149`.

## Claim boundary

No plaintext, language, syntax, topic, cipher identity, author, semantics, content transport or latent state is established. Visible spaces remain analysis production units, not proven linguistic words.