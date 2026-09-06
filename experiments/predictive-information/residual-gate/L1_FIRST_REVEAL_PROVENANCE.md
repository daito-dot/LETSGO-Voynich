# Issue #121 L1 first-reveal provenance

Date: 2026-09-06
Parent: Issue #88 / Issue #118
Status: **AUTHORITATIVE FIRST REVEAL**

## Frozen scientific head

`30a7a8caf1a358d8c98fb4376ff9d4943d44b0ff`

No L1 `G_edge` value or transition-topology diagnostic was inspected before PR #122 was opened at this head.

## Workflow authority

- workflow: `Issue121 boundary-edge same-order L1 first reveal`
- run: `34026787486`
- conclusion: **SUCCESS**
- artifact: `9987357230`
- artifact ZIP digest: `sha256:3370dc79c17e7d8e700ac42264c242fed7ea93f50c9715ea1bc516e9b0b007cd`
- result JSON SHA-256: `574216279d545c9c0c7f468c1e36f0b022ab331f21fa450bd8f0e7bf6f17899c`

## Embedded core authority

The L1 scorer reran the corrected Phase-1 core and reproduced the merged Issue #119 normalized authority SHA-256:

`0d7f311dac17f5736f8191b8ea38cf5f2eac9b7391150a986204772da181ae27`

The already-merged one-cell floating-point Amendment A was the only permitted normalization. Source, corrected order, folds, B3 target support and interpretation firewall all passed before L1 scoring.

## Frozen model comparison

Both byte experts were forced to the same fixed hyperparameters:

- `k=2`
- `alpha=.01`

Only boundary policy differed:

- `RESET2`: history cleared before every visible token;
- `CONT2`: history carried across visible tokens on a physical leaf and cleared only at leaf change.

Each expert was mixed with the same corrected B3 probability using `w=0.00..1.00`, selected by pooled inner accepted-token likelihood only, ties to smaller `w`.

## Authoritative result

Frozen classification:

> **BOUNDARY-EDGE RESIDUAL SURVIVES SAME-ORDER CONTROL**

Primary `G_edge = bits(MIX_RESET2)-bits(MIX_CONT2)`:

- fold0 `+0.013939262960121823`
- fold1 `+0.00811504079524461`
- fold2 `+0.00930042233496664`
- fold3 `+0.010865786933976551`
- fold4 `+0.010940638641795175`
- mean `+0.01063223033322096 bit/token`
- positive folds `5/5`
- frozen gate: **PASS**

Mean code lengths:

- B3 `9.517268842963203`
- MIX_RESET2 `9.497295653343732`
- MIX_CONT2 `9.486663423010512`

Inner-selected mixture weights:

- RESET2: `.04` in all five outer folds;
- CONT2: `.08,.08,.09,.08,.09`.

Thus the Issue #118 residual does not depend on RESET and CONT having selected different byte n-gram orders.

## Predeclared descriptive localization

These diagnostics were frozen before the reveal and do not alter the primary class.

By relation to the immediately previous visible token:

- `SAME_LINE`: n=22,141, mean delta `+0.011497425824750905`, total `+254.5645051858098 bits`;
- `CROSS_LINE_SAME_ITEM`: n=2,631, mean `-0.0007373234074281035`, total `-1.9398978849433404`;
- `CROSS_ITEM_SAME_DOCUMENT`: n=226, mean `+0.0004219232574831847`, total `+0.09535465619119975`;
- `CROSS_DOCUMENT_SAME_LEAF`: n=36, mean `-0.008703347225276215`, total `-0.3133205001099437`;
- `LEAF_START`: n=37, mean `+0.3276686383469451`, total `+12.123739618836968`.

The rare `LEAF_START` stratum is not evidence for cross-token dependence because no previous token exists there; it reflects the predeclared generic BOS/END start-distribution difference between the two fixed experts.

The scientifically relevant cross-token pattern is therefore descriptive but strong: essentially all positive non-leaf-start contribution is within the same source line; carry-over across a line break supplies no positive average advantage in this reveal.

By already-defined observable state:

- paragraph/first-line `ENTRY`: n=4,394, mean `+0.0193291985196144`;
- `BODY`: n=20,677, mean `+0.008685877195947139`;
- line-state `FIRST`: same n/mean as ENTRY;
- `MIDDLE`: n=17,502, mean `+0.00827776067057223`;
- `FINAL`: n=3,175, mean `+0.01093559544070672`.

These are descriptive localizations only. They do not establish a causal line state, Currier effect or hidden state.

## Interpretation boundary

L1 supports the narrow statement:

> After forcing RESET and CONT to the identical k=2 byte model, a small reproducible advantage remains for carrying immediate raw-surface boundary context across adjacent visible units. The observed advantage is descriptively concentrated within source lines rather than across line breaks.

L1 does **not** establish semantics, plaintext, language, cipher family, historical copy/mutate behavior, or latent state. The residual remains only about `0.0106 bit/token`, and the next licensed step is explicit observable/topological localization before any latent-state challenger receives interpretation.
