# Phase 56 — latent multiscale state map

The execution plan was frozen in `PLAN.md` before implementation.

## Phase 56A — canonical substrate: COMPLETE

`phase56_build_state_matrix.py` parses the actual ZL3b page-header metadata and preserves physical leaf and page-side separately.

Audited substrate:

- 226 page headers in source
- 4,087 included P-coded prose lines
- **206 page-sides**
- **99 physical leaves**
- **736 paragraphs**
- recto 104 / verso 102

The 197 page-sides overlapping the earlier Phase55 folio-feature map were regression-checked on TTR, token-unit length, edit-1 family coverage, previous-10 locality, line-position MI, and first/final entropy. Maximum absolute difference was **0.0** for every checked feature.

## Phase 56B — drift versus regimes: COMPLETE AS DEVELOPMENT DIAGNOSTIC

After exact matching on section + Currier + hand, physical locality remains real: same-leaf / adjacent-leaf fingerprints are closer than distant leaves. However, neither one globally smooth trajectory nor a small set of sharp changepoints adequately describes the full pattern. The best current description is broad state/block differences plus local physical similarity.

See `phase56b_results.json` for the full model comparison.

## Phase 56C — latent dimensionality and cross-scale state: COMPLETE AS DEVELOPMENT DIAGNOSTIC

### Critical sample-size correction

The first page-side PCA used page fingerprints computed from each page's full available text. Its PC1 correlated **r=-0.886 with page token count**. The apparent dominant `section` axis was therefore substantially contaminated by sample-size-sensitive features such as TTR and inventory size.

That interpretation is withdrawn.

Phase56C rebuilt page fingerprints from **30 random contiguous 40-token windows per page-side**, averaged within page-side. Paragraph fingerprints were independently built from **20 random contiguous 20-token windows per paragraph**.

### Matched page-side latent structure

197 page-sides, 11 matched features.

PCA variance:

- PC1 31.9%
- PC2 21.4%
- PC3 10.4%
- first 3 cumulative **63.7%**
- first 5 cumulative **78.7%**
- first 7 cumulative **90.0%**

The dominant matched PC1 is no longer a section axis. Its largest loadings are:

- local previous-10 near-family continuity +0.450
- edit-1 family coverage +0.434
- TTR -0.371
- unit inventory -0.342
- token-length dispersion -0.333

This is best described provisionally as a **near-family activation / local-continuity axis**.

PC2 emphasizes mean token length, first/final entropy, and `k/t` mass. PC3 emphasizes `k/t` mass and the balance within `{k,t}`.

Metadata effects are distributed across several dimensions rather than dominated by one axis.

### Cross-scale replication at paragraph level

635 paragraphs with >=20 body tokens were analyzed using matched 20-token windows.

The first paragraph PC is again dominated by local near-family continuity and edit-1 family coverage; the second is again dominated by mean length, final/initial entropy and `k/t` mass.

The top two page-side and paragraph subspaces have principal angles about **5.8° and 22.2°**, indicating substantial recurrence of the same low-order structural directions across scales.

In the paragraph 5D latent space:

- same page-side mean distance: **3.244**
- same section+hand but different page: **3.567**
- broadly unrelated: **3.910**

Thus a page-local state exists below broad section/hand labels.

### Physical locality decomposed by latent axis

After exact section+Currier+hand matching, mean absolute difference on matched PC1 rises from about **1.54** for same/adjacent leaves to **2.46** at leaf gap >=11. The corresponding increase is smaller on PCs 2-5.

Therefore much of the physical-locality effect is concentrated in the near-family/local-continuity dimension: nearby physical units tend to activate more similar token-family topology.

### Linear versus nonlinear compression

Five-fold grouped held-out reconstruction by physical leaf:

| dimensions | PCA MSE | RBF kernel-PCA MSE |
|---:|---:|---:|
| 2 | 0.492 | 0.592 |
| 3 | 0.390 | 0.533 |
| 4 | 0.325 | 0.441 |
| 5 | 0.250 | 0.373 |
| 6 | 0.163 | 0.321 |

Kernel-gamma sensitivity can approach the linear result but does not beat it. There is currently **no evidence that nonlinear manifold compression improves on the linear latent basis** for these audited matched page features.

## Phase 56C decision

**H56-1: QUALIFIED SUPPORT / REFINED.**

The manuscript's matched structural variation is moderately low-dimensional, but not a one- or two-axis system. Roughly 3 dimensions capture ~64% and 5 capture ~79% of page-side variance, with similar leading directions recurring at paragraph scale.

The important correction is that raw page-level sample size can manufacture a seemingly dominant section axis. Future latent/residual analyses must use matched token counts or explicitly model estimator/sample-size effects.

Current structural picture:

`broad document/section constraints`

`+ page-local token-family activation state`

`+ morphology / edge-entropy / {k,t} dimensions`

`+ paragraph and line-position dynamics`

rather than one global section axis or one smooth physical drift.

## Phase 56D frontier — transitions and residualization

Before semantic/cipher testing:

1. project paragraph/line transitions into the matched latent basis;
2. test whether paragraph entry follows a reproducible multivariate trajectory rather than only the original near-family metric;
3. test transfer of that trajectory across positive-reset sections;
4. predict structural state from broad metadata + local page state + paragraph-relative line position;
5. retain grouped held-out residuals as the candidate future information-bearing target.

Detailed numeric results are in `phase56c_results.json`.
