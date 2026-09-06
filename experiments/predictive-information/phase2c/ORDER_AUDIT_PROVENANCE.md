# Issue #98 Phase 2C Gate 0 — ordering-authority audit provenance

Date: 2026-09-06
Status: **AUTHORITATIVE GATE 0 FAIL**

## Authority

- GitHub Actions run: `34019697161`
- head: `cadf39f1af8e75cc3b54bde1ce27711923db0a1e`
- workflow conclusion: `success` (the scientific gate outcome is encoded in the result, not CI failure)
- artifact: `issue98-phase2c-order-audit`
- artifact ID: `9985065213`
- artifact digest: `sha256:4ad2d8c8fbc64e5283cd88356c70871c1601334140cbb6e6eccdf2ce2d66e053`
- `phase2c_order_audit.json` SHA-256: `210400a81409270b33df6749285dd5d4d7c246de8cc5379c19ab51a3b7123df6`

Firewall:

- predictive scores computed: false;
- surface target metrics scored: false;
- semantic/image context used: false.

## Gate result

> `STOP_AND_CORRECT_ORDER_THEN_RERUN_PREDICTIVE_PHASES`

The existing shared parse/order path is not a valid causal-order authority for all documents.

### Paragraph-order mismatch

- parsed documents with paragraph items: `206`;
- documents where lexical `item_id` order differs from numeric paragraph order: **20**;
- max parsed paragraphs on one document: **18** (`f103r`);
- total paragraph items: `736`;
- causal-history-affected items: **249**;
- parser-accepted tokens whose preceding paragraph history can differ: **5,541 / 25,071 = 22.1012%**;
- visible tokens in affected items: `7,295 / 32,570`.

Affected documents are:

`f67r2`, `f103r`, `f103v`, `f104r`, `f104v`, `f105r`, `f105v`, `f106r`, `f106v`, `f107r`, `f107v`, `f108r`, `f112r`, `f112v`, `f113r`, `f113v`, `f114r`, `f114v`, `f115r`, `f115v`.

The mechanism is exactly the anticipated lexical-sort failure: paragraph ids such as `p10` sort before `p2` when strings are used as the causal order key.

### Page-side/document-order mismatch

The raw ZL3b source page-header order also differs from lexical document order on **6 numeric physical leaves**:

- leaf 68;
- leaf 86;
- leaf 89;
- leaf 90;
- leaf 95;
- leaf 102.

Examples include source order `f68r1,f68r2,f68v3,f68v2` versus lexical `f68r1,f68r2,f68v2,f68v3`, and nontrivial foldout ordering on leaf 86.

This matters because previous Phase-1/2A/2B causal histories reset only at the numeric physical-leaf boundary and therefore use document order within those leaves.

### Fold membership

The five frozen folds are leaf-based. Correcting within-leaf causal order does **not** change fold membership.

## Scientific consequence

Do not run the planned Phase-2C PREV1/OLDER or same-side/cross-side predictive decomposition on the old ordering.

Before any further attribution:

1. create an explicit source-order authority from raw ZL3b page headers and numeric paragraph indices;
2. leave V2/token-internal authorities unchanged unless a test explicitly depends on sequential item order;
3. rerun the prediction-only Phase-1 local/long/state ladder under corrected causal order, using the same candidate families and selection firewalls;
4. rerun Phase 2A source attribution and Phase 2B boundary localization under corrected order;
5. compare old versus corrected conclusions and mark any superseded claims clearly;
6. only if the corrected hierarchy still supports a previous-paragraph signal proceed to the Phase-2C decomposition.

No old S1/S2/H62/R1 or semantic result may guide the correction.