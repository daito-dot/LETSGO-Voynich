# Meta-analysis of the research trajectory

This document analyzes the research process itself rather than any single Voynich hypothesis.

## 1. The project changed from decipherment hunting to constraint discovery

Early work repeatedly asked whether a visually or statistically interesting pattern supported a direct reading, cipher relation, periodic system, copy mechanism, or other concrete explanation. Stronger controls progressively weakened many of those interpretations.

The project now operates more like a constraint-discovery program:

- identify a reproducible structural effect;
- build stronger nulls and matched controls;
- determine which part of the effect survives;
- test whether a candidate mechanism reproduces several surviving constraints simultaneously;
- retain failed mechanisms and corrections in the hypothesis ledger.

This is a better fit for Voynich research because highly flexible mappings can make many apparent readings look plausible.

## 2. The most informative results have usually been residuals after controls

A recurring pattern is that the first headline statistic is not the durable result.

Examples:

- edit-distance-1 family density looked highly unusual, but constructed languages and abbreviated medieval manuscripts can also produce high raw density;
- after token-length / inventory controls, a substantial Voynich excess remains;
- short-range continuity looked like a possible Voynich generator signature, but medieval Latin prose reproduces it readily;
- paragraph-boundary discontinuity survived as the more discriminating residual;
- the original Phase54 paragraph headline then changed again after page-side auditing and section decomposition.

The useful object of study is therefore not a single high statistic. It is the intersection of constraints that remain after progressively stronger controls.

## 3. Internal data structure was audited too late in several phases

The clearest example is the Phase53/54 parser collapsing `f1r` and `f1v` to the common physical-leaf id `f1`. The paragraph-entry effect survived correction, but its magnitude changed and the effect proved section-dependent.

The methodological lesson is explicit:

> manuscript units and metadata should be mapped before mechanism fitting.

Future analyses must declare the unit of observation separately for physical leaf, page-side, section, paragraph, line, and token. A statistically interesting result is provisional until its unit definition has been audited.

## 4. Single-feature explanations have repeatedly failed

Several candidate mechanisms reproduced one or two properties and then failed elsewhere:

- literal copy-and-modify: good predictive code length, weak directional evidence;
- simple finite-state DSL: reproduced near-family density and locality, failed line and paragraph structure;
- line-conditioned morphology: reproduced line-position grammar cheaply, did not explain paragraph structure;
- paragraph active-family/topic mechanisms: produced boundary reset only by overproducing generic local clustering;
- paragraph surface/alphabet state: damaged the near-family topology while still underproducing the desired reset.

This suggests that the manuscript should be represented by a multivariate structural fingerprint rather than a sequence of one-statistic challenges.

Current recurring dimensions include:

- token-internal morphology / positional constraints;
- near-family network density after matched nulls;
- modest generic short-range clustering;
- line-position grammar;
- broad section/document-role differences;
- physical-order / leaf-local drift;
- section-dependent paragraph-entry dynamics;
- known structural-equivalence candidates such as `{k,t}`.

Any mechanism should be evaluated on the joint fingerprint and charged for added degrees of freedom.

## 5. The important contrast is increasingly hierarchy and dynamics, not linear versus nonlinear classification

Phase55 found that nonlinear ExtraTrees did not materially outperform linear logistic models at the folio-feature scale. At the same time, a strong physical-order signal emerged:

- recto/verso of the same leaf are unusually close;
- adjacent leaves are closer than distant leaves;
- fingerprint distance grows with physical separation.

This points away from a picture dominated by a single complex nonlinear clustering surface. A more economical description is a hierarchy with locally evolving state.

Current descriptive hierarchy:

`manuscript -> section/document role -> locally drifting leaf/page state -> paragraph dynamics -> line-position grammar -> token morphology`

Currier and hand cut across this hierarchy but are heavily confounded with section and with each other in the observed manuscript design.

This hierarchy is a descriptive model, not yet a historical/generative explanation.

## 6. The major explanatory families remain open, but their simple forms have narrowed considerably

The project has not yet separated natural-language, cipher, formal-generation, and mixed explanations decisively.

That is not equivalent to making no progress. The admissible forms of each family are now more constrained.

A plausible explanation must now accommodate, or explain away with matched document controls:

- strong internal token grammar;
- line-position effects;
- section/document-role differences that survive some crossed hand/Currier comparisons;
- physical-order drift below broad section labels;
- unusually dense near-family topology after simple length/inventory controls;
- paragraph-entry effects in several prose-heavy sections, but not as a manuscript-universal rule;
- the failure of simple topic/family concentration as a sufficient paragraph mechanism.

Simple substitution cipher, simple online copying, one stationary paragraph topic, and the frozen simple DSL are not sufficient broad explanations under current tests.

## 7. Negative results are a central product of the project

The ledger contains many `NOT SUPPORTED`, `WEAKENED`, or `FALSIFIED AS SUFFICIENT MECHANISM` entries. This is desirable in a domain where unconstrained explanations are cheap.

Research quality has improved when the project has:

- demoted contaminated held-out evidence rather than preserving a stronger label;
- retained negative semantic matching results;
- compared against matched natural-language and document controls;
- corrected the page-side parser issue and reduced the headline effect rather than defending the old result;
- required bounded deception/cipher freedom instead of treating failed semantic tests as evidence for deliberate deception.

## 8. The next conceptual target should be latent structure before decipherment

A recurring inefficiency has been:

`look for meaning -> discover a structural confound -> model the confound -> look for meaning again`.

A better order is:

`model internal structure -> remove/predict structural variation -> inspect what remains`.

The key meta-question is now:

> How many independent latent axes are required to explain the manuscript's observed variation across physical order, section, paragraph, line, and token morphology?

Several labels currently treated separately may be manifestations of fewer underlying states. Candidate latent dimensions could include:

- document/register/content state;
- physical/scribal drift state;
- local discourse/item-entry state;
- global token-construction grammar.

If a compact latent-state model predicts most of the known structural variation, then the residual becomes a better place to search for information-bearing content or cipher value.

## 9. Recommended methodological shift

Before returning to new generator mechanisms or semantic mappings:

1. build a manuscript-wide multiscale state map using page-side, physical order, section, paragraph, line and token features;
2. distinguish smooth physical drift from discrete changepoints;
3. estimate the minimum latent dimensionality needed to predict held-out structural features;
4. test whether the same latent coordinates transfer across sections or whether separate local grammars are required;
5. only then define residuals and test whether those residuals correlate with independently grounded content, illustrations, labels, or candidate plaintext structure.

The goal is not to force all Voynich variation into one latent model. The model is useful if it identifies what is predictable from document structure and what remains unexplained.

## 10. Current meta-level conclusion

The project has moved farther from unconstrained 'readings' and closer to a falsifiable structural model of the manuscript.

The strongest current progress is not a decipherment. It is a narrowing of the search space and a clearer distinction between:

- structure that ordinary text/manuscript practice can reproduce;
- structure that simple formal generators can reproduce;
- structure that survives matched controls;
- structure that depends on section or physical state;
- residual variation that has not yet been assigned to meaning, cipher state, or generation mechanism.

The most productive next step is therefore to estimate the manuscript's latent multiscale state structure before adding another mechanism-specific model.
