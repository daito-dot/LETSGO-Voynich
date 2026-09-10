# Issue #221 — S1 exact reversible distribution matching under frozen V2

Date: 2026-09-10  
Parent: #172  
Predecessor: #184 / RC-A0 S0  
Role: **CONTROL / TARGET-AWARE UPPER BOUND**  
Status: **PREREGISTERED PLAN — NO S1 TARGET FIT OR R2 SCORE MAY PRECEDE MERGE**

## 1. Question

Can an exact information-lossless encoder carry an independently chosen compressed plaintext bitstream while constraining its emitted Voynich-like tokens to a finite-block approximation of the already-frozen OGH-C V2 probability law, closely enough to retain the current #172 R2 token-internal complete-66 topology?

A positive result is an engineered upper bound only. It cannot identify a historical mechanism, plaintext, semantics, language/cipher family, or decipherment.

## 2. Chronology / authority

This plan must be merged before any S1 target-side V2 fit, Hamilton composition, candidate corpus, or new R2 score is computed.

Pre-existing authorities only:

- #184 S0 result: `S0_CAPACITY_16PLUS_EXACT`; 4,643,467 distinct literal surfaces; 4,621,471 single-parse literal surfaces.
- frozen parser/value inventory: `experiments/issue26-music/issue26e_core.py`, `SlotParser(min)`, `SLOTS`.
- frozen memoryless content grammar: `experiments/occupancy-generation-hierarchy/ogh_c.py:V2Model`; second-order `(prev2, prev) -> next` unit chain with V1 backoff and `BACKOFF=1.0` inherited from `ogh_b.py`.
- frozen R2 replay statistic: OGH-A / Issue #75 complete-66 scorer and gates from `experiments/occupancy-generation-hierarchy/PLAN_A.md`.
- frozen skeleton sizes: ZL3b 25,071 accepted tokens; IT2a 28,280 accepted tokens.

No #179 score is licensed.

## 3. External plaintext / compression P0

Plaintext is independent of Voynich:

- repository: `karpathy/char-rnn`;
- path: `data/tinyshakespeare/input.txt`;
- pinned commit: `370cbcd448eb7daf32f21a6be560b70e0b33c4e3`;
- Git blob SHA-1: `7dcb3a2d4cc3b48b6283dd46870bfeb78f88aac9`;
- byte size: `1,115,394`.

P0 is target-blind and must run before T0. It fetches exactly that pinned blob, verifies the Git blob identity/size, computes plaintext SHA-256, then compresses the exact bytes with Python `zlib.compress(data, level=9)`.

P0 must archive before T0:

- plaintext SHA-256 and bytes;
- compressed SHA-256, bytes, bits;
- Python version;
- `zlib.ZLIB_VERSION` and `zlib.ZLIB_RUNTIME_VERSION`;
- the exact compressed payload, or an immutable byte-identical artifact reference.

That compressed byte sequence becomes the only S1 payload. No compressor/level/source substitution is permitted after target reveal.

## 4. Target probability law T0

Use one global target law only:

1. load the canonical ZL3b population through the unchanged OGH-C loader;
2. retain all `SlotParser(min)`-accepted token unit sequences;
3. fit one global `ogh_c.V2Model` to all accepted ZL3b tokens;
4. do **not** fit a separate IT2a V2 law.

This is intentionally maximally target-aware and must be charged as such under R10. It is an upper-bound control, not a prospective historical model.

### 4.1 Literal-surface alphabet

Enumerate every non-empty 12-slot structural sequence exactly as in #184. Group structural sequences by concatenated literal surface.

For S1, define `U1` as only literal surfaces having exactly one structural sequence. The exclusion rule is fixed from the target-blind S0 ambiguity audit; no V2 probability is consulted to decide exclusion.

For each `s in U1`, its target mass is exactly `V2.prob(unique_unit_sequence(s))`. Let raw unique-surface mass be `C = sum_s q_raw(s)`. Require the probability over **all** structural sequences to sum to 1 within `1e-10`, then normalize `q(s)=q_raw(s)/C` on `U1`.

Report excluded ambiguous-surface mass `1-C`. Gate: `1-C <= 0.05`.

No observed Voynich token-type list is used as an alphabet or codebook.

## 5. Frozen finite blocks

Two predetermined evaluation arms are used because the accepted-token skeleton sizes are already frozen by the historical scorer:

- primary ZL3b arm: `B_Z = 25,071` tokens;
- reading-transport IT2a arm: `B_I = 28,280` tokens.

Both use the same ZL3b-fitted `q`. The only arm-specific operation is deterministic quantization to the pre-existing denominator `B` and placement into the corresponding frozen line skeleton. IT2a token content/probabilities may not fit the matcher.

There is no search over block length.

## 6. Hamilton composition

For each arm independently, but from the same `q`:

1. compute `a_s = B*q(s)`;
2. set `n_s = floor(a_s)`;
3. let `R = B - sum_s n_s`;
4. add one count to the `R` surfaces with largest fractional remainder `a_s-floor(a_s)`;
5. ties are resolved by Python Unicode/code-point lexicographic order of the literal surface.

The resulting composition is `p_B(s)=n_s/B` and exactly sums to 1.

Before R2 interpretation report:

- total variation `TV(p_B,q) = 0.5*sum |p_B-q|`;
- Jensen-Shannon divergence in bits, with zero terms handled by continuity;
- shape-marginal TV after mapping surfaces to their unique 12-bit occupied-slot signature;
- nonzero composition support;
- excluded ambiguous mass.

Frozen fidelity gate for **each** arm: `TV(p_B,q) <= 0.05`. If either arm fails, classification is `S1_DISTRIBUTION_FIDELITY_FAIL` and an R2 pass cannot rescue it.

## 7. Exact CCDM code

Let the nonzero composition, ordered by literal surface lexicographically, be counts `n_0...n_{m-1}` with sum `B`.

The type-class size is exact integer

`M = B! / product_i n_i!`.

Payload bits per block:

`K = floor(log2 M)` and `N=2^K`.

Report `M`, `K`, and engineered payload rate `K/B` bits/token. This is not an estimate of manuscript information rate.

### 7.1 Rank spread

For input integer `x in [0,N)`, map to the type-class lexicographic rank

`r(x) = floor(((2*x + 1) * M) / (2*N))`.

Because `N <= M < 2N`, this map is injective and spreads the used ranks across the complete type class instead of taking a lexicographic prefix.

Inverse from a valid used rank is fixed as

`x = floor(((2*r + 1) * N) / (2*M))`,

followed by the mandatory assertion `r(x) == r`. Any failure is `S1_REVERSIBILITY_FAIL`.

### 7.2 Multiset ranking / unranking

Use exact-integer lexicographic multiset-permutation ranking/unranking. At a state with `t` remaining symbols, type-class count `M_t`, and candidate symbol count `c_i`, the branch size is exactly

`M_t * c_i / t`.

No floating point may enter rank/unrank. A Fenwick tree or equivalent exact cumulative-count structure is permitted only as an implementation acceleration; it must not alter ordering.

Synthetic preflight must exhaustively close multiple toy compositions before any target candidate output is scored.

## 8. Full external-payload framing / decoder closure

For each arm separately, form

`FRAME = uint64_be(L) || compressed_bits || 1 || 0...0`

where `L` is the exact compressed payload length in bits and zero padding extends the frame to a multiple of that arm's `K`.

Encode every K-bit frame block through the CCDM map. Every output block therefore has the same frozen composition.

Decoder must:

1. recover each type-class rank from the literal token block;
2. recover each K-bit integer exactly;
3. reconstruct `FRAME`;
4. read `L` and the compressed payload;
5. assert the next bit is `1` and all remaining padding bits are `0`;
6. reproduce the P0 compressed SHA-256 byte-for-byte;
7. `zlib.decompress` and reproduce the pinned plaintext SHA-256/bytes byte-for-byte.

Any failure is `S1_REVERSIBILITY_FAIL` and dominates all structural scores.

## 9. R2 evaluation block

Only **block 0** from each arm is used for R2. There is no block selection: every full block has exactly the same token composition.

Place block-0 tokens sequentially into the corresponding frozen OGH-A line skeleton, preserving only line lengths/order/folds. Parse emitted strings with unchanged `SlotParser(min)`.

Reuse the OGH-A / Issue #75 scorer unchanged except the responsibility label is current #172 R2:

- candidate-owned reference nulls: 1,000 within-line independent slot shuffles;
- disjoint candidate-owned test nulls: 1,000;
- existence: `valid_folds >= 4`, `W >= 0.50`, `p_exist <= 0.01`;
- for **both** frozen target readings: Pearson `r >= 0.70`, maxT `p_r <= 0.01`, sign agreement `>= 50/66`, maxT `p_sign <= 0.01`.

Primary arm is the ZL3b skeleton. IT2a is a transport replication using the same ZL3b-derived target law. No individual edge may be inspected to change the encoder.

Null seed namespaces must be frozen in the executable before the first R2 run and start with `ISSUE221:S1:`. The CCDM itself is deterministic and has no stochastic seed.

## 10. Frozen outcome logic

Evaluate in this order:

1. `S1_INVALID` — authority/hash/probability-sum/scorer/invariant failure.
2. `S1_REVERSIBILITY_FAIL` — any exact rank, compressed-stream, delimiter/padding, decompression, or plaintext closure fails.
3. `S1_DISTRIBUTION_FIDELITY_FAIL` — excluded ambiguous mass >0.05 or either arm TV >0.05.
4. `S1_EXACT_DISTRIBUTION_MATCH_R2_REPLICATED` — exact closure/fidelity and frozen R2 pass on both skeleton arms.
5. `S1_EXACT_DISTRIBUTION_MATCH_R2_PRIMARY_ONLY` — exact closure/fidelity; ZL3b arm passes R2; IT2a transport arm fails.
6. `S1_EXACT_DISTRIBUTION_MATCH_R2_FAIL` — exact closure/fidelity; primary ZL3b arm fails R2.

No weighted aggregate may override these classes.

## 11. Target-access / complexity declaration

S1 is deliberately target-aware:

- full frozen 12-slot surface constraint: yes;
- all accepted ZL3b token content to fit one global V2: yes;
- target-derived V2 transition probabilities: yes;
- frozen ZL3b/IT2a layout skeletons: yes;
- target complete-66 vectors: scorer only, not encoder fitting;
- empirical token vocabulary lookup: no;
- IT2a content fit: no;
- Currier/section/folio/scribe labels: no;
- paragraph-entry/line-edge/slow-history target information: no;
- candidate-specific local repair after reveal: prohibited.

Algorithmic complexity is the fixed V2 model + deterministic Hamilton composition + exact CCDM ranker. The large generated codebook is implicit; no empirical dictionary is stored.

## 12. Interpretation firewall / stopping rule

A positive S1 would establish a narrow existence result: **exact reversible payload transport can coexist not only with the frozen support constraint but with a close finite-block approximation to the known token-internal V2 law and its R2 topology.**

It would not establish that Voynich uses CCDM or any reversible code. Because the encoder is explicitly supplied with the target-derived V2 law, R10 cost is high and historical promotion is forbidden.

S1 does not test R1 or R3-R8. Do not add cross-token memory to this issue. Do not score #179. Do not alter the target law, ambiguity rule, plaintext, compression, block sizes, quantizer, rank map, R2 scorer, or gates after reveal.

If S1 passes, close this upper-bound lane and return #172 to independently motivated mechanism discrimination. If it fails, record whether failure is reversibility, distribution approximation, or R2; no in-phase rescue.
