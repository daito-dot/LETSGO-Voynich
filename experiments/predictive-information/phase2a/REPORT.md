# Issue #94 / Issue #88 Phase 2A report — causal prefix inventory versus ordered history

Date: 2026-09-06
Authority: `FIRST_REVEAL_PROVENANCE.md`
Classification: **MIXED PREFIX + ORDER CONTRIBUTIONS**

## Executive result

Issue #92 showed that extending the edit-1 recency model beyond the previous 40 tokens to the entire preceding physical-leaf prefix improved held-out prediction by about `0.04693 bit/token`. Phase 2A asks what that apparent long-history gain actually contains.

The answer is not a single leaf-long memory effect.

The strongest order-free control, which keeps the frozen LOCAL40 predictor and adds only the accumulated causal-prefix token-family inventory, gains:

> **`+0.04431 bit/token`, positive in 5/5 folds.**

The full ordered `H=ALL,tau=128` model then beats that hybrid by only:

> **`+0.00262 bit/token`, positive in 4/5 folds.**

A separately matched random-lag control gives a larger order-sensitive contrast:

> **`+0.01976 bit/token`, positive in 5/5 folds.**

Therefore the Phase-1 `H=ALL` preference decomposes into **a dominant causal-prefix inventory effect plus a smaller reproducible order/lag-sensitive residual**.

## 1. Why Phase 2A was necessary

The Phase-1 B2 result was striking: all five nested selectors chose all preceding tokens on the physical leaf, `tau=128` and `pi=.30`. But those are model-grid outcomes, not direct evidence that the writer literally remembers the entire page.

A long causal prefix conveys at least two distinct kinds of information:

1. **inventory information** — which token families have already appeared and are therefore locally active;
2. **order/lag information** — which particular source occurrence appeared at which distance.

Those mechanisms can be separated prospectively without introducing semantic labels or hidden states.

## 2. Models

The experiment retains the Phase-1 support, five physical-leaf folds, V2 literal-surface probabilities and exact edit-distance-1 neighbour relation.

- **A0 LOCAL40**: frozen Phase-1 local anchor (`H=40,tau=32`).
- **A1 PREFIX-BAG-CV**: all preceding eligible source occurrences, equal source weights; pi nested-selected.
- **A2 ORDERED128-FIXED**: exact Phase-1 B2 reference (`H=ALL,tau=128,pi=.30`).
- **A3 PREFIX-BAG-FIXED**: A2 with uniform source weights and the same fixed pi.
- **A4 RANDOM-LAG-FIXED**: A2's exact recency-weight multiset randomly reassigned across the same prior source occurrences, five fixed randomizations.
- **A5 LOCAL_PLUS_PREFIX-CV**: retains A0 and adds A1's order-free all-prefix inventory with nested-selected mixing `rho`.
- **A6 RANDOM-LAG-CV**: same five A4 randomizations, but the randomized control's mixture strength is selected independently by nested likelihood.

A5 and A6 were added by prereveal Amendment A to avoid giving the ordered reference an unfair advantage by making controls discard local information or inherit an unsuitable mixture coefficient.

## 3. Mean held-out code length

| model | bits/token | relation to question |
|---|---:|---|
| A0 LOCAL40 | 9.596181 | <=40-token local anchor |
| A1 PREFIX-BAG-CV | 9.559030 | order-free causal prefix replacing local model |
| A2 ORDERED128-FIXED | **9.549254** | full ordered long-history reference |
| A3 PREFIX-BAG-FIXED | 9.559030 | matched uniform weighting |
| A4 RANDOM-LAG-FIXED | 9.569018 | matched lag reassignment |
| A5 LOCAL_PLUS_PREFIX-CV | **9.551875** | local + order-free prefix inventory |
| A6 RANDOM-LAG-CV | 9.569018 | calibrated lag reassignment |

The strongest order-free hybrid A5 is within `0.00262 bit/token` of the full ordered reference A2.

## 4. Prefix inventory is a major predictive source

Primary prefix contrast:

`G_prefix_cond = LOCAL40 - LOCAL_PLUS_PREFIX`

Mean `+0.0443059 bit/token`, positive in every outer fold.

| fold | gain, bit/token |
|---:|---:|
| 0 | +0.0360571 |
| 1 | +0.0388196 |
| 2 | +0.0622477 |
| 3 | +0.0561319 |
| 4 | +0.0282733 |

A5 selected `rho=.20-.21` in all five folds, close to the local mechanism's own memory-mixture scale. This is stable evidence that knowing the **order-free set/frequency mixture of already activated edit-1 token families in the causal leaf prefix** improves unseen-token prediction beyond the previous-40 history.

It does not establish that the inventory is semantic topic. It may reflect register, page-specific production choices, content, manuscript layout, or another slowly varying external/internal state.

## 5. Actual order contributes less, but does not vanish

### 5.1 Against the strongest hybrid

`G_order_hybrid = LOCAL_PLUS_PREFIX - ORDERED128`

Mean `+0.0026212 bit/token`; positive in 4/5 folds.

One fold reverses (`-0.00454`). The formal preregistered stability rule passes, but the effect size is tiny. This is the most conservative estimate of the incremental value of the ordered long-history model after a strong order-free inventory baseline is already present.

### 5.2 Against matched randomized lag assignment

`G_order_random_cv = RANDOM-LAG-CV - ORDERED128`

Mean `+0.0197641 bit/token`; positive in 5/5 folds.

The random-lag control preserves:

- the same causal prefix;
- the same eligible source occurrences;
- the same source-to-neighbour distributions;
- the same recency-weight multiset;

and destroys only the association between source identity and actual lag. All five nested selectors choose `pi_random=.30`, so the result is not explained by forcing the randomized control to use the ordered model's mixture strength.

This establishes that the actual source/lag assignment carries reproducible predictive information under the tested representation.

The different magnitudes of the hybrid and randomized contrasts matter. They show that “order information” is not a single scalar independent of the control model. The strongest hybrid absorbs nearly all of the total long-history gain, while source/lag permutation causes a larger degradation. The safe conclusion is therefore qualitative: **a small order-sensitive residual survives**, not that long-range order is the dominant source.

## 6. Relation to the Phase-1 result

Phase-1 long-history increment:

`LOCAL40 - ORDERED128 = 0.0469271 bit/token`.

Phase-2A order-free conditional prefix gain:

`LOCAL40 - LOCAL_PLUS_PREFIX = 0.0443059 bit/token`.

Numerically, the order-free prefix component accounts for roughly 94% of the Phase-1 increment if these nested-model differences are viewed descriptively. This fraction is not used as a causal partition or decision threshold because A5 and A2 are not an orthogonal additive decomposition.

The important inferential correction is:

> The earlier `H=ALL` preference should no longer be described primarily as evidence for a leaf-long memory mechanism.

Most of its held-out predictive benefit is recoverable from causal prefix inventory without preserving long-range order.

## 7. What remains unexplained

Two predictive components now require localization:

1. a large, slow **prefix-inventory** component;
2. a much smaller but reproducible **order/lag-sensitive** component.

Separately, Issue #92 already showed that observable line/paragraph position adds about `0.02893 bit/token` after the ordered B2 model.

The next scientific question is therefore not “which hidden state fits?” It is:

> **Which observable manuscript scale or production position explains the prefix-inventory effect, the residual ordered effect, and the separate layout-position gain, and which of these effects transport across independent strata?**

## 8. Next phase

Phase 2B should condition the Phase-2A baseline on observable document geometry before introducing richer latent models. A clean first layer can use only information already present in the ZL3b structural parse:

- within-line / across-line history;
- within-paragraph / across-paragraph history;
- paragraph-entry versus body;
- line-position bins.

Then, after an independent metadata authority is frozen, extend attribution to Currier/section/scribe or equivalent manuscript strata and carry the surviving effects into transport tests.

This ordering directly tests whether the apparent distance horizon is globally stable or is an aggregate of different local document regimes.

## 9. Claim boundary

Phase 2A does not establish language, plaintext, topic, semantics, cipher identity, author, syntax, hidden state, or a historical copy/mutate procedure. It does not prove visible spaces are words. It establishes only prospective held-out predictive attribution under the current space-delimited representation.