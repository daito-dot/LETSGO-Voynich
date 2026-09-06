# Issue #104 Phase 3A — Currier A/B transport first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL**
Parent: Issue #88

## Pre-reveal authorities

The following were fixed before any Phase-3A predictive transport score:

- Issue #104 transport design;
- `GATE0_PLAN.md`;
- `AMENDMENT_A.md`;
- `GATE0_PROVENANCE.md`;
- `TRANSPORT_PLAN.md`;
- corrected source-order authority `source_order_authority.py`.

The scorer re-computed Gate 0 and required its JSON SHA-256 to equal the merged authority before prediction.

Expected and observed Gate-0 JSON SHA-256:

`e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`

## Authoritative reveal

- workflow run: `34021428084`
- scientific head: `fec2224263f0c93d83ffa2175d68bb2619a90879`
- conclusion: `success`
- artifact: `issue104-phase3a-currier-transport`
- artifact ID: `9985643333`
- artifact digest: `sha256:538694b5db9d7c41d5fef4e53f05684429236494fbf06d819f031f97f5c94ed8`
- result JSON SHA-256: `6cd0acbf86a39952493f693e58fd2c9f623871d577721ca4b29e052992c51b02`

All five target folds were scored in each direction. The authority, source order and prediction-only firewall checks passed.

## Frozen source-stratum parameters

Selected using source-stratum-only held-out likelihood:

- Currier A: `pi_LOCAL=.14`, `alpha_ALL_PREV=.09`
- Currier B: `pi_LOCAL=.16`, `alpha_ALL_PREV=.19`

No opposite-stratum target token entered these selections.

## Formal classifications

- LOCAL40: **BIDIRECTIONAL TRANSPORT**
- PREV_PARAS exact scalar-parameter transfer: **A->B ONLY**
- combined CORE: **BIDIRECTIONAL TRANSPORT**

These are the classifications frozen in Issue #104. Continuous oracle penalties and target-oracle diagnostics are reported in `REPORT.md` and do not redefine the decision rule after reveal.

## Secondary full-support arm

The strict source-trained V2/vocabulary/index diagnostic produced finite scores in all folds in both directions, so its technical classification is `VALID` rather than support-inconclusive.

However it suffers large exact-token OOV and code-length penalties relative to the primary target-support arm. This is evidence of vocabulary/emission support mismatch and is intentionally kept separate from mechanism transport.

## Firewall

The result asserts:

- prediction-only scoring;
- target-side emission/edit support in the primary arm;
- no target token used to select source parameters;
- no H/tau/window reselection;
- no edit-relation or history-pool change;
- no S1/S2/H62/R1 or Issue #84 target metric;
- no hand/section/scribe conditioning;
- no semantic/image/plaintext context;
- no latent state;
- no future target token.

## Authority rule

Future quantitative references to Phase 3A should cite run `34021428084`, artifact `9985643333`, and result JSON SHA-256 `6cd0acbf86a39952493f693e58fd2c9f623871d577721ca4b29e052992c51b02`.