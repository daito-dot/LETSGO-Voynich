# Issue #26 experiment B — Ptolemaic tonos↔zodiac pairing

Status: **NOT SUPPORTED**

## Historical correction before the test

The useful historical candidate is narrower than a common modern formulation of Ptolemy's "tone-zodiac".

`PLAN_B.md` rejected a literal "12 zodiac signs = 12 modern chromatic pitch classes" reading. In *Harmonics* III.8–9 the two-octave Perfect System and the zodiac are compared geometrically; the complete system contains fifteen notes / fourteen intervals, so there is no literal one-interval-per-sign identity. The approximately twelve-whole-tone span motivates a circular analogy, but not a modern equal-tempered chromatic substitution table.

The confirmatory test instead used the externally specified III.12 seven-`tonoi` relation to celestial latitude. Four complete same-tonos sign pairs survive in the Voynich zodiac sequence:

- Gemini–Leo — Lydian
- Taurus–Virgo — Phrygian
- Aries–Libra — Dorian
- Pisces–Scorpio — Hypolydian

Cancer and Sagittarius lack their corresponding partner in the surviving manuscript sequence and were excluded from the target pairing score while remaining in the production-order nuisance fit.

## Frozen test

- source: ZL3b exact blob `2a4533ab9bdfa85db9bad602d590978953055df1`
- population: `Lz` labels on physical pages 135–146
- sign groups: Pisces, Aries, Taurus, Gemini, Cancer, Leo, Virgo, Libra, Scorpio, Sagittarius
- morphology: equal-weight unigram + bigram within-token frequency cosine
- nuisance control: OLS of all 45 sign-pair similarities on absolute physical-page distance
- primary score: mean residual similarity of the four same-tonos pairs
- exact null: all 105 perfect matchings of the same eight target signs
- no rotation, reversal, category relabeling, pair dropping or feature selection

Plan, parser and representation details were all committed before the executable and before the scientific reveal.

## Result

Frozen classification: **`NOT SUPPORTED`**

Primary:

- target mean residual similarity: **-0.007878**
- exact p (`matching score >= target`): **0.714286**
- target rank: **75 / 105**
- chronology slope: **-0.032896 cosine similarity per page-distance unit**

The negative chronology slope independently reproduces the expected direction of zodiac production-order proximity: signs closer in physical production order are morphologically more similar.

### Target pairs

| Ptolemaic pair | page distance | raw cosine | chronology-expected | residual |
|---|---:|---:|---:|---:|
| Gemini–Leo | 2.0 | 0.79755 | 0.80509 | -0.00754 |
| Taurus–Virgo | 4.5 | 0.59416 | 0.72285 | -0.12869 |
| Aries–Libra | 7.5 | 0.62977 | 0.62416 | +0.00561 |
| Pisces–Scorpio | 10.0 | 0.64103 | 0.54192 | +0.09910 |

Two pairs are above the chronology expectation and two below it. Taurus–Virgo is strongly negative and dominates much of the aggregate failure; removing it descriptively makes the remaining three positive on average, but that influence diagnosis was predeclared and cannot rescue the four-pair historical hypothesis.

## Predeclared sensitivities

All remain null:

| representation | target score | exact p |
|---|---:|---:|
| unigram only, chronology residualized | -0.02011 | 0.73333 |
| bigram only, chronology residualized | +0.00435 | 0.65714 |
| combined raw cosine, no chronology correction | 0.66563 | 0.79048 |

The raw test being even less unusual shows that the Ptolemaic pairing is not being hidden by the linear production-order correction.

Leave-one-target-pair-out descriptive mean residuals:

- omit Gemini–Leo: -0.00799
- omit Taurus–Virgo: +0.03239
- omit Aries–Libra: -0.01237
- omit Pisces–Scorpio: -0.04354

## Interpretation

Retain only:

> The surviving Voynich zodiac-label morphology does not preferentially group the four available same-tonos sign pairs from Ptolemy *Harmonics* III.12 after the frozen production-order correction.

This is a direct test of an externally specified historical music-cosmology relation, not a generic sonification. It therefore weakens one of the cleaner `musica mundana`-style hypotheses available for the zodiac section.

It does **not** reject all astronomical/music-theory content. In particular, III.8–9 contains geometric interval/aspect relations rather than the categorical same-tonos pairing tested here; a future test would need an independently fixed geometric observable rather than inventing a glyph-to-pitch mapping.

## First-reveal provenance

- PR: `#28`
- scientific head: `8d4b64632bac35fe7fe6cd4273f0073cae221b44`
- Actions run: `33354342497`
- job: `99373515303`
- artifact: `9744635099`
- artifact ZIP SHA-256: `be34925808c26d8628e672c2a1419aa4c42dc2b28e006906ff1a3c99c97af562`
- raw JSON SHA-256: `c286ad5648c66146b5e9a9c7ffde6fb6312f9f6f07981db1d8124c62093a0a66`
- plan SHA-256: `6dc63e65b61aa948250efe316d4f7c20db5ac715dde778dba7bc8ecaeee369e3`
- parser amendment SHA-256: `82d7f2afb0e7eef36577d5d24bba5c29a048bed808de80b59e4b1978c0c26043`
- representation amendment SHA-256: `8f53501a627c32fb0a1bcfb7e3897dc8fa7f25119b31250b7c0ef687b09a3266`
- executable SHA-256: `3304e29c4d5669550cdbe10df35a2937d7bbbcaafec09c0774f04d6306c59ad2`
