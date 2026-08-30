# Phase 50 — formal systems and finite-state DSL

## Question

Can strongly structured formal/programming systems explain Voynich near-neighbor token topology without invoking natural-language morphology or cipher behavior?

## Controls

Exploratory controls included Lisp-like, Prolog-like and regex-like formal syntax plus real local SQL, XML and TeX source material.

On the matched 141-token word-like-lexeme metric, conventional formal/programming sources remained far below the Voynich edit1-family density reference.

## Finite-state DSL demonstration

A synthetic DSL used:

- finite root families
- one-character root variants
- optional prefix/suffix slots
- block-local latent state

The initial model could generate **too much** near-neighbor structure. Varying block length showed that global near-neighbor density and short-range locality are separable: local-state persistence strongly controls locality.

An exploratory post-target grid found a 64-root, block-length-4, state-use-probability-0.30 configuration giving roughly:

- edit1 density: `0.7315`
- local excess: `0.0381`

against then-used Voynich references near:

- edit1 density: `0.7573`
- local excess: `0.0313`

This configuration was selected after seeing the targets. It is therefore a **mechanism demonstration only**, not validation or evidence of historical truth.

## Interpretation

Ordinary formal/programming text alone does not explain the observed topology. But a meaning-light finite-state morphology plus weak local state can reproduce the two selected statistics.

The correct next test was therefore to freeze the model and attack unused dimensions rather than add more features. Phase51 performed that falsification and showed that the frozen DSL fails strongly on paragraph reset and line-position grammar.
