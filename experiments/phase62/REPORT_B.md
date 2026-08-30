# Phase 62B — N0 structured-medieval baseline

Status: **N0 FAILS the frozen joint broad-regime gate**.

This phase evaluated source-native meaningful structured medieval text only. C0, frozen A1, and the sealed H62-P1 prospective statistic were not evaluated.

## Frozen inputs and audit trail

- Voynich: exact ZL3b blob `2a4533ab9bdfa85db9bad602d590978953055df1`
- CREMMA: `HTR-United/CREMMA-Medieval-LAT@292525969ad98380b398e6606a9c2a36d51913ae`
- primary manuscripts: BIS193, CLM13027, Mazarine915, UBL758
- manuscript, not entry, is the equal-weight replication unit
- H318 is a predeclared sensitivity only

Execution was deterministic under `PLAN.md` and `IMPLEMENTATION_B.md`.

Raw workflow artifact:

- run `33312611679`
- artifact `9732449121`
- artifact ZIP SHA-256 `da12b0171f7f6f5a0762ad17fee5f13d55df199e5f65b0cf935ceb0e04ba8f9d`

A compact durable numerical record is `phase62b_n0_results.json`.

## Effective sample after source-native item segmentation

The corpus-wide source panel was frozen using literal-pilcrow candidate availability before this score was computed. The stricter actual item parser then required each item to end at the next pilcrow and applied the preregistered base/S1 eligibility rules.

| dataset | total items | base eligible S2/S3 | S1 eligible |
|---|---:|---:|---:|
| Voynich | 736 | 594 | 431 |
| BIS193 | 98 | 51 | 40 |
| CLM13027 | 53 | 29 | 20 |
| Mazarine915 | 80 | 32 | 29 |
| UBL758 | 10 | 5 | 5 |
| H318 sensitivity | 5 | 3 | 2 |

The primary manuscripts remain exactly the frozen four-manuscript panel despite these post-segmentation counts.

## Primary result

Across the five outer Voynich physical-leaf folds:

| target | held-out Voynich | N0 equal-manuscript | N0 / Voynich | gate |
|---|---:|---:|---:|---|
| **S1 entry-specific projection** | 0.87599 | **-0.85872** | **-0.980** | FAIL |
| **S2 local near-family excess** | 0.04388 | **0.00585** | **0.133** | FAIL |
| **S3 line-position eta2 mean** | 0.02827 | **0.02797** | **0.989** | PASS |

N0 therefore fails two of the three preregistered primary dimensions.

## S1 — source-native medieval entries point the wrong way on the common 8D direction

The striking result is not merely that N0 has a smaller entry effect. Under the training-derived Voynich generic 8D entry-minus-pseudo direction, the equal-manuscript N0 projection is negative.

Every primary manuscript is negative when averaged over the five Voynich folds:

- BIS193: **-1.389**
- CLM13027: **-1.420**
- Mazarine915: **-0.362**
- UBL758: **-0.264**

The equal-manuscript N0 aggregate is negative in **all five** Voynich outer folds, while the held-out Voynich projection is positive in all five.

This is robust to manuscript omission. Every leave-one-manuscript-out aggregate remains negative.

Interpretation:

> source-native medieval entry structure exists, but under the new sample-size-neutral cross-representation 8D scorecard its average direction is not the Voynich entry specialization.

This does not erase Phase59. Phase59 used a different development representation and deliberately showed that medieval entry structure can span part of the broader Voynich transition space. Phase62 asks the stricter prospective question of whether an objective all-eligible structured-medieval panel reproduces the specific common held-out direction; N0 does not.

## S2 — ordinary structured Latin has much weaker local near-family activation

Voynich held-out locality excess above the vocabulary/line-layout preserving null is:

**0.04388**.

N0 equal-manuscript excess is:

**0.00585**, or about **13.3%** of the Voynich level.

Per manuscript:

- BIS193: 0.00520
- CLM13027: 0.00814
- Mazarine915: 0.00770
- UBL758: 0.00236

Leave-one-manuscript-out N0/Voynich ratios remain only about **0.116–0.160**.

Therefore the result is not explained by one low-locality manuscript dominating the aggregate.

Interpretation:

> meaningful structured medieval text can naturally produce some local edit-neighbour clustering, but the tested source-native documents do not approach the Voynich excess after controlling for each document's own vocabulary and line-token layout.

## S3 — generic line-position grammar is ordinary enough to reproduce

Here N0 performs very differently.

Voynich mean eta2: **0.02827**  
N0 mean eta2: **0.02797**  
ratio: **0.989**

This survives manuscript heterogeneity reasonably well: leave-one-manuscript-out ratios are approximately 0.72–1.21.

This is an important downgrade of evidential specificity:

> a generic line-position effect at this resolution is not a strong discriminator between Voynich and ordinary structured medieval documents.

Line-position structure should therefore carry much less weight when cited alone.

## H318 sensitivity

H318 was predeclared as a small Phase52 medical/recipe sensitivity and remains outside the primary panel because it has only four audit-eligible pilcrow candidates and only two S1-eligible items under strict item segmentation.

Its result is highly different:

- S1 mean: +2.046
- S2: -0.01796
- S3: 0.18236

The tiny sample can align strongly on entry direction while failing locality and massively overproducing line-position eta2. This is exactly why Phase62 does not promote a favorable small semantic subset into the primary result after inspection.

## Decision

N0 is **not materially competitive** under the frozen Phase62 exposed scorecard.

The current evidence now separates three facts more cleanly:

1. **generic medieval line-position grammar is easy to reproduce** — N0 passes S3;
2. **the sample-size-neutral Voynich entry specialization is not reproduced by the objective source-native N0 panel** — N0 fails S1 and is opposite in sign;
3. **Voynich local near-family activation remains much stronger than these meaningful medieval controls after vocabulary/layout correction** — N0 fails S2.

This does not favor G/A1 yet, because A1 has not been evaluated on this common Phase62 scorecard and carries substantial target dependence through the supplied Voynich vocabulary and explicit mechanisms.

## Next action — unchanged by the result

Proceed exactly to the already-frozen Phase62C:

- evaluate the five predeclared global boundary-blind reversible C0 transforms;
- re-score frozen A1 under the same common S1–S3 representation without retuning it;
- keep H62-P1 sealed;
- do not create C1 or A2 inside this comparison.

Only after Phase62C is complete should Phase62D freeze the exposed-score structural ranking/unresolved set.