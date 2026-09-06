# Issue #130 — L4b support-matched edge-table Gate 0

Date: 2026-09-06
Status: **SCORE-FREE / FROZEN BEFORE MATCHED TRANSPORT SCORING**
Parent: Issue #127

## Purpose

Issue #127 L4 found target-calibrated source-table transport B→A only, but B has roughly twice A's source edge observations. Before interpreting that directionality as a Currier-specific identity map, equalize source conditional-table estimation support without using edge outcomes or target scores.

Gate 0 computes no current-initial distribution, probability, likelihood, bits/token, rho, gain or transport result.

## Parent authority

Reproduce the merged Issue #127 score-free Gate0 JSON SHA-256 exactly:

`31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`

Reuse its Phase 3A Currier population, source order, physical-leaf folds and `f57v -> B` authority.

## Source edge events

Use **all visible line-body edge events** in each Currier source regime, matching the training population of the explicit terminal→initial table.

For each line-body current-token locus, define an outcome-blind event identity:

`document | item_id | line_index | token_index | previous_terminal_byte`

The current token's initial byte, token string and any target score are excluded from the identity and from Gate selection.

Group events only by previous-terminal raw-byte class `c`.

## Context-matched support

Let:

- `n_A(c)` = visible A source edge events with previous-terminal class c;
- `n_B(c)` = visible B source edge events with previous-terminal class c.

Use only classes observed in both A and B. For each shared class:

`m_c = min(n_A(c), n_B(c))`.

Thus every matched A and B source table will contain exactly the same number of observations for every retained conditioning context.

Classes unique to one Currier regime are excluded from matched source tables and will use the already-frozen target-POS2 fallback at predictive time.

## Five frozen outcome-blind selections

Freeze seed strings:

- `issue130-match-v1-r0`
- `issue130-match-v1-r1`
- `issue130-match-v1-r2`
- `issue130-match-v1-r3`
- `issue130-match-v1-r4`

For each seed, Currier regime and shared previous-terminal class independently:

1. compute SHA-256 of `seed | regime | previous_terminal | event_identity`;
2. sort ascending by `(hash, event_identity)`;
3. select the first `m_c` events.

The ranking never uses current-initial outcome.

## Gate output

Gate may report only:

- shared/unshared previous-terminal class identities;
- `n_A(c)`, `n_B(c)`, `m_c`;
- total original and matched source-event counts;
- selected event counts by regime/context/seed;
- SHA-256 digest of the sorted selected event identities for each regime/seed;
- fold/document/leaf counts of selected event loci if useful for provenance.

It must not report current-initial outcomes or pair counts for selected samples.

## PASS rule

PASS only if:

1. parent Issue #127 Gate0 authority reproduces exactly and passes;
2. at least two previous-terminal classes are shared;
3. total matched support is >0;
4. for every seed and every shared terminal class, A selected count = B selected count = `m_c`;
5. every regime/seed has the same total matched event count `sum_c m_c`;
6. selection digests are deterministic under an internal repeat check;
7. the score-free firewall remains intact.

Otherwise STOP before matched predictive transport.

## Predictive consequence

After this Gate is merged, L4b may reconstruct the exact selected events, attach their current-initial outcomes only then, train five matched source conditional tables per Currier regime, and repeat only the already-frozen target-calibrated source-table transport test.
