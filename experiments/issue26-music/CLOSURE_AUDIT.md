# Issue #26 direct-music research closure audit

Status: **CURRENT BOUNDED RESEARCH PROGRAM COMPLETE — DIRECT MUSICAL ENCODING NOT SUPPORTED BY TESTED MODELS**

## Scope of this closure

Issue #26 asked whether Voynichese could directly encode musical events, a music-theoretical state system, or plaintext through a musical cipher layer. It deliberately separated that question from Issue #25, where music-analysis methods are used only as generic sequence-analysis tools.

This document audits whether the current Issue #26 program has reached a defensible stopping boundary.

The answer is yes for the model families that can currently be specified independently and tested without open-ended remapping.

This is **not** a universal proof that no imaginable musical encoding could occur anywhere in the manuscript. It is a closure of the present falsifiable research program: the tested direct-music mechanisms are negative, and the main remaining variants lack an independently fixed manuscript-side observable or an auditable historical key. Continuing by trying additional mappings after each failure would turn the project into uncontrolled model search.

## Evidence by hypothesis family

### H1 — visible-token / finite-state musical event code

The first direct-music screen reduced Voynich tokens to sequence-blind finite musical states and compared held-out cadence/motif behavior with real medieval plainchant and nonmusical language controls.

Frozen result: **`DIRECT-MUSIC SCREEN NEGATIVE`**.

Voynich was closer to medieval Latin than to chant in all five physical-leaf folds. Chant showed strong terminal-state and terminal-transition concentration; Voynich did not. Six-state solmization sensitivity and paragraph-final-line checks remained negative.

Interpretation: the tested visible-token→monophonic finite-state reading does not reproduce the most basic phrase/cadence geometry of the musical comparator.

### H2 — Guidonian / solmization-like state system

E through E6 found that a six-state Voynich morphological factor could be fitted statically to a Guidonian 20×6 lattice under some weaker comparator families. Stronger controls then showed substantial mathematical non-uniqueness and selection sensitivity.

E7 supplied the decisive theory-internal prospective test. After the static mapping was learned without order information, the unused historical consequences of actual Guidonian organization — overlapping hexachords, pitch identity, and legal same-pitch mutation — were tested on held-out Voynich order.

Frozen result: **`STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS`**.

Primary ZL/min:

- dynamic compatibility observed `.53601` vs order-null median `.53608`, p=`.5155`;
- mutation-specific legality observed `.42768` vs null `.42564`, p=`.2531`;
- no parser/transcription sensitivity produced a prospective dynamic effect.

Interpretation: the retained resemblance is static/formal rather than evidence that the fitted cells are literal Guidonian pitches/voces.

### H3 — music theory / musica mundana / astronomical relation

The Ptolemaic same-tonos zodiac-pair audit used an externally fixed historical relation and exact matching controls.

Result: **NOT SUPPORTED** (`p=.7143`, target rank 75/105).

A second design audit found that generic 12-fold zodiac geometry cannot identify music by itself: opposition/trine/square angular relations exist in an ordinary zodiac whether or not musical meaning is encoded. This was stopped as **non-identifying as stated**, not counted as a negative statistical result.

The explicit public `daiin/aiin + f67r2 + f113r/Veni Creator` package was also reconstructed adversarially and failed all four frozen components.

Interpretation: the clean externally specified astronomy/music candidates tested so far do not organize the Voynich labels, while generic zodiac-angle correspondences lack identifying power without an additional independent observable.

### H4 — music as intermediate cipher / mnemonic carrier

The historical-cipher series deliberately moved across structurally different mechanisms instead of repeatedly tuning one decoder.

Tested families include:

- Nicholas Philip 1436 four-duration partition: not supported; exhaustive vowel-fixed control showed the apparent near-hit was explained by isolating `aeiou`, not Philip's consonant subdivision;
- Philip explicit decode: no readable plaintext;
- Sloane MS 351 5×5 code: no readable plaintext;
- Öttingen/Wallerstein 5×5 and sequential-dyad mechanisms: negative / collapse-dominated;
- Porta 11×2: no readable plaintext despite exact synthetic solver recovery;
- León / Visigothic-style 23-family monoalphabetic substitution: E11F found a real Voynich order residual, but the key was unstable and output unreadable; E11G then showed that genuine Latin order is not specific — all 200 frequency/run-length-matched pseudo-Latin models fit held-out Voynich better in raw CE;
- Kircher 6×4: negative;
- Bacon biliteral binary carrier: negative under a fully validated solver and refitted nulls;
- Friderici pure-rhythm ternary mechanism: negative;
- Friderici separate 8×3 tone/motif×repetition mechanism: negative after 60/60 exact-key positive-control folds; held CE `4.5099` vs Latin `2.4516`, top-five `.7523` vs `.5102`, zero >=6 CREMMA substrings.

The León result is particularly useful methodologically: low fitted character 4-gram CE is not sufficient to identify a Latin plaintext model. E11G converted what initially looked like a Latin-like residual into a broader model-identifiability/sequential-structure question.

## What remains untested and why it does not justify continued open-ended search

### Martinus Polonus 1277

The historical attribution is relevant and chronologically attractive, but the exact complete key has not been recovered in an auditable machine-readable form from the sources available in this research pass. Guessing or reconstructing the key from an unclear illustration after seeing Voynich statistics would violate the source-first rule.

Disposition: **eligible future trigger, not currently executable**.

### Generic medieval tablature / mensural / multi-voice schemes

The manuscript period contains alphabetic tablature, mensural notation and transformational/canonic practice. Those facts establish historical possibility, not a specific Voynich decoder.

At present there is no independent manuscript-local feature that fixes, before target inspection:

- which Voynich unit is pitch versus duration;
- a seven-note/register mapping;
- voice separation or simultaneity;
- rhythmic value semantics;
- a staff/clef/register anchor;
- a transformation instruction and its scope.

The ordinary running-text layout also lacks the explicit graphical/vertical organization that makes historical polyphonic or tablature readings identifiable.

Disposition: **under-specified / non-identifying without a new external anchor**. Do not manufacture a mapping from whichever slot cardinalities happen to fit.

### Generic music-cosmology correspondences

Circular/zodiacal geometry alone is not identifying. A future test needs an additional independently specified label relation, textual marker, or graphical relation that distinguishes a musical diagram from an ordinary astronomical/astrological one.

Disposition: **requires a new independent observable**.

## Stopping rule

Issue #26 should not continue by adding named historical ciphers or musical mappings one at a time merely because they can be found in the literature.

Reopen or extend the direct-music program only when at least one of the following is available **before** looking at a new Voynich target score:

1. an auditable exact historical key for a chronologically relevant candidate such as Martinus Polonus;
2. a manuscript-local visual/textual feature that independently selects a pitch/duration/voice/cipher mapping;
3. a finite historical candidate family whose complete membership and family-level multiplicity rule can be frozen in advance;
4. a new historical source that supplies a genuinely new, testable consequence not already absorbed by the failed model families.

Without one of these, further exploration would mainly increase researcher degrees of freedom.

## Residuals that survive but are not music evidence

Two observations should leave Issue #26 rather than be discarded.

### E10 slot3×slot5 recurrence

The failed Sloane 351 decoder selected the same complete slot3×slot5 axis/permutation key in 4/5 physical-leaf folds. Because the output was strongly collapsed and unreadable, this is not Sloane/music/plaintext evidence.

The pre-recorded non-musical follow-up is:

> Does the native 5×5 slot3×slot5 representation show cross-leaf predictive dependence / stable association beyond frequency-preserving controls?

That audit must exclude the Sloane table, Latin likelihood, `con`, and music-derived ordering.

### E11 STA-family order residual

E11F established that real within-segment STA-family order is strongly different from frequency- and segment-length-preserving order shuffles under the fitted objective. E11G established that genuine Latin order is not what makes that objective fit.

The surviving question is therefore hypothesis-neutral:

> What manuscript-native local sequential constraints make the 23-family STA stream different from matched order nulls?

Future work should use direct sequence models and matched controls rather than a León/Latin substitution decoder.

## Closure conclusion

The current evidence supports the following bounded conclusion:

> **No tested, independently constrained direct-musical or music-cipher model provides held-out evidence that Voynich running text encodes music or readable plaintext through a musical state system. Several apparent static or low-CE fits were eliminated by prospective historical predictions, stronger matched nulls, solver validation, or readability/identifiability checks.**

Issue #26 can therefore be closed as a completed negative research direction at the current evidence boundary.

The strongest surviving observations are manuscript-structure residuals and should continue in non-musical issues rather than be used to keep the music hypothesis alive.

No merge to `main` is authorized by this closure audit.
