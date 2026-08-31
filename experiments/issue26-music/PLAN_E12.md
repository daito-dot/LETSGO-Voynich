# Issue #26E12 — Porta 1602 11×2 musical-cipher plaintext probe

Status: **FROZEN BEFORE E12 EXECUTABLE / REVEAL**

Base research state: Issue26E8 head `343afac73da2e52b3a75f69e0a43257d54bdf952`.

## Purpose

E10 Sloane and parallel E11-O Öttingen both used 5×5 historical music-cipher tables. Neither yielded readable Latin. Sloane showed a 4/5 recurrent fitted key; Öttingen only 3/5, while both collapsed strongly to a few output characters.

E12 deliberately leaves the 5×5 family.

Question:

> If Giambattista della Porta's historically attested two-note-value × eleven-pitch musical cipher is used as an actual decoder, with the eleven-position dimension imposed explicitly from the historical cipher rather than claimed as a Voynich discovery, does held-out Voynich produce readable medieval Latin?

E12 is exploratory. Porta 1602 postdates the usual Voynich production window and is used as a structurally different historical decoder family, not as historical-origin evidence.

## Historical cipher frozen before reveal

Source: Giambattista della Porta, *De Furtivis Literarum Notis* (1602), with the well-known musical cipher reproduced in modern historical surveys.

The documented construction maps:

- `A` through `M`, omitting `J` and `K`, to **ascending semibreves** across eleven stepwise pitch positions;
- the remainder of the alphabet, omitting `V` and `W`, to **descending minims** across the same eleven positions.

Use pitch rank `0..10` from low to high. The frozen plaintext table is therefore:

- semibreve row, low→high: `a b c d e f g h i l m`;
- minim row, low→high: `z y x u t s r q p o n`.

Thus the supported 22-letter plaintext alphabet is:

`a b c d e f g h i l m n o p q r s t u x y z`

Letters `j/k/v/w` are unsupported by this exact historical table. For the external Latin corpus, normalize `j→i`, `v→u`; `k` and `w` then break a supported run.

The direction and two note-value classes may not be changed after reveal.

Historical references frozen for provenance:

- Porta, *De Furtivis Literarum Notis*, Naples, 1602;
- David Løberg Code, “Can musical encryption be both? A survey of music-based ciphers,” *Cryptologia* 47(4), 2023, DOI `10.1080/01611194.2021.2021565`;
- Wikimedia Commons reproduction `Porta Music Cipher.jpg` from the 1602 treatise.

## Voynich representation

Use the exact frozen ZL3b source and parser used in E8–E11:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`;
- expected ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`.

Primary parser: `min`. `max` is sensitivity only.

### Two-value note-class factor

Under the adopted Zattera grammar, exactly one slot has **two raw states including EMPTY**:

- slot11: `EMPTY / y`.

E12 therefore uses slot11 as the two-valued note-class channel with **no slot selection**.

The mapping of `EMPTY/y` to `semibreve/minim` has exactly two orientations and is selected on training leaves only.

### Eleven-position pitch factor

No adopted Voynich slot naturally has eleven states. Therefore **11 is explicitly hypothesis-side**, imposed by Porta's historical cipher.

For each physical-leaf fold:

1. exclude slot11 from the morphology used to infer pitch position;
2. represent each parsed token type by one-hot values of slots0..10, including EMPTY states;
3. fit deterministic `k=11` clustering on **unique parsed token types occurring in the 4/5 training leaves**, equal weight per type;
4. use deterministic farthest-first initialization, lexicographic tie-breaking, and Lloyd updates, analogous to the frozen Issue26E deterministic clustering implementation;
5. assign held-out token types to the nearest frozen centroid; never refit on held-out leaves.

The 11 clusters are only a Porta-required decoding coordinate. Their existence is **not evidence that Voynich has an independently discovered eleven-state pitch system**.

## External Latin model

Use frozen CREMMA medieval Latin:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`;
- `BIS-193`, `CLM13027`, `Mazarine915`, `UBL758`.

Normalize lowercase ASCII, `j→i`, `v→u`; `k/w` and nonletters break supported Porta runs.

Build:

1. an additive-smoothed character bigram model (`alpha=.1`) used **only for training-key selection**;
2. an additive-smoothed character 4-gram model (`alpha=.1`) used for held-out readability evaluation;
3. a supported-word lexicon from the same frozen external corpus.

Compute a five-fold external Latin self-baseline for the 4-gram evaluator and record its top-five-character fraction.

## Porta key search

A Porta decoding key consists of:

- one duration orientation (`EMPTY/y → semibreve/minim` or the reverse);
- one bijection from the 11 train-fitted morphology clusters to the 11 ordered pitch ranks.

Total exact key space per fold is `2 × 11! = 79,833,600`; it is not exhaustively enumerable under the sequence objective.

Use a frozen deterministic simulated-annealing search on training **raw-symbol bigram sufficient statistics**.

For each duration orientation independently:

- 24 deterministic restarts;
- 40,000 proposed pitch-rank swaps per restart;
- state = a permutation of ranks `0..10` assigned to cluster labels `0..10`;
- proposal = uniformly choose two distinct cluster labels and swap their assigned pitch ranks;
- objective = mean negative log2 probability per training adjacent plaintext-character pair under the frozen external Latin bigram model;
- physical line breaks/unparseable-token breaks are never crossed;
- geometric temperature schedule from `.05` bits/pair to `.00005`;
- improving moves always accepted; worsening move delta `d` accepted with probability `exp(-d/T)`;
- deterministic seed `Issue26E12:Porta11x2:v1:{policy}:{fold}:{orientation}:{restart}`;
- after annealing, deterministic steepest pair-swap descent over all 55 swaps until no improvement >`1e-12`;
- choose the globally best restart/orientation by training objective; ties: orientation 0 first, then lexicographic permutation.

The held-out fold is untouched until the key is frozen.

## Mandatory solver positive control

A real Voynich negative is interpretable only if this structured 11×2 key solver can recover a known Porta key at comparable sequence length.

For each fold:

1. take supported frozen-CREMMA Latin runs until the symbol count matches the corresponding Voynich training+held population approximately;
2. encode them with the exact historical Porta table;
3. apply a deterministic hidden random permutation of the eleven pitch labels and a deterministic hidden duration flip, seeded from `Issue26E12:PositiveKey:v1:{fold}`;
4. run the **identical E12 key optimizer**, without access to the hidden key;
5. score a held-out fifth of the synthetic encoded runs.

Positive-control gate passes only if both hold averaged across folds:

- recovered held-out 4-gram CE is within `0.05 bits/char` of true-key held-out CE;
- occurrence-weighted decoded-letter accuracy >= `.95`.

If the positive-control gate fails, frozen classification is **`SOLVER INADEQUATE`** and no Voynich negative inference is made.

## Voynich held-out outputs

For each fold record:

- training token-type count and k=11 centroid metadata;
- selected duration orientation and pitch permutation;
- training bigram CE;
- held-out 4-gram CE and scored-character count;
- decoded character counts and top-five-character fraction;
- first 20 held-out decoded physical lines length >=12, capped at 160 chars;
- exact decoded whole-token CREMMA lexicon hits length >=4;
- count/list of distinct exact hits length >=6;
- top 50 decoded 4-grams with CREMMA counts.

Pool held-out folds for descriptive output only; keys/clusters remain fold-specific.

## Frozen practical interpretation

First require the solver positive control.

### `PORTA PLAINTEXT LEAD`
Only if all hold under primary `min`:

1. mean held-out 4-gram CE <= Latin self-baseline + `0.50 bits/char`;
2. pooled top-five-character fraction <= Latin baseline + `0.15` absolute;
3. at least 10 distinct exact whole-token CREMMA hits length >=6 across at least 3 folds;
4. the same slot11 duration orientation is selected in >=4/5 folds.

This is an exploratory lead, not decipherment.

### `NO READABLE PORTA PLAINTEXT`
If the positive control passes but any of the four lead criteria fails.

### `SOLVER INADEQUATE`
If the positive control fails.

## Anti-collapse interpretation

Explicitly flag **`LOW-DIVERSITY OPTIMUM`** if pooled top-five-character fraction >=.90, regardless of CE. Such an optimum cannot be called plaintext-like even if the language model score improves.

## Boundaries

- Do not claim `11` as a data-discovered Voynich constant.
- Do not test alternative k after reveal and call it E12.
- Do not choose another two-state factor; slot11 is the only natural binary raw slot under the adopted grammar.
- Do not reverse or reorder the historical Porta rows after reveal.
- Do not use held-out plaintext appearance to choose a key.
- Do not manually respell, anagram, re-space, or select favorable folios.
- E12 is exploratory and later-than-Voynich; it cannot establish historical transmission.
- Keep E12 on its research branch; do not merge to main without explicit user authorization.
