# Issue #184 — S0-R1 canonical occupancy-mask representability preflight

Date: 2026-09-07
Parent: Issue #184 / #172
S0 outcome: `S0_CAPACITY_16PLUS_EXACT`
Status: **ADAPTER-ONLY PREFLIGHT — NO VOYNICH CORPUS / G7A PROBABILITY ACCESS**

## Why S0-R1 is required

S0 established 4,643,467 distinct legal literal surface strings and at least 22 bits/token of support-level capacity. That is enough for an exact reversible code, but S1 aims to ask a stronger question: can reversible distribution matching reproduce the **G7A occupancy-shape law** under the exact current R2 adapter?

The current R2 adapter does not score an abstract structural path. It reparses the emitted literal string with `SlotParser(min)`. Because some literal strings have multiple legal slot parses, a structural occupancy mask is usable for exact G7A distribution matching only if at least one literal surface has that mask as its canonical `min` parse.

S0-R1 checks this representation fact before reading any G7A probability or Voynich corpus.

## Frozen population

All 4,095 non-empty occupancy masks over the 12 frozen slots.

For each mask:

1. enumerate the Cartesian product of the frozen values in the occupied slots;
2. concatenate values in slot order;
3. parse the literal surface with the unchanged `SlotParser(min)`;
4. retain the lexicographically smallest literal surface whose canonical `min` signature equals the requested mask;
5. if none exists after exhausting the mask's entire value product, mark the mask `NO_CANONICAL_SURFACE`.

No observed token, token frequency, G7A/V2 probability or complete-66 edge enters this search.

## Hard gate

`S0R1_FULL_CANONICAL_MASK_COVERAGE` requires **4095/4095** masks to have a canonical literal representative.

The gate is intentionally exact. G7A uses smoothing and defines a complete shape distribution; silently deleting masks after seeing their target probabilities would create a new distribution.

If any mask lacks a canonical representative:

- classify `S0R1_PARTIAL_CANONICAL_MASK_COVERAGE`;
- do not run the planned exact-G7A distribution matcher;
- record the missing masks;
- any later renormalized/canonical-language matcher is a separately specified control, not an in-place repair.

## Outputs allowed

- mask count 4095;
- represented/missing counts;
- deterministic mask→surface table;
- search-trial counts;
- representative literal-length distribution;
- parser closure assertion;
- SHA-256 of the table/result.

Must assert:

- `voynich_corpus_accessed = false`;
- `g7a_probabilities_accessed = false`;
- `r2_scientific_score_computed = false`.

No #179 or R1–R8 candidate score is licensed by this preflight.
