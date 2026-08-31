# Phase 66B — prospective botanical-attribute ↔ attached-label test

Status: **CLOSED — M8-B2 NO DETECTED ATTRIBUTE-LABEL RELATION**

## Question

Does a representation fixed before cross-modal inspection — externally grounded botanical morphology plus background-normalized color — carry object-level information about a separately frozen structural representation of the physically attached Voynich labels?

This test was designed to avoid holistic human visual-similarity judgment. Image attributes and text attributes were frozen independently before the first association statistic was revealed.

## Image side

Primary morphology features were limited by the Phase66A eligibility firewall to:

- `leaf_composition`
- `leaf_arrangement`
- `leaf_margin`

Color A was retained as a failed imaging preflight because fixed named HSV bins leaked parchment/scan coloration. Color B then used a preregistered parchment-background normalization and data-driven Lab clustering without pre-naming colors.

Color B selected three chromatic clusters by its frozen silhouette rule. The confirmatory image representation used:

- binary presence: C1, C2;
- continuous area fractions: C1, C2, C3.

No color threshold, cluster count, morphology state, or eligibility decision was changed after text association was opened.

## Text side

The ZL3b attached-label representation was frozen independently from image attributes. Five equally weighted structural groups were used:

1. glyph length;
2. first glyph;
3. last glyph;
4. morphology-blind frequent-unigram presence;
5. morphology-blind frequent-bigram presence.

The retained unigram and bigram vocabularies were fixed by prevalence only before association.

## Statistic and null

Within each physical row, all unordered object pairs were compared by:

- composite image-attribute distance;
- composite text-structure distance.

The row statistic was Spearman rho. The page statistic `T` was the pair-count-weighted mean of row rho values.

The exact null permuted complete label identities only within physical rows, holding all image measurements fixed.

Frozen pass rule:

- `T >= 0.20`, and
- exact one-sided `p <= 0.05`.

Primary page was f102v2. Replication page was f100v and was mandatory regardless of the primary result.

## Synthetic preflight

GitHub Actions run `33361388517` passed every frozen implementation gate before real association was opened, including exact permutation counts, aligned synthetic signal, independence control, U handling, and equivalence of optimized and direct Spearman computation.

Frozen scientific executable SHA256:

`698252876f7a6187ac8c80f1e95372e2afa3c8e3dc30f7e62170b3ad492a3290`

No scientific code or parameter was modified between primary and replication.

## Primary — f102v2

Workflow run: `33361478853`

Artifact: `9746827681`

Raw result SHA256: `5b259f53a503132ffa430ff83a606d6141168bb86966ee14618b58f718100fc2`

Result:

- `T = 0.00301060073648908`
- exact one-sided `p = 0.4896875`
- permutations = `86,400`
- pass = **false**

Row rho:

- L2: `-0.03942677655029598` (15 pairs)
- L3: `+0.06666666666666667` (10 pairs)

The primary page therefore showed essentially no global monotonic relation under the frozen representation.

## Replication — f100v

Workflow run: `33361602833`

Artifact: `9746865196`

Raw result SHA256: `1c5a1b2935389096e813306dfa4bbf9e71acb2d74029ddebf140b38102699cc1`

Result:

- `T = -0.15277449822904368`
- exact one-sided `p = 0.7352719907407408`
- permutations = `69,120`
- pass = **false**

Row rho:

- T: `-0.7142857142857143` (6 pairs)
- M: `+0.41818181818181815` (10 pairs)
- B: `-0.5428571428571428` (6 pairs)

The positive M-row value is descriptive only. It was not a preregistered standalone claim and cannot repair the failed page-level global test.

## Classification

Primary fail + replication fail gives the preregistered classification:

> **M8-B2 NO DETECTED ATTRIBUTE-LABEL RELATION**

Under this specific frozen representation, the tested botanical morphology/color attributes did not predict the generic structural form of their attached label strings.

## What this does not mean

This result does **not** establish that:

- the drawings lack meaningful botanical distinctions;
- colors are meaningless;
- attached labels lack semantics;
- labels cannot contain plant names or categorical information;
- Voynichese is meaningless or non-linguistic;
- any particular cipher/language hypothesis is false.

The result is narrower: neither whole-image morphology similarity in Phase65B nor this explicit morphology+color/global-label-structure representation in Phase66B produced a replicated positive relation on this 24-object pharmaceutical population.

A semantic system need not encode taxonomically similar plants with globally similar strings. If content work continues, the next hypothesis must make a genuinely different prospective prediction rather than reweighting or repairing the failed Phase66B representation.

## Provenance

Inputs used identically in primary and replication:

- morphology table SHA256 `8a7c43053331523f15e9af23ee36dbc89945a281927f1037b53ff2ee98c1ce0d`
- Color-B feature table SHA256 `1f717d6e201344059d88e952b2bcd16872859d09190537b19c4a51bf66bc0ac5`
- Phase65 source manifest SHA256 `71023a2c395ad95848697e866373541deb1beb02dfbfaaabcd21140293775a56`
- text feature freeze SHA256 `7de8433f4cfb194e166e64611c68ec9a08aa37cfd0c4f65ca72e2dfcc960cfda`
- science executable SHA256 `698252876f7a6187ac8c80f1e95372e2afa3c8e3dc30f7e62170b3ad492a3290`

Primary artifact ZIP digest: `sha256:6776358299c66be196753b04eb16399c3fba401a3725560ebbfde4762fc81ed7`

Replication artifact ZIP digest: `sha256:22ca844852f2f8dcc4f056bf82eaaea7936ed579b537ec82bf087bdd5bff9ac9`
