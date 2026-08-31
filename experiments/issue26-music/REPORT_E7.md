# Issue #26E7 — prospective Guidonian dynamic prediction report

Status: **STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS**

## 1. Question

E7 was designed after recognizing an important limitation of the E3–E6 artificial-lattice controls.

Those controls establish mathematical non-uniqueness: other constructed six-state lattices can reproduce the static fit. They do **not** by themselves establish that Guidonian-like structure is common among real historical systems.

E7 therefore asks a different, stronger question without manufacturing another family of six-state competitors:

> After the E/E2 static Guidonian mapping is learned sequence-blind on training leaves, does the historical Guidonian theory correctly predict previously unused ordering properties of held-out Voynich tokens?

The answer under the preregistered primary test is **no**.

## 2. Historical prediction

The existing frozen Guidonian 20×6 matrix contains 42 allowed row/vox cells. Before looking at any E7 sequence score, these were frozen as the seven historical overlapping hexachords, each carrying:

`ut re mi fa sol la`

The seven row starts are:

`0, 3, 6, 7, 10, 13, 14`

and the seven pitch starts, in semitones relative to low Gamma/G, are:

`0, 5, 10, 12, 17, 22, 24`.

The voice offsets are:

`ut,re,mi,fa,sol,la = 0,2,4,5,7,9`.

This adds historical **ordering/pitch information** that E/E2 never used.

The mutation rule was frozen from medieval theory: a mutation changes solmization vox at the same sign/sound/pitch. The 13th-century TML text explicitly states that mutation occurs `sub eodem signo et in eodem sono`, requires at least two voces at the place, and excludes `b fa` / square-B `mi` because they are different signs and sounds.

Sources used before reveal:

- https://chmtl.indiana.edu/tml/13th/ARITRA_TEXT.html
- https://en.wikisource.org/wiki/A_Dictionary_of_Music_and_Musicians/Hexachord

The implementation therefore distinguishes B-flat/fa from B-natural/mi even where the existing 20-row static representation places them in the same row.

## 3. Prospective firewall

For every physical-leaf fold:

1. train the exact existing k=20 residual morphology representation on four-fifths of leaves;
2. fit all 720 state↔vox permutations and the 20 cluster↔row assignment on training occurrence counts only;
3. freeze the mapping;
4. then, and only then, inspect token order on held-out leaves.

Training uses no adjacency, line-transition, hexachord-run, mutation, or pitch-order statistic.

Only statically admitted Guidonian cells enter the dynamic test. Unparsed or statically disallowed tokens break a run; E7 never stitches across them or across line/paragraph boundaries.

The null preserves the exact fitted Guidonian cells and run lengths and destroys **only their within-run order** (5,000 deterministic shuffles).

Thus E7 does not ask whether some other six-state model can fit. It asks whether the already observed Guidonian static fit predicts new historical dynamics.

## 4. Replay firewall

All four historical architecture-level means replay exactly within 1e-12:

| transcription | parser | expected | replay |
|---|---|---:|---:|
| ZL | min | `0.8509664380470466` | `0.8509664380470466` |
| ZL | max | `0.8439032769036159` | `0.8439032769036159` |
| IT2a | min | `0.8512154779726009` | `0.8512154779726009` |
| IT2a | max | `0.8404723923113318` | `0.8404723923113318` |

So the negative dynamic result is not caused by changing the original E/E2 fitting implementation.

## 5. Primary ZL/min result

Sample size gates pass comfortably:

- admitted adjacent transitions: **13,261**
- inferred hexachord switches: **10,751**
- same-hexachord transitions: 2,510 (`18.93%`)

### D1 — overall dynamic compatibility

A transition counts as compatible if it remains in one hexachord or, when switching hexachords, at least one boundary-note pitch can serve as a legal shared-pitch mutation locus.

Observed:

**`0.5360078425`**

Order-destruction null:

- median: **`0.5360832516`**
- q95: `0.5406832064`
- observed − median: **`-0.0000754091`**
- p: **`0.5154969006`**
- positive fold effects: **2/5**

The original order is essentially exactly at the random-order median.

D1 gate: **FAIL**.

### D2 — mutation-specific legality

Among the 10,751 observed hexachord switches:

- legal at one of the two boundary pitches: 4,598
- observed legality: **`0.4276811459`** (`42.77%`)
- switches between hexachords with no shared pitch at all: **5,178**

Order-destruction null:

- median: **`0.4256448459`**
- q95: `0.4307245969`
- observed − median: **`+0.0020363001`** (~+0.20 percentage point)
- p: **`0.2531493701`**
- positive fold effects: **2/5**

So the small positive raw difference is ordinary under random ordering of the exact same fitted cells.

D2 gate: **FAIL**.

Frozen classification:

**`STATIC COMPATIBILITY DOES NOT PREDICT GUIDONIAN DYNAMICS`**

## 6. Max-parser sensitivity

The E6 `max` sensitivity had retained the most interesting static topology-class preference. E7 therefore provides an important prospective check on whether that residual static signal carries historical musical dynamics.

It does not.

### ZL/max

- transitions: 13,000
- switches: 10,496
- D1 observed `0.5203076923`
- D1 null median `0.5213076923`
- D1 p **`.6456708658`**
- D2 observed `0.4058689024`
- D2 null median `0.4082992291`
- D2 p **`.7736452709`**
- D1 positive folds 2/5; D2 positive folds 2/5

Both dynamic metrics are slightly **worse** than the shuffled-order median.

Thus the E6 residual `max` static preference does not forecast the unused Guidonian sequence constraint.

## 7. IT2a transcription robustness

IT2a is another transcription lineage of the same manuscript, not independent content. It is therefore only a transcription robustness sensitivity.

It reproduces the negative result.

### IT/min

- D1 observed `0.5219696970` vs null `0.5240214646`, p **`.7792441512`**
- D2 observed `0.4125223058` vs null `0.4139277047`, p **`.6816636673`**

### IT/max

- D1 observed `0.5182709158` vs null `0.5186603492`, p **`.5640871826`**
- D2 observed `0.4014998790` vs null `0.4058375536`, p **`.9268146371`**

No parser/transcription combination shows a prospective dynamic effect.

## 8. Interpretation

E7 is more informative for the historical music hypothesis than simply generating more artificial 20×6 alternatives.

The original static observation remains factual:

> under the adopted Zattera decomposition, Voynich contains a six-state factor whose sequence-blind morphology can be fitted unusually well to the Guidonian admissibility table under some weaker comparison families.

But when the fitted table is treated as the **actual musical system**, it should bring additional structure for free: seven overlapping hexachords, pitch identity, and same-pitch mutation constraints.

Those unused constraints do not predict held-out Voynich order.

In the primary ZL/min analysis, real order is indistinguishable from randomly permuting the same already-fitted Guidonian cells. Even mutation-specific legality is only +0.20 percentage point above its null median and is not significant (`p=.253`). Under `max`, the direction is negative.

Therefore the best current interpretation is:

> **the Voynich/Guidonian resemblance is static/formal rather than dynamically musical under this direct cell-sequence reading.**

This substantially weakens the hypothesis that the fitted six-state/20-locus structure represents literal Guidonian voces/pitches or a directly solmized musical sequence.

It does not prove that the manuscript cannot discuss music, use music as an analogy, or contain a more indirect musical cipher. Those are different hypotheses.

## 9. What this says about E3–E6

E7 also corrects a possible overreading of the artificial-null work.

E3–E6 validly show that the static fit is **mathematically non-unique** under increasingly matched constructed alternatives. They do not prove that such alternatives are common among real historical systems.

E7 avoids that population problem. It tests the Guidonian hypothesis against its own unused historical consequences. The negative result therefore does not depend on claiming that arbitrary six-state structures are common in the real world.

## 10. Current frontier

The direct literal-Guidonian sequence branch now has a strong negative prediction test.

Do not respond by searching additional mappings, changing the parser, relaxing mutation, or selecting a different sequence score on the same reveal. That would consume the falsification value of E7.

If music-related research continues, it should move to a genuinely different hypothesis class, e.g. music as metadata/instruction, a non-literal intermediate code, or externally motivated manuscript-local music anchors. The present static slot-lattice should not be promoted to literal pitches/voces without new independent evidence.

## 11. First-reveal provenance

- branch: `issue26-music-e7-guidonian-sequence`
- plan-first commit: `c7c28ac269cb2bba518fec119f8ea7ac4fcf14e0`
- first executable: `78432a63034b9eecd7ff9381d3424f9d3216e5f4`
- scientific head: `982af565464dc550c038ad137539d163b903ad7d`
- Actions run: `33372509796`
- job: `99426576294`
- artifact: `9750691619`
- artifact ZIP SHA-256: `c4335238efb457ce48f1c1b136392e4bee92f93021762b051bf0d4b5b6a46c5f`
- raw JSON SHA-256: `e126a49a1f539c134142d21b4c5565220a5982a6e7b301cb2c7e22474326e03d`
- plan SHA-256: `386ff02258f9de90f02bf56364bda594f5a692e11dd1cda3adebfe7b056977c8`
- executable SHA-256: `2af1d1bd6315f13f6f8653b1e291036eb8199c6bfc6fea5f95121cb34db37731`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`

No merge to `main` is authorized by this result.
