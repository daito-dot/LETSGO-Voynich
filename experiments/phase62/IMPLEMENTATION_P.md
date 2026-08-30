# Phase 62P — H62-P1 prospective implementation freeze

Status: **frozen after Phase62D and before any H62-P1 Voynich value is computed or revealed**.

This file resolves only execution details left implicit by the already-frozen H62-P1 definition in `PLAN.md`. It does not change the five bins, null, normalization, candidate models, or Phase62D ranking.

## Chronology firewall

Required repository order:

1. Phase62A froze H62-P1 before N0/C0/A1 outcomes;
2. Phase62B/C completed the exposed scorecard;
3. Phase62D committed the exposed-score ranking and pre-result H62-P1 interpretation;
4. this implementation is committed;
5. only then may a run compute/reveal H62-P1.

The executable must not tune A1, select a new C0 transform, introduce C1/A2/M0, or replace H62-P1.

## Inputs and candidate identity

Use the same pinned inputs as Phase62B/C:

- ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- CREMMA commit `292525969ad98380b398e6606a9c2a36d51913ae`.

Candidate identity is inherited, not reselected:

- **N0:** the frozen equal-weight BIS193 / CLM13027 / Mazarine915 / UBL758 panel;
- **C0:** use the exact per-fold transform selected in committed `phase62c_c0_a1_results.json`; no H62-P1-based transform choice;
- **A1:** use exact Phase61C fold parameters and the exact Phase62C five held-out generator seeds/replicates; no retuning.

## Included items

Use the Phase62 primary `base_eligible` items only:

- at least three physical lines;
- at least five usable tokens on line0 and line2.

This keeps the prospective population aligned with the Phase62 tournament population.

Within each included paragraph/item, flatten its physical lines to one token sequence. Token distance may cross physical line boundaries but never paragraph/item boundaries.

## Frozen distance bins

For a token occurrence at position `i`, the full bin is available only if all requested preceding distances exist within the same item.

- B1: distances 1–2, eligible when `i >= 2`;
- B2: 3–5, eligible when `i >= 5`;
- B3: 6–10, eligible when `i >= 10`;
- B4: 11–20, eligible when `i >= 20`;
- B5: 21–40, eligible when `i >= 40`.

For each eligible occurrence/bin, indicator = 1 iff at least one token at the exact distances in that bin is a **non-identical edit-distance-1** token under the same graphematic token representation used by Phase62.

Observed `O_b` is the pooled mean indicator across all eligible occurrences in the evaluated item set.

## Frozen null

For each evaluated item set:

- independently permute token order within every included paragraph/item;
- preserve every item token multiset and item length exactly;
- do not move tokens between items;
- use 100 deterministic replicates;
- for each replicate calculate the same pooled bin indicators.

Seed base is a SHA-256-derived stable integer from `phase62p:H62P1:<entity-label>`; replicate `r` uses base + `r`. Within one replicate a single RNG shuffles all items in deterministic item order.

For each bin:

`E_b = O_b - median(null_b)`.

Also record null 2.5% / 97.5% quantiles and eligible occurrence counts.

## Frozen normalization

Let:

`A = sum_b abs(E_b)`.

If `A > 0`:

`P_b = E_b / A`

and

`C_short = (E_B1 + E_B2 + E_B3) / A`.

If `A = 0`, the profile is invalid for distance comparison and the candidate cannot be declared a prospective leader.

Candidate-vs-held-out-Voynich distance:

`D_profile = sum_b abs(P_b(candidate) - P_b(Voynich))`.

The second primary diagnostic is:

`abs(C_short(candidate) - C_short(Voynich))`.

No weighted combination of these two metrics is allowed.

## Manuscript aggregation for N0/C0

The Phase62 replication unit remains manuscript.

For each of the four primary manuscripts:

1. compute its own `O_b`, null medians, and `E_b` vector;
2. average the four **E vectors equally by manuscript**;
3. normalize only after equal-manuscript averaging to obtain the N0/C0 `P_b` and `C_short`.

Do not pool all Latin entries before normalization and do not average already-normalized manuscript profiles.

C0 is computed separately for every distinct transform selected by Phase62C, then the committed selected transform for each Voynich fold is used. No prospective reselection is possible.

## Voynich outer folds

Use the exact five physical-leaf folds already used in Phase62B/C.

For each fold:

- held-out Voynich profile uses only `base_eligible` paragraphs on the fold's held-out leaves;
- N0 is the fixed equal-manuscript profile;
- C0 uses the transform already selected for that fold in Phase62C;
- A1 is generated on that fold's held-out layout only.

Across-fold summaries report mean and median candidate `D_profile`, mean absolute `C_short` difference, and fold-wise wins.

## A1 stochastic aggregation

Reuse the exact Phase62C generation procedure:

- Phase61C empirical vocabulary and edit1 neighbor graph;
- shape scores learned on the fold's training leaves only;
- frozen parameter pairs:
  - fold0: entry strength .5, local-family p=.20;
  - fold1: .5/.20;
  - fold2: .5/.30;
  - fold3: .5/.30;
  - fold4: .5/.20;
- five deterministic held-out replicates;
- exact Phase62C seed formula:
  `6190000 + fold*100000 + int(strength*10)*1000 + int(local_p*100)*10 + replicate`.

For every A1 realization:

1. compute a full 100-replicate H62-P1 null and its `E_b` vector;
2. average the five realization **E vectors** within the fold;
3. normalize after averaging to obtain the fold A1 `P_b` and `C_short`.

Do not average already-normalized A1 replicate profiles.

## Frozen prospective comparison rule

No forced winner is required.

For each candidate N0/C0/A1, across the five folds report:

- mean `D_profile`;
- median `D_profile`;
- number of folds with the uniquely lowest `D_profile` (ties do not count as wins);
- mean absolute `C_short` difference;
- number of folds with the uniquely lowest absolute `C_short` difference.

A candidate is the **prospective profile leader** only if the same candidate simultaneously:

1. has the lowest mean `D_profile`;
2. has the lowest median `D_profile`;
3. wins `D_profile` in at least 3/5 folds;
4. has the lowest mean absolute `C_short` difference;
5. wins absolute `C_short` difference in at least 3/5 folds.

Otherwise H62-P1 returns **no unique prospective leader**.

### Frozen interpretation of A1

A1 receives genuinely prospective support only if it is the prospective profile leader under the rule above.

A1 receives a **prospective contradiction relative to another tested candidate** if the same competitor:

- has lower mean `D_profile` than A1;
- has lower mean absolute `C_short` difference than A1;
- beats A1 on `D_profile` in at least 3/5 folds;
- beats A1 on absolute `C_short` difference in at least 3/5 folds.

If neither condition holds, H62-P1 is inconclusive for A1 relative to the tested alternatives.

A contradiction does not erase historical Phase61/62 exposed-score passes; it weakens A1's current mechanism-family status and must be recorded before any A2 repair.

## Output requirements

The result JSON must include:

- exact input identities;
- confirmation that `DECISION_D.md` exists in the evaluated repository state;
- committed Phase62C selected C0 transform per fold;
- full observed/null/excess/profile vector for every held-out Voynich fold;
- per-manuscript N0/C0 profile details;
- every A1 realization E vector and fold-averaged profile;
- fold-wise candidate distances and C-short differences;
- frozen-rule summary and prospective interpretation.

## Interpretation limits

A favorable A1 result would be prospective structural evidence for the frozen A1 mechanism, not proof of meaninglessness or historical origin.

A favorable N0/C0 result would not identify Latin or a historical cipher; it would show that the tested meaningful-text family better predicts this unseen structural dimension.

No semantic/decipherment claim follows directly from H62-P1.