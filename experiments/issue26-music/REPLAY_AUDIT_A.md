# Issue #26 direct-music experiment A — replay audit

Status: **EXACT RAW REPLAY PASS**

The direct-music experiment was moved from the temporary `experiments/phase66/` namespace to `experiments/issue26-music/` because a separately prepared botanical attribute-label track already uses Phase66 numbering. The frozen plan text and executable bytes were preserved unchanged.

Replay provenance:

- branch head used by replay: `249fc06d6ed43afd11b3f0d9cd6245ba601d1b7d`
- Actions run: `33353739622`
- job: `99371840920`
- replay artifact: `9744514585`
- plan SHA-256: `e5fb1a437244ad826638dc5fe98c580b87d4d10045c8c8787047db08b3581bb5`
- executable SHA-256: `39ab719892047051775d2932e08e5102d5128bc1c763c02d7d7c928ece21c54a`
- replay raw JSON SHA-256: `8ea72eff1c4550df47b5f7202b3528a0aa43c63d30d573b7fc935cb7a11a7228`

The replay raw JSON SHA-256 is **identical** to the first scientific reveal raw JSON SHA-256 recorded in `REPORT_A.md`.

Replay verdict and primary values are therefore byte-stable under the namespace move:

- classification: `DIRECT-MUSIC SCREEN NEGATIVE`
- Voynich mean Z: `[-2.352923633291695, -1.4039287603969388, 1.4399245746163063, 1.2197252236867286]`
- chant Z: `[32.50899111007105, 101.72002143301397, 159.2154097009444, 183.04887724411145]`
- Latin Z: `[-0.5346091030002609, 0.2216688905449299, 0.26895614308987686, 0.19435150349782693]`
- music-closer folds: `0/5`
- mean `D_music`: `264.2148242594995`
- mean `D_latin`: `3.107812801733286`

No scientific definitions were changed between first reveal and this replay.
