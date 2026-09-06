# Issue #100 — source-order correction and predictive hierarchy rerun

Date frozen: 2026-09-06
Parent: Issue #98 / Issue #88
Trigger authority: `experiments/predictive-information/phase2c/ORDER_AUDIT_PROVENANCE.md`
Status: **FROZEN BEFORE CORRECTED PREDICTIVE OUTER SCORING**

## Correction only

The old parser artifacts remain untouched. Corrected reruns install the versioned `source_order_authority.py` adapter:

- raw ZL3b page-header first-occurrence rank defines document order;
- numeric `:pN` defines paragraph order inside each document;
- line/token order inside an item is unchanged;
- physical-leaf reset and five frozen leaf folds are unchanged.

The adapter must verify source document order and monotone numeric paragraph order before any predictive selection or score.

## C1 Phase 1 rerun

Reuse Issue #92 exactly:

- B0 frozen V2 support/probability;
- B1 restrict H=40 within the original H/tau/pi candidate grid;
- B2 full original H/tau/pi grid;
- B3 ENTRY_BODY versus LINE4 and original lambda grid;
- B4 reset versus continuous byte challenger and original k/alpha grids;
- same nested outer/inner physical-leaf folds;
- same literal-surface scoring population.

Do not force old B1/B2/B3 selections. B0 must reproduce exactly because item order does not enter V2 token probabilities. No grid extension is allowed.

## C2 Phase 2A rerun

Only after C1 is frozen, use corrected selected B1 as LOCAL and corrected selected B2 as ORDERED_LONG.

Matched controls use the same corrected B2 history support H, decay tau and selected mixture pi:

- order-free bag over the same H support;
- fixed-mixture matched bag;
- matched random-lag with the same H/tau weight multiset;
- LOCAL + bag with nested scalar rho;
- calibrated random-lag with nested scalar mixture.

If corrected B2 remains `H=ALL,tau=128,pi=.30`, this is algebraically the old Phase-2A family under corrected order. Otherwise no old `128/.30` value is forced.

## C3 Phase 2B rerun

Use corrected LOCAL as base and corrected ORDERED_LONG H/tau for order controls. Re-run the same disjoint pools:

- LINE;
- CURR_PARA;
- PREV_PARAS;
- LEAF_PREFIX.

Bag and random/ordered scalar mixtures retain the old `0..0.30 step .01` nested selection. No boundary-specific H/tau search.

## Comparison rule

Old results are shown only after corrected selection is frozen. They cannot alter corrected hyperparameters or classifications.

Status labels:

- `ROBUST TO ORDER CORRECTION`;
- `QUALITATIVELY CHANGED`;
- `NO LONGER SUPPORTED`;
- `NOT COMPARABLE`.

## Firewall

No S1/S2/H62/R1, Issue #84 target, semantic/image context, Currier/section/scribe metadata, future token, latent state or post-result candidate expansion is permitted.