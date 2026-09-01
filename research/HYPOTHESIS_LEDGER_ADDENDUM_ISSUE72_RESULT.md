# Hypothesis ledger addendum — Issue #72 result

Status: **V2 COMPLETE / ALL THREE RESPONSIBILITY CLASSES FROZEN**

Issue #72 asked which layers can validly be identified as contributing to the Naibbe/Voynich R1 resemblance when fixed-realization direct-emission effects, total upstream pipeline effects, and final-surface sufficiency are separated.

The result narrows R1 from a general process resemblance into a more specific **complete-token construction/inventory constraint**.

## H72-C1-EL — effective-letter emitted-value association contributes directly to R1

### Prediction

Under an exactly fixed realized process path, randomizing the association between effective-letter identity and emitted values should systematically reduce R1 if that association is part of the R1-generating scaffold.

### Result

**SUPPORTED.**

Across 31 prospectively fixed assignments:

- ZL3b median ΔR `-0.246725`
- IT2a median ΔR `-0.253840`
- direction: `31/31` both negative

The effect is large relative to Stage B2 positive-control variation.

## H72-C1-ES — functional-state emitted-value association contributes directly to R1

### Prediction

If unigram/prefix/suffix specialization contributes directly to the surface topology, randomizing state-value association on the fixed realized process path should reduce R1.

### Result

**SUPPORTED.**

- ZL3b median ΔR `-0.213530`
- IT2a median ΔR `-0.233840`
- direction: `31/31` both negative

## H72-C1-ET — table-label emitted-value association is a major direct R1 scaffold

### Result

**NOT SUPPORTED AS A COMPARABLY STRONG NECESSITY.**

- ZL3b median ΔR `-0.018601`
- IT2a median ΔR `-0.043740`
- direction: `18` both negative / `12` both nonnegative / `1` mixed

Specific allocation across table labels is substantially more exchangeable than EL, ES or EG under this experiment.

## H72-C1-EG — global reachable-cell emitted-value association contributes directly to R1

### Result

**STRONGLY SUPPORTED.**

- ZL3b median ΔR `-0.334150`
- IT2a median ΔR `-0.368101`
- direction: `31/31` both negative

## Direct-emission localization after C1

The compact mechanistic summary supported by C1 is:

> `effective-letter × functional-state -> emitted glyph value`

This is a major direct-emission scaffold for the Naibbe/Voynich R1 resemblance under fixed realized process paths.

It does not establish historical Naibbe use.

## H72-PT — observed local plaintext character order is materially necessary for R1 through the full pipeline

### Prediction

If exact local plaintext sequence materially drives R1 through Naibbe's complete stateful pipeline, then shuffling character order within each plaintext line while preserving that line's exact character multiset and count should systematically reduce R1 after a complete rerun.

### Frozen result

**REFUTED UNDER THE PREREGISTERED PT ESTIMAND.**

Complete population:

- `31 assignments × 5 RNG blocks = 155/155`
- `0 drops`
- `0 rerolls`

Block-averaged displacement:

- ZL3b mean D `+0.000879`, median D `+0.000827`, nonloss `19/31`, `p_nonloss=0.6250`
- IT2a mean D `-0.000240`, median D `+0.000153`, nonloss `17/31`, `p_nonloss=0.5625`
- joint directions: `15` both nonnegative / `10` both negative / `6` mixed
- frozen `p_both=0.6250`

Interpretation:

> Exact within-line plaintext character order is not supported as a material causal necessity for the Naibbe R1 resemblance when linewise character composition is held fixed.

This does not eliminate effects of plaintext composition, global statistics, semantics, or other source properties.

## H72-FI-M — observed placement of complete tokens within manuscripts is necessary for R1

### Prediction

If the final placement of already-produced tokens within each manuscript contributes materially to R1 beyond the manuscript's token inventory, then within-manuscript complete-token randomization should place the observed identity statistic unusually high in the randomization distribution.

### Frozen result

**REFUTED.**

- identity T `0.8830282501011794`
- 199 preregistered FI-M randomizations
- median randomized T `0.8853778655206299`
- `145/199` randomizations had `T >= T_identity`
- raw p `0.730`
- Holm-adjusted p `1.000`
- about `99.6%` of token slots changed token identity
- each manuscript's exact complete-token multiset and parser-accepted count were preserved

Observed within-manuscript token placement carries no detected extra R1 requirement once the complete-token inventory is fixed.

## H72-FI-G — observed allocation of complete-token inventories among manuscripts is necessary for R1

### Prediction

If corpus-level R1 depends materially on which manuscript receives which already-produced token instances, then globally redistributing the fixed complete-token inventory across the retained token-slot skeleton should reduce T relative to identity.

### Frozen result

**REFUTED.**

- identity T `0.8830282501011794`
- 199 preregistered FI-G randomizations
- median randomized T `0.88509154879863`
- `138/199` randomizations had `T >= T_identity`
- raw p `0.695`
- Holm-adjusted p `1.000`
- about `99.6%` of token slots changed token identity

Even manuscript-level allocation of the already-produced complete-token inventory is not required to retain comparable R1 under the tested control.

## H72-FI — final complete-token inventory is sufficient under the tested allocation controls

### Result

**SUPPORTED.**

Frozen aggregate classification:

> `FINAL_COMPLETE_TOKEN_INVENTORY_SUFFICIENT_UNDER_TESTED_FI_CONTROLS`

This is a sufficiency statement, not an upstream-origin statement.

## Integrated scientific revision caused by Issue #72

Issue #68 showed that published Naibbe can reproduce the replicated R1 topology very well, but did not say what aspect of Naibbe generated that resemblance.

Issue #72 now separates that resemblance into three responsibility layers.

The combined evidence is:

1. **State-dependent emitted-value association matters strongly.** Breaking EL, ES or EG while holding the realized path fixed produces large R1 losses.
2. **Exact local plaintext order does not matter detectably under PT.** Destroying local source sequence while retaining linewise composition and rerunning the whole pipeline leaves R1 essentially unchanged.
3. **Final placement of complete tokens does not matter detectably under FI.** Relocating almost every finished token instance, even globally across manuscripts, leaves R1 typical of or slightly above the original identity allocation.

The best current localization is therefore:

> **R1 primarily constrains the generation and corpus-level distribution of internally structured complete token forms. It does not currently constrain exact local plaintext sequence or the observed placement of finished tokens.**

A compact causal picture is:

`source composition / encoder state opportunities`

`        ↓`

`state-dependent emitted-value mapping`

`        ↓`

`internally structured complete-token inventory + frequencies   <-- R1-sensitive`

`        ↓`

`token placement / sequence / manuscript allocation             <-- no detected extra R1 requirement`

## Consequence for future inverse mechanism search

R1 should no longer be credited as evidence that a candidate reproduces Voynich syntax, paragraph logic, document layout, or source-language sequence merely because its corpus-level residual topology matches.

Its appropriate role is narrower:

> **Does the candidate mechanism naturally generate the right family of internally structured complete-token forms, in roughly the right corpus-level distribution?**

Sequence, recurrence, paragraph-entry behavior, reversibility and other responsibilities must remain independent constraints.

This also clarifies why Naibbe's R1 success does not rescue its overall Issue #68 status: Naibbe remains `NOT COMPETITIVE` because it fails R2, R3 and R4 despite satisfying this token-construction/inventory constraint.

## New falsifiable frontier

The next useful step should not continue perturbing placement or local plaintext order. Those responsibilities are now empirically weak for R1.

The next frontier is to turn the C1 localization into a **mechanism-class constraint**:

> Which minimal families of state-dependent token generators can reproduce the frozen Voynich R1 inventory topology without using a target-aware Voynich-derived codebook, and which structural features are actually necessary?

A defensible next experiment should separate at least:

1. target-aware glyph/codebook choice from generic state-dependent emission architecture;
2. effective-letter/state specialization from merely matching token-length and glyph-frequency marginals;
3. internally generated complete-token inventory from direct resampling of an already-matching inventory;
4. R1 success from the independent R2/R3/R4 responsibilities.

### Falsifying directions

- If generic non-target-aware state-dependent generators reproduce R1 after matching only broad marginals, R1 is a broad token-grammar universality class and weak as a mechanism discriminator.
- If R1 survives only when specific Voynich-derived codebook structure is retained, the target-aware codebook itself accounts for much of Naibbe's R1 success.
- If a minimal generic generator reproduces R1 and also improves independent R2/R3/R4 responsibilities, that family becomes materially more interesting than Naibbe itself.

Historical Naibbe use, Latin plaintext and decipherment remain unsupported by Issue #72.
