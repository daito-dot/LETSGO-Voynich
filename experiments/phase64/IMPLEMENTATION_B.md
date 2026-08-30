# Phase 64B implementation freeze — published Naibbe C1-E0

Status: **frozen before first scientific reveal**.

Normative authorities:

- `C1_SOURCE_AUDIT_B.md`
- `PLAN_B.md`

Executable:

- `phase64b_naibbe.py`

## 1. No external algorithm modification

The executable imports `naibbe_v2.py` from the separately checked-out pinned repository. It calls the published functions directly:

- `clean_line`
- `encrypt_naibbe`
- `respace_line`
- `build_bigram_catalog`

The adapter does not copy or rewrite the encryption algorithm.

Before use it hard-checks:

- external commit;
- `naibbe_v2.py` blob;
- `naibbe_tables.csv` blob;
- README blob;
- published defaults and table/state/alphabet order;
- 78-card weights.

## 2. Ciphertext token representation

Each Naibbe ciphertext word is represented as a tuple of its literal published glyph-string characters, e.g. `qokchdy -> ('q','o','k','c','h','d','y')`.

This is the same character-level representation used for canonical ZL3b tokens in the Phase62 scorecard.

When published 3% space removal concatenates two encrypted words, the concatenated string becomes one longer output token exactly as the published script specifies.

## 3. Line and item preservation

Every source `b.Item` remains one output `b.Item` with the same item ID and manuscript identity.

Every source physical line produces one output physical line. An empty encrypted line is retained as an empty line rather than deleted, so line indices are not shifted by the adapter.

Source word spaces are not preserved because Naibbe's `clean_line()` + `respace_plaintext()` deliberately removes/resegments them.

## 4. RNG pairing

For manuscript index `m` and realization `r`, Python global `random` is seeded exactly once with:

`6480000 + 100*m + r`

The entire manuscript is then processed in source order.

For each nonempty cleaned line:

1. call `encrypt_naibbe`;
2. retain the raw encrypted-token list for sensitivity;
3. call `respace_line` unconditionally;
4. retain the respaced tokens for the primary view.

Thus raw and primary views share exactly the same encryption history, and recording the raw view does not alter later-line RNG consumption.

## 5. Mapping permutation implementation

The published mapping is copied, never destructively edited as authority.

For each frozen permutation seed, a dedicated `random.Random(seed)` shuffles glyph values independently within each state across the 6 tables × 23 reachable normalized plaintext letters.

Unreachable `j/k/w` cells remain unchanged. They remain present in Naibbe's ambiguity catalog exactly as in the published implementation.

After installing a mapping, the adapter recomputes:

- `unigram_glyphs`;
- `bigram_catalog`.

This is necessary because those are module globals used by the published ambiguity-rejection code.

The cipher's global RNG is then seeded independently, so mapping permutation does not consume encryption randomness.

## 6. Score computation order

For each mapping / manuscript / realization / view, compute once:

- S2;
- S3;
- H62-P1 excess profile;
- S1 projection under each of the five frozen Voynich training-fold directions.

Then aggregate:

1. five cipher realizations within manuscript;
2. four manuscripts with equal weight.

For H62, excess vectors `E` are averaged at each level and normalized only after aggregation via the frozen `aggregate_excess` implementation.

For the mapping-permutation control, first form one equal-manuscript aggregate for each of the five mappings, then equal-average the five mapping `E` vectors and scalar metrics.

No paragraph/item is promoted to an independent replication unit.

## 7. Joint exposed relative MSE

The codebook-specificity diagnostic uses:

For each Voynich fold:

`MSE_f = mean_k((candidate_k / heldout_target_{f,k} - 1)^2)`

for `k in {S1,S2,S3}`.

Then:

`joint_relative_MSE = mean_f(MSE_f)`.

This diagnostic is frozen before result and cannot rescue or redefine the primary exposed gate.

## 8. Frozen `PARTIAL` operationalization

`C1-E0 H62 RIVAL TO A1-R1` and `C1-E0 STRUCTURALLY VIABLE` are defined exactly in `PLAN_B.md`.

If neither is met, `C1-E0 PARTIAL` is assigned iff at least one of these predeclared substantive signals holds:

- the full exposed S1/S2/S3 gate passes; or
- the full H62 N0/C0 viability rule passes; or
- mean H62 `D_profile` is lower than the better of N0 and C0; or
- mean H62 `|ΔC_short|` is lower than the better of N0 and C0.

Otherwise classify `C1-E0 NOT COMPETITIVE`.

This rule is committed before first reveal to prevent post-result rhetorical relabeling.

## 9. Raw-token sensitivity

The paired pre-respacing raw view is evaluated with the same full S1/S2/S3 + H62 machinery for diagnosis.

It cannot determine the frozen primary classification and is not included in codebook-specificity rescue logic.

## 10. Character-retention diagnostics

For every manuscript/realization, record:

- source graphematic units entering the adapter;
- characters remaining after published `clean_line()` normalization;
- their ratio;
- nonempty source/cleaned line counts;
- primary/raw ciphertext token counts;
- Naibbe ambiguity retry count.

These diagnostics are descriptive only.

## 11. First-reveal firewall

Before first scientific run:

1. this file and the executable must be committed;
2. a non-scientific preflight may verify external source hashes/defaults and toy encryption only;
3. the science workflow must be committed with read-only repository permissions;
4. no Phase64B score may have been calculated.

After reveal, do not switch to a reuse-enabled Naibbe variant or tune parameters to repair H62.
