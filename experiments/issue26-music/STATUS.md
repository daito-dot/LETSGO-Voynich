# Issue #26 direct-music research status

Updated after Issue26E8-A2 first emitted reveal.

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
| E8-A | Is the 1436 Nicholas Philip four-duration alphabet partition unusually compatible with a natural four-state Voynich slot, versus equal-capacity external alphabet partitions? | **PHILIP DURATION-GROUP NOT SUPPORTED; STABLE NEAR-HIT** | `min`: target D=.19130 vs null median .28564, 5/5 fold median wins and identical slot0/key in 5/5, but frozen p=.06294 fails the `.05` gate. |
| E8-A2 | Conditional on keeping `aeiou` intact, is Philip's exact consonant subdivision special among all 126,126 equal 5+5+5 consonant partitions? | **VOWEL ISOLATION EXPLAINS E8A NEAR-HIT** | Philip rank 61,261/126,126, conditional p=.4857, only 3/5 fold median wins. The exact historical consonant subdivision is ordinary once vowels are fixed. |

## Current interpretation

Issue #26 does **not** support visible Voynich running text as a literal Guidonian musical sequence. E7 is the cleanest falsification of that direct reading because the static mapping failed to predict historical musical dynamics that were not used to fit it.

The robust positive object from E/E2 remains narrower:

> Under the adopted Zattera slot decomposition, Voynich contains a six-state morphological/dependency factor, and a Guidonian 20×6 table can fit that static factor well under some comparison families.

But E3–E6 establish mathematical flexibility/non-uniqueness, and E7 shows that interpreting the static fit as actual Guidonian pitches/voces does not predict held-out order.

E8 moved to a genuinely different model family rather than rescuing the Guidonian mapping: historically attested music-as-cipher.

## E8-A — Nicholas Philip 1436 intermediate-cipher screen

The tested historical construction has four duration groups of five letters:

- `aeiou`
- `bcdfg`
- `klmnp`
- `qrstz`

The full five-pitch × four-duration product was deliberately **not** tested. A generic 5×4 product is only a twenty-symbol substitution code unless a historical feature first predicts something new.

E8-A compared the historical four-way alphabet partition against 1,000 deterministic alternative partitions of the same twenty letters into four equal groups of five. Every target/null partition received identical training-only freedom to choose among the three natural four-state Zattera slots and all 24 state↔group bijections before held-out scoring.

Primary `min`:

- Philip mean held-out JSD distance: `0.1912990849`;
- null median: `0.2856364100`;
- lower-tail p: **`.0629370629`**;
- target beats null-fold median: **5/5**;
- exact target key recurrence: **5/5**;
- recurrent key: slot0, permutation `[0,3,1,2]`.

So the pattern was stable but failed the preregistered significance gate. The frozen result remains:

**`PHILIP DURATION-GROUP NOT SUPPORTED`**.

The stability nevertheless justified one adversarial explanation test because the target's first group is exactly the five Latin vowels.

## E8-A2 — exhaustive vowel-fixed control

E8-A2 fixed `aeiou` in **every** comparator and exhaustively enumerated every unordered partition of the remaining fifteen consonants into three groups of five.

Complete universe:

**126,126 partitions** including Philip.

Primary `min`:

- Philip target D: `0.1912990849`;
- exhaustive-universe median: `0.1921073411`;
- strict rank: **61,261 / 126,126**;
- conditional p: **`.4857127000`**;
- fold median wins: **3/5**;
- target key remains slot0 / `[0,3,1,2]` in 5/5 folds.

The best non-Philip partition,

`aeiou | bfgkz | cdnst | lmpqr`,

reaches D=`0.1071589913`, far closer than Philip, and itself has a 5/5 stable slot6 key.

The `max` sensitivity is less favorable still:

- conditional p=`.5772640058`;
- fold median wins=`0/5`.

Therefore the E8-A near-hit is not specific to Nicholas Philip's musical-cipher consonant grouping. Once the obvious linguistic condition `aeiou` is held fixed, Philip is approximately a median member of the complete candidate universe.

Frozen E8-A2 classification:

**`VOWEL ISOLATION EXPLAINS E8A NEAR-HIT`**.

This is a mechanistic explanation of the near-hit, not merely a failure to cross `.05`.

## What E8-A2 changes

The specific 1436 Philip intermediate-cipher hypothesis is now **not supported** at the duration-group signature level.

Do **not** run the reserved five-pitch E8-B as a rescue. The pitch stage was gated behind a positive duration-group necessary condition; that condition failed, and E8-A2 identifies a straightforward non-musical reason for the apparent stability.

There is a potentially useful non-music observation embedded here:

> a natural four-state Voynich slot can show stable sequence-level compatibility with a Latin partition that isolates vowels from consonants.

That observation belongs to a linguistic/morphological hypothesis family, not to evidence for a musical cipher. It should only be developed elsewhere with its own controls if it is scientifically useful.

## H4 research boundary after E8

H4 — music as an intermediate cipher — is not globally falsified by the failure of one historical scheme. However, testing historical musical ciphers one by one until one happens to fit would create a new uncontrolled model-selection problem.

Before testing another cipher, one of the following must be true:

1. a **finite historically justified candidate family** is frozen before seeing any new Voynich score, with multiplicity charged across the whole family; or
2. an independent manuscript-local visual/textual anchor selects a specific historical cipher family before the text statistic is inspected.

Without one of those selectors, do not proceed by opportunistically trying Martinus Polonus, Sloane 351, or later musical ciphers in sequence.

## Research boundaries

- Do not retune E7 sequence rules or promote `max`.
- Do not reinterpret E8-A as positive because it has 5/5 stability; `p=.06294` failed the frozen gate.
- Do not run the five-pitch E8-B after E8-A2.
- Do not claim constructed E3–E6 alternatives establish real-world base rates.
- Preserve the distinction between mathematical non-uniqueness, historical theory-internal prediction, and external historical cipher comparison.
- No current Issue #26 result identifies plaintext, melody, pitches, rhythm, or a decipherment.
