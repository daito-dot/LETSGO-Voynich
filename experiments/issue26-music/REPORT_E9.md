# Issue #26E9 — Nicholas Philip full-cipher plaintext probe

Status: **TARGET-ONLY EXPLORATORY REVEAL COMPLETE / STRONG LEAD GATE ALREADY IMPOSSIBLE**

Parent: Issue26E8 / draft PR #40.

## Question

After E8-A found a stable but non-significant four-duration near-hit and E8-A2 showed that the near-hit was explained by preserving the Latin vowel class, we nevertheless asked the practical exploratory question:

> If the historically attested 1436 Nicholas Philip 5-pitch × 4-duration cipher is applied as an actual decoder, does a held-out Voynich plaintext stream become recognizably medieval-Latin-like?

This was intentionally separated from E8's confirmatory interpretation. E9 cannot retroactively rescue E8-A/E8-A2.

## Frozen decoding rule

Historical Philip table in common low→high pitch coordinates:

- duration group 0: `a e i o u`
- duration group 1: `g f d c b`
- duration group 2: `k l m n p`
- duration group 3: `z t s r q`

The E8-A primary duration correspondence was frozen without refit:

- slot0 `EMPTY → group0 (aeiou)`
- slot0 `q → group3 (qrstz)`
- slot0 `s → group1 (bcdfg)`
- slot0 `d → group2 (klmnp)`

For pitch, the only natural five-state Zattera slots including EMPTY were searched:

- slot3: `EMPTY,t,k,p,f`
- slot5: `EMPTY,cth,ckh,cph,cfh`

Each fold trained only over 2 slots × 5! pitch bijections = 240 pitch keys using an external frozen medieval-Latin character 4-gram model. The selected key was then applied to held-out physical leaves.

No semantic/manual choice of key was allowed.

## First target-only reveal

GitHub Actions:

- branch: `issue26-music-e9-philip-decode-probe`
- plan-first commit: `1ecdaca55815b83e659777e109b0b154586950e3`
- first executable commit: `06c5308890ecea66a40af7cc4f06d5c17ba479e6`
- historical-alphabet correction was made before reveal; final executed head: `1ecd62d06b11dfd57d6ba14fedd86b02322d266e`
- run: `33378547467`
- job: `99445420999`
- artifact: `9752837236`
- raw JSON SHA-256: `c9c2ea9e412a5c3239d5f315d28844220495f547bc7c10df68d3c58173aefd1a`
- artifact ZIP SHA-256: `e1dcba4ca28d619b0da8adbfe844bed1eb8f3dec7385c5705e33fd89dd1e2903`

External Latin population used by the diagnostic:

- 30 files
- 7,698 retained runs
- 42,124 retained 20-letter-alphabet characters
- 4,650 supported-only normalized lexicon entries.

## Primary `min` result

Mean held-out 4-gram cross-entropy:

`4.1174818542 bits/char`

Selected pitch keys:

| fold | pitch slot | raw-state→rank permutation | train CE | held CE |
|---|---:|---|---:|---:|
| 0 | 5 | `[2,1,3,4,0]` | 4.09875 | 4.16360 |
| 1 | 5 | `[2,3,1,0,4]` | 4.11538 | 4.06854 |
| 2 | 5 | `[2,3,1,0,4]` | 4.08603 | 4.18073 |
| 3 | 5 | `[2,1,3,4,0]` | 4.08872 | 4.18052 |
| 4 | 5 | `[2,3,1,0,4]` | 4.13612 | 3.99402 |

The most recurrent exact pitch key is therefore only **3/5 folds**, below the preregistered >=4/5 strong-lead requirement.

Total held-out 4-gram-scored characters across the five disjoint folds: **8,701** in **2,783** retained decoded streams.

### Direct plaintext samples

Representative held-out streams printed before any semantic selection:

```text
f22r    iiiiismiemom
f77v    diismiisisim
f101r   iiiiisiidiii
f101v   iiiiiiidiiiis
f101v   misimrmismii
f33v    iiiiiimmmmii
f48v    isiiiiiiiiiiii
f83v    ssissiimeiii
f39v    diiisiimiiiim
f54r    miiieiimiiim
f84r    iiefmiisiiisi
f75v    sisiiiidimsmi
f75v    msmssiiimisi
f80r    diiesssmoisi
f46r    isisdioiisoi
f76r    dsrisiimddii
```

These are not visually or grammatically coherent Latin plaintext. They are dominated by repeated `i`, with secondary `s/m/d` under `min`.

In the first 100 reported held-out sample streams (20/fold), 709 printed characters contained approximately:

- `i`: 469
- `s`: 116
- `m`: 71
- `d`: 24
- `e`: 15
- `o`: 10
- all other letters together: 4.

This sample diagnostic is descriptive, not a separate test statistic, but it shows the practical failure mode clearly: the decoder collapses much of the manuscript into a very low-diversity `i/s/m` stream rather than exposing ordinary Latin-looking text.

## External lexicon inspection

Across held-out decoded streams, the longest exact substrings found in the frozen CREMMA supported-only lexicon were only **5 characters**.

Examples:

- `missi` (corpus frequency 1), appearing inside strings such as `missiiii`, `mississssi`, `missisiii`;
- `ssioi` (frequency 5);
- shorter 4-character hits such as `semi`, `meis`, `ssio`.

No >=6-character supported-only Latin lexicon hit appeared in the top exhaustive-by-length reports for any fold.

The local contexts do not form coherent multiword Latin. Isolated forms such as `missi`, `semi`, or `meis` therefore cannot be promoted as plaintext evidence; with thousands of decoded positions, short dictionary substrings are expected to occur by chance.

The most frequent decoded 4-grams reinforce the same point. For example in fold 0 under `min`:

- `iiii`: decoded 244, Latin corpus 6
- `iiis`: decoded 67, Latin 0
- `isii`: decoded 67, Latin 0
- `iisi`: decoded 65, Latin 0
- `siii`: decoded 59, Latin 0
- `iiim`: decoded 33, Latin 0
- `iimi`: decoded 31, Latin 0.

Thus the key selected to maximize Latin 4-gram likelihood still leaves many of the dominant held-out tetragrams absent from the external medieval-Latin corpus.

## `max` sensitivity

`max` lowers mean held-out CE to `3.6200604640 bits/char`, but does not produce readable plaintext and does not stabilize the pitch key:

- exact pitch-key recurrence: **3/5**;
- representative streams are even more strongly dominated by `i`, e.g. `iiiiiiiiiiii`, `isiiiiiiiiiiii`, `iiiiiiiiiiisi`;
- longest lexicon hits remain 5 characters.

As preregistered, `max` cannot rescue the primary path.

## Interpretation

The practical decoding experiment answers the user's exploratory question directly:

> Applying the historically attested Philip 5×4 cipher in the most favorable training-only way available under the existing slot grammar does **not** expose a coherent Latin plaintext in held-out Voynich text.

This is stronger than saying only that E8-A missed `p=.05`: the actual decoded output has the wrong qualitative form. The fitted decoder largely collapses into repeated letters, exact pitch keys are not stable enough across folds, and the few dictionary substrings are short and isolated.

### Strong-lead gate

`PLAN_E9.md` required the identical pitch key in >=4/5 folds for `PLAINTEXT-LIKE PHILIP LEAD`.

Observed primary recurrence is 3/5. Therefore **the strong positive E9 class is already impossible independent of the still-unrun 1,000 within-group-order null tournament**.

Running the 1,000 nulls could still distinguish `LATIN-LIKE BUT NON-SPECIFIC` from `NO PHILIP PLAINTEXT SIGNAL`, but it cannot recover the strong lead and is not required to answer whether readable meaning emerged. Given the direct output, that null tournament is lower information value than moving to a different independently motivated hypothesis.

## What this does and does not say

- It does **not** show that all historical musical ciphers are impossible.
- It does **not** erase the E8-A numerical near-hit.
- It does show that the specific Nicholas Philip full decoder, when applied without manual cherry-picking, does not yield recognizable medieval-Latin content.
- Do not manually re-space, anagram, Caesar-shift, substitute synonyms, cherry-pick folios, or tune individual letters on this reveal and present the result as E9.
- Any further music-cipher attempt needs a new independent historical/manuscript anchor rather than rescue tuning of this output.
