# Research protocol — criterion validity before threshold hardness

Status: **NORMATIVE FOR EVIDENTIAL DISCIPLINE**

This file defines how LETSGO-Voynich should design and interpret scientific decision criteria across all research lanes.

`research/RESEARCH_OBJECTIVE.md` controls what the program is trying to achieve. Phase/Issue-specific frozen plans and first-reveal artifacts control historical exact methods and results. This protocol controls the evidential discipline used when new decision rules are designed.

## 1. Core rule

> **A hard decision rule is useful only if the criterion itself is scientifically valid for the claim being decided.**

The project must not optimize for making hypotheses difficult to pass.

A more stringent threshold is not automatically a better threshold. A highly reproducible, perfectly preregistered, strongly multiple-comparison-corrected test can still answer the wrong scientific question if its criterion does not validly represent the claim.

Therefore:

> **criterion validity precedes statistical stringency.**

Preregistration, held-out testing, null models, family-wise error control and threshold robustness protect a valid criterion from bias and chance. They do not make an invalid criterion valid.

## 2. Four distinct questions that must not be collapsed

Every decisive criterion must be evaluated on four separate axes.

### A. Construct validity

Does the measured quantity actually represent the property named in the scientific claim?

Examples:

- a reversible decoder claim can validly require exact recoverability of its declared plaintext target;
- a 12-slot parser-coverage threshold measures compatibility with that representation, not automatically historical-model truth;
- a replicated token-construction graph measures an output-construction constraint, not automatically semantic presence/absence or cipher-family identity.

### B. Threshold validity

Why is the numerical decision boundary where it is?

A threshold needs a stated source. "Strict" or "conservative" is not a sufficient source.

### C. Procedural/statistical validity

Given a valid criterion and threshold, are bias, multiple testing, leakage, stochasticity, null calibration and held-out separation controlled adequately?

### D. Robustness

Would reasonable perturbations of implementation, sample, transcription or non-fundamental threshold choices materially change the conclusion?

A result may be robust without its criterion being valid, and a valid criterion may be noisy or underpowered. These properties must be reported separately.

## 3. Allowed sources for a decisive threshold

Every hard numerical threshold must be tagged with one of the following sources.

### T1 — logical / definitional

The threshold follows from the claim itself.

Example: if the claim is exact deterministic closure `D(E(P)) = P*`, then 100% exact recovery is a definitional requirement for that exact-closure claim.

This is the strongest threshold source.

### T2 — empirically calibrated positive-control / measurement variation

The threshold is derived prospectively from how the target behaves across independent readings, folds, observers, instruments, resamples, or known-positive systems.

Preferred form:

> require a candidate to fall inside or sufficiently near the empirically observed target-to-target variation rather than choosing a round human number.

Where feasible, this should replace arbitrary equivalence bands.

### T3 — null / error-control derived

The threshold controls a specified false-positive family under a scientifically appropriate null.

Examples include preregistered empirical p-values or family-wise maxT thresholds.

This can establish evidence against a null, but it does not by itself establish practical equivalence to the Voynich target.

### T4 — externally justified standard

A threshold comes from an independent literature, measurement standard or accepted domain convention whose applicability is explicitly argued.

### T5 — pragmatic / interface heuristic

A threshold exists because a minimum population, parser coverage or numerical stability is needed to run a defined comparison fairly, but no stronger scientific calibration exists.

T5 thresholds are allowed, but they carry restricted interpretation.

**A T5 failure may reject compatibility with the current testing interface; it must not be silently upgraded into rejection of the underlying mechanism or historical family.**

If a hard gate is T5, its plausible-threshold sensitivity must be reported after the frozen primary result as a non-promoting robustness analysis.

### T0 — unsupported

A threshold has no defensible source beyond convenience, round-number preference, or a desire to make passage difficult.

T0 thresholds are forbidden as decisive gates.

## 4. No hardness objective

The following reasoning is prohibited:

- "this threshold is safer because fewer candidates will pass";
- "a serious decipherment claim should face a very high bar" without linking that bar to the actual claim;
- adding responsibilities because a candidate otherwise looks too successful;
- retaining a metric as a hard discriminator after evidence shows that materially different mechanism families naturally reproduce it, unless the claim is explicitly narrowed;
- interpreting a criterion as strong merely because its p-value is small;
- choosing a demanding round number when a target-derived calibration is available.

The correct question is:

> **What observation would be expected if the scientific property named in the claim were genuinely present, and what observation would meaningfully count against that property?**

The purpose of a threshold is to implement that distinction, not to create an obstacle course.

## 5. Positive-control and negative-control calibration

Before a new criterion becomes a decisive hard gate, the plan should identify, where feasible:

1. a positive control or target-to-target replication showing that the metric can recognize the property it is meant to recognize;
2. a negative or structure-destroying control showing that the metric does not pass indiscriminately;
3. the expected variation of both.

If no defensible positive control exists, the criterion must be labeled **PROVISIONAL** rather than treated as fully validated.

A known positive that barely passes a threshold is evidence that the threshold may be poorly calibrated. A known positive with a large margin and matched negatives with a large opposite margin provides stronger calibration.

## 6. Criterion transport is not automatic

A criterion validated for one role is not automatically valid for another.

For example:

- a statistic can be excellent for demonstrating that a manuscript structure replicates across independent transcriptions;
- the same statistic may later prove weak as a discriminator between historical mechanism families because a materially different target-aware cipher can reproduce it.

When a metric changes role — discovery → replication → discrimination → inverse-model rejection → decipherment validation — its construct validity must be re-audited for the new role.

Historical success does not grandfather a metric into every later tournament.

## 7. Failure interpretation must match the gate

Every hard gate must freeze not only PASS/FAIL conditions but also **what a failure is allowed to mean**.

Examples:

- representation-compatibility failure → `not directly evaluable / not compatible under this representation`, unless independent evidence justifies a broader claim;
- wrong-sign paragraph-entry effect → failure of that paragraph-entry responsibility;
- exact-decoder closure failure → failure of exact decoder closure under the stated decoder target and side-information rules;
- line-local-null residual failure → failure to demonstrate token-internal interaction beyond that null, not proof of randomness or absence of meaning.

A narrow gate must not produce a broader rejection sentence than its construct supports.

## 8. Decisive-plan criterion table

Every future preregistered plan containing hard decisions should include a **Criterion Validity Table** before executable target code exists.

Minimum columns:

| Field | Required content |
|---|---|
| Claim / responsibility | Exact scientific property being judged |
| Construct | What observable property represents that claim |
| Metric | Exact statistic / identity / score |
| Direction | What better/worse means |
| Threshold | Numerical or logical gate |
| Threshold source | T1/T2/T3/T4/T5 |
| Why this source applies | Scientific justification |
| Positive control | Known-positive or target-to-target calibration |
| Negative control / null | Matched negative or destruction control |
| Failure meaning | Maximum claim licensed by failure |
| Known blind spots | Mechanisms that could pass/fail for irrelevant reasons |
| Robustness plan | What non-promoting sensitivity will be reported |

A decisive gate without this table entry is incomplete.

## 9. Preferred hierarchy for designing a criterion

When possible, use this order:

1. define the scientific claim precisely;
2. identify the minimal observable consequence required by that claim;
3. establish measurement reliability / target-to-target variation;
4. select a metric that measures that consequence;
5. calibrate the threshold from T1/T2/T3/T4 evidence;
6. use T5 only where unavoidable and restrict its interpretation;
7. preregister procedural protections;
8. reveal the target once;
9. report both the continuous result and the categorical class;
10. run non-promoting robustness/sensitivity analyses without rewriting the frozen primary result.

This order prevents the common inversion in which a convenient statistic is chosen first and a scientific story is attached to it afterward.

## 10. Continuous evidence must accompany binary classes

Binary PASS/FAIL labels are useful for sequencing, but they must not erase distance from the threshold.

For each decisive metric report, where applicable:

- raw effect size;
- uncertainty / null distribution;
- distance from the decision boundary;
- positive-control range;
- negative-control range;
- classification under a small prospectively meaningful set of non-promoting alternative thresholds when the primary threshold is T5 or otherwise partly conventional.

This makes clear whether a result is a knife-edge decision or a large-margin failure/success.

## 11. Robustness analysis cannot retroactively redefine the primary result

After a frozen reveal, threshold-sensitivity analysis is encouraged.

It may answer:

- how far must a threshold move before the class changes?
- does the result survive alternative legal parser policies, transcriptions, folds or matched nulls?
- is the decision dominated by one stratum or one edge?

It may not:

- choose a new primary threshold because it gives a preferred outcome;
- promote a sensitivity result into the original confirmatory result;
- hide that the original threshold was heuristic.

If robustness analysis reveals that the original criterion was scientifically poorly motivated, the correct response is a **new preregistered criterion-calibration phase**, not retroactive repair.

## 12. Complexity and information-access gates require the same validity standard

Penalizing flexibility is important, but complexity accounting must reflect the scientific claim rather than function as punishment for sophisticated models.

A model may legitimately be complex if the proposed historical or mathematical mechanism requires that complexity.

What must be controlled is unpriced freedom that can absorb the target after inspection:

- target-dependent parameter selection;
- post-reveal codebook changes;
- per-item adaptation;
- hidden side information;
- selected output views;
- undocumented preprocessing degrees of freedom.

The purpose is to distinguish explanation from flexible fitting, not to reward simplicity for its own sake.

## 13. Null-model validity must itself be argued

A stringent p-value is meaningful only relative to the null actually tested.

Every null must state:

- which lower-order structures it preserves;
- which dependency it destroys;
- why destroying that dependency corresponds to the tested scientific alternative;
- important structures it leaves uncontrolled.

If a richer null later reproduces an effect, the interpretation of the earlier result must narrow accordingly. This is scientific refinement, not a reason to protect the old claim.

## 14. Current project example: Issue #68

Issue #68 is useful as a methodological example, not as a universal template.

It showed why the distinctions above matter:

- Naibbe passed the replicated R1 token-construction responsibility while failing R2, R3 and R4. Therefore R1 remains a strong replicated **output-construction constraint**, but its standalone **mechanism-discrimination validity is weaker than its replication validity**.
- A1 failed the 60% common-representation coverage gate. The 60% boundary is a pragmatic T5 interface threshold, so that result is correctly interpreted as failure of direct R1 compatibility under the existing 12-slot representation, not proof that A1's underlying process is false.
- Naibbe's R3 failure is much less threshold-sensitive because its S1 direction was opposite to the target; this is closer to a construct-level failure than a marginal equivalence-band miss.
- Naibbe's R4 exact-closure requirement is T1 for the declared exact-decoder claim; lowering it merely to make the decoder pass would change the claim rather than improve calibration.

Future work should reuse these lessons, not mechanically reuse every #68 threshold.

## 15. Required status labels for criteria

Each major criterion should carry one of these labels when summarized:

- **VALIDATED FOR ROLE** — construct and threshold are supported for the exact current role by strong calibration / identity;
- **CALIBRATED FOR ROLE** — empirically useful with positive/negative controls, but not logically necessary;
- **PROVISIONAL FOR ROLE** — plausible and preregistered, but important calibration is still missing;
- **INTERFACE / HEURISTIC ONLY** — operational threshold needed for fair execution; failure interpretation must remain narrow;
- **DESCRIPTIVE ONLY** — not authorized to drive a categorical scientific class.

A criterion's label may change as new controls are tested.

## 16. Research-selection rule

When choosing the next experiment, prefer work that improves one of:

- construct validity of an important criterion;
- threshold calibration;
- independent replication;
- discrimination between live mechanism families;
- movement toward a constrained reversible/invertible account.

Do not spend research effort merely making an already-difficult tournament more difficult.

## 17. Minimal rule for future agents

Before writing a new PASS/FAIL rule, answer these questions explicitly:

1. **What exact claim is this rule deciding?**
2. **Why does this observable measure that claim?**
3. **Why is the threshold at this value?**
4. **What known positive should pass?**
5. **What matched negative/null should fail?**
6. **What does failure actually license us to say?**
7. **Would a different but scientifically plausible threshold change the conclusion?**

If these cannot be answered, the rule is not ready to be a hard scientific gate.
