# Phase 69A — long-range near-family persistence beyond A1 direct memory

Status: **FROZEN BEFORE H69-P1 REVEAL**

Date: 2026-08-31

## Why this is the next frontier

Phases 65–68 repeatedly failed to find a direct local content relation from pharmaceutical image morphology or attached `Lf` labels to the adjacent running text. Continuing to alter the same local content features would be low-value.

The strongest positive research line remains the A1-like formal generation layer: paragraph-entry specialization plus short-range non-identical edit-distance-1 family recurrence using a direct memory window of ten tokens. H62-P1 already showed that this mechanism predicts the previously sealed 1–40-token recurrence-distance profile unusually well.

Phase69 moves outward in scale rather than adding another local semantic crib.

## Primary question

> Does Voynichese contain **persistent long-range near-family recurrence on the same physical leaf**, at distances well beyond the frozen A1 direct 10-token memory, that the already-frozen A1-R1 mechanism systematically underpredicts?

If yes, A1 is missing a persistent leaf/topic/state channel. Such a channel could be semantic, cryptographic, recipe-level, scribal, or another formal mechanism; this test does not identify which.

If no, then a bounded local family mechanism plus indirect chaining can account for more long-range structure than its literal ten-token memory might suggest, weakening the argument that long-range recurrence alone demonstrates latent content.

This is a genuinely new prospective statistic. No >40-token physical-leaf H69 value has been inspected before this freeze.

## Frozen source and A1 implementation

Use the same exact ZL3b source and frozen Phase61/63 A1 parameterization:

- ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`;
- source commit for retrieval: `Aspect-Research/voynich-autoexploration@31819c914061cc6b63bbf4983e33d643ede52e46`;
- A1 implementation: `experiments/phase61/phase61c_joint_model.py`;
- five physical-leaf folds exactly as produced by that implementation;
- frozen per-fold A1 `(entry_strength, local_family_p)` from Phase61C/62;
- training-side vocabulary only for generation, as in A1-R1 / Phase63A robustness rather than full-manuscript output vocabulary.

No parameter is selected from Phase69 results.

## Physical-leaf sequence

For both Voynich target and generated A1 text:

1. retain paragraph tokenization/layout from the frozen parser;
2. group all tokens by physical leaf number;
3. within a leaf, concatenate tokens in manuscript paragraph order and line order;
4. paragraph/page boundaries do **not** reset the long-range sequence;
5. a physical leaf is eligible when its concatenated sequence contains at least 321 tokens, so all three frozen bins have possible observations.

Each outer fold pools all eligible held-out physical leaves in that fold.

If any of the five held-out folds has zero eligible leaves, Phase69A returns `NO VERDICT — INSUFFICIENT LONG-RANGE LEAF COVERAGE` and no scientific classification is made.

## Near-family relation

Use exactly the existing non-identical Levenshtein-distance-1 relation.

For each evaluated dataset separately, construct edit1 neighbors from the token types present in its eligible physical-leaf sequences, matching the H62-P1 metric convention.

Exact token equality is **not** a near-family hit.

## Frozen long-range bins

The three primary preceding-token distance bins are deliberately non-overlapping with H62-P1, which ended at distance 40:

- `L1 = 41–80`
- `L2 = 81–160`
- `L3 = 161–320`

For a token at position `i`, a bin is available only when all positions in that bin exist before `i`. A bin hit occurs if at least one token in that preceding distance interval is an edit1 neighbor of the current token.

## Within-leaf order null

For each target or generated dataset:

- hold each physical leaf's token multiset and length fixed;
- independently shuffle token order within each eligible leaf;
- use exactly **40** deterministic null shuffles;
- compute recurrence rate in each long-range bin for every shuffle;
- null baseline for each bin = median shuffled rate;
- signed excess = observed rate - null median.

This controls token inventory/frequency while asking about order-dependent long-range clustering.

## Primary scalar

For each fold define:

`E_long = excess_L1 + excess_L2 + excess_L3`.

Positive `E_long` means more long-range near-family recurrence than expected from the same leaf token multiset in random order.

Primary Voynich statistic:

`V = mean(E_long_Voynich_fold)` over the five frozen physical-leaf folds.

## Frozen A1 predictive distribution

For each of exactly **50** A1-R1 realization indices `r = 0..49`:

- generate held-out text independently in each of the five folds using frozen A1-R1 parameters and deterministic seeds;
- compute `E_long` with the identical eligible-leaf/bin/null procedure;
- aggregate `A_r = mean(E_long_A1_fold,r)` across the five folds.

This gives 50 frozen-mechanism predictive realizations of the manuscript-wide mean long-range excess.

## Primary one-sided model check

The predeclared failure direction is that real Voynich has **more** persistent long-range excess than A1:

`p_upper = (1 + count(A_r >= V)) / 51`.

Also report `delta = V - mean(A_r)`.

Classification:

- if `p_upper <= 0.05` and `delta > 0`: **A1 LONG-RANGE UNDERPREDICTION — PERSISTENT STATE REQUIRED**;
- otherwise: **NO DETECTED LONG-RANGE EXCESS BEYOND FROZEN A1**.

This is a model-adequacy statement, not evidence that A1 is the historical generator.

## Profile-shape diagnostic

For each fold and A1 realization, normalize the three signed excess values by their L1 absolute mass when nonzero, exactly as H62-P1 normalized its five-bin profile.

Report, descriptively:

- Voynich mean normalized `[L1,L2,L3]` profile;
- A1 mean profile;
- L1 profile distance between them.

This diagnostic is not a second significance gate and cannot rescue or overturn the primary scalar classification.

## Secondary exact-token sensitivity

Repeat the complete analysis using **exact token equality** rather than edit1 neighbors. This is predeclared secondary and cannot overturn the primary near-family result.

It asks whether any detected persistent state is specific to morphological families or also appears as literal token repetition.

## Interpretation limits

A primary A1 underprediction would show that the current bounded local-family model lacks a longer-lived same-leaf state. It would not distinguish:

- semantic/topic state;
- recipe/component state;
- cipher-key/state persistence;
- scribal/orthographic state;
- another nonsemantic generator.

A null does not prove semantic emptiness. It only says the already-frozen A1 mechanism is not measurably deficient in the preregistered >40-token recurrence-excess direction.

Do not alter bins, eligibility, null shuffles, A1 realization count, parameters, failure direction, or statistic after reveal.
