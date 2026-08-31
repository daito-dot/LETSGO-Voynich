# Issue26E17A — Friderici 8×3 triadic/motif plaintext probe

Status: **COMPLETED — `NO READABLE FRIDERICI 8x3 PLAINTEXT`**

## Question

E16 tested Friderici's pure-rhythm ternary construction and was negative. E17A moved to Friderici's separate 8×3 construction: eight tones or tone-groups, each repeated one, two, or three times, producing a 24-letter alphabet.

The Voynich side was restricted before reveal to the exact pre-existing Zattera products that can supply those cardinalities without learned clustering:

- 8-state motif axis: one of slot0/slot6/slot9 (four states including `EMPTY`) crossed with the unique binary slot11 (`EMPTY/y`);
- 3-state repetition axis: one of slot1/slot2/slot4/slot7/slot8;
- 15 candidate representations total.

Every fold could fit only an 8-row permutation and a 3-column permutation onto the frozen historical table.

## Provenance

- E16 parent/report head: `7810d01060e75e2324e774b5cba05137bfe8d8f3`
- plan-first commit: `8598f9b8dd03ba496a15368db750392b2607af5e`
- executable commit: `1c8124bce9b63472e402b570ea877505cb6cf14f`
- workflow/reveal head: `aadb9738b8ae746d0e7e63fcb437c61eb44ccbb4`
- Actions run: `33392298329`
- job: `99488545642`
- artifact: `9758219285`
- raw JSON SHA-256: `d092b2fc8908272e4bad6bc8f7fdf086eb881b4f0f4e5fa5dbcc3e5023bae42a`
- artifact ZIP SHA-256: `b2b65d1481c3fd18211b54eb7bd8a0d95b2130114678864fa37d7b1542208f98`.

The workflow verified the plan-before-executable boundary, exact frozen ZL3b mirror commit/blob, and frozen CREMMA commit before execution.

## Historical model

The frozen normalized Friderici grid was:

```text
a b c
d e f
g h i
k l m
n o p
q r s
t u w
x y z
```

The row selects one of eight motifs/tone-groups. The column selects repetition count 1/2/3. This is an exploratory later historical mechanism: Friderici's publication is 1685 and therefore substantially postdates the usual Voynich production window.

No historical row, letter, repetition count, Voynich slot family, or search cardinality was changed after reveal.

## Solver validation

The structured product solver passed the mandatory positive control completely.

Across 12 deterministic hidden Friderici product keys × 5 held-out folds:

- exact hidden row+column key recovery: **60/60**;
- minimum held-out decoded-character accuracy: **1.000**;
- mean accuracy: **1.000**;
- maximum recovered-vs-true held CE difference: **0.0**;
- maximum accepted-move verification discrepancy: `1.03e-13`.

Thus the Voynich negative cannot be attributed to failure of the frozen solver on the model family it was asked to recover.

## Frozen Latin baseline

Under the same frozen CREMMA source/normalization:

- five-fold Latin self CE: **`2.4515716158 bits/char`**;
- pooled Latin top-five-character fraction: **`.5102175496`**.

## Primary `min` population

- visible tokens: **32,570**;
- parsed carrier tokens: **25,071**;
- parse coverage: **`.7697574455`**;
- scoring runs: **5,634**.

The parse-coverage gate therefore passed.

## Primary held-out result

Frozen classification:

> **`NO READABLE FRIDERICI 8x3 PLAINTEXT`**

Pooled held-out diagnostics:

- CE: **`4.5099204585 bits/char`**;
- excess over Latin self baseline: about **`+2.05835 bits/char`**;
- decoded top-five-character fraction: **`.7523034582`**;
- excess over Latin top-five fraction: about **`+.24209`**;
- distinct exact CREMMA substrings length >=6: **0**;
- folds with a >=6 exact substring: **0/5**;
- exact complete-key recurrence: **3/5**.

All substantive Stage-A plaintext gates failed. Only the parse-coverage gate passed.

### Frozen gate table

| gate | result |
|---|---|
| exact complete key recurrence >=4/5 | **FAIL** (`3/5`) |
| held CE <= Latin + .50 | **FAIL** |
| top-five <= Latin + .15 | **FAIL** |
| >=10 distinct CREMMA substrings length >=6 | **FAIL** (`0`) |
| >=6 hits across >=3 folds | **FAIL** (`0/5`) |
| parse coverage >=.70 | **PASS** (`.7698`) |

## Fold behavior

The nominal modal key used:

- four-state slot: **6** (`EMPTY/e/ee/eee`);
- repetition slot: **7** (`EMPTY/s/d`);
- row permutation: `[2,6,1,7,0,4,3,5]`;
- column permutation: `[2,0,1]`.

It recurred exactly in folds 0, 3 and 4.

Fold 2 selected the same slot pair and column permutation but changed the final two row assignments; fold 1 selected a different representation (slot9 × slot11 with slot8). This is why representation-level recurrence is visually stronger than exact-key recurrence, but the preregistered complete-key gate remains 3/5 and fails.

Held CE by fold ranged from approximately `4.463` to `4.579`, all far from the Latin baseline.

Representative decoded runs are collapse-heavy, for example:

- `hiiiifiiziiii`
- `iwiiwiiiiiwiiiii`
- `iawihiiiiiihihiiiiiiiifiif`
- `wiiiiiiiiiiwiiiwii`.

The pooled character concentration quantifies the same failure rather than relying on visual reading.

## `max` sensitivity

The alternative parser policy does not rescue the mechanism.

- exact complete-key recurrence: **4/5**;
- pooled held CE: **`4.4931699841`**;
- top-five-character fraction: **`.9031151530`**;
- distinct >=6 CREMMA substrings: **0**.

Although recurrence reaches 4/5 under `max`, the decoded alphabet collapses much more severely and the absolute language/readability gates remain strongly negative. The plan explicitly prohibited `max` from promoting a primary failure.

## Stage-B decision

E17B is **not authorized**.

The preregistered Stage-B null/historical-table specificity audit was conditional on E17A passing every Stage-A lead condition. It did not. Running additional refitted nulls or alternative 8×3 tables now would be a rescue of an absolute plaintext failure rather than a confirmatory follow-up.

## Interpretation

This result weakens the tested Friderici 8×3 product-code mechanism on the exact natural Voynich representations available under the adopted slot grammar.

The useful negative is stronger than a simple optimizer failure:

- the historical product cipher is fully recoverable under synthetic controls;
- Voynich supplies exact natural 8-state and 3-state product candidates without learned clustering;
- yet held-out decoded output remains far from medieval Latin, strongly character-collapsed, lexically empty, and not fully key-stable.

The 3/5 modal-key recurrence and the 4/5 reuse of the slot6×slot11 / slot7 representation are retained only as numerical diagnostics. They are not music-cipher evidence, especially because the `max` sensitivity selects a different representation and is even more collapsed.

Do not rescue E17 with learned state merging, different slot products, section-specific keys, variable repetition semantics, token edits, respacing, or a modified Friderici alphabet.

No merge to `main` is authorized.
