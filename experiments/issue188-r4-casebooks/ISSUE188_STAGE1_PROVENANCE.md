# Issue #188 — R4 / Casebooks Stage1 provenance and decision

Date: 2026-09-08  
Parent: Issue #188 / Issue #172  
Status: **COMPLETE — `MIXED_OR_UNSTABLE`**

## Frozen chronology

The scientific score was not computed until the following were committed in order:

1. Stage1 plan commit `e3350632fb142800a3fcb712036537ee412390c0`;
2. scorer commit `a1b517aa149b5cbfe0339fdd49b5e95d7c09b48d`;
3. workflow commit / first-reveal head `839b4dbe165a8773eb5c23c6da900f81200d1715`.

Frozen blobs:

- Stage1 plan: `763b2a8c8f5661745a1024d2109b8df8ae9a6a0b`
- Stage1 scorer: `0e3053b7ea2d110e938aef32b2e2e5acac0bc051`
- Stage1 workflow: `465a9773b6bd96ce76094c86c5711cc7d1516823`
- Gate0 extractor: `9792e32a0cb86bd293491701625e8fe2d530aacd`
- historical Phase62B S1 implementation: `e0ada366845c7a6c5a5dd75de91fe262b72a94b6`
- historical Phase62B result: `e798b3af89fd029660f9a90750985630c3d283ac`
- Casebooks commit: `9d42295d72b5ba8889575a32d79311cc72bce73a`
- ZL3b blob: `2a4533ab9bdfa85db9bad602d590978953055df1`

The scorer reproduced all five historical held-out Voynich S1 values exactly within the frozen tolerance before evaluating Casebooks.

## First reveal authority

- PR: #190
- workflow: `Issue188 R4 Casebooks Stage1`
- run ID: `34166155488`
- job ID: `101877469075`
- conclusion: `success`
- artifact: `issue188-r4-casebooks-stage1`
- artifact ID: `10034216152`
- artifact ZIP SHA-256: `c9f52459c19eef54cd24c5ed1c6c77a6957ec2501685cd4ed39d22e1944c4368`
- raw result JSON SHA-256: `40a20c56c242a51d42b70f3e7633f4908b83b7d82dddf5dc784c2cc8f81718db`
- raw result Git blob: `fde5b2896687affefae453c514e9b11efd501307`

No second score, threshold change, source repair, sign flip, or consultation-class rescue is used in this interpretation.

## Frozen primary outcome

Classification:

> **`MIXED_OR_UNSTABLE`**

The equal-volume primary statistic is strongly positive:

- 51 pre-authorized source volumes;
- fold means: `0.63765, 0.61801, 0.64056, 0.65315, 0.63366`;
- positive folds: **5/5**;
- grand mean: **0.63661**;
- Voynich mean: `0.87599`;
- numeric ratio: **0.72672×**;
- stable-positive volumes: **36/51**;
- stable-negative volumes: **14/51**.

Thus the equal-volume statistic by itself clears the frozen sign, fold-stability, stable-volume-count, and numeric historical magnitude range.

It does **not** receive `R4_MAGNITUDE_COMPATIBLE`, because the preregistration allowed that label only after the complete direction-replication rule passed.

## Why the complete direction rule failed

The two predeclared independent practices have opposite signs.

| stratum | n eligible | mean S1 | positive folds |
|---|---:|---:|---:|
| Forman practice | 114 | **-0.30950** | 0/5 |
| Napier practice | 968 | **+0.69186** | 5/5 |
| exact `#sforman` hand | 108 | **-0.36281** | 0/5 |
| exact `#rnapier` hand | 866 | **+0.60980** | 5/5 |

The practice split is therefore mirrored by the two principal exact hand strata. It is not an artifact of the equal-volume weighting rule.

The all-eligible pooled Casebooks result is positive (`0.58636`, 5/5 positive), but pooled support was explicitly forbidden from overriding the practice replication failure.

## Volume heterogeneity

The primary volume population is not uniformly positive.

- 36 volumes have positive mean S1, all 36 meeting the frozen stable-positive rule;
- 15 volumes have negative mean S1;
- 14 of those 15 meet the stable-negative rule;
- one negative volume is internally mixed across target folds.

Among the six Forman primary volumes:

- `Forman001`: `+0.56340`, 5/5 positive;
- `Forman002`: `+0.59674`, 5/5 positive;
- `Forman003`: `-0.01154`, 2/5 positive;
- `Forman004`: `-1.48789`, 0/5 positive;
- `Forman005`: `-0.33132`, 0/5 positive;
- `Forman006`: `-1.50168`, 0/5 positive.

Napier contributes 45 primary volumes, of which 34 are stable-positive and 11 stable-negative.

These volume details are descriptive parts of the frozen primary population. They are not used to reclassify a favored subgroup after reveal.

## Mechanism-discrimination consequence

The Casebooks result rules out a simple interpretation of R4 as a generic property of one document architecture.

A source-authenticated meaningful historical record corpus can produce a positive S1 of Voynich-like order under the unchanged statistic, but the sign changes sharply across predeclared production practices and principal hands inside the same corpus. Therefore the paragraph-entry effect is sensitive to production practice / scribal realization, not only to broad semantic genre or to the existence of paragraph boundaries.

This weakens R4 as a standalone anti-language or anti-plaintext discriminator. It does **not** make R4 non-informative: Forman is consistently wrong-sign while Napier is consistently positive at the practice/hand aggregate, and source volumes remain heterogeneous. The useful question has narrowed from “can meaningful text produce positive R4?” to “what independently defined production features make the signed entry contrast positive or negative?”

The result also does not license treating Napier alone as a successful Voynich mechanism. The complete preregistered external classification is `MIXED_OR_UNSTABLE`, and post-reveal subgroup promotion is forbidden.

## Routing

Priority 1 has now established three materially different external facts:

1. ordinary CREMMA structured Latin primary controls were wrong-sign;
2. the frozen Alberti paragraph reset was wrong-sign;
3. Casebooks contains a large positive external regime, but it splits by predeclared practice/hand.

A further Priority-1 experiment should only be run if it prospectively discriminates a production factor implicated by this split; simply adding another broad genre corpus has lower value. Otherwise the near-term sequence can move to Priority 2, the productive/open-vocabulary responsibility audit, while retaining R4 as a compatibility responsibility with production-practice sensitivity.
