# Issue #75 Phase B — generic K/R/S occupancy-shape result

Date: 2026-09-01  
Status: **COMPLETE / FIRST-REVEAL AUTHORITY PERMANENTLY FROZEN**

## Primary result

Frozen classification:

`M2_GENERIC_KRS_SHAPE_DESCRIPTORS_INSUFFICIENT_STATEFUL_CONFIGURATION_RULE_REQUIRED`

Generic occupancy geometry — occupied-slot count `K`, contiguous occupied-run count `R`, occupied span `S`, plus slot main effects — is materially insufficient to reproduce the replicated Voynich R1 topology.

## Exact authority

- scientific head: `693f627910f5775406da410ec4d7157a161021e4`
- first-reveal run: `33504481315` — success
- artifact ID: `9799146088`
- artifact digest: `sha256:1a0ac70625f70ad87b591b3a4500073a3329a0ca1ef8e691ffb5c8e6c6890d43`
- complete population: `31/31`
- drops: `0`
- rerolls: `0`
- aggregate SHA-256: `f0c5e9e210f3cf9bd0fa9c9b818c0ee61649a906b051998346db1583c60fb566`
- Phase-B0 SHA-256: `9c180c7026e4f9464954dd029b71973cc1890f25223af6152959649dde57e834`
- frozen Phase-A positive-control aggregate SHA-256: `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`

## M2-KRS result

| metric | frozen value |
|---|---:|
| median T=min(R_ZL3b,R_IT2a) | `0.287338055` |
| median R ZL3b | `0.287338055` |
| median R IT2a | `0.295490425` |
| median residual energy E | `3.040259285` |
| median fold reliability W | `0.872586960` |
| median p_exist | `0.000999001` |
| median sign agreement ZL3b | `43.000/66` |
| median sign agreement IT2a | `42.000/66` |
| paired median gap vs frozen M+ center | `-0.677756021` |
| allowed loss q95 | `-0.009768313008182594` |
| no material loss | `false` |

The preregistered sufficiency rule was `gap_M2 >= -0.009768313008182594`. Observed `gap_M2=-0.6777560206049392` is far outside that tolerance.

## What changed from M1

Phase A M1 knew slot main effects and exact occupied-slot count `K`, yet had median topology correlation near `-0.17`. M2 additionally knows whether occupied positions form one or several runs and how wide their span is. That raises median topology correlation to about `0.29`, so coarse geometry contains real information, but most of the empirical-pattern topology remains unexplained.

The important distinction is therefore:

`slot prevalence` — insufficient

`+ occupied count K` — strong dependencies, wrong geometry

`+ coarse run/span geometry` — partial recovery only

`+ compact configuration/state rule` — now required frontier

`empirical complete-signature inventory` — sufficient positive control

## Non-memorization audit

M2 has zero explicit slot-pair interaction parameters and zero complete-signature-specific parameters. It conditions on generic `(K,R,S)` classes and uses slot main effects within class.

Target-blind B0 diagnostics:

- descriptor classes by fold: `[110, 112, 111, 111, 112]`
- training distinct complete signatures by fold: `[611, 601, 595, 602, 610]`
- generated distinct complete signatures across 31 reps: `1873..1946`

Thus M2 is materially coarser than empirical-signature resampling and is not a disguised replay of the empirical inventory.

## Sensitivity

The primary q95 tolerance remains authoritative. Non-promoting checks agree:

- q90 delta: `0.009053328589145426`; no-material-loss `false`
- q99 delta: `0.009905727081199411`; no-material-loss `false`

## Licensed next frontier

The preregistered rule licenses M3: a separately preregistered compact state/transition occupancy generator may now be tested. M3 must be interpretable as a generator and must not fit selected target edges or optimize the 66-edge target loss.

This license comes from the frozen Phase-B outcome only. The earlier failed Phase-C workflow attempts are not scientific evidence and must not be treated as an M3 result.

## Boundaries

This result concerns the 12-slot occupancy representation only. It does not identify slot meanings, literal token spellings, plaintext, cipher tables, natural-language word boundaries, historical Naibbe use, or decipherment.
