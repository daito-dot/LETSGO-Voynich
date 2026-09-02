# Issue #75 Phase C — nearest-neighbor state/transition occupancy generator result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Primary result

Frozen classification:

`M3_KRS_NEAREST_NEIGHBOR_TRANSITION_GRAMMAR_INSUFFICIENT_NONLOCAL_OR_LATENT_RULE_REQUIRED`

The preregistered `M3-KRS-CHAIN` model substantially improves on coarse occupancy geometry, but remains far from the empirical-pattern positive-control ceiling. A rule using only unary slot tendencies and nearest-neighbor occupied-pair transitions, even after preserving the exact training-only `(K,R,S)` descriptor distribution, is not sufficient to reproduce the replicated Voynich R1 topology.

## Exact authority

- first-reveal run: `33508975967` — success
- scientific head: `8d02507355f428ffc80d590bbcfe256ce9fd0d95`
- complete population: `31/31`
- drops: `0`
- rerolls: `0`
- final artifact ID: `9800955706`
- artifact digest: `sha256:1a860009ab8a2ddfa8731d167137f59073365633be54b7f9185c333939b13ac5`
- aggregate SHA-256: `34affe98b68a1e410ea3d4384a917450c2b58e7a8e02a30da8befa660712421a`
- Phase-C0 authority SHA-256: `1ff4469f57a84093b8c5d6463bb276a8de6fc108eed666bf63c9c7dacbf622a6`
- permanent post-reveal authority commit: `9664e7cd1cf1eec8c2dacf37ceeb9c15c31a1f2a`

Repository authority:

`experiments/minimal-occupancy-generator/stage-c-first-reveal/`

## Model tested

`M3-KRS-CHAIN` preserves the exact training-only distribution of:

- `K`: number of occupied slots;
- `R`: number of contiguous occupied runs;
- `S`: span from first to last occupied slot.

Within each `(K,R,S)` class it uses a maximum-entropy occupancy generator with:

- 11 free unary slot terms;
- 10 free nearest-neighbor pair terms;
- 21 continuous parameters per cross-fit training split;
- explicit nonadjacent pair terms: `0`;
- empirical complete-signature-specific parameters: `0`.

The architecture and decision rule were fixed before first target access. The recovered chronology also establishes that no earlier Phase-C target score existed.

## Frozen result

| metric | median |
|---|---:|
| `T=min(R_ZL3b,R_IT2a)` | `0.5934673293` |
| R ZL3b | `0.5934673293` |
| R IT2a | `0.6194154849` |
| sign agreement ZL3b | `51/66` |
| sign agreement IT2a | `52/66` |
| residual energy E | `3.1450497603` |
| physical-fold reliability W | `0.9441114543` |
| p_exist | `0.0009990010` |

Across the 31 frozen realizations:

- T range: `0.5647499059 .. 0.6346185797`
- R IT2a range: `0.5912851481 .. 0.6607230253`
- W range: `0.9340585104 .. 0.9677853827`

Thus M3 consistently creates a strong, reliable residual topology. The problem is not failure to create structure. The remaining problem is **which dependencies are present**.

## Primary sufficiency decision

Frozen Phase-A empirical-signature positive controls:

- M+ A median T: `0.9643123239`
- M+ B median T: `0.9655940680`
- q95 self-difference tolerance: `0.0097683130`

M3 paired median gap from the frozen M+ center:

`gap_M3 = -0.37325753997796984`

Sufficiency required:

`gap_M3 >= -0.009768313008182594`

Observed M3 is therefore nowhere near the equivalence region.

The same conclusion holds under the non-promoting q90 and q99 tolerance checks.

## What M3 adds over M2

The hierarchy now shows a useful progression:

| model | information supplied | median T |
|---|---|---:|
| M0 | slot marginals | `-0.110` |
| M1 | marginals + K | `-0.167` |
| M2 | marginals + exact K/R/S geometry | `0.287` |
| M3 | exact K/R/S + unary + nearest-neighbor transition terms | `0.593` |
| M+ | empirical complete occupancy signatures | `~0.965` |

M3 roughly doubles the positive topology recovery achieved by M2. Nearest-neighbor organization is therefore not irrelevant; it carries a large amount of the required structure.

But it does not close the gap.

This sharply localizes the missing information:

> Voynich token occupancy is not adequately described as a first-order chain over the 12 structural positions, even when token size, run count and span are already controlled.

## Mechanistic interpretation

The current evidence supports a layered construction law:

`slot prevalence`

`+ token size / coarse geometry (K,R,S)`

`+ local nearest-neighbor transition preferences`

`+ additional nonlocal or latent configuration structure  <-- still required`

`= empirical occupancy-pattern inventory`

Two broad mechanisms remain scientifically live:

1. **nonlocal structural coupling** — occupancy at one position directly constrains positions more than one slot away; or
2. **latent construction states/classes** — tokens are generated under different hidden templates or modes, and mixing those modes produces long-range residual dependencies without requiring every distant pair to interact directly.

Phase C does not distinguish these two explanations.

## Relationship to earlier results

Issue #72 showed that exact plaintext local order and final corpus placement are not detected necessities for R1, while upstream state-dependent emission assignment matters strongly.

Issue #75 now shows, generatively:

- slot prevalence is insufficient;
- occupied-slot count is insufficient;
- coarse token geometry is insufficient;
- first-order nearest-neighbor transitions are still insufficient;
- the empirical occupancy-pattern inventory remains sufficient.

The causal target is therefore increasingly specific: **a compact rule for selecting complete within-token occupancy configurations**.

## Licensed next frontier

A new prospective phase is licensed to distinguish a minimal nonlocal extension from a latent-state explanation. It must be separately preregistered after this result and must not select distant interactions by inspecting the 66 target edges.

The old premature Phase-D workflow commits are non-authoritative and are not promoted by this result.

## Boundaries

Phase C does not establish:

- meanings for slots;
- literal Voynich token spelling rules;
- plaintext letters or language;
- a cipher table;
- semantic absence;
- natural-language word boundaries;
- historical Naibbe use;
- decipherment.

It establishes only that the replicated 12-slot R1 topology requires configuration structure beyond coarse geometry and nearest-neighbor occupancy transitions.
