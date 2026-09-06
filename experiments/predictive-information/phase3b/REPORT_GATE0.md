# Issue #107 Phase 3B — observable hand/domain metadata Gate 0

Date: 2026-09-06
Status: **AUTHORITATIVE SCORE-FREE RESULT**
Parent: Issue #88

## Question

Can independently defined IVTFF writing-hand or illustration/domain metadata be crossed with Currier A/B strongly enough to explain the roughly twofold Phase-3A PREV_PARAS strength difference without introducing a hidden state?

## Result

> **NO ADEQUATELY CROSSED OBSERVABLE FACTOR**

Under the preregistered support-only criterion, none of `$H` Davis writing hand, `$I` illustration type, or `$C` legacy Currier hand has at least two levels that are each represented in both Currier A and B across >=4/5 frozen physical-leaf folds.

Therefore no multilevel hand/domain-conditioned predictive model is licensed from this Gate.

## Writing hand is essentially confounded with Currier A/B

Davis hand `$H` is highly informative as manuscript metadata but statistically unsuitable for the intended conditional test because its levels are nearly separated by Currier class:

| Davis hand | Currier A accepted | A folds | Currier B accepted | B folds |
|---|---:|---:|---:|---:|
| H1 | 7,274 | 5 | 0 | 0 |
| H2 | 0 | 0 | 8,422 | 5 |
| H3 | 426 | 1 | 8,050 | 5 |
| H5 | 0 | 0 | 549 | 4 |

H4 has no A/B prediction population after the frozen Currier exclusions.

The one mixed-hand numeric leaf is f115, where the source explicitly switches H=2/H=3 via legal text tags. The audit resolves those tags at token position rather than treating the page as one hand.

Because there is no adequately crossed pair of hands, a hand-conditioned model would be unable to separate hand from Currier regime. Fitting one anyway would convert confounding into an apparent explanatory state.

## Legacy Currier hand is even more confounded

The main `$C` levels are completely one-sided:

- C1: A 5,141 accepted tokens; B 0;
- C2: A 0; B 7,360;
- C3/C5/X/Y are B-only or sparse;
- C4 is A-only.

Legacy hand therefore cannot identify the A/B slow-strength difference independently either.

## Illustration/domain offers one common matched stratum

The illustration variable `$I` is also largely associated with Currier regime, but one level is strongly crossed:

> **Herbal (`I=H`)**

- Currier A: 5,520 accepted tokens, 47 numeric leaves, all 5 folds;
- Currier B: 2,449 accepted tokens, 16 leaves, all 5 folds.

Other major domains are one-sided or sparse:

- Biological (`I=B`): B only, 4,936 accepted tokens;
- Pharmaceutical (`I=P`): A only, 1,608;
- Stars (`I=S`): A 426 in 1 fold vs B 7,748 in 5 folds;
- Text-only (`I=T`): A 146 in 1 fold vs B 1,550 in 2 folds.

Thus illustration type fails as a **multilevel** crossed factor, but Herbal provides a valid matched-domain population for a narrower prospective test.

## What can and cannot be inferred

The Gate establishes a design constraint, not a historical explanation.

It does **not** show that writing hand causes Currier A/B differences. In fact, the data structure prevents that effect from being identified cleanly with the current corpus because hand and Currier are too confounded.

It also does not show that illustration/domain explains the difference. Only one domain, Herbal, is sufficiently common to both Currier strata to support a clean matched-domain comparison.

## Next licensed experiment

The highest-information next test is:

> **Repeat the Currier A/B parameter/transport comparison inside `I=H` Herbal only, using the same frozen V2 + LOCAL40 + PREV_PARAS mechanism family and original physical-leaf folds.**

This asks whether the approximately twofold A/B PREV_PARAS strength difference survives when domain composition is held fixed at the only adequately crossed illustration category.

Possible prospective interpretations:

- if A/B alpha values converge and exact PREV transfer becomes bidirectional within Herbal, Phase-3A asymmetry was substantially driven by domain composition;
- if the alpha gap and transfer asymmetry persist within Herbal, illustration/domain composition alone cannot explain the Currier dependence;
- either result still leaves hand confounded and does not license semantic or latent-state interpretation.

The matched-Herbal test requires its own frozen plan before predictive scoring.

## Audit validity

The metadata scanner exactly reproduced 32,570 visible and 25,071 parser-accepted tokens, with zero line-mapping mismatch, zero tag conformance violation, zero raw-L/Phase-3A authority mismatch, and valid corrected source order.

See `GATE0_PROVENANCE.md` for workflow/hash authority.