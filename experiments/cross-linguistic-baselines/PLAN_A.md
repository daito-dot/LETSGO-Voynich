# Issue #84 Phase A — cross-linguistic and cross-transcription baselines for the OGH synthesis

Status: **PREREGISTERED — NO PHASE-A VALUE FOR ANY NEW CORPUS REVEALED**

Parent: Issue #84. Exploratory origin: `experiments/occupancy-generation-hierarchy/falsification-probes/` (ZL3b, CREMMA Latin, V2 generator). Those exploratory values are **not** thresholds here.

## 1. Question

> Does any natural language, written as ordinary prose, fall inside the Voynich regime of (Q1) inter-token dependence and (Q2) repeat clustering — and do all independently produced Voynich transcriptions fall inside it?

## 2. Corpora (frozen list; every corpus scored is reported)

**Voynich readings** (voynich.nu IVTFF files, hash-verified at fetch; paragraph loci `P` only; documents = pages):

| label | alphabet | units |
|---|---|---|
| ZL3b | Eva- | EVA letters with frozen composite collapse (`cth ckh cph cfh` → 1 unit; `ch sh` → 1 unit) |
| IT2a | EvaT | same |
| VT0e | EvaT | same |
| RF1b-e | Eva- | same |
| GC2a | v101 | native v101 units (`phase63b_common._native_units`) |
| CD2a | Currier | single characters `[A-Za-z0-9]` |
| FG2a | FSG | single characters `[A-Za-z0-9]` |

Inline tags `<…>`, comments `{…}`, entities `@nnn;`, uncertain markers and non-alphanumerics are removed; tokens split on `.` and whitespace; a token is kept if non-empty after cleaning.

**Natural languages**: the multilingual parallel Bible corpus (`christos-c/bible-corpus`, commit fixed at fetch), every file. For each language, the **first 32,570 tokens of the New Testament in canonical order** (Matthew onwards), documents = chapters. Files with fewer than 32,570 NT tokens are reported as `INSUFFICIENT_SIZE` and excluded from the regime test (not from the report). Tokens: whitespace-split, punctuation stripped, letters/marks kept, lower-cased; `-tok` files are used for Chinese, Japanese, Thai, Vietnamese and the untokenized versions of those four are excluded.

**Anchors**: CREMMA four primary manuscripts (graphematic, files as documents) and the OGH-C memoryless V2 generator in the ZL3b skeleton (rep 0).

## 3. Statistics (frozen)

- **Q1 dependence**: null-corrected mutual information between tokens at distances 1, 2, 5, 20 within documents; null = within-document token shuffle, 20 replicates, seed fixed. Also **Q1b**: compression-based ordering information, `(zlib(shuffled ids) − zlib(original ids)) × 8 / N` bits per token, mean over 5 shuffles.
- **Q2 clustering**: exact-repeat rate `P(∃ d ∈ bin: w_i = w_{i−d})` within documents for bins `1–2, 3–5, 6–10, 11–20, 21–40, 41–80, 81–160, 161–320`; excess over within-document shuffle null (50 replicates) and its z-score.
- **Q3 density** (descriptive only): five-fold cross-fitted second-order unit-chain cross-entropy, bits/token and bits/unit, held-out OOV type rate; folds by document interleave.

## 4. Frozen regime definitions and classification

Voynich regime, per statistic, = the closed interval spanned by the seven Voynich readings.

A natural language is **inside the Voynich regime** iff (i) its Q1 `d=1` corrected MI ≤ the maximum Voynich reading value, **and** (ii) its Q2 excess z-score is ≤ +2 in both far bins (`81–160`, `161–320`).

Classification:

- `NO NATURAL LANGUAGE IN VOYNICH REGIME` — zero qualifying languages.
- `SOME NATURAL LANGUAGES IN VOYNICH REGIME` — list them; the OGH synthesis's "not ordinary language" reading is withdrawn for that set.

Transcription independence:

- `VOYNICH REGIME TRANSCRIPTION-ROBUST` — all seven readings have Q1 `d=1` MI below the minimum language value and non-positive far-bin excess (z ≤ +2).
- `VOYNICH REGIME TRANSCRIPTION-DEPENDENT` — otherwise; name the readings.

Percentile placement of each Voynich reading within the language distribution is reported for Q1, Q2 short-range (bins ≤ 20), Q2 far-range, and Q3; these are descriptive.

## 5. Interpretation boundaries

The Bible is one genre (narrative/religious prose); genre controls are Phase C. Q3 is representation-dependent and is not part of the regime test. No result bears on meaning, plaintext, cipher tables, or decipherment.

## 6. Prohibited

Adding/removing corpora after seeing values; changing bins, nulls, seeds, size rule or regime definitions; using exploratory ZL3b values as thresholds.

## Implementation clarification (2026-09-02, before any full-population value was used)

The first full execution parsed only the 8 Bible files whose `<seg>` attributes use single quotes; 96 files use double quotes and were mis-reported as `NO_NT_MARKER`. The segment regex now accepts both quote styles. No statistic, corpus rule, bin, null or regime definition changed; the 8 scored languages and all Voynich readings are recomputed identically in the rerun. The partial first execution is retained in git history (`first-reveal/` of commit b6c09b1's successor) for transparency and is not used.
