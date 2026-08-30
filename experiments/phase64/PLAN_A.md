# Phase 64A plan — empirical-inventory autonomy ablation

Status: **FROZEN BEFORE IMPLEMENTATION / RESULT REVEAL**

Hypothesis ID: **P64-A1-R2**

Strategic authority: `DECISION_64.md`

## 1. Question

Phase63A showed that A1-R1 does not need token types unique to held-out leaves. Phase63B showed that the key structure and frozen A1-R1 transfer survive independent transcriptions.

A larger dependence remains:

> A1-R1 still receives the complete empirical token-type inventory from each outer training fold, and its local-family mechanism uses the edit1 graph induced by that observed list.

Phase64A asks:

> **Does the frozen A1 structural advantage survive when the observed training token list is no longer available as the generator's output vocabulary, and is replaced by a low-level training-only morphology generator?**

This is an inventory-autonomy ablation. It is not A2 and does not attempt to repair known A1 residuals.

## 2. Candidate name

The tested candidate is **A1-R2/MG0**.

- **A1**: exact boundary-aware entry + one previous-10 local-family body mechanism.
- **R2**: empirical training token list removed from output candidates.
- **MG0**: a frozen low-complexity character Markov morphology generator learned from distinct outer-training token types only.

A failure falsifies this specific autonomy replacement, not every possible autonomous G model.

## 3. Source arms

Two arms are frozen.

### 3.1 ZL primary arm

Reuse the exact canonical Phase63A/ZL population, physical-leaf folds, held-out targets, S1 training direction/scaling, N0/C0 baselines, Phase61C A1 parameters and five historical generator seeds.

The only causal intervention relative to A1-R1 is:

`empirical outer-training vocabulary -> MG0-generated synthetic vocabulary`

### 3.2 IT independent confirmatory arm

Reuse the exact Phase63B **IT2a W1** population, physical-leaf folds, held-out targets, S1 training direction/scaling, N0/fixed-C0 baselines, Phase61C A1 parameters and five historical generator seeds.

IT W2 is not a Phase64A model-selection path. Phase63B already established W1/W2 observational and A1-R1 stability. Phase64A keeps one predeclared independent arm to minimize new degrees of freedom.

GC is not used for A1-R2 transfer because Phase63B deliberately avoided inventing a v101-to-EVA/shape mapping. GC remains independent-alphabet observational evidence, not a generator-tuning source.

## 4. Information firewall

For source `S`, outer fold `f`, all MG0 learning uses only token strings occurring on `S` training physical leaves.

Held-out token identities may be inspected only for:

- target scoring already required by the held-out evaluation;
- post-generation overlap diagnostics.

They may not influence:

- MG0 order selection;
- transition counts;
- alphabet;
- vocabulary size beyond the training-derived target size;
- sampling/rejection;
- A1 parameters;
- pass/fail thresholds.

The held-out layout still supplies paragraph/line/token counts, exactly as in A1/A1-R1. Phase64A does not claim layout autonomy.

## 5. MG0 morphology model

### 5.1 Training observations

Let `V_train` be the set of distinct token strings on the outer training leaves.

Each distinct type contributes **once**, regardless of token frequency. This matches the A1 body generator's type-uniform candidate vocabulary and prevents high-frequency tokens from becoming an implicit output lexicon.

The outer-training character alphabet is:

`A = sorted(unique characters appearing in V_train)`.

`EOS` is an abstract end-of-token symbol not present in the alphabet. `BOS` is an abstract start context only.

### 5.2 Frozen candidate orders

MG0 chooses one Markov context order from:

`K = {0, 1, 2}`

corresponding to character unigram, previous-one-character and previous-two-character models.

No higher order, template grammar, affix model, edit-family seeding or post-result model is available in Phase64A.

### 5.3 Transition probabilities

For an order `k`, each training type is represented as its character sequence followed by `EOS`, with `k` BOS symbols prepended only as initial context.

Transition probabilities use additive smoothing:

`alpha = 0.5`

across the fixed outer-training symbol set `A + {EOS}`:

`P(x | context) = (count(context,x) + alpha) / (count(context,*) + alpha * (|A| + 1))`.

An unseen context therefore yields the uniform smoothed distribution over `A + {EOS}`.

### 5.4 Training-only order selection

Order selection is nested entirely inside each outer training fold.

Distinct types in `V_train` are deterministically assigned to one of five inner folds by:

`int.from_bytes(SHA256(UTF8(token))[:8], 'big') mod 5`.

For each `k in {0,1,2}`:

1. train MG0 on four inner type folds;
2. score each type in the fifth fold;
3. include EOS probability;
4. compute negative log likelihood per symbol for that type;
5. average the per-type values equally across all inner-held-out types and all five inner folds.

The selected order is the lowest mean inner-CV NLL.

Tie rule: values within `1e-12` are tied; choose the lower order.

The selected order is then refit on all `V_train` types.

**S1/S2/S3/H62-P1 and outer held-out strings are never used to select MG0 order.**

## 6. Synthetic vocabulary sampling

For each source/fold and each of the five A1 generator replicates, MG0 generates one fresh synthetic vocabulary.

### 6.1 Vocabulary size

Required synthetic vocabulary size is exactly:

`|V_synth| = |V_train|`.

This preserves one coarse training-derived diversity budget while removing the empirical membership list.

### 6.2 Fixed morphology seeds

- ZL: `6400000 + fold * 1000 + replicate`
- IT: `7400000 + fold * 1000 + replicate`

These seeds are distinct from the historical A1 layout-generation seeds.

### 6.3 Sequence sampling

Start with the required BOS context. Repeatedly sample from `A + {EOS}` using the fitted MG0 probabilities.

A sampled type is accepted iff:

1. at least one real character occurs before EOS;
2. EOS is emitted at or before real-character length 20;
3. the same string has not already been accepted into the current synthetic vocabulary.

If EOS is not emitted by length 20, reject that sampled type and restart.

Empty strings are rejected.

### 6.4 Critical no-membership rule

**Do not query whether a sampled synthetic type occurs in empirical training or held-out vocabulary when deciding acceptance.**

If MG0 independently regenerates an observed type, it remains valid output. Overlap is measured only after the synthetic vocabulary is complete.

This distinction is central: Phase64A removes explicit vocabulary membership access, not the possibility that a generative model reproduces an observed form.

### 6.5 Uniqueness failure rule

Maximum sampling attempts per synthetic vocabulary:

`200 * |V_train|`.

If exact target vocabulary size cannot be reached within that budget, that source/fold/replicate is a **frozen MG0 instantiation failure**. There is no fallback model, relaxed uniqueness rule or increased budget after observing the failure.

Synthetic vocabulary is sorted before it is passed to A1.

## 7. Exact A1 contract after vocabulary replacement

For each source/fold/replicate:

1. build the edit-distance-1 neighbor graph on `V_synth` using the exact Phase61C `build_neighbors` implementation;
2. learn entry shape scores from the **observed outer-training paragraphs** using the exact Phase61C `learn_shape_scores` function, but evaluate those shape scores on `V_synth`;
3. construct the entry weighted cumulative distribution using the exact frozen Phase61C entry strength for that fold;
4. use the exact frozen Phase61C local-family probability for that fold;
5. use the exact previous-10 direct memory and fallback behavior from `generate_layout`;
6. use the true held-out paragraph/line/token-count layout exactly as A1-R1 did;
7. use the exact historical A1 layout-generation seed:

`6190000 + fold*100000 + int(entry_strength*10)*1000 + int(local_p*100)*10 + replicate`.

No parameter is re-estimated from Phase64A held-out performance.

## 8. Frozen A1 parameters

Per fold:

- fold0: entry strength `0.5`, local-family p `0.20`
- fold1: `0.5`, `0.20`
- fold2: `0.5`, `0.30`
- fold3: `0.5`, `0.30`
- fold4: `0.5`, `0.20`

Any mismatch with committed Phase62/63 authority is a hard execution error.

## 9. Scorecard

Phase64A does not introduce a new success metric.

For each source arm, score A1-R2/MG0 on the same three exposed metrics:

- **S1** paragraph-entry real-minus-pseudo projection;
- **S2** previous-10 near-family locality excess over the frozen layout/vocabulary-preserving null;
- **S3** aggregate line-position eta2 mean.

Also score the same frozen H62-P1 five-bin recurrence geometry:

- `D_profile`;
- absolute `C_short` difference.

H62-P1 bins, 100-null procedure, normalization and diagnostics are unchanged.

## 10. Null/randomness pairing

Where technically compatible, use the same deterministic null labels as the corresponding A1-R1 source arm so stochastic null variation is paired rather than introduced as a new degree of freedom.

### ZL

Use the Phase63A labels:

`A1:fold{f}:rep{r}`

for generated S2/H62 computations.

### IT W1

Use the Phase63B labels:

- S2: `Phase63B:IT2a:W1:A1-S2:fold{f}:rep{r}`
- H62-P1: `Phase63B:IT2a:W1:A1-H62P1:fold{f}:rep{r}`

MG0 randomness is controlled only by the separate Phase64 morphology seeds above.

## 11. Frozen source-arm pass rule

A source arm passes only if **all** of the following hold.

### 11.1 Exposed regime

Across-fold ratio-of-means A1-R2 / held-out source target for each of S1/S2/S3 must lie in:

`[0.5, 2.0]`.

This retains the historical aggregate gate. It is not converted into an all-fold rule after the fact.

### 11.2 H62 mean superiority

A1-R2 must have both:

- lower mean `D_profile` than N0 **and** C0;
- lower mean absolute `C_short` difference than N0 **and** C0.

### 11.3 H62 fold majority

Against **each** of N0 and C0 separately, A1-R2 must win at least:

- `3/5` folds on `D_profile`;
- `3/5` folds on absolute `C_short` difference.

Strict comparison uses epsilon `1e-12`; ties are not wins.

No superiority over A1-R1 is required. Degradation versus A1-R1 is reported, not used as a hidden rescue/failure threshold.

## 12. Overall Phase64A classification

- **STRONG INVENTORY-AUTONOMY SUPPORT:** ZL primary arm passes and IT independent arm passes.
- **PRIMARY-ONLY SUPPORT / INDEPENDENT FAILURE:** ZL passes, IT fails.
- **INCONSISTENT / PRIMARY FAILURE:** ZL fails, IT passes.
- **NOT SUPPORTED:** both fail.

The only wording that licenses the claim that the tested advantage survives inventory removal is the first classification.

## 13. Mandatory morphology diagnostics

Report for every source/fold/replicate, without using them for post-result selection:

- selected Markov order;
- inner-CV NLL for all candidate orders;
- alphabet size;
- empirical training vocabulary size;
- synthetic vocabulary size;
- attempts/rejections to reach target size;
- synthetic type overlap count/fraction with empirical training types;
- synthetic type overlap count/fraction with held-out types;
- token-length mean/SD/min/max for empirical training and synthetic vocabularies;
- edit1 type density in empirical training and synthetic vocabularies;
- fraction of synthetic types with at least one edit1 neighbor;
- mean synthetic edit1 degree;
- number of synthetic alphabet symbols absent/present relative to training (must be zero absent-from-training by construction);
- generated output token/type counts.

Observed/held-out overlap is diagnostic only and must not affect sampling.

## 14. Complexity/dependence ledger

A1-R2 removes one explicit dependency:

- **removed:** empirical training token membership list as output candidate vocabulary.

It retains:

- training token strings to estimate a low-order character morphology model;
- training-derived alphabet;
- training-derived synthetic vocabulary size;
- training paragraph entry/body shape statistics;
- frozen Voynich-selected A1 architecture/parameters;
- true held-out paragraph/line/token-count layout;
- an explicit 10-token local-family mechanism.

New charged freedom:

- one selected Markov order among three candidates, selected by frozen training-only inner CV;
- additive alpha fixed at 0.5;
- max token length fixed at 20;
- deterministic synthetic-vocabulary sampling seeds.

The report must include the number of nonzero fitted transition cells and selected order. A1-R2 is therefore **inventory-autonomous in the tested sense**, not target-independent or manuscript-autonomous.

## 15. Predeclared failure interpretation

### If ZL + IT pass

Allowed statement:

> **Under the frozen MG0 lower-level morphology generator, A1's tested exposed and prospective structural advantage survives removal of the explicit empirical training-token inventory as its output vocabulary.**

This materially reduces the inventory-topology objection.

### If one or both fail

Record the failure before any model change. Decompose it into:

- morphology instantiation failure;
- S1 entry failure;
- S2 local-family failure;
- S3 aggregate-position failure;
- H62 profile-shape failure;
- H62 short-concentration failure;
- source-specific transfer failure.

Do not add edit-family seeding, templates, affix rules, longer memory or additional mechanisms in Phase64A after seeing the result.

## 16. Claims forbidden regardless of outcome

Phase64A cannot establish:

- Voynichese is meaningless;
- semantics are absent;
- A1 is the historical generator;
- G is superior to the full C or N family;
- the manuscript is deciphered.

A serious C1 fairness challenge and independently grounded content relation remain required.

## 17. Reveal chronology requirement

1. Commit `DECISION_64.md`.
2. Commit this `PLAN_A.md`.
3. Implement MG0/A1-R2 exactly from the frozen plan.
4. Commit executable and workflow **before any Phase64A result is calculated**.
5. First scientific calculation must be triggered from that frozen head.
6. Preserve first-reveal artifact/hash before any result-recording edits.
7. Record pass or failure without repair.
