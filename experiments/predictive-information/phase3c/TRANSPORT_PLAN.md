# Issue #109 / Issue #88 Phase 3C — matched-Herbal transport contract

Date: 2026-09-06
Status: **FROZEN BEFORE PHASE-3C PREDICTIVE SCORING**
Entry authority: `PURE_HERBAL_GATE0_PROVENANCE.md`

## Question

Does the Currier A/B PREV_PARAS scalar-strength asymmetry found in all-domain Phase 3A persist after prospectively restricting the entire analysis to whole numeric physical leaves whose visible parsed-P population is pure Herbal (`I=H`) and pure Currier A or B?

## Frozen population

The exact eligible leaf sets are the merged Gate-0 authority with JSON SHA-256:

`ec8c1dcb14f4450fe6e9f42d80ad00a60872719553c5ee46c153287723f705d8`

- A_HERBAL: 46 leaves, 5,462 parser-accepted tokens;
- B_HERBAL: 15 leaves, 2,382 accepted tokens;
- original five physical-leaf folds retained;
- no token filtering inside an eligible leaf.

The scorer must recompute Gate 0 and refuse to run if this authority hash changes.

## Frozen mechanism family

Reuse the Phase-3A target-support mechanism exactly:

1. target-side V2 emission/support;
2. LOCAL40 edit-1 recency with fixed `H=40`, `tau=32`, scalar `pi` only;
3. order-free `PREV_PARAS` edit-1 inventory on top of LOCAL40, scalar `alpha` only.

`pi, alpha in {0.00,0.01,...,0.30}`. Exact ties choose the smaller value.

No H/tau/window, edit relation, paragraph pool, tokenization, domain, or fold search is licensed.

## Source parameter selection

For A_HERBAL and B_HERBAL separately:

- select one source `pi` by summed five-fold held-out likelihood within that source-Herbal stratum only;
- fix source pi, then select one source `alpha` by summed five-fold held-out likelihood;
- no opposite-stratum token enters source selection.

## Target oracle

For each target outer fold:

- select target-Herbal `pi` using only the other four target-Herbal folds;
- fix that pi, then select target-Herbal `alpha` using the same nested target-only inner folds;
- target outer fold never enters selection.

## Primary scores

For A_HERBAL -> B_HERBAL and B_HERBAL -> A_HERBAL, report:

- `G_local_transfer = bits(T_V2) - bits(T_LOCAL(source pi))`;
- `G_prev_transfer = bits(T_LOCAL(source pi)) - bits(T_CORE(source pi,source alpha))`;
- `G_core_transfer = bits(T_V2) - bits(T_CORE(source params))`;
- local and core penalties relative to target-Herbal oracle.

Directional pass: mean > 0 and positive in >=4/5 target folds.

Component classifications are exactly the Phase-3A labels:

- `BIDIRECTIONAL TRANSPORT`
- `A->B ONLY`
- `B->A ONLY`
- `NO BIDIRECTIONAL TRANSPORT`
- `SUPPORT / FOLD INVALID`.

## Matched-domain PREV interpretation

The all-domain Phase-3A PREV classification is frozen as `A->B ONLY`.

Interpret the Herbal PREV classification prospectively:

- `BIDIRECTIONAL TRANSPORT` -> **HERBAL RESTORES BIDIRECTIONAL PREV TRANSPORT**;
- exactly `A->B ONLY` or `B->A ONLY` -> **CURRIER PREV ASYMMETRY PERSISTS WITHIN HERBAL**;
- `NO BIDIRECTIONAL TRANSPORT` -> **HERBAL PREV NONTRANSPORT**;
- otherwise -> **SUPPORT INVALID**.

Report all source/oracle alpha values continuously. Do not create an after-reveal equality/tolerance threshold.

## Secondary strict source-support diagnostic

Repeat the Phase-3A full source-trained V2/vocabulary/edit-index diagnostic on pure Herbal only. Report finite validity, exact-token OOV and code-length penalty. This arm cannot override the mechanism-only classification.

## Frozen references

All-domain Phase 3A source parameters are diagnostic references only:

- A: `pi=.14`, `alpha=.09`;
- B: `pi=.16`, `alpha=.19`.

They do not enter Herbal parameter selection.

## Firewall

- prediction-only literal-surface code length;
- pure-Herbal population fixed before prediction;
- corrected source order;
- original five folds;
- no S1/S2/H62/R1 or Issue #84 target;
- no hand conditioning;
- no imagery/plaintext/semantics;
- no latent state;
- no future target token;
- no post-reveal domain/fold/H/tau/window/pool/grid expansion.