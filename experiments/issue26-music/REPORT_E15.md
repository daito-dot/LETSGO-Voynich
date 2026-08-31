# Issue #26E15 — Bacon biliteral two-difference musical-carrier probe

Status: **COMPLETED — `NO READABLE BACON BILITERAL PLAINTEXT`**

## Question

E15 moved away from pitch×duration/table ciphers to a structurally different sequential binary carrier. Bacon's biliteral cipher represents a 24-letter alphabet by five successive instances of two differences (`a/b`), and Bacon explicitly notes that such differences can be conveyed by objects accommodated to the ear, including bells and trumpets.

The Voynich-side binary observable was fixed before reveal to the unique natural two-state raw Zattera slot:

- slot11 `EMPTY`
- slot11 `y`.

The historical five-bit grouping is model-side; it was not discovered from Voynich.

## Frozen search space

Only ten target keys were permitted:

- one global five-bit phase: `0..4`;
- one global binary orientation: `EMPTY=a,y=b` or the reversal.

No paragraph-, line-, folio-, or section-specific phase was allowed.

The frozen Bacon alphabet used the 24 codes `00000..10111`; codes `11000..11111` were explicit invalid groups and broke Latin scoring runs rather than being silently discarded or reassigned.

## Preregistration and provenance

- plan-first commit: `7bf9e1fff61a09268cfc6d1771cd73eb06d5f280`
- first executable: `a17d182ed70eee9291cfc8b20286f9c651e36ef7`
- first-reveal workflow/head: `76f902c0a08b6e269c21ec3b820d0771641e7a7f`
- Actions run: `33388293307`
- job: `99475801258`
- artifact: `9756455439`
- raw JSON SHA-256: `631d70feee7004ec5aeb92b6ca0e256e8a2fce60e59ad7b527149b460017f5de`
- artifact ZIP SHA-256: `8b30e021f77e4264feac801bc0775d5b00ff80e138a2ecf8b1df2e805601fda6`
- ZL3b source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- ZL3b blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- CREMMA commit: `292525969ad98380b398e6606a9c2a36d51913ae`.

The workflow verified plan-before-executable chronology and exact external inputs before reveal.

## Mandatory positive control

**PASS**.

Five deterministic hidden Bacon carriers used different hidden phase/orientation keys. The frozen ten-key selector recovered:

- exact hidden key: **5/5**
- mean decoded-letter accuracy: **1.000**
- mean valid-group fraction: **1.000**
- mean recovered-minus-true held CE: **0.000 bits/char**.

Thus the target negative cannot be attributed to inability of the selector to recover the frozen Bacon mechanism.

## External Latin baseline

Frozen CREMMA medieval-Latin self baseline:

- mean held-out 4-gram CE: **`2.4515716158 bits/char`**
- pooled top-five character fraction: **`.5102175496`**.

## Primary `min` population

- visible tokens: **32,570**
- parsed slot11 carrier states: **25,071**
- parse coverage: **`.7697574455`**
- carrier runs: **5,634**
- total carrier bits: **25,071**.

## Primary result

Frozen classification:

> **`NO READABLE BACON BILITERAL PLAINTEXT`**

Selected key:

- global phase `0`
- orientation `EMPTY=a, y=b`
- exact key recurrence: **5/5 folds**.

Held-out pooled diagnostics:

- five-bit groups: **2,864**
- invalid groups: **545**
- valid-group fraction: **`.8097067039`**
- invalid-group fraction: **`.1902932961`**
- pooled held-out CE: **`4.6988939426 bits/char`**
- 4-gram scored characters after invalid-run breaks: **59**
- decoded valid characters: **2,319**
- top-five character fraction: **`.3937041828`**
- distinct exact CREMMA words length >=6: **0**
- folds with any >=6 word: **0**.

The very low number of scored 4-gram characters is itself diagnostic: approximately 19% of five-bit groups fall into Bacon's eight unassigned codewords, repeatedly fragmenting the decoded output before four consecutive valid letters can form.

The five held folds independently selected the same phase/orientation, but their held valid fractions ranged only from about `.776` to `.837`; held CEs were approximately `4.585, 4.585, 4.585, 4.926, 4.804`.

No decoded valid segment reached the report's length-12 sample threshold. This is not hidden readable text; it reflects heavy fragmentation by invalid five-bit groups.

## Frozen gates

- exact key recurrence >=4/5: **PASS** (5/5)
- valid-group fraction >=.95: **FAIL** (`.8097`)
- CE within Latin +.50: **FAIL** (`4.6989` vs threshold `2.9516`)
- top-five fraction within Latin +.15: **PASS**
- >=10 distinct words length >=6: **FAIL** (0)
- long words across >=3 folds: **FAIL** (0 folds)
- refitted order-null p <=.01: **FAIL** (`.20398`)
- real CE >=.10 below null median: **PASS** by only `.11339 bits/char`.

Neither formal auxiliary flag fired:

- `LOW-VALIDITY` threshold was <.80; observed `.8097` is just above it;
- `LOW-DIVERSITY OPTIMUM` threshold was >=.90; observed `.3937` is far below it.

The absence of these flags does not rescue readability because the primary validity, CE, lexical, and order-specificity gates fail.

## Fully refitted 200-null order test

Each null independently shuffled slot11 bits within every carrier run while preserving exact binary frequency, run length, paragraph, and leaf identity. Every null then received the complete ten-key five-fold selection from scratch.

Results:

- real CE: **`4.6988939426`**
- null median CE: **`4.8122882467`**
- null q05: **`4.6161479476`**
- null minimum: **`4.4171326810`**
- nulls with CE <= real: **40/200**
- lower-tail p: **`.2039800995`**
- real advantage below null median: **`.1133943042 bits/char`**.

The real sequence is slightly better than the null median, but not remotely exceptional under the frozen p-value gate. The apparent 5/5 key recurrence is also not intrinsically surprising in this tiny ten-key problem: among shuffled nulls, recurrence was 2/5 in 27 cases, 3/5 in 65, 4/5 in 60, and 5/5 in 48.

Thus phase-0/orientation-0 stability is **not evidence for a Bacon carrier**.

## Literal phase-0 comparison

The selected key is also the literal phase-0 `EMPTY=a,y=b` convention. It gives:

- valid fraction `.8097`
- CE `4.6989`
- zero >=6 lexicon hits.

Reversing only the binary orientation at phase 0 is worse on validity (`.6177`) and CE (`4.8051`).

## `max` parser sensitivity

Also negative:

- phase/orientation recurrence: **5/5**, same phase0/orientation0
- pooled valid fraction: **`.8023743017`**
- pooled CE: **`4.7357989817`**
- top-five fraction: **`.3838120104`**
- distinct >=6 words: **0**.

The parser sensitivity does not rescue the result.

## Interpretation

E15 gives a clean practical negative for a mechanism that is substantially different from the preceding musical cipher probes.

The manuscript does contain a natural binary slot, and the same global phase/orientation is preferred in every physical-leaf fold. But the historical Bacon five-bit code produces too many unassigned codewords, highly fragmented valid runs, poor medieval-Latin 4-gram likelihood, no long lexical material, and no significant advantage over fully refitted frequency-preserving order nulls.

Therefore the observed binary asymmetry should not be promoted as a music/cipher residual on the basis of E15.

E15 weakens the idea that the negative music-cipher results are merely a local optimum of the earlier pitch-table families: a low-freedom sequential binary carrier fails as well.

No post-reveal variable phases, bit insertions/deletions, error correction, alternate 24-of-32 codebooks, or alternative binary Voynich features are authorized as E15 rescue analyses.

No merge to `main` is authorized.
