# Issue #92 / Issue #88 Phase 1 — held-out predictive-information budget

Date frozen: 2026-09-06
Parent program: Issue #88
Implementation issue: #92
Status: **PREREGISTERED BEFORE PHASE-1 EXECUTABLE SCORING**

## 1. Program question

> **How much reproducible held-out predictive information remains in the Voynich token sequence beyond the frozen V2 emission grammar and the Phase-0 likelihood-selected local recency mechanism?**

Phase 1 is prediction-only. It does not try to improve S1, S2, H62, R1 or any Issue #84 inter-token target. Those statistics are unavailable to Phase-1 selectors and are not Phase-1 outputs.

The point is to distinguish three possibilities:

1. most tested cross-token predictability is already exhausted by a small local recency mechanism;
2. longer history or observable document state adds reproducible predictive information;
3. a flexible sequence model exposes additional cross-token predictability missed by the hand-designed models.

This is an empirical predictive budget under declared model classes, **not** a proof of conditional entropy.

## 2. Frozen population and evaluation firewall

Reuse the Issue #81 / Issue #90 ZL3b authority and exact five physical-leaf outer folds.

For the V2-based ladder:

- fit every model only on outer-training leaves;
- select every architecture/hyperparameter using nested leave-one-fold-group-out literal-surface likelihood inside outer training;
- score the exact same parser-accepted outer-held-out token positions used by Issue #90;
- all visible prior surface tokens enter history, including parser-rejected tokens, as in Issue #90;
- history resets only at physical-leaf boundaries unless a model is explicitly the token-boundary-reset flexible control;
- no outer-fold result may alter a grid or architecture.

For the flexible byte predictor:

- train only on outer-training leaves;
- use the same outer physical-leaf test partition;
- primary flexible-model comparison scores the same parser-accepted target-token positions as the V2 ladder;
- preceding visible tokens, whether parser-accepted or not, may supply context equally to both flexible conditions;
- all model selection is nested likelihood only.

S1, S2, H62, R1, Phase-A/B/C target intervals, manuscript illustrations, proposed plaintexts and semantic labels are unavailable to all selectors.

## 3. Predictive ladder

### B0 — frozen V2

Exact Issue #90 memoryless V2 literal-surface likelihood baseline.

Expected regression authority from Phase 0:

`mean outer held-out = 9.7089061017 bits/token`.

This number is a regression check, not a parameter-selection target.

### B1 — bounded local recency anchor

Replay the Phase-0 `DECAY40` family using likelihood-only nested selection and verify the frozen result before interpreting richer models.

Architecture:

- previous at most 40 surface tokens;
- exact edit-distance-1 training-vocabulary neighbours;
- source occurrence weight `exp(-d/tau)`;
- neighbour emission weighted by outer-training token frequency;
- mixture `(1-pi) P_V2 + pi Q_decay`.

Frozen B1 grid:

- `tau in {16, 32, 64, 128, 256, INF}`;
- `pi = 0.00, 0.01, ..., 0.30`.

`INF` is uniform over eligible source occurrences inside the fixed 40-token history.

Phase-0 regression expectation: all five folds should select an architecture in the same local regime and reproduce approximately `9.596181 bits/token` mean. Exact byte identity is not required because the grid is now a Phase-1 replay grid; material failure to reproduce the Phase-0 predictive result triggers an audit before B2-B4 interpretation.

### B2 — longer-history recency challenger

Use the **same edit-1 mechanism** while allowing history beyond 40 tokens. This asks whether longer sequence context improves held-out probability without changing the mutation relation.

Frozen history windows:

`H in {40, 80, 160, 320, ALL}`

where `ALL` means all preceding surface tokens on the current physical leaf only.

Frozen decay scales:

`tau in {16, 32, 64, 128, 256, INF}`.

Frozen mixture grid:

`pi = 0.00, 0.01, ..., 0.30`.

For finite `tau`, source weight is `exp(-d/tau)`. `INF` is uniform over eligible source occurrences inside the chosen history window.

Selection:

- select the single `(H,tau,pi)` with maximum summed nested literal-surface likelihood per outer fold;
- exact tie within `1e-12`: smaller `pi`, then smaller finite `H`, then smaller finite `tau`; `ALL` sorts after finite H and `INF` after finite tau;
- this grid is final. A boundary winner does **not** license extension after seeing outer results.

Primary B2 increment:

`Delta_long = bits/token(B1) - bits/token(B2)`.

A reproducible longer-history gain requires positive mean `Delta_long` and positive `Delta_long` in at least `4/5` outer folds.

### B3 — observable structural-state challenger on top of B2

B3 asks whether simple visible document position adds held-out information after the best B2 history model. It is still a budget measurement, not yet source attribution.

Two prospectively defined state representations compete:

#### B3a `ENTRY_BODY`

Reuse Issue #81 X3 state definition exactly:

- `ENTRY`: every token on the first line of a paragraph/item;
- `BODY`: tokens on all later lines.

#### B3b `LINE4`

Define line state from paragraph/item geometry only:

- `SINGLE`: paragraph/item has exactly one line;
- `FIRST`: first line of a multi-line paragraph/item;
- `MIDDLE`: neither first nor final line;
- `FINAL`: final line of a multi-line paragraph/item.

No token content is used to define either state.

For each inner training split:

1. fit frozen global V2;
2. fit the existing Issue #81 `ContextV2Model` on the chosen state labels, using its unchanged V2 backoff prior;
3. form a normalized surface base

   `P_base_lambda(t|state) = (1-lambda) P_V2(t) + lambda P_stateV2(t|state)`;

4. replace `P_V2` by `P_base_lambda` inside the already selected B2 memory mixture while leaving B2 `(H,tau,pi)` fixed for that outer-fold ladder stage.

Frozen state-strength grid:

`lambda in {0.00, 0.25, 0.50, 0.75, 1.00}`.

Selection:

- B2 is selected first from nested likelihood;
- conditional on that frozen outer-fold B2 architecture, select `(state_family,lambda)` by the same nested-validation likelihood values;
- exact tie within `1e-12`: smaller `lambda`, then `ENTRY_BODY` before `LINE4`;
- `lambda=0` makes B3 reduce exactly to B2.

Primary B3 increment:

`Delta_state = bits/token(B2) - bits/token(B3)`.

A reproducible observable-state gain requires positive mean `Delta_state` and positive `Delta_state` in at least `4/5` outer folds.

Currier, section, scribe and imagery are **not** introduced in Phase 1. They belong to Phase 2 source attribution / Phase 3 transport once the size of the remaining predictive budget is known.

## 4. B4 — flexible cross-token sequence challenger

B4 is deliberately architecturally different from the V2/edit-1 ladder. Its purpose is to detect predictable sequence information that the hand-designed token mechanism may miss.

It must not confound better token-internal modeling with cross-token information. Therefore the primary quantity is a matched continuous-context versus token-reset comparison inside one model family.

### Representation

Encode every literal visible token surface as its UTF-8 bytes followed by one special `END_TOKEN` symbol. The predictive alphabet is the fixed `256` byte values plus `END_TOKEN`, so support is universal and there is no character OOV decision.

No linguistic alphabet, EVA decomposition, slot parse or token meaning is supplied to B4.

### Model family

Use a fixed-order additive-smoothed byte n-gram:

`P(x | context_k) = (count(context_k,x) + alpha) / (count(context_k) + alpha * 257)`.

Frozen order grid:

`k in {0,1,2,3,4,5,6}`.

Frozen smoothing grid:

`alpha in {0.01, 0.10, 1.00}`.

No backoff variant, neural model or extra order is added after outer results.

### B4R — token-reset internal control

Training and test history resets to a fixed BOS context before every visible token. Thus the model predicts literal token bytes and `END_TOKEN` using within-token context only.

### B4C — continuous cross-token challenger

History resets only at physical-leaf boundaries. `END_TOKEN` remains in the byte stream between adjacent visible tokens, so the model may use preceding token endings/surfaces as context for the next token.

Line and paragraph boundary markers are **not** supplied; observable structure is tested separately by B3.

### Training/scoring rule

- B4R and B4C are fitted separately on all visible literal tokens in outer-training leaves;
- `(k,alpha)` is selected separately for B4R and B4C by summed nested likelihood;
- on outer test leaves, the model processes every visible token in sequence so context is correct;
- primary code length is accumulated only for the same parser-accepted target-token positions as B0-B3;
- bytes of parser-rejected preceding tokens may affect B4C history but their own code length is not included in the primary accepted-position score;
- a secondary all-visible-token score is reported as a construct-validity diagnostic.

Primary flexible cross-token quantity:

`Delta_flex = bits/token(B4R) - bits/token(B4C)`.

A reproducible flexible cross-token gain requires positive mean `Delta_flex` and positive `Delta_flex` in at least `4/5` outer folds.

Because B4R and V2 have different token-internal model classes, **absolute B4 bits/token must not be subtracted directly from V2 and called cross-token information**. The matched `B4R-B4C` difference is the valid B4 cross-token quantity.

## 5. Comparing simple and flexible cross-token gains

Define the already-tested simple local gain per fold:

`G_local = bits/token(B0) - bits/token(B1)`.

Define:

`Delta_flex_over_local = Delta_flex - G_local`.

This is an empirical challenger comparison, not a formal decomposition because the internal base models differ.

If mean `Delta_flex_over_local > 0` and the value is positive in at least `4/5` folds, B4 is evidence that a flexible sequence model exposes more cross-token predictability than the simple local edit-1 mechanism captures.

If not, B4 does not establish residual information beyond B1; it does not prove its absence outside the tested model class.

## 6. Criterion Validity Table

| Claim | Construct | Primary metric | Frozen success rule | Evidence source | Positive control / anchor | Main blind spot |
|---|---|---|---|---|---|---|
| local recency is predictive | held-out probability from bounded edit-1 history | `G_local = B0-B1` bits/token | mean > 0 and >0 in >=4/5 folds | T2/T3 paired held-out likelihood | Issue #90 DECAY40 | model-family-specific, not entropy |
| longer history adds information | predictive value beyond <=40 tokens in same mechanism family | `Delta_long = B1-B2` | mean > 0 and >0 in >=4/5 folds | T2/T3 nested held-out likelihood | B1 nested anchor | longer window may still encode only lexical cache |
| visible structural state adds information | line/paragraph position beyond B2 | `Delta_state = B2-B3` | mean > 0 and >0 in >=4/5 folds | T2/T3 nested held-out likelihood | lambda=0 exact B2 fallback | no causal/semantic state attribution |
| flexible sequence context contains cross-token information | context spanning visible token boundaries | `Delta_flex = B4R-B4C` | mean > 0 and >0 in >=4/5 folds | T2/T3 matched held-out likelihood | B4R reset control | byte n-gram may miss longer/nonlocal dependencies |
| flexible model exposes more cross-token information than simple local family | relative empirical context gain | `Delta_flex_over_local` | mean >0 and >0 in >=4/5 folds | T3 cross-model diagnostic | B1 / B4R matched baselines | not an additive information decomposition |

The `4/5` rule is a prespecified stability criterion, not a p-value. All fold values and continuous means are reported regardless of classification.

## 7. Phase-1 classification

### `MATERIAL PREDICTIVE INFORMATION REMAINS`

Classify here if **any** of the following prospective conditions holds:

1. B2 has a reproducible positive `Delta_long`; or
2. B3 has a reproducible positive `Delta_state`; or
3. B4 has reproducible positive `Delta_flex_over_local`.

Interpretation: the Phase-0 local model does not exhaust the tested sequence predictability. Move to Issue #88 Phase 2 source attribution using prospective ablations; rich latent-state work is still not automatically licensed.

### `TESTED PREDICTIVE BUDGET NEAR-SATURATED BY SIMPLE CONTEXT`

Use only if:

- B2 does not pass `Delta_long`;
- B3 does not pass `Delta_state`;
- B4 does not pass `Delta_flex_over_local`;
- B4R/B4C support and normalization are valid.

Interpretation: under these prospectively tested classes, no richer challenger establishes more cross-token predictive information than the small local mechanism. This is not proof that unrestricted conditional entropy is exhausted.

### `MODEL-CLASS / SUPPORT INCONCLUSIVE`

Use if the matched likelihood comparisons are not technically comparable or B4 normalization/support fails. Do not convert an implementation failure into evidence for saturation.

## 8. Fixed diagnostics

Report before interpretation:

- per-fold B0, B1, B2, B3 bits/token;
- B1/B2 selected H, tau, pi and full inner likelihood tables;
- B3 selected state family/lambda and state counts;
- `G_local`, `Delta_long`, `Delta_state` by fold and mean;
- B4R/B4C selected `(k,alpha)` by fold;
- B4R/B4C accepted-position and all-visible bits/token;
- `Delta_flex` and `Delta_flex_over_local` by fold and mean;
- number of scored parser-accepted tokens per fold;
- all-visible token counts;
- any non-finite probability / normalization failure;
- parameter/context table counts for every candidate;
- exact source/fold/code hashes.

No S1/S2/H62/R1 value is produced by the Phase-1 executable.

## 9. Preflight / reveal structure

Phase 1 has no separate surface-target reveal. The held-out predictive scores are themselves the scientific outcomes.

Before the first outer-test run:

1. compile/self-test probability normalization on synthetic data;
2. verify exact source hash and fold identity;
3. verify B0 and B1 regression on training/nested contexts without opening new outer-test B2-B4 scores where practical;
4. verify B4R/B4C use the same 257-symbol alphabet and scoring positions;
5. freeze code and workflow hashes;
6. archive the first complete outer-test run as the authoritative Phase-1 reveal.

No candidate family or grid may be added after that run because an outer fold underperformed.

## 10. Interpretation boundary

Phase 1 measures predictive structure only.

It does not establish:

- what the predicted information means;
- whether it is plaintext, cipher state, scribal habit, layout convention or external content;
- that visible spaces are natural-language word boundaries;
- a historical memory window;
- a latent semantic state;
- absence of meaning;
- decipherment.

If material residual predictive information remains, Phase 2 will ask **where it resides**. If the tested budget is near-saturated, the program should shift attention away from increasingly rich hidden-state generators and toward the information carried by individual production units and the validity of the visible-space boundary.