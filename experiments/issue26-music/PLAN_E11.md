# Issue #26E11 — Öttingen-Wallerstein 5×5 music-cipher plaintext probe

Status: **FROZEN BEFORE E11 EXECUTABLE / REVEAL**

Parent research state: Issue26E8 branch at `343afac73da2e52b3a75f69e0a43257d54bdf952`.

## Purpose

E10 found an intriguing 4/5 recurrent fitted key under the Sloane 351 5×5 probe, but the decoded output collapsed to `concon...` and was decisively non-Latin. A future non-musical slot3×slot5 audit has been retained separately.

E11 continues the user's requested music-cipher exploration while explicitly testing whether the E10 recurrence was a **local optimum of the 5×5 decoder family** rather than anything specific to Sloane.

Question:

> If a historically attested but independently structured 5×5 musical Polybius cipher is applied to the same two natural five-state Voynich factors under the same training/held-out protocol, does readable Latin emerge, and does the optimizer again converge stably to a low-diversity mapping?

E11 is exploratory. It is **not historical-origin evidence**, because the source is ca. 1600, later than the Voynich manuscript's usual dating window.

## Historical cipher frozen before reveal

Source family: Friedrich von Öttingen-Wallerstein, *Steganographia comitis*, ca. 1600. The Herzog August Bibliothek transcription gives the 5×5 angel table with row/column solfège coordinates. The concealed instruction says that the two notes identify the angel and the **third letter of the angel's name** is the plaintext letter.

External source records used for reconstruction:

- HAB manuscript/transcription: Cod. Guelf. 56 Aug. 4°, especially the transcribed angel table;
- David Løberg Code, “Can musical encryption be both? A survey of music-based ciphers,” *Cryptologia* 47(4), 2023, DOI `10.1080/01611194.2021.2021565`;
- Western Michigan historical cipher reconstruction as secondary check.

Using the HAB transcription, the plaintext cell table in its documented row/column order is frozen as:

```text
q r s t u
w x y z l
 a b c d e
l m n o p
f g h i k
```

More precisely, rows correspond to the transcribed row solfège order `ut, sol, fa, mi, re` and columns to `ut, fa, sol, mi, re`:

- row `ut`: `q r s t u`
- row `sol`: `w x y z l`
- row `fa`: `a b c d e`
- row `mi`: `l m n o p`
- row `re`: `f g h i k`

The second `l` comes from the intentionally superfluous `Lalalala` cell noted in the historical discussion. Thus the table has 25 musical cells but only 24 distinct plaintext letters; `j` is absent and `u/v` are not distinguished under the Latin normalization used in prior probes.

No cell contents may be changed after reveal.

## Voynich representation

Reuse the unchanged Zattera parser, exact ZL3b input, physical-leaf folds, and frozen CREMMA medieval-Latin corpus used in E9/E10.

Exactly two adopted Zattera slots have five raw states including EMPTY:

- slot3: `EMPTY,t,k,p,f`
- slot5: `EMPTY,cth,ckh,cph,cfh`

Each parsed Voynich token therefore supplies one ordered pair of 5-state values.

Primary parser: `min`. `max` is sensitivity only.

## Analysis engine / comparability with E10

E11 must reuse the **exact E10 language-model/search engine** from scientific head `39eebc9f3fc1085e506a0b55ed86e43c83dbc579`, with only the historical 5×5 plaintext TABLE replaced by the frozen Öttingen table above and output labels changed.

This preserves:

- CREMMA normalization (`j→i`, `v→u`);
- character 4-gram model and alpha `0.1`;
- five physical-leaf folds;
- 2 axis assignments × 120 row permutations × 120 column permutations = **28,800 keys/fold**;
- training-only key selection;
- held-out decoding and diagnostics;
- literal Track A conventions;
- top-five-character concentration and exact lexicon-hit diagnostics.

The E10 engine is a fixed implementation dependency, not a source of E10 results.

## Track A — literal/canonical application

As in E10, report four deterministic unfitted conventions:

- slot3=row, slot5=column; documented order;
- slot3=row, slot5=column; reversed column order;
- slot5=row, slot3=column; documented order;
- slot5=row, slot3=column; reversed column order.

No language-driven fitting.

## Track B — exhaustive training-only alignment

For each fold, evaluate all 28,800 row/column/axis keys on 4/5 Voynich leaves under the external medieval-Latin 4-gram model. Select the lowest training cross-entropy with deterministic tie-breaking inherited from E10. Freeze the key and decode the untouched 1/5 leaves.

Record:

- mean and pooled held-out cross-entropy;
- exact full-key recurrence across folds;
- selected raw slot→coordinate mappings;
- top-five-character fraction;
- exact CREMMA lexicon hits length >=6;
- representative held-out streams;
- top 4-grams and their CREMMA counts.

## Primary interpretation gates

Use the same practical readability logic as E10. A plaintext lead requires all of:

1. exact fitted key recurrence >=4/5;
2. pooled held-out CE <= Latin self-baseline + `0.50 bits/char`;
3. at least 10 distinct exact CREMMA lexicon hits length >=6;
4. top-five-character fraction <0.80.

If any fails: **`NO READABLE OETTINGEN PLAINTEXT`**.

## Local-optimum diagnostic fixed before reveal

Regardless of plaintext classification, compare E11 descriptively with E10.

Flag **`5X5 LOCAL-OPTIMUM PATTERN REPEATS`** if:

- E11 exact fitted-key recurrence >=4/5;
- E11 plaintext gate fails;
- E11 top-five-character fraction >=0.90;
- and representative output is dominated by repetitive low-diversity fragments rather than coherent lexical sequences.

This does not establish a formal null distribution. It is a mechanistic cross-probe diagnostic indicating that stable keys can recur across different historical 5×5 tables because the optimizer exploits Voynich state imbalance / Latin frequency structure.

## Boundaries

- Do not tune the Öttingen table to Voynich.
- Do not reinterpret the later date as Voynich-origin evidence.
- Do not promote key recurrence alone as decryption evidence.
- Do not use E11 to erase or rescue E10.
- Keep the non-musical slot3×slot5 residual question on backlog while the music-cipher branch continues.
- No claim of decipherment without independently replicated coherent multi-folio plaintext.
- Keep this branch separate from main unless the user explicitly authorizes integration.
