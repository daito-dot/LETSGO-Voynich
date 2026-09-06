# Issue #100 C3 — corrected-source-order Phase 2B provenance

Date: 2026-09-06
Status: **AUTHORITATIVE CORRECTED PHASE-2B RESULT**

## Authority

- GitHub Actions run: `34020290736`
- scientific head: `4bbd0a994dcc7307038b1b16c7726cffca5f3f65`
- workflow conclusion: `success`
- artifact: `issue100-c3-phase2b-source-order`
- artifact ID: `9985268839`
- artifact digest: `sha256:0bb01973eb1d9a278b4160d16cbd9c33f332943c3ec0f0c4bac5737a0dd19920`
- `issue100_c3_phase2b.json` SHA-256: `d0ffb426ca268cea3c6c4090aaaac48f260dd4832e8806fbf20419f6f638c014`

All corrected-order regressions passed:

- C1 LOCAL40 reference;
- C1 ORDERED128 standalone reference;
- C2 leaf-prefix-bag selection and code length;
- source document order and numeric paragraph order.

No boundary-specific tau/window search, old-result selection, future token, surface-target statistic, semantic context or latent state was used.

## Corrected result

Classification remains:

> **MULTISCALE**

Mean held-out code lengths:

| model | corrected bits/token | legacy bits/token |
|---|---:|---:|
| LOCAL40 | 9.5943670127 | 9.5961811202 |
| LOCAL + LINE_BAG | 9.5943670127 | 9.5961811202 |
| LOCAL + CURR_PARA_BAG | 9.5938517037 | 9.5954732856 |
| LOCAL + PREV_PARAS_BAG | **9.5443610736** | 9.5439510434 |
| LOCAL + LEAF_PREFIX_BAG | 9.5523929929 | 9.5518752000 |
| LOCAL + CURR_PARA_ORDERED128 | 9.5939597438 | 9.5955931630 |
| LOCAL + CURR_PARA_RANDOM_LAG | 9.5938851838 | 9.5955054726 |
| LOCAL + PREV_PARAS_ORDERED128 | 9.5458221825 | 9.5488434809 |
| LOCAL + PREV_PARAS_RANDOM_LAG | 9.5501300850 | 9.5494508993 |
| ORDERED128 standalone | 9.5461691796 | 9.5492540389 |

## Primary corrected contrasts

### Same-line inventory beyond LOCAL40

`G_line_inventory = 0`, positive 0/5, **FAIL**.

All folds still select zero additional same-line bag weight.

### Current-paragraph inventory beyond LOCAL40

`G_within_para_inventory`:

- mean `+0.0005153090 bit/token`;
- folds `+0.0002953, +0.0006548, +0.0012066, +0.0005877, -0.0001679`;
- positive 4/5;
- **PASS**, but effect-small.

Legacy mean was `+0.0007078346`.

### Inventory gained by crossing the paragraph boundary

`G_cross_para_inventory`:

- mean **`+0.0414587108 bit/token`**;
- folds `+0.0323311, +0.0364938, +0.0576772, +0.0559376, +0.0248540`;
- positive 5/5;
- **PASS**.

Legacy mean was `+0.0435980855`.

The dominant inventory result therefore survives the ordering correction with only a modest reduction.

### Current-paragraph lag/source association

`G_order_within_para`:

- mean `-0.0000745600 bit/token`;
- positive 0/5;
- **FAIL**.

The corrected result again finds no value in exact current-paragraph lag assignment beyond the matched control.

### Previous-paragraph lag/source association

`G_order_cross_para`:

- mean **`+0.0043079025 bit/token`**;
- folds `+0.0035594, +0.0021534, +0.0055965, +0.0036425, +0.0065876`;
- positive **5/5**;
- **PASS**.

Legacy mean was only `+0.0006074185`, positive 4/5. Correct source order therefore strengthens the evidence for a real but still secondary cross-paragraph order/lag component.

## Corrected selected weights

Previous-paragraph bag alpha remains high and stable:

- fold0 `.23`
- fold1 `.24`
- fold2 `.22`
- fold3 `.22`
- fold4 `.24`

Current-paragraph bag alpha remains only `.01-.02`, while same-line bag remains `.00`.

Previous-paragraph ordered/random controls select approximately `.20-.24`, so the cross-paragraph result is not driven by a vanishingly small control mixture.

## Robustness judgement

The old Phase-2B scientific conclusion is:

> **ROBUST TO ORDER CORRECTION, WITH STRONGER CROSS-PARAGRAPH ORDER EVIDENCE.**

The main hierarchy is unchanged:

1. no extra same-line inventory beyond LOCAL40;
2. tiny current-paragraph inventory effect;
3. dominant previous-paragraph inventory effect;
4. no useful exact current-paragraph lag assignment;
5. a smaller but now clearly reproducible previous-paragraph lag/source association.

`LOCAL + PREV_PARAS_BAG = 9.5443611 bits/token` remains better than the full leaf-prefix bag (`9.5523930`) and slightly better than the standalone ORDERED128 reference (`9.5461692`) under the tested conditional family.

The conclusion that a uniform token-distance memory is an inadequate description is therefore not an artifact of the lexical-order bug.

## Next program consequence

Issue #98 Phase 2C may resume using this corrected authority. It should split the corrected `PREV_PARAS` source into:

- immediately previous paragraph versus older paragraphs;
- same page-side versus cross-side causal paragraphs within the numeric physical leaf.

Because the corrected cross-paragraph order residual is larger than before, Phase 2C should retain both inventory and matched order/lag diagnostics rather than treating order as negligible.

## Claim boundary

This remains predictive source attribution only. It does not establish paragraph semantics, topic, plaintext, language, syntax, a literal historical memory process, cipher identity, author, or latent state.