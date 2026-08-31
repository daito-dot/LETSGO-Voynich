# Issue #26E11 — León-style musical-glyph substitution probe

Status: **FROZEN BEFORE E11 EXECUTABLE / SCIENTIFIC REVEAL**

Issue: #26
Base research state: Issue26E10 head `ba5f83b67b8ccb25f73b4449b9aaafa04b207513`.
Historical audit: `HISTORICAL_AUDIT_E11.md`.

Pre-executable amendment: the originally drafted `64 × 100,000` annealing budget was reduced to `16 × 30,000` before any E11 executable existed or any E11 score/plaintext was computed. This is a computational-budget change only. The mandatory matched known-cipher positive control remains the authority on whether the reduced solver is adequate; if it fails, E11 is `SOLVER INADEQUATE` rather than a Voynich negative result.

## Question

Early medieval León / Visigothic musical cryptography is not a pitch/rhythm product code. The historically attested core mechanism is alphabetic substitution using neume-shaped or neume-like visible signs, with scribal variation and occasional homophony.

E11 therefore asks a mechanism-level practical question:

> Can the visible Voynich sign stream be decoded by a **single manuscript-wide monoalphabetic substitution key** into medieval Latin, such that a key selected on some physical leaves remains stable and produces Latin-like untouched leaves?

This is deliberately different from E8–E10. No 4-state, 5-state, 6-state, 20-cell, or 25-cell Voynich factor is selected to resemble a historical cipher table.

A positive result would support only a **León-like substitution mechanism class**: musical-looking/graphical signs acting as cipher letters. It would not show that the actual Voynich shapes descend from León signs and would not establish music content.

A negative result weakens the strict one-sign→one-letter version of that historical mechanism. It does not reject every homophonic/polygraphic cipher.

## Historical basis fixed before reveal

Use the source audit already committed in `HISTORICAL_AUDIT_E11.md`:

- Elsa De Luca, “Musical Cryptography and the Early History of the ‘León Antiphoner’,” *Early Music History* 36 (2017), DOI `10.1017/S0261127917000018`;
- Elsa De Luca & John Haines, “Medieval Musical Notes as Cryptography,” DOI `10.4324/9781315267449-2`.

The historical properties relevant here were fixed before E11 code:

- plaintext is ordinary alphabetic text, including Latin examples;
- cipher signs can be genuine neumes or altered/neume-like signs;
- a broad common alphabet exists, but scribal forms vary;
- multiple cipher signs for one plaintext letter can occur in the wider tradition.

E11 tests the **strict monoalphabetic core first** because it is fully identifiable and falsifiable. No degree of homophony is invented post hoc after reveal.

## Frozen Voynich data

Use the same frozen ZL3b source as E/E7–E10:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- expected git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`.

Use paragraphs/physical lines from the same parser used in Issue26E, but **do not use the Zattera slot decomposition for E11 symbols**.

## Frozen visible-grapheme tokenizer

EVA/ZL transliteration uses digraphs/compounds for some visible signs. E11 uses a deterministic, language-blind maximal-munch tokenizer.

At every position in a normalized Voynich token, try the following compounds in this exact order:

`cth, ckh, cph, cfh, ch, sh`

If none matches, emit the next single ASCII letter as one cipher symbol.

Consequences fixed before reveal:

- repeated `e/ee/eee` become repeated `e` cipher-symbol events;
- repeated `i/ii/iii` become repeated `i` events;
- `ch`, `sh`, and the four gallows/bench compounds above are retained as single visible-grapheme classes;
- token boundaries are retained for plaintext inspection and exact-word diagnostics;
- primary character-LM scoring ignores token boundaries but never crosses physical line boundaries or an unparseable/nonalphabetic break.

No grapheme class may be merged/split after seeing E11 plaintext quality and still be called E11.

## External medieval-Latin model

Reuse the exact frozen CREMMA corpus from E8–E10:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`;
- `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`.

Normalize to lowercase ASCII; `j→i`, `v→u`.

The plaintext alphabet is the fixed 24-letter set:

`abcdefghiklmnopqrstuvwxyz`

(i.e. modern a–z with `j` merged into `i` and `v` merged into `u`).

Train an additive-smoothed character 4-gram language model with `alpha=.1` on the frozen external corpus. Physical Latin line/nonletter boundaries break LM runs.

Compute a five-fold external Latin self-baseline exactly as in E10 and additionally record its character-frequency/top-five-character fraction.

## Strict substitution model

Let the E11 tokenizer reveal `M` distinct Voynich cipher-symbol classes. This is a descriptive property of the frozen transcription, not a fitted hyperparameter.

If `M > 24`, strict injection is structurally impossible; report `STRICT MODEL INAPPLICABLE` and do not silently merge glyph classes.

Otherwise a key is an injection:

`Voynich cipher symbol -> one of 24 Latin plaintext letters`

with no two Voynich symbols sharing the same plaintext letter.

Thus this is a classical monoalphabetic substitution model. The ornamental/neumatic shape of a historical León cipher sign is irrelevant to the sequence likelihood once the substitution key is unknown.

## Frozen optimizer

The substitution objective is medieval-Latin character 4-gram cross-entropy on **training Voynich leaves only**.

Represent an injective key as the first `M` entries of a full permutation of the 24 plaintext letters; the remaining entries are unused plaintext letters.

For each physical-leaf fold:

1. use four-fifths of eligible Voynich leaves as training;
2. optimize the full permutation using deterministic multi-start simulated annealing over pair swaps;
3. use exactly **16 restarts**;
4. each restart uses exactly **30,000 proposed swaps**;
5. proposal = uniformly choose two distinct positions in the 24-position full permutation and swap them;
6. score = mean 4-gram NLL in bits/character over the frozen training streams;
7. temperature schedule is geometric from `0.05` bits/character at proposal 0 to `0.00005` at proposal 29,999;
8. accept every improving move; accept worsening delta `d` with probability `exp(-d/T)`;
9. seed restart `r` from SHA-256 of `Issue26E11:LeonMonoSub:v1:{fold}:{r}`;
10. after annealing, run deterministic steepest pair-swap descent over all `24 choose 2 = 276` swaps until no swap improves by more than `1e-12`;
11. choose the restart with minimum final training CE; ties use lexicographically smaller full plaintext permutation;
12. freeze the first `M` symbol assignments and decode the held-out leaves.

Implementation may use Numba/C++/vectorized sufficient statistics for exact speed-up, but it may not change the objective, proposals, seeds, schedule, or final local-descent rule.

## Mandatory positive control — known monoalphabetic Latin cipher

A negative Voynich result is uninterpretable if the solver cannot recover the cipher class at this data size.

Before classifying E11, run a deterministic positive control using the same `M` cipher symbols and approximately the same number of symbol events as the Voynich population.

1. Rank plaintext letters by frequency in the frozen external Latin corpus; take the top `M` letters. Ties lexicographic.
2. In Latin runs, any plaintext letter outside that top-`M` set breaks a run.
3. Retain runs in source order until their total symbol count first reaches the total E11 Voynich symbol-event count; truncate only the final run if necessary.
4. Assign retained runs to five folds round-robin in source order.
5. Encrypt with one deterministic random bijection from the top-`M` Latin letters to the `M` Voynich symbol labels, seed `Issue26E11:PositiveKey:v1`.
6. Run the **identical E11 optimizer** independently in each fold, allowing mappings into all 24 plaintext letters.

Record:

- true-key held-out CE;
- recovered-key held-out CE;
- exact recovered key accuracy;
- occurrence-weighted recovered-key accuracy;
- exact key recurrence across the five solver fits.

Positive-control gate passes only if:

- mean recovered held-out CE is within `0.05 bits/char` of mean true-key held-out CE;
- occurrence-weighted key accuracy is >= `.95` averaged across folds.

If this gate fails, E11 classification is `SOLVER INADEQUATE`, not a negative Voynich inference.

## Voynich five-fold outputs

For each fold record:

- selected full key and symbol→letter mapping;
- training CE;
- held-out CE and scored character count;
- decoded character frequencies;
- top-five-character fraction;
- first 20 held-out decoded physical lines with token spaces preserved, each capped at 160 plaintext characters;
- exact whole-token Latin lexicon hits for decoded Voynich tokens of decoded length >=4;
- distinct exact whole-token lexicon hits length >=6, with corpus frequency, page, line, and context;
- top 50 decoded character 4-grams and their CREMMA counts.

No manual respacing, anagramming, spelling substitution, selective folio fitting, or human key choice.

## Key-stability statistic

A true manuscript-wide monoalphabetic key need not have perfectly stable assignments for extremely rare glyphs, so E11 preregisters both exact and frequency-weighted stability.

Using glyph frequencies pooled over the full frozen Voynich population only for **weights** (never for selecting a plaintext key):

1. for each cipher glyph, find the modal plaintext letter assigned across the five fold-trained keys; ties lexicographic;
2. glyph stability = modal count / 5;
3. weighted key stability = sum over glyphs of `(glyph occurrence fraction × glyph stability)`.

Also record exact full-key recurrence and pairwise mapping agreements.

## Frozen primary interpretation

First require the mandatory positive control to pass.

### `LEON-LIKE MONOALPHABETIC PLAINTEXT LEAD`

Only if all hold under the frozen ZL3b E11 representation:

1. pooled/mean held-out Voynich CE is no more than **0.50 bits/char above** the frozen Latin self-baseline;
2. weighted key stability >= **0.90**;
3. exact same full `M`-glyph key recurs in >= **3/5** folds;
4. pooled decoded output's top-five-character fraction is no more than **0.15 absolute** above the Latin baseline top-five fraction;
5. at least **10 distinct exact whole-token CREMMA lexicon hits of length >=6** occur across at least **3 folds**.

This is only a lead. It would require a new independent transcription/population test before any decipherment claim.

### `LATIN-LIKE BUT KEY-UNSTABLE`

If criterion 1 passes but either stability criterion 2/3 fails.

### `STABLE NON-LANGUAGE OPTIMUM`

If stability criteria 2 and 3 pass but criterion 1 or both output-quality criteria 4/5 fail. This explicitly guards against the E10 frequency-collapse pathology.

### `NO READABLE LEON-LIKE MONOALPHABETIC PLAINTEXT`

If the positive control passes but criterion 1 fails and stability does not justify the `STABLE NON-LANGUAGE OPTIMUM` label.

### `SOLVER INADEQUATE`

If the positive control gate fails.

## Descriptive sensitivity — no-word-boundary issue

The primary 4-gram objective already ignores Voynich token boundaries. Therefore uncertainty about whether Voynich spaces are true word boundaries cannot rescue a poor primary CE.

Whole-token lexicon hits are a **readability diagnostic/gate**, not part of key fitting. If character statistics become strongly positive but token-word diagnostics fail, report that mismatch rather than retuning spaces.

## Historical interpretation boundary

A negative E11 would weaken the simple León-like model:

> one visible Voynich grapheme = one plaintext Latin letter under a stable substitution key.

It would **not** reject the full Visigothic practice, because the real historical tradition can include homophony, rotated variants, distorted signs, and occasional ordinary letters. Those freedoms require separately sourced constraints before a more flexible E12 can be justified.

A positive E11 would not mean that the Voynich manuscript is musical. In the León mechanism, music primarily supplies the visual disguise/alphabetic sign repertoire.

## Merge policy

E11 stays on `issue26-music-e11-leon-substitution` as a dedicated research branch/draft PR. Do not merge to `main` without explicit user authorization.
