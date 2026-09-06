# Issue #84 Phase B — cipher-family map for the Voynich inter-token regime

Status: **PREREGISTERED — NO PHASE-B CANDIDATE OUTPUT HAS BEEN SCORED**

Parent: Issue #84. Base authority: Issue #84 Phase A (`PLAN_A.md`, `REPORT_A.md`, `first-reveal/phase84a_results.json`) and the project-wide `research/RESEARCH_PROTOCOL.md`.

This plan is frozen before `phase84b.py` exists and before any Phase-B candidate output is scored.

## 1. Question

> Which bounded reversible cipher-operation families, applied to the already frozen CREMMA medieval-Latin source panel, can move an ordinary-language token sequence into the **same inter-token regime** as the seven independent Voynich readings?

This is a mechanism-family screen, not a decipherment attempt. The object is the transformation of token-to-token statistics. A Phase-B hit says that a frozen transform can reproduce the measured regime from Latin; it does not identify the historical mechanism, plaintext, key, semantics, or author.

## 2. Fixed source authority

Plaintext source is exactly the four equal-weight CREMMA manuscripts already used by Phase62/64:

- `BIS193` → `data/BIS-193`
- `CLM13027` → `data/CLM13027`
- `Mazarine915` → `data/Mazarine915`
- `UBL758` → `data/UBL758`

CREMMA authority: `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`.

Parsing is the frozen `phase62b_n0.parse_latin_manuscript` representation. For Phase-B Q1/Q2/Q3 scoring, transformed items are flattened to the same four manuscript-level documents used by the Phase-A `CREMMA_Latin_graphematic` anchor. No source manuscript may be added, removed, reweighted or selected after output is seen.

The Phase-A result authority is `first-reveal/phase84a_results.json`, raw SHA-256 `86d18560b5999836b7c0d22fa9c3d8dbfd9f11ba246613fd0c2527d5ed5ffe1c`. The seven-reading target ranges are computed by the executable from that frozen JSON; they are not re-estimated from Phase-B outputs.

## 3. Primary statistics — unchanged from Phase A

The scorer is imported from `phase84a.py`; no Phase-B copy with altered definitions is allowed.

Primary components:

1. **Q1 adjacent dependence** — null-corrected token mutual information at distance 1 (`MI1`).
2. **Q2 immediate exact-repeat concentration** — z-score for distance bin `1–2` (`z1_2`).
3. **Q2 mid-range exact-repeat concentration** — z-score for distance bin `21–40` (`z21_40`).

Reported but non-decisive:

- Q1 corrected MI at distances 2, 5 and 20;
- Q1b zlib ordering information;
- all other Q2 bins;
- Q3 cross-fitted second-order unit-chain bits/token, bits/unit and OOV;
- token/type counts.

The Phase-A far bins `81–160` and `161–320` are **not** hard Phase-B criteria. Phase A demonstrated that they were confounded by document length and non-discriminating under the chosen document units.

## 4. Target regime — empirical T2 calibration

For each primary component, the Voynich regime is the closed interval spanned by the seven frozen Phase-A readings (`ZL3b`, `IT2a`, `VT0e`, `RF1b`, `GC2a`, `CD2a`, `FG2a`). Exact numeric endpoints are read from the frozen JSON and recorded into the Phase-B result before candidate classification.

Approximate values from the already published Phase-A report, for orientation only:

- `MI1`: about `0.053 … 0.111` bits;
- `z1_2`: about `+2.8 … +8.5`;
- `z21_40`: about `-0.8 … +3.4`.

The executable uses the exact JSON endpoints, not these rounded values.

A value below the Voynich interval is not automatically better. In particular, a memoryless-like transform with `MI1 ≈ 0` does **not** satisfy the Voynich adjacent-dependence responsibility.

## 5. Frozen candidate family

All in-house transforms operate on normalized source units only and use opaque synthetic cipher atoms. Atom labels are arbitrary and are not chosen from Voynich symbols. Source word and line boundaries are preserved unless the candidate explicitly says otherwise.

### P0 — source Latin anchor

Untransformed CREMMA graphematic tokens. Not a cipher and not eligible for a Phase-B cipher hit. It verifies exact replay of the Phase-A CREMMA anchor within Monte-Carlo scoring noise.

### S1 — monoalphabetic substitution

A fixed one-to-one mapping from every observed source unit to one opaque cipher atom, boundaries preserved. This is an invariance control: a bijective relabeling should leave token identity relations unchanged.

Decoder: inverse atom map.

### H2 / H4 / H8 — homophonic substitution

Every source unit receives exactly `k ∈ {2,4,8}` disjoint cipher atoms. Every unit occurrence selects one of its `k` atoms uniformly with a fixed candidate/replicate seed. Word and line boundaries remain unchanged.

Decoder: every homophone maps uniquely back to its source unit.

### N256-1 — deterministic nomenclator/codebook

The 256 most frequent complete source word types in the four-manuscript panel are ranked by `(-count, lexical token tuple)` using **source data only**. Each receives one disjoint whole-word code atom. Other words are encoded by S1.

The number 256 is a frozen pragmatic architecture size, not a target-derived threshold and not a claim about historical table size.

Decoder: code atom → full word for codebook words; otherwise inverse S1.

### N256-4 — homophonic nomenclator/codebook

The same frozen top-256 source types each receive four disjoint whole-word code atoms, chosen uniformly per occurrence by fixed seed. Other words are encoded by S1.

Decoder: each code atom → its source word.

### NULL10 / NULL20 / NULL30 — null insertion

Starting from S1 unit encoding, after each encoded source unit independently insert one null atom with probability `p ∈ {0.10,0.20,0.30}`. The inserted atom is chosen uniformly from four disjoint null symbols. Word and line boundaries are preserved.

Decoder: remove the four declared null atoms, then apply inverse S1.

### TRANS-LINE — line-local token transposition

Start from S1 output. Within every original source line, permute the encoded word-token order using a deterministic Fisher-Yates permutation seeded from the fixed replicate seed plus a stable hash of `(manuscript, item_id, line_index)`. No token crosses a source line. The inverse permutation is retained and exact decoding is required.

This is the one candidate that intentionally changes token order while retaining line locality.

### VERBOSE2 — boundary-preserving verbose recoding

Each source unit maps bijectively to a fixed ordered pair of opaque cipher atoms. Word and line boundaries are preserved. This is a deliberately minimal verbose-code representative and an invariance control for within-token expansion; it does **not** exhaust historical verbose/syllabic systems.

Decoder: each legal atom pair maps uniquely to the source unit.

### NAIBBE — exact published external challenger

Replay the exact published Naibbe v2 mechanism already frozen and audited in Phase64B:

- repository `greshko/naibbe-cipher`;
- commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`;
- `naibbe_v2.py` blob `b566ad82e4b6ff0782ecdddebf77718dac44f292`;
- `references/naibbe_tables.csv` blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`;
- published defaults `RESPACING=17`, 78-card deck, published table weights, `SPACE_REMOVAL_RATE=0.03`, `UNAMBIGUOUS=True`, `MAX_BIGRAM_RETRIES=10000`;
- the Phase64B drop-only interface projection for unsupported medieval Unicode characters remains frozen;
- Phase64B cipher seeds `6480000 + 100*manuscript_index + realization` are reused exactly.

The primary NAIBBE view is the published respaced output. The raw-token view is reported as non-promoting sensitivity only.

Naibbe is explicitly **target-aware at the concrete glyph-codebook level**. A hit is therefore an existence proof for this published architecture, not independent historical evidence for its glyph assignment.

## 6. Replicates and seeds

Deterministic candidates `P0`, `S1`, `N256-1`, `VERBOSE2` are scored once.

Stochastic in-house candidates `H2`, `H4`, `H8`, `N256-4`, `NULL10`, `NULL20`, `NULL30`, `TRANS-LINE` use exactly five fixed replicates.

Master seed formula:

`seed = 8420000 + 100 * candidate_index + replicate`

Candidate indices are frozen in this order:

`H2=1, H4=2, H8=3, N256-4=4, NULL10=5, NULL20=6, NULL30=7, TRANS-LINE=8`.

Naibbe uses the already frozen Phase64B seeds rather than this new formula.

No rerolls, dropped replicates or seed replacement are allowed.

## 7. Reversibility prerequisite

Every in-house cipher candidate must satisfy exact source closure on every generated realization:

`decode(encode(source, key, seed), key, seed) == source`

including original token order and line boundaries.

This is a T1 logical/definitional prerequisite. A closure failure means `IMPLEMENTATION INVALID`; it is not counted as evidence that the scientific cipher family fails.

For Naibbe, Phase B reuses the published external algorithm and Phase64B source interface. Because the published Phase64B primary representation includes cleaning/projection and respacing, Phase B reports its already-declared external reversibility status and does not retrofit a new exact-closure claim to diplomatic CREMMA input.

## 8. Candidate-level summary and classification

For a deterministic candidate, its sole realization is its center.

For a five-realization candidate, the **componentwise median** of the five realizations is its frozen center. The median is used to avoid one stochastic realization dominating the family representative; all five values remain visible.

Define `inside(x, [lo,hi]) := lo ≤ x ≤ hi`.

Three responsibilities:

- `R_MI`: center `MI1` is inside the seven-reading MI1 interval;
- `R_SHORT`: center `z1_2` is inside the seven-reading z1_2 interval;
- `R_MID`: center `z21_40` is inside the seven-reading z21_40 interval.

Classification for a valid reversible in-house candidate or the separately declared external Naibbe candidate:

- **`VOYNICH INTER-TOKEN REGIME HIT`** — all three responsibilities pass;
- **`PARTIAL INTER-TOKEN HIT (2/3)`** — exactly two pass;
- **`PARTIAL INTER-TOKEN HIT (1/3)`** — exactly one passes;
- **`NO INTER-TOKEN HIT`** — none pass.

For every component also report signed distance to the nearest target-interval boundary, zero when inside. Report realization-level values so knife-edge stochastic results are visible. No family is promoted from a near miss by inspecting those realization values.

No weighted omnibus score can override a component failure.

## 9. R1 surface compatibility is deliberately not a generic Phase-B hard gate

Issue #84 asks which cipher families reduce Q1/Q2 into the Voynich regime while keeping R1-compatible surfaces. For generic opaque S1/H/N/NULL/TRANS/VERBOSE outputs, however, R1 depends on an arbitrary choice of surface glyph codebook and on compatibility with the project's 12-slot parser. Treating parser coverage or R1 as a hard family rejection here would transport a representation criterion into a mechanism-family claim without construct validity, contrary to `research/RESEARCH_PROTOCOL.md`.

Therefore Phase B separates two questions:

1. **primary family map:** can the abstract reversible operation create the Voynich inter-token regime from Latin?
2. **surface realization:** only a primary HIT licenses a later, separately preregistered target-independent surface-realization/R1 test.

The sole pre-existing exception is exact published Naibbe, which already has a concrete target-aware Voynich-like codebook and frozen R1 evidence from Issue #68 / Phase64. Phase B annotates that frozen evidence; it does not rescore or generalize it to the whole cipher family.

Thus a generic Phase-B miss means only that the frozen representative does not reproduce the inter-token regime. A hit does not automatically satisfy R1.

## 10. Criterion Validity Table

| Claim / responsibility | Construct | Metric | Direction / threshold | Source | Positive control | Negative/control anchor | Failure meaning | Known blind spots / robustness |
|---|---|---|---|---|---|---|---|---|
| Candidate is a reversible transform under its declared interface | exact closure | equality of decoded source items to original source items | 100% exact | **T1** | identity/S1 toy closure and full-source closure | deliberately corrupted inverse in self-test | implementation/candidate is not validly reversible as implemented | does not establish historical plausibility |
| Voynich-like adjacent token dependence | local sequence dependence at one-token lag | Phase-A corrected `MI1` | center inside exact 7-reading interval | **T2** empirical target variation | seven independent Voynich readings | CREMMA Latin and V2 anchors | candidate does not reproduce this dependence responsibility | tokenization/boundaries can change MI; exact interval endpoints and realization values reported |
| Voynich-like immediate exact repetition | excess exact recurrence within 1–2 tokens | Phase-A Q2 `z1_2` | center inside exact 7-reading interval | **T2** | seven readings | CREMMA Latin and V2 | candidate does not reproduce immediate-repeat concentration | only exact equality, not edit-1 H62 families; later H62 remains distinct |
| Voynich-like suppression of language mid-range burstiness | excess exact recurrence at 21–40 tokens | Phase-A Q2 `z21_40` | center inside exact 7-reading interval | **T2** | seven readings | 101 languages / CREMMA; V2 null-like anchor | candidate retains/creates the wrong mid-range recurrence regime | document definition fixed to four manuscripts; other genres deferred to Phase C |
| Generic surface is R1-compatible | 12-slot parsed residual topology | Issue #68 R1 | **not a Phase-B hard criterion** | — | — | — | no family rejection licensed here | surface-codebook dependent; requires a separate preregistered realization test |

## 11. Required controls and self-tests before target scoring

The executable must fail before candidate scoring if any of these fail:

1. CREMMA git HEAD equals the frozen commit.
2. Phase-A result SHA-256 equals the frozen digest.
3. The seven target labels exist and produce non-empty, finite intervals.
4. Re-scored P0 matches the committed Phase-A CREMMA anchor to numerical Monte-Carlo tolerance on deterministic observables and to expected stochastic tolerance on Q1/Q2 null-derived values; exact observed repeat rates/type counts must match.
5. S1 and VERBOSE2 preserve the complete source token equality relation matrix in a deterministic sample; H2 demonstrates valid homophone decoding; TRANS-LINE inverse restores exact line order.
6. Every in-house full-source realization passes exact decode closure before its Q1/Q2 score is accepted.
7. Naibbe repository head and relevant blobs equal the frozen Phase64B authority.

Any necessary compatibility amendment caused by an execution/interface error must be committed and described before the first successful full Phase-B result is inspected. No scientific statistic, candidate family, parameter grid, interval, seed or classification rule may change in such an amendment.

## 12. Interpretation matrix

- At least one **target-independent in-house HIT**: that operation family becomes a live reversible mechanism class for a separately frozen surface/R1 challenge and later joint R1/S1/S2/H62 testing.
- Only **Naibbe HIT**: meaningful-text encryption remains an existence proof in the target-aware published architecture, but the codebook-dependence caveat remains; do not infer historical identity.
- Only partial hits: identify which responsibility each family can and cannot supply; do not combine them post hoc in Phase B.
- No hits: the tested common cipher operations do not by themselves map Latin into the measured Voynich inter-token regime. This rejects these frozen representatives, **not all possible ciphers**. Phase C genre controls and separately justified residual cipher architectures remain live.

## 13. Prohibited

- changing the seven-reading target intervals after seeing a candidate;
- accepting values merely because they are "lower than language" when they fall below Voynich;
- tuning homophone counts, nomenclator size, null rate, transposition window, verbose expansion or Naibbe parameters to target values;
- adding a new cipher family after seeing which responsibility the frozen set misses;
- averaging the three primary responsibilities into one score that hides a miss;
- inventing a Voynich-like glyph mapping for generic candidates before the primary family map is revealed;
- using the invalidated Phase-A far bins as a decisive Phase-B discriminator;
- claiming plaintext, meaning, historical mechanism, or decipherment from a Phase-B hit.
