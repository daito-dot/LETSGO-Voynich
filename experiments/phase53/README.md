# Phase 53 — minimal hierarchical generator ablation

Status: **development / model selection**. Phase 51/52 targets were already exposed. Nothing in this phase is prospective validation.

## Question

Phase 51 falsified the frozen Phase50 DSL on two unused dimensions: paragraph-boundary near-family reset and line-position grammar. Phase 53 asks whether minimal hierarchical additions repair those failures without destroying the Phase50 successes (high edit-1 family density and modest short-range locality).

Reference targets under the Phase51 preprocessing are approximately:

- paragraph boundary reset: **0.1333**
- line-position MI: **0.1435 bits**
- matched-window edit-1 family density: about **0.77** (window-sampling variation)
- local previous-10 excess: about **0.033**

## M0 — frozen Phase50 DSL

M0 has root families, one-character variants, prefixes/suffixes, and weak token-scale state. It has no knowledge of line or paragraph boundaries.

A representative full-corpus run remains close to the Phase50 density/locality regime but has weak line and paragraph structure.

## M1 — line-position morphology only

Minimal addition: modify only prefix/suffix probabilities at first/middle/last token positions in a line.

A line-strength around 0.4 gives a representative full-corpus result:

- density: 0.703
- local excess: 0.0336
- paragraph reset: 0.0480
- line-position MI: **0.1476**

Interpretation: **line-position grammar is cheap to reproduce**. A small explicit positional morphology mechanism can reach the Voynich line-position MI while leaving local excess near the target. It does not solve paragraph reset.

## M2/M3 mechanism A — paragraph active-root pool

Mechanism: each paragraph samples a restricted subset of active roots; token generation is biased toward that subset. M3 adds the line-position mechanism.

This does create a sharp paragraph reset. One selected M3 development run reached approximately:

- density: 0.788
- local excess: **0.138**
- paragraph reset: 0.173
- line-position MI: 0.221

The problem is not failure to generate reset; it is **over-generation of generic local clustering**. The mechanism makes related families too concentrated everywhere inside the paragraph.

## Mechanism B — compact paragraph surface/alphabet state

Mechanism: root selection remains global, but each paragraph chooses one of a small number of deterministic cyclic surface maps. This tests a compact cipher-like/orthographic state change without narrowing the root pool.

Best tested M3S development setting (K=2, forced state change, line mechanism) gave approximately:

- density: 0.604
- local excess: 0.069
- paragraph reset: 0.075
- line-position MI: 0.227

This mechanism damages near-family density and still does not reproduce the Voynich reset cleanly.

## Mechanism C — paragraph preferred families

Mechanism: every paragraph chooses 1–4 preferred root families, used with a small extra probability. This is a minimal analogue of a topic term, state-dependent codeword family, or latent paragraph theme. M3P adds line-position morphology.

The best four-target development setting found was:

- preferred families: 4
- paragraph bias: 0.30
- line strength: 0.40
- density: **0.733**
- local excess: **0.0603**
- paragraph reset: **0.0903**
- line-position MI: **0.1453**

A weaker paragraph bias (4 families, 0.20) preserves density/locality better (~0.766 / 0.040) but reset falls to ~0.066.

Thus there is a consistent tradeoff: strengthening simple paragraph-local family reuse increases reset only by also increasing ordinary within-paragraph clustering too much.

## Main result

The minimal hierarchy is only partly successful.

1. **Line position is easy:** a small position-conditioned morphology can reproduce line-position MI with little damage elsewhere.
2. **Paragraph reset is not equivalent to ordinary local/topic clustering:** three minimal mechanisms were tried (restricted active pool, surface-state shift, preferred families). None jointly matches the strong boundary discontinuity and the much weaker generic local excess.
3. The best current M3P improves the joint fingerprint substantially but remains under the Voynich reset while roughly doubling local excess.

This suggests that the Voynich paragraph effect is more specific than “same family/topic repeated within a paragraph.” The generator must reorganize relationships at the boundary without simply increasing repeated/nearby use of a small token-family inventory.

## New exposed diagnostic

Phase 53 exposes a useful architecture-selection tension:

> **sharp boundary-specific family change with only modest generic short-range clustering**

This is now a development target and cannot later be used as pristine validation.

## Decision

M0 is insufficient. M1 solves only line position. The tested M2/M3 paragraph mechanisms are insufficient as joint mechanisms.

Do **not** add arbitrary complexity immediately. The next phase should characterize the boundary-specificity constraint more directly and compare it with real structured documents and bounded cipher/generative mechanisms. A successful next paragraph mechanism should produce reset through distributed reconfiguration rather than simple paragraph-local family concentration.
