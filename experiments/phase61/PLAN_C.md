# Phase 61C — A1 joint-model test

Status: frozen before execution.

## A1 architecture

A1 is the first explicit repair of rejected A0. It adds exactly one new mechanism:

1. **boundary-aware entry mixture** — paragraph line0 is drawn from a global entry-biased token-shape mixture, as in A0;
2. **local-family body activation** — from line1 onward, token generation may reuse or mutate a token from the recent local window with one edit, otherwise drawing from the ordinary body inventory.

No persistent paragraph latent state is allowed. No section-specific grammar is allowed. No additional line-position rule is added. Any further repair after this test becomes A2.

## Frozen parameters / search freedom

The entry-mixture strength may use the coarse Phase61A grid only: 0.5, 1.0, 1.5, 2.0.

The new local-family activation probability may use only: 0.05, 0.10, 0.20, 0.30.

Model selection must be based on training physical leaves only. Held-out leaves evaluate the selected pair.

## Joint targets

Evaluate simultaneously:

- real-entry-minus-pseudo projection on the training-derived Voynich direction;
- local previous-10 near-family fraction;
- line-position eta2 mean and max;
- edit1 type density, marked non-independent if empirical Voynich vocabulary is used;
- absence of persistent line0 prospective memory is structural by construction and must not be contradicted by adding paragraph state.

## Selection rule

Within each outer physical-leaf fold, choose the parameter pair minimizing mean squared relative error across the three nontrivial training targets:

1. entry projection;
2. local-prev10 fraction;
3. line-position eta2 mean.

Do not use held-out statistics for parameter choice.

## Falsification

A1 fails if it cannot bring entry projection, local-family activation and line-position grammar into the same broad regime on held-out leaves without another mechanism.

A1 survives only as a structural generator if the joint fit improves materially. It does not gain semantic plausibility from fitting.

## Complexity accounting

Relative to A0, A1 pays one additional global mechanism plus one fitted scalar (`local_family_p`). Entry strength remains an A0 parameter.
