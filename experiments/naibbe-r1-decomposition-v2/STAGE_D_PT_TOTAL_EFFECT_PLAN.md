# Issue #72 V2 — Stage D PT full-pipeline plaintext-order total effect

Status: **PREREGISTERED AFTER C1, BEFORE ANY PT R1 TARGET SCORE**

Normative authority:

- `research/RESEARCH_PROTOCOL.md`;
- `STAGE_A_TRACE_AUDIT_PLAN.md` / `STAGE_A_REPORT.md`;
- `STAGE_B2_REPORT.md`;
- `STAGE_C1_REPORT.md` and permanent `stage-c1/` first-reveal authority.

The completed C1 result motivates this next question but does not alter the PT intervention definition frozen in Issue #72: PT is a full-pipeline upstream intervention, not a fixed-path ablation.

## 1. Scientific question

> **Does within-line order of the effective plaintext characters contribute materially to Naibbe's Voynich-like R1 topology through the complete published pipeline, beyond the per-line character inventory that PT preserves?**

PT is intentionally a **total-effect** experiment. After plaintext order changes, segmentation, deck/table draws, ambiguity retries, card consumption, reshuffles, emitted tokens, and final 3% ciphertext-space removal may all diverge. Those downstream changes are part of the estimand and must not be frozen away as noise.

PT does not estimate a direct semantic or direct letter-order effect isolated from the pipeline.

## 2. Frozen source and mechanism authority

Use exactly:

- CREMMA-Medieval-LAT commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- manuscripts in frozen order: `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`;
- Naibbe commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`;
- encoder blob `b566ad82e4b6ff0782ecdddebf77718dac44f292`;
- tables blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`;
- published Naibbe defaults and published 3% respaced primary output view;
- Phase64B drop-only effective-letter projection with `j/k/w` unavailable and no invented transliteration.

No codebook value, Naibbe parameter, parser policy, source manuscript, output view, or preprocessing rule may be changed from this authority.

## 3. Exact PT intervention

For every source line:

1. form the exact published `clean_line` output;
2. apply the frozen Phase64B effective-letter projection;
3. let the resulting effective plaintext be `c[0..L-1]`;
4. permute the **character instances within that same line only**;
5. send the permuted line into the unchanged published Naibbe encryption pipeline.

PT preserves exactly, line by line:

- effective plaintext length;
- effective plaintext character multiset;
- manuscript/item/line identity;
- the set of empty effective lines.

PT destroys:

- within-line effective character order;
- all order-dependent adjacent/source-span structure.

It does **not** preserve downstream segmentation, tables, retries, token boundaries, or ciphertext spacing.

## 4. Prospective PT randomization population

Use exactly `31` PT assignments, `j = 0..30`.

For each line, character instances are ordered by the ascending tuple

`(SHA256("issue72v2:stageD:PT:{j}:{manuscript}:{item_id}:{line_index}:{source_position}"), source_position)`.

The character attached to each ordered source-position instance is emitted in that order.

This hash-order construction:

- does not touch Python's global cipher RNG;
- is deterministic across runs;
- treats duplicate characters as separate position instances;
- preserves line length and character multiset by construction.

A line may remain textually unchanged by chance, especially if short or repetitive. **No reroll is allowed.** Changed-line counts are descriptive intervention-strength diagnostics only.

`31` is a T5 computational Monte Carlo resolution inherited for tractable Issue #72 decomposition. It is not a truth threshold. Minimum finite non-loss rank is `1/32`.

## 5. Frozen cipher-path blocking population

Use the five historically pre-existing Phase64B realizations `rep0..rep4` as RNG-path blocks.

For manuscript index `mi=0..3` and block `r=0..4`:

`cipher_seed(mi,r) = 6480000 + 100*mi + r`.

For each PT assignment `j`, run all five blocks from the same initial cipher seeds used by their unchanged baselines.

The same-seed pairing is a **coupling/blocking device only**. It does not mean the PT and baseline executions share a fixed process path. Once the changed plaintext causes RNG consumption or retry behavior to diverge, the divergence remains part of the total effect.

The five blocks are not five independent texts. They are technical stochastic realizations over the same frozen source panel.

## 6. Why rep0..rep4 rather than treating 25 B2 realizations as 25 independent experiments

B2 calibrated 25 unchanged executions and remains the authority for ordinary mechanism variation. The PT intervention itself is evaluated across the historically frozen five-path block set already selected before Issue #72 intervention results existed.

Using five blocks avoids pretending that repeated RNG executions are independent source corpora, while still preventing the relatively target-high rep0 from standing alone. B2's full 25-rep distribution is retained as continuous effect-size context.

No min/max of either the five or the 25 positive controls is a hard PT boundary.

## 7. Target-blind Stage D0 support freeze

Before any PT R1 target score, generate the complete `31 × 5 = 155` PT surface population and freeze for every assignment/block/manuscript:

- cipher seed;
- PT permutation namespace/law identity;
- effective-character count;
- exact per-line length/multiset invariant checks;
- number/fraction of textually changed nonempty lines;
- primary and raw surface SHA-256;
- visible and parser-accepted primary token counts;
- parser coverage;
- ambiguity retry count;
- primary/raw token counts.

D0 must also reconstruct all unchanged `rep0..rep4` baselines and prove exact equality to `stage_b0_support.json` before PT support is accepted.

D0 may not load ZL3b/IT2a target residual vectors and may not compute:

- pair Q;
- residual Z;
- E/W;
- target topology correlation;
- sign agreement;
- target p/rank quantities.

Every one of the 155 PT surfaces proceeds regardless of coverage, retries, changed-line fraction, or apparent surface shape. No outcome-based deletion or reroll is allowed.

## 8. R1 measurement after D0 freeze

Only after D0 is durably frozen may Stage D1 score PT.

Each PT output is scored as its **own full output surface** using the same R1 measurement family as B1/B2:

- frozen `SlotParser(min)`;
- all 66 unordered slot pairs;
- same K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule-Q;
- candidate-owned line-local reference null;
- empirical mid-rank normal residual Z;
- residual energy E;
- fold reliability W;
- separate topology correlations to frozen ZL3b #58C and IT2a #58D.

Use `N_ref=1000` with deterministic namespace:

`issue72v2:stageD:PT:j{j}:rep{r}:reference`

and reference replicate index `n=0..999` under the unchanged line-local null generator.

No target reading is averaged into the other.

## 9. No token-position common-support estimand

C1 used common final positions because its fixed-path interventions preserved the process path and final positional correspondence.

PT changes the full pipeline and can change tokenization and visible spacing. Therefore final-token positional alignment is **not a valid construct** for PT and is explicitly forbidden as the primary estimand.

PT and baseline surfaces are each measured independently under the same frozen R1 definition.

Parser coverage is reported separately as representation evidence and is never a hard mechanism-truth gate.

## 10. Primary paired total-effect estimand

For target reading `t`, PT assignment `j`, and RNG block `r`:

`delta_R[j,r,t] = R_PT[j,r,t] - R_baseline[r,t]`

where `R_baseline[r,t]` is the already frozen unchanged-Naibbe B1/B2 result for the same historical block.

For each assignment and reading:

`D[j,t] = mean_{r=0..4}(delta_R[j,r,t])`.

The equal-block mean is the primary finite blocked total-effect summary. Also report all five block effects; the mean must not hide disagreement.

Interpretation:

- `D < 0`: within-line order destruction made the full pipeline less Voynich-R1-like on average over the frozen path blocks;
- `D ≈ 0`: little detectable total R1 effect at this intervention resolution;
- `D > 0`: the shuffled order was at least as/more target-like on average.

## 11. Finite randomization evidence, not a hard gate

For each target reading separately report:

`p_nonloss[t] = (1 + #{j : D[j,t] >= 0}) / 32`.

Also report:

`p_both = max(p_nonloss[ZL3b], p_nonloss[IT2a])`.

These are prospective finite-randomization rank/evidence quantities. They are **not** promoted to a classical universal p-value threshold, and no `.05` PASS/FAIL label is attached solely because the minimum possible value is `.03125`.

Evidence strength must be interpreted jointly from:

- direction across both independent target readings;
- direction consistency across the five blocks;
- continuous effect magnitude;
- B2 unchanged-process variation scale;
- representation/coverage changes.

## 12. B2 effect-size context

Use the frozen 25-rep B2 distributions only as calibrated T2 context.

In particular:

- ZL3b R population SD `0.010907479701133605`, MAD `0.00897810342736527`;
- IT2a R population SD `0.008561663953448985`, MAD `0.005799322835226439`.

For every PT assignment report `D/SD_B2` and `D/MAD_B2` as descriptive scale ratios where defined.

No multiple of SD/MAD becomes a hard causal threshold.

## 13. Criterion Validity Table

| Claim / role | Construct | Metric | Direction / decision use | Threshold source | Positive control | Structure-destroying comparison | Failure / non-effect meaning | Blind spot |
|---|---|---|---|---|---|---|---|---|
| within-line effective plaintext order contributes through the full published pipeline to R1 | displacement of full-output residual topology after preserving each line's effective character inventory but randomizing order | paired `delta_R`, assignment-level `D`, separate ZL3b/IT2a distributions | systematic negative displacement is evidence for an order-dependent total effect; no binary hard gate | **DESCRIPTIVE + finite randomization evidence**; B2 is T2 scale | unchanged rep0..rep4 exact baselines; B2 25-rep distribution | 31 prospectively fixed line-wise order randomizations | near-zero/mixed displacement means no clear detectable order-dependent total effect under this PT intervention, not proof order never matters | total effect does not isolate which downstream step mediates it |
| PT really preserves line inventory | exact line length and `Counter(char)` equality for every source line | all invariants true | required to identify the intervention | **T1** | original effective lines | PT transformed lines | any violation invalidates implementation before target access | does not prove permutations are maximally different |
| same published mechanism is rerun | exact source/codebook/default authority plus baseline replay | exact commits/blobs and exact baseline surface hashes | required implementation identity | **T1** | frozen Stage B0 baselines | none | mismatch is an implementation/authority failure, not scientific PT result | external environment may still affect unpinned dependencies if introduced |
| parser coverage does not become a surrogate truth criterion | representability under frozen 12-slot interface | coverage/accepted count | descriptive only, no cutoff | **DESCRIPTIVE / T5 interface only** | B2 coverage distribution | PT outputs | low coverage narrows what R1 measures; it does not itself reject mechanism history | R1 only describes parser-accepted surface |
| effect magnitude is large/small relative to ordinary Naibbe execution variation | unchanged stochastic R variation | B2 SD/MAD scale ratios | continuous context only | **T2** | B2 25 unchanged reps | PT distribution | small relative effect weakens practical localization; no boundary is decisive | B2 is same source panel, not cross-corpus variation |

## 14. Interpretation map

### Both readings systematically negative, broadly replicated across blocks

Licensed statement:

> **Within-line effective plaintext order contributes materially to Naibbe's R1 resemblance through the complete published pipeline under the frozen source panel/configuration.**

This does not identify whether the mediator is segmentation, table schedule, ambiguity retry dynamics, emitted-token composition, or final spacing.

### Both readings near zero relative to B2 variation

Licensed statement:

> **No substantial total R1 dependence on the tested within-line plaintext ordering is detected once per-line effective character inventory is preserved.**

This is not proof that plaintext order is historically irrelevant.

### Readings or blocks disagree materially

Status:

> **PT TOTAL-EFFECT LOCALIZATION MIXED / INCONCLUSIVE**

Report the disagreement; do not average it away or redesign the shuffle after reveal.

### Positive displacement

Report as-is. A shuffled source order being more R1-like is evidence that the published CREMMA order is not uniquely privileged by this R1 measure under the tested mechanism.

## 15. Strict firewall and forbidden post-reveal actions

Before D1 first reveal, the following must be in ancestry and frozen:

- this plan;
- exact PT permutation implementation;
- exact 31 assignments;
- exact rep0..rep4 block population;
- D0 full 155-surface support authority;
- D1 scorer and aggregation law.

Before D1 target access do not:

- inspect any PT pair-Q/residual-Z/target correlation;
- choose a subset of PT assignments;
- replace an unchanged line with a rerolled line;
- change the number of assignments or blocks because support looks weak/strong;
- change parser policy, codebook, source panel, output view, or target reading;
- introduce final-position matching borrowed from C1;
- turn coverage into a post-hoc eligibility gate.

## 16. Maximum inference

Stage D can localize a **full-pipeline total effect of within-line effective plaintext order** on R1.

It cannot establish:

- historical use of Naibbe;
- Latin as Voynich plaintext;
- semantic content;
- decipherment;
- a direct isolated letter-order mechanism;
- which downstream Naibbe component mediates the total effect;
- independence from the frozen CREMMA source panel.

After Stage D is frozen, Issue #72 should execute the already-preregistered FI final-token allocation control before making its broader codebook/process/final-surface decomposition statement.
