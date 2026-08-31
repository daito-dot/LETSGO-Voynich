# Issue #26 direct-music research status

Updated after Issue26E9 target-only plaintext reveal.

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
| E9 | If the full Nicholas Philip 5×4 cipher is nevertheless used as an actual decoder, does held-out Voynich become readable medieval Latin? | **NO COHERENT PLAINTEXT IN TARGET-ONLY PROBE; STRONG LEAD GATE IMPOSSIBLE** | `min` pitch key recurrence only 3/5. About 8,701 held-out scored characters collapse mainly to repeated `i/s/m`; longest frozen Latin-lexicon hits are 5 chars and isolated. |

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

The full five-pitch × four-duration product was deliberately **not** tested in the confirmatory E8 path. A generic 5×4 product is only a twenty-symbol substitution code unless a historical feature first predicts something new.

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

## E9 — direct full-cipher decoding probe

E9 was added after the user explicitly asked a different practical question: even though E8 was negative as a hypothesis test, what happens if we simply use the historically established Philip mechanism as a decoder and ask whether meaning comes out?

This was preregistered as an **exploratory post-E8 probe**, not as a rewrite of E8.

The E8-A primary duration key was frozen:

- `EMPTY → aeiou`
- `q → qrstz`
- `s → bcdfg`
- `d → klmnp`.

The actual Philip pitch×duration table was then applied. Only the two natural five-state pitch slots (slot3 / slot5) and 120 pitch-rank bijections were available, giving 240 finite pitch keys per fold. Key selection used only 4/5 Voynich leaves and an external frozen medieval-Latin character 4-gram model; the remaining 1/5 leaves were decoded untouched.

### Primary `min`

Mean held-out cross-entropy:

`4.1174818542 bits/char`

All five folds select pitch slot5, but the exact permutation is not stable enough:

- `[2,3,1,0,4]` in 3/5 folds;
- `[2,1,3,4,0]` in 2/5 folds.

So exact key recurrence is **3/5**, below the preregistered >=4/5 requirement for a strong plaintext lead.

Across all five disjoint held-out folds:

- 8,701 characters receive a complete 4-gram score;
- 2,783 decoded streams are retained.

Representative untouched decoded streams are:

```text
iiiiismiemom
diismiisisim
iiiiisiidiii
iiiiiiidiiiis
misimrmismii
iiiiiimmmmii
isiiiiiiiiiiii
ssissiimeiii
diiisiimiiiim
miiieiimiiim
iiefmiisiiisi
sisiiiidimsmi
msmssiiimisi
diiesssmoisi
isisdioiisoi
dsrisiimddii
```

The output is visibly low-diversity and dominated by `i`, with secondary `s/m/d`, rather than ordinary Latin-looking plaintext.

The first 100 reported held-out sample streams contain 709 printed characters, approximately:

- `i`: 469
- `s`: 116
- `m`: 71
- `d`: 24
- `e`: 15
- `o`: 10
- everything else: 4.

The dominant held-out tetragrams are also poor matches to the external Latin corpus. In fold0, for example:

- `iiii`: decoded 244, Latin 6;
- `iiis`: decoded 67, Latin 0;
- `isii`: decoded 67, Latin 0;
- `iisi`: decoded 65, Latin 0;
- `siii`: decoded 59, Latin 0;
- `iiim`: decoded 33, Latin 0;
- `iimi`: decoded 31, Latin 0.

### Literal lexicon inspection

The frozen CREMMA supported-only lexicon contains 4,650 normalized entries. Across the held-out decoded streams, the longest exact dictionary substrings reported in any fold are only **5 characters**.

Examples include:

- `missi`, occurring inside `missiiii`, `mississssi`, `missisiii`;
- `ssioi`;
- 4-letter fragments such as `semi`, `meis`, `ssio`.

These do not join into coherent Latin syntax or multiword content. With thousands of tested positions, isolated 4–5-character dictionary substrings cannot be treated as decipherment evidence.

### `max` sensitivity

`max` gives lower numerical cross-entropy (`3.6200604640 bits/char`) but an even more obvious repeated-`i` plaintext collapse, e.g. `iiiiiiiiiiii`, `isiiiiiiiiiiii`, and again only 3/5 exact pitch-key recurrence. It does not rescue the result.

### E9 stopping point

The preregistered strong class `PLAINTEXT-LIKE PHILIP LEAD` requires exact pitch-key recurrence >=4/5. Primary E9 has only 3/5.

Therefore that strong class is **already impossible regardless of the still-unrun 1,000 within-group-order null tournament**.

The null tournament could still label the weak result as `LATIN-LIKE BUT NON-SPECIFIC` versus `NO PHILIP PLAINTEXT SIGNAL`, but it cannot change the practical answer to the decoding question: **no coherent medieval-Latin plaintext emerged**.

See `PLAN_E9.md` and `REPORT_E9.md` for the frozen design and reveal record.

## H4 research boundary after E9

H4 — music as an intermediate cipher — is not globally falsified. However:

1. the specific Philip duration signature is not specific after vowel conditioning;
2. the full Philip decoder does not yield readable held-out plaintext;
3. continuing to alter this decoder after seeing its output would be rescue tuning.

Another historical musical cipher may be studied only if selected by an independent historical/manuscript anchor or as part of a finite candidate family frozen before its Voynich scores are inspected.

## Research boundaries

- Do not retune E7 sequence rules or promote `max`.
- Do not reinterpret E8-A as positive because it has 5/5 stability; `p=.06294` failed the frozen gate.
- Do not rewrite E8-A2 after E9; vowel isolation remains the explanation of the E8 near-hit.
- Do not manually re-space, anagram, Caesar-shift, synonym-substitute, or cherry-pick E9 folios to manufacture readable Latin.
- Do not claim constructed E3–E6 alternatives establish real-world base rates.
- Preserve the distinction between mathematical non-uniqueness, historical theory-internal prediction, external historical cipher comparison, and exploratory plaintext probing.
- No current Issue #26 result identifies plaintext, melody, pitches, rhythm, or a decipherment.
