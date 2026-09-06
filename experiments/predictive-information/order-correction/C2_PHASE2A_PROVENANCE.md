# Issue #100 C2 — corrected-source-order Phase 2A provenance

Date: 2026-09-06
Status: **AUTHORITATIVE CORRECTED PHASE-2A RESULT**

## Authority

- GitHub Actions run: `34020178998`
- head: `184dd3b6fd6347d118bf2c394f374834aea8da47`
- workflow conclusion: `success`
- artifact: `issue100-c2-phase2a-source-order`
- artifact ID: `9985231931`
- artifact digest: `sha256:9a3ba7751d07e0e48800d17d215691ae95482387f29c25ba2f8e63e33d622ff9`
- `issue100_c2_phase2a.json` SHA-256: `46ac2a8cbf45cbba370d1e7526030b5a6ee821a722f111ac7fdd24f4918ae8b4`

The first C2 attempt failed before an outer result because the archived Phase-2A base scorer referenced its locally defined `mix_probs` helper through the imported Phase-1 namespace. The successful run uses the same compatibility alias as the original authoritative Phase-2A runner; no model mathematics, grid, source order or C1 reference changed.

## Corrected result

Classification remains:

> **MIXED PREFIX + ORDER CONTRIBUTIONS**

Mean held-out code lengths:

| model | corrected bits/token | legacy bits/token |
|---|---:|---:|
| A0 LOCAL40 | 9.5943670127 | 9.5961811202 |
| A1 PREFIX_BAG_CV | 9.5601001202 | 9.5590296433 |
| A2 ORDERED128 | 9.5461691796 | 9.5492540389 |
| A5 LOCAL_PLUS_PREFIX | 9.5523929929 | 9.5518752000 |
| A6 RANDOM_LAG_CV | 9.5710183902 | 9.5690181087 |

Corrected A5 nested rho values:

`.20, .21, .19, .19, .21`.

Corrected A5 outer code lengths:

- fold0 `9.708707246008231`
- fold1 `9.616829204374666`
- fold2 `9.381175453451064`
- fold3 `9.421851096308558`
- fold4 `9.633401964439729`

A6 still selects `pi_random=.30` in all five folds.

## Primary corrected contrasts

### Order-free prefix inventory beyond corrected LOCAL40

`G_prefix_cond`:

- mean `+0.0419740198 bit/token`;
- positive 5/5;
- PASS.

Legacy mean was `+0.0443059201`.

### Corrected ORDERED128 over corrected local + prefix hybrid

`G_order_hybrid`:

- mean `+0.0062238133 bit/token`;
- positive 4/5;
- PASS;
- fold2 reverses slightly (`-0.0003081`).

Legacy mean was `+0.0026211611`.

### Corrected ORDERED128 over calibrated matched random lag

`G_order_random_cv`:

- mean `+0.0248492106 bit/token`;
- positive 5/5;
- PASS.

Legacy mean was `+0.0197640698`.

## Robustness judgement

The old Phase-2A scientific conclusion is:

> **ROBUST TO ORDER CORRECTION.**

Correct source order modestly reduces the order-free prefix increment and increases both order-sensitive contrasts, but all three primary pass/fail outcomes and the overall `MIXED PREFIX + ORDER CONTRIBUTIONS` classification remain unchanged.

The corrected result still says that a substantial order-free causal-prefix inventory source exists beyond local recency and that a smaller but reproducible actual source/lag association also remains.

## C3 reference

C3 boundary localization must use:

- corrected LOCAL40 pi `.21,.21,.21,.21,.22`;
- corrected LOCAL40 outer bits from C1;
- corrected ORDERED128 `H=ALL,tau=128,pi=.30` outer bits from C1;
- corrected leaf-prefix-bag A5 rho `.20,.21,.19,.19,.21` and outer code lengths above.

No legacy reference constant is to be forced in C3.

## Firewall

Source order and C1 were frozen before C2 selection. No old outer result entered corrected selection; no candidate/grid extension, future token, surface-target metric, semantic or latent-state signal was used.