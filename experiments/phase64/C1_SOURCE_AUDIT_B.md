# Phase 64B C1 source audit — published Naibbe external challenger

Status: **frozen before any Phase64B score is computed**.

Parent main at source-freeze start:

`9621f009786be0b14de07bd9d496c4b94d2a2aa0`

## 1. Why use an external C1 first

Phase64A leaves family-comparison fairness as the highest-value mechanism objection. Building an in-house cipher/shorthand model immediately would create substantial researcher freedom.

Phase64B therefore starts with an already published, executable C-family construction whose architecture was fixed outside this project:

> Michael A. Greshko (2025), **The Naibbe cipher: a substitution cipher that encrypts Latin and Italian as Voynich Manuscript-like ciphertext**, *Cryptologia*, DOI `10.1080/01611194.2025.2566408`.

The author describes Naibbe as a hand-executable, historically plausible **verbose homophonic substitution cipher** intended to test whether meaningful Latin/Italian can generate Voynich-like statistical structure.

This makes it a stronger and more relevant C-family challenger than our deliberately simple C0.

## 2. Frozen repository identity

External repository:

`greshko/naibbe-cipher`

Pinned commit:

`f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`

Pinned relevant blobs:

- `naibbe_v2.py` blob SHA-1: `b566ad82e4b6ff0782ecdddebf77718dac44f292`
- `references/naibbe_tables.csv` blob SHA-1: `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`
- `README.md` blob SHA-1: `486782221285186c0f78dd9474b676e067cd4bea`

The repository README explicitly associates the code with the 2025 Cryptologia paper and provides a modified MIT-style research/software license requiring citation.

## 3. Exact published algorithm frozen for the primary challenger

Phase64B primary external challenger uses `naibbe_v2.py` **as published at the pinned blobs**, including these defaults:

- alphabet placeholders over `a-z`, with Latin normalization mapping `W→UU`, `J→I`, `K→C` before encryption;
- six homophonic tables: `alpha`, `beta1`, `beta2`, `beta3`, `gamma1`, `gamma2`;
- states: `unigram`, `prefix`, `suffix`;
- plaintext respacing parameter `RESPACING = 17`;
- `USE_78_CARD_DECK = True`;
- 78-card table weights `28 / 14 / 11 / 11 / 7 / 7`;
- ciphertext `SPACE_REMOVAL_RATE = 0.03`;
- `UNAMBIGUOUS = True`;
- `MAX_BIGRAM_RETRIES = 10000`;
- the exact pinned `naibbe_tables.csv` glyph strings.

The original script processes plaintext line by line. Each line is cleaned, original word spaces are removed, the resulting character stream is randomly resegmented into one- or two-character plaintext units, and those units are encoded via the shuffled homophonic deck. The published respaced output then removes 3% of encrypted-token spaces stochastically.

## 4. Explicit exclusions

The pinned repository also contains later experimental variants. Phase64B **does not use** any implementation that adds explicit short-range ciphertext reuse or other locality machinery.

In particular, variants such as `naibbe_cv_vc_reuse.py` are outside C1-E0.

Reason: importing an explicit reuse mechanism after A1/H62 would collapse the distinction between an independently published C-family challenger and our already successful local-family mechanism.

Any reuse-augmented C model would require a separately frozen later hypothesis and complexity charge.

## 5. Historical motivation versus target dependence

Naibbe's broad operation family is historically motivated. Published work on Renaissance/early-modern cryptography documents simple substitution, homophonic substitution and nomenclator-like systems in Italian diplomatic practice; the Naibbe paper explicitly frames its construction as achievable with 15th-century materials.

However, **the concrete Naibbe glyph codebook is target-aware by design**. The repository and paper explicitly aim to generate Voynich-Manuscript-like ciphertext, and `naibbe_tables.csv` contains Voynich-like glyph strings.

Therefore Phase64B must charge two facts simultaneously:

1. Naibbe is a legitimate external existence-proof candidate for `meaningful plaintext + reversible obscuration`;
2. a good fit is not independent evidence that a historical Voynich encipherer used this exact codebook, because the codebook was designed after observing Voynich structure.

The model is consequently a **strong external challenger with substantial target-dependence cost**, not a neutral historical null.

## 6. Effective codebook complexity

The source code defines six tables × three states × 26 letters = 468 placeholder cells. The plaintext normalizer maps `j/k/w` away before encryption, so 23 letters are effectively reachable in normal Phase64B Latin input, corresponding to 414 effective table/state/letter cells.

The codebook also contains:

- fixed table-weight vector;
- stochastic 1/2-character plaintext segmentation;
- state-specific prefix/suffix composition for bigrams;
- ambiguity rejection against unigram and cross-bigram collisions;
- stochastic post-encryption space removal.

This is materially more representational power than C0 and must be recorded as such.

## 7. Why H62-P1 is valuable here

Naibbe was published before this project's Phase62 H62-P1 recurrence-distance test was defined. The pinned `naibbe_v2.py` contains no explicit previous-10 reuse mechanism.

Thus H62-P1 is not merely another statistic used to construct this external code. It is an out-of-model, post-publication challenge to the published mechanism.

A strong Naibbe H62 result would show that a reversible meaningful-text cipher can generate the same short-vs-long near-family recurrence geometry without A1's explicit local-family reuse rule.

A weak Naibbe H62 result would show that reproducing broad Voynich-like token distributions is insufficient for the prospectively validated recurrence signature.

## 8. Plaintext control authority

Phase64B will encrypt exactly the same four equal-weight source-native medieval Latin controls already frozen for Phase62:

- BIS193
- CLM13027
- Mazarine915
- UBL758

CREMMA source authority remains:

`HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`

This prevents choosing plaintext after seeing Naibbe output.

## 9. References frozen before result

Primary external candidate:

- Greshko, M. A. (2025), *Cryptologia*, DOI `10.1080/01611194.2025.2566408`.
- Public code/data: `https://github.com/greshko/naibbe-cipher`

Historical context used only to justify the broad C family, not to tune the score:

- DECRYPT project / *Cryptologia* survey of historical nomenclator keys: `https://doi.org/10.1080/01611194.2020.1755915`
- Library of Congress guide to medieval/early-modern Latin scribal abbreviation categories, including suspension, contraction and conventional signs: `https://guides.loc.gov/manuscript-transcription/abbreviations`
- Cappelli abbreviation dictionary/data resources are noted as a possible later shorthand-specific C track, but are **not** part of Phase64B C1-E0.

## 10. Source-freeze conclusion

The first serious C-family challenge will be the **exact published Naibbe v2 mechanism**, not an in-house optimized cipher.

No Phase64B scientific metric has been computed at this point.
