# Issue #68 — R1 target implementation identities

Status: **FROZEN BEFORE TARGET SCORER EXECUTABLE AND BEFORE R1 FIRST REVEAL**

Authority:

- design main: `b2298d7fe251070dacd21852ae3b5a1dac95fe65`
- `PLAN_A.md`
- exact target-free preflight JSON SHA-256: `fdd2b1138542bf1b332b20f27a9869ac7a3501038e7d4ec9ccf40910e3b98771`
- preflight run `33455622645`, job `99694846814`, artifact `9781331687`

No real-candidate pairwise Q, residual Z, residual energy, reliability, target topology, or R1 p-value has been computed at the time this note is committed.

## 1. Representation gate has already selected the R1 execution set

Frozen preflight result:

- A1: `12650 / 32570 = 0.3883942278170095` direct parser coverage → **`FAIL_REPRESENTATION_COMPATIBILITY`**.
- Naibbe: `29759 / 33574 = 0.886370405671055` → **`AUTHORIZED_FOR_R1_REVEAL`**.

Therefore:

> **The first R1 reveal computes a real complete-66 graph for Naibbe only. A1 real pair/residual computation is forbidden.**

This is not early stopping. It is the preregistered representation gate.

Familywise candidate dimension therefore contains the only representation-compatible prospectively selected candidate, Naibbe. The target-reading dimension still contains both ZL3b and IT2a exactly as planned.

## 2. Frozen Naibbe primary surface identity

Primary published respaced realization 0 only:

| manuscript | seed | canonical surface SHA-256 | accepted / visible |
|---|---:|---|---:|
| BIS193 | 6480000 | `fbf275e179297b947ccd2de5686e02340ea15d6ab9ca4b73a26dd9448b286805` | 11346 / 12804 |
| CLM13027 | 6480100 | `da43249442db277a367bb8171b7228a9bf4b63b055924e9efd06240452d4ad77` | 9716 / 10918 |
| Mazarine915 | 6480200 | `2ebecc4d281df810f57ec370cd1ba0d4708be0391d8185d3ed2ccb588df1f33d` | 6659 / 7536 |
| UBL758 | 6480300 | `5c6649425d9be84f8b9ce04c257cc6fb308e9b8a59191320fcf1a63c86affa89` | 2038 / 2316 |

Pooled canonical primary surface SHA-256:

`47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`

The target executable must abort before any pair calculation if any of these identities differs.

## 3. Candidate fold authority

Naibbe reliability folds are the four frozen CREMMA manuscript identities in this exact order:

0. BIS193
1. CLM13027
2. Mazarine915
3. UBL758

Every parsed token inherits the manuscript fold of its source item.

## 4. Candidate occupancy adapter

For every emitted primary Naibbe token:

1. preserve generated item and line identity;
2. call unchanged `issue26e_core.SlotParser.pick(token, "min")`;
3. discard only tokens that fail this frozen parser;
4. convert the returned 12-slot tuple to binary occupancy `B_s = 1[value_s != ""]`;
5. assign within-line position label `singleton`, `initial`, `interior`, or `final` from the **full emitted line before parser rejection**;
6. do not rewrite, split, merge, transliterate, or subset accepted tokens.

R1 uses all 29,759 directly accepted primary tokens.

## 5. Candidate-owned null namespaces

The preexisting deterministic `stable_seed(label)` hash convention is used. Exact label strings are fixed here:

Reference null replicate `r` (`0..999`):

`issue68:B2:Naibbe:C1-E0:published-respaced:reference-null:{r}`

Independent test null replicate `r` (`0..999`):

`issue68:B2:Naibbe:C1-E0:published-respaced:test-null:{r}`

No alternate namespace may be selected after the reveal.

The same line-local relocation operation as #58B/#58C is used, preserving line × slot occupied counts while independently relocating each slot within its line. Manuscript fold and position labels remain attached to token rows.

## 6. Residual calibration

For the real Naibbe graph and every independent test-null graph:

- compute the complete 66-edge K_other-conditional Jeffreys-smoothed MH Yule-Q vector;
- transform edge `e` through the 1,000 Naibbe **reference-null** edge values using the same empirical mid-rank normal transform as #58C;
- calculate residual energy `E = sqrt(mean(Z_e^2))`;
- calculate four-fold reliability from manuscript folds using the same #58C leave-one-fold-out correlation definition.

Reference and test nulls remain disjoint.

## 7. Residual-existence familywise p

Because Naibbe is the only representation-compatible prospective R1 candidate, test replicate `r` contributes its Naibbe test-null residual energy directly to the candidate-family maximum.

`p_exist_maxT = (1 + #{E_null,r >= E_obs}) / 1001`.

The preregistered effect/reliability requirements remain:

- at least four valid folds;
- `W >= .50`;
- `p_exist_maxT <= .01`.

## 8. Frozen target references

The scorer must read, not re-estimate, the exact pooled `ALL` residual-Z target vectors from the already archived first-reveal authorities:

- ZL3b: #58C exact first reveal;
- IT2a: #58D exact first reveal.

Target Q or target null calibration is never recomputed during Issue #68.

The executable must assert:

- both target vectors contain exactly the same 66 ordered slot pairs used by the candidate;
- both are finite 66-vectors;
- the archived #58D cross-reading `ALL` Pearson/sign values match their frozen record before candidate scoring is emitted.

## 9. Topology familywise maxT

For each independent Naibbe test-null residual graph `Z_r` compute against both fixed target vectors:

- Pearson `R(Z_r, Z_ZL3b)` and `R(Z_r, Z_IT2a)`;
- sign agreement against each target.

For replicate `r`:

- correlation maxT value = maximum of the two target-reading correlations;
- sign maxT value = maximum of the two target-reading sign agreements.

Each observed Naibbe↔target statistic is evaluated against these same reading-family maxima:

`p_R,maxT = (1 + #{max_R_null,r >= R_obs}) / 1001`

`p_sign,maxT = (1 + #{max_sign_null,r >= sign_obs}) / 1001`.

Both ZL3b and IT2a must independently satisfy the frozen effect-size and p-value gates.

## 10. Target output boundary

The R1 first-reveal result may contain:

- exact source/surface/provenance identities;
- candidate population/coverage;
- real complete Q and residual-Z vectors;
- E/W;
- null distribution summaries and maxT p-values;
- topology against both target readings;
- frozen historical R2/R3/R4/R5 statuses;
- candidate/global classification mechanically implied by `PLAN_A.md`.

It may not contain:

- a post-reveal remapped Naibbe view;
- selected-edge rescue analysis;
- alternative realization promotion;
- lowered parser gate;
- new candidate family;
- target-guided decoder repair;
- altered R1/R2/R3/R4/R5 thresholds.

Sensitivities, if later desired, belong after the exact primary first reveal is permanently archived.
