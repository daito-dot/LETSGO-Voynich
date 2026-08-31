# Issue #26 direct-music experiment A — first reveal

Status: **DIRECT-MUSIC SCREEN NEGATIVE**

Historical first-reveal label: `Phase66A`. The experiment was initially placed under `experiments/phase66/` before noticing that the separately prepared attribute-level image↔label track already uses Phase66 numbering on branch `phase66-attribute-label-preregister`. The scientific identifiers below are retained unchanged for provenance; this report uses an Issue-26-specific namespace to avoid conflating the two research tracks.

## Frozen question

Does Voynich running text, after a sequence-blind seven-state reduction based only on token-internal form, show phrase-ending concentration and short motif recurrence closer to medieval plainchant than to structured medieval Latin prose?

The plan was committed before the executable and before any scientific output.

## Frozen comparators

- Voynich: ZL3b, exact blob `2a4533ab9bdfa85db9bad602d590978953055df1`, five Phase62 physical-leaf folds.
- Latin: the four Phase62 CREMMA manuscripts at commit `292525969ad98380b398e6606a9c2a36d51913ae`.
- Plainchant: `bacor/ISMIR2020@ab3edb742a718fe5c3fd40550c54f104fe9b6078`, antiphon test subset, exact CSV blob `616fcd986226873cb1f58b8711c1936ad0794af4`.

Voynich and Latin token types were mapped to seven states using only sequence-blind token-form features. Plainchant Volpiano pitches were reduced modulo seven. State labels themselves carry no note-name interpretation.

Four frozen order statistics were compared with 500 within-sequence shuffles:

- M1: final-state concentration excess;
- M2: final-transition concentration excess;
- M3: repeated 3-state motif mass;
- M4: repeated 4-state motif mass.

## Primary result

Mean held-out Voynich Z vector:

`[-2.3529, -1.4039, +1.4399, +1.2197]`

Plainchant Z vector:

`[+32.5090, +101.7200, +159.2154, +183.0489]`

Equal-weight medieval Latin Z vector:

`[-0.5346, +0.2217, +0.2690, +0.1944]`

Voynich was closer to the Latin reference than the chant reference in **all five** physical-leaf folds.

| fold | D to chant | D to Latin | closer |
|---:|---:|---:|---|
| 0 | 265.404 | 1.895 | Latin |
| 1 | 262.935 | 2.604 | Latin |
| 2 | 263.697 | 7.014 | Latin |
| 3 | 265.262 | 1.030 | Latin |
| 4 | 263.775 | 2.997 | Latin |

Mean distances:

- chant: **264.215**
- Latin: **3.108**

Frozen gate: **0/5 music-distance wins**, therefore `DIRECT-MUSIC SCREEN NEGATIVE`.

All four preregistered conditions fail.

## What drives the separation

The main difference is not a subtle motif statistic. Plainchant has a large cadence/phrase-order signature under the same within-sequence null, whereas Voynich does not.

Plainchant raw excess over shuffle:

- M1: `+0.05769`
- M2: `+0.06307`
- M3: `+0.17634`
- M4: `+0.15789`

Mean Voynich raw excess:

- M1: `-0.00433`
- M2: `-0.00355`
- M3: `+0.00045`
- M4: `+0.00064`

Thus the Voynich reduction shows slightly *less* terminal-state / terminal-transition concentration than its own composition-preserving shuffle baseline, while the chant phrases show strong positive terminal concentration. Voynich has some fold-local positive motif-order excess, but its magnitude is tiny relative to chant.

The strongest individual Voynich fold is fold 2: M1 `Z=-5.17`, M2 `Z=-3.67`, M3 `Z=+2.90`, M4 `Z=+2.56`. This is not chant-like: the cadence coordinates point in the opposite direction.

## Predeclared sensitivities

### Paragraph-final Voynich lines

Mean Z vector:

`[-0.4957, -0.3336, +0.2698, +0.2698]`

Restricting Voynich to literal paragraph-final lines does not uncover a chant-like cadence effect.

### Strong chant barline (`4`) only

Eligible sample remained above the frozen floor. Z vector:

`[+39.5315, +244.3736, +142.0162, +166.0127]`

The chant phrase-boundary signal becomes stronger, not weaker.

### Six-state / solmization sensitivity

Frozen classification remains `DIRECT-MUSIC SCREEN NEGATIVE` with **0/5** music-distance wins.

- mean D to chant: `228.411`
- mean D to Latin: `3.906`
- mean Voynich Z: `[-2.8004, -1.6886, +1.4563, +1.1563]`
- chant Z: `[+29.0139, +108.8038, +132.0596, +149.1070]`

## Cross-corpus Z caveat and post-reveal diagnostic

The primary plan compared Z vectors directly. Z magnitude depends partly on effective sample size because the null SD shrinks in larger corpora; the chant comparator is larger than an individual Voynich fold or Latin manuscript. Therefore the numerical size of the Z-distance separation should not itself be interpreted as an effect-size ratio.

After reveal, a non-gating diagnostic compared the unstandardized excess `observed - null_mean` instead. This does **not** repair or replace the frozen test. It checks whether the result is only an artifact of Z scaling.

The raw-excess diagnostic gives the same direction in **5/5 folds**. Mean Voynich raw-excess distance is approximately `0.253` from chant and `0.0116` from Latin. Thus the negative result is not explained solely by unequal Z precision.

## Interpretation

Retain only:

> Under the frozen sequence-blind six/seven-state reductions, Voynich running-text sequences do not reproduce the cadence and short-motif order geometry of the tested medieval plainchant comparator and are substantially closer to the tested structured medieval Latin comparator.

This weakens the simplest direct monophonic finite-state / solmization-like model tested here.

It does not reject:

- music encoded at a different structural level, such as internal slot units rather than visible tokens;
- duration or multi-voice information encoded separately from pitch-like state;
- tablature-like rules whose state mapping is historically constrained by an external key;
- music-theory or `musica mundana` content in specific astronomical diagrams;
- music used as an intermediate cipher or mnemonic carrier.

No state remapping or metric retuning should be performed against this result and called a continuation of experiment A.

## First-reveal provenance

A first workflow attempt stopped before any scientific computation because the provenance check used a shallow checkout. The only change was `fetch-depth: 0`.

Successful first scientific reveal:

- PR: `#27`
- head: `b7d588dd64a31d6a96dbafd6f687cba986e5bb8e`
- Actions run: `33353324223`
- job: `99370674372`
- artifact: `9744368386`
- artifact ZIP SHA-256: `d2d16b463e79f3e0042dafcd8f8945ba9e17fba57548603bfe2cae5b7517d1cc`
- raw result JSON SHA-256: `8ea72eff1c4550df47b5f7202b3528a0aa43c63d30d573b7fc935cb7a11a7228`
- frozen plan SHA-256: `e5fb1a437244ad826638dc5fe98c580b87d4d10045c8c8787047db08b3581bb5`
- executable SHA-256: `39ab719892047051775d2932e08e5102d5128bc1c763c02d7d7c928ece21c54a`
