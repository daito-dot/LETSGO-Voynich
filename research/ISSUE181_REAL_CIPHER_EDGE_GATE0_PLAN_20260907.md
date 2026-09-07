# Issue #181 — real historical ciphertext R5 edge: frozen Gate0 plan

Date: 2026-09-07
Parent: Issue #172
Issue: #181
Status: **FROZEN GATE0 / EXTERNAL ONLY — NO VOYNICH TARGET SCORING**

## Scientific question

Does a real historical ciphertext with independently preserved physical lines and cipher-unit boundaries show an immediate terminal-unit → next-initial-symbol predictive edge that is useful within a physical line but not robustly useful across physical line breaks?

This is a calibration of historical ciphertext document behavior. It is not a Voynich candidate score and does not compare external effect magnitude with Voynich.

## External authority

Repository:

- `matthewdgreen/cipher_benchmark`
- pinned commit: `729aad62d12483c549e64a2541d4f9255538c8cf`

Primary source:

- `benchmark/sources/borg/transcriptions/*.canonical.txt`
- creation authority: `scripts/create_borg_benchmark.py`

The benchmark creation code documents MSS Borg.lat.898 as a 17th-century Latin medical/pharmaceutical text encrypted with a monoalphabetic substitution cipher. The diplomatic transcription contains whitespace-separated cipher character groups; the canonical conversion maps each cipher character to one stable `S###` symbol and joins the original groups with literal `|` delimiters while preserving physical source lines.

The canonical conversion skips cleartext-only lines and editorial bracket content before writing the canonical page, so #181 uses the committed canonical files as the external representation authority rather than reinterpreting the manuscript.

## NON-COMPOSABLE external source

Copiale was included provisionally at Issue opening, but Gate0 inspection before any edge scoring established that its canonical files preserve a line-wise `S###` symbol stream without a cipher-unit delimiter corresponding to Borg `|` / Voynich visible-unit boundaries.

Therefore:

> **Copiale = NON-COMPOSABLE for the #181 R5 terminal-unit → initial-unit primary.**

No word segmentation, plaintext alignment, fixed-width grouping, logogram grouping, or learned boundary model may be added to make it composable after this discovery.

Copiale may be used only in a future separately preregistered symbol-stream question.

## Score-free Borg Gate0

Before any edge likelihood is calculated, freeze and report:

1. exact external repository commit;
2. number of committed Borg canonical page files;
3. number of non-empty canonical pages;
4. number of physical non-empty lines;
5. number of cipher-unit groups delimited by `|`;
6. number of same-line adjacent unit pairs;
7. number of cross-line adjacent pairs within page;
8. full `S###` atom inventory;
9. malformed tokens / `UNKNOWN_*` / uncertainty-marked tokens, if any;
10. page support in each frozen fold;
11. same-line and cross-line event support in each fold;
12. firewall assertion that no POS/EDGE likelihood or gain was computed in Gate0.

Any unexpected representation token causes Gate0 to stop as `INVALID_EXTERNAL_REPRESENTATION`; do not silently clean it after seeing scores.

Empty committed canonical files are retained in the audit but contribute no scored events.

## Frozen parser

For each canonical page:

- each non-empty newline-delimited row is one physical source line;
- split a physical line on literal `|` into cipher units;
- strip surrounding ASCII whitespace from each unit;
- every non-empty unit must contain one or more whitespace-separated atoms matching `^S[0-9]{3,4}$`;
- no skip-over adjacency: if a line/unit were invalid, the Gate0 is invalid rather than linking around it;
- a same-line edge exists only between immediately adjacent valid units on the same physical line;
- a cross-line edge exists only between the last unit of physical line `j` and first unit of physical line `j+1` on the same page;
- no cross-page carry.

For every edge:

- `X` = terminal atom of the preceding cipher unit;
- `Y` = initial atom of the following cipher unit.

## Frozen folds

Sort non-empty Borg page IDs lexicographically and assign page index `i` to fold `i mod 5`.

Folds are therefore deterministic, page-disjoint and score-independent.

Gate0 must show every fold contains same-line and cross-line events. If a fold has zero support for either primary event class, classify `INVALID_EXTERNAL_REPRESENTATION` rather than redesign the folds.

## Frozen probability contract

The effect scorer may be implemented only after Gate0 is green and committed.

Use:

- atom vocabulary `V` = all valid `S###` atoms present anywhere in the pinned Borg canonical corpus, fixed before fold scoring;
- additive smoothing `alpha = 0.01`, inherited unchanged from the established R5 common-EVA contract;
- no backoff other than the additive-smoothed table;
- no hyperparameter fitting.

### Same-line identity comparison

For each outer fold:

Training on the other four folds:

- `POS_BODY(Y)`: pooled first-atom distribution over line-body current units, ignoring previous-unit identity;
- `EDGE_BODY(Y|X)`: terminal→initial table for immediately adjacent same-line cipher units.

Held-out gain per same-line edge:

`g_line = log2 P_EDGE_BODY(Y|X) - log2 P_POS_BODY(Y)`

Fold statistic:

`G_line[f] = mean(g_line)`.

### Cross-line identity comparison

Training on the other four folds:

- `POS_LINESTART(Y)`: pooled initial-atom distribution for first units of physical lines that have a preceding physical line on the same page;
- `EDGE_CROSS(Y|X)`: terminal→initial table from last unit of one physical line to first unit of the immediately following physical line on the same page.

Held-out cross-line gain:

`g_cross = log2 P_EDGE_CROSS(Y|X) - log2 P_POS_LINESTART(Y)`

Fold statistic:

`G_cross[f] = mean(g_cross)`.

This factor-only formulation is deliberate: these are exactly the first-symbol factors that distinguish identity-conditioned from position-only models. Shared token-internal factors would cancel in the likelihood difference and are not re-estimated for this external control.

## Frozen pass logic

A quantity `G` passes iff:

- mean across the five held-out folds is `> 0`; and
- at least 4/5 fold values are `> 0`.

No effect-size threshold is added.

Per-corpus classification:

1. `EXTERNAL LINE-LOCAL EDGE` — `G_line` passes and `G_cross` fails.
2. `EXTERNAL EDGE WITH CROSS-LINE CONTINUATION` — both pass.
3. `NO ROBUST EXTERNAL EDGE` — `G_line` fails.
4. `INVALID EXTERNAL REPRESENTATION` — Gate0/support/parser failure.

The opening Issue used the name `G_beyond`; this frozen factor-only implementation names the actually scored cross-boundary identity increment `G_cross`. The scientific distinction is unchanged: whether previous-unit identity has robust incremental value beyond a physical line break.

## Non-gating diagnostics frozen now

After reveal, report without changing class:

- foldwise event counts;
- corpus-global mean/median per-edge gain for same-line and cross-line events;
- first/terminal atom marginal support;
- page-level mean same-line gain distribution;
- line length in cipher units;
- number of distinct previous-terminal contexts represented in each training complement;
- pages containing mixed cleartext according to benchmark metadata if this can be read without changing the canonical population.

Do not subgroup by manuscript location, symbol identity, plaintext word, cipher key mapping or line length to rescue a failed primary.

## Interpretation boundary

A positive Borg result would mean that an actual historical monoalphabetic ciphertext document can exhibit the R5-like qualitative topology in its surface transcription.

It would **not** show that monoalphabetic substitution generates that topology. Borg's transform can preserve source-side dependencies, and its physical grouping/layout may matter. A positive result therefore licenses only a new source-side mechanism question, not a Borg/Voynich candidate reveal.

A negative result does not reject historical ciphers in general; it rejects this particular real historical control as an external example of the topology.

No Voynich data, target likelihood, R1–R10 candidate score or historical-anchor output may be accessed by the #181 external scorer.
