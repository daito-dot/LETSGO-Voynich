# Issue26E11D — monoalphabetic solver calibration and certification

Status: **FROZEN BEFORE E11D EXECUTABLE / CONTROL RESULTS**

E11C was classified `SOLVER INADEQUATE`; its Voynich outputs are non-authoritative and must not be used to tune a solver.

E11D contains **no Voynich plaintext scoring at all**. It develops and certifies a substitution solver using only known synthetic medieval-Latin monoalphabetic ciphers. Only a solver that passes untouched certification controls may later be frozen for a new Voynich test.

## Frozen language source

Use the same CREMMA commit/manuscripts and symmetric line-concatenated 24-letter normalization as E11C:

- `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`
- BIS-193, CLM13027, Mazarine915, UBL758
- lowercase ASCII
- `j→i`, `v→u`
- exact alphabet `abcdefghiklmnopqrstuwxyz` (24 letters)
- character 4-gram model, additive alpha=.1.

The first 140,000 retained top-23-letter plaintext events are used per synthetic control, approximately matching the E11C Voynich volume. A letter outside the selected top-23 plaintext letters breaks a run.

## Synthetic cipher dimensionality

- 23 ciphertext symbol labels, canonically `A..W` excluding I/O as needed only as opaque labels; actual labels have no linguistic meaning.
- plaintext set = 23 most frequent normalized Latin letters in the frozen corpus, ties lexicographic.
- one of the full 24 Latin letters is therefore absent from the true plaintext key.
- each synthetic control uses a deterministic hidden random bijection between the 23 plaintext letters and the 23 opaque cipher labels.

## Frequency-ranked initialization

Every candidate solver begins from a plaintext-frequency initialization, a standard property available for any monoalphabetic substitution:

1. rank ciphertext symbols by their occurrence counts descending, ties cipher-label order;
2. rank all 24 Latin letters by frozen CREMMA unigram frequency descending, ties lexicographic;
3. map the ranked 23 cipher symbols to the first 23 ranked Latin letters;
4. place the remaining Latin letter in the unused 24th key position.

This initialization uses no true key information.

For restart `r>0`, deterministically perturb the frequency key with exactly `2 + (r mod 5)` random pair swaps over all 24 key positions, using the candidate/restart/control seed namespace below.

## Candidate solver family

All candidates share:

- 8 restarts/control;
- 20,000 proposed pair swaps/restart;
- uniform pair proposal over all 24 positions;
- geometric temperature schedule ending at `.00005 bits/char`;
- exact character-4gram CE objective;
- after annealing, deterministic exhaustive steepest pair-swap descent over all 276 swaps until no improvement > `1e-12`;
- choose lowest final CE, tie lexicographic full key.

Only starting temperature differs:

- `FREQ-T005`: T0=.05
- `FREQ-T020`: T0=.20
- `FREQ-T080`: T0=.80
- `FREQ-T200`: T0=2.00

Candidate seed:

`Issue26E11D:DEV:{control}:{candidate}:{restart}`.

## Development controls and automatic selection

Create exactly 5 development ciphers with hidden-key seeds:

`Issue26E11D:DEVKEY:0` through `:4`.

Every candidate solves every development cipher.

For each candidate record per-control:

- recovered held-out/whole-control CE;
- true-key CE;
- exact key accuracy over 23 cipher symbols;
- occurrence-weighted key accuracy;
- CE excess over the true key.

Select one candidate automatically by this lexicographic criterion:

1. highest mean occurrence-weighted key accuracy;
2. highest worst-control occurrence-weighted accuracy;
3. lowest mean absolute CE excess;
4. candidate ID lexicographic.

The selected candidate is frozen before certification results are inspected.

## Untouched certification controls

Generate 5 new hidden ciphers using seeds:

`Issue26E11D:CERTKEY:0` through `:4`.

The selected solver alone is run on these certification controls, using restart seed:

`Issue26E11D:CERT:{control}:{selected_candidate}:{restart}`.

Certification passes only if all hold:

1. mean occurrence-weighted key accuracy >= `.98`;
2. worst-control occurrence-weighted key accuracy >= `.95`;
3. mean recovered CE exceeds mean true-key CE by <= `.05 bits/char`;
4. no individual control CE excess > `.10 bits/char`.

If certification fails, no subsequent Voynich substitution test is allowed with this solver family. A new solver family would require a new calibration plan.

## Information firewall

E11D code must not download, parse, import, score, or reference Voynich transcription content. The only Voynich-derived quantity permitted is the rounded scale target `140,000` events, used solely to match control length.

Candidate selection and certification therefore cannot be influenced by the non-authoritative E11C Voynich mappings or plaintext strings.

## Next-step authority

If certification passes, create a **new preregistered E11E plan** that freezes:

- the selected E11D candidate configuration exactly;
- the already-audited official STA family representation;
- the Voynich population/folds;
- the existing E11C decision gates or stricter gates.

Only E11E may apply the certified solver to Voynich. E11D itself makes no Voynich inference.
