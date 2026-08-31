# Issue #26 experiment D — adversarial audit of public direct-music claim

Status: **NOT SUPPORTED**

Frozen components passed: **0 / 4**.

## Question

Does the explicit March-2026 public music interpretation survive literal transcription checks and multiplicity-aware tests without repairing its mapping after inspection?

The frozen package claimed:

1. f67r2 `aiin` forms trace two tetrachords separated by an absence at sectors 5–6;
2. an exact `ain` near 12 o'clock is opposed by a `-daiin` form near 6 o'clock, supporting `daiin = octave`;
3. f113r paragraphs 6–8 are an `A+B / A / B` word-for-word repeat;
4. the fixed prefix map `che=G, o=D, qo=F, sho=A, cho=E, ch=C` makes f113r paragraphs 1–3 reproduce the Mode-VIII *Veni Creator Spiritus* contour.

The plan and the chant fixture were committed before the executable and before scientific output.

## Frozen sources

Voynich:

- ZL3b commit `315f0cad4de3d021bd4185765c037cf2a28d341c`
- exact blob `2a4533ab9bdfa85db9bad602d590978953055df1`

Chant reference:

- *Veni Creator Spiritus*, GregoBase score 14258 / Solesmes 1983, Mode VIII
- first-stanza pitch groups frozen in `VENI_CREATOR_STANZA1_PITCH_GROUPS.txt`
- no alternative melody/version was selected after reveal

## D1 — f67r2 tetrachord/disjunction pattern

Frozen expected first-seven sector pattern for `aiin`-family presence:

`[present, present, present, present, absent, absent, present]`

### Primary strict `aiin` substring

Observed across all 12 sectors:

`[0,1,0,0,1,1,1,1,1,1,1,1]`

First-seven agreement: **2 / 7**.

### Predeclared broad `a[i]+n` sensitivity

Observed across all 12 sectors:

`[1,1,1,1,1,1,1,1,1,1,1,1]`

First-seven agreement: **5 / 7**.

The broad family is present in every sector, so the claimed positions-5–6 disjunction is not present under the broader reading either.

**D1: FAIL.**

## D2 — f67r2 `ain` opposite `-daiin`

This component contains an important factual nuance.

The literal observation does exist in ZL3b under the frozen sector indexing:

- sector 3 (~12:00) contains exact token `ain`;
- opposite sector 9 (~6:00) contains a token ending in `daiin`.

However exact `ain` occurs in sectors 1 and 3, while `-daiin` suffixes occur in sectors 2, 8, 9, 10 and 12. The observed number of diametric root→octave hits is 1.

Exact 12-rotation null scores:

`[1,1,0,0,0,1,0,2,0,2,1,2]`

One-sided exact p: **0.583333**.

Therefore the highlighted opposition is a real positional fact but is not unusual given the occupancy of these forms around the circle. It does not provide statistical support for `daiin = octave`.

**D2: FAIL.**

## D3 — f113r `A+B / A / B` word-for-word repetition

Token counts:

- P6: 39
- P7: 20
- P8: 28

Literal tests:

- P7 is a prefix of P6: **false**
- P8 is a suffix of P6: **false**
- `P7 + P8 == P6`: **false**

Similarity diagnostics are also weak:

| comparison | longest common contiguous run | LCS | token-set Jaccard |
|---|---:|---:|---:|
| P6 vs P7 | 1 token | 2 | 0.0351 |
| P6 vs P8 | 1 token | 2 | 0.0476 |

Thus the public `word for word` statement is directly contradicted by the current frozen ZL3b transcription.

**D3: FAIL.**

## D4 — fixed f113r prefix→pitch mapping vs *Veni Creator Spiritus*

Published mapping, unchanged:

- `che` → G
- `o` → D
- `qo` → F
- `sho` → A
- `cho` → E
- `ch` → C

Only literal token-initial prefix matches were allowed; longest prefix wins. No undocumented stripping of leading glyphs was performed.

Target P1–P3:

- mapped-token coverage: **0.652174**
- normalized interval-DTW distance to frozen chant stanza: **1.03125**

### Mapping multiplicity

All `6! = 720` one-to-one assignments of the same six prefixes to the same six diatonic pitch values were enumerated.

- published mapping rank: **126 / 720**
- exact `p_map`: **0.177778**

The published assignment is not unusually close to the chant among the mapping freedom available.

### Paragraph-window multiplicity

With the published map fixed, every eligible contiguous three-paragraph window on f113r was evaluated.

- eligible windows: **14**
- P1–P3 rank: **6 / 14**
- `p_window`: **0.428571**

P1–P3 is not an unusually Veni-like region of the page under the fixed mapping.

**D4: FAIL.**

## Frozen classification

D1 fail / D2 fail / D3 fail / D4 fail → **0 / 4**.

Frozen overall classification: **`NOT SUPPORTED`**.

## Interpretation

Retain only:

> The tested March-2026 public direct-music package is not supported under literal current-ZL3b transcription checks and multiplicity-aware comparison. One highlighted f67r2 `ain`↔`-daiin` opposition is factually present, but it is not statistically exceptional; the claimed tetrachord gap, the f113r word-for-word responsory structure and the specific *Veni Creator Spiritus* mapping do not survive the frozen tests.

This does **not** reject every possible musical encoding. In particular, it does not test a historically constrained slot-level tablature / Guidonian gamut model or a hidden/intermediate musical coding layer.

## First-reveal provenance

- PR: `#30`
- scientific head: `e1011b39081a2a12743e8412f38df9fa62934d80`
- Actions run: `33355144370`
- job: `99375736084`
- artifact: `9744879635`
- artifact ZIP SHA-256: `7682cd79f38f9a8ad348ee6b82e78e77302802e8129583f74912cf0a4d9193a8`
- raw JSON SHA-256: `e47b9ca6abb45636787f51895460bf1dfa4f3886fcf0dc26a57f98f42888eb17`
- plan SHA-256: `64c066806c8e5fc72ef5ebdebc3c23363e10ea007fa21d7a9bede85478dfd8d9`
- chant fixture SHA-256: `c636201c2f0e9a11375856fec1b7a24038bbbf7f1e47d024f428fa6590b1a067`
- executable SHA-256: `ba7651e5c764a2466453b990a5ac87c5149c07a25bd2804b47668b810ae2ab15`
