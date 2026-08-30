# Phase 64B report — published Naibbe C1 fairness challenge

Status: **COMPLETE — C1-E0 PARTIAL; not structurally viable under the full frozen gate and not an A1-R1 rival.**

This report records the first successful Phase64B scientific reveal and its pre-result chronology. Exact numerical authority is `phase64b_science_results.json`.

## Scientific question

> Can an independently published, materially stronger meaningful-text + cipher mechanism rival the leading tested A1 mechanism on the already frozen held-out entry/locality scorecard and sealed H62-P1 recurrence geometry, without importing A1's previous-10 process or Voynich-specific boundary tuning?

Phase64B tests one bounded C-family candidate only. It is a fairness challenge, not a family-wide test of all meaningful/cipher mechanisms.

## Frozen C1-E0

External model:

- Greshko `naibbe-cipher`
- commit `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`
- `naibbe_v2.py` Git blob `b566ad82e4b6ff0782ecdddebf77718dac44f292`
- `references/naibbe_tables.csv` blob `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`
- `README.md` blob `486782221285186c0f78dd9474b676e067cd4bea`

Plaintext panel:

- exact equal-weight Phase62 CREMMA manuscripts: `BIS193`, `CLM13027`, `Mazarine915`, `UBL758`
- CREMMA commit `292525969ad98380b398e6606a9c2a36d51913ae`

Voynich authority:

- ZL3b Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`

Published Naibbe defaults were kept fixed: `RESPACING=17`, 78-card deck, published table weights, `SPACE_REMOVAL_RATE=0.03`, `UNAMBIGUOUS=True`, `MAX_BIGRAM_RETRIES=10000`. Five cipher realizations were run per manuscript using the frozen seeds. Five within-state codebook permutations were frozen as a control. No Naibbe parameter was selected from Voynich outcomes.

The exact scorecard remained the Phase62/63 held-out S1/S2/S3 plus H62-P1 profile comparison. Phase63A A1-R1 is the frozen leading comparator.

## Pre-result compatibility chronology

The original science head `c7e7732b3ab5f8d28864ef9fcd4c71d0f0d69255` was the first authorized execution attempt.

Actions run `33337753319`, job `99327642094` passed all exact source checks but stopped during plaintext preparation with:

`RuntimeError: Naibbe clean_line emitted unsupported normalized letters: ['ꝯ']`

The pinned external `clean_line()` uses Unicode `str.isalpha()`. Medieval alphabetic characters can therefore survive its published cleaning despite having no published Naibbe codebook cell.

Crucially, the failure occurred before candidate `output_metrics()` and before verdict-summary/artifact steps. No Phase64B S1/S2/S3, H62, mapping-control or classification value was revealed.

`PREFLIGHT_AMENDMENT_B3.md` therefore froze one generic interface rule before successful science:

- run the exact published `clean_line()` first;
- retain only the already frozen 23 effective Naibbe plaintext letters;
- drop other surviving Unicode alphabetic characters;
- do not transliterate or expand them;
- record retention diagnostics;
- change no cipher parameter, mapping, seed, metric, threshold or classification rule.

B4 toy preflight run `33337950314`, job `99328190295`, at head `c99b801684cf731e90ab39efab1f012a1db7bfc8` succeeded without checking out or reading ZL3b/CREMMA science. It verified the drop-only projection, preserved published W/J/K and æ/œ/þ normalization, and verified deterministic toy encryption.

## First successful reveal provenance

Frozen successful scientific head:

`1e80c41f0e502a7dacb593723dbf9d81f9f84add`

Actions:

- run `33338000172`
- job `99328325145`
- artifact `9739776686`
- artifact name `phase64b-first-reveal`
- artifact ZIP SHA-256 `f8534605b0c6b2396341d47d54b7d4280632ba14eb30ae7f34b8208921dab378`
- raw JSON SHA-256 `f88954c2efa2ec69e4bee0cd6fb1c70b49f08b1f44206c7f70bd540ad538d35d`

The artifact was hash-verified and its exact raw JSON bytes were committed as `phase64b_science_results.json` before interpretation documents were written.

## Primary published-output result

Frozen classification:

> **C1-E0 PARTIAL**

### Exposed S1/S2/S3

| metric | Voynich target mean | Naibbe mean | Naibbe / Voynich | frozen gate |
|---|---:|---:|---:|---|
| S1 paragraph-entry projection | 0.875994 | -0.082776 | **-0.0945×** | FAIL |
| S2 local-prev10 near-family excess | 0.043882 | -0.000835 | **-0.0190×** | FAIL |
| S3 aggregate line-position eta2 | 0.028274 | 0.017648 | **0.6242×** | PASS |

Joint relative exposed MSE: `0.8715183571712986`.

The core failure is not a small threshold miss. Published Naibbe produces essentially no positive Voynich-like paragraph-entry S1 or previous-10 S2 signal; both aggregate means have the opposite sign. It reproduces only the generic aggregate S3 regime, which earlier N0 work already showed is a weak Voynich-specific discriminator.

### H62-P1 recurrence geometry

| candidate | mean D_profile | median D_profile | mean |ΔC_short| |
|---|---:|---:|---:|
| N0 | 1.52982 | 1.47990 | 0.63750 |
| C0 | 1.85866 | 1.87201 | 1.30765 |
| **published Naibbe C1-E0** | **1.23763** | **1.25067** | **0.69290** |
| **A1-R1** | **0.76660** | **0.80945** | **0.11769** |

Against N0, Naibbe:

- has lower mean `D_profile`;
- wins `D_profile` in **4/5 folds**;
- has *worse* mean `|ΔC_short|`;
- wins `|ΔC_short|` in **0/5 folds**.

Against C0, Naibbe:

- has lower mean `D_profile` and lower mean `|ΔC_short|`;
- wins **5/5 folds on both diagnostics**.

Against A1-R1, Naibbe:

- does not beat mean or median `D_profile`;
- wins D in only **1/5 folds**;
- does not beat mean `|ΔC_short|`;
- wins C-short in **0/5 folds**.

Thus `H62_viable_vs_N0_C0 = false` and `A1_R1_rival = false` under the frozen rules.

The important asymmetric result is that a serious C mechanism substantially improves on C0 and even improves N0's overall H62 profile distance, but it fails specifically on the short-range concentration quantity that the sealed H62-P1 test was designed to expose.

## Fold-level primary result

| fold | S1 ratio | S2 ratio | S3 ratio | Naibbe D | Naibbe |ΔC_short| |
|---|---:|---:|---:|---:|---:|
| 0 | -0.0843 | -0.0198 | 0.6179 | 1.65265 | 0.82370 |
| 1 | -0.0223 | -0.0186 | 0.5346 | 1.25067 | 0.55033 |
| 2 | -0.5590 | -0.0172 | 0.9880 | 1.28004 | 0.55613 |
| 3 | -0.1740 | -0.0196 | 0.7761 | 1.22912 | 0.88054 |
| 4 | -0.0655 | -0.0203 | 0.4503 | 0.77567 | 0.65381 |

Fold4 is the only fold in which Naibbe beats A1-R1 on `D_profile` (`0.77567` vs `1.02343`), but A1 remains dramatically better there on `|ΔC_short|` (`0.02994` vs `0.65381`). This is retained rather than averaged away.

## Raw-token sensitivity

Removing the published respacing view does not rescue the mechanism.

Raw-token ratios:

- S1 `-0.08819×`
- S2 `-0.01401×`
- S3 `0.57128×`

H62 improves somewhat:

- mean `D_profile = 1.15199`
- median `D_profile = 1.14976`
- mean `|ΔC_short| = 0.62487`

The raw view satisfies the frozen H62 baseline-viability subcriterion, but still fails the exposed S1/S2 gate and does not rival A1-R1. Its overall frozen classification remains **PARTIAL**. Therefore published respacing is not the principal reason the primary C1 fails.

## Mapping-permutation control

The aggregate of five preregistered within-state glyph-assignment permutations is also **PARTIAL**:

- S1 `0.05901×`
- S2 `-0.00897×`
- S3 `0.59422×`
- mean `D_profile = 1.43381`
- mean `|ΔC_short| = 0.74867`
- exposed joint relative MSE `0.66842`

Individual controls:

| mapping | classification | S1 ratio | S2 ratio | S3 ratio | mean D | mean |ΔC_short| |
|---|---|---:|---:|---:|---:|---:|
| perm0 | PARTIAL | -0.0135 | 0.0068 | 0.6339 | 1.13319 | 0.42149 |
| perm1 | NOT COMPETITIVE | 0.0402 | -0.0367 | 0.5581 | 1.93036 | 1.36935 |
| perm2 | PARTIAL | 0.2103 | -0.0237 | 0.6453 | 1.40230 | 0.82198 |
| perm3 | PARTIAL | 0.0275 | -0.0201 | 0.5203 | 1.28607 | 0.72134 |
| perm4 | PARTIAL | 0.0305 | 0.0288 | 0.6136 | 1.18124 | 0.33460 |

The published assignment has better H62 D and C-short error than the permutation aggregate, but a *worse* exposed joint MSE. Consequently `published_assignment_gets_specific_credit = false`.

This prevents a post-hoc claim that the published Voynich-like glyph assignment itself is uniquely responsible for the partial structural proximity.

## B3 source-retention audit

The alphabet-domain projection is not numerically trivial and is therefore explicitly retained in the report.

For realization 0 (source retention is identical across realizations):

| manuscript | source units | published-clean chars | unsupported dropped | final chars | nonempty source / final lines |
|---|---:|---:|---:|---:|---:|
| BIS193 | 21,974 | 20,948 | 1,140 | 19,808 | 734 / 729 |
| CLM13027 | 18,064 | 17,944 | 885 | 17,059 | 457 / 457 |
| Mazarine915 | 13,609 | 12,470 | 791 | 11,679 | 484 / 482 |
| UBL758 | 3,709 | 3,710 | 62 | 3,648 | 100 / 100 |

Dropped source-native medieval Unicode types include forms such as `ꝑ`, `ꝓ`, `ꝙ`, `ꝯ`, `ꝰ`, `ꝵ`, `ħ`, `ẜ` and manuscript-specific superscript forms. They were dropped, not expanded into guessed readings.

This is a limitation of applying the exact published modern-Latin Naibbe alphabet to diplomatic medieval transcriptions. It does not authorize a later favorable expansion unless separately preregistered as a new model.

## What Phase64B changes

The result rejects two overly simple interpretations simultaneously:

1. **"C0 failed only because ciphering cannot create Voynich-like recurrence structure."** False as stated. Published Naibbe is materially better than C0 on H62 and beats C0 5/5 on both frozen recurrence diagnostics.
2. **"Any sufficiently elaborate meaningful-text cipher will naturally reproduce the A1 evidence."** Not supported by this strong example. Exact published no-reuse Naibbe still lacks the paragraph-entry specialization and previous-10 near-family excess and misses the sealed short-range concentration geometry.

Accepted current statement:

> **A1-R1 remains the leading tested structural mechanism. A materially stronger independently published meaningful-text cipher improves substantially over simple C0, but exact published Naibbe does not reproduce the Voynich paragraph-entry/local-recurrence signature and does not rival A1 on H62-P1.**

This strengthens A1 relative to the tested bounded C1. It does **not** establish that all C-family mechanisms fail, that Voynichese is meaningless, that A1 is the historical generator, or that the manuscript is deciphered.

## Next implication

Phase64B closes the immediate "give C a serious competitor" fairness gate for one independently published model. Repeating arbitrary cipher searches until one fits would create an open-ended model-selection problem.

The next research frontier should therefore be chosen by information gain rather than by repairing Naibbe or A1 after reveal. In particular:

- no post-result Naibbe locality/reuse rescue inside Phase64B;
- no A2 repair of Phase64A S3;
- preserve the unresolved C family globally;
- prioritize an independently grounded content-relation bridge if a defensible localized alignment can be constructed; otherwise freeze one explicit, historically motivated residual C hypothesis with a distinct prediction before testing it.

## Claim limit

Phase64B is a structural mechanism comparison. It supplies no plaintext, translation, historical identification or semantic absence result.
