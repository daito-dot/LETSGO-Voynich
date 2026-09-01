# Issue #68 — R1 finite-null ordering freeze

Status: **FROZEN BEFORE TARGET SCORER EXECUTABLE AND BEFORE R1 FIRST REVEAL**

The candidate-owned null is distributionally invariant to arbitrary line ordering, but the finite deterministic 1,000-reference / 1,000-test realization can change if the stable RNG stream is assigned to lines in a different order.

Therefore the exact Naibbe candidate line order is fixed before executable scoring:

1. manuscript order: `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`;
2. within manuscript: the existing `phase62b_n0.parse_latin_manuscript` / `phase64b_naibbe.encrypt_manuscript` item order without re-sorting;
3. within item: emitted line index ascending in existing item order;
4. a line enters the occupancy tensor iff at least one emitted token is accepted by the frozen `SlotParser(min)`;
5. within each line, accepted rows retain emitted token order after simply omitting parser-rejected tokens.

The flat occupancy matrix is exactly `concatenate(line.occ)` in this frozen line order.

The padded line tensor is built in the same order; its row width is the maximum number of **accepted** tokens in any included line, exactly matching the #58B/#58C line-local relocation convention.

No later lexical/item-id sorting is allowed.

Reference/test null seeds remain those already frozen in `IMPLEMENTATION_TARGET.md`.
