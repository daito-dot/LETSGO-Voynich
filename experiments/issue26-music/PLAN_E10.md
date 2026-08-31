# Issue #26E10 — Sloane 351 late-medieval musical-cipher decode probe

Status: **FROZEN BEFORE E10 EXECUTABLE / REVEAL**

Issue: #26
Base research state: Issue26E8 branch at `343afac73da2e52b3a75f69e0a43257d54bdf952`.

## Purpose

E9 applied the 1436 Nicholas Philip cipher as a practical decoder and did not recover coherent medieval-Latin plaintext. E10 tests a different, historically attested music-cipher construction rather than modifying Philip.

Target: British Library Sloane 351, late fifteenth century, musical cipher described in the manuscript and in Bernhard Bischoff's catalogue of medieval cryptographic systems.

This is **exploratory** because Sloane 351 is later than the usual early-fifteenth-century dating of the Voynich parchment/manuscript. A match cannot establish historical transmission or origin by itself.

## Historical table frozen before reveal

Bischoff's description of Sloane 351 fol. 15r gives five musical note-form families distributed over five staff positions:

1. triangular, up-stemmed, ascending: `a e i o u`;
2. triangular/un-stemmed, ascending: `l m n r s`;
3. square/un-stemmed, ascending: `b c d f g`;
4. square/down-stemmed, descending from the upper space: `k p q t`;
5. square/up-stemmed, ascending: `x y z et con`;
6. `h` is an oblique cross on the middle line and explicitly outside the note system.

Secondary corroboration: Eric Sams describes Sloane 351 as a late-fifteenth-century musical cipher using five pitches on a three-line staff, with altered stem directions/note values, encoding 24 letters plus `et`.

### Canonical 5×5 completion used only for computation

The musical part contains 24 note cells: four complete 5-position families plus one 4-position family. Family 4 begins in the upper space and descends through four positions; therefore its top-line cell is the unique unused cell of the 5×5 product.

For a deterministic 25-cell computational table, place the sole out-of-system character `h` into that sole unused cell. **This is a computational completion, not a historical claim that Sloane encoded `h` with that note.**

Use pitch rows low→high:

- p0 bottom line
- p1 lower space
- p2 middle line
- p3 upper space
- p4 top line

Use style columns S0..S4 in the historical family order above.

Frozen plaintext table by `(style, pitch low→high)`:

- S0: `a e i o u`
- S1: `l m n r s`
- S2: `b c d f g`
- S3: `t q p k h`  (historical `k,p,q,t` occupy p3,p2,p1,p0 respectively; p4 is canonical-completion `h`)
- S4: `x y z et con`

`et` and `con` are emitted as multi-letter plaintext tokens; scoring expands them to characters `et` / `con`. Thus one Voynich token can emit 1, 2, or 3 Latin letters under this historical code.

## Voynich representation

Use unchanged Zattera parser and ZL3b input from Issue26E.
Primary parser: `min`; `max` sensitivity only.

Exactly two adopted Zattera slots have five raw states including EMPTY:

- slot3: `EMPTY,t,k,p,f`
- slot5: `EMPTY,cth,ckh,cph,cfh`

These are the only five-state factors used.

## Track A — literal canonical application

No language-model fitting.

Evaluate exactly four deterministic axis/order conventions:

1. slot3=style, slot5=pitch, both grammar order low→high;
2. slot3=style, slot5=pitch, pitch order reversed;
3. slot5=style, slot3=pitch, both grammar order low→high;
4. slot5=style, slot3=pitch, pitch order reversed.

The raw grammar order for each slot is exactly the order listed above. Style family order is never permuted in Track A.

Decode every parseable token. Physical line boundaries and unparseable tokens break streams. Emit representative plaintext streams and objective Latin diagnostics.

Track A exists to answer the most literal practical question: does the known cipher read without a fitted key?

## Track B — strongest training-only application

To give the historical scheme a generous but auditable chance, use five physical-leaf folds.

For each fold, training data may choose:

- which of slot3/slot5 is style vs pitch: 2 choices;
- all 5! mappings of the style slot raw states to S0..S4;
- all 5! mappings of the pitch slot raw states to p0..p4.

Total: `2 × 120 × 120 = 28,800` keys per fold.

Key choice uses only 4/5 training leaves. Held-out leaves are decoded after the key is frozen.

## External language model

Reuse the exact frozen CREMMA medieval-Latin corpus from E8/E9:

- commit `292525969ad98380b398e6606a9c2a36d51913ae`;
- BIS-193, CLM13027, Mazarine915, UBL758;
- lowercase ASCII; `j→i`, `v→u`;
- unsupported characters break runs.

Unlike E9's Philip 20-letter alphabet, Sloane output includes `h`, `x`, `y` and expands `et`/`con`; therefore train the Latin model over normalized `a-z` after `j→i`, `v→u`, with observed alphabet fixed before Voynich scoring.

Use additive-smoothed character 4-gram cross-entropy (`alpha=.1`). Lower bits/character is more Latin-like.

For computational efficiency, training-key selection may aggregate raw `(style_state,pitch_state)` 4-gram counts before evaluating all 28,800 keys, but the decoded sequence and objective must be exactly equivalent to explicit decoding.

## Diagnostics

For Track A and held-out Track B emit:

- mean cross-entropy bits/character;
- decoded character count and stream count;
- character-frequency table;
- 50 most frequent decoded 4-grams with Latin-corpus counts;
- first 20 streams length >=12 per fold/population, cap 100 characters;
- longest exact normalized Latin lexicon substrings length >=4, with corpus frequency and context.

No manual respacing, anagramming, Caesar shifts, spelling substitutions, or folio cherry-picking.

## Frozen interpretation

### `DIRECT SLOANE PLAINTEXT LEAD`
Only if Track A contains at least one deterministic convention satisfying all:

1. mean CE is within `0.30 bits/char` of a held-out Latin self-baseline computed from the frozen corpus;
2. at least 10 distinct exact lexicon hits of length >=6 occur in coherent non-overlapping contexts;
3. visual inspection shows multiword-looking diversity rather than collapse to <=5 dominant characters.

### `FITTED SLOANE PLAINTEXT LEAD`
Only if Track A fails but Track B primary `min` satisfies all:

1. exact full key recurs in >=4/5 folds;
2. mean held-out CE is within `0.50 bits/char` of the Latin self-baseline;
3. at least 10 distinct held-out exact lexicon hits length >=6 occur across >=3 folds;
4. decoded streams do not collapse to <=5 characters accounting for >=80% of output.

### `NO READABLE SLOANE PLAINTEXT`
Otherwise.

These gates are intentionally practical rather than proof-of-cipher gates. E10 asks whether a known near-period musical cipher actually yields readable material.

## Boundaries

- Sloane 351 is later than Voynich and cannot by itself establish provenance.
- The `h` completion is explicitly computational and cannot count as historical evidence.
- Do not modify the table after seeing Voynich output.
- Do not try other language models/languages after reveal and call them E10.
- A fitted-key lead is exploratory and requires independent replication before any decipherment claim.
- Keep E10 on its dedicated branch/draft PR; do not merge to main without explicit user authorization.
