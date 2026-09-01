# Issue #72 — R1 target implementation freeze

Status: **FROZEN BEFORE TARGET SCORER EXECUTABLE AND BEFORE COUNTERFACTUAL R1 FIRST REVEAL**

Authority:

- `PLAN_A.md`;
- permanent `source-audit/` Stage-A record;
- permanent `family-preflight/` record;
- `family-preflight/TARGET_AUTHORIZED_AXES.txt`;
- `family-preflight/TARGET_AUTHORIZED_REALIZATIONS.txt`;
- exact realization surface SHA-256 values in `family-preflight/preflight.json`.

No real counterfactual pair-Q/residual result exists when this note is committed.

## 1. Parallel realization scoring

Every target-authorized realization is scored in an independent CI matrix job from the same exact first-reveal head.

A realization job may score **only its own frozen surface** and emits:

- exact source/surface identity;
- complete real 66-edge Q vector;
- complete real 66-edge residual-Z vector;
- E and four-manuscript W;
- 1,000 independent test-null energy values;
- 1,000 test-null correlations against each frozen target reading;
- 1,000 test-null sign agreements against each frozen target reading;
- observed topology against both readings.

It does **not** assign final p-values or PASS locally because familywise correction requires the complete counterfactual family.

## 2. Surface identity gate before pair calculation

Each matrix job must:

1. regenerate only its authorized counterfactual from exact frozen sources and intervention labels;
2. find the exact matching realization record in `family-preflight/preflight.json`;
3. require exact canonical surface SHA-256 equality;
4. require exact visible/accepted counts and coverage equality;
5. require axis and realization appear in both frozen target-authorization files.

Any mismatch stops before pair-Q calculation.

## 3. Occupancy adapter

Use the same direct representation adapter as Issue #68:

- preserve manuscript order `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`;
- preserve existing generated item order;
- preserve line order;
- determine full emitted line token count before parser rejection;
- call unchanged `SlotParser.pick(token,"min")`;
- omit only rejected tokens;
- binary occupancy from the returned 12-slot tuple;
- every parsed token inherits its source manuscript fold;
- include a line in the padded line tensor iff at least one token is parsed;
- preserve accepted-token order within the line.

The flat matrix must equal `padded[line_mask]` exactly.

## 4. Candidate-owned null calibration

For realization ID `RID` under axis `A`:

Reference replicate `n` namespace:

`issue72:{A}:{RID}:reference-null:{n}`

Test replicate `n` namespace:

`issue72:{A}:{RID}:test-null:{n}`

This is a literal implementation of PLAN_A's disjoint family namespaces; `RID` is the committed realization token such as `P0`, `S2`, `T5`.

Each realization independently builds its own 1,000 sorted reference-Q distributions and residualizes itself/test nulls against those distributions.

## 5. Target references

Load the exact already archived pooled residual-Z vectors:

- ZL3b #58C;
- IT2a #58D.

Do not recompute manuscript target Q/null calibration.

Before candidate scoring, verify the frozen ZL3b↔IT2a pooled cross-reading values:

- Pearson `0.9884483852763541`;
- sign agreement `65/66`.

## 6. Per-realization reliability

Use the four frozen CREMMA manuscripts as held-out folds.

`W` is median train-other-three vs held-one residual-graph correlation under the realization's own reference calibration.

All four valid folds are required by the plan's `>=4` rule.

## 7. Aggregate familywise stage

After all authorized realization jobs complete, an aggregate job must require artifacts for **exactly every ID in `TARGET_AUTHORIZED_REALIZATIONS.txt` and no other scientific candidate**.

For test replicate index `n=0..999` construct:

- `M_E[n]`: maximum null residual energy across all scored realizations;
- `M_R[n]`: maximum null Pearson across all scored realizations × both target readings;
- `M_A[n]`: maximum null sign agreement across all scored realizations × both target readings.

Final empirical p-values use `(1 + exceedances)/1001`.

No per-axis or per-realization familywise reset is allowed.

## 8. Per-realization and axis classification

The aggregate job applies the exact PLAN_A full R1 gates and computes:

`REL = min(R_ZL3b,R_IT2a) / 0.8830282501011794`.

Axis classes use the preregistered `R1_RETAINED / R1_COLLAPSED / R1_MODULATED` definitions, including:

- `Q=ceil(2N/3)`;
- strong realization = full R1 PASS and REL>=.90;
- retained = strong count>=Q and median REL>=.90;
- collapsed = zero full passes and median REL<.70;
- otherwise modulated.

## 9. Global causal class

The aggregate job applies PLAN_A verbatim:

- I retained → `R1 IS PREDOMINANTLY CODEBOOK/INVENTORY-EMBEDDED`;
- otherwise distinguish codebook-association/state structure, encryption/plaintext process, mixed, or inconclusive from the frozen axis classes/support requirements.

Published Naibbe's already-observed R1 is a frozen reference only, never included in the new counterfactual maxT family.

## 10. First-reveal transport requirements

To avoid the Issue #68 stdout-framing failure:

- scorer stdout must be saved in full;
- the scientific JSON must be written to a dedicated file by the scorer itself, not recovered from stdout;
- stderr progress remains separate;
- each realization artifact contains raw JSON + SHA256 + provenance;
- aggregate artifact contains exact aggregate JSON + SHA256 + complete list/hashes of realization inputs.

The PR-open first-reveal event is not complete until every authorized realization and the aggregate artifact exist.

## 11. R1-only interpretation firewall

Do not compute counterfactual R2/R3/R4 for promotion.

Do not emit selected-edge interpretation before aggregate first-reveal archival.

No intervention family, realization, support rule, threshold, target reading, null count or namespace may change after the first-reveal event.
