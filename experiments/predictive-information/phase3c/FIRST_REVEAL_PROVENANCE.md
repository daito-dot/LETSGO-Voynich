# Issue #109 Phase 3C — matched-Herbal first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL**
Parent: Issue #88

## Pre-reveal authorities

Before any Phase-3C predictive score, the following were frozen and merged/committed:

- Issue #109 design;
- `PURE_HERBAL_GATE0_PLAN.md`;
- `PURE_HERBAL_GATE0_PROVENANCE.md`;
- `TRANSPORT_PLAN.md`;
- corrected source-order authority;
- Phase-3A target-support transport family.

The scorer recomputed the pure-Herbal Gate and required its JSON SHA-256 to equal:

`ec8c1dcb14f4450fe6e9f42d80ad00a60872719553c5ee46c153287723f705d8`

before prediction.

## Authoritative reveal

- workflow run: `34022384737`
- scientific head: `b02b1c9f818f1810275aa18de28fd2c9a8e0e6be`
- conclusion: `success`
- artifact: `issue109-phase3c-herbal-transport`
- artifact ID: `9985940850`
- artifact digest: `sha256:72f411141d91d9528bdb613177f41106fef95bfc6792bdbebca3505f8a2683ad`
- result JSON SHA-256: `13579242a30e9001a8913db6c4328a952118268b4fb5ad7a1f919f88c0ecd234`

All five target folds were scored in each direction and all authority/firewall assertions passed.

## Frozen matched-Herbal source parameters

Selected by source-Herbal-only five-fold held-out likelihood:

- A_HERBAL: `pi_LOCAL=.10`, `alpha_ALL_PREV=.04`
- B_HERBAL: `pi_LOCAL=.11`, `alpha_ALL_PREV=.08`

All-domain Phase-3A reference was A `.14/.09`, B `.16/.19`. Those values were diagnostic references only and did not enter Herbal selection.

## Formal classifications

- LOCAL40: **BIDIRECTIONAL TRANSPORT**
- PREV_PARAS: **A->B ONLY**
- CORE: **BIDIRECTIONAL TRANSPORT**

Matched-domain interpretation frozen before reveal:

> **CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL**

## Target-oracle diagnostic

Within pure Herbal:

- A target-oracle PREV increment: mean `+0.0022579 bit/token`, positive `3/5` — does not pass the frozen reproducibility rule;
- B target-oracle PREV increment: mean `+0.0047485`, positive `4/5` — passes.

Thus the residual paragraph-scale effect is weaker overall after domain matching and remains more stable in Currier B.

## Secondary full-support arm

The strict source-trained V2/vocabulary/index arm is finite in all folds in both directions (`VALID`) but retains large support mismatch. Quantitative OOV/code-length penalties are reported in `REPORT.md` and remain diagnostic only.

## Firewall

The result asserts:

- prediction-only literal-surface scoring;
- pure-Herbal population fixed before prediction;
- whole-leaf filtering only;
- no within-leaf token filtering;
- target-side emission/edit support in the primary arm;
- no opposite-target token used in source parameter selection;
- no H/tau/window, edit-relation, history-pool, fold or domain reselection;
- no S1/S2/H62/R1 or Issue #84 target;
- no hand conditioning;
- no semantics/imagery/plaintext;
- no latent state;
- no future target token.

## Authority rule

Future references to Phase 3C should cite run `34022384737`, artifact `9985940850`, and result JSON SHA-256 `13579242a30e9001a8913db6c4328a952118268b4fb5ad7a1f919f88c0ecd234`.