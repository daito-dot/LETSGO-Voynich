# Phase 64B preflight amendment B2 — exact reachable Naibbe codebook

Status: **recorded before any ZL3b/CREMMA Phase64B scientific metric is computed**.

Inspection-only B2 Actions run `33336527081` / job `99324310521` loaded the exact pinned external Naibbe commit and printed codebook occupancy. It did not check out or read ZL3b or CREMMA scientific sources.

## Exact external finding

Pinned `naibbe_tables.csv` / `naibbe_v2.py` loads exactly **414 mapping entries**.

The apparent 468-cell grid (`3 states × 6 tables × 26 letters`) differs only because the external codebook intentionally has no cells for `j`, `k`, or `w`:

- `clean_line()` maps `j -> i`;
- `clean_line()` maps `k -> c`;
- `clean_line()` maps `w -> uu`.

Therefore those 54 cells (`3 states × 6 tables × 3 normalized-away letters`) are unreachable by normal input and are absent from the pinned published CSV.

B2 verified:

- loaded entries: **414**;
- effective grid: `3 × 6 × 23 = 414`;
- effective present: **414/414**;
- effective missing: **0**;
- extra entries outside the effective grid: **0**;
- per state: unigram `138/138`, prefix `138/138`, suffix `138/138`.

## Frozen correction

The official first-reveal entrypoint must therefore require:

`set(placeholder_to_glyph) == {state_table_letter for 3 states × 6 tables × 23 EFFECTIVE_LETTERS}`

exactly.

It must **not** synthesize the 54 normalized-away `j/k/w` cells and must not pad or alter the external codebook.

The complexity charge remains exactly **414 reachable codebook cells**, as already intended in `C1_SOURCE_AUDIT_B.md` and `PLAN_B.md`.

## Computational-only implementation clarification

The mapping-permutation control in `PLAN_B.md` requires only the primary published-output view. The paired raw-token sensitivity is required for the published mapping, not for each permutation.

Before first reveal, the official entrypoint is therefore allowed to skip raw-token score computation for permutation mappings while still:

1. running the exact published encryption;
2. calling `respace_line()` on every nonempty line;
3. preserving the exact cipher RNG stream;
4. scoring the primary respaced output identically.

This removes redundant computation only. It does not change any candidate output, seed, mapping, metric, aggregation, threshold, or frozen classification rule.

## Stdout firewall

Importing the pinned external module emits a diagnostic line (`Total ambiguity retries: ...`) on stdout. To keep the first-reveal artifact valid JSON, the official entrypoint must capture stdout produced by external loading/execution and print the final JSON only after scientific computation finishes.

Captured external stdout is diagnostic only and cannot affect scoring.

## Chronology

- failed preflight `33336415410`: project-side 468-length assumption exposed; no science read;
- failed B1 preflight: still required nonexistent normalized-away cells; no science read;
- inspection B2 `33336527081`: exact 414-cell external occupancy established; no science read;
- this amendment freezes the exact correction before any first scientific reveal.
