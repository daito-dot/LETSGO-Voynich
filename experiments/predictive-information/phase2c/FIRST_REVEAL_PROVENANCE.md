# Issue #98 Phase 2C — first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE CORRECTED PHASE-2C RESULT**
Parent: Issue #88

## Frozen design authority

- `AMENDMENT_AFTER_ORDER_CORRECTION.md` was committed before the first Phase-2C predictive score.
- corrected causal-order authority: `experiments/predictive-information/source_order_authority.py`
- corrected upstream authorities: Issue #100 C1/C2/C3
- no H/tau/window search was reopened; order diagnostics use frozen `tau=128`.

## Reveal chronology

### First scientific computation

Workflow run `34020598328` at head `d72e30b9c8ff1c106721beb45ef735985cbadb44` completed the scientific Phase-2C computation and wrote `phase2c_results.json` before a post-computation CI assertion failed.

The failure was not scientific: the workflow used `assert all(x['regression'].values())`, while the intentionally correct field `fold_membership_changed` is `False`. Thus a correct negative invariant was treated as a failing truthiness check.

The first computed result already classified:

- temporal: `TEMPORAL MULTISCALE`;
- page/panel: `CROSS-SIDE TRANSPORT SURVIVES`.

No model, grid, pool, randomization, selector, seed, source-order rule or decision threshold was changed after this reveal.

### CI-only repair and authoritative transport

Commit `5c9c1a6ef2208ce104c1a44ede35e59e322da3df` changes only the workflow assertion to check the three positive regression invariants explicitly and require `fold_membership_changed is False`.

Authoritative successful run:

- run: `34020713068`
- scientific code: unchanged from the first computation
- head: `5c9c1a6ef2208ce104c1a44ede35e59e322da3df`
- conclusion: `success`
- artifact: `issue98-phase2c-decomposition`
- artifact ID: `9985408973`
- artifact digest: `sha256:85e35772b1e9f9ab2eeea606ada7edb0dca95cfcf1b7893966d09620a2870026`
- result JSON SHA-256: `16cad5206cafc5ae1a856427c705afddfc591e2e706962de8bae326d32c1f149`

The two runs agree in classification, selections and reported effects to numerical precision. Tiny last-bit floating differences in a few randomized averages prevent byte-identical JSON; they do not affect any fold sign, selected hyperparameter or classification.

## Regression and firewall

Successful run verifies:

- corrected LOCAL40 mean exactly reproduced;
- corrected ALL_PREV nested alpha reproduced in all five folds;
- corrected ALL_PREV mean exactly reproduced;
- fold membership unchanged;
- numeric paragraph order valid;
- raw source document/page-panel order valid;
- no future test token used;
- no S1/S2/H62/R1 or Issue #84 target used;
- no Currier/section/scribe metadata used;
- no semantic/image context used;
- no latent state fitted;
- no post-reveal pool/grid/randomization extension.

## Authority rule

For future quantitative work, cite the successful run/artifact above. The earlier failed workflow remains part of the audit trail because it was the first scientific computation, but it is not the transport authority.