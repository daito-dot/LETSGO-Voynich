# Issue26E11E — validated-solver León/STA family substitution re-analysis

Status: **FROZEN BEFORE E11E EXECUTABLE / TARGET RE-ANALYSIS**

Parent solver state: E11D `E11D SOLVER VALIDATED`, recorded at `e7e14388c9407816b6a9d8bccb58e13c34fc1df9`.

## Epistemic status

E11C previously exposed a Voynich target run using a solver that subsequently failed its mandatory synthetic positive control. Its Voynich mapping/output was declared non-authoritative and was not used to tune the validated E11D solver.

E11E is therefore **not a pristine first-ever target reveal**. It is a prospectively specified re-analysis with a solver that was developed and locked behind a Voynich-data firewall, then independently validated 12/12 on known substitutions before this plan.

E11E asks:

> With the now-validated frozen monoalphabetic solver, does the externally defined 23-family STA representation of Voynich yield stable, held-out, readable medieval Latin under a León-style one-to-one substitution?

## Frozen target source and representation

Use only the official ZL3b STA1 source already audited in E11B–E11D:

- `https://www.voynich.nu/data/sta/ZL3b.txt`
- expected header `#=IVTFF STA1 2.0 M 5`
- SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`.

Primary cipher symbol = first uppercase family letter of each two-character STA code.

Frozen family order:

`A B C D E F G H J K L M N P Q R S T U V W X Z`

Exactly 23 families. No deletion, merge, split, or family-member refinement is allowed in E11E.

Parse running-text loci whose kind contains `P`; bracketed alternatives use the first reading; `<->` and physical-line boundaries break character sequences. Certain/uncertain token spaces are retained only for plaintext diagnostics and never crossed by whole-token dictionary matching.

## Reconciled analysis population

E11D source reconciliation established:

- broad source audit: 4,130 running-text lines / 140,589 family events, including `fRos`;
- numerical-leaf five-fold population: **4,119 lines / 140,423 family events**;
- excluded from cross-validation: exactly 11 `fRos` Rosettes lines / 166 events because `fRos` has no numerical physical-leaf ID.

E11E uses only the 4,119 / 140,423 numerical-leaf population for all fitted and held-out metrics. `fRos` is not assigned to an arbitrary fold and is not used for key fitting or primary diagnostics.

Physical folds: sorted numeric physical leaf numbers, round-robin to five folds exactly as E11C.

## Frozen external Latin model

Exactly E11D:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`;
- directories `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`;
- normalization `j→i`, `v→u`;
- 24-letter plaintext alphabet `abcdefghiklmnopqrstuwxyz`;
- additive-smoothed character 4-gram model, alpha `.1`;
- source run boundaries never crossed.

Compute the same five-fold external-Latin self-baseline used by the Issue26 plaintext probes.

## Frozen solver — no target-specific tuning

Use `FREQ-HILL` exactly as frozen in `E11D_SOLVER_FREEZE.md` and validated in `REPORT_E11D_VALIDATION.md`:

1. 23 observed cipher positions + explicit unused plaintext-letter position;
2. frequency-ranked initialization from 4/5 training leaves and frozen external Latin unigrams;
3. deterministic steepest pair-swap descent on the 4-gram training objective;
4. all 276 swaps considered, including unused-letter swaps;
5. accept only improvement >`1e-12`;
6. safety cap 100 accepted swaps;
7. no annealing, restart, randomization, dictionary selection, or held-out appearance used for key choice.

For every fold, independently recompute final training CE with the explicit 24-letter scorer. If discrepancy >`1e-10`, classification is `E11E IMPLEMENTATION FAILURE`.

## Held-out procedure

For each fold:

1. fit the complete 23-family→24-letter injective key on the other four physical-leaf folds only;
2. freeze the key;
3. decode the held-out fold without any update;
4. compute held-out 4-gram CE;
5. retain original Voynich token boundaries for diagnostics only.

Pool held-out decoded streams only after every fold has been independently decoded.

## Frozen key-stability metrics

### Exact key recurrence

The full 24-position key includes all 23 family mappings plus the unused plaintext letter. Count the maximum number of folds sharing an exactly identical full key.

### Occurrence-weighted key stability

Let global target family weights be their frequencies in the fixed 4,119-line / 140,423-event analysis population.

For each of the 10 unordered fold-key pairs, compute the fraction of global family-event mass whose family receives the same plaintext letter in both keys. The primary stability statistic is the arithmetic mean of those 10 weighted agreements.

This definition is fixed before E11E output and operationalizes the E11C phrase “occurrence-weighted key stability”.

## Frozen plaintext diagnostics

Record per fold and pooled:

- training CE and accepted swap count;
- held-out CE and scored-character count;
- full family→letter key and unused letter;
- decoded character counts and top-five-character fraction;
- first 20 held-out physical-line plaintext streams length >=12, capped at 160 chars;
- first 20 held-out tokenized lines with original token spaces;
- all exact whole-token CREMMA lexicon hits length >=4;
- distinct exact whole-token hits length >=6 and folds containing them;
- top 50 decoded 4-grams with frozen CREMMA counts.

No manual respacing, anagramming, Caesar shifts, homophone changes, selective folios, spelling repair, or semantic key choice.

## Frozen classification

First require implementation audit success.

### `STA-FAMILY LEON-LIKE PLAINTEXT LEAD`

Only if all primary gates hold:

1. pooled held-out CE <= Latin self-baseline + `.50 bits/char`;
2. mean pairwise occurrence-weighted key stability >= `.90`;
3. an identical complete key recurs in >=3/5 folds;
4. pooled top-five-character fraction <= Latin baseline + `.15` absolute;
5. at least 10 distinct exact whole-token CREMMA hits length >=6 across at least 3 folds.

This is an exploratory lead, not decipherment. Any lead requires independent follow-up predictions on unused structure or another transcription.

### `LATIN-LIKE BUT KEY-UNSTABLE`

If gate 1 passes but either stability gate 2 or 3 fails.

### `STABLE NON-LANGUAGE OPTIMUM`

If both stability gates 2 and 3 pass but any language/readability gate 1, 4, or 5 fails.

### `NO READABLE STA-FAMILY LEON-LIKE PLAINTEXT`

Otherwise, with implementation audit success.

## Boundaries

A negative rejects only this **23 externally defined STA-family, manuscript-wide monoalphabetic Latin substitution representation**.

It does not reject:

- individual STA member distinctions within a family;
- homophonic substitution;
- nulls;
- polygraphs;
- polyalphabetic/keyed systems;
- non-Latin plaintext;
- non-textual musical/procedural use.

No more flexible León-like model may be introduced as an E11E rescue after reveal. It requires a new hypothesis and new preregistration.

Keep E11E on this dedicated research branch; do not merge to main without explicit user authorization.
