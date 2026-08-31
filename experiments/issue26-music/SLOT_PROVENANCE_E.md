# Issue #26E — slot provenance and parser-reconstruction boundary

Status: **FROZEN BEFORE ISSUE26E EXECUTABLE / SCIENTIFIC REVEAL**

## What is and is not recovered

The current public `main` does not contain the original Phase01–02 slot parser. The public archive begins materially later, and `experiments/ARCHIVE_STATUS.md` explicitly records that some historical raw/source material remained dependent on the earlier local workspace.

Legacy project artifacts retained outside current GitHub do establish the historical representation used by the project:

- tokens were parsed against the **12-position Zattera slot inventory**;
- ambiguous legal assignments were summarized by **earliest-valid (`min`)** and **latest-valid (`max`)** policies;
- historical pilot coverage was about 85% of token occurrences;
- recorded signatures include `0-8-9-10` for `dain/daiin/sain...`, `4-8-10` for `chol/chor/...`, and the examples listed below.

The original parser source itself has **not** been recovered from current GitHub. Therefore Issue26E must not claim to replay the historical implementation.

## Fresh implementation authority

Issue26E will implement a new parser directly from the published Zattera 12-slot table summarized by the Voynich.nu word-paradigm reference to Zattera (2022):

| slot | non-empty values |
|---:|---|
| 0 | `q`, `s`, `d` |
| 1 | `o`, `y` |
| 2 | `l`, `r` |
| 3 | `t`, `k`, `p`, `f` |
| 4 | `ch`, `sh` |
| 5 | `cth`, `ckh`, `cph`, `cfh` |
| 6 | `e`, `ee`, `eee` |
| 7 | `s`, `d` |
| 8 | `o`, `a` |
| 9 | `i`, `ii`, `iii` |
| 10 | `d`, `l`, `r`, `m`, `n` |
| 11 | `y` |

Every slot may be empty. A legal single-unit parse is a concatenation of at most one non-empty value from each slot in strictly increasing slot order, covering the complete normalized token.

All legal parses are enumerated.

- `min` = lexicographically smallest tuple of occupied slot indices;
- `max` = lexicographically largest tuple of occupied slot indices.

The parser is intentionally limited to **one legal slot unit per visible token**. Earlier work found that this is not universal, especially in pharmaceutical labels where multiple legal units may concatenate. Issue26E therefore tests a narrower single-unit-parsed population and must report coverage; it may not interpret excluded tokens as evidence for or against music.

## Historical-signature validation gate

Before any Issue26E scientific statistic is emitted, the fresh parser must reproduce all of these previously recorded examples exactly:

| form | expected `min` signature | expected `max` signature |
|---|---|---|
| `otedy` | `1-3-6-7-11` | `1-3-6-10-11` |
| `okal` | `1-3-8-10` | `1-3-8-10` |
| `okol` | `1-3-8-10` | `1-3-8-10` |
| `otchdy` | `1-3-4-7-11` | `1-3-4-10-11` |
| `qokedy` | `0-1-3-6-7-11` | `0-1-3-6-10-11` |
| `chedy` | `4-6-7-11` | `4-6-10-11` |
| `y` | `1` | `11` |
| `d` | `0` | `10` |
| `dain` | `0-8-9-10` | `0-8-9-10` |
| `daiin` | `0-8-9-10` | `0-8-9-10` |

If any assertion fails, Issue26E stops before scientific evaluation. Fixing the parser after seeing a scientific outcome requires a new experiment label.

## Why slot 10 is eligible for a six-state music test

Including the empty state, Zattera slot 10 has exactly six states:

`EMPTY, d, l, r, m, n`

This cardinality is a property of the independently published slot inventory, not something selected after inspecting musical sequence statistics. That makes it eligible for one narrow test against the six Guidonian `voces` (`ut re mi fa sol la`).

No claim is made here that slot 10 *is* a solmization syllable channel. That is the hypothesis to be tested.
