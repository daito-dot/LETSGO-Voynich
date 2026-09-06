# Phase 0 authoritative score-free Preflight B provenance

Date: 2026-09-06
Status: **AUTHORITATIVE PRE-TARGET SELECTION AUTHORITY**

Preflight B was executed after the one-time prereveal Amendment B and before any DECAY40/TILT10 S1/S2/H62/R1 target score existed.

## Authority

- GitHub Actions run: `34016904359`
- scientific / workflow head: `152bec1de1db393e46eb712f54320013ff6c301a`
- workflow conclusion: `success`
- artifact: `issue90-phase0-preflight-b`
- artifact ID: `9984254233`
- artifact digest: `sha256:a326b27fd5ed4c6caed371970c14ef347770f6a2732b818ca7ffee831b94c4a5`
- `phase0_preflight_b.json` SHA-256: `e016e0da642277adc86b257851eba459e946e40015622d127cb13b85afed33d4`
- explicit JSON field: `target_score_calls = 0`
- selection SHA-256: `8eb8c32709cdf65949e328ad9094f772dc512da52e1241232c44ed72ec856206`
- fold identity SHA-256: `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`

The artifact is the full pre-target authority. The failed prior B transport attempt at head `ef1206a...` completed the score-free computation but produced no artifact because strict JSON rejected a diagnostic `-inf`; the subsequent fix only labeled non-finite diagnostic values for transport and did not alter model mathematics or target access.

## Final target-blind selection

The one-time extended decay-scale grid was `{1,2,4,8,16,32,64,128,INF}`, with history still bounded to the previous at most 40 surface tokens.

All five outer-fold selectors independently chose the same **interior** scale `tau=32`:

| outer fold | family | pi | tau |
|---:|---|---:|---:|
| 0 | DECAY40 | 0.21 | 32 |
| 1 | DECAY40 | 0.21 | 32 |
| 2 | DECAY40 | 0.20 | 32 |
| 3 | DECAY40 | 0.21 | 32 |
| 4 | DECAY40 | 0.21 | 32 |

Thus the Preflight-A `tau=32` boundary hit was not an arbitrary truncation artifact.

Best nested-validation log-likelihood differences relative to `tau=32`:

| outer fold | tau=64 | tau=128 | uniform-40 `INF` |
|---:|---:|---:|---:|
| 0 | -7.624 | -25.310 | -52.478 |
| 1 | -3.268 | -18.458 | -42.961 |
| 2 | -11.545 | -30.221 | -57.488 |
| 3 | -3.922 | -19.264 | -43.770 |
| 4 | -6.862 | -24.218 | -51.115 |

The selector therefore supports a broad but non-uniform recency kernel inside the frozen 40-token window. No further Phase-0 tau or history-window extension is licensed.

## Predictive-only result

No S1/S2/H62/R1 target metric entered model or hyperparameter selection.

- frozen X0 V2: `9.7089061017 bits/token`
- Issue #81 X2-HARD10 replay: `9.6495705599 bits/token`
- X2 gain over X0: `0.0593355418 bits/token`
- selected DECAY40: `9.5961811202 bits/token`
- selected gain over X0: **`0.1127249815 bits/token`**
- selected gain positive in **5/5** outer folds: `0.1098184, 0.1169346, 0.1403904, 0.1028663, 0.0936153 bits/token`
- frozen predictive criterion: **PASS**

X2-HARD10 replay again selected `pi=0.10` in all five folds, reproducing the archived Issue #81 likelihood result.

TILT10 did not win any outer fold. The local predictive gain is therefore better captured, under this frozen candidate set, by a recency-weighted edit-1 memory branch than by the tested multiplicative soft V2 tilt.

## Frozen selected-generation hashes

These score-free hashes were produced before target scoring and must be reproduced byte-for-byte by the first-reveal implementation before S2/H62/R1 scoring:

- rep0: `ee594b3a8b3c3881f0c2aace1c7e5f694d8c6bada8b17ef22e831c2e9b161ee4`
- rep1: `560ca8529279354850420b92fee177b7980436ced6abfe760b79a4b68342fdea`
- rep2: `a8971db75d1cedc79c2bed379d3e5393e1b976abd3d338be356a17369efbb002`

## Firewall transition

This provenance freezes candidate identity, hyperparameters, predictive evidence and generated populations. Only after this commit may the Phase-0 first-reveal implementation expose S2, raw H62, H62 profile and R1 for these exact frozen selected generations.

No result from that reveal may alter the selections above.