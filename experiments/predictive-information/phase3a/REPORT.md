# Issue #104 Phase 3A — Currier A/B mechanism transport

Date: 2026-09-06
Status: **AUTHORITATIVE RESULT**
Parent: Issue #88

## Question

Do the corrected local-recency and previous-paragraph-inventory mechanisms transport between the independently defined Currier A/B strata, once vocabulary/emission support is separated from the scalar cross-token mechanism parameters?

The primary arm therefore fits V2 and the edit-1 support index on the **target** stratum and transfers only the source stratum's `pi_LOCAL` and `alpha_ALL_PREV`.

## Formal result

| Component | Frozen classification |
|---|---|
| LOCAL40 | **BIDIRECTIONAL TRANSPORT** |
| PREV_PARAS exact scalar transfer | **A->B ONLY** |
| combined CORE | **BIDIRECTIONAL TRANSPORT** |

This is not evidence that Currier A/B are languages, meanings or semantic states. It is a structural prediction/transport result under those pre-existing manuscript labels.

## Source-stratum parameters

Selected entirely within each source stratum by five-fold held-out literal-surface likelihood:

| Source stratum | `pi_LOCAL` | `alpha_ALL_PREV` |
|---|---:|---:|
| A | 0.14 | 0.09 |
| B | 0.16 | 0.19 |

The local strength is similar across A/B. The previous-paragraph inventory strength differs by about a factor of two.

## A -> B mechanism-only transport

Using A parameters on B target-side emission/support:

- LOCAL40 gain: **`+0.06031 bit/token`**, positive 5/5;
- PREV_PARAS incremental gain: **`+0.02313`**, positive 5/5;
- CORE gain over B-side V2: **`+0.08343`**, positive 5/5.

Foldwise CORE gains:

`0.06254, 0.07794, 0.11585, 0.08965, 0.07120 bit/token`.

A's local parameter is essentially target-optimal for B:

- mean local oracle penalty: only `+0.00030 bit/token`.

The A CORE parameters are also close to B target-oracle performance on average:

- mean CORE oracle penalty: `+0.00526 bit/token`.

B target-oracle parameters select:

- `pi_LOCAL=.15-.16`;
- `alpha_ALL_PREV=.17-.20`.

Thus A's weaker paragraph-inventory weight (`.09`) still improves B in every fold, although B prefers a materially stronger weight.

## B -> A mechanism-only transport

Using B parameters on A target-side emission/support:

- LOCAL40 gain: **`+0.05718 bit/token`**, positive 5/5;
- PREV_PARAS incremental gain: `-0.00028`, positive only 2/5 — FAIL;
- CORE gain over A-side V2: **`+0.05690`**, positive 5/5.

Foldwise PREV_PARAS increments:

`-0.01689, +0.02507, -0.01092, -0.00038, +0.00173 bit/token`.

The local parameter again transfers almost without cost:

- mean local oracle penalty: `-0.00071 bit/token`.

The CORE source-parameter penalty is larger:

- mean CORE oracle penalty: `+0.00933 bit/token`, positive 4/5.

A target-oracle parameters select:

- `pi_LOCAL=.11-.15`;
- `alpha_ALL_PREV=.07-.10`.

The A oracle PREV_PARAS component itself is positive in **5/5 folds**, with mean incremental gain `+0.00976 bit/token`.

Therefore the B->A PREV_PARAS transfer failure does **not** mean the paragraph-inventory family is absent in A. A independently selects and benefits from the same family, but at a substantially weaker mixture strength. Applying B's `alpha=.19` to A overweights that component.

## Structural synthesis

The result separates two levels that were previously conflated.

### 1. LOCAL40 architecture and strength are strongly transportable

A and B independently select similar local strengths (`.14` vs `.16`), and transferred LOCAL40 improves every held-out target fold in both directions with negligible target-oracle penalty.

This is currently the strongest evidence that the short edit-1 recency mechanism is a manuscript-wide production regularity rather than a Currier-specific regime effect.

### 2. Previous-paragraph inventory architecture appears shared, but its strength is regime-dependent

Both A and B target-oracle fits use nonzero PREV_PARAS weights and gain prediction in all five target folds:

- B oracle PREV increment: mean `+0.02809 bit/token`, 5/5;
- A oracle PREV increment: mean `+0.00976`, 5/5.

But the frozen exact-parameter transport test is asymmetric:

- A's weaker `alpha=.09` transports to B;
- B's stronger `alpha=.19` does not transport back to A.

The safest interpretation is therefore:

> **the same slower paragraph-inventory mechanism is supported in both Currier strata, but its optimal strength is observably state-dependent.**

This rejects a simple universal-single-alpha account while avoiding an unsupported claim that Currier A and B require different mechanism families.

### 3. CORE still transports bidirectionally because the local component is robust

The combined CORE improves all target folds in both directions. In B->A, however, this should not be mistaken for full transport of the paragraph-scale parameter: the LOCAL40 component carries the positive CORE result while the transferred PREV increment itself fails.

## Vocabulary/emission support transport

The secondary strict source-support arm is technically `VALID` in all folds, but performs far worse than the primary mechanism-only arm.

A-trained full support -> B:

- mean exact-token OOV: **28.2%**;
- mean source-support CORE: `11.7654 bits/token`;
- mean target-support mechanism-only CORE: `9.3850`;
- mean penalty: **`+2.3804 bits/token`**.

B-trained full support -> A:

- mean exact-token OOV: **14.8%**;
- mean source-support CORE: `10.6880 bits/token`;
- mean target-support mechanism-only CORE: `9.3650`;
- mean penalty: **`+1.3230 bits/token`**.

Thus vocabulary/emission distributions transport poorly even where the short cross-token mechanism transfers well. This is exactly why support and mechanism transport must remain separate.

No semantic interpretation follows: Currier-associated vocabulary/support differentiation is compatible with multiple historical explanations.

## Consequence for the program

A rich latent-state model is still not licensed as the next step.

The current evidence instead motivates a narrower observable-state question:

> Which independently defined manuscript metadata explains the approximately twofold PREV_PARAS strength difference between Currier A and B?

Before introducing hidden states, the next transport/source-attribution phase should test independently authoritative section/domain and hand/scribe labels, with score-free metadata/support audits first.

Priority should be to determine whether Currier dependence is explained by section/domain composition, hand/scribe, or remains after those observable strata are controlled.

## Provenance

Authoritative run: `34021428084`.

- artifact ID: `9985643333`
- artifact digest: `sha256:538694b5db9d7c41d5fef4e53f05684429236494fbf06d819f031f97f5c94ed8`
- result JSON SHA-256: `6cd0acbf86a39952493f693e58fd2c9f623871d577721ca4b29e052992c51b02`

See `FIRST_REVEAL_PROVENANCE.md`.

## Claim boundary

This result establishes neither plaintext, language identity, syntax, topic, meaning, cipher identity, authorship nor semantic latent state. Currier A/B are used only as independently pre-existing manuscript strata.