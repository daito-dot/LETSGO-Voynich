# Issue #72 V2 — FI final complete-token allocation sufficiency

Date: 2026-09-01  
Status: **COMPLETE; FIRST-REVEAL POPULATION PERMANENTLY FROZEN**

## Question

FI asks a deliberately narrow final-surface question:

> Once the exact Naibbe rep0 complete tokens already exist, does their observed allocation across the retained manuscript/item/line token-slot skeleton materially contribute to the Voynich R1 resemblance, or is the already-produced inventory sufficient under the preregistered controls?

FI does not identify upstream historical mechanism. It tests final-surface allocation sufficiency only.

## Representation clarification

The R1 scorer does **not** compare literal token strings or glyph identities directly.

For every parser-accepted token, `SlotParser(min)` maps the token into the frozen 12-slot representation and the R1 scorer converts it to a 12-element binary occupancy vector:

`X[token, slot] = occupied / empty`

The 66 R1 edges are then computed from the `C(12,2)=66` unordered pairs of these binary slot occupancies, using the frozen `K_other`-conditional association and null-residual calibration.

Therefore the direct object measured by R1 is the **distribution and residual dependency structure of 12-slot occupancy signatures**, not lexical identity as such.

This matters for interpreting FI. Shuffling whole tokens necessarily preserves the global multiset of their parsed occupancy signatures. FI tests whether the *observed placement* of those already-existing signatures across manuscripts, lines and token slots adds R1 information beyond that inventory.

## Frozen design

Normative preregistration:

- `STAGE_C1_FI_PLAN.md`
- plan commit `a053efd9803b6c0f74614986289c54a8add7d904`

Frozen implementation:

- scorer commit `efad503afeb45500a8e520680ed7189bf9ee33f1`
- aggregate commit `285fb10db3f92df401f3f459d73827590af637a7`
- successful target-blind preflight run `33496383052`
- preflight head `3ac22384ce5379d82883f9fd9ae7daa01677f27d`

Identity authority:

- rep0 pooled primary surface SHA-256 `47d52d28d4e2ac126bb8681c881ec339cb339c9b1bb329fb48263e6c1e9758bd`
- visible complete-token instances: `33,574`
- distinct complete tokens: `7,146`
- parser-accepted instances: `29,759`
- pooled coverage: `0.886370405671055`
- fixed identity statistic `T_identity = min(R_ZL3b, R_IT2a) = 0.8830282501011794`

Two prospectively fixed randomization families were tested, each with 199 assignments:

- `FI-G`: globally shuffle complete token instances across the fixed token-slot skeleton while preserving the global complete-token multiset and every manuscript/item/line visible-token count.
- `FI-M`: shuffle complete token instances only within each manuscript while preserving each manuscript's exact complete-token multiset and every manuscript/item/line visible-token count.

For every assignment the token strings themselves are unchanged. Only their allocation to token slots changes.

The randomization test was frozen as:

`p_F = (1 + count(T_perm >= T_identity)) / 200`

for each family, followed by Holm step-down correction across exactly FI-G and FI-M at family-wise alpha `.05`.

No case was dropped or rerolled. No coverage gate, arbitrary topology threshold, target-reading average, additional post-reveal family, or global R1 PASS/FAIL class was introduced.

## Exact first-reveal authority

Canonical scientific head:

`442fa401dcd82fda7f6bb1c4720b908c50900c0b`

Canonical workflow:

- run `33496538872`
- conclusion `success`
- complete population `398/398 = 199 FI-G + 199 FI-M`
- first-reveal artifact ID `9796801812`
- artifact digest `sha256:5defd596ca91164e9d897c2d5cd5d34c6287465613d867b5c1f3bd528113b309`
- aggregate SHA-256 `40eb7b63370c1cd33a00586414778c93eaa68372b32c7d3b68fc97cd7b0a8dea`

Permanent post-reveal transport-only freeze:

- workflow run `33499435173` — `success`
- repository commit `cd38b1dfc001d9f54add16f6c5b97ae0b1ad9ee0`
- permanent directory `experiments/naibbe-r1-decomposition-v2/stage-c1-fi/`

## Frozen result

| family | T identity | randomization median T | identity - median | T_perm >= identity | raw p | Holm p |
|---|---:|---:|---:|---:|---:|---:|
| FI-G | 0.8830282501 | 0.8850915488 | -0.0020632987 | 138/199 | 0.695 | 1.000 |
| FI-M | 0.8830282501 | 0.8853778655 | -0.0023496154 | 145/199 | 0.730 | 1.000 |

Identity percentile among the 199 randomizations:

- FI-G: `30.65%`
- FI-M: `27.14%`

The observed identity allocation is therefore not unusually high-R1 relative to either randomization family. The randomization medians are slightly above the identity statistic.

Frozen aggregate classification:

`FINAL_COMPLETE_TOKEN_INVENTORY_SUFFICIENT_UNDER_TESTED_FI_CONTROLS`

That label is retained exactly because it was preregistered. The representation audit above sharpens its scientific meaning: the R1 information preserved by the complete-token inventory is carried through the inventory of parsed 12-slot occupancy signatures.

## Licensed interpretation

Under these FI controls, the observed placement of already-produced Naibbe tokens is not required to retain the R1 resemblance.

At the level R1 actually measures:

1. `FI-M`: within-manuscript placement of occupancy signatures is exchangeable with respect to R1 once each manuscript's token/occupancy inventory is fixed.
2. `FI-G`: even manuscript-level allocation is not required; the pooled occupancy-signature inventory plus the retained line/token-count skeleton produces comparable R1.

The strongest representation-correct claim is:

> **For the tested Naibbe surface, R1 is principally a corpus-level 12-slot occupancy-grammar/inventory statistic, not a statistic of where those occupancy patterns occur.**

FI does not show that literal glyph identity or full lexical token identity is irrelevant to Voynich structure generally. Those details are largely projected away by the R1 representation before scoring.

## Integration with Stage C1 and Stage D1/PT

### Stage C1 — upstream emitted-value association matters

Fixed-path emission randomization strongly reduced R1 for:

- effective-letter value association (`EL`),
- functional-state value association (`ES`),
- global reachable-cell value association (`EG`).

The compact upstream localization was:

`effective-letter × functional-state -> emitted glyph value`

Table-label allocation (`ET`) was much more exchangeable.

Because R1 ultimately scores binary slot occupancy, C1 should be interpreted as an upstream causal pathway:

`state-dependent emitted glyph assignment -> parsed token shape -> 12-slot occupancy signature -> R1`

C1 does **not** mean that R1 directly recognizes particular glyph identities.

### Stage D1/PT — exact local plaintext order is not required

Extensive within-line plaintext character-order randomization produced essentially zero systematic R1 displacement:

- ZL3b mean D `+0.000879`, median `+0.000827`
- IT2a mean D `-0.000240`, median `+0.000153`
- `p_both = 0.625`

Thus the observed local plaintext sequence was not supported as a material causal necessity for the resulting occupancy topology under the PT estimand.

### FI — final occupancy-pattern placement is not required

Relocating nearly every already-produced complete token instance likewise did not reduce R1. About 99.6% of token slots changed literal token identity in both FI families, yet the occupancy inventory remained fixed and R1 remained typical or slightly higher than identity.

## Mechanistic synthesis

Taken together, the evidence localizes the Naibbe/Voynich R1 resemblance to the production of a characteristic **inventory of token-internal slot-occupancy patterns and their residual dependencies**, rather than to local source order or final token placement.

A representation-correct schematic is:

`source composition / encoder state opportunities`

`        ↓`

`state-dependent emitted-value mapping`

`        ↓`

`surface token strings`

`        ↓  SlotParser(min)`

`12-slot occupied/empty signatures + corpus frequencies   <-- R1-sensitive layer`

`        ↓`

`placement across lines/manuscripts                       <-- no detected extra R1 requirement`

This is narrower than saying R1 measures a complete lexical grammar. It measures a replicated **morphotactic occupancy grammar** under the frozen 12-slot representation.

## Consequence for inverse mechanism search

A candidate mechanism should not receive R1 credit merely because it reproduces plausible-looking token strings, syntax-like sequencing, or document layout.

The direct R1 question is:

> **Does the mechanism naturally generate the correct distribution and 66-edge residual dependency topology of 12-slot occupied/empty token shapes?**

Literal glyph inventories, token spellings, recurrence, paragraph-entry behavior, sequence organization and reversibility remain separate constraints.

## What this does not establish

These results do not establish:

- historical use of Naibbe;
- Latin plaintext;
- absence of semantics;
- absence of genuine syntax or document structure in Voynich;
- that glyph identity or token spelling is irrelevant to other constraints;
- decipherment.

## Issue #72 endpoint

All three V2 responsibility classes requested by Issue #72 are resolved:

- fixed-path direct-emission effects: Stage C1;
- total-pipeline plaintext-order effect: Stage D1/PT;
- final-surface allocation sufficiency: FI.

The resulting R1 role is now precise:

> **R1 is a replicated constraint on the corpus-level residual grammar of 12-slot token occupancy. State-dependent emission assignment can strongly alter that grammar upstream, while exact local plaintext order and the observed placement of finished occupancy patterns carry no detected additional R1 requirement.**
