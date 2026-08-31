# Issue #26E10 — Sloane 351 plaintext probe report

Status: **FIRST REVEAL RECORDED**

Frozen classification: **`NO READABLE SLOANE PLAINTEXT`**

## Question

If a real fifteenth-century musical cipher structurally closer to a two-factor 5×5 code is applied to the adopted Voynich slot representation, does readable medieval-Latin plaintext emerge?

E10 tested the musical cipher in British Library Sloane MS 351, fol. 15, described by the British Library catalogue as fifteenth-century cipher rules and by Bernhard Bischoff as a note cipher using staff position plus note-form/stem families.

Secondary literature (Eric Sams, “Musical Cryptography”) describes the scheme as a late-fifteenth-century musical cipher using five pitches and altered note forms/stems for 24 letters plus `et`.

## Historical representation

The preregistered table preserved Bischoff's five musical note-form families:

- `a e i o u`
- `l m n r s`
- `b c d f g`
- `k p q t` in the four-position descending family
- `x y z et con`

Bischoff explicitly places `h` outside the note system as an oblique cross. For a deterministic computational 5×5 completion only, E10 assigned `h` to the one unused cell in the four-position family. This completion is **not** claimed to be historical.

## Preregistration provenance

- E10 branch base: Issue26E8 research state `343afac73da2e52b3a75f69e0a43257d54bdf952`
- plan-first commit: `fcb839634d352a34b953def7bc2b47c0995e2011`
- first executable commit: `8c08a99a563a9ffef021e1b09f1436abbaf584f5`
- executed scientific head: `39eebc9f3fc1085e506a0b55ed86e43c83dbc579`
- Actions run: `33380140973`
- job: `99450413972`
- artifact: `9753431124`
- raw JSON SHA-256: `66ad75b172230ed62900c9fe11225ef898ae8fc2af3e0ca37737df61090eaeb4`
- artifact ZIP SHA-256: `29d28bff083bcfbfc14a1ee42a67e9b134291873937601ebcedf99f8aa1de570`

The workflow verified that the plan commit predates the executable and verified the frozen ZL3b and CREMMA commits/blobs before execution.

## External Latin baseline

Five-fold CREMMA self-prediction with the frozen character 4-gram model:

- mean held-out cross-entropy: **`2.4515716158 bits/char`**
- fold values: `2.46248, 2.46827, 2.45917, 2.44398, 2.42395`

This gives a direct scale for what genuinely held-out medieval Latin looks like under the same language model.

## Track A — literal canonical application

Four deterministic conventions were tested without fitting a language key.

Primary `min` results:

| style slot | pitch slot | pitch order | CE bits/char | top-5 char fraction | distinct lexicon hits >=6 |
|---:|---:|---|---:|---:|---:|
| 3 | 5 | grammar | 5.05769 | .96514 | 0 |
| 3 | 5 | reversed | 4.86123 | .95946 | 0 |
| 5 | 3 | grammar | 4.73279 | .96514 | 0 |
| 5 | 3 | reversed | 4.99523 | .96396 | 0 |

Representative untouched outputs:

```text
aaaabbabeaia
aaabaaababaa
baaaallaalaa

uuuuggugouiu
uuuguuuguguu
guuuussuusuu

aaaaiiailaba
aaaiaaaiaiaa
iaaaaeeaaeaa
```

All four are far from the Latin self-baseline and collapse to a very small character set. No six-character-or-longer exact lexicon hit occurred.

Therefore the literal known code does not read the Voynich stream under the canonical slot orders.

## Track B — exhaustive training-only fitted application

The historical plaintext table was held fixed. For each physical-leaf fold E10 exhaustively evaluated:

- both assignments of slot3/slot5 to style vs pitch;
- all 120 style-state permutations;
- all 120 pitch-state permutations.

Total: **28,800 keys per fold**.

Selection used only four-fifths of Voynich leaves; the fifth was decoded untouched.

### Numerical result

Primary `min`:

- pooled held-out CE: **`4.2224109527 bits/char`**
- mean fold CE: `4.2226003324`
- exact full-key recurrence: **4/5 folds**
- pooled decoded characters: **51,408**
- streams: **7,321**
- top five output characters: **94.6915%** of all output
- distinct exact CREMMA lexicon hits length >=6: **0**

Held-out fold CEs:

- fold0 `4.2039524860`
- fold1 `4.2245843141`
- fold2 `4.2204409090`
- fold3 `4.2074400687`
- fold4 `4.2565838840`

Four folds select exactly:

- style slot = `3`
- style permutation = `[4,0,1,3,2]`
- pitch slot = `5`
- pitch permutation = `[4,1,3,2,0]`

Fold2 differs only in the pitch permutation: `[4,3,2,1,0]`.

Representative untouched held-out output:

```text
conconconcon
conconconsconconscon
uyconconconconcon
conconconcon
conconconucon
conconconconet
conconuconconu
uconconconuconcon
conssconetycon
uconconconcon
```

The longest reported exact Latin-lexicon hits are only four characters (`usus`, `uetu`, etc.). No >=6 hit exists.

Frequent tetragrams are dominated by artifacts of repeated `con`:

- `conc` 4867 occurrences (Latin comparator count 5)
- `onco` 4867 (Latin 0)
- `ncon` 4867 (Latin 1)
- `scon` 2346 (Latin 1)
- `cons` 2331 (Latin 8)

## Why the 4/5 recurrent fitted key is not plaintext evidence

The recurrence is a real numerical observation and should not be discarded. But its mechanism is visible from the frozen key.

The recurrent mapping sends:

- slot3 `EMPTY` to historical style family S4 = `x/y/z/et/con`;
- slot5 `EMPTY` to pitch p4;
- S4 × p4 is the historical abbreviation cell `con`.

The adopted slot grammar makes EMPTY states extremely common, so the optimizer gains language-model probability by mapping a dominant raw cell to the multi-character Latin abbreviation `con`. The resulting held-out text then repeats `con` rather than producing ordinary Latin syntax or lexical diversity.

This is consistent with all three observed diagnostics:

1. key recurrence is high (4/5);
2. cross-entropy remains **1.77 bits/char worse** than the Latin self-baseline (`4.2224` vs `2.4516`);
3. output collapses to a few characters/abbreviation fragments (top five characters `94.69%`) with zero >=6 lexicon hits.

So the stable fitted key is best interpreted as a **stable frequency-collapse / abbreviation-exploitation optimum**, not a stable decryption key.

This explanation is post-reveal and descriptive; it does not alter the preregistered classification.

## Max sensitivity

For the tested slot3/slot5 factors, `max` reproduces the same E10 numerical results and decoded outputs as `min` in this experiment. It therefore does not rescue the result.

## Frozen classification

Neither preregistered lead gate passes.

- Track A is nowhere near the Latin self-baseline and has no >=6 lexical hits.
- Track B does meet the key-recurrence gate, but fails the Latin-distance, lexical, and non-collapse gates decisively.

**`NO READABLE SLOANE PLAINTEXT`**

## Interpretation

E10 does not show that music ciphers in general are impossible. It answers the practical exploratory question more narrowly:

> A documented fifteenth-century musical cipher with an approximately 5×5 pitch × note-form construction does not produce readable medieval Latin when applied either literally or after exhaustive training-only alignment to the two natural five-state Zattera factors.

Together with E9, this weakens the idea that the Voynich slot structure can be turned into plaintext simply by borrowing a known near-period music cipher.

The most informative residual observation is not plaintext but representation behavior: multiple historical cipher probes can align stably with highly imbalanced Voynich slot states by assigning dominant empty-state cells to high-frequency Latin classes or abbreviations. Future cipher probes should explicitly control this frequency-collapse mechanism rather than interpreting key stability alone as support.

## Historical/source boundary

British Library catalogue: Sloane MS 351, f.15b, “Ciphers: Rules for a cipher: 15th cent.”

Bischoff's catalogue supplies the detailed note-family assignments used in this test. Eric Sams independently describes the five-pitch / altered-note-form construction and its 24 letters plus `et`.

Sloane 351 is later than the usual Voynich dating window. E10 therefore remains a structural/decoding comparison, not evidence that this specific cipher was available to the Voynich author.

## Merge policy

This is a negative exploratory research branch. Keep it separate from `main` unless the user explicitly authorizes integration of the research record.
