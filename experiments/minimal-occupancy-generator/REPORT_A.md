# Issue #75 Phase A — minimal low-order occupancy generator result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Primary question

Phase A asked:

> Are the replicated 66 residual slot-occupancy relationships recoverable from only the 12 slot marginals, or from those marginals plus the distribution of the number of occupied slots per token?

The answer is **no** under the preregistered cross-fitted test.

The empirical occupancy-pattern inventory positive control succeeds strongly, while both lower-order models fail by a very large margin.

Frozen ordered classification:

`LOW_ORDER_MODELS_INSUFFICIENT_EMPIRICAL_PATTERN_STRUCTURE_REQUIRED`

## Representation

The scientific object is the frozen 12-slot binary representation of parser-accepted Voynich tokens:

`x in {0,1}^12`

R1 is the complete 66-edge null-residual dependency topology over the `C(12,2)=66` unordered slot pairs.

This phase does not compare literal token strings or glyph identities.

## Preregistered model hierarchy

### M0 — slot main effects only

A non-empty maximum-entropy model over all 4095 possible non-empty occupancy signatures, fitted from training folds to reproduce only the 12 individual slot occupancy rates.

No pair interactions. No occupancy-count distribution supplied.

### M1 — slot main effects + occupied-slot count K

Adds the exact training-only distribution of

`K = number of occupied slots in a token`

and samples conditional on K using only slot main effects.

No pair interactions and no empirical occupancy-pattern inventory.

### MPLUS-A / MPLUS-B — empirical-signature resampling controls

Two independent cross-fitted positive-control banks sampling complete 12-bit occupancy signatures from training folds.

These are sufficiency controls, not mechanistic explanations.

## Frozen experimental authority

Normative plan:

- `PLAN_A.md`
- commit `8d984cfa61a5616bef61b45248c0a7a5d213fbf8`

Stage A0 target-blind generation authority:

- 124/124 corpora frozen before target access
- permanent commit `c703b2d01c941b6bfd17758f09868c71a200f212`
- authority SHA-256 `83e5808576a6416e4b03e302242805509c05d16928403d3a58e5636bdbf9ecd2`
- no drops / no rerolls

Pretarget exact-replay preflight:

- run `33501747280` — success
- head `698e7ee5503bc7e47d183deb7d8cc09d89502216`

Pretarget full candidate-null smoke:

- run `33501857058` — success
- head `b4a723c204996764a64ac53121156cc194461c98`
- each family completed 66 Q values, 1000 reference nulls, residual Z, fold reliability and 1000 test nulls without target access

First reveal:

- scientific head `785bd9f04afceadf4072ea576812649554ad6c6e`
- workflow run `33502168755` — success
- population `124/124 = 31 × (M0, M1, MPLUS-A, MPLUS-B)`
- drops `0`
- rerolls `0`
- final artifact ID `9798525603`
- artifact digest `sha256:548da64c4b3c759e5137387b3bd1dc1335d098b7c0799b06283a75535eda4612`
- aggregate SHA-256 `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

Permanent post-reveal transport-only freeze:

- run `33503313661` — success
- permanent authority commit `5059eaf60d5725e65895c8c0fac8dfe859151cf7`
- directory `experiments/minimal-occupancy-generator/stage-a-first-reveal/`

## Positive-control calibration

The preregistered control floor was the lower frozen within-reading residual reliability:

`T_control_floor = 0.9447148364`

Observed median conservative topology score `T=min(R_ZL3b,R_IT2a)`:

| family | median T |
|---|---:|
| MPLUS-A | `0.9643123239` |
| MPLUS-B | `0.9655940680` |

Both exceed the control floor. Therefore the evaluation interface is calibrated and lower-order conclusions are licensed.

The two independent M+ banks differ only slightly:

- q95 positive-control self-difference `delta_plus = 0.0097683130`

This is the frozen equivalence tolerance for M0/M1.

## Primary result

| family | median T | median R ZL3b | median R IT2a | median residual E | median W | median p_exist |
|---|---:|---:|---:|---:|---:|---:|
| M0 | `-0.110091` | `-0.106195` | `-0.106538` | `1.195170` | `0.011352` | `0.015984` |
| M1 | `-0.167412` | `-0.167412` | `-0.155270` | `3.251186` | `0.323847` | `0.000999` |
| MPLUS-A | `0.964312` | `0.967040` | `0.964312` | `3.248136` | `0.986790` | `0.000999` |
| MPLUS-B | `0.965594` | `0.968486` | `0.965594` | `3.254354` | `0.985757` | `0.000999` |

Paired median topology gaps against the two-bank M+ center:

- `gap_M0 = -1.0779969902`
- `gap_M1 = -1.1307973706`

Both are enormously more negative than the permitted stochastic tolerance:

- `delta_plus = 0.0097683130`

Therefore:

- M0 no-material-loss: **false**
- M1 no-material-loss: **false**

The same classification remains under non-promoting q90 and q99 tolerance sensitivity.

## What M0 tells us

M0 generates each slot from training-only slot prevalence, subject only to the logical constraint that a token is not completely empty.

It fails badly:

- topology is approximately uncorrelated to mildly anticorrelated with Voynich;
- median `T=-0.110`;
- fold reliability is essentially zero (`W≈0.011`).

Thus the replicated R1 topology is not an artifact of individual slot frequencies plus the non-empty-token constraint.

This strengthens the older #58C residual result by showing the same point generatively rather than only through residualization.

## What M1 tells us

M1 is more informative and more surprising.

It is given:

- the training-only 12 slot main effects; and
- the exact training-only distribution of how many slots a token occupies.

This produces a **strong residual object**:

- median `E=3.251`, essentially the same magnitude as M+ (`≈3.25`);
- `p_exist=0.000999` for all 31 realizations;
- positive but moderate fold reliability (`median W=0.324`).

Yet its topology is wrong:

- median ZL3b `R=-0.167`;
- median IT2a `R=-0.155`;
- conservative median `T=-0.167`;
- sign agreement is fixed near only `38/66` for ZL3b and `37/66` for IT2a.

This is an important distinction:

> **Controlling token occupancy count is sufficient to create strong non-random slot dependencies, but it creates the wrong dependency geometry.**

In other words, the existence of a structured graph is not enough. Voynich requires a specific rule selecting *which slots occur together*.

## What M+ tells us

Cross-fitted empirical occupancy-signature resampling succeeds strongly against both independent readings:

- median R around `0.967–0.968` for ZL3b;
- median R around `0.964–0.966` for IT2a;
- sign agreement typically `64/66` ZL3b and `65/66` IT2a;
- W around `0.986`.

Because each held-out fold is generated only from the other four folds, this is not simply replaying the held-out tokens themselves.

It demonstrates that the **training occupancy-pattern inventory generalizes across physical leaves and retains the independently replicated graph**.

It remains a positive control rather than an explanation because the complete empirical signatures are supplied directly.

## Mechanistic interpretation

Phase A rules out two simple explanations:

1. “some slots are just common and others rare”;
2. “tokens simply regulate how many structural slots they use.”

Neither explains R1.

The missing information lies in the arrangement of occupancy inside a token:

> **given that a token uses K slots, the identity/configuration of the occupied slots is strongly constrained.**

A useful decomposition is now:

`individual slot propensity`  — insufficient

`+ number of occupied slots K` — creates strong structure, but wrong structure

`+ specific within-token configuration rule` — required frontier

`empirical full signature inventory` — sufficient positive control

So the research target has narrowed from “how are Voynich words built?” to a more precise question:

> **What compact rule determines which subsets of the 12 structural positions are allowed/preferred together?**

## Relationship to Issue #72

#72 showed that:

- state-dependent emission can strongly alter R1 upstream;
- exact local plaintext order is not a detected R1 necessity;
- final placement of completed occupancy patterns across the corpus is not a detected R1 necessity.

Phase A adds:

- marginal slot propensity is not enough;
- occupied-slot count is not enough;
- the empirical within-token occupancy configuration inventory is enough.

Thus the current localization is now sharper:

`upstream generator`

`    ↓`

`selection of specific 12-slot occupancy configurations  <-- required R1 information`

`    ↓`

`corpus inventory of those configurations`

`    ↓`

`placement across lines/manuscripts                      <-- no detected extra R1 information`

## Licensed next step

The preregistered outcome map explicitly licenses M2/M3 only in the observed case:

- M0 fails;
- M1 fails;
- M+ succeeds.

Therefore the next phase may search for a compact within-token configuration rule between M1 and empirical-signature resampling.

It must not fit the 66 target edges directly.

The next models should be chosen by generic occupancy-shape structure, prospectively, for example:

- coarse geometric/pattern descriptors of a 12-bit signature;
- a small latent or state-transition construction grammar;
- training-only selection/parameterization with held-out physical leaves and IT2a retained as target validation.

The scientific objective is not simply to improve fit. It is to find the **minimum interpretable rule that replaces empirical pattern memorization**.

## Boundaries

Phase A does not establish:

- literal token spelling rules;
- meanings for the 12 slots;
- plaintext letters;
- a cipher table;
- natural-language word boundaries;
- historical Naibbe use;
- Latin plaintext;
- decipherment.

It establishes that the replicated R1 constraint contains genuine within-token **configuration information** beyond slot marginals and occupancy count.
