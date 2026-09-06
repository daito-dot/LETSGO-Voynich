# Issue #127 — L4 Currier transport of explicit terminal→initial edge

Date: 2026-09-06
Status: **FROZEN BEFORE PREDICTIVE TRANSPORT REVEAL**
Parent: Issue #88 / Issue #104 / Issue #125

## Entry authorities

Score-free Gate0 is merged and authoritative:

- Gate result JSON SHA-256 `31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`;
- Phase 3A Currier authority SHA-256 `e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`;
- all ten Currier A/B × fold cells have substantial accepted line-body edge support.

Issue #125 established the explicit observable relation to transport:

> after generic line-start/interior onset control, previous-token terminal raw-byte identity adds robust held-out information about the next token onset within the same source line.

L4 is **mechanism-only transport**. It does not refit the Issue #125 B3 mixture. The question here is whether the compact terminal→initial relation itself transfers between Currier regimes when target-local onset and within-token emission are retained.

## Frozen populations and order

Reuse exactly:

- frozen ZL3b source;
- corrected source order;
- Phase 3A Currier A/B authority, including the frozen `f57v -> B` fallback;
- original five physical-leaf folds;
- no mixed A/B leaves;
- Issue #125 literal UTF-8 byte representation, `END_TOKEN=256`, byte vocabulary size `257`;
- fixed `k=2`, additive `alpha=.01`.

Scientific scoring support is **parser-accepted line-body current tokens only**. The immediately previous visible token need not be parser-accepted, exactly matching the Issue #125 edge definition. Line-start accepted tokens are excluded from L4 scoring because POS2 and EDGE differ only on line-body identity; including identical line-start terms would only dilute the same likelihood contrast.

## Target-local POS2 base

For each target training split, train the explicit Issue #125 target-local POS2 factors using all visible target-regime tokens:

- line-start first-symbol distribution;
- pooled line-body first-symbol distribution;
- line-start/body second-symbol distributions conditional on current first symbol;
- shared within-token k2 remainder.

No source-regime emission or onset distribution is substituted into these target-local factors.

## Edge table

An edge table is the conditional line-body first-symbol distribution:

`P(current_initial | previous_terminal)`

with fixed additive `alpha=.01` over 257 outcomes.

### Native target edge

Use the target training split's own previous-terminal conditional counts.

### Transferred source edge

Train the conditional table on **all eligible source-regime items**. Source and target Currier populations are disjoint by frozen Gate0 authority, so using all source leaves cannot expose any target outer-fold token.

On a target line-body token:

- if `previous_terminal` was observed as a source edge context, use the source conditional table for the current first symbol;
- if that previous-terminal class was not observed in the source table, fall back exactly to the target-local POS2 pooled line-body first-symbol distribution.

Second-symbol and third+ symbol factors remain target-local POS2 factors in all cases.

This fallback is frozen before reveal and represents **no transferred edge relation** for an unsupported source context, rather than importing a source marginal emission distribution.

## Edge-strength mixture

For any target POS2 token probability `p_pos` and edge-table token probability `p_edge`, define:

`p_rho = (1-rho) * p_pos + rho * p_edge`

with frozen grid:

`rho = 0.00, 0.01, ..., 1.00`.

Tie rule: smaller `rho`.

Because POS2 and EDGE differ only at the line-body first-symbol factor and are each normalized token models, this mixture is a normalized mechanism-strength interpolation. It is deliberately separate from the prior B3-versus-byte mixture weight.

## Source-only strength selection

For each source regime `S in {A,B}`, select one `rho_S` using **source-only five-fold cross-validation**:

For each source fold `g`:

- train source POS2/native-edge factors on source leaves outside fold `g`;
- score accepted line-body targets in source fold `g`;
- accumulate held-out log likelihood for every rho.

Sum over all five source validation folds and select rho by maximum pooled source-CV likelihood, ties to smaller rho.

No target token enters `rho_S` selection.

## Target outer-fold evaluation

For each direction `S -> T` and each untouched target outer fold `f`:

1. train target POS2/native-edge factors on target leaves outside `f`;
2. score accepted line-body targets in target fold `f` exactly once;
3. use a source conditional table trained on all eligible source items;
4. compute the four frozen edge variants below.

### FULL_TRANSFER

Source edge table + source-only `rho_S`.

`G_full = bits(POS2_T) - bits(FULL_TRANSFER)`.

This is exact table+strength transport.

### SOURCE_TABLE_TARGET_RHO

Source edge table + rho selected only on target inner folds outside outer `f` while the source table remains fixed.

For each inner target fold `g != f`:

- train target POS2 factors on target leaves outside `f,g`;
- score target fold `g` using the fixed all-source edge table;
- pool likelihood across inner folds and select rho.

`G_table = bits(POS2_T) - bits(SOURCE_TABLE_TARGET_RHO)`.

This asks whether the **source identity table** transfers after target-only strength recalibration.

### TARGET_TABLE_SOURCE_RHO

Native target edge table trained outside outer `f` + source-only `rho_S`.

`G_strength = bits(POS2_T) - bits(TARGET_TABLE_SOURCE_RHO)`.

This asks whether the **source-selected scalar strength** transfers when target identity mapping is supplied.

### TARGET_ORACLE

Native target edge table + rho selected on target inner folds outside outer `f`.

`G_oracle = bits(POS2_T) - bits(TARGET_ORACLE)`.

This is the target-local reference and does not define transport by itself.

## Stability rule

For each direction and each gain family, PASS iff:

- mean gain > 0; and
- positive in at least 4/5 untouched target outer folds.

No effect-size threshold or equivalence margin may be added after reveal.

## Frozen formal classifications

For both `TABLE_TRANSPORT` (using `G_table`) and `EXACT_TRANSPORT` (using `G_full`), classify:

- `BIDIRECTIONAL` — A→B and B→A pass;
- `A→B ONLY` — A→B passes, B→A fails;
- `B→A ONLY` — B→A passes, A→B fails;
- `NONE` — neither direction passes.

For `SOURCE_STRENGTH_COMPATIBILITY` (using `G_strength`), use the same four-way classification.

Also report `TARGET_NATIVE_EDGE` separately for target A and B from `G_oracle`.

Interpretation rules are fixed:

- table bidirectional + exact bidirectional: shared relation table and source-selected strength both transport;
- table bidirectional + exact asymmetric/nontransport: mapping is shared but useful scalar strength differs by regime;
- strength bidirectional + table asymmetric/nontransport: overall strength is compatible but terminal→initial mapping differs;
- both table and strength asymmetric/nontransport: regime-specific edge relation is required under this model family.

These are predictive mechanism statements only.

## Diagnostics

Report without altering any class:

- selected `rho_A`, `rho_B` from source-only CV;
- target-inner selected rho for source-table and native-table variants by outer fold;
- target line-body accepted support;
- source-context fallback count/rate on each target outer fold;
- raw POS2 bits/token and all four mixed edge bits/token;
- foldwise gains and oracle penalties;
- source conditional-table terminal-class count and observed terminal→initial pair count.

## Firewall

L4 must not:

- use target outer-fold tokens for any parameter selection;
- import source POS2 emission/onset factors into target;
- tune alpha, byte order, rho grid or fallback after reveal;
- fit latent states;
- condition on writing hand, illustration/domain or semantics;
- score Issue #84 surface targets;
- infer plaintext, language, cipher family, author, hoax status or historical mechanism.

Currier A/B is an observable manuscript regime, not a semantic or hidden state.
