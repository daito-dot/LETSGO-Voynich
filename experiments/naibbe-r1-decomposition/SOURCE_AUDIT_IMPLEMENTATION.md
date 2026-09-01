# Issue #72 Stage A — support-pilot implementation freeze

Status: **FROZEN BEFORE SOURCE-AUDIT EXECUTABLE AND BEFORE ANY COUNTERFACTUAL R1 SCORE**

These pilots exist only to test whether proposed causal interventions are mechanically valid, deterministic and representation-supported. Their R1 complete-graph statistics are forbidden in Stage A.

The later target `PLAN_A.md` may retain, reject or refine an axis based only on the predeclared support/invariant evidence from Stage A, never on R1 performance.

## Common authority

- published Naibbe commit and codebook fixed in `SOURCE_AUDIT_PLAN.md`;
- published primary realization-0 encryption seed per manuscript remains `6480000 + 100*manuscript_index`;
- unchanged `SlotParser(min)`;
- support gate `>=0.60` direct parser coverage;
- local intervention RNGs use `random.Random(stable_seed(label))` and **must not consume/change the published encoder's global RNG stream before `encrypt_manuscript` reseeds it**.

`stable_seed(label)` is the existing SHA-256 first-8-byte deterministic convention from the repository.

## P0 — plaintext-order support pilot

For every normalized/effective nonempty source line:

1. obtain the exact Phase64B effective plaintext character string;
2. copy its characters;
3. Fisher-Yates shuffle them with a local RNG label:
   `issue72:P:pilot0:{manuscript}:{item_id}:{line_index}`;
4. assert identical line length and character multiset;
5. feed the shuffled line into the unchanged published Naibbe encoder with the original realization-0 encryption seed.

This destroys within-line plaintext sequence/bigrams while preserving per-line character marginals and all codebook definitions.

Downstream ambiguity retries/deck consumption are allowed to change because they are causal consequences of the changed plaintext order under the published algorithm.

## L0 — global effective-letter association support pilot

Construct one deterministic derangement-like permutation of the 23 effective letters from label:

`issue72:L:pilot0:global-effective-letter-permutation`

using deterministic shuffle; if any fixed points remain, rotate the shuffled list by the smallest positive offset that removes all fixed points, failing if no derangement is found.

Use the **same letter permutation for every table/state**:

`new_map[state,table,letter] = old_map[state,table,perm(letter)]`.

This preserves the glyph multiset inside every table×state pool exactly while breaking the published letter↔glyph association consistently across the codebook.

## S0 — state-allocation support pilot

For every table × effective-letter triplet, rotate published glyph values one step through the frozen state order:

`unigram <- suffix`

`prefix <- unigram`

`suffix <- prefix`

Equivalently each old value moves to the next state in `unigram → prefix → suffix → unigram`.

This preserves each table+letter's exact three-value multiset and the global codebook inventory while destroying published state specialization.

## T0 — table-allocation support pilot

For every state × effective-letter six-tuple, rotate published glyph values one step through the frozen table order:

`alpha → beta1 → beta2 → beta3 → gamma1 → gamma2 → alpha`.

The published table-selection deck weights remain unchanged.

This preserves each state+letter's exact six-value multiset and the global codebook inventory while changing which glyph values receive high/low table-selection probability.

## G0 — global-cell association support pilot

Take the 414 reachable cell instances in exact lexicographic key order over:

`state order × table order × effective-letter order`.

Deterministically shuffle the 414 **cell-instance values** with label:

`issue72:G:pilot0:global-effective-cell-permutation`.

Assign shuffled values back to the same ordered cell keys.

Duplicate glyph strings do not make the operation ambiguous because the permutation acts on cell instances, not unique value labels.

Assert that the complete 414-value multiset is exactly preserved.

## I0 — exact published-output inventory support pilot

This is an explicit upper-bound inventory control and does not call the plaintext encryption lookup.

1. Generate the exact four published primary rep0 Naibbe surfaces already frozen in Issue #68.
2. Flatten **whole published ciphertext tokens** in the frozen manuscript/item/line/token order.
3. Deterministically permute the complete token-instance list with label:
   `issue72:I:pilot0:published-primary-token-instance-permutation`.
4. Refill the exact original line slots in the same order.

This preserves exactly:

- the global published primary ciphertext-token multiset;
- total token count;
- every line's token count;
- every item/manuscript line layout;
- direct parser coverage globally.

It destroys token-to-plaintext, token-to-item and token-to-line association except for coincidental reassignment.

Because complete token inventory is held exact, I0 is **not** a neutral historical null. It is a deliberate upper-bound test of whether R1 is already carried by the emitted token inventory plus line-local allocation/null structure.

## Stage-A support output only

For P0/L0/S0/T0/G0/I0 report only:

- deterministic surface SHA-256;
- visible/accepted token counts and direct parser coverage;
- generation completion;
- ambiguity retry count/diagnostics where encryption is used;
- claimed invariant checks;
- no pair/occupancy association values.

The audit executable must not import/call real-surface Q/residual scoring functions.
