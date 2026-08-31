# Issue #26 direct-music research closure audit

Status: **CURRENT BOUNDED RESEARCH PROGRAM COMPLETE — DIRECT MUSICAL ENCODING NOT SUPPORTED BY TESTED MODELS**

## Scope

Issue #26 asked whether Voynichese could directly encode musical events, a music-theoretical state system, or plaintext through a musical cipher layer. It is separate from Issue #25, where music-analysis methods may be useful as generic sequence-analysis tools without implying musical content.

The current program has reached a defensible stopping boundary for model families that can be specified independently and tested without open-ended remapping.

This is not a proof that no imaginable musical encoding can occur anywhere in the manuscript. It closes the current falsifiable program because tested mechanisms are negative and the main remaining variants lack an independently fixed manuscript-side observable or an auditable historical key.

## Evidence by family

### H1 — finite-state musical event code

The direct screen compared sequence-blind 6/7-state Voynich reductions with medieval plainchant and structured Latin under held-out cadence/motif diagnostics.

Result: **DIRECT-MUSIC SCREEN NEGATIVE**. Voynich was closer to Latin than chant in all five physical-leaf folds; chant had strong terminal/cadential concentration that Voynich lacked.

### H2 — Guidonian / solmization state system

E–E6 found static compatibility between a six-state Voynich factor and some features of the Guidonian 20×6 lattice, but stronger controls showed mathematical non-uniqueness, selection sensitivity and non-musical sufficiency.

E7 then tested a prospective consequence not used to fit the mapping: historical overlapping-hexachord / same-pitch mutation dynamics on held-out order.

Result: **STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS**. The surviving object is generic morphology/dependency structure, not evidence that the states are literal Guidonian pitches or voces.

### H3 — music theory / musica mundana / astronomical relation

The externally fixed Ptolemaic same-tonos zodiac pairing was not supported (`p=.7143`). Generic zodiac angular geometry was stopped as non-identifying because an ordinary zodiac already contains the same opposition/trine/square relations. The explicit public `daiin/aiin + f67r2 + f113r/Veni Creator` package also failed its frozen components.

### H4 — music as intermediate cipher

Multiple structurally distinct historical mechanisms were tested rather than repeatedly retuning one decoder:

- Nicholas Philip 1436: duration-group near-hit explained by vowel isolation; exploratory full decoder produced no coherent medieval-Latin plaintext;
- Sloane MS 351 5×5: no readable plaintext;
- León / 23-family monoalphabetic substitution: validated solver; low CE but unstable key and unreadable output; E11F found a genuine Voynich-order effect; E11G showed that effect is not specific to genuine Latin order and all 200 matched pseudo-Latin models fit held-out Voynich better in raw CE;
- Porta 11×2: no readable plaintext despite exact positive-control recovery;
- Öttingen sequential dyad: negative / collapse-dominated;
- Kircher 6×4: negative;
- Bacon biliteral: negative under validated positive control and fully refitted nulls;
- Friderici pure rhythm: negative;
- Friderici 8×3 grid: negative after exact positive-control validation.

The León sequence is especially important methodologically: a low fitted language-model CE is not enough to identify a Latin plaintext model. The final residual is a sequence/model-identifiability question, not a decipherment.

## Untested remainder

### Martinus Polonus

Historically relevant and chronologically attractive, but no complete auditable exact key was recovered in the research pass. Reconstructing one after looking at Voynich target statistics would violate the source-first rule.

Disposition: **future trigger if an exact key becomes available**.

### Generic tablature / mensural / multivoice schemes

Historical possibility is real, but no independent Voynich feature currently fixes pitch versus duration, seven-note/register mapping, voice separation, rhythmic semantics, clef/register anchor, or transformation rule before target inspection.

Disposition: **under-specified / non-identifying without a new external anchor**.

### Generic music-cosmology correspondences

Circular geometry alone is non-identifying. A future test requires an additional independently specified label, textual marker, or graphical relation that distinguishes a musical diagram from an ordinary astronomical/astrological one.

## Stopping rule

Do not continue Issue #26 by adding named ciphers or musical mappings one at a time merely because another historical example can be found.

Reopen only when at least one of the following exists before looking at a new target score:

1. an auditable exact historical key;
2. a manuscript-local feature that independently selects pitch/duration/voice/cipher mapping;
3. a finite historical candidate family whose complete membership and family-level multiplicity are frozen in advance;
4. a new historical source that supplies a genuinely new testable consequence.

Without such a constraint, continued search mainly increases researcher degrees of freedom.

## Residuals moved out of music interpretation

Three observations remain scientifically useful but must leave the music hypothesis:

- **E10 slot3×slot5 recurrence:** test native 5×5 cross-leaf dependency under hypothesis-neutral frequency-preserving controls, excluding the Sloane table and Latin/music objectives.
- **E11 STA-family order residual:** characterize the manuscript-native local sequential constraints that separate real order from matched order nulls, without León/Latin substitution rescue models.
- **E–E7 six-state factor:** explain the stable morphology/dependency regularity with generic token-grammar models rather than literal solmization/pitch labels.

## Closure conclusion

> **No tested, independently constrained direct-musical or music-cipher model provides held-out evidence that Voynich running text encodes music or readable plaintext through a musical state system. Several apparent static or low-CE fits were eliminated by prospective historical predictions, stronger matched nulls, solver validation, readability checks, or identifiability controls.**

The experiment-level branches remain research evidence. This documentation PR proposes only the consolidated interpretation and stopping boundary for `main`; it does not merge the individual exploratory experiment branches wholesale.
