# Issue26E11C — STA-family León-style substitution test

Status: **FROZEN BEFORE E11C EXECUTABLE / SCIENTIFIC REVEAL**

E11C follows `HISTORICAL_AUDIT_E11.md` and the completed non-scientific source audit `REPORT_E11B.md`.

## Question

Does the early-medieval León-style mechanism become readable Latin if externally defined STA visual families are treated as allographic cipher-sign classes under one manuscript-wide one-to-one substitution?

This is a strong representation test, not a claim that an STA family is the true Voynich character.

## Frozen Voynich source

Use only the official ZL3b STA1 file frozen by E11B:

- `https://www.voynich.nu/data/sta/ZL3b.txt`
- header `#=IVTFF STA1 2.0 M 5`
- SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`
- 472861 bytes.

Use running-text loci whose kind contains `P`. Resolve bracketed alternatives by first reading. Text interruption `<->` breaks a sequence. Other IVTFF markup is removed. Certain and uncertain spaces remain token boundaries for readability diagnostics but are ignored by character-language scoring. No sequence crosses a physical-line/interruption boundary.

Each STA code is two ASCII characters. The primary cipher symbol is its first uppercase family letter. The externally observed family set is fixed as:

`A B C D E F G H J K L M N P Q R S T U V W X Z`

There are exactly 23 families. No family may be deleted, merged, or split after reveal.

Physical folds use sorted numeric physical leaf numbers from the folio identifiers, assigned round-robin to five folds.

## Latin and solver

Reuse the exact CREMMA medieval-Latin population and the symmetric physical-line character 4-gram model frozen in E11 / `PLAN_E11_AMENDMENT.md`: lowercase ASCII, `j→i`, `v→u`, 24-letter alphabet `abcdefghiklmnopqrstuvwxyz`, additive smoothing alpha=.1.

A key injectively maps the 23 STA families to 23 distinct Latin letters, leaving one Latin letter unused.

Reuse the already-frozen E11 optimization procedure and budget: 16 deterministic restarts, 30000 pair-swap proposals per restart, geometric temperature .05→.00005, then exhaustive steepest pair-swap descent. Use new seed namespace `Issue26E11C:STAFamilyMonoSub:v1:{fold}:{restart}`. Key fitting sees only 4/5 Voynich leaves; the remaining 1/5 is untouched.

## Mandatory positive control

Before interpreting Voynich, build a known Latin monoalphabetic substitution control of the same 23-symbol dimensionality and approximately the same event volume. Use the 23 most frequent frozen Latin letters, a single deterministic hidden bijection to the 23 STA family labels (`Issue26E11C:PositiveKey:v1`), and the identical solver/folds.

The solver is adequate only if:

- recovered held-out CE is within .05 bits/char of true-key held-out CE; and
- mean occurrence-weighted key accuracy is at least .95.

Otherwise classify `SOLVER INADEQUATE`; do not call Voynich negative.

## Held-out diagnostics

Record per fold and pooled:

- training and held-out CE;
- family→letter mapping and unused Latin letter;
- character frequencies and top-five fraction;
- first 20 decoded held-out runs with original token spaces;
- exact whole-token CREMMA lexicon hits, especially distinct hits length >=6;
- top decoded 4-grams with CREMMA counts;
- exact and occurrence-weighted key stability across folds.

No manual respacing, key choice, spelling changes, anagrams, or folio cherry-picking.

## Frozen classification

First require the positive control.

`STA-FAMILY LEON-LIKE PLAINTEXT LEAD` only if all hold:

1. pooled held-out CE <= Latin self-baseline + .50 bits/char;
2. occurrence-weighted key stability >= .90;
3. identical 23-family key recurs in >=3/5 folds;
4. pooled top-five-character fraction <= Latin baseline + .15 absolute;
5. at least 10 distinct exact whole-token CREMMA hits length >=6 across at least 3 folds.

If CE passes but stability fails: `LATIN-LIKE BUT KEY-UNSTABLE`.

If both stability gates pass but language/readability gates fail: `STABLE NON-LANGUAGE OPTIMUM`.

Otherwise, with an adequate solver: `NO READABLE STA-FAMILY LEON-LIKE PLAINTEXT`.

## Boundary

A negative E11C rejects only the family-normalized strict substitution representation. It does not reject distinct STA family members, historically attested homophony, nulls/polygraphs, non-Latin plaintext, or musical content. Any more flexible model requires separate preregistration.

Keep E11C on the dedicated Issue26 research branch. Do not merge to main without explicit user authorization.
