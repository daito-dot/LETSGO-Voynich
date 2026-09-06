# Issue #134 — augmented observable-core residual closure

Status: **FROZEN BEFORE NEW RESIDUAL SCORING**

Parent: Issue #88. Entry authority: Issue #134.

This plan freezes the final observable-core closure test before any new residual likelihood is inspected. It does not fit a latent state and does not change token segmentation.

## 1. Frozen source, order, population and folds

- Source: ZL3b `ZL3b-n.txt` from `matthewdgreen/cipher_benchmark` commit `315f0cad4de3d021bd4185765c037cf2a28d341c`.
- Expected source git blob SHA-1: `2a4533ab9bdfa85db9bad602d590978953055df1`.
- Expected source SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`.
- Corrected source order: `experiments/predictive-information/source_order_authority.py` exactly as merged after Issue #98.
- Outer CV: the original five physical-leaf folds. No new split is created.
- Scientific targets: exactly the parser-accepted token positions used by corrected Phase-1 B3.
- All visible source tokens remain available as training history where the frozen predecessor models used them.

Before any new residual score is valid, corrected B3 must reproduce the normalized authority SHA-256
`0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`
and every outer-fold B3 score/target count must match that authority to `1e-12` where numerical comparison applies.

## 2. Augmented observable expert

The observable expert is the Issue #125 explicit `k=2` onset factorization with one prospectively frozen Currier policy.

Fixed representation:

- literal UTF-8 token bytes plus `END_TOKEN`;
- `k = 2`;
- additive `alpha = 0.01` over byte vocabulary size `257`;
- source-line boundaries are hard resets;
- no cross-line terminal→initial edge;
- line-start first-symbol distribution pooled over all training items;
- line-body first-symbol position-only distribution pooled over all training items;
- line-start and line-body second-symbol distributions pooled over all training items and conditioned on current first symbol;
- third and later emitted symbols use the ordinary pooled within-token `k=2` table, exactly as Issue #125.

Only the first symbol of a non-line-start token receives Currier-conditioned terminal identity.

### Currier table policy

Currier labels come only from the already-audited Phase 3A/ZL3b header authority.

For a non-line-start target with previous terminal class `c`:

1. if target Currier is `A` or `B` and that same regime has training support for `c`, use that regime's `P(first | previous_terminal=c)` table;
2. otherwise, if the pooled training population has support for `c`, use the pooled `P(first | previous_terminal=c)` table;
3. otherwise use the pooled line-body first-symbol distribution.

For unknown/other Currier targets, start at rule 2. No writing-hand conditioning is allowed.

All three cases use the same fixed additive smoothing. The fallback hierarchy is frozen now and may not be changed after residual reveal.

## 3. Composition with corrected B3

Let `p_B3(t)` be the corrected B3 target probability and `p_edge(t)` the Currier-policy explicit observable expert probability.

The augmented core is

`p_aug(t; rho) = (1-rho) p_B3(t) + rho p_edge(t)`.

Grid: `rho = 0.00, 0.01, ..., 1.00`.

For each outer fold, `rho` is selected by pooled accepted-token likelihood across the four inner validation folds, with both outer and current inner fold excluded from fitting. Ties go to smaller `rho`. The selected `rho` is then frozen before the untouched outer fold is scored.

No challenger likelihood participates in `rho` selection.

## 4. Frozen flexible residual challenger

The challenger retains the established Phase-1 byte n-gram family but is restricted to the source-line topology localized by Issue #123.

Two matched families are required:

- `RESET`: history resets before every visible-space token;
- `LINE`: history resets at each source line and otherwise carries across visible-space token boundaries within that line.

Both use literal UTF-8 bytes plus `END_TOKEN` and the same candidate grid:

- `k in {0,1,2,3,4,5,6}`;
- `alpha in {0.01,0.10,1.0}`.

For each outer fold and family, `(k, alpha)` is selected by pooled inner accepted-token likelihood of the raw byte expert only. Ties: smaller `k`, then larger `alpha`.

After `rho`, `k` and `alpha` are frozen, each family is mixed independently with the same augmented core:

`p_final_family(t; w) = (1-w) p_aug(t) + w p_family(t)`

with `w = 0.00, 0.01, ..., 1.00`, selected by pooled inner accepted-token likelihood. Ties go to smaller `w`.

The two families may select different `(k, alpha, w)`, as in Issue #118. They may not select different augmented-core `rho`.

## 5. Primary quantity and frozen decision rule

For each outer fold:

`G_residual = bits(MIX_RESET) - bits(MIX_LINE)`.

Positive values mean source-line cross-token byte context adds predictive information after the explicit observable edge is already in the core.

Frozen stability rule:

- mean `G_residual > 0`; and
- `G_residual > 0` in at least `4/5` untouched outer folds.

Classification is exactly one of:

1. `ROBUST RESIDUAL REMAINS BEYOND AUGMENTED OBSERVABLE CORE` if the rule passes;
2. `NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE` if the rule fails;
3. `INVALID CORE / SUPPORT REGRESSION` if any frozen authority, fold, support, finite-probability or implementation invariant fails.

No effect-size threshold, subgroup rescue or fourth class may be added after reveal.

## 6. Score-free Gate before scorer creation

The Gate must run before a new residual scorer is added. It may reproduce already-known B3/Currier authorities, but it must not calculate a new Issue #134 edge likelihood, challenger likelihood, residual gain or classification.

For every outer training population and every outer+inner training population it must verify:

- physical-leaf train/eval disjointness;
- corrected B3 authority/fold identity;
- audited Currier metadata authority;
- non-empty pooled line-start and line-body support;
- non-empty A and B line-body edge support;
- at least two previous-terminal classes in A, B and pooled training support;
- deterministic construction of the A/B/pooled fallback hierarchy;
- the untouched evaluation target population is non-empty;
- outer evaluation parser-accepted counts equal corrected B3 authority counts.

Gate output may expose support counts, Currier labels, fold identities and outcome-blind event-support digests. It must not expose first-symbol outcome distributions or probabilities.

## 7. Reveal discipline

The predictive scorer and its workflow are added only after the score-free Gate has passed from a committed revision. The scorer must be committed before its first outer-fold run.

After the first successful reveal:

- do not tune Currier policy, smoothing, fallback, grids, tie rules, challenger topology or pass rule;
- a substantive bug requires a named correction issue and a newly frozen preregistration before rerun;
- diagnostic strata are descriptive only and cannot change the class.

## 8. Firewall

Forbidden in Issue #134:

- hidden/latent states;
- writing-hand repair;
- target-aware Currier/table selection;
- S1/S2/H62/R1 tuning;
- segmentation changes;
- semantic/image/plaintext/language/cipher/historical-mechanism inference;
- interpreting a flexible predictor as an entropy bound or decipherment.
