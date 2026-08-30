# Phase 61 — joint architecture discriminator

## Purpose

Phase60 leaves two broad mechanism families alive:

- **A — boundary-aware nonsemantic generator:** a formal generator may remain viable, but it must know or infer document boundaries and reproduce the manuscript-wide entry register in addition to ordinary local token-family structure.
- **B — structured meaningful plaintext + global encoding:** medieval plaintext can already carry entry/register structure, so a position-independent cipher can inherit it. Ciphering becomes explanatory only if it also accounts for Voynich-specific morphology/local family structure rather than merely preserving plaintext paragraphing.

Phase61 compares these as architectures, not as stories.

## Frozen joint target vector

No model is judged on one statistic alone. It must jointly address:

1. **entry specificity** — real paragraph entry transition exceeds internal pseudo-boundaries;
2. **entry direction** — generated/encoded entry transition aligns with the frozen Voynich structural direction;
3. **near-family density** — unusually high edit-distance-1 family density;
4. **local family activation** — near-family/local-prev10 excess is locally concentrated;
5. **line-position grammar** — token/form distributions depend on line position beyond simple line length;
6. **section modulation** — major H/B/P/S/T sections differ while sharing an entry role;
7. **short entry memory** — line0 does not add prospective prediction of later absolute state after immediate prior state is known.

A candidate that improves one target by breaking another is not sufficient.

## Model A0 — boundary-aware nonsemantic generator

Start from the frozen Phase50/51 token-family DSL. Add exactly one new mechanism before seeing Phase61 outcomes:

- at paragraph line0 only, draw from a separate **entry mixture** over the same root/family inventory;
- line1 onward returns immediately to the ordinary body generator;
- no persistent paragraph latent state is allowed, matching Phase60E memory-horizon evidence;
- entry mixture complexity is bounded to a small number of global parameters and is shared across sections; section modulation may alter mixture weights but not invent separate grammars.

### Falsification

A0 is weakened if a low-complexity entry mixture cannot jointly reach the Voynich entry direction and near-family/local/line-position constraints without large retuning or section-specific exceptions.

## Model B0 — structured plaintext + global encoding

Use independently selected medieval structured-document controls with source-native item/paragraph boundaries. Apply only global, boundary-blind transforms:

- monoalphabetic symbol substitution;
- fixed homophonic substitution;
- fixed token/codeword mapping or similarly bounded morphographic recoding.

No transform may inspect paragraph position, Voynich section label, or the Voynich target vector.

### Falsification

B0 is weakened if the plaintext+encoding family preserves entry grammar but repeatedly fails to generate the Voynich-specific near-family/local/line-position combination under fixed low-complexity transforms.

## Evaluation

Primary comparison is Pareto/joint fit, not a single weighted score. Report every target separately and flag which constraints each architecture satisfies, misses, or can satisfy only by explicit additional machinery.

Complexity accounting is mandatory. Every added boundary condition, state variable, section-specific parameter or codebook degree of freedom is counted as explanatory cost.

## Anti-rescue rule

After results are observed, do not add a new mechanism merely to repair one failed target. Any extension becomes a separately named A1/B1 hypothesis with its own frozen prediction and complexity increment.

## Phase61A first executable test

Construct A0 on the local Voynich layout and ask the narrow first question:

> Can a single global entry mixture, with no persistent entry state, reproduce the frozen Voynich real-entry-minus-pseudo direction while retaining the frozen body generator?

Sweep only entry-mixture strength on a preregistered coarse grid. The mixture direction itself must be learned from training physical leaves and evaluated on held-out leaves; it may not use held-out entry statistics.

If even this narrow cross-fitted test fails, A0 is rejected before broader joint fitting.
