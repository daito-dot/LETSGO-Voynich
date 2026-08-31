# Issue #26 experiment B — Ptolemaic tonos↔zodiac pairing test

Status: **FROZEN BEFORE SCIENTIFIC REVEAL**

## Historical candidate audit

The direct claim "Ptolemy mapped the twelve zodiac signs one-to-one to twelve modern chromatic pitch classes" is not accepted as the historical model.

In *Harmonics* III.8–9 Ptolemy compares the two-octave Perfect System with the zodiac geometrically. The Perfect System has fifteen notes / fourteen intervals; the analogy cannot be a literal one-interval-per-sign assignment. A scholarly reconstruction explicitly notes this mismatch and treats the correspondence as geometric. Ptolemy nevertheless also notes that the double octave is approximately twelve whole tones, motivating a twelve-sector circular analogy.

A more sharply constrained candidate occurs in III.12: seven Greek `tonoi` are associated with seven celestial latitude bands whose intersections with the ecliptic delimit the twelve zodiacal signs. The sign↔tonos pattern is externally specified:

- Cancer — Mixolydian
- Gemini + Leo — Lydian
- Taurus + Virgo — Phrygian
- Aries + Libra — Dorian
- Pisces + Scorpio — Hypolydian
- Aquarius + Sagittarius — Hypophrygian
- Capricorn — Hypodorian

Primary historical references used to freeze this candidate:

- Ptolemy *Harmonics* Book III chapter sequence, especially III.8–12; Andrew Barker's scholarship on Ptolemaic harmonics.
- Canterbury Christ Church University thesis/repository discussion of Ptolemy's tone-zodiac and the explicit seven-tonoi/twelve-sign mapping: https://fileserver-az.core.ac.uk/download/287636482.pdf
- Jacqueline Feke, *Ptolemy's Philosophy: Mathematics as a Way of Life*, discussion of III.12: the seven tonoi correspond to the tropics, equator and four intermediate parallels; these intersect the ecliptic at zodiac boundaries.
- Barcelona dissertation discussion of III.8: https://diposit.ub.edu/bitstreams/2138bc45-60f7-4180-85a2-9e5d4cbfeb94/download — fifteen-note/fourteen-interval Perfect System prevents a literal 12-sign interval mapping.

This experiment tests the externally fixed **same-tonos sign pairing**, not note names and not a 12-tone chromatic cipher.

## Question

After controlling the already-established production-order morphology drift, are Voynich zodiac label registers assigned to the same Ptolemaic `tonos` more morphologically similar than alternative pairings of the same zodiac signs?

## Manuscript population

Voynich source:

- `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`
- `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- exact git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`

Use only zodiac labels with locus subtype `Lz` on physical pages 135–146.

Sign groups are fixed by the source's explicit page comments and the existing project chronology convention:

- Pisces: page 135
- Aries: pages 136–137 combined
- Taurus: pages 138–139 combined
- Gemini: page 140
- Cancer: page 141
- Leo: page 142
- Virgo: page 143
- Libra: page 144
- Scorpio: page 145
- Sagittarius: page 146

Capricorn and Aquarius are absent from this surviving zodiac sequence and are not imputed.

The four complete Ptolemaic same-tonos pairs available in the manuscript are therefore frozen as:

1. Gemini–Leo (Lydian)
2. Taurus–Virgo (Phrygian)
3. Aries–Libra (Dorian)
4. Pisces–Scorpio (Hypolydian)

Cancer and Sagittarius are not used in the primary pairing score because their partners are absent. They remain in the nuisance chronology fit.

## Text normalization

For each `Lz` locus:

1. remove editorial angle-bracket annotations and bracket-choice markup conservatively;
2. split on visible dot/space separators;
3. retain contiguous lowercase `a-z` runs of length >=1;
4. do not join across visible token separators;
5. aggregate all retained runs from all `Lz` loci belonging to the same sign group.

No glyph equivalence, slot collapse, proposed note mapping or Voynich-specific semantic mapping is introduced.

## Frozen morphology representation

For each sign, construct two frequency blocks from within-token character n-grams:

- unigram frequencies over `a-z`;
- bigram frequencies observed anywhere in the ten-sign zodiac population.

A bigram never crosses a visible token boundary.

Within each sign, each block is normalized to sum to 1. Concatenate the unigram and bigram blocks after multiplying each block by `1/sqrt(2)`, giving equal total L2 weighting opportunity to the two resolutions before cosine similarity.

No n-gram is selected by association with the historical candidate.

## Production-order nuisance correction

The repository already established a strong zodiac morphology trajectory with physical page order. The historical candidate must not receive credit for similarities explained by that drift.

Define the sign's physical-position coordinate as the mean page number of its group:

`Pisces 135; Aries 136.5; Taurus 138.5; Gemini 140; Cancer 141; Leo 142; Virgo 143; Libra 144; Scorpio 145; Sagittarius 146`.

For all `10 choose 2 = 45` sign pairs:

1. compute raw cosine similarity of the frozen morphology vectors;
2. compute absolute physical-position distance;
3. fit one ordinary least-squares line `similarity = a + b * page_distance` across all 45 pairs, without using Ptolemaic category labels;
4. define residual similarity as observed minus fitted similarity.

The nuisance fit is fixed before the Ptolemaic pairing score is evaluated and is identical for every exact-null matching.

## Primary statistic and exact null

Primary target signs are exactly these eight:

`Pisces, Aries, Taurus, Gemini, Leo, Virgo, Libra, Scorpio`.

Observed score:

> mean residual similarity of the four frozen Ptolemaic same-tonos pairs.

Exact null:

- enumerate all `8! / (2^4 4!) = 105` perfect matchings of the same eight signs into four unordered pairs;
- compute the same mean residual similarity for every matching;
- one-sided exact p = fraction of the 105 scores greater than or equal to the frozen Ptolemaic score.

There is no rotation, reversal, category relabeling, pair dropping, feature selection or parameter optimization.

## Frozen classification

- **SUPPORTED CANDIDATE RELATION:** exact `p <= 0.05` and observed score > 0.
- **NOT SUPPORTED:** exact `p > 0.05` or observed score <= 0.

Because n=4 target pairs is small, even a pass is only a narrow historical-structure signal and not a decipherment.

## Predeclared sensitivities

These cannot rescue the primary classification:

1. unigram block only;
2. bigram block only;
3. raw cosine similarity without chronology residualization, reported specifically to show the size/direction of the production-order confound;
4. leave-one-target-pair-out descriptive scores for influence diagnosis.

No alternative historical mapping or state assignment may be substituted after reveal.

## Falsification / interpretation

A negative result supports only:

> The surviving Voynich zodiac-label morphology does not preferentially group the four available same-tonos sign pairs from Ptolemy *Harmonics* III.12 after the frozen production-order correction.

A positive result supports only:

> The four surviving sign pairs assigned to the same Ptolemaic tonos are unusually morphologically similar relative to alternative perfect matchings after the frozen chronology correction.

A positive result would require independent-transcription replication before any semantic or historical promotion.
