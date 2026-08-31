# Issue #26E5 — selection-adjusted external-structure surprise audit

Status: **FROZEN BEFORE E5 EXECUTABLE / SCIENTIFIC REVEAL**

Issue: #26

Base main at branch creation: `21ca553d0dc7f5e203465d08ae606b4c43305817`

## Why E5 is needed

E4 answered a different question: a topology learned directly from Voynich morphology can transfer between two transcriptions of the same manuscript better than the Guidonian comparator. That does **not** by itself make the external Guidonian fit unsurprising, because the Voynich-trained competitor is allowed to learn Voynich structure from Voynich.

E5 therefore asks the more relevant question:

> After charging the post-reveal selection freedom actually used on the path from E to E2-C, how unusual is it for the historically external Guidonian 20×6 topology to produce a stable six-state correspondence on ZL and then transfer that correspondence to the independent IT2a transcription?

This is an audit of **external-structure surprise**, not a contest against a self-trained Voynich model.

## Frozen sources and representation

Reuse Issue26E/E2/E3 exactly unless this plan says otherwise:

- ZL3b source, required Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`;
- IT2a/Takahashi source, required SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- fresh Zattera 12-slot parser and validation signatures from `issue26e_core.py`;
- exact five physical-leaf folds frozen in E2/E3;
- candidate channel = slot10 states `EMPTY,d,l,r,m,n`;
- residual morphology = categorical one-hot slots `0..9,11`;
- deterministic sequence-blind `k=20` clustering on training token types only;
- held-out score = allowed parsed occurrences / parsed occurrences.

No sequence, section, illustration, line position, music labels, pitch order, melody, rhythm or semantics may enter E5.

### Why slot10 and k=20 are not re-searched here

The published Zattera inventory has exactly one slot with six states including EMPTY: slot10. It was selected in E because the external Guidonian hypothesis has six voces. `k=20` was fixed because the external historical target has twenty gamut loci. E5 does not search alternative slots or alternative k values.

This does not erase the broader research-program multiplicity of having considered music at all; E5 quantifies only the explicit within-model selection path from E to E2-C.

## The selection freedom being charged

Issue26E freely optimized all `6! = 720` state↔column bijections on ZL training data for every fold and for both parser policies (`min` and `max`). After reveal, the `max` parser showed one state mapping recurring in 4/5 folds:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`

index tuple `(0,3,4,1,2,5)`.

That post-reveal stability motivated E2-C, where the mapping was frozen and transferred to IT2a.

E5 gives **every comparator topology the same or greater ZL-only selection opportunity** before IT is inspected.

## Shared candidate lattices

The same candidate lattice must be used across all five ZL folds and all five IT folds. This is essential because E5 evaluates cross-fold mapping stability.

### Primary null family: 200 degree-matched non-Guidonian lattices

Generate exactly 200 deterministic shared null lattices from the Guidonian matrix by degree-preserving double-edge swaps using labels:

`Issue26E5:degree:null:<j>` for `j=0..199`.

Every null must preserve:

- 20 rows;
- the exact Guidonian row-degree profile by row;
- all six column degrees = 7;
- 42 allowed cells;
- non-identity to Guidonian;
- uniqueness within the catalog.

No null is regenerated per fold.

### Secondary structured family

Reuse the already-frozen 100 E3 pair-overlap-histogram-matched non-Guidonian lattices from `E3_STRUCTURED_NULLS.json` without modification.

### Exact-pair specificity diagnostic

Reuse the three exhaustive E3 non-Guidonian alternatives whose full labeled 6×6 pair-intersection matrix is exactly identical to Guidonian from `E3_EXACT_PAIR_ALTERNATIVES.json`.

These three are diagnostic, not an empirical p-value family.

## ZL-only model-selection emulator

For each candidate lattice `L` independently, including Guidonian:

### 1. Free fold fits under each parser policy

For each policy `p ∈ {min,max}` and each ZL fold:

- fit the 20 morphology clusters on ZL training leaves only;
- fit all 720 six-state↔column bijections plus optimal 20-cluster↔row assignment on training occurrences, exactly as Issue26E;
- record the selected six-state permutation and held-out accuracy.

### 2. Mapping recurrence

For a policy, let `R_p` be the maximum number of the five folds sharing an identical selected six-state permutation.

This is invariant to a global relabeling of a candidate lattice's six columns.

### 3. Conservative choice among tied recurring maps

Let `Q_p` be the set of fitted permutations achieving recurrence `R_p`.

For every `q ∈ Q_p`, re-evaluate ZL five-fold held-out accuracy with `q` fixed in all folds while allowing only the 20 cluster→row assignment to fit on each training fold.

Select `q*_p` with the highest mean fixed-map ZL held-out accuracy; ties are broken lexicographically.

This gives null candidates at least as much ZL-only freedom as the historical post-reveal observation, where Guidonian's 4/5 `max` mode was unique.

### 4. Parser-policy selection

Select one policy `p*` using the ZL-only tuple, in descending priority:

1. larger recurrence `R_p`;
2. larger mean fixed-map ZL held-out accuracy for `q*_p`;
3. if still tied, `min` before `max` lexicographically.

Freeze `(p*, q*)` before IT scoring for that lattice.

IT2a is never used to choose policy or six-state mapping.

## IT prospective transfer for every candidate

For each candidate's frozen `(p*, q*)`:

- use the same parser policy `p*` on IT2a;
- in each IT fold, fit the 20 morphology clusters on IT training leaves only;
- keep `q*` fixed;
- fit only the one-to-one 20 IT clusters→20 lattice rows assignment on IT training occurrences;
- score held-out IT leaves.

Report mean IT fixed-map accuracy `A_IT` and five fold accuracies.

## Mandatory Guidonian replay/selection gate

Before any null ranking is accepted, Guidonian must reproduce the historical selection path:

- selected policy = `max`;
- selected recurrence = `4/5`;
- selected mapping = `(0,3,4,1,2,5)`;
- IT mean fixed-map accuracy = `0.8337140490098738` within `1e-12`;
- IT fold accuracies reproduce E2-C within `1e-12`.

If this gate fails, E5 stops as an implementation mismatch.

## Primary and secondary statistics

Let Guidonian have recurrence `R_G` and IT accuracy `A_G`.

For the 200 primary degree-matched nulls report:

1. **selection-adjusted transfer rank**
   - `p_transfer = (1 + #{null: A_IT >= A_G}) / 201`;
2. **joint recurrence+transfer exceedance**
   - `p_joint = (1 + #{null: R >= R_G and A_IT >= A_G}) / 201`;
3. **lexicographic historical-path exceedance**
   - a null is at least as impressive if `R > R_G`, or `R == R_G and A_IT >= A_G`;
   - `p_lex = (1 + #exceedances) / 201`;
4. null medians, q95, maxima, and recurrence distribution.

Repeat analogous descriptive/rank statistics over the 100 E3 structured nulls with denominator 101. Because that catalog was generated for a previous purpose, treat it as a stronger secondary audit rather than a fresh confirmatory family.

For the three exact-pair alternatives, report each candidate's selected policy, recurrence, mapping and IT accuracy versus Guidonian.

## Frozen interpretation categories

E5 will not use a single binary verdict. Report these categories mechanically:

### `SELECTION-ADJUSTED EXTERNAL FIT REMAINS UNUSUAL`

if all hold in the primary degree-matched family:

- `p_transfer <= 0.05`;
- `p_joint <= 0.05`;
- `p_lex <= 0.05`.

### `EXTERNAL FIT SURVIVES ORDINARY NULLS BUT NOT STRUCTURAL SPECIFICITY`

if the primary category above passes, but either:

- structured-null `p_joint > 0.05`, or
- at least one exact-pair alternative has recurrence >= Guidonian and IT accuracy >= Guidonian.

This means the external Guidonian topology remains unusual relative to ordinary matched lattices, but the evidence still does not identify Guidonian-specific higher-order structure.

### `SELECTION FREEDOM EXPLAINS THE APPARENT SURPRISE`

if primary `p_transfer > 0.05` or `p_joint > 0.05` or `p_lex > 0.05`.

## Interpretation boundary

Even the strongest E5 outcome would support only:

> A historically external Guidonian-like six-state dependency geometry matches a stable Voynich slot relationship unusually well after explicitly charging the ZL parser/mapping selection path that led to E2-C.

It would **not** establish literal `ut/re/mi/fa/sol/la`, pitch order, melody, rhythm, musical plaintext, authorship, or a decipherment.

Conversely, E5 cannot prove that the manuscript is non-musical. It only measures how surprising the specific E→E2-C structural path remains under matched selection.

## Chronology firewall

This plan must be committed before `phaseE5_selection_audit.py` exists on the branch. The workflow must verify plan-first ancestry before reveal.

No main merge is authorized by completion of E5. Parallel experiments are active; any E5 branch/PR remains unmerged unless the user explicitly authorizes a merge.
