# Issue #68 Stage 0 — pre-target authority corrections

Status: **CORRECTION RECORD — BEFORE ANY ISSUE #68 TARGET SCORE**

This addendum preserves two source/audit corrections discovered while implementing the preregistered `STAGE0_PLAN.md`.

They are not candidate-performance-driven changes. At the time of these corrections:

- no Issue #68 `PLAN_A.md` target plan had been accepted;
- no Issue #68 target executable existed;
- no new R1/R2/R3 joint candidate score had been computed;
- no Issue #68 first-reveal candidate result existed.

The original Stage-0 plan remains the historical preregistration and is not rewritten to hide these corrections.

## Correction A — Naibbe authority and decoder role

Earlier Stage-0 orchestration used the wrong table path `sixteentables.csv` and incorrectly described the pinned published Naibbe repository as lacking an explicit decoder.

The frozen Phase64B source authority already records the correct table path:

- repository: `greshko/naibbe-cipher`
- pinned commit: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`
- encoder: `naibbe_v2.py`, blob `b566ad82e4b6ff0782ecdddebf77718dac44f292`
- table: `references/naibbe_tables.csv`, blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`

Direct inspection of that same pinned commit also confirms:

- decoder: `decrypt_naibbe.py`, blob `b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b`;
- it constructs reverse unigram/prefix/suffix mappings from `references/naibbe_tables.csv`;
- it emits alternatives for ambiguous parses and `[?]` for unresolved tokens;
- it attempts compound-token splits for ciphertext tokens affected by spacing.

Therefore the correct tournament role is:

> **published target-aware cipher / decoder challenger**

This does **not** imply exact recovery of the original source text. The published encoder removes original plaintext spaces/punctuation, normalizes `W→UU`, `J→I`, `K→C`, randomly segments the normalized stream into one- or two-character units, and in the primary published configuration removes 3% of ciphertext spaces.

Accordingly the fair closure target is the **normalized plaintext letter stream**, with ambiguity/unresolved output and information loss reported explicitly. Original orthography and word-boundary recovery are not free successes, and no hidden boundary/orthography side information may be supplied.

## Correction B — C0 structured reversibility

Earlier Stage-0 commentary incorrectly stated that `C0-4_digraph` destroys source token boundaries and therefore requires boundary side information.

Current authoritative Phase62C code shows the opposite:

- `transform_items` preserves item → line → token hierarchy;
- `C0-4_digraph` groups units only **inside each existing token**;
- each grouped atom uses the injective length-delimited `encoded_atom` representation;
- odd final units are explicitly marked with `S`, paired units with `D`.

Therefore C0-4 is exactly invertible back to the represented source token structure without external boundary side information.

The corrected Stage-0 audit includes a synthetic structured round-trip test for every frozen C0 transform and must fail if exact recovery does not hold.

## Scientific consequence

Both corrections strengthen the fairness of the reversible side of the tournament rather than selectively weakening a candidate after seeing target results:

- C0 receives the exact-reversible status its implementation warrants;
- Naibbe receives explicit decoder eligibility while retaining its genuine preprocessing/information-loss limitations.

Neither correction changes R1, R2, R3, their frozen historical values, their source populations, their folds, or any future target threshold.
