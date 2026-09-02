# OGH-A — minimal occupancy-generation rule for the replicated R1 topology

Status: **PREREGISTERED — NO OGH TARGET RESULT REVEALED**

Lane: token-construction program, post Issue #72.

Parent authority:

- `research/HYPOTHESIS_LEDGER_ADDENDUM_ISSUE72_RESULT.md`, section "New falsifiable frontier";
- Issue #68 R1 scorer `experiments/joint-constraint-tournament/target68.py` (frozen gates reused unchanged);
- #58C / #58D frozen ZL3b and IT2a pooled residual vectors (the R1 target readings).

This plan is committed **before** any executable that generates an OGH candidate corpus or computes any OGH candidate R1 pair-Q, residual energy, or topology statistic.

## 1. Scientific question

Issue #72 localized Naibbe's R1 success to the **corpus-level distribution of 12-slot occupied/empty token signatures**: state-dependent emission (EL/ES/EG) matters, exact plaintext order (PT) does not, and final placement of already-produced signatures (FI-M/FI-G) does not.

The next question is therefore not about Naibbe. It is about the target object itself:

> **What is the minimal rule over 12-slot occupancy signatures that, sampled independently token by token into the manuscript's own line skeleton, reproduces the replicated complete-66 R1 residual topology?**

A secondary, representation-critical sub-question is embedded in the hierarchy:

> **How much of R1 is already implied by the frozen `SlotParser(min)` grammar itself, i.e. by which occupancy signatures the parser can emit at all?**

## 2. Why this is the right next step

- If a near-parameter-free rule reproduces R1, then R1 is far less mechanism-specific than currently assumed and must be downgraded as a discriminator among candidate mechanisms.
- If only a compact state-dependent construction grammar reproduces R1, then R1 identifies a **generator class**, and later inverse models must belong to it.
- If only empirical signature resampling reproduces R1, R1 remains a strong descriptive constraint without a compact generative explanation yet.
- If even resampling fails, then within-line or sequential dependence contributes to R1, contradicting the Issue #72 FI picture for the manuscript itself.

Every branch is informative and none requires touching Naibbe, A1, R2, R3 or R4.

## 3. Frozen representation and target

- Parser: unchanged 12-slot `SlotParser`, policy `min`, from `experiments/issue26-music/issue26e_core.py`.
- Base statistic: `K_other`-conditional Jeffreys-smoothed Mantel-Haenszel Yule Q on all `C(12,2)=66` unordered slot pairs (`phase58b_graph_stability.pair_codes / q_cond`).
- Residualization: candidate-owned 1,000 reference line-local slot-occupancy shuffle nulls, edge-wise empirical mid-rank normal score (`phase58c_residual_graph.normal_score_array`).
- Validation nulls: independent 1,000 candidate-owned test nulls, disjoint seed namespace.
- Target readings: frozen #58C ZL3b `real.z_full.ALL` (raw SHA-256 `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`) and frozen #58D IT2a `real_IT2a.z_full.ALL` (raw SHA-256 `f26db8123f8f2b7a4148495fdeebe81c8c042a23606eb7c22e1c0687faaf86a6`). Cross-check `r=0.9884483852763541`, signs `65/66` must hold before scoring.
- No selected edge is used anywhere in fitting, generation, or decision.

## 4. Candidate corpus construction (common to all models)

A candidate corpus is a matrix of 12-bit occupancy rows placed into a **frozen line skeleton**:

- primary skeleton: the ZL3b #58C population (`build_dataset(ZL3b, min)`): 4,082 lines with at least one accepted token, 25,071 accepted tokens, 5 physical-leaf folds, frozen line order;
- replication skeleton: the IT2a #58D population (`build_it_dataset(IT2a, ZL3b, min)`): 28,280 accepted tokens, same 5 physical-leaf folds.

The skeleton supplies only **layout**: number of accepted tokens per line, line order, fold label. It supplies no occupancy information to the generator. Line-position and Currier/section labels are not used.

Each model is expressed as an explicit probability vector over the `2^12 - 1 = 4095` non-empty signatures. For each held-out fold `f ∈ {0..4}`:

1. fit the model **only** on accepted-token signatures from the other four folds of the same source;
2. sample one signature per skeleton token of fold `f` i.i.d. from the fitted vector with `numpy.random.default_rng(stable_seed("OGH-A:{source}:{model}:fold{f}:rep{rep}"))`.

The pooled corpus is the concatenation of the five held-out-fold generations. No token is generated from parameters fitted on its own leaf.

Replicates: `rep ∈ {0,1,2}`. **`rep=0` is the primary realization** for every model. `rep=1,2` are non-promoting stochastic sensitivities and may not be selected among.

## 5. Frozen model hierarchy

Let `A ⊂ {1..4095}` be the set of signatures that `SlotParser(min)` can emit for at least one string (enumerated exhaustively over all value assignments; a representation property, computed before any target score and recorded in the preflight). Let `n(x)` be the training count of signature `x`.

| ID | Model | Probability vector | Free parameters | Role |
|---|---|---|---|---|
| G0 | independent slot Bernoulli | `∏_s p_s^{x_s}(1-p_s)^{1-x_s}` over all 4095 non-empty signatures, `p_s` = training slot marginal | 12 | negative calibration anchor |
| G1 | admissible uniform | `1[x∈A] / |A|` | 0 | representation-only control |
| G2 | admissible maxent, slot marginals | `1[x∈A] exp(Σ_s θ_s x_s) / Z` with `θ` fitted so model slot marginals equal training marginals | 12 | lower-order |
| G3 | admissible maxent, slot marginals + occupancy count | `1[x∈A] exp(Σ_s θ_s x_s + λ_{|x|}) / Z`, matching marginals and the distribution of `|x|` | 12 + 11 | lower-order + shape size |
| G4 | admissible left-to-right last-occupied construction grammar | `1[x∈A] ∏_{s=0}^{11} P(x_s | ℓ_s) / Z`, where `ℓ_s ∈ {none,0,…,s-1}` is the most recent occupied slot before `s`; conditionals estimated by add-½ counts | 78 | compact state-dependent construction grammar |
| G5 | admissible pairwise maxent | `1[x∈A] exp(Σ_s θ_s x_s + Σ_{s<t} J_st x_s x_t) / Z`, matching all first and second moments | 12 + 66 | pairwise-moment sufficiency control, **non-promoting** |
| G6 | empirical signature resampling | `(n(x) + 0) / N` on training signatures | ≤ number of observed signatures | positive sufficiency ceiling, **non-promoting** |

Nesting: G1 ⊂ G2 ⊂ G3 ⊂ G5 as exponential families on `A`; G4 is a distinct compact generator class; G6 is saturated.

Fitting is exact by enumeration over `A` (convex maximum likelihood for G2/G3/G5, closed form for G0/G1/G4/G6). For each model and fold, record training and held-out mean log-likelihood per token (natural log) as the complexity/predictive-fit accounting.

Any fitted maxent must reach its moment constraints to within `1e-6` (max absolute moment error); otherwise the model is reported `FIT_FAILED` and receives no R1 score.

## 6. Frozen R1 scoring — identical to Issue #68

For each `(source, model, rep)` corpus:

- reference null namespace `OGH-A:{source}:{model}:rep{rep}:reference-null`, `n=0..999`;
- test null namespace `OGH-A:{source}:{model}:rep{rep}:test-null`, `n=0..999`;
- null operation: within every line and every slot independently, permute occupancy values across that line's tokens (`phase58c_residual_graph.shuffled_flat`), preserving every line × slot occupied count;
- real residual `z` (66), residual energy `E = sqrt(mean z²)`;
- reliability `W`: median over the five folds of Pearson(train-fold residual, held-fold residual) using the same reference calibration per view;
- `p_exist`: upper empirical p of `E` within the 1,000 test-null energies;
- topology per target reading `T ∈ {ZL3b, IT2a}`: Pearson `r_T`, sign agreement `a_T/66`, `p_r,maxT` and `p_a,maxT` from the test-null maxima over the two readings.

**R1 pass** (unchanged from `target68.topology_result` / `main`):

- existence: `valid_folds ≥ 4`, `W ≥ 0.50`, `p_exist ≤ 0.01`;
- and for **both** readings: `r_T ≥ 0.70`, `p_r,maxT ≤ 0.01`, `a_T ≥ 50`, `p_a,maxT ≤ 0.01`.

Primary statistic for the hierarchy decision is the `rep=0` pass/fail of each model on the ZL3b skeleton. The IT2a-skeleton arm is a replication arm and is reported in full; a hierarchy verdict is called **replicated** only if the same model classes pass/fail on both arms.

## 7. Frozen hierarchy classification

Evaluated on `rep=0`, primary arm, in this order:

1. `REPRESENTATION-ADMISSIBILITY DOMINANT` — G1 passes R1.
2. `LOWER-ORDER SUFFICIENT` — G1 fails; G2 or G3 passes.
3. `COMPACT CONSTRUCTION GRAMMAR SUFFICIENT` — G1, G2, G3 fail; G4 passes.
4. `PAIRWISE-MOMENT SUFFICIENT ONLY` — G1–G4 fail; G5 passes.
5. `INVENTORY-ONLY SUFFICIENT` — G1–G5 fail; G6 passes.
6. `NO TESTED TOKEN-IID MODEL SUFFICIENT` — G6 fails.

Additional frozen expectations that act as scorer sanity gates (not hypotheses):

- G0 must **fail** R1 with `E` inside the test-null range; if G0 passes, the scorer or the null is broken and the reveal is `INVALID`.
- G6 on the ZL3b skeleton resamples the target's own training-fold inventory; its outcome is a ceiling, not evidence for any mechanism.

Graded distances (`r_T`, `a_T`, `E`, held-out log-likelihood) are reported for all models to show how the topology accrues along the ladder, but they do not alter the class labels.

## 8. What each outcome changes

- Class 1 or 2: R1 is largely a property of the parser grammar plus first-order occupancy statistics. R1 must be downgraded from "mechanism-specific construction grammar" to "representation + inventory constraint"; future tournaments should weight R2/R3/R4 and a coarser representation-independent token object more heavily.
- Class 3: a compact left-to-right construction grammar suffices. This defines the generator class future reversible mechanisms must emulate, and G4's conditionals become a frozen descriptive target for follow-up.
- Class 4: R1 is second-order-sufficient but not compactly generated; it constrains pairwise moments only.
- Class 5: no compact generative rule found; R1 remains a descriptive inventory constraint.
- Class 6: within-line/sequential dependence is part of R1 for the manuscript; reopen the FI-analog question for Voynich itself under a new plan.

None of these outcomes bears on plaintext, semantics, historical Naibbe use, or decipherment.

## 9. Prohibited after reveal

- adding, removing or re-parameterizing any G-model;
- changing thresholds, seeds, namespaces, `N_REF`, `N_TEST`, or the skeleton;
- selecting among replicates;
- promoting G5 or G6 as mechanisms;
- using individual edge residuals to design the next model in the same phase;
- interpreting any pass as evidence about meaning.

## 10. Execution and provenance

The executable will emit one JSON per `(source, model, rep)` plus an aggregate JSON with SHA-256 sums. The first execution of the aggregate is the first reveal, wherever it runs; environment, interpreter and library versions are recorded. A GitHub Actions replay workflow is provided for exact re-execution from the frozen head.

Sources are third-party transcriptions obtained from `voynich.nu` and verified by hash (`ZL3b-n.txt` Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`; `IT2a-n.txt` SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`). They are not redistributed.
