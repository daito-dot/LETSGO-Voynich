# Issue #58B — signed occupancy-graph stability first-reveal report

Status: **FIRST REVEAL COMPLETE — FROZEN CLASSIFICATIONS AUDITED**

Parent: Issue #62 under umbrella Issue #58.

## 1. Research object

This phase concerns the internal construction of **space-delimited Voynich tokens** under the frozen 12-slot representation. It is not sentence-level syntax, and it does not assume that visible spaces are proven natural-language word boundaries.

Program-level orientation is recorded in `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

Issue #58A established a broad signed occupancy graph across all 66 unordered slot pairs. #58B asked whether that complete graph is recognizably shared across externally defined Currier/section/line-position strata, or whether the pooled graph is materially a mixture.

## 2. Frozen source and population

Source:

- repository: `matthewdgreen/cipher_benchmark`
- commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`
- file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`
- required Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- primary parser policy: `min`
- non-promoting parser sensitivity: `max`
- physical-leaf split: frozen five folds inherited from #55/#58A

Population reproduced before target scoring:

- visible tokens: `32,570`
- parsed tokens: `25,071`
- parse coverage: `0.7697574455`

Primary supported strata:

- Herbal Currier A (`AH`): `5,520`
- Herbal Currier B (`BH`): `2,449`
- Currier-B section B (`BB`): `4,936`
- Currier-B section S (`BS`): `7,748`
- line-initial: `2,915`
- line-interior: `19,556`
- line-final: `2,585`

The source audit was completed before target pair scoring and remains archived under `source-audit/`.

## 3. Frozen primary statistic

Every stratum was represented by all 66 pairwise slot-occupancy relations using the preregistered `K_other`-conditional Jeffreys-smoothed Mantel-Haenszel common odds ratio mapped to Yule Q.

For each planned contrast the primary similarity was Pearson correlation across the complete 66-edge signed graph.

Reliability and transfer were assessed with the frozen five physical-leaf folds.

The null used exactly 1,000 deterministic line-local slot-occupancy relocations. It preserved each line's length, line x slot occupied count, metadata labels, leaf fold and token-position labels while destroying same-token cross-slot pairing. Family-wise `p_maxT` used the maximum graph correlation across all seven planned contrasts.

## 4. Frozen first-reveal classifications

Primary register/section classification:

> **`CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`**

Position classification:

> **`LINE-POSITION GRAPH STABILITY INCONCLUSIVE`**

All seven planned contrasts were individually `INCONCLUSIVE` under the frozen gates.

| Contrast | R_full | p_maxT | W source | W target | X source→target | X target→source | Frozen class |
|---|---:|---:|---:|---:|---:|---:|---|
| Currier A vs B within Herbal | 0.6995 | 1.0000 | 0.9693 | 0.9442 | 0.6723 | 0.7180 | INCONCLUSIVE |
| section B vs H within Currier B | 0.9484 | 0.5475 | 0.9757 | 0.9442 | 0.9095 | 0.9358 | INCONCLUSIVE |
| section B vs S within Currier B | 0.9613 | 0.0849 | 0.9757 | 0.9686 | 0.9313 | 0.9460 | INCONCLUSIVE |
| section H vs S within Currier B | 0.9458 | 0.6484 | 0.9442 | 0.9686 | 0.9254 | 0.9040 | INCONCLUSIVE |
| initial vs final | 0.8896 | 1.0000 | 0.9498 | 0.9619 | 0.8624 | 0.8365 | INCONCLUSIVE |
| initial vs interior | 0.8682 | 1.0000 | 0.9498 | 0.9891 | 0.8635 | 0.7866 | INCONCLUSIVE |
| interior vs final | 0.9431 | 0.7453 | 0.9891 | 0.9619 | 0.9004 | 0.9360 | INCONCLUSIVE |

## 5. Why high observed correlations did not establish a shared graph

The observed graphs are numerically very similar in most comparisons. Within-stratum fold reliability is also high, and cross-stratum held-out transfer is generally strong.

However, the preregistered null produced an unusually high similarity baseline:

- null maxT minimum: `0.9086826294`
- null maxT median: `0.9493879329`
- null maxT 95th percentile: `0.9632268790`
- null maxT maximum: `0.9744829266`

This means that a complete 66-edge correlation around `0.94–0.96` is not by itself surprising after same-token pairings are destroyed while line-local slot prevalence is retained.

The test therefore cannot promote the visually high real correlations to evidence for a deeper manuscript-wide interaction graph.

## 6. Why this also does not establish mixture or difference

The frozen `DIFFERENT_OR_MIXTURE` gate required reliable strata plus either `R_full < 0.40` or directional held-out transfer below `0.30`.

No planned contrast came close to those practical difference gates.

Therefore the correct result is genuinely **inconclusive**, not a hidden negative result:

- **not supported:** a shared deep signed interaction graph under this raw graph-similarity test;
- **not supported:** material Currier/section/position divergence under the frozen difference gates;
- **retained:** substantial token-internal occupancy structure and high numerical cross-stratum resemblance;
- **new methodological constraint:** much of whole-graph resemblance can be generated by lower-order line-local occupancy architecture.

## 7. Non-promoting sensitivities

The parser-`max` real-data conditional graph correlations remained high (`0.8495–0.9548` across the seven contrasts), so the basic observation of numerical resemblance is not a `min`-parser artifact.

The raw-unconditional `min` correlations also remained broadly high (`0.7345–0.9649`). These sensitivities do not alter the frozen primary classification.

## 8. Scientific consequence

Do not repeat the same whole-graph correlation with a new threshold.

The next plan-first phase should ask whether there is an **excess/residual interaction graph after removing the null-expected contribution of line-local slot prevalence**.

The follow-up must first test whether a graph-level residual exists at all. Only if that existence gate survives should cross-stratum residual transfer be interpreted.

To avoid defining and validating residuals on the same simulated populations, the next design should freeze separate reference-null and test-null sets before reveal.

This consequence is a new hypothesis generated by #58B. It is not a post-hoc repair of the #58B confirmatory test.

## 9. Interpretation boundary

This result does not establish:

- that spaces are genuine linguistic word boundaries;
- sentence grammar;
- meanings for any slot;
- a cipher table or plaintext mapping;
- one historical generator;
- semantic absence;
- decipherment.

Its role is narrower: determine whether the internal construction constraints of one space-delimited token can be promoted from a representation-specific occupancy pattern to a stable, non-trivial manuscript-wide generative constraint.

## 10. First-reveal provenance

Scientific first reveal:

- branch head: `ebc794567574e20eac82df6a856d5ea4dd72b9cb`
- Actions run: `33437742982`
- preflight job: `99638198622`
- target job: `99638298655`
- artifact ID: `9775074050`
- artifact ZIP digest: `sha256:ef02c4e7333cef13a9a4793a6bdc0a91996feb416bd32756e7254ea33c6f329f`
- raw result JSON SHA-256: `45024fd1d15b2d2484ffc26657ccc8007fd6a04dc3ed1b53b243f77ba455f8a0`

The exact first-reveal result is preserved under `first-reveal/` together with provenance and checksums.