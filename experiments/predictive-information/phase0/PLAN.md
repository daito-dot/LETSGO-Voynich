# Issue #90 / Issue #88 Phase 0 — target-blind soft near-family / recency closure

Date frozen: 2026-09-06
Parent program: Issue #88
Implementation issue: #90
Base authority: Issue #81 first reveal (`experiments/cross-token-memory/REPORT_A.md`)
Status: **PREREGISTERED BEFORE PHASE-0 TARGET SCORING IMPLEMENTATION**

## 1. Scientific question

> Can a small target-blind local near-family mechanism retain the predictive gain and S2/H62 short-range geometry discovered in Issue #81 while avoiding X2's raw-recurrence overshoot, without changing the frozen V2 token-emission grammar or losing R1?

This is a surface-closure experiment. It does not identify the historical generator, plaintext, language, semantics, cipher identity, or meaning of any state.

The program-level purpose is constrained by `research/PREDICTIVE_INFORMATION_PROGRAM.md`: Phase 0 closes an already-licensed local surface question before Phase 1 measures the larger predictive-information budget.

## 2. Frozen authorities reused without target-driven modification

- V2 emission grammar / parser representation: OGH-C (`experiments/occupancy-generation-hierarchy/ogh_c.py`).
- Issue #81 corpus loading, five physical-leaf folds, literal-surface likelihood, exact edit-distance-1 neighbour index, generated-surface handling and R1 interface: `experiments/cross-token-memory/issue81_minimal_memory.py`.
- ZL3b primary source authority and frozen five physical-leaf folds: unchanged from Issue #81.
- S2 and H62-P1 computation: unchanged Phase62/64 authority as used in Issue #81.
- R1 complete-66 residual topology scorer and ZL3b/IT2a targets: unchanged Issue #68 / OGH-A authority as re-hosted by Issue #81.
- A1-R1 H62 profile comparator: unchanged Phase63A / Issue #81 authority.
- Issue #81 X2 first-reveal result is an already-observed anchor, not a selector target.

No Phase-A/B/C cross-linguistic/cipher/genre target statistic participates in Phase-0 fitting or model selection.

## 3. Population and firewall

ZL3b remains primary for cross-token scoring. The five frozen physical-leaf folds remain the outer train/test split.

For every outer fold `f`:

- leaves in `f` are never used for candidate-family or hyperparameter selection;
- the remaining four fold groups are used in nested leave-one-group-out validation exactly in the spirit of Issue #81;
- candidate family + hyperparameters are selected by summed literal-surface log likelihood only;
- S1, S2, H62, R1 and Issue #84 target intervals are unavailable to selectors.

Generation uses fixed seed namespaces and exactly three realizations per scored candidate. There are no rerolls.

## 4. Frozen candidate family

The family is intentionally small. Phase 0 tests only the following architectures.

### P0 — `X2-HARD10` replay anchor

Exact Issue #81 X2 architecture:

- previous at most 10 surface-token occurrences;
- eligible source occurrence must have at least one training-vocabulary exact edit-distance-1 neighbour;
- eligible source occurrences are uniform;
- emitted neighbour is weighted by outer-training token frequency;
- mixture probability `(1-pi) P_V2 + pi Q_edit1`;
- `pi` selected by the unchanged nested literal-surface likelihood grid `0.00..1.00` step `.01`.

Scientific role: historical anchor / regression control. Its already-known first-reveal target score is not treated as new evidence.

### P1 — `DECAY40`

Architecture:

- history contains the previous at most 40 surface-token occurrences on the same physical leaf;
- for a source occurrence at lag `d` (`d=1` most recent), source weight is `exp(-d/tau)`;
- only occurrences with at least one training-vocabulary exact edit-distance-1 neighbour are eligible;
- conditional on the chosen source occurrence, emitted neighbour probability is proportional to outer-training token frequency, unchanged from X2;
- memory distribution `Q_decay` is normalized over eligible weighted source occurrences;
- mixture probability is `(1-pi) P_V2(token) + pi Q_decay(token | history, tau)` when at least one eligible source exists, otherwise exactly `P_V2`.

Frozen hyperparameter grid:

- `tau in {1, 2, 4, 8, 16, 32}` tokens;
- `pi = 0.00, 0.01, ..., 0.30`.

The upper `pi=0.30` bound is an architecture/regularization bound, not a Voynich target bound. It is three times the stable Issue #81 likelihood optimum and still permits a materially stronger branch while preventing the grid from becoming an unrestricted copy generator. If the nested-likelihood optimum lands at `.30`, this is recorded as a boundary hit and Phase 0 does not extend the grid after target reveal.

Tie rule: larger total inner-validation likelihood wins; within `1e-12`, choose smaller `pi`, then smaller `tau`.

### P2 — `TILT10`

Architecture:

- history contains previous at most 10 surface-token occurrences;
- construct `A(t | history)` as the number of recent source occurrences for which literal candidate token `t` is an exact edit-distance-1 training-vocabulary neighbour;
- no separate forced memory branch exists;
- start from the frozen V2 literal surface distribution;
- reweight only training-vocabulary neighbour surfaces using

  `P_tilt(t | h) ∝ P_V2(t) * exp(beta * A(t | h))`;

- all non-activated V2-supported surfaces retain multiplicative weight `1`;
- normalization is exact over the finite V2 surface support induced by the training model as implemented in the prereveal implementation note; if exact normalization cannot be computed without changing the declared model, P2 is `IMPLEMENTATION_BLOCKED`, not replaced post hoc by a different formula.

Frozen hyperparameter grid:

- `beta in {0.10, 0.20, 0.40, 0.80, 1.20, 1.60}`.

Tie rule: larger total inner-validation likelihood wins; within `1e-12`, choose smaller `beta`.

Scientific role: tests whether the hard branch/copy event itself caused the raw recurrence overshoot, while preserving the same independently motivated edit-1 local activation.

### No Phase-0 composition

`DECAY40` and `TILT10` are rivals. They may not be combined after target reveal. Paragraph ENTRY/BODY X3 is not composed in Phase 0.

## 5. Candidate selection rule

For each outer fold independently:

1. compute inner-fold literal-surface likelihood for every legal candidate/hyperparameter setting;
2. choose the single highest-likelihood setting across `DECAY40` and `TILT10` only;
3. retain `X2-HARD10` as a replay anchor but do not let its known target score select the winner;
4. refit empirical V2/vocabulary/frequency tables on all outer-training leaves using the selected architecture/hyperparameters unchanged;
5. evaluate outer held-out literal-surface likelihood;
6. only after all five outer selections are frozen generate the three fixed target realizations and expose S2/H62/R1.

The selected architecture may differ across outer folds. Report both per-fold selections and the aggregate frequency of architecture choices. No majority-vote refit on the full manuscript is permitted in Phase 0.

## 6. Criterion Validity Table

| Claim / responsibility | Construct | Metric | Direction | Frozen criterion | Source | Positive control | Negative / contrast control | Failure meaning | Blind spots / robustness |
|---|---|---|---|---|---|---|---|---|---|
| Local mechanism contains genuine predictive information | unseen literal token probability | outer held-out surface bits/token | lower is better | mean selected-model bits/token `<` mean X0 bits/token **and gain is positive in at least 4/5 outer folds** | T2/T3 empirical paired held-out comparison; sign-count is a prespecified stability requirement, not a p-value | Issue #81 X2 had positive gain all 5 folds | frozen X0 V2 | tested local form does not provide stable predictive gain | effect size in bits/token always reported; no claim of entropy bound |
| S2 local near-family responsibility | generated corpus reproduces frozen S2 scale | aggregate candidate S2 / held-out target S2 | near 1 | candidate aggregate lies inside the **five-fold held-out target measurement interval expanded only by the frozen three-realization Monte Carlo uncertainty rule below** | T2 target-to-target / sampling calibration | held-out Voynich folds | X0 memoryless | candidate does not reproduce S2 under this representation | continuous ratio and each realization reported |
| Raw H62 amount | generated total near-family recurrence excess matches observed amount rather than merely exceeding a lower bound | `abs_excess_sum` | near target | candidate aggregate must lie inside the **min..max of the five frozen held-out Voynich `abs_excess_sum` values**, expanded on each side by one preregistered generator-MC half-range estimated from its three fixed realizations | T2 target measurement variation + candidate stochastic measurement precision | five held-out Voynich folds | X0 and X2-HARD10 anchors | candidate under/over-produces raw recurrence outside empirical target variation | this is intentionally two-sided; exact continuous distance reported; no threshold adjusted after seeing X2=2.12x |
| H62 short-range geometry | normalized lag profile matches an already accepted positive-control regime | Phase64 `D_profile` and `abs_C_short_diff` | lower is better | both candidate means no worse than frozen A1-R1 means, unchanged from Issue #81 | T2 positive-control calibration | frozen A1-R1 | X0 | candidate does not reproduce accepted short-range geometry | comparator validity remains limited to surface geometry, not mechanism identity |
| R1 emission compatibility | generated surfaces retain replicated token-internal construction constraint | Issue #81/68 complete-66 R1 gate after min reparsing | pass | unchanged Issue #81 R1 necessary gate | mixed T2/T3 with parser coverage T5 as already documented | ZL3b↔IT2a replicated target / V2 family | candidate-owned line-local null | surface output is not R1-compatible under current representation | parser coverage failure remains interface-limited |

### S2 target-variation implementation

Before candidate target generation, the implementation must extract the five frozen held-out Voynich S2 values from the unchanged Phase62/64 contexts. The target interval is their literal `[min,max]`; no candidate result may alter this interval.

For a stochastic candidate with realization-level S2 values `s_r`, define generator-MC half-range as `(max(s_r)-min(s_r))/2`. The candidate aggregate mean must lie within `[target_min - MC_half_range, target_max + MC_half_range]`.

This rule acknowledges three-realization generator noise without inventing a percentage band. The unexpanded target interval and MC expansion are both reported.

### Raw-H62 target-variation implementation

Before candidate target generation, extract the five frozen held-out Voynich `abs_excess_sum` values. The literal target interval is `[min,max]`.

For candidate realization-level raw values `h_r`, MC half-range is `(max(h_r)-min(h_r))/2`. The candidate aggregate raw value must lie within `[target_min - MC_half_range, target_max + MC_half_range]`.

The target interval itself is immutable and candidate-independent; only the separately reported MC measurement allowance depends on candidate stochasticity.

## 7. Overall Phase-0 classifications

### `LOCAL-CLOSURE SUFFICIENT`

The selected target-blind architecture must satisfy all of:

1. stable positive predictive gain versus X0 under the frozen held-out criterion;
2. S2 target-variation criterion;
3. two-sided raw-H62 target-variation criterion;
4. frozen H62 profile criterion;
5. R1 retained in all three realizations.

S1 is not a Phase-0 responsibility.

### `PREDICTIVE BUT SURFACE-INCOMPLETE`

Stable positive predictive gain exists, but at least one S2/raw-H62/profile/R1 responsibility fails.

### `NO STABLE PREDICTIVE GAIN`

The selected local family fails the predictive criterion. Surface-statistic matches, if any, remain descriptive and cannot promote the family.

### `IMPLEMENTATION_BLOCKED`

A preregistered architecture cannot be implemented as mathematically declared without changing its probability model. It is not silently replaced after reveal.

## 8. Fixed diagnostics

Report before interpretation:

- per-fold chosen architecture and hyperparameters;
- full inner-CV likelihood tables/curves;
- outer held-out surface bits/token for X0, X2-HARD10, DECAY40, TILT10 where evaluable, and selected model;
- bits/token gain versus X0 by fold and mean;
- memory-context availability;
- DECAY40 realized memory-event rate, source-lag distribution and fallback rate;
- TILT10 activated-neighbour mass / normalization diagnostics;
- all three realization S2/raw-H62/H62-profile values;
- immutable target fold ranges used by T2 criteria;
- R1 parser coverage and continuous topology statistics for all three selected-model realizations;
- X2-HARD10 replay consistency against the archived Issue #81 result.

S3 and S1 may be reported descriptively but do not participate in Phase-0 classification.

## 9. Preflight before target reveal

Before the first candidate S2/H62/R1 target run, a score-free preflight must establish:

- source hash / frozen fold identity;
- exact reuse of V2 / parser / neighbour relation;
- DECAY40 probability normalization on synthetic histories;
- TILT10 probability normalization on synthetic/training-only histories or else `IMPLEMENTATION_BLOCKED`;
- deterministic nested-selection reproducibility;
- generated population/line/token counts and seed determinism without calling S2/H62/R1 scoring functions;
- no target scoring call occurs in preflight.

Any prereveal implementation amendment must be committed as a clearly labeled amendment before the first target-scoring workflow run and may not be motivated by target outcomes.

## 10. Interpretation boundary and next-program rule

A Phase-0 pass means only that a small local predictive mechanism is sufficient for the frozen local surface responsibility. It does not establish that the mechanism was historically used.

A fail means only that the frozen local forms are insufficient.

Regardless of pass/fail, the next program-level question under Issue #88 is Phase 1: measure the broader held-out predictive-information budget. A Phase-0 pass does not automatically license semantic interpretation, a rich latent-state search, or a post-hoc X3 composition.