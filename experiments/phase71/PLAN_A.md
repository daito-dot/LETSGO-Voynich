# Phase 71A — source-grounded Alberti boundary-signal test

Status: **FROZEN BEFORE ANY PHASE71 VOYNICH SCORE**

Date: 2026-08-31

Pre-science representation correction: the first draft treated Alberti's capital alignment signal as a standalone token. Before implementation or any Phase71 score, this was replaced by the more conservative rule below: a capital signal is **prefixed to the following encrypted plaintext word inside the same token**. Alberti's example writes the signal intermingled in the ciphertext rather than establishing it as a separate word. This preserves one output token per retained plaintext word and prevents an invented one-character token from trivially changing line-entry token counts. This correction is frozen before science.

## Motivation

Phase70 showed a sharp mechanistic split. An exactly recoverable meaningful-plaintext construction with the already-frozen A1 local selector reproduced the tested short-range recurrence / H62 regime and aggregate line-position structure, but it reached only about `0.151×` of the Voynich paragraph-entry projection. The blinded Phase70 Route P forbids tuning that construction or inventing `SC2` to repair the entry failure.

Phase71 therefore changes scientific question.

> Can a **historically attested, independently specified boundary-indicator/reset mechanism** produce a Voynich-direction paragraph-entry effect in meaningful ciphertext, without importing the A1 entry model?

The test is a source-grounded mechanism control, not a continuation or repair of Phase70.

## Historical anchor

Leon Battista Alberti's *De componendis cifris* / *De cifris* (1466–1467) describes a rotating cipher disk with a stationary 24-position ring and a movable 24-symbol ring. In the first method, a capital letter in the ciphertext signals the current disk alignment. Alberti explicitly says that after three or four words the sender may rotate the disk and insert a new capital signal to announce the changed alphabet.

The exact alphabets used here are the published/transcribed example:

- stationary ring: `ABCDEFGILMNOPQRSTVXZ1234`
- movable ring: `gklnprtuz&xysomqihfdbace`
- movable index: `k`

Historical references used only to freeze the mechanism:

- Alberti first-method quotation / teaching transcription: https://sites.wcsu.edu/mbxml/html/section_alberti.html
- historical discussion of the 1466–1467 disk and rotating alphabets: https://research-information.bris.ac.uk/ws/portalfiles/portal/263833703/Myths_and_Histories_of_the_Spartan_scytale_29_11_2020.pdf
- 15th-century Italian cipher-key context: Judit W. Somogyi (2016), *Caratteristiche strutturali di cifrari monoalfabetici italiani nei secoli XV e XVI*, https://ojs.ppke.hu/verbum/article/view/405

Chronology caveat: Alberti's surviving description is later than the Voynich vellum radiocarbon range. Phase71 uses it as a near-period **mechanism control**, not evidence that the Voynich manuscript used Alberti's disk.

## Hypothesis P71-AB1

If a paragraph behaves like an independently initialized ciphertext unit, a historically valid initial alignment signal + alphabet reset may generate a stable paragraph-entry state even when the underlying plaintext is meaningful.

The primary causal comparison is between two uses of the same Alberti mechanism on the same medieval Latin source panel.

### Arm `CONT`

Treat each manuscript as one continuous cipher message:

- one initial capital alignment signal at the start of the manuscript;
- change alphabet after every **4 plaintext words**;
- emit the required capital signal at every change;
- paragraph boundaries are preserved in layout but have **no cryptographic effect**.

### Arm `PARA`

Treat each source paragraph/pilcrow item as a fresh cipher message:

- emit a fresh initial alignment signal on line 0 of every paragraph;
- reset the disk alignment at every paragraph boundary;
- within each paragraph, change alphabet after every **4 plaintext words**, with the same historical signal convention.

Thus the scientific intervention is the historically valid **message-initial signal + reset bundle applied at paragraph boundaries**.

The experiment does not claim that Voynich paragraphs are messages. It asks whether this independently attested mechanism class is sufficient to generate the missing formal signature.

## Plaintext panel

Use the exact frozen equal-weight four-manuscript CREMMA medieval Latin panel already used in Phase62/64/69/70:

- BIS193
- CLM13027
- Mazarine915
- UBL758

Authority commit remains:

`HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`

Voynich target authority remains the exact frozen ZL3b source used by Phase62–70:

`matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c`

with Git blob for `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`:

`2a4533ab9bdfa85db9bad602d590978953055df1`

No Phase71 selection may use IT/GC or any additional Voynich transcription.

## Plaintext projection

Alberti's stationary alphabet is smaller than normalized modern Latin. Before encryption each source word is independently projected as follows:

1. Unicode NFKD decomposition;
2. remove combining marks;
3. lowercase;
4. `j -> i` and `u -> v`;
5. retain only `abcdefgilmnopqrstvxz`;
6. drop an empty projected word.

No word is expanded, guessed, translated or supplied from Voynich outcomes.

The projection diagnostics (source words, retained words, retained characters, dropped characters/types) must be recorded.

## Cipher construction

### Disk alignment

For any chosen capital indicator `C` from the 20 stationary letters, rotate the movable ring so its fixed index `k` lies under `C`. Plaintext letters on the stationary ring map positionally to movable-ring symbols.

### Indicator choice

Indicator capitals are not optimized.

For each manuscript × realization × signal event, choose the capital by a deterministic SHA-256-derived pseudorandom index over the 20 stationary letters. The seed namespace and event index are fixed in code before science. Within one message, a periodic alphabet change is forced to a different alignment from the current one if the deterministic draw happens to repeat it.

### Word/token representation

- each retained plaintext word produces exactly **one** ciphertext token;
- ordinary token content is the encrypted movable-ring symbol sequence for that plaintext word;
- when Alberti requires an alignment signal before a word, the uppercase signal unit is **prefixed to that encrypted word inside the same token**;
- therefore an initial signal modifies the first retained token of a message rather than creating an extra token;
- source paragraph and line layout is preserved;
- no optional Alberti nulls, numeral supercipher or nomenclator is used because their placement/use is not uniquely fixed by the historical rule needed here.

### Realizations

Use exactly **5 deterministic realizations per manuscript per arm**. Realization randomness affects only independently allowed alignment choices, never the Voynich target or scoring.

## Frozen scorecard

Reuse the exact Phase62/63/64 scoring machinery without changing metric definitions:

- **S1** paragraph-entry projection is primary;
- S2 previous-10 near-family excess is descriptive;
- S3 aggregate line-position eta2 is descriptive;
- H62-P1 recurrence profile is descriptive.

The Voynich S1 direction remains training-leaf derived exactly as in the frozen prior machinery. No Phase71 direction is learned from the control ciphertexts.

### Primary statistic

For each arm, compute the ratio of equal-manuscript mean candidate S1 to the held-out Voynich mean S1 using the same five physical-leaf target folds.

Define:

- `R_CONT` = continuous-message S1 ratio;
- `R_PARA` = paragraph-reset S1 ratio.

Primary paired improvement:

`abs(R_PARA - 1) < abs(R_CONT - 1)`.

Count the number of target folds in which the `PARA` candidate S1 projection is strictly positive.

## Frozen positive gate

Classify **`P71-AB1 BOUNDARY-SIGNAL MECHANISM DEMONSTRATED`** only if all hold:

1. `0.5 <= R_PARA <= 2.0`;
2. `PARA` has positive S1 projection in at least **4/5** target folds;
3. `abs(R_PARA - 1) < abs(R_CONT - 1)`;
4. `R_PARA > R_CONT`.

These gates concern S1 only. S2/S3/H62 cannot rescue a failed primary gate.

If conditions 3 and 4 pass but either 1 or 2 fails, classify:

`P71-AB1 BOUNDARY-SIGNAL PARTIAL`.

Otherwise classify:

`P71-AB1 BOUNDARY-SIGNAL NOT SUPPORTED`.

## Predeclared sensitivity

Repeat both arms with Alberti's equally attested **3-word** alphabet-change interval.

This is sensitivity only:

- it cannot rescue a failed 4-word primary;
- no best-of-3/4 interval selection is allowed;
- report it regardless of direction.

## Preflight before first score

Before any Phase71 scientific score is authorized, verify without calling S1/S2/S3/H62:

1. exact ZL and CREMMA authorities;
2. exact ring lengths `24/24` and unique movable symbols;
3. index `k` exists exactly once;
4. for every capital alignment, all 20 plaintext letters map one-to-one to 20 movable symbols;
5. deterministic reproducibility of indicator sequences/ciphertext;
6. `PARA` prefixes exactly one message-initial indicator per nonempty paragraph;
7. `CONT` prefixes no paragraph-boundary reset after the first nonempty manuscript item;
8. identical projected plaintext word sequence and output token count in paired arms;
9. every retained output token contains at least one encrypted data unit even when prefixed by a signal;
10. no plaintext recovery claim is made here; this is a deterministic substitution-control construction.

Preflight must print **`NO PHASE71 SCIENTIFIC SCORE COMPUTED`**.

## Falsification and claim boundary

A negative result means only that this exact historically grounded boundary-signal/reset control does not reproduce the Voynich paragraph-entry direction strongly enough.

A positive result means only:

> a historically attested message-initial indicator/reset mechanism is sufficient, when applied at paragraph boundaries, to place meaningful ciphertext in the Voynich paragraph-entry regime under the frozen S1 statistic.

It would **not** establish:

- that Voynich paragraphs are separate messages;
- that Alberti's disk was used historically for the manuscript;
- a plaintext language;
- a cipher key;
- semantic content;
- decipherment.

No interval, alphabet, projection, indicator policy, paragraph/message mapping, metric or threshold may be changed after first reveal to improve the result.
