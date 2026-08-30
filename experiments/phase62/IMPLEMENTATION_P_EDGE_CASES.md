# Phase62P H62-P1 — frozen edge-case rule

Status: committed before the H62-P1 executable and before any H62-P1 value is evaluated.

`IMPLEMENTATION_P.md` requires all five distance bins. To prevent post-result handling choices:

- every primary profile entity used for a scientific comparison must have at least one eligible token occurrence in **every** B1–B5 bin;
- for N0/C0 this applies to each of the four primary manuscripts before equal-manuscript E-vector aggregation;
- for held-out Voynich this applies to every outer fold;
- for A1 this applies to every generated realization used in the fold average;
- if any required entity has zero eligible observations in any bin, the executable emits **no H62-P1 scientific verdict** and reports the missing entity/bin;
- no manuscript, fold, replicate, or bin may be dropped after inspection to rescue the analysis.

This conservative failure rule is preferred to inventing a missing-value imputation after seeing the prospective result.