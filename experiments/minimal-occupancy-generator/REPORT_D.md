# Issue #75 Phase D — nested distance-banded nonlocal occupancy grammar result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Primary result

Frozen classification:

`M4_KRS_CHAIN_DISTANCE_NONLOCAL_GRAMMAR_INSUFFICIENT_LATENT_CONFIGURATION_RULE_REQUIRED`

The preregistered `M4-KRS-CHAIN-DISTANCE` model retains all of the successful Phase-C local grammar and adds eight generic nonadjacent separation-distance interactions. It improves the complete-66 R1 topology modestly, but remains far outside the frozen empirical-signature equivalence region.

Therefore a rule of the form

`K/R/S geometry + local position-specific transitions + generic distance-dependent nonlocal coupling`

is not sufficient to reproduce the replicated Voynich occupancy topology.

## Exact authority

- first-reveal run: `33511592593` — success
- scientific head: `26e885e45783664857764bfcc8a079c16afd904f`
- complete population: `31/31`
- drops: `0`
- rerolls: `0`
- final artifact ID: `9801993243`
- artifact digest: `sha256:906676c1e4d7c44b2d4255e0b8cf53acafd6f8692e7258babc08d09e0ce1c58b`
- aggregate SHA-256: `c15ffb92030220596cacef9db9cb3bdb26c92607f675c24ff0fa607e16764489`
- Phase-D0 authority SHA-256: `5c31aaa5fdb959873d89d7762dfd78db42c1a773a091b71a9f0731e90fa269cb`
- permanent post-reveal authority commit: `b9b7dea91e914c89e3f35647f87b29a0391127cc`

Repository authority:

`experiments/minimal-occupancy-generator/stage-d-first-reveal/`

The permanent freeze is transport-only: it copies and verifies the exact successful first-reveal artifact and does not recompute target scores.

## Model tested

`M4-KRS-CHAIN-DISTANCE` conditions on the exact training-only empirical distribution of:

- `K`: occupied-slot count;
- `R`: occupied-run count;
- `S`: first-to-last occupied span.

Within each `(K,R,S)` class it retains Phase C's local maximum-entropy terms and adds generic nonadjacent separation terms:

- 11 free unary slot terms;
- 10 free position-specific adjacent interaction terms;
- 8 free generic nonadjacent distance terms for separations `3..10`;
- total `29` free continuous parameters per cross-fit training split;
- named nonadjacent slot-pair parameters: `0`;
- empirical complete-signature-specific parameters: `0`;
- latent-state parameters: `0`.

The exact complete-state within-`(K,R,S)` rank audit is:

`11 -> 21 -> 29`.

The additional apparent distance directions are non-identifiable because of exact descriptor identities; in particular `C_11` is fixed by span.

## Target-blind D0 and pretarget validation

Valid D0:

- run `33510693677` — success
- 31 frozen target-blind corpora
- authority SHA-256 `5c31aaa5fdb959873d89d7762dfd78db42c1a773a091b71a9f0731e90fa269cb`
- maximum training-moment fit error `8.900935544176036e-13`, below the frozen `1e-10` tolerance
- generated distinct-signature range `1172..1236`
- all target-access flags false

Pretarget validation:

- run `33511195719` — success
- exact D0 replay passed for reps `0` and `30`
- rep-0 candidate-owned `1000` reference + `1000` test null smoke completed with target loader hard-blocked
- candidate-smoke E `3.0662698685620127`
- candidate-smoke W `0.9496019313081269`
- candidate-smoke `p_exist=0.000999000999000999`
- no Phase-D target result existed when `PRETARGET_EXECUTION_FREEZE_D.md` was committed

Two earlier Phase-D workflow attempts, runs `33510176784` and `33510519140`, stopped at pre-generation chronology/plan gates and are non-authoritative. Neither produced a Phase-D target result.

## Frozen result

| metric | median |
|---|---:|
| `T=min(R_ZL3b,R_IT2a)` | `0.6225259878` |
| R ZL3b | `0.6284498369` |
| R IT2a | `0.6225259878` |
| sign agreement ZL3b | `51/66` |
| sign agreement IT2a | `50/66` |
| residual energy E | `3.0748615728` |
| physical-fold reliability W | `0.9514708583` |
| p_exist | `0.0009990010` |

Across the 31 frozen realizations:

- T range: `0.5707678455 .. 0.6514936319`
- R ZL3b range: `0.5714825714 .. 0.6576091397`
- R IT2a range: `0.5707678455 .. 0.6514936319`
- W range: `0.9402517161 .. 0.9718360090`
- ZL3b sign agreement range: `50..53 / 66`
- IT2a sign agreement range: `49..52 / 66`

The model creates a strong and highly reliable residual network. Its failure is again topological: it does not create the correct complete dependency geometry closely enough.

## Primary sufficiency decision

Frozen Phase-A empirical complete-signature controls remain the ceiling:

- M+ A median T `0.9643123239`
- M+ B median T `0.9655940680`
- q95 self-difference tolerance `0.009768313008182594`

Phase-D paired median gap from the frozen M+ center:

`gap_M4 = -0.3391848198669607`

Sufficiency required:

`gap_M4 >= -0.009768313008182594`

Observed M4 is therefore far outside the equivalence region. The q90 and q99 non-promoting sensitivity checks also remain false.

## What M4 adds over M3

Paired across the same 31 replication indices:

`median(T_M4 - T_M3) = +0.021217706030355665`.

This means generic nonlocal separation effects are not irrelevant. They recover a small additional portion of the replicated topology.

But the gain is minor relative to the unresolved gap:

| model | information supplied | median T |
|---|---|---:|
| M0 | slot marginals | `-0.110` |
| M1 | marginals + K | `-0.167` |
| M2 | exact K/R/S geometry | `0.287` |
| M3 | K/R/S + position-specific nearest-neighbor transitions | `0.593` |
| M4 | M3 + generic nonadjacent separation coupling | `0.623` |
| M+ | empirical complete occupancy signatures | `~0.965` |

The important negative result is therefore not “long-range relations do not matter.” It is narrower and stronger:

> **Long-range dependence cannot be reduced to a generic function of slot separation.**

Two slot pairs at the same distance are not interchangeable enough for that representation to recover the complete R1 geometry.

## Mechanistic interpretation

The progressively surviving construction picture is now:

`slot prevalence`

`+ token size / coarse K/R/S geometry`

`+ local position-specific transitions`

`+ weak generic distance effects`

`+ configuration-specific hidden structure  <-- still required`

`= empirical occupancy-pattern topology`

A parsimonious explanation now worth testing is a **small number of latent token-construction modes**. Under such a model, distant slots need not directly interact pair-by-pair. Instead, a hidden mode can change several slot preferences at once, and mixing those modes can induce the observed nonlocal dependency pattern.

This is materially different from adding selected distant edges after seeing the target graph.

## Licensed next frontier

Phase D licenses only a separately preregistered latent-state/configuration test.

The next model must:

- be selected without inspecting Phase-D target-edge residuals;
- not add target-selected distant slot pairs;
- not fit the held-out ZL3b or IT2a R1 graph;
- retain the frozen parser, physical folds, candidate-owned null, 66-edge evaluation, and Phase-A M+ sufficiency rule;
- use a compact latent architecture whose complexity is fixed or selected from training occupancy information only;
- freeze a complete target-blind generated population before first target access.

An unrestricted 66-edge pairwise model is not licensed as the next step because it would answer a weaker memorization question rather than the minimal-generator question.

## Boundaries

Phase D does not establish:

- meanings for slots;
- literal token spelling rules;
- plaintext letters or language;
- a cipher table;
- semantic absence;
- natural-language word boundaries;
- historical Naibbe use;
- decipherment.

It establishes that, within the replicated 12-slot occupancy representation, the missing construction information is more configuration-specific than coarse geometry, first-order local transitions, or generic separation-dependent coupling can express.