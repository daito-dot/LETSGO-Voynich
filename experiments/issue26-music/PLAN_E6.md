# Issue #26E6 — fully refitted structured-null architecture audit

Status: **FROZEN BEFORE E6 EXECUTABLE / SCIENTIFIC REVEAL**

Issue: #26

Base main: `21ca553d0dc7f5e203465d08ae606b4c43305817`

## Motivation

E5 corrected the interpretation of E2-C by giving each comparator lattice its own ZL discovery→freeze→IT transfer path. That showed that the striking fixed-map transfer was not selection-adjusted evidence for Guidonian specificity.

One positive-looking result still remains: the original E / E2-B **architecture-level** comparison, where Guidonian and ordinary degree-matched nulls were each allowed full per-fold training freedom (all `6! = 720` state↔column permutations plus optimal 20-cluster↔20-row assignment) and Guidonian showed a held-out advantage in both ZL and IT2a.

E6 asks whether that remaining advantage survives against the stronger non-musical structures frozen in E3 when **every candidate is fully refitted independently on every training fold**.

## Frozen question

> Under the exact E/E2 architecture and full per-fold mapping freedom, does the Guidonian 20×6 lattice outperform non-musical lattices that preserve much more of its six-state overlap geometry, on held-out ZL and independently maintained IT2a transcriptions?

This is a specificity test, not a decipherment test.

## Frozen data and representation

Use the existing `issue26e_core.py` implementation unchanged:

- ZL3b source blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`;
- IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- Zattera 12-slot parser;
- six-state slot10 channel `EMPTY,d,l,r,m,n`;
- residual one-hot morphology from slots `0..9,11`;
- deterministic sequence-blind `k=20` clustering on unique training token types;
- exact five frozen physical-leaf folds;
- held-out allowed-occurrence accuracy.

Parser policies:

- primary: `min` earliest-valid;
- preregistered sensitivity: `max` latest-valid.

No fixed state→vox map is used in E6.

## Candidate families

### Guidonian target

Use `issue26e_core.GUIDO` unchanged.

### Family S — E3 structured nulls

Reuse the frozen `E3_STRUCTURED_NULLS.json` catalog (SHA-256 `3ded6745d58701d1a1c38a38f268c57396afffbbbf0a681ec9b16bb09f1e47bd`).

Each of its 100 non-Guidonian lattices preserves:

- 20 rows;
- row-degree multiset `1×4, 2×10, 3×6`;
- all six column degrees = 7;
- 42 allowed cells;
- the Guidonian **pair-overlap histogram**.

It does not preserve the labeled 6×6 pair-intersection matrix.

### Family X — exhaustive exact-pair alternatives

Reuse `E3_EXACT_PAIR_ALTERNATIVES.json` (SHA-256 `652e23fa08701a87e0aaab961f4a267f2389ccc19769eb31ed05e651c2bedfaf`).

The catalog exhaustively contains exactly four feasible row-neighborhood multisets having the complete labeled Guidonian 6×6 pair-intersection matrix: Guidonian plus exactly three non-Guidonian alternatives.

These three alternatives are the decisive test of structure beyond second-order pair geometry.

## Full per-fold fitting

For every dataset (`ZL`, `IT`), parser policy (`min`, `max`), fold, and candidate lattice independently:

1. fit the `k=20` morphology clusters on training leaves only;
2. form training count matrix `C[20,6]`;
3. call the unchanged E mapping procedure `fit_mapping(C, lattice)`:
   - enumerate all `720` six-state↔column permutations;
   - for each permutation fit the optimal one-to-one 20-cluster↔20-row assignment;
   - choose the training optimum with frozen lexical tie-breaks;
4. freeze that fold-specific mapping;
5. score the same held-out leaves.

Thus Guidonian, every structured null, and every exact-pair alternative receive **identical adaptation freedom**.

No mapping, parser choice, cluster assignment, or topology is transferred between ZL and IT in the primary architecture-level test.

## Replay firewall

Before accepting E6 comparisons, Guidonian must replay the already revealed architecture-level results within `1e-12`:

### ZL
- `min` mean accuracy: `0.8509664380470466`
- `max` mean accuracy: `0.8439032769036159`

### IT2a
- `min` mean accuracy: `0.8512154779726009`
- `max` mean accuracy: `0.8404723923113318`

The IT full-precision constants were recovered from the first-reveal E2 Actions job log (`99378839395`) before the E6 executable existed.

## Statistics

For each dataset/policy:

- `A_G` = mean Guidonian held-out accuracy across five folds;
- for each structured lattice j, `A_S[j]` = its mean held-out accuracy across the same five folds;
- empirical `p_S = (1 + #{j: A_S[j] >= A_G - EPS}) / 101`;
- report structured median, q95, maximum, Guidonian-minus-median, and per-fold comparisons;
- for each of the three exact-pair alternatives, report its mean and fold accuracies and Guidonian-minus-alternative.

No multiple-testing correction is needed between the three exact alternatives for the decisive gate because the requirement is conjunctive: Guidonian must beat **all** of them.

## Frozen primary decision

The primary (`min`) classification is:

### `GUIDONIAN SPECIFICITY SURVIVES FULL REFIT`
Only if **all** of the following hold:

1. ZL structured family: `p_S <= 0.05` and `A_G > median(A_S)`;
2. IT structured family: `p_S <= 0.05` and `A_G > median(A_S)`;
3. on ZL, Guidonian mean accuracy is strictly greater than each of the three exact-pair alternatives;
4. on IT, Guidonian mean accuracy is strictly greater than each of the three exact-pair alternatives.

### `PAIR GEOMETRY / GENERIC STRUCTURE SUFFICIENT UNDER FULL REFIT`
If either exact-pair condition (3 or 4) fails, regardless of structured-family p-values.

### `STRUCTURED NULLS EXPLAIN ARCHITECTURE EFFECT`
If both exact-pair conditions happen to pass but either structured-family gate (1 or 2) fails.

## Max-policy sensitivity

Repeat the complete comparison under `max`.

This is descriptive robustness only and cannot rescue a failed primary classification. Report whether the primary qualitative conclusion repeats.

## Interpretation boundary

A failure of Guidonian specificity means:

> the positive E/E2-A/B architecture-level performance does not require the historical Guidonian higher-order lattice once comparators preserve the relevant six-state overlap geometry and receive the same full fitting freedom.

It does **not** prove that no manuscript content can concern music.

A survival result would still establish only an unusual structural compatibility with the Guidonian lattice, not literal pitches, melody, rhythm, mode, or plaintext.

## Chronology and merge policy

This plan must be committed before `phaseE6_refit_structured_null.py` exists and before any E6 scientific score is computed.

E6 remains on a dedicated branch/draft PR. Do not merge to `main` without explicit user authorization.
