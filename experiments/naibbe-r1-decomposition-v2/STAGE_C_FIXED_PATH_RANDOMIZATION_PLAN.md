# Issue #72 V2 — Stage C fixed-path emission-association randomization plan

Status: **PREREGISTERED BEFORE ANY EL/ES/ET/EG R1 TARGET SCORE**

Normative evidential authority:

- `research/RESEARCH_PROTOCOL.md`
- Stage A exact trace result
- Stage B1/B2 unchanged-Naibbe positive-control calibration

Permanent Stage B2 raw authority:

`archive/stage_b2_calibration.json`

SHA-256:

`2da5f0a4f8191820875ed264284f2d3b651489a7e8aeed3805cc2ed4d08c5147`

At the time this plan is committed:

- EL R1 is unrevealed;
- ES R1 is unrevealed;
- ET R1 is unrevealed;
- EG R1 is unrevealed;
- PT R1 is unrevealed;
- FI R1 is unrevealed.

This stage addresses **fixed-realization direct emission association only**. PT total-pipeline and FI final-surface questions remain separate later stages.

---

## 1. Scientific question

> **Conditional on Naibbe's already-realized segmentation/table/state/retry/spacing paths, does the published assignment of Voynich-like glyph values to emission cells produce a systematically more Voynich-R1-like output than outcome-independent association-destroying reassignments?**

This is narrower and more identifiable than asking whether a full codebook rerun "causes" R1.

The process path is deliberately held fixed. Therefore any measured effect belongs to the **direct emission mapping conditional on those paths**, not to downstream retry/RNG feedback.

---

## 2. Why Stage C does not use rep0 alone

Stage B2 showed that historical Issue #68 `rep0` is a valid unchanged-Naibbe realization but relatively high in target topology similarity within `rep0..rep24`:

- `M_R` empirical midrank ≈ `0.86`;
- IT2a correlation empirical midrank ≈ `0.94`.

Choosing a new "representative" subset after seeing the 25-rep distribution would create selection freedom.

Therefore Stage C uses exactly the **historically pre-existing Phase64B five-path panel `rep0..rep4`**, all of it, with no post-B2 path selection.

These five realizations existed and were frozen before Issue #72 was conceived. Stage B2 independently established that all five belong to the highly stable unchanged-mechanism family.

Primary Stage C estimand is explicitly:

> the direct emission-association effect over the fixed historical `rep0..rep4` process-path panel.

It is not silently generalized to every possible Naibbe random path.

---

## 3. Required Stage C0 target-blind trace extension

Before any intervention R1 calculation, reconstruct accepted-event traces for all four CREMMA manuscripts under each `rep0..rep4` seed.

For every `(rep, manuscript)` baseline:

1. run the unchanged historical Phase64B implementation;
2. run the instrumented trace implementation;
3. require raw-token equality;
4. require published-primary equality;
5. require trace-only renderer equality;
6. require exact frozen baseline surface identity from B0/B1 authority.

These are T1 exact-equality gates.

No intervention surface from a baseline trace may proceed if the baseline trace fails exact reproduction.

---

## 4. Fixed process-path representation

A trace freezes, for every emitted event:

- effective plaintext unit identity;
- unigram vs bigram segmentation already realized;
- selected table(s);
- state (`unigram`, `prefix`, `suffix`);
- exact accepted code-cell key(s);
- retry history and accepted attempt;
- final ciphertext-space removal mask / published token grouping.

Fixed-path interventions **do not rerun**:

- plaintext respacing RNG;
- deck shuffling;
- table consumption;
- ambiguity rejection;
- retry draws;
- final space-removal RNG.

They only re-render the already-accepted cell keys through an altered value assignment.

Thus a fixed-path counterfactual can become ambiguous under the published decoder constraint. That is recorded as an outcome and is never repaired or used as an exclusion gate.

---

## 5. Process-path pooling

For the primary Stage C R1 measurement, the five historical paths are pooled as five independent realized blocks over the same frozen CREMMA source panel.

Every `(rep, manuscript, item, line)` retains its own line identity. Line-local R1 null permutations remain within that realized line; no token is shuffled between paths or source lines.

The pooled object is therefore a Monte Carlo block estimate of emitted topology conditional on the frozen Latin panel and the five historical process realizations.

This stage does not use B2 to choose favorable paths.

---

## 6. Four direct-emission axes

All randomization laws operate on **cell instances**, preserving duplicate glyph strings as duplicate instances where relevant.

### EL — source-letter association

Claim tested:

> association between effective plaintext letter identity and emitted glyph values contributes directly to R1, conditional on the fixed process paths.

Randomization:

- effective alphabet = exact 23 Phase64B reachable letters;
- create one global permutation of the 23 effective letters;
- reuse the same letter permutation across every table and state;
- value at `(state, table, letter)` becomes the published value at `(state, table, permuted_letter)`.

Preserves exactly:

- every table×state glyph-value multiset;
- state structure;
- table structure;
- process path;
- visible event grouping / final spacing mask.

It destroys the published source-letter↔value association while preserving cross-state/table coordination by permuted letter identity.

### ES — state association

Claim tested:

> assignment of each table+letter's values to unigram/prefix/suffix state contributes directly to R1.

For every `(table, effective_letter)` independently:

- uniformly permute its three published value instances among `unigram/prefix/suffix`.

Preserves exactly:

- each table+letter three-value multiset;
- letter identity;
- table identity;
- process path.

It destroys systematic state specialization rather than merely applying one global cyclic rotation.

### ET — table association

Claim tested:

> assignment of values to table labels, under the already-realized unequal table-use schedule, contributes directly to R1.

For every `(state, effective_letter)` independently:

- uniformly permute its six published value instances among the six table labels.

Preserves exactly:

- each state+letter six-value multiset;
- state identity;
- letter identity;
- exact realized table schedule and its unequal historical frequencies.

### EG — global reachable-cell association

Claim tested:

> structured assignment across the whole reachable cell system contributes directly beyond the mere global reachable glyph-value inventory.

Randomization:

- canonical cell order: state → table → effective letter using the frozen published orders;
- permute all 414 reachable glyph-value **instances** globally among those 414 cell keys;
- duplicate glyph strings remain duplicate instances;
- unreachable j/k/w cells remain unchanged.

Preserves exactly:

- global reachable value multiset;
- process path.

Destroys:

- letter association;
- state association;
- table association;
- their interactions.

EG is therefore a broad association-destruction control, not a uniquely interpretable one-factor ablation.

---

## 7. Deterministic randomization family

Each axis uses exactly **31** target-blind random assignments, indices `0..30`.

This count is a T5 computational Monte Carlo choice, not a truth threshold.

Why 31:

- together with the published assignment it gives a 32-position rank grid;
- it keeps full complete-66 residual scoring computationally tractable;
- it permits a useful empirical displacement distribution without pretending to exhaust enormous permutation spaces.

No scientific conclusion is defined as "p < .05" or any other significance cutoff, so the 1/32 resolution is not being chosen to manufacture a pass/fail gate.

### Stable permutation construction

Do not depend on Python `random.shuffle` implementation details.

For every finite set of instances, construct the assignment order by sorting canonical instance indices on:

`SHA256("issue72v2:stageC:{AXIS}:{j}:{GROUP}:{instance_index}")`

with canonical index as deterministic tie-breaker.

- EL group = `global-effective-letter`
- ES group = exact `table|letter`
- ET group = exact `state|letter`
- EG group = `global-effective-cell`

The randomization labels and indices are frozen by this plan.

Identity/fixed points are not rejected. The law is an outcome-independent exchangeability/random-assignment law, not a maximum-disruption generator.

No realization may be rerolled because it changes few events, has low parser coverage, becomes ambiguous, or later performs unusually on R1.

---

## 8. Stage C0 support quantities — target-blind only

For every axis×randomization and the pooled five-path output, freeze before target scoring:

- exact surface SHA-256;
- visible token count;
- parser-accepted token count under unchanged `SlotParser(min)`;
- parser coverage;
- coverage by rep and manuscript;
- fraction of final token strings changed from published baseline;
- ambiguity-admissible fraction under the published Naibbe codebook/collision rule;
- exact invariant checks for the nominated randomization law.

### No parser cutoff

There is **no `0.60` or other hard parser-coverage gate** in Stage C.

Coverage is a causal/representational outcome of the value assignment.

An ES or EG realization with 0.53 coverage is not "repaired", excluded, or replaced.

---

## 9. Common-support object

For each randomized surface, align final published-token positions with its exact fixed-path published baseline.

Define **common support** as positions where:

- the published baseline token parses under `SlotParser(min)`; and
- the randomized token at the same fixed-path position also parses.

Freeze before target scoring:

- common-support token count;
- common-support fraction of visible positions;
- per-line common-support counts;
- SHA-256 of the aligned common-support position mask.

This permits a paired R1 comparison on **identical event positions**.

### Interpretation boundary

Common-support analysis does not recover or represent the rejected intervention tokens.

It answers only:

> among event positions representable under both assignments, does reassignment alter the R1 topology?

Coverage loss remains a separate result and must not be hidden by the common-support analysis.

This avoids pretending that parser survivors are an unchanged causal population.

---

## 10. R1 measurement authority

After Stage C0 is permanently frozen, every scored graph uses the same Stage B1 R1 measurement coordinate system:

- unchanged `SlotParser(min)`;
- all 66 unordered slot pairs;
- exact same K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule-Q;
- candidate-owned 1,000 reference line-local nulls;
- empirical mid-rank normal residual-Z transformation;
- complete residual topology correlation to both exact frozen target readings:
  - ZL3b #58C;
  - IT2a #58D.

No selected edge and no edge-specific weighting is permitted.

Stage C does not need a new residual-existence PASS gate. It measures topology displacement of emitted surfaces in the already validated R1 coordinate system.

---

## 11. Primary paired estimand

For every axis `A`, randomization `j`, and target reading `t`:

1. compute the baseline common-support residual graph `Z_base[A,j]`;
2. compute the randomized common-support residual graph `Z_rand[A,j]`;
3. compute target correlations:
   - `R_base[A,j,t] = corr(Z_base[A,j], Z_target[t])`
   - `R_rand[A,j,t] = corr(Z_rand[A,j], Z_target[t])`
4. define paired displacement:

`DELTA_R[A,j,t] = R_rand[A,j,t] - R_base[A,j,t]`

Interpretation:

- negative `DELTA_R`: random reassignment made the same representable event positions less target-like;
- near zero: little direct target-topology effect on common support;
- positive: random reassignment made the common-support graph more target-like.

This paired estimand is primary because it controls event-position support exactly within each randomization.

---

## 12. Randomization rank evidence — no arbitrary hardness band

For each axis and reading, report:

- all 31 `DELTA_R` values;
- median, mean, MAD, min, max;
- count negative / zero / positive;
- empirical Monte Carlo rank quantity:

`p_nonloss = (1 + count(DELTA_R >= 0)) / 32`.

This answers:

> under the frozen association-randomization law, how often does a reassignment preserve or improve the published mapping's target alignment on the exact same support?

For the conjunctive statement "published association is favored in both independent readings", report:

`p_both = max(p_nonloss_ZL3b, p_nonloss_IT2a)`.

`p_both` is reported as evidence strength, **not compared to a newly invented hard cutoff**.

The reading-specific distributions remain visible; the max operation may not hide a disagreement between readings.

---

## 13. Full-survivor R1 is secondary but necessary

For every randomized surface also compute R1 on all parser-accepted randomized tokens, without forcing common support.

Report:

- `R_full_ZL3b`;
- `R_full_IT2a`;
- residual E and W as continuous diagnostics;
- parser coverage.

This describes the complete representable randomized output.

For ES/EG especially, it may differ substantially from the common-support result because representability itself changes.

No claim may combine coverage and R1 into one ad hoc omnibus score.

---

## 14. B2 positive-control scale

Stage B2 supplies the ordinary unchanged-process variation scale:

- `SD(R_ZL3b)=0.010907479701133605`
- `MAD(R_ZL3b)=0.00897810342736527`
- `SD(R_IT2a)=0.008561663953448985`
- `MAD(R_IT2a)=0.005799322835226439`
- unchanged pairwise residual-Z correlation min `0.9761239364746696`, median `0.9916670321955685`.

For each Stage C axis, compare the randomization displacement distribution continuously with these scales, e.g.:

- `median(|DELTA_R_ZL3b|) / B2_MAD_R_ZL3b`
- `median(|DELTA_R_IT2a|) / B2_MAD_R_IT2a`.

These are descriptive calibration ratios only. There is no rule such as "greater than 2 MAD = causal".

B2 measures stochastic execution variation; Stage C measures structural reassignment. They are not identical probability models.

---

## 15. Criterion Validity Table

| Claim | Construct / observable | Randomization or control | Criterion source | Maximum licensed conclusion | Main blind spot |
|---|---|---|---|---|---|
| EL direct contribution | paired common-support `DELTA_R` plus coverage displacement after global letter reassignment | 31 hash-defined global effective-letter permutations | construct T1/T2; Monte Carlo family T5, no hard cutoff | published letter↔value association contributes directly on the frozen five-path panel if random assignments systematically reduce target alignment | cannot include retry/RNG feedback because path is fixed |
| ES direct contribution | paired common-support `DELTA_R` plus coverage displacement after within-table+letter state exchange | 31 independent exchangeability assignments | construct T1/T2; Monte Carlo family T5 | state allocation contributes directly on fixed paths | common support can be much smaller; cannot generalize rejected tokens |
| ET direct contribution | paired common-support `DELTA_R` plus coverage displacement after within-state+letter table exchange | 31 independent exchangeability assignments | construct T1/T2; Monte Carlo family T5 | table-value allocation under the realized table schedule contributes directly | does not test how a rerun retry path would change |
| EG broad structured association | paired common-support `DELTA_R` plus coverage after global 414-cell permutation | 31 global cell-instance permutations | construct T1/T2; Monte Carlo family T5 | structured reachable-cell assignment beyond global inventory contributes directly | combines letter/state/table interactions; not one-factor localization |
| parser representability | direct accepted/visible coverage | published mapping vs same target-blind randomization family | T1 observable, T2 comparative distribution | mapping affects compatibility with the established 12-slot representation | representation compatibility is not historical truth |
| common-support R1 | target correlation on identical positions representable under both assignments | paired baseline for each randomized support mask | T1 pairing + validated R1 measurement role | topology changed among mutually representable event positions | no claim about rejected positions |
| full-survivor R1 | target correlation among all randomized parser survivors | B2 positive-control context | T2 calibrated descriptive | describes resulting representable surface | survivor population changes with treatment |

No T0 threshold appears in this stage.

---

## 16. Evidence-language rules

Stage C may use language such as:

### Strong direct-association evidence

> `PUBLISHED {AXIS} ASSOCIATION IS SYSTEMATICALLY MORE R1-ALIGNED ON THE FROZEN FIVE-PATH PANEL`

only when the paired randomization distributions show the same displacement direction for both target readings and the continuous effect is not merely negligible relative to unchanged B2 variation.

There is deliberately no single numeric gate. The exact counts, rank evidence and scale ratios must accompany the sentence.

### Little detectable direct effect

> `NO MATERIAL FIXED-PATH {AXIS} DISPLACEMENT DETECTED AT THE OBSERVED CALIBRATION SCALE`

only when randomization effects cluster near zero relative to B2 variation in both readings.

This is not proof that the layer is historically irrelevant; retry/process feedback is outside the fixed-path estimand.

### Representation-dominant effect

If coverage falls strongly while common-support R1 remains similar:

> `{AXIS} PRIMARILY CHANGES 12-SLOT REPRESENTABILITY UNDER FIXED-PATH ABLATION; SURVIVING COMMON-SUPPORT R1 IS COMPARATIVELY STABLE`

This is more valid than declaring R1 failure from an arbitrary coverage gate.

### Mixed effect

If both coverage and common-support topology move materially, report both. Do not collapse them into a single PASS/FAIL.

---

## 17. Forbidden post-reveal actions

After any Stage C target score exists, do not:

- change the 31 randomization indices;
- reroll an inconvenient assignment;
- exclude a low-coverage surface;
- alter the parser;
- remap glyphs to improve parseability;
- change common-support definition;
- replace rep0..rep4 with a B2-selected path subset;
- introduce a `.90`, `.70`, `R>=x`, coverage, or p-value cutoff and call it preregistered;
- promote a selected slot edge;
- reinterpret EG as an isolated letter/state/table effect;
- use ambiguity legality as a repair gate.

---

## 18. Stage boundary

Stage C ends with fixed-path direct-emission association results only.

It cannot answer whether:

- plaintext sequence matters through the full published pipeline (PT);
- final token inventory + layout alone is sufficient (FI);
- Naibbe is historically correct;
- Latin is the manuscript plaintext;
- any exact decoder exists.

PT and FI will receive their own criterion-validity plans after Stage C so their distinct causal roles are not mixed with fixed-path emission effects.

---

## 19. Required next step before target reveal

Implement **Stage C0 target-blind support freeze** only:

1. exact rep0..rep4 trace extension;
2. 31 EL + 31 ES + 31 ET + 31 EG assignments;
3. exact surface/invariant/coverage/ambiguity/common-support records;
4. permanent SHA/provenance archive;
5. explicit confirmation that no real intervention complete-66 Q/residual/target correlation has been calculated.

Only after C0 is permanently frozen may a separate scorer implementation be added.
