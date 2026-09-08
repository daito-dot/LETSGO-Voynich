# Issue #203 — Dee plaintext→cipher R5 source attribution preregistration

Date: 2026-09-08  
Parent: #172  
Follows: #181, #182, #196, #198  
State: **FROZEN BEFORE DEE EDGE REVEAL**

## Scientific question

Using the exact source-space, physical-line, plaintext-boundary and 1:1 plaintext/cipher alignment frozen in #198, determine whether the previous-terminal → next-initial edge is line-local on true lexical boundaries, and whether that topology is already present in solved plaintext or appears only in ciphertext.

This is an external historical source-attribution test. It does not score Voynich and cannot by itself promote the Dee system as a Voynich candidate.

## Input authority

Gate 0 final class: `COMPOSABLE_AND_STAGE1_SUPPORT_LICENSED`.

Frozen inputs:

- `experiments/issue198-dee-gate0/issue198_gate0_event_ledger.csv`
  - SHA-256 `362bcd4a4edbbc5e93559b11a2e495ee71e897bdb97b28f1802b8a9df647edd5`
- `experiments/issue198-dee-gate0/issue198_gate0_final.json`
- public author `dee.xlsx`
  - SHA-256 `c339aeac63da1b81560e63b02abb807a187a4003d3df44ebf389d3934055605d`
- frozen 1,099-character cipher stream
  - SHA-256 `3e0aab0f59160896fa8fdf088c7ee15af2c9bad1eced404f8ed7b6d020a56446`
- frozen 1,099-character plaintext stream
  - SHA-256 `21458f41a44a4ec45938f84bd6c341b0e695bb9f8b2c6fb3afee14bea61d4c27`

No Stage-1 normalization may change any of these identities.

## Frozen primary population

Primary events are `LEXICAL_BOUNDARY` only.

- same physical line: `147` events;
- cross physical line before page treatment: `26` events;
- page/folio transition line `18 → 19`: excluded before scoring to preserve #181's `no cross-page carry` rule;
- primary cross-line lexical population after that exclusion: `25` events;
- #198 `UNALIGNED_OR_AMBIGUOUS`: always excluded;
- `WITHIN_WORD_SPLIT`: excluded from the primary score.

The page exclusion is an observed layout fact and is not score-dependent.

## Pair definition

For each frozen boundary at author-sheet offset `k`:

- `X = stream[k-1]`;
- `Y = stream[k]`.

The plaintext and ciphertext use exactly the same event IDs, physical-relation labels and folds.

## Five-fold split

Because this source has only two manuscript pages, the #181 page-modulo split is impossible. The frozen line-grouped analogue is:

`fold = (right_physical_line - 1) mod 5`

All events predicting an atom on the same physical line therefore share one held-out fold.

Every primary fold must contain nonzero same-line and cross-line train/test support. Failure is `INVALID`; no alternative fold assignment is permitted after reveal.

## Frozen likelihood factor

The statistic is the #181 first-symbol factor with no hyperparameter search:

- additive smoothing: `alpha = 0.01`;
- vocabulary: complete character inventory of the corresponding frozen 1,099-character stream, fixed before folds are scored;
- baseline: `POS(Y)` fit on the training events of that physical-relation population;
- edge model: `EDGE(Y|X)` fit on exactly the same training events;
- held-out gain per event: `log2 P_EDGE(Y|X) - log2 P_POS(Y)`;
- fold value: mean held-out gain in bits/event.

For each of plaintext and ciphertext:

- `G_line`: primary same-line lexical-boundary gain;
- `G_cross`: primary cross-line lexical-boundary gain.

A quantity passes iff:

1. five-fold mean `> 0`, and
2. at least `4/5` fold means are `> 0`.

This is unchanged from #181.

## Frozen topology labels

Per stream:

- `LINE_LOCAL`: `G_line` PASS, `G_cross` FAIL;
- `EDGE_WITH_CROSS_LINE_CONTINUATION`: both PASS;
- `NO_ROBUST_LINE_EDGE`: both FAIL;
- `CROSS_ONLY_OR_UNSTABLE`: `G_line` FAIL, `G_cross` PASS.

Joint primary class:

- `LINE_LOCAL_PRESENT_BEFORE_AND_AFTER_CIPHER`: plaintext and ciphertext are both `LINE_LOCAL`;
- `CIPHER_STREAM_ONLY_LINE_LOCAL`: only ciphertext is `LINE_LOCAL`;
- `PLAINTEXT_ONLY_LINE_LOCAL`: only plaintext is `LINE_LOCAL`;
- `NO_SHARED_LINE_LOCAL_TOPOLOGY`: neither is `LINE_LOCAL`;
- `INVALID`: authority/hash/event/fold/scorer invariant failure.

## Frozen secondary diagnostics — non-gating

These are reported but cannot alter the primary class.

### Paired transform shift

For identical folds/events:

- `D_line = G_line(ciphertext) - G_line(plaintext)`;
- `D_cross = G_cross(ciphertext) - G_cross(plaintext)`.

Report five fold differences, mean and positive-fold count. No threshold/class is attached.

### All-aligned-boundary replay

Re-run the same scorer on every non-ambiguous `LEXICAL_BOUNDARY + WITHIN_WORD_SPLIT` event, with the same line 18→19 page exclusion. This diagnoses whether mixing physical line-wrap fragments back into the event population changes the raw #181-style topology.

It does not replace the lexical-boundary primary.

### Within-word splits

Report count/location only. No within-word predictive score can become a post-reveal rescue primary.

## Frozen implementation

Scorer:

`experiments/issue203-dee-stage1/issue203_dee_stage1_scorer.py`

Pre-commit source identities:

- scorer SHA-256: `b59b8fdf1e7923a9fd7e5ecdc2f1bae7c5165a14713f2601818533b265849476`
- scorer Git-blob SHA-1: `3210c45883d9949479d379e96540efcb5ff703f4`

The scorer reads XLSX cached values with Python stdlib only; it does not evaluate spreadsheet formulas or invoke Latin/text repair.

Before emitting a Dee result it asserts exact XLSX/stream/ledger hashes, 1,099/1,099 stream lengths, frozen event counts, the line 18→19 page exclusion, unique primary event IDs and nonzero fold support.

## Target-free preflight

A synthetic-only preflight is provided by:

`.github/workflows/issue203-dee-stage1-prereg.yml`

It runs only `--synthetic-preflight`, exercises five-fold smoothed POS/EDGE likelihood paths, and asserts that no Stage-1 result artifact exists in the prereg phase. It reads neither Dee source data nor Voynich data.

## Reveal license

Only after this preregistration/scorer is committed and merged, and the synthetic-only preflight succeeds, may one fixed-source Dee reveal run execute the frozen scorer.

The reveal transport must:

1. check out the exact merged preregistration commit;
2. retrieve `dee.xlsx` and assert its frozen SHA before scoring;
3. use the #198 ledger/final JSON from that exact checkout;
4. emit one result JSON and provenance record;
5. archive the full result SHA before interpretation.

A transport failure before result emission permits only transport repair. Population, page exclusion, folds, alpha, vocabulary rule, pair definition, pass rule and classes cannot change.

## Firewall

Before the preregistration merge there is no authorized Dee edge result.

After reveal, do not:

- change a boundary/alignment/plaintext spelling/cipher correction;
- move the page exclusion;
- change `alpha=0.01`;
- change the five folds;
- subset lines, events or symbols;
- replace lexical-boundary primary with all-boundary or within-word scoring;
- compare to Voynich effect magnitude to reinterpret a failed class;
- infer general cipher-family behavior or decipherment from this one source.
