# Issue #167 — sparse next-initial support of the Currier outcome bias

Status: **PREREGISTERED BEFORE GATE0 CODE**

Parent: #88. Normative issue: #167.

## Entry authority

Issue #161 is complete with frozen classification:

> `NO ROBUST CONTEXT-SPECIFIC CURRIER EDGE RESIDUAL`

The accepted compact edge responsibility is:

> one shared terminal→initial base table + Currier-specific global next-initial bias.

Frozen #161 authority:

- Gate0 merge / PR #163: `6192e5cbe0a5212d089f890ca26bb7d9a10eedbf`
- Gate0 result SHA-256: `32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94`
- Gate0 script blob: `00e5bddc0484b9472bb4fce9dadb89dd52bf578f`
- Gate0 provenance blob: `67e91ba26a76898f679a5182828ab3e9f512d49a`
- scorer commit: `ecfa604519f1469eac289b9d200f9eedd6a24ddb`
- scorer blob: `d24149977770118505f2147c5aa2bb727631906f`
- first-reveal provenance blob: `73100548fef5dbc0d08a1951e3c0ca5b370cd6f4`
- run: `34077382499`
- artifact: `10002558153`
- result JSON SHA-256: `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`
- science merge / PR #164: `72ff98da2eac4b830dd02eae7623577362c29150`

Issue #165 subsequently found `NO ROBUST SECTION/DOMAIN OUTCOME INFORMATION`; it does not change the #161 base model and no section/domain factor enters this issue.

## Question

Is the predictive Currier next-initial bias concentrated in a small, training-identifiable subset of common-EVA initial outcomes, or is broad 32-outcome support required?

This issue does not reopen whether Currier A/B differ, whether previous-terminal-specific Currier interactions are required, or whether section/domain should enter the model.

## Frozen authority and representation

Reuse Issue #161 exactly:

- same ZL3b and Takahashi/IT2a authorities;
- same common Basic-EVA fixed 32-outcome order (`31 atoms + END`);
- same maximal contiguous clean runs and SlotParser target population;
- same Currier A_ONLY/B_ONLY physical-leaf labels;
- same five outer physical-leaf folds, SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- same exact support-matched `C_A^MATCH`, `C_B^MATCH`, and `C_POOL` tables;
- same full #161 `W_A(y)` and `W_B(y)` multipliers;
- fixed `k=2`, `alpha=.01`, `V=32`;
- no target-native fallback;
- no Currier×previous-terminal interaction.

No representation, Currier label, fold, target population, support rule, pooled weight, smoothing, or full multiplier may change.

## Training-only ranking

For each outer fold, aggregate exact matched training counts:

`G_R(y)=Σ_c C_R^MATCH(c,y)` for `R∈{A,B}`.

The matched A and B aggregate masses are exactly equal. Define:

`q_R(y)=(G_R(y)+alpha)/(M+alpha*V)`.

Rank the fixed 32 outcomes by symmetric Jeffreys-divergence contribution:

`J(y)=(q_A(y)-q_B(y))*ln(q_A(y)/q_B(y))`.

Frozen ranking rules:

- ranking uses training counts only;
- `J(y) >= 0` up to numerical tolerance;
- one ranking is shared by A/B and both readings within an outer fold;
- descending `J(y)` order;
- exact ties broken by the frozen #161 outcome-vocabulary order;
- no held-out current outcome enters ranking or support selection.

## Frozen sparse ladder

Evaluate exactly:

`K ∈ {1, 2, 4, 8, 16}`.

For top-K set `S_K`:

`W_R^K(y)=W_R(y)` if `y∈S_K`, otherwise `1`.

For every retained previous-terminal context:

`P_SPARSE_K,R(y|c) ∝ P_POOL(y|c) * W_R^K(y)`

with exact normalization over the fixed 32 outcomes.

All sparse models remain context-invariant. `K=32` is not a candidate; the exact #161 `EDGE_OUTCOME` is the frozen full ceiling.

## Frozen scientific quantities

For reading `T`, regime `R`, outer fold `f`, and each K:

`G_sparse[K,T,R,f] = bits(EDGE_POOL) - bits(EDGE_SPARSE_K)`

`G_missing[K,T,R,f] = bits(EDGE_SPARSE_K) - bits(EDGE_OUTCOME_FULL)`.

Require within `1e-12`:

`G_sparse + G_missing = G_outcome` from #161.

A sparse model is useful within a reading×regime cell iff mean `G_sparse > 0` and at least 4/5 fold gains are positive.

A full-over-sparse residual is robust within a cell iff mean `G_missing > 0` and at least 4/5 fold residuals are positive.

A K suffices prospectively iff all four reading×regime cells are useful and none of the four cells has a robust full-over-sparse residual.

The primary classification chooses the smallest sufficient K in the frozen ascending ladder. All K are reported. No retention-percentage rescue threshold exists.

## Frozen classifications

Exactly one:

1. `CURRIER OUTCOME BIAS SPARSE SUPPORT: K=1 SUFFICES`
2. `CURRIER OUTCOME BIAS SPARSE SUPPORT: K=2 SUFFICES`
3. `CURRIER OUTCOME BIAS SPARSE SUPPORT: K=4 SUFFICES`
4. `CURRIER OUTCOME BIAS SPARSE SUPPORT: K=8 SUFFICES`
5. `CURRIER OUTCOME BIAS SPARSE SUPPORT: K=16 SUFFICES`
6. `NO TESTED SPARSE CURRIER OUTCOME SUPPORT SUFFICES`
7. `INVALID SPARSE CURRIER OUTCOME FACTORIZATION`

## Mandatory score-free Gate0

Before any real-target sparse probability or likelihood is computed:

1. reproduce merged #161 Gate0 authority and pin #161 scientific scorer/provenance/result identity;
2. reproduce all five exact A/B/POOL matched training tables and equal aggregate masses;
3. reproduce the exact 32-outcome order and full #161 multipliers;
4. compute and archive training-only `q_A`, `q_B`, `J(y)`, and deterministic top-1/2/4/8/16 sets for every fold;
5. prove nesting `S_1⊂S_2⊂S_4⊂S_8⊂S_16` and deterministic tie handling;
6. construct every sparse conditional and prove finite exact normalization for every retained context/regime/K without held-out outcomes;
7. reproduce all reading×regime×fold support/leakage cells from #161;
8. pass synthetic controls showing selected global shifts can enter, excluded outcome contrasts remain excluded, and no previous-terminal interaction is introduced;
9. keep every real-target sparse likelihood, `G_sparse`, `G_missing`, minimal-K classification, semantic interpretation, and post-hoc K change behind the firewall.

Authority/ranking/nesting/support/normalization failure is INVALID; do not repair the scientific family after reveal.

## Consequence fork

If a small K suffices, promote that smaller observable Currier responsibility. A later descriptive issue may inspect the frozen selected EVA outcomes without assigning semantics.

If no tested K suffices, retain the full context-invariant 32-outcome Currier bias. Do not reintroduce previous-terminal interaction merely because sparse support fails.

## Firewall

Do not use held-out target outcomes to rank/select outcomes; change K after reveal; alter labels/representation/folds/support/pooling/target population; tune alpha/ranking/temperature/interpolation/fallback/mixture; reintroduce Currier×previous-terminal interaction; condition on hand/section/domain; fit latent states; or infer words, plaintext, semantics, language/cipher family, authorship, historical mechanism/direction, artificiality/hoax, or decipherment.

Refs #88 #145 #151 #155 #158 #161 #164 #165 #167.
