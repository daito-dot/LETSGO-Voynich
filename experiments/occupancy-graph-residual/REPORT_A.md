# Issue #58C / #64 — null-residual token-construction graph first-reveal report

Status: **FIRST REVEAL COMPLETE — FROZEN CLASSIFICATION AUDITED**

Parent: Issue #64 under umbrella Issue #58.

## 1. Research object

This phase studies the internal construction of **one space-delimited Voynich token** under the frozen 12-slot representation.

It is not sentence-level syntax, and visible spaces are not assumed to be proven natural-language word boundaries.

Program orientation: `research/TOKEN_CONSTRUCTION_PROGRAM.md`.

The decipherment-relevant architectural question is whether a later inverse model can treat one non-trivial token-construction mechanism as shared across the manuscript, or whether multiple/hierarchical generators are required.

## 2. Why #58C was necessary

Issue #58A established a broad signed 66-edge occupancy graph.

Issue #58B then showed that raw complete-graph similarity is not sufficiently discriminating: real Currier/section/position graphs looked highly similar, but a line-local null that destroyed same-token cross-slot pairing while preserving line×slot occupancy marginals also produced whole-graph correlations near `0.95`.

Frozen #58B result:

- `CURRIER/SECTION GRAPH STABILITY INCONCLUSIVE`
- `LINE-POSITION GRAPH STABILITY INCONCLUSIVE`

#58C therefore asked a new, logically prior question:

> **After calibrating each edge against the association expected from the exact line-local occupancy null, is there any reproducible graph-level residual interaction signal left at all?**

Only if that existence gate passed was cross-stratum residual transfer allowed to promote.

## 3. Frozen design

The preregistered plan predates the target executable.

Frozen inputs and representation:

- source repository: `matthewdgreen/cipher_benchmark`;
- source commit: `315f0cad4de3d021bd4185765c037cf2a28d341c`;
- source file: `benchmark/unsolved/sources/voynich/transcriptions/ZL3b-n.txt`;
- required source Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`;
- primary parser policy: `min`;
- parser `max`: non-promoting sensitivity;
- same frozen 12-slot grammar and five physical-leaf folds as #55/#58A/#58B;
- all `C(12,2)=66` unordered slot pairs retained.

Primary base association remained the `K_other`-conditional Jeffreys-smoothed Mantel-Haenszel odds ratio mapped to Yule Q.

### Independent null split

Exactly 1,000 deterministic **reference nulls** were used only to define the residual calibration for each group/view/edge.

A separate 1,000 deterministic **test nulls** were used only to validate graph-level residual existence and residual similarity.

The two namespaces were frozen and disjoint before reveal.

### Residual transform

For each fixed group/view/edge, the candidate real or test-null Q value was mapped to its mid-rank within the 1,000 reference-null Q values and then transformed through the standard-normal quantile function.

The resulting 66-edge vector is the residual graph `Z`.

This removes the need to choose a post-reveal mean/median or SD/MAD normalization and calibrates every edge against its own null sampling distribution.

### Primary existence statistic

Residual energy:

`E = sqrt(mean_e Z_e^2)`

over all 66 edges.

The primary pooled graph existed only if both:

- independent test-null `p_exist_ALL <= .01`;
- physical-leaf residual reliability `W_ALL >= .50`.

If this failed, cross-stratum residual similarity was not allowed to rescue the phase.

## 4. First-reveal result

Frozen overall classification:

> **`RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`**

This is the central #58C result.

### 4.1 Pooled residual existence

Real full-manuscript residual energy:

- `E_ALL = 3.2315507868`.

Independent 1,000-test-null distribution:

- minimum: `0.7258061085`;
- median: `0.9900432214`;
- 95th percentile: `1.1342638078`;
- maximum: `1.2831839812`.

Empirical significance:

- `p_exist_ALL = 1/1001 = 0.000999000999`.

Physical-leaf reproducibility:

- `W_ALL = 0.9447148364`.

Therefore both frozen existence gates passed decisively.

The real residual energy is not a marginal threshold effect: it is roughly 2.5 times the maximum value seen in the independent test-null ensemble.

## 5. Residual existence within every planned stratum

All seven non-ALL strata passed the frozen family-wise residual-existence gate with `p_E,maxT = 1/1001` and high physical-leaf reliability.

| Stratum | Residual energy E | W | p_E,maxT | Supported? |
|---|---:|---:|---:|---|
| Currier A within Herbal (AH) | 2.9462 | 0.9188 | 0.000999 | yes |
| Currier B within Herbal (BH) | 3.0639 | 0.8968 | 0.000999 | yes |
| section B within Currier B (BB) | 3.1652 | 0.9362 | 0.000999 | yes |
| section S within Currier B (BS) | 3.1421 | 0.9308 | 0.000999 | yes |
| line initial | 3.0287 | 0.9093 | 0.000999 | yes |
| line interior | 3.2029 | 0.9551 | 0.000999 | yes |
| line final | 3.0255 | 0.9343 | 0.000999 | yes |

Independent group-energy maxT null distribution:

- median: `1.1118844955`;
- 95th percentile: `1.2144549874`;
- maximum: `1.3178412558`.

Thus the residual association system is not confined to one Currier class, one section, or one line position.

## 6. Residual topology across strata

The independent test-null maximum correlation across all seven planned contrasts had:

- median: `0.1462279942`;
- 95th percentile: `0.2858787177`;
- maximum: `0.4330970654`.

Every real contrast exceeded the entire 1,000-null maxT ensemble, so every planned residual-similarity test had `p_R,maxT = 1/1001`.

| Contrast | R_Z | X source→target | X target→source | Frozen class |
|---|---:|---:|---:|---|
| Currier A vs B within Herbal | 0.6487 | 0.5911 | 0.6611 | RELATED_RESIDUAL_BUT_MODULATED |
| section B vs H within Currier B | 0.8240 | 0.7676 | 0.8379 | STABLE_RESIDUAL |
| section B vs S within Currier B | 0.8791 | 0.8863 | 0.8798 | STABLE_RESIDUAL |
| section H vs S within Currier B | 0.8848 | 0.8580 | 0.8181 | STABLE_RESIDUAL |
| initial vs final | 0.7471 | 0.7810 | 0.7174 | RELATED_RESIDUAL_BUT_MODULATED |
| initial vs interior | 0.6247 | 0.6745 | 0.5579 | RELATED_RESIDUAL_BUT_MODULATED |
| interior vs final | 0.8237 | 0.7918 | 0.8416 | STABLE_RESIDUAL |

Frozen family classifications:

> **`REGISTER/SECTION RESIDUAL MODULATION`**

> **`LINE-POSITION RESIDUAL MODULATION`**

No contrast met the preregistered `DIFFERENT_RESIDUAL_OR_MIXTURE` gate.

Therefore the result is not evidence for wholly separate token grammars. The supported model at this stage is a **strong shared residual construction core with measurable modulation**, especially between Currier A/B within Herbal and around line-initial tokens.

## 7. What #58C changes scientifically

#58B left open a serious alternative explanation:

> perhaps the apparent 66-edge grammar was largely just a consequence of some slots being generally common/rare within the same kinds of lines.

#58C directly controls that mechanism edge by edge using an independently estimated line-local null baseline.

That explanation is now insufficient.

A broad, reproducible residual interaction system remains after the lower-order occupancy architecture is removed.

This supports the stronger statement:

> **Under the frozen 12-slot representation, Voynich space-delimited tokens contain substantial token-internal construction constraints that cannot be explained by line-local slot prevalence alone. A large part of that residual constraint system is shared across the tested manuscript strata, but it is not exactly invariant.**

This is materially stronger than the raw #58A/#58B occupancy-graph observation.

## 8. Parser `max` non-promoting sensitivity

The alternative `max` parser policy reproduced the qualitative geometry without promoting the primary result:

- pooled residual energy: `3.1178578405`;
- pooled physical-leaf reliability: `0.9532616582`;
- Currier A/B residual correlation: `0.6760604991`;
- initial/final: `0.7118818286`;
- initial/interior: `0.6228036227`;
- interior/final: `0.8306658418`;
- section B/H: `0.7823039921`;
- section B/S: `0.7791739142`;
- section H/S: `0.8580757628`.

This makes the main qualitative conclusion unlikely to be a peculiarity of choosing parser `min` rather than `max`.

## 9. Post-reveal descriptive breadth — non-confirmatory

Only after the frozen graph-level classification was known, the pooled residual vector was inspected descriptively.

Because the empirical normal-score transform uses only 1,000 reference nulls, values outside the whole reference range saturate near `|Z| = 3.2908`.

In the pooled real graph:

- 38/66 edges are negative and 28/66 positive;
- 61/66 edges reach at least `|Z| >= 3.29`;
- 36 hit the lower finite-reference extreme and 25 the upper extreme.

This supports the qualitative impression that the result is broad rather than driven by one selected edge, but the finite-reference saturation means **individual saturated edge magnitudes/ranks must not be interpreted as finely resolved evidence**.

Residual-sign agreement was also high descriptively:

- Currier A/B within Herbal: 51/66;
- section B/H: 57/66;
- section B/S: 61/66;
- section H/S: 60/66;
- initial/interior: 53/66;
- initial/final: 57/66;
- interior/final: 58/66.

These counts are descriptive only; the preregistered complete-graph tests above are the confirmatory evidence.

## 10. Interpretation boundary

#58C does **not** establish:

- that visible spaces are linguistic word boundaries;
- sentence-level grammar;
- semantic meanings for slots;
- a plaintext alphabet;
- a cipher table;
- a specific historical production algorithm;
- that the underlying information is natural language, ciphered language, artificial text, or meaningless text;
- decipherment.

What it does establish under the tested representation is a much stronger **surface-generation constraint**.

## 11. Next scientific requirement

Before using this residual graph to constrain a reversible/inverse decoding model, test whether the finding survives a materially independent transcription/reading or equivalent representation perturbation without retuning the token grammar after seeing the result.

The next question should therefore be:

> **Is the residual token-construction core manuscript-real, or is a material part of it specific to the ZL3b transcription / parser representation?**

If the residual existence and core/modulation geometry survive an independent transcription, the stable residual constraints become strong candidates for prospective restrictions on reversible generative/inverse models.

If they do not, the current result must be narrowed to a representation-dependent structural fact.

## 12. First-reveal provenance

Scientific first reveal:

- authorized by PR #65;
- exact checked-out branch head: `aa64f31942bc21f75695fcdf0065e3e7e922f687`;
- Actions run: `33442306206`;
- preflight job: `99653167521`;
- target-first-reveal job: `99653243946`;
- artifact ID: `9776775160`;
- artifact ZIP digest: `sha256:ed3c28b214ed78b9c19a67182eac7e867e51bc3e13ef4ee6c778ef329f9a7650`;
- raw result JSON SHA-256: `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`;
- deterministic gzip SHA-256: `666cfa3e211b097b30025a7947cf8bbb22e1bf24cae18a55d99017328b511d4f`.

The JSON metadata contains GitHub's pull-request synthetic merge-context SHA (`24b668f9e978f8464a12e674201dae46cd73ac5e`). The workflow log is authoritative for the actual explicitly checked-out scientific head `aa64f319...`.

The exact first-reveal bytes are permanently preserved under `first-reveal/`; later reruns may verify the science but must not replace this first reveal.