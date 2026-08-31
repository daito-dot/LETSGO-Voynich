# Phase 69B — locate the missing long-range family state across paragraph boundaries

Status: **FROZEN BEFORE H69-P2 REVEAL**

Date: 2026-08-31

## Motivation

Phase69A prospectively showed that the frozen A1 generator underpredicts same-physical-leaf non-identical edit1-family recurrence at distances 41–320 tokens. The contrast is specific: long-range **exact-token** recurrence is matched almost perfectly, while long-range **family/variant** recurrence is not.

Phase69B asks where that missing state lives in the document hierarchy before any new generator is added.

## Primary question

> Is the Phase69A A1 mismatch specifically carried by edit1-family returns that cross paragraph boundaries on the same physical leaf?

If yes, the missing process survives paragraph transitions and an A2 model needs a longer-lived leaf-level state/cache or equivalent mechanism.

If no, but the mismatch remains within paragraphs, the next model should refine paragraph-internal organization instead of introducing a leaf-persistent state.

No Phase69B cross/within statistic has been inspected before this freeze.

## Frozen source, folds, and A1 mechanism

Reuse Phase69A without modification:

- ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- source retrieval commit `31819c914061cc6b63bbf4983e33d643ede52e46`;
- five physical-leaf folds from `phase61c_joint_model.py`;
- frozen per-fold A1 `(entry_strength, local_family_p)`;
- training-vocabulary-only A1 generation;
- exactly 50 A1 predictive realization indices;
- deterministic A1 seed family already used by Phase69A;
- exactly 40 within-leaf order-null shuffles per target/generated dataset.

No A1 parameter is selected from Phase69B.

## Physical-leaf sequence with paragraph identity

For target and generated datasets:

1. concatenate tokens in manuscript paragraph order and line order within each physical leaf;
2. retain, for every token position, its paragraph identity `(page, pid)`;
3. paragraph/page-side boundaries do not reset the physical-leaf token sequence;
4. eligible physical leaf requires at least 321 tokens, identical to Phase69A.

## Frozen distance bins

Exactly Phase69A:

- `L1 = 41–80`
- `L2 = 81–160`
- `L3 = 161–320`

Only preceding positions in the full frozen interval are considered. A relation-specific denominator includes a current token/bin only when at least one candidate position of that relation class exists inside the bin.

## Frozen relation classes

For a current token at paragraph `P`:

### Primary: CROSS_PARAGRAPH

Candidate preceding positions in the distance bin whose paragraph identity is **not** `P`.

An edit1 cross-paragraph hit occurs when at least one candidate token is a non-identical Levenshtein-distance-1 neighbor of the current token.

### Secondary localization: WITHIN_PARAGRAPH

Candidate preceding positions in the same distance bin whose paragraph identity **is** `P`.

The same non-identical edit1 hit rule is used.

Exact token equality is not an edit1 hit.

## Paragraph-geometry-preserving within-leaf null

For each target or generated dataset:

- hold every physical leaf length fixed;
- hold the paragraph identity assigned to every token position fixed;
- hold the complete physical-leaf token multiset fixed;
- independently shuffle token identities across positions within that leaf;
- use exactly 40 deterministic shuffles.

Thus the null preserves paragraph lengths/boundary geometry and the leaf vocabulary/inventory, but breaks token-family placement relative to those boundaries.

For each bin and relation class:

`excess = observed hit rate - median shuffled hit rate`.

## Primary scalar

For every fold:

`E_cross = excess_cross_L1 + excess_cross_L2 + excess_cross_L3`.

Voynich primary statistic:

`V_cross = mean(E_cross_Voynich_fold)` across all five frozen folds.

For each frozen A1 predictive realization `r = 0..49`:

`A_cross,r = mean(E_cross_A1_fold,r)` across the same five folds.

## Primary one-sided model check

The preregistered failure direction is again A1 underprediction:

`p_cross = (1 + count(A_cross,r >= V_cross)) / 51`.

Report `delta_cross = V_cross - mean(A_cross,r)`.

Classification:

- if `p_cross <= 0.05` and `delta_cross > 0`:
  **CROSS-PARAGRAPH PERSISTENT FAMILY STATE REQUIRED**;
- otherwise:
  **NO DETECTED CROSS-PARAGRAPH FAMILY EXCESS BEYOND FROZEN A1**.

This is a model-adequacy classification, not a semantic interpretation.

## Secondary localization: within-paragraph edit1

Compute the identical `E_within` statistic for same-paragraph candidate positions and compare Voynich to the same 50 A1 predictive realizations with an upper-tail plus-one p-value.

This secondary test cannot overturn the primary classification. It localizes the deficit:

- primary cross positive + within null -> missing state is specifically paragraph-persistent;
- both positive -> missing mechanism acts at more than one scale;
- cross null + within positive -> paragraph-internal organization is the more likely missing layer;
- both null -> Phase69A mismatch depends on mixing cross/within candidates or another interaction and should be decomposed differently before adding A2.

## Secondary exact-token cross-paragraph control

Repeat the CROSS_PARAGRAPH analysis using exact token equality instead of edit1 family membership.

This tests whether the Phase69A edit1/exact dissociation survives explicit paragraph-boundary localization. It cannot rescue or overturn the primary edit1 result.

## Descriptive outputs

For target and A1 report:

- relation-specific available denominator counts by bin;
- observed and null-median recurrence rates;
- signed excess by bin;
- normalized signed-excess profile;
- five Voynich fold `E_cross` values;
- A1 predictive interval and profile distance.

## Interpretation limits

A cross-paragraph A1 deficit would establish only that the frozen ten-token mechanism is missing a family-level state that persists/reappears across paragraph boundaries on the same physical leaf.

Candidate mechanisms still include:

- semantic/topic or recipe/component persistence;
- cipher-key / encoding-state persistence;
- scribal/orthographic state;
- an explicitly nonsemantic long-lived family cache.

Do not alter paragraph identities, bins, eligibility, null shuffles, A1 parameters, predictive realization count, relation definitions, or failure direction after reveal.
