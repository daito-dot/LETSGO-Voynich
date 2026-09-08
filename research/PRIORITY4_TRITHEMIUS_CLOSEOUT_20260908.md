# Priority 4 closeout — Trithemius TP1518-WA0

Date: 2026-09-08  
Parent: #172  
Issue: #207

## Decision

Priority 4 is complete at the **historical mechanism selection / external executability** level.

Selected candidate:

**`TP1518-WA0` — Trithemius `Polygraphia` sequential word-alphabet strict core**

H0 class:

**`H0_ARCHITECTURE_RECOVERED`**

External H1 bounded round-trip:

**PASS**

No Voynich target statistic was used in H0 or H1.

## What has actually been established

The 1518 `Clavis Polygraphiae` supplies the missing information that blocked T1463:

- one code-bearing Latin word represents one secret Roman letter;
- the writer advances through the alphabets in order;
- alphabets are not to be skipped;
- words outside the alphabetical sequence are explicitly non-code filler;
- long messages may restart from the head or continue into the next book under documented rules;
- the receiver inverts each observed table word using its alphabet position and concatenates the recovered letters.

The strict core therefore has a source-defined encoder and inverse for the hidden Roman-letter stream. It does not recover hidden lexical spaces or punctuation.

## Frozen bounded H1

Three consecutive historical alphabets independently reproduced by Falconer (1685) were frozen as a deliberately small executable prefix.

Input:

`ABC`

Output code units:

`Deus Clementissimus Conservans`

Inverse:

`ABC`

Round-trip: PASS.

The exact 72-cell table serialization is 1,151 UTF-8 bytes / 9,208 bits with SHA-256:

`ddfbecb0666b4d840a384e0dbf8ae1937769c609a95d538a8a21a27a28a50ad4`

No cycling, filler or restart was used.

## Full-table cost gate

A public mechanized extraction already exists in `Trithemius-Corpus/Trithemius-Corpus` at pinned commit:

`0e38a37671a5e3b5decd11c19fe82de79883cae7`

Relevant implementation:

`scripts/build_cipher_data.py`

It parses rendered Style-C cipher tables and emits `site/static/cipher-data.json`. This is useful evidence that hundreds of table cells need not be transcribed manually.

It is **not** accepted as final scientific table authority, because the parser is intentionally tolerant of OCR loss: it keeps substitution columns when at least half of the 24 cells are present and drops more severely damaged columns. The resulting public JSON also preserves OCR scannos. That behavior is appropriate for an exploratory cipher interface, not for an exact historical encoder authority.

Consequently this project will **not** spend the Priority-4 lane manually repairing or transcribing approximately 400 alphabets. Nor will it silently promote the tolerant OCR-derived JSON to an exact codebook.

## Boundary of the result

Priority 4 required selection of one independently documented historical multi-glyph mechanism with sufficiently specified output construction, encoder and inverse. That requirement is met.

The following claims are not made:

- that the full `Polygraphia` cover-text generator is unique;
- that every historical table cell is already source-verified here;
- that TP1518-WA0 resembles Voynich;
- that it passes any R1–R10 target criterion;
- that cyclic reuse of the frozen three-alphabet excerpt is valid;
- that the public OCR-derived full table can be used without an admission audit.

## Next program step

The next main-lane task is the Priority-5 / Issue-#172 joint-tournament admission decision.

Before TP1518-WA0 can receive a Voynich score, a separate preregistered admission step must freeze an **adequately long, source-verifiable executable table corpus** and its R10 cost. That admission step should first test whether the existing mechanized extraction can be filtered to a sufficiently long set of complete, facsimile-verifiable columns without lexical repair. If not, TP1518-WA0 remains a documented architecture/control and the project should not invest in manual table reconstruction merely to force tournament entry.
