# Issue #26E8-A2 — vowel-fixed exhaustive Philip specificity control

Status: **VOWEL ISOLATION EXPLAINS E8A NEAR-HIT**

## 1. Why this follow-up was necessary

E8-A tested the historically attested 1436 Nicholas Philip four-duration alphabet partition:

- `aeiou`
- `bcdfg`
- `klmnp`
- `qrstz`

against 1,000 equal-capacity partitions of the same twenty letters. The frozen E8-A result was negative (`p=.06294`) but unusually stable: the historical target beat the null-fold median in all five held-out folds and selected exactly the same Voynich key in 5/5 folds.

That near-hit had an immediate non-musical explanation. Philip's first duration class is exactly the five Latin vowels `aeiou`, while ordinary random 5+5+5+5 partitions almost always destroy that natural linguistic class.

E8-A2 therefore conditioned on the obvious linguistic structure instead of increasing the number of generic random nulls.

The frozen question was:

> If `aeiou` is held intact for every comparator, is Philip's exact subdivision of the remaining fifteen consonants into `bcdfg | klmnp | qrstz` still unusually compatible with held-out Voynich four-state sequence geometry?

## 2. Exhaustive comparator universe

The vowel group was fixed to:

`aeiou`

The remaining consonants were:

`bcdfgklmnpqrstz`

Every unordered partition of those fifteen consonants into three groups of five was exhaustively enumerated.

Universe size:

`C(15,5) × C(10,5) / 3! = 126,126`

This universe includes the historical Philip partition exactly once. There are therefore 126,125 non-Philip comparators.

No random sampling is used in E8-A2.

Every candidate receives exactly the E8-A fitting freedom on each Voynich physical-leaf fold:

- candidate slots exactly 0, 6, 9;
- all `4! = 24` state→external-group bijections;
- selection using training leaves only;
- held-out score only after the key is frozen;
- distance `D = JSD(unigram) + JSD(ordered bigram)`;
- primary parser `min`, `max` sensitivity only.

Thus the only scientific difference between candidates is how the fifteen consonants are divided after the vowel class has already been conditioned on.

## 3. Replay firewall

The historical Philip target replayed E8-A exactly within `1e-12`.

Primary `min`:

- mean held-out D: `0.19129908493223063`
- target key in all 5 folds: slot0, permutation `[0,3,1,2]`
- fold distances:
  - `0.1671100600086904`
  - `0.18571262717003223`
  - `0.18769991148862755`
  - `0.20508107071913317`
  - `0.21089175527466975`

All replay assertions passed.

The `max` E8-A path also replayed exactly.

## 4. Primary result

Frozen classification:

**`VOWEL ISOLATION EXPLAINS E8A NEAR-HIT`**

Across the complete 126,126-member vowel-fixed universe:

- Philip target mean D: **`0.1912990849`**
- universe median D: `0.1921073411`
- q05: `0.1523131848`
- q01: `0.1323896655`
- minimum: `0.1071589913`
- strict Philip rank: **61,261 / 126,126**
- candidates tied with or better than Philip: **61,261**
- exact conditional percentile / p-value: **`0.4857127000`**
- per-fold median wins: **3/5**

Philip is therefore almost exactly in the middle of the complete comparator population once the vowel group is held fixed.

The five target fold distances versus the exhaustive per-fold medians are:

| fold | Philip D | vowel-fixed universe median | Philip better? |
|---:|---:|---:|:---:|
| 0 | `0.1671101` | `0.1697046` | yes |
| 1 | `0.1857126` | `0.1890785` | yes |
| 2 | `0.1876999` | `0.1865571` | no |
| 3 | `0.2050811` | `0.2053155` | yes |
| 4 | `0.2108918` | `0.2098795` | no |

The target key remains perfectly stable across folds, but that stability is not Philip-specific because the target's held-out distance is ordinary once the vowel class is conditioned on.

## 5. Better non-Philip partitions exist in abundance

The best vowel-fixed comparator is:

`aeiou | bfgkz | cdnst | lmpqr`

with mean held-out D:

**`0.1071589913`**

versus Philip:

`0.1912990849`.

Its selected Voynich key is also perfectly stable across all five folds: slot6, permutation `[0,2,3,1]`.

Several neighboring consonant subdivisions score around `0.1075–0.1077`, far better than the historical Philip subdivision.

This is useful diagnostically: the E8-A key stability was not a unique fingerprint of the 1436 cipher.

## 6. `max` sensitivity

The preregistered `max` sensitivity is even less favorable to Philip after vowel conditioning:

- target mean D: `0.2140154357`
- universe median: `0.2065111137`
- strict rank: `72,808 / 126,126`
- conditional p: **`0.5772640058`**
- fold median wins: **0/5**
- target key remains slot6 / `[0,3,2,1]` in 5/5 folds.

So neither parser supports Philip-specific consonant grouping.

## 7. Interpretation

### Observed fact

E8-A genuinely found a stable mapping between a natural four-state Voynich slot and the four-state sequence produced by applying Philip's historical duration grouping to medieval Latin.

### What E8-A2 identifies

That apparent specificity disappears almost completely when the obvious linguistic property is conditioned on:

> keeping `aeiou` together is sufficient to make Philip's remaining consonant subdivision ordinary.

The exact historical subdivision `bcdfg / klmnp / qrstz` has no detectable special relationship to Voynich under this test.

### Therefore

The E8-A near-hit is parsimoniously explained by **vowel isolation / broad Latin phonographic structure**, not by the Nicholas Philip musical cipher.

This is a stronger explanation than saying merely that E8-A missed `.05` by a small amount. E8-A2 shows why the near-hit occurred.

The specific Philip 1436 intermediate-cipher hypothesis should therefore be treated as **not supported**.

## 8. Consequence for the reserved five-pitch test

Do **not** run the planned five-pitch × four-duration E8-B as a rescue.

The pitch dimension was explicitly reserved behind a positive duration-group necessary-condition gate. That gate failed in E8-A, and E8-A2 shows that the most interesting part of the E8-A pattern is non-musically explained by vowel isolation.

Testing pitch now would consume a new degree of freedom after the historical signature that motivated the model has failed.

## 9. Broader H4 lesson

H4 — music as an intermediate cipher — is not globally falsified by one historical cipher.

But the research method must change before testing another historical musical cipher. Trying named ciphers one after another and stopping on whichever gives the best fit would itself create an uncontrolled model-selection problem.

Any continuation of H4 should first freeze a finite, historically justified candidate family and its multiplicity rule, or identify a manuscript-local anchor that selects a cipher before inspecting Voynich text statistics.

## 10. Engineering-failure chronology

The first E8-A2 Actions attempt (run `33376066892`, job `99437711627`, scientific head `3cc7309f43d909bbf20fd5050f33de225d6c28bc`) completed the exhaustive numerical calculation but failed while serializing the result because the standard JSON encoder rejected a NumPy boolean scalar.

No classification, rank, p-value, audit summary, or artifact was emitted by that run. It is therefore recorded as a **non-reveal engineering failure**.

A serialization-only wrapper was then added. It converts NumPy scalar objects to native Python scalar objects during `json.dump`; it does not alter the candidate universe, data, fitting, scoring, thresholds, or classification logic.

The first emitted reveal is the successful second run below.

## 11. First emitted reveal provenance

- branch: `issue26-music-e8-philip-cipher`
- E8-A2 plan-first commit: `a995ce13615cc5cfa73f24feb065012bac8c5cf0`
- E8-A2 scientific executable first commit: `2c08c0505ce849492f5adf582145ced6b71e24ea`
- non-reveal failed workflow head: `3cc7309f43d909bbf20fd5050f33de225d6c28bc`
- serialization-only wrapper commit: `7bcafd6a451cdc20d3797490766424f2b97e4f99`
- first emitted reveal head: `820c02ef402e384f044d772d2857b4748097a6b1`
- successful Actions run: `33376289470`
- job: `99438403840`
- artifact: `9752019365`
- artifact ZIP SHA-256: `ad8d487185a1797abcaa9ef67efa56168acdd8851cc1a9feb2f55d27c3bd280e`
- raw JSON SHA-256: `ca964035ae3a52a09f32fb32378bd616a3d8476106be8b7ee20e7d75bfb3413d`
- plan SHA-256: `5564023803c9f2bcd26c1af6ac31e7569f53ad0bf85ed44186e899213a879d88`
- scientific script SHA-256: `8c43b579b445d67af871f7595b9a5f6fff3c1d17e477298fc46ff137964d6d04`
- parent E8-A script SHA-256: `8de3919cedc2e84e58dad60c0db93fc25935b90d881658a871ab0be06d29cb85`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`

No merge to `main` is authorized by this result.
