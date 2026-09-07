# Issue #191 — Productivity / open-vocabulary Stage 0 authority plan

Date: 2026-09-08  
Issue: #191  
Parent: #172  
Base commit: `ce07544a43d9a90c05e5d9fd041262a43b40370d`  
Status: **FROZEN BEFORE STAGE-0 EXECUTABLE**

## Purpose

Stage 0 is a score-free authority and firewall audit for the prospectively defined productivity responsibility in Issue #191. It licenses Stage 1 only if the existing parser, physical-leaf fold lineage, historical OGH grammar authorities, and already-revealed ZL3b OGH-C observation can be identified exactly from the repository.

Stage 0 does not compute a new held-out productivity result.

## Scientific firewall

Stage 0 may read only repository-resident historical authorities and source code. It may replay already-revealed facts needed to verify lineage. It must not load the ZL3b or IT2a transcription data and must not calculate any new quantity from manuscript tokens.

Forbidden in Stage 0:

- constructing train/test canonical vocabularies from manuscript tokens;
- computing held-out new-type/OOV rates beyond replaying frozen OGH-C C0 JSON;
- computing any IT2a new-type/OOV statistic;
- computing any real-manuscript novelty annotation;
- running real-manuscript rarefaction;
- running the 1,000-permutation C2 finite-inventory null;
- generating V2 productivity-control realizations;
- applying the Issue #191 outcome classification.

The executable must emit exactly:

- `marker = "NO ISSUE191 NEW PRODUCTIVITY SCIENTIFIC RESULT COMPUTED"`;
- `scientific_score_computed = false`;
- `stage1_licensed = true` only when every frozen authority check passes.

## Frozen repository authorities

All Git blob SHA-1 values below were re-read from current GitHub `main` at the base commit; these values supersede stale local/chat notes.

| role | path | git blob SHA-1 |
|---|---|---|
| common OGH parser/skeleton integration | `experiments/occupancy-generation-hierarchy/ogh_a.py` | `396284f8b3c94bd4dcf8114bd7b5fb7233de821b` |
| G7A second-order shape grammar | `experiments/occupancy-generation-hierarchy/ogh_b.py` | `844d46ff685ef2d1abbc0c37dcb2f4b1fb75258f` |
| V2/V+ content grammar and historical C0 scorer | `experiments/occupancy-generation-hierarchy/ogh_c.py` | `742513b5ccfcd088e93b8e9480ac02cbc792e986` |
| OGH-C first-reveal report | `experiments/occupancy-generation-hierarchy/REPORT_C.md` | `03d14b586a004f365b97507bc5ad905dc771471a` |
| historical OGH-C information budget | `experiments/occupancy-generation-hierarchy/stage-c0/information_budget.json` | `2ba7f2a488c5302acc04b2c1dd3266ccd271f2f1` |
| frozen 12-slot parser | `experiments/issue26-music/issue26e_core.py` | `8bafba7f2bce4cf77c9001c729936c1ce619759b` |
| IT2a common-representation / ZL-defined fold lineage | `experiments/occupancy-graph-independent-transcription/phase58d_independent_residual.py` | `161f721a325a53632f3d6d917ec5a27da48e2944` |
| historical OGH ZL3b preflight | `experiments/occupancy-generation-hierarchy/preflight/preflight_ZL3b.json` | `123428983b10d1fee2b74056caa402d067d7b5ae` |
| historical OGH IT2a preflight | `experiments/occupancy-generation-hierarchy/preflight/preflight_IT2a.json` | `15a206c85dd1fed4653881b17058640139405399` |
| admissible-shape authority | `experiments/occupancy-generation-hierarchy/preflight/admissible_signatures.json` | `ee376d25b83c7ac79d82d1811c9557d193cf9227` |

## Representation invariants to verify without manuscript data

1. `issue26e_core.py` contains exactly 12 slot inventories and the parser exposes `parses`, `pick`, and `validate_parser`.
2. The 12 inventories contain 33 `(slot,value)` units in total.
3. `ogh_c.py` defines the 33-unit representation from those 12 slots, contains `token_units`, `VPlusModel`, and `V2Model`, and retains the frozen V2 selection rule.
4. `ogh_b.py` contains `fit_g7a` and retains the second-order successor role.
5. `phase58d_independent_residual.py` freezes five folds, ZL blob `2a4533ab9bdfa85db9bad602d590978953055df1`, IT2a blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`, and a 99-leaf check in `frozen_folds_from_zl`.
6. `ogh_a.py` uses five folds, the 12-slot representation, and imports the same parser / Phase58D lineage.

Exact blob identity is controlling; static source checks are explanatory guards against pinning the wrong role.

## Allowed historical replay

Stage 0 may read `stage-c0/information_budget.json` and verify only these already-revealed OGH-C facts:

- schema `ogh-c-c0-v1`;
- five folds;
- selected content grammar `V2`, with positive V2-over-V1 held-out gain in 5/5 folds;
- historical ZL3b V+ mean OOV fraction `0.07034275261192205`;
- historical held-out parsed support by fold `[4430, 4810, 5516, 5447, 4868]`;
- historical parsed total `25071`;
- G7A mean shape cost `7.009998907083391` bits/token;
- V2 mean cost `9.708971376158532` bits/token.

These are historical replay values, not Issue #191 first-reveal results.

## Canonical token identity frozen for Stage 1

Primary canonical type = ordered `(slot,value)` sequence produced by unchanged `SlotParser(min)`. Surface identity = concatenation of unit values. Occupied-slot shape = ordered occupied slot sequence / equivalent 12-bit mask. Rejected tokens remain outside the primary legal-form population and are support-only.

## Frozen implementation details not specified numerically in Issue #191

These choices are fixed now, before the new reveal:

- rarefaction fractions: `[0.10, 0.25, 0.50, 0.75, 1.00]`;
- rarefaction sample size at fraction `q`: `max(1, floor(q*N))`, capped at `N`;
- exact without-replacement expected distinct count: sum over types of `1 - C(N-c,n)/C(N,n)`;
- edit-near test: ordinary character-level Levenshtein distance exactly 1 on canonical surface strings;
- C2 permutations: 1,000 per reading; deterministic namespace `Issue191:C2:<reading>:perm:<i>`;
- C3 V2 realizations: 100 per fold per reading; deterministic namespace `Issue191:C3:<reading>:fold:<f>:rep:<r>`;
- C2 one-sided p-value: `(1 + # null >= observed) / 1001`;
- Monte-Carlo interval for C3: central 95% empirical interval, 2.5th and 97.5th percentiles using linear interpolation.

The Stage-0 executable may self-test these helper definitions on synthetic toy data only. No manuscript tokens may enter those tests.

## Stage-1 contract

If Stage 0 passes, Stage 1 must implement Issue #191 verbatim:

- five physical-leaf held-out new-type measures;
- exact without-replacement rarefaction at the five frozen fractions;
- non-exclusive structural novelty annotations plus intersections;
- C1 closed V+ lookup;
- C2 1,000 deterministic exchangeable finite-inventory permutations;
- C3 100 deterministic V2 realizations per fold;
- ZL3b and IT2a common-representation replication;
- frozen outcome labels and thresholds.

No Stage-0 observation may alter those definitions.

## Admission rule

`stage1_licensed = true` iff:

- all ten Git blob identities match;
- all static parser/OGH/Phase58D invariants match;
- historical C0 JSON matches the allowed replay values;
- the executable's own synthetic helper tests pass;
- no manuscript source file is opened;
- output firewall flags are exact.

Any mismatch returns `stage1_licensed = false`; Stage 1 must stop until the discrepancy is resolved prospectively.