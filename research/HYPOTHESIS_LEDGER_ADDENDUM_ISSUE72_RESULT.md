# Hypothesis ledger addendum — Issue #72 result

Status: **V2 COMPLETE / ALL THREE RESPONSIBILITY CLASSES FROZEN**

Issue #72 asked which layers can validly be identified as contributing to the Naibbe/Voynich R1 resemblance when fixed-realization direct-emission effects, total upstream pipeline effects, and final-surface sufficiency are separated.

## Representation authority

R1 does not directly score literal glyph identity or literal token strings.

For every parser-accepted token, the frozen scorer uses `SlotParser(min)` and converts the token to a binary 12-slot occupancy vector:

`X[token, slot] = occupied / empty`

The 66-edge R1 object is the null-residual dependency topology over all `C(12,2)=66` unordered occupancy pairs.

Accordingly, Issue #72 localizes the causal production of a **12-slot token-occupancy grammar**, not a complete lexical/string grammar.

## H72-C1-EL — effective-letter emitted-value association contributes upstream to R1

### Result

**SUPPORTED.**

Across 31 prospectively fixed assignments:

- ZL3b median ΔR `-0.246725`
- IT2a median ΔR `-0.253840`
- direction: `31/31` both negative

Because R1 scores parsed occupancy rather than glyph identity, the causal path is:

`effective-letter value association -> emitted token form -> parsed occupancy signature -> R1`

## H72-C1-ES — functional-state emitted-value association contributes upstream to R1

### Result

**SUPPORTED.**

- ZL3b median ΔR `-0.213530`
- IT2a median ΔR `-0.233840`
- direction: `31/31` both negative

Unigram/prefix/suffix state specialization materially affects the occupancy topology produced by the fixed path.

## H72-C1-ET — table-label emitted-value association is a major direct R1 scaffold

### Result

**NOT SUPPORTED AS A COMPARABLY STRONG NECESSITY.**

- ZL3b median ΔR `-0.018601`
- IT2a median ΔR `-0.043740`
- direction: `18` both negative / `12` both nonnegative / `1` mixed

Specific allocation across table labels is substantially more exchangeable than EL, ES or EG under this experiment.

## H72-C1-EG — global reachable-cell emitted-value association contributes upstream to R1

### Result

**STRONGLY SUPPORTED.**

- ZL3b median ΔR `-0.334150`
- IT2a median ΔR `-0.368101`
- direction: `31/31` both negative

## Direct-emission localization after C1

The compact upstream mechanistic summary remains:

> `effective-letter × functional-state -> emitted glyph value`

but its R1 consequence should be stated precisely as:

> structured state-dependent emission is a major upstream determinant of which 12-slot occupancy signatures are generated.

This does not establish historical Naibbe use.

## H72-PT — observed local plaintext character order is materially necessary for R1 through the full pipeline

### Result

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

> Exact within-line plaintext character order is not supported as a material causal necessity for the resulting R1 occupancy topology when each line's character composition is held fixed.

This does not eliminate effects of plaintext composition, global statistics, semantics, or other source properties.

## H72-FI-M — observed placement of occupancy signatures within manuscripts is necessary for R1

### Result

**REFUTED.**

- identity T `0.8830282501011794`
- 199 preregistered FI-M randomizations
- median randomized T `0.8853778655206299`
- `145/199` randomizations had `T >= T_identity`
- raw p `0.730`
- Holm-adjusted p `1.000`
- about `99.6%` of literal token slots changed token identity
- each manuscript's exact complete-token multiset was preserved

Because complete-token shuffling also preserves each token's parsed occupancy signature, FI-M shows that observed within-manuscript placement of those occupancy signatures carries no detected extra R1 requirement.

## H72-FI-G — observed manuscript/line allocation of occupancy signatures is necessary for R1

### Result

**REFUTED.**

- identity T `0.8830282501011794`
- 199 preregistered FI-G randomizations
- median randomized T `0.88509154879863`
- `138/199` randomizations had `T >= T_identity`
- raw p `0.695`
- Holm-adjusted p `1.000`
- about `99.6%` of literal token slots changed token identity

Even global redistribution of the already-produced occupancy-signature inventory across manuscripts and lines is not required to retain comparable R1 under the tested control.

## H72-FI — final complete-token inventory is sufficient under the tested allocation controls

### Result

**SUPPORTED UNDER THE PREREGISTERED LABEL.**

Frozen aggregate classification:

> `FINAL_COMPLETE_TOKEN_INVENTORY_SUFFICIENT_UNDER_TESTED_FI_CONTROLS`

Representation-level clarification:

> The R1 information retained by that complete-token inventory is carried through its multiset of parsed 12-slot occupied/empty signatures. FI is therefore strongest as a test of **occupancy-pattern allocation sufficiency**, not literal lexical identity sufficiency.

## Integrated scientific revision caused by Issue #72

Issue #68 showed that published Naibbe can reproduce the replicated R1 topology very well, but did not identify which aspect of the mechanism mattered.

Issue #72 now separates the resemblance into three responsibility layers:

1. **State-dependent emitted-value association matters strongly upstream.** Breaking EL, ES or EG changes the parsed occupancy grammar and produces large R1 losses.
2. **Exact local plaintext order does not matter detectably under PT.** Destroying local source sequence while retaining linewise composition and rerunning the complete pipeline leaves R1 essentially unchanged.
3. **Final placement of already-existing occupancy signatures does not matter detectably under FI.** Relocating almost every finished token instance, even globally across manuscripts, leaves R1 typical of or slightly above the original allocation.

The best current localization is therefore:

> **R1 primarily constrains the corpus-level distribution and residual dependency topology of 12-slot occupied/empty token shapes. It does not currently constrain exact local plaintext sequence or the observed placement of those shapes.**

A representation-correct causal picture is:

`source composition / encoder state opportunities`

`        ↓`

`state-dependent emitted-value mapping`

`        ↓`

`surface token strings`

`        ↓  SlotParser(min)`

`12-slot occupancy-signature inventory + 66-edge residual topology   <-- R1`

`        ↓`

`token sequence / line / manuscript allocation                       <-- no detected extra R1 requirement`

## Consequence for future inverse mechanism search

R1 should no longer be credited as evidence that a candidate reproduces Voynich syntax, literal token spellings, paragraph logic, document layout, or source-language sequence merely because its residual graph matches.

Its direct role is:

> **Does the candidate mechanism naturally generate the correct family and corpus-level distribution of 12-slot occupied/empty token shapes, including the replicated 66-edge residual dependency topology?**

Literal glyph identity, token spelling, recurrence, paragraph-entry behavior, sequence organization and reversibility remain independent responsibilities.

This also clarifies why Naibbe's R1 success does not rescue its overall Issue #68 status: Naibbe remains `NOT COMPETITIVE` because it fails R2, R3 and R4.

## New falsifiable frontier

The next useful step should decompose the occupancy inventory itself rather than continue perturbing token placement or local plaintext order.

Primary question:

> **What is the minimal within-token occupancy-generation rule needed to reproduce the replicated R1 residual topology?**

A defensible hierarchy should distinguish, prospectively and without using selected observed edges as tuning targets:

1. **independent-slot marginals** — preserve only occupancy frequency of each of the 12 slots;
2. **occupancy-count / shape-size structure** — additionally preserve how many slots a token occupies;
3. **lower-order occupancy-pattern families** — preserve broad pattern classes without preserving the exact empirical signature inventory;
4. **state-dependent construction grammar** — generate occupancy signatures through a compact latent/state rule rather than empirical resampling;
5. **empirical occupancy-inventory resampling** — positive sufficiency control, not a mechanistic explanation.

All models should be evaluated on the complete 66-edge residual vector and, where possible, independent transcription/held-out strata. No model should be allowed to fit the target 66 edges directly and then claim them as validation.

### Falsifying directions

- If independent slot marginals or simple occupied-slot-count models reproduce R1, the residual topology is much less mechanism-specific than currently assumed.
- If those fail but a small generic state-dependent occupancy generator succeeds, R1 identifies a broad morphotactic generator class rather than Naibbe-like codebooks specifically.
- If only empirical occupancy-inventory resampling succeeds, R1 remains a strong descriptive constraint but no compact generative explanation has yet been found.
- If a compact generator also improves independent R2/R3/R4 responsibilities, it becomes materially more interesting than Naibbe itself.

Historical Naibbe use, Latin plaintext and decipherment remain unsupported by Issue #72.
