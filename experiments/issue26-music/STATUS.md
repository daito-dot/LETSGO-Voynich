# Issue #26 direct-music research status

Updated after Issue26E8 first reveal.

| Track | Direct question | Result | Narrow interpretation |
|---|---|---|---|
| A | Do visible Voynich tokens reduced sequence-blind to 6/7 finite states reproduce medieval plainchant cadence/motif geometry? | **NOT SUPPORTED** | 0/5 folds closer to chant; Voynich much closer to structured medieval Latin under frozen screen. |
| B | Do surviving zodiac labels preferentially group Ptolemy *Harmonics* III.12 same-tonos zodiac pairs? | **NOT SUPPORTED** | target rank 75/105, exact p=.714 after production-order correction. |
| C | Can Ptolemy III.8–9 interval↔zodiac geometry itself identify musical encoding? | **NON-IDENTIFYING AS STATED** | ordinary zodiac geometry already contains opposition/trine/square angular relations; requires an extra independent observable. |
| D | Does the March-2026 public `daiin=octave` / f67r2 / f113r *Veni Creator* package survive literal and multiplicity-aware audit? | **NOT SUPPORTED** | 0/4 frozen components pass. |
| E | Does Zattera slot10 as a six-state channel plus k=20 remaining morphology fit the Guidonian 20×6 admissibility lattice? | **NARROW STATIC POSITIVE, LATER REFINED** | Guidonian beat ordinary degree-matched nulls under full refit, but `20` is hypothesis-side and later stronger controls remove primary specificity. |
| E2 | Does E survive higher null resolution, IT2a transcription, and fixed-map transfer? | **NUMERIC STATIC REPLICATION, LATER REFINED** | architecture-level means replay across ZL/IT; E5 shows the large fixed-map transfer surprise was not selection-adjusted evidence for Guidonian specificity. |
| E3 | Does fixed-map transfer require Guidonian higher-order neighborhoods? | **MATHEMATICAL NON-UNIQUENESS** | exact-pair non-Guidonian alternatives can equal/beat Guidonian. This does not establish real-world prevalence of such structures. |
| E4 | Can a purely non-musical topology learned from Voynich transfer to another transcription? | **NON-MUSICAL SUFFICIENCY, ASYMMETRIC** | ZL-learned topology transfers well to IT, but Voynich→Voynich self-learning is not a fair external-origin likelihood comparison. Draft PR #34 remains unmerged. |
| E5 | After matching the ZL parser/map selection freedom used to obtain E2-C, is Guidonian fixed-map transfer unusual? | **SELECTION FREEDOM EXPLAINS FIXED-MAP SURPRISE** | 86/200 degree-matched alternatives transfer at least as well as Guidonian (`p≈.433`). Draft PR #36 remains unmerged. |
| E6 | Under full per-fold 720-map refitting, does Guidonian beat stronger pair-overlap-matched mathematical alternatives? | **PRIMARY STATIC SPECIFICITY FAILS** | `min`: structured-null p=.376 (ZL), .525 (IT). `max` retains a narrow static topology-class preference. Draft PR #37 remains unmerged. |
| E7 | Does the sequence-blind static Guidonian mapping prospectively predict historical hexachord/mutation dynamics? | **STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS** | ZL/min D1 p=.515, mutation D2 p=.253; `max` and IT sensitivities also negative. Draft PR #38 remains unmerged. |
| E8-A | Is the 1436 Nicholas Philip four-duration alphabet partition unusually compatible with a natural four-state Voynich slot, versus equal-capacity external alphabet partitions? | **PHILIP DURATION-GROUP NOT SUPPORTED; STABLE NEAR-HIT** | `min`: target D=.19130 vs null median .28564, 5/5 fold median wins and identical slot0/key in 5/5, but frozen p=.06294 fails the `.05` gate. Strongest alternative is generic vowel-group structure. |

## Current interpretation

Issue #26 does **not** support visible Voynich running text as a literal Guidonian musical sequence. E7 is the cleanest falsification of that direct reading because the static mapping failed to predict historical musical dynamics that were not used to fit it.

The robust positive object from E/E2 remains narrower:

> Under the adopted Zattera slot decomposition, Voynich contains a six-state morphological/dependency factor, and a Guidonian 20×6 table can fit that static factor well under some comparison families.

But E3–E6 establish mathematical flexibility/non-uniqueness, and E7 shows that interpreting the static fit as actual Guidonian pitches/voces does not predict held-out order.

E8 therefore moved to a different model family rather than rescuing the Guidonian mapping: historically attested music-as-cipher.

## E8-A — Nicholas Philip 1436 intermediate-cipher screen

The tested historical construction has four duration groups of five letters:

- `aeiou`
- `bcdfg`
- `klmnp`
- `qrstz`

The full five-pitch × four-duration product was **not** tested, because a generic 5×4 product is only a twenty-symbol substitution code unless a historical feature first predicts something new.

E8-A compared the historical four-way alphabet partition against 1,000 deterministic alternative partitions of the same twenty letters into four equal groups of five. Every target/null partition received identical training-only freedom to choose among the three natural four-state Zattera slots and all 24 state↔group bijections before held-out scoring.

Primary `min`:

- Philip mean held-out JSD distance: `0.1912990849`;
- null median: `0.2856364100`;
- null q05: `0.1862773689`;
- null minimum: `0.1241821903`;
- lower-tail p: **`.0629370629`**;
- target beats null-fold median: **5/5**;
- exact target key recurrence: **5/5**;
- recurrent key: slot0, permutation `[0,3,1,2]`.

So the observed pattern is stable and substantially better than the typical equal-capacity partition, but it fails the preregistered significance gate. It must remain classified:

**`PHILIP DURATION-GROUP NOT SUPPORTED`**.

The `max` sensitivity is weaker (`p=.142857`) despite 5/5 fold direction and key recurrence.

## Why E8-A is still worth following up

The near-hit has a major non-musical alternative explanation: Philip's first group is exactly the five Latin vowels `aeiou`.

Random equal-capacity null partitions normally destroy the vowel class. Therefore a stable four-state match could be caused by **generic vowel-vs-consonant sequence structure**, not by Philip's musical-cipher design.

The next high-information control is therefore external and adversarial:

> Fix `aeiou` as one group in every comparator, and vary only the remaining fifteen consonants among three five-letter groups. Ask whether Philip's exact consonant groups `bcdfg / klmnp / qrstz` remain unusually close under the same training-only Voynich slot/key search.

This is a stronger interpretation test than increasing random-null resolution or immediately testing the reserved five-pitch dimension.

If the effect collapses, the E8-A near-hit is explained by vowel isolation and should not motivate a Philip-like cipher claim.

If it survives a vowel-fixed control, only then is a new prospective cipher-specific test warranted. The full pitch dimension still requires separate preregistration and cannot rescue the already-negative E8-A result.

## Research boundaries

- Do not retune E7 sequence rules or promote `max`.
- Do not reinterpret E8-A as positive because it has 5/5 stability; `p=.06294` failed the frozen gate.
- Do not run the five-pitch E8-B as a rescue after the negative E8-A classification.
- Do not claim that constructed E3–E6 alternatives establish real-world base rates.
- Preserve the distinction between mathematical non-uniqueness, historical theory-internal prediction, and external historical cipher comparison.
- No current Issue #26 result identifies plaintext, melody, pitches, rhythm, or a decipherment.
