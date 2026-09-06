# Phase 2B authoritative first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE PHASE-2B RESULT**
Parent: Issue #88
Implementation issue: #96
PR: #97

## Authority

- GitHub Actions run: `34019400119`
- scientific head: `9063d5a10ce252d738f939db2c499fef25816192`
- workflow conclusion: `success`
- artifact: `issue96-phase2b-boundary-localization`
- artifact ID: `9984976498`
- artifact digest: `sha256:1b972d4845be475c80a8c41ebdce9f5c091421740ab31372a09b031f15f90a50`
- `phase2b_results.json` SHA-256: `e940e9404bed2bf284c49f02fc4e96ad18796301ea3014ff9fe23ae632254323`

All reference regressions passed in all five folds:

- Phase-1 LOCAL40;
- Phase-1 ORDERED128 standalone;
- Phase-2A A5 LEAF_PREFIX_BAG nested selection;
- Phase-2A A5 LEAF_PREFIX_BAG held-out code length.

Firewall fields are clean:

- no future test token;
- no S1/S2/H62/R1 target scoring;
- no Issue #84 target;
- no Currier/section/scribe metadata;
- no semantic/image context;
- no latent state;
- no tau/window reselection.

## Classification

> **MULTISCALE**

Formal decision inputs:

- WITHIN inventory: PASS;
- WITHIN order: FAIL;
- CROSS inventory: PASS;
- CROSS order: PASS;
- WITHIN: true;
- CROSS: true.

The formal class is intentionally based only on the frozen sign/stability rule. Effect sizes are required for scientific interpretation because the within- and cross-paragraph effects are extremely unequal.

## Mean held-out code length

| model | bits/token |
|---|---:|
| LOCAL40 | 9.5961811202 |
| LOCAL + LINE_BAG | 9.5961811202 |
| LOCAL + CURR_PARA_BAG | 9.5954732856 |
| LOCAL + PREV_PARAS_BAG | **9.5439510434** |
| LOCAL + LEAF_PREFIX_BAG | 9.5518752000 |
| LOCAL + CURR_PARA_ORDERED128 | 9.5955931630 |
| LOCAL + CURR_PARA_RANDOM_LAG | 9.5955054726 |
| LOCAL + PREV_PARAS_ORDERED128 | 9.5488434809 |
| LOCAL + PREV_PARAS_RANDOM_LAG | 9.5494508993 |
| ORDERED128 standalone | 9.5492540389 |

## Primary contrasts

### Same-line inventory beyond LOCAL40

`G_line_inventory = 0.0000000 bit/token`, positive 0/5, FAIL.

All five nested selectors chose `alpha=0.00`.

### Current-paragraph inventory beyond LOCAL40

`G_within_para_inventory = +0.0007078346 bit/token`, positive 4/5, PASS.

Fold values:

`+0.0003326, +0.0006928, +0.0023338, +0.0005944, -0.0004143`.

Nested alphas: `.01,.01,.02,.02,.02`.

This is formally reproducible but very small and reverses in one fold.

### Inventory gained by crossing the paragraph boundary

`G_cross_para_inventory = +0.0435980855 bit/token`, positive 5/5, PASS.

Fold values:

`+0.0357244, +0.0381268, +0.0599139, +0.0555375, +0.0286877`.

This is the dominant boundary-localized effect.

The previous-paragraph-only bag selects large nested weights `.24,.25,.23,.23,.24` and reaches `9.5439510 bits/token`, better than both the full LEAF_PREFIX_BAG and the standalone ORDERED128 reference under the tested conditional model.

### Current-paragraph order/lag association

`G_order_within_para = -0.0000876905 bit/token`, positive 0/5, FAIL.

All five folds are slightly negative. Actual current-paragraph lag/source association does not beat its matched random-lag control.

### Previous-paragraph order/lag association

`G_order_cross_para = +0.0006074185 bit/token`, positive 4/5, PASS.

Fold values:

`+0.0009400, +0.0008659, +0.0016661, +0.0015192, -0.0019541`.

This is formally reproducible but tiny and reverses in one fold.

## Scientific interpretation boundary

The Phase-2B result rejects a simple reading in which one uniform token-distance memory horizon explains the main long-range gain.

The dominant additional predictive information after LOCAL40 is associated with **token-family inventory in earlier paragraphs on the same physical leaf**, not with additional same-line/current-paragraph inventory and not with precise current-paragraph lag order.

A much smaller source/lag-sensitive effect survives across previous paragraphs.

This does not establish that paragraph boundaries are semantic, that the state is topical, or that the writer historically used a paragraph-memory process. The previous-paragraph inventory could still reflect page/side production state, register, content, layout, scribe, section, or another slowly varying variable.

The next attribution layer should localize the previous-paragraph pool itself before rich latent-state modeling.