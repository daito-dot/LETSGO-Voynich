# Issue #26 direct-music research status

Updated after Issue26E10 first reveal.

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
| E9 | If the 1436 Nicholas Philip 5×4 system is nevertheless used as an actual decoder, does held-out Voynich become readable medieval Latin? | **NO PLAINTEXT LEAD** | Training-only pitch fitting gives only 3/5 exact-key recurrence; output collapses to repeated `i/s/m`, with no coherent long Latin material. Separate draft PR #41. |
| E10 | If the fifteenth-century Sloane 351 note cipher is applied literally or after exhaustive training-only 5×5 alignment, does readable Latin emerge? | **NO READABLE SLOANE PLAINTEXT** | Literal CE 4.73–5.06 vs Latin self-baseline 2.45; fitted 28,800-key search gives 4/5 recurrent key but held-out CE 4.222, top-5 chars 94.69%, zero >=6 lexicon hits; output collapses to repeated `con`. |

## Current interpretation

Issue #26 does **not** support visible Voynich running text as a literal Guidonian musical sequence. E7 is the cleanest falsification of that direct reading because the static mapping failed to predict historical musical dynamics that were not used to fit it.

The robust positive object from E/E2 remains narrower:

> Under the adopted Zattera slot decomposition, Voynich contains a six-state morphological/dependency factor, and a Guidonian 20×6 table can fit that static factor well under some comparison families.

But E3–E6 establish mathematical flexibility/non-uniqueness, and E7 shows that interpreting the static fit as actual Guidonian pitches/voces does not predict held-out order.

E8–E10 moved to a different question: historically attested music-as-cipher systems. The results do not show that all possible musical ciphers are impossible; they do show that two concrete near-period schemes do not turn the adopted Voynich slot representation into readable medieval Latin.

## E8-A / E8-A2 — Nicholas Philip 1436

The tested historical duration groups are:

- `aeiou`
- `bcdfg`
- `klmnp`
- `qrstz`

E8-A compared the historical four-way partition against 1,000 deterministic alternative equal-capacity partitions under identical training-only Voynich slot/key freedom.

Primary `min`:

- Philip mean held-out JSD distance: `0.1912990849`;
- null median: `0.2856364100`;
- lower-tail p: **`.0629370629`**;
- target beats null-fold median: **5/5**;
- exact target key recurrence: **5/5**;
- recurrent key: slot0, permutation `[0,3,1,2]`.

The stable near-hit failed the preregistered significance gate.

E8-A2 then fixed `aeiou` in every comparator and exhaustively enumerated all **126,126** unordered partitions of the remaining 15 consonants into 5+5+5.

- Philip D: `0.1912990849`
- universe median: `0.1921073411`
- rank: **61,261 / 126,126**
- conditional p: **`.4857127000`**
- fold median wins: **3/5**

Frozen interpretation:

**`VOWEL ISOLATION EXPLAINS E8A NEAR-HIT`**.

The specific Philip consonant grouping is ordinary once the vowel class is preserved.

## E9 — practical Philip decode probe

At the user's request, the negative E8 inference was kept intact while a separate exploratory question was asked: what if the known 1436 mechanism is simply used as a decoder anyway?

The E8-A 4-state duration key was fixed. Only the two natural five-state Voynich pitch slots and their 120 permutations were fit on training leaves.

Primary `min`:

- mean held-out CE `4.1174818542 bits/char`;
- exact pitch-key recurrence `3/5`;
- representative output: `iiiiismiemom`, `diismiisisim`, `iiiiisiidiii`;
- longest reported exact supported-Latin lexicon matches only 5 characters and occur in incoherent contexts.

This is a practical negative decode result, not a new confirmatory test of E8.

## E10 — Sloane 351 practical decode probe

British Library Sloane MS 351 contains fifteenth-century cipher rules. Bischoff describes a musical cipher using five staff positions and several note-form/stem families for 24 note-system symbols, with `h` outside the system. E10 preregistered a transparent 25-cell computational completion solely to map the code onto the two natural five-state Zattera factors.

### Literal Track A

Four deterministic, unfitted axis/order conventions produce:

- CE range `4.73279–5.05769 bits/char`;
- Latin self-baseline `2.45157 bits/char`;
- top-five-character fractions about `95.9–96.5%`;
- zero distinct exact lexicon hits length >=6.

Representative output is of the form `aaaabbabeaia`, `uuuuggugouiu`, `aaaaiiailaba`.

### Fitted Track B

Every fold exhaustively searches exactly `2 × 120 × 120 = 28,800` axis/permutation keys on training leaves only.

Primary `min`:

- pooled held-out CE `4.2224109527`;
- exact full-key recurrence **4/5**;
- 51,408 decoded held-out characters across 7,321 streams;
- top five output characters **94.6915%**;
- distinct exact lexicon hits length >=6: **0**.

Representative output:

`conconconcon`, `uyconconconconcon`, `conconconconet`, `conssconetycon`.

The recurrent key maps the dominant EMPTY×EMPTY raw cell to Sloane's `con` abbreviation cell. Therefore key stability is best read as a stable **frequency-collapse / abbreviation-exploitation** optimum, not as readable plaintext. This mechanism-level interpretation is post-reveal; the frozen classification remains simply:

**`NO READABLE SLOANE PLAINTEXT`**.

## What E8–E10 add methodologically

A useful distinction is now explicit:

1. **hypothesis support:** does a historical system have an externally fixed signature that is unusually compatible with Voynich under fair controls?;
2. **practical decode probe:** even if confirmatory support is weak, does applying the established historical method actually expose coherent held-out text?;
3. **optimizer pathology:** does a stable fitted key merely map dominant Voynich states onto high-frequency language classes/abbreviations?

E9 and E10 show why (2) is worth checking but cannot substitute for (1), and why key stability alone is unsafe without (3).

## H4 research boundary after E10

H4 — music as an intermediate cipher — is not globally falsified. But sequentially trying arbitrary historical ciphers until something looks readable remains uncontrolled model selection.

E9/E10 are retained as explicitly exploratory practical-decoding probes. They must not be promoted into confirmatory evidence merely because a key or slot mapping appears stable.

Before another historical cipher is used for **hypothesis support**, one of the following must hold:

1. a finite historically justified candidate family is frozen before seeing new Voynich scores, with multiplicity charged across the family; or
2. an independent manuscript-local visual/textual anchor selects a specific cipher family before text statistics are inspected.

A further practical decode probe may still be informative as exploration, but its result must remain labeled exploratory and should include explicit controls for frequency collapse.

## Research boundaries

- Do not retune E7 sequence rules or promote `max`.
- Do not reinterpret E8-A as positive because it has 5/5 stability; `p=.06294` failed the frozen gate.
- Do not use E9 or E10 to retroactively rescue E8.
- Do not interpret E10's 4/5 key recurrence as plaintext evidence; the held-out output is non-language-like and collapse-dominated.
- Do not claim constructed E3–E6 alternatives establish real-world base rates.
- Preserve the distinction between mathematical non-uniqueness, theory-internal prediction, historical cipher comparison, and exploratory decoding.
- No current Issue #26 result identifies plaintext, melody, pitches, rhythm, or a decipherment.
