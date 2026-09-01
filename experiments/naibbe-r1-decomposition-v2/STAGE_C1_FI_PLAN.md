# Issue #72 V2 — Stage C1 final-token allocation randomization

Status: **PREREGISTERED BEFORE ANY FI R1 RANDOMIZATION SCORE**

Parent evidence:

- Stage A: `TRACE-IDENTIFIED INTERVENTION SET READY FOR TARGET DESIGN`;
- Stage B0: historical rep0–rep4 surfaces frozen target-blind;
- Stage B1: `UNCHANGED-NAIBBE R1 STOCHASTIC VARIATION CHARACTERIZED`.

Normative protocol:

`research/RESEARCH_PROTOCOL.md`

## 1. Scientific question

Issue #68 and Stage B1 show that the published Naibbe configuration repeatedly emits a surface with a highly stable R1 residual topology.

Before asking which internal codebook association creates that topology, test the simpler and more causally identifiable possibility:

> **Is the exact assignment of already-produced complete Naibbe tokens to manuscript/line positions necessary for the high R1 topology match, or is the final complete-token inventory itself largely sufficient?**

No token spelling, glyph, codebook cell, plaintext, encryption retry, or token count is changed in this experiment.

## 2. Why FI comes before deeper codebook ablation

The final token surface is downstream of every Naibbe mechanism component.

If random reassignment of the exact already-produced complete tokens retains the same R1 topology, then much of R1 is already encoded in the final token inventory and deeper upstream attribution has a narrower role.

If reassignment destroys the topology, the experiment identifies which level of placement matters before spending effort on more local codebook factors.

This is high-information decomposition, not an attempt to make Naibbe fail.

## 3. Exact identity surface

Use only the exact frozen Issue #68 / Stage-A rep0 primary surface:

`47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`

Population:

- complete primary token instances: `33,574`;
- distinct complete tokens: `7,146`;
- parser-accepted instances: `29,759`;
- pooled parser coverage: `0.886370405671055`.

Identity R1 reference from exact Stage B1/Issue #68 replay:

- E `3.1784043855151296`;
- ZL3b Pearson `0.8830282501011794`;
- IT2a Pearson `0.9000974100381157`;
- ZL3b signs `60/66`;
- IT2a signs `61/66`.

Primary identity topology statistic:

`T_identity = min(R_ZL3b, R_IT2a) = 0.8830282501011794`.

No new identity threshold is inferred from this number.

## 4. Two nested allocation nulls

Exactly two prospectively defined token-allocation randomization families are tested.

### FI-G — global complete-token allocation

Uniformly permute all `33,574` complete token **instances** over the exact existing token slots across the four-manuscript population.

Preserve exactly:

- global whole-token instance multiset;
- every manuscript/item/line visible token count;
- total visible tokens;
- global parser-accepted token multiset and pooled coverage, because token spellings are unchanged.

Destroy:

- manuscript-specific token inventory allocation;
- item/line token identity allocation;
- same-line combination of complete tokens.

Interpretation:

> tests whether the pooled complete-token inventory plus the frozen line-length/layout skeleton is sufficient for R1 without the observed allocation of token identities to manuscripts/lines.

### FI-M — within-manuscript complete-token allocation

Independently permute complete token instances **within each manuscript only** over that manuscript's exact token slots.

Preserve exactly:

- each manuscript's whole-token instance multiset;
- each manuscript/item/line visible token count;
- each manuscript's visible and parser-accepted token counts and coverage;
- global whole-token inventory.

Destroy:

- item/line token identity allocation within manuscript;
- same-line combination of complete tokens.

Interpretation:

> tests whether within-manuscript token placement carries R1 information beyond manuscript-specific token inventories and line lengths.

## 5. Criterion Validity Table

| Claim / role | Construct | Metric / test | Decision source | Positive control | Randomization null | Licensed inference | Blind spot |
|---|---|---|---|---|---|---|---|
| identity surface is unusually R1-like relative to FI-G | agreement of complete 66-edge residual topology with both independent Voynich readings | `T=min(Pearson_ZL3b, Pearson_IT2a)`; one-sided FI-G randomization rank | **T3 randomization inference**, effect context from B1 T2 | five unchanged Naibbe reps; identity rep0 exact replay | global whole-token instance allocation over frozen slots | token allocation above pooled inventory/line skeleton contributes to R1 if identity is extreme | cannot identify whether manuscript, item, or line level is responsible |
| identity surface is unusually R1-like relative to FI-M | same topology construct with manuscript inventory held fixed | same `T`; one-sided FI-M randomization rank | **T3**, B1 T2 context | same | within-manuscript whole-token allocation | within-manuscript placement contributes beyond manuscript inventory if identity is extreme | does not separate item vs line mechanism |
| parser coverage is not an FI selection confound | token spellings unchanged | exact pooled coverage invariance; FI-M also exact per-manuscript coverage invariance | **T1** | identity surface | permutation preserves complete tokens | validates topology comparison support | FI-G can redistribute accepted tokens among manuscripts/folds even though pooled coverage is fixed |
| finite residual calibration is adequate | candidate-owned 1,000-reference line-local null coordinate | same residual transform as Issue #68 | **T2** B1 calibration | B1 primary/secondary null calibrations | candidate-specific line-local reference null | residual-coordinate noise is known to be small | no new test-null p-value is produced |

No `0.90×`, `0.70×`, coverage cutoff, or human-chosen topology threshold is used.

## 6. Primary statistic

For every FI randomization:

1. run unchanged `SlotParser(min)` on the allocated complete tokens;
2. retain all 66 unordered slot pairs;
3. compute the same K_other-conditional Jeffreys-smoothed Mantel-Haenszel Yule-Q;
4. generate that randomization's own `N_ref=1000` line-local reference nulls preserving its accepted line×slot marginals;
5. apply the exact empirical mid-rank normal residual transform;
6. correlate the full 66-edge residual vector with frozen pooled ZL3b #58C and IT2a #58D;
7. define

`T = min(R_ZL3b, R_IT2a)`.

The minimum is used because the R1 topology claim is required to agree with **both** independent readings. It prevents a randomization from being promoted by matching only one reading.

B1 calibrated the natural unchanged-Naibbe range of this same `M_R/T` coordinate (`0.857780–0.883028`) but that range is descriptive context, not the FI decision boundary.

## 7. Randomization population and p-value

For each family independently:

`N_perm = 199`.

Deterministic target-independent namespaces:

- FI-G allocation: `issue72v2:C1:FI-G:allocation:<index>`;
- FI-G residual reference: `issue72v2:C1:FI-G:reference:<index>`;
- FI-M allocation: `issue72v2:C1:FI-M:allocation:<index>`;
- FI-M residual reference: `issue72v2:C1:FI-M:reference:<index>`.

For family F:

`p_F = [1 + #{T_perm >= T_identity}] / 200`.

This is a one-sided exact Monte Carlo randomization question: whether the observed assignment is more target-like than random assignments under the declared preserved quantities.

Minimum attainable p-value is `1/200 = .005`.

## 8. Multiplicity

There are exactly two planned promoting FI allocation questions.

Report:

- raw p for FI-G and FI-M;
- Holm-adjusted p across the two tests.

A layer-specific allocation contribution is supported only when its Holm-adjusted p is `<= .05`.

The `.05` family-wise error rate is a T3 error-control convention, not an effect-size barrier. Raw effect sizes and full randomization distributions remain primary evidence.

No new family may be added after reveal to obtain a more favorable allocation result.

## 9. Secondary continuous outputs

For every family report without extra promotion gates:

- identity T;
- randomization T median, MAD, min, max;
- identity percentile/rank;
- `Delta_T = T_identity - median(T_perm)`;
- separate ZL3b and IT2a Pearson distributions;
- sign-agreement distributions against both readings;
- residual energy E distribution;
- pooled parser coverage distribution;
- for FI-G, accepted token counts by manuscript/fold;
- for FI-M, exact proof that per-manuscript accepted counts are invariant.

B1 stochastic variation is shown beside these effects as context.

## 10. No separate R1 PASS class

FI randomizations are not candidate decipherment mechanisms. Therefore they do not receive the full Issue #68 R1 PASS/FAIL class.

The test asks only whether a particular allocation layer contributes to the already-observed R1 topology.

No test-null existence p-value, full candidate classification, R2, R3, R4 or decoder claim is relevant here.

## 11. Interpretation map

### FI-G significant; FI-M significant

Supported interpretation:

> **R1 depends on token allocation below the manuscript-inventory level; within-manuscript placement contributes beyond the final manuscript-specific inventories.**

Do not yet claim line order specifically; the permutation changes item/line assignment jointly.

### FI-G significant; FI-M not significant

Supported interpretation:

> **R1 depends on manuscript-level inventory allocation, while additional within-manuscript placement is not detectably required under this control.**

### FI-G not significant; FI-M not significant

Supported interpretation:

> **No evidence that the observed token-to-manuscript/line allocation is unusually responsible for R1 once the exact final complete-token inventory and line-count skeleton are fixed. The final inventory is sufficient under the tested FI controls.**

This does not prove the codebook caused that inventory.

### FI-G not significant; FI-M significant

This logically unusual pattern must be reported as-is and treated as `ALLOCATION DECOMPOSITION INCONCLUSIVE` pending diagnosis; no post-hoc relabeling.

## 12. Failure meaning

A nonsignificant result is not proof of literal equality or proof that allocation never matters. It means the identity assignment is not unusually target-like relative to the specified randomization family at the planned resolution/error control.

A significant result does not establish historical Naibbe or plaintext semantics. It identifies a necessary/special allocation layer within this synthetic mechanism comparison.

## 13. Strict target firewall

Before the FI scorer and randomization seeds are committed:

- this plan must be in ancestry;
- N_perm, namespaces, T, multiplicity and interpretation map are frozen;
- no FI-G or FI-M Q/residual/topology result exists.

No permutation may be selected, removed, rerun under a new mapping, or filtered based on R1 performance.
