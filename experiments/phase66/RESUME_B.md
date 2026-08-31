# Phase 66 resume

Status: **Phase66B closed — M8-B2 NO DETECTED ATTRIBUTE-LABEL RELATION**

## Accepted result

The prospective Phase66 test decomposed the images into independently predefined botanical morphology and background-normalized color measurements, independently froze a generic structural label representation, and only then connected the two.

Primary f102v2:

- T `0.00301060073648908`
- exact one-sided p `0.4896875`
- 86,400 row-restricted permutations
- FAIL

Replication f100v:

- T `-0.15277449822904368`
- exact one-sided p `0.7352719907407408`
- 69,120 row-restricted permutations
- FAIL

Classification: **`M8-B2 NO DETECTED ATTRIBUTE-LABEL RELATION`**.

## What is now closed

Do not rerun Phase66B by changing weights, morphology eligibility, color thresholds/clusters, text vocabulary, page chronology, row structure, or pass thresholds. Such a run would be a new hypothesis, not a repair.

Phase65B and Phase66B together show that two prospective bridges failed on the same localized pharmaceutical population:

1. whole-crop visual similarity ↔ generic string similarity (Phase65B);
2. explicit botanical morphology + normalized color ↔ generic label structural similarity (Phase66B).

This narrows these particular forms of direct morphology-to-label-form coupling.

## What remains open

Do not conclude that attached labels lack semantics. A semantic naming or categorical system does not have to make morphologically similar objects globally string-similar. Plant identity, lexical classes, inventory roles, ordinal/categorical attributes, or another external mapping would require a genuinely different independently frozen prediction.

The positive f100v M-row rho in Phase66B is descriptive only and cannot be promoted into a primary result after the failed global test.

## Frozen provenance

Scientific executable SHA256:
`698252876f7a6187ac8c80f1e95372e2afa3c8e3dc30f7e62170b3ad492a3290`

Synthetic preflight:
- run `33361388517`
- artifact `9746798875`
- all gates pass

Primary:
- run `33361478853`
- artifact `9746827681`
- raw result SHA256 `5b259f53a503132ffa430ff83a606d6141168bb86966ee14618b58f718100fc2`

Replication:
- run `33361602833`
- artifact `9746865196`
- raw result SHA256 `1c5a1b2935389096e813306dfa4bbf9e71acb2d74029ddebf140b38102699cc1`

Canonical interpretation is in `REPORT_B.md`.
