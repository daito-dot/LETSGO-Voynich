# Phase 56 — latent multiscale state map

The execution plan was frozen in `PLAN.md` before implementation.

## Phase 56A — canonical substrate: COMPLETE

`phase56_build_state_matrix.py` now parses the actual ZL3b page-header metadata and preserves physical leaf and page-side separately.

Audited substrate:

- 226 page headers in source
- 4,087 included P-coded prose lines
- **206 page-sides**
- **99 physical leaves**
- **736 paragraphs**
- recto 104 / verso 102

Section counts among included page-sides:

- H 128
- S 25
- B 19
- P 16
- C 7
- T 6
- A 5

Currier is absent from the ZL3b source header on 10 included page-sides; this is not a parser failure. `f115r` has hand `$H=@` in the source and is retained literally.

### Regression audit

The 197 page-sides overlapping the earlier Phase55 folio-feature map were compared on:

- TTR
- mean/sd token-unit length
- edit-1 family coverage
- previous-10 locality
- line-position MI
- first/final entropy

Maximum absolute difference was **0.0** on every checked feature. Phase56A-v1 is therefore frozen as the canonical substrate for 56B-D.

### Parser correction during audit

The first GitHub implementation incorrectly looked for `$I/$L/$H` on comment records. Actual ZL3b stores them on page-header records such as `<f1r> <! ...>`. This was caught before any Phase56 model result was accepted and the builder was replaced.

## Phase 56B — drift versus regimes: IN PROGRESS

Initial predictive comparison used 197 sufficiently populated page-sides, an 11-feature standardized structural fingerprint, and five contiguous physical-leaf held-out blocks.

Mean held-out standardized MSE:

- section-mean baseline: **0.990**
- distance-weighted smooth physical neighbor: **0.926**
- contiguous 2-regime model: 0.964
- contiguous 3-regime model: 1.052
- contiguous 4-regime model: 0.962
- contiguous 6-regime model: 1.137
- contiguous 8-regime model: 0.995

The smooth physical predictor improves mean error by about **6.4%** relative to section means. Simple discrete physical bins do not beat it. However, one central held-out block favors the section baseline, so this is **provisional support for smooth local drift**, not closure of H56-2.

Next inside 56B: explicit changepoint and mixed regime-plus-drift comparisons, then matched-stratum sensitivity before moving to latent dimensionality.
