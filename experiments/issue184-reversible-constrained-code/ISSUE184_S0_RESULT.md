# Issue #184 S0 exact reversible-capacity result

Date: 2026-09-10  
Parent: #172  
Issue: #184  
Working identifier: `RC-A0`  
Role: `CONTROL / TARGET-AWARE UPPER BOUND`

## Classification

**`S0_CAPACITY_16PLUS_EXACT`**

The frozen 12-slot surface language has more than enough distinct literal surfaces for the preregistered 16-bit exhaustive reversible codebook. Every one of the first 65,536 deterministic lexicographic codewords round-trips exactly and is accepted by `SlotParser(min)`.

This is a support-capacity control only. It is not an R2 pass, historical mechanism claim, plaintext claim, or decipherment result.

## Frozen authority used

Only the authority permitted by `research/ISSUE172_REVERSIBLE_CONSTRAINED_CODE_PREFLIGHT_20260907.md` was used:

- 12 ordered slot sets and 33 literal slot values from `experiments/issue26-music/issue26e_core.py`;
- current `issue26e_core.py` Git blob SHA-1: `8bafba7f2bce4cf77c9001c729936c1ce619759b`;
- the existing `SlotParser` concatenation/parsing rule;
- `min` parse for parser-acceptance audit.

No Voynich corpus, token frequencies, empirical vocabulary, G7A/V2 probabilities, Currier/section/folio/scribe metadata, R2 target edges, or R1-R8 scientific score was accessed.

## Exact enumeration

Slot cardinalities:

`[3, 2, 2, 4, 2, 4, 3, 2, 2, 3, 5, 1]`

Analytical structural-path count:

`N_paths = product_s(1 + |SLOTS[s]|) - 1 = 4,665,599`

After concatenating slot values and deduplicating identical literal strings:

- distinct literal surfaces `|U| = 4,643,467`;
- structural collisions `N_paths - |U| = 22,132`;
- surfaces with more than one structural parse: `21,996` (`0.0047369777797494845` of distinct surfaces, about `0.474%`);
- maximum structural parse multiplicity: `4`.

Parse-multiplicity histogram over distinct literal surfaces:

| structural parses | distinct surfaces |
|---:|---:|
| 1 | 4,621,471 |
| 2 | 21,873 |
| 3 | 110 |
| 4 | 13 |

The multiplicity identity closes exactly:

`1*4,621,471 + 2*21,873 + 3*110 + 4*13 = 4,665,599`.

## Capacity

`floor(log2 |U|) = 22`.

Thus the abstract distinct-surface set contains at least `2^22 = 4,194,304` codewords, with a margin of `449,163` surfaces above that threshold. Per the preregistration, S0 does not exhaustively test a 22-bit codebook; it performs the frozen practical S0-16 audit.

## Deterministic S0-16 audit

Codebook definition: first 65,536 strings of sorted distinct set `U` under Python Unicode/code-point lexicographic order.

Results:

- codebook size: `65,536`;
- encode/decode round-trip: `65,536 / 65,536` exact;
- `SlotParser(min)` acceptance: `65,536 / 65,536`;
- codebook newline serialization SHA-256: `2f7f4154508ba70226f6d4ad06b455e1ecd5de2f71d51869f37ef277e10b14c1`.

The parser's pre-existing validation examples also pass unchanged, including ambiguous single-character `d`/`y` and the frozen min/max parses for `otedy`, `qokedy`, `dain`, and `daiin`.

## Deterministic integrity checks

A separate post-run invariant audit verified:

- analytical `N_paths` equals the enumerated multiplicity total;
- parse-multiplicity histogram reconstructs all `4,665,599` paths;
- length-distribution counts sum to `|U|`;
- `2^22 <= |U| < 2^23`;
- the round-trip and parser-acceptance counts both equal the frozen S0-16 population.

Execution-script SHA-256: `e021bcea104f6f031283454ed54dae3f68d1db1683db2ae6d882e8a5e82c7a13`  
Raw result-file SHA-256: `5c2b5d73f36a113639dbf67fc0a36743933df48659e1912d3fc2b239034f2402`  
Canonical result-object SHA-256: `c7a673d20a18ed70b8b4872bc2756dc9fc9e4dcf64e1c5c8883339954bdb0277`

## Required firewall flags

- `voynich_corpus_accessed = false`
- `g7a_v2_probabilities_accessed = false`
- `r1_r8_scientific_score_computed = false`

## Interpretation

This result answers one narrow mathematical question: restrictive Voynich-like token-internal support is not, by itself, incompatible with exact reversible information transport. The frozen surface constraint contains millions of distinct legal literal strings, enough for a deterministic fixed-block code with at least 22 bits of index capacity per abstract token.

That does **not** mean the observed manuscript carries 22 bits/token, nor that its empirical distribution uses this capacity uniformly. The observed compact V2 code length and R2 topology are different questions. S0 was forbidden from using those probabilities or target scores.

Therefore:

- do not promote RC-A0 as a historical mechanism;
- do not count this as R2 PASS;
- do not infer plaintext or semantics;
- do not automatically proceed to the conditional S1 distribution-matching experiment.

Any S1 requires an explicit roadmap revision and a separately frozen plan under the existing #184/#172 firewall.
