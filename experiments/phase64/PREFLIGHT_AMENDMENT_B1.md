# Phase 64B preflight amendment B1 — external codebook row count

Status: **recorded before any ZL3b/CREMMA Phase64B scientific metric is computed**.

The first non-scientific preflight run `33336415410` failed after successfully verifying the pinned external repository/hash and compiling the adapter.

The failure was a project-side static assertion:

`len(placeholder_to_glyph) == 6 * 3 * 26`

That equality is not required by the frozen scientific design. What the design requires is that every published `(state, table, alphabet-letter)` cell used by `naibbe_v2.py` exists and that the exact pinned CSV/hash is loaded. The CSV may contain additional rows that the external module retains in its ambiguity data structures.

No Voynich or CREMMA scientific source was checked out/read in the failed preflight, and no S1/S2/S3/H62 metric was computed.

B1 therefore changes only the adapter validation:

1. require all `3 × 6 × 26 = 468` source-defined placeholder codes to exist;
2. retain any additional pinned CSV entries exactly as the published module loads them;
3. report total loaded mapping entries and extra-code count diagnostically;
4. keep the frozen **reachable normal-input cells = 3 × 6 × 23 = 414** complexity charge unchanged;
5. do not change cipher behavior, defaults, permutation cells, seeds, scorecards or pass/fail rules.

The official Phase64B first-reveal entrypoint is `phase64b_science.py`, which implements this corrected source-validation rule while reusing the already committed adapter functions unchanged.
