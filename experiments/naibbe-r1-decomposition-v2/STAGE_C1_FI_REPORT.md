# Issue #72 V2 — FI final complete-token allocation sufficiency

Date: 2026-09-01  
Status: **COMPLETE; FIRST-REVEAL POPULATION PERMANENTLY FROZEN**

## Question

FI asks a deliberately narrow final-surface question:

> Once the exact Naibbe rep0 complete tokens already exist, does their observed allocation across the retained manuscript/item/line token-slot skeleton materially contribute to the Voynich R1 resemblance, or is the complete-token inventory itself sufficient under the preregistered controls?

FI does not identify upstream historical mechanism. It tests final-surface sufficiency only.

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

For every assignment the complete tokens themselves are unchanged. Only their allocation to token slots changes.

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

The observed identity allocation is therefore not unusually high-R1 relative to either randomization family. The randomization medians are in fact slightly above the identity statistic.

Frozen aggregate classification:

`FINAL_COMPLETE_TOKEN_INVENTORY_SUFFICIENT_UNDER_TESTED_FI_CONTROLS`

## Licensed interpretation

Under these FI controls, the observed placement of already-produced complete Naibbe tokens is not required to retain the R1 resemblance.

This holds at both tested allocation scales:

1. `FI-M`: within-manuscript token placement is exchangeable with respect to R1 once each manuscript's complete-token inventory is fixed.
2. `FI-G`: even the observed allocation of token inventories among manuscripts is not required; the pooled complete-token inventory plus the retained token-slot-count skeleton is sufficient to obtain comparable R1.

The strongest licensed FI claim is therefore:

> **For the tested Naibbe surface, R1 is principally a property of the corpus-level inventory/distribution of internally structured complete tokens, not of where those token instances are placed.**

FI does not say that the complete-token inventory appeared without a generating mechanism. It says that once that inventory exists, its observed allocation carries no detected additional R1 requirement.

## Integration with Stage C1 and Stage D1/PT

The three intervention classes now separate cleanly.

### Stage C1 — direct emission structure matters

Fixed-path emission randomization strongly reduced R1 for:

- effective-letter value association (`EL`),
- functional-state value association (`ES`),
- global reachable-cell value association (`EG`).

The compact direct-emission localization was:

`effective-letter × functional-state -> emitted glyph value`

Table-label allocation (`ET`) was much more exchangeable.

### Stage D1/PT — exact local plaintext order is not required

Extensive within-line plaintext character-order randomization produced essentially zero systematic R1 displacement:

- ZL3b mean D `+0.000879`, median `+0.000827`
- IT2a mean D `-0.000240`, median `+0.000153`
- `p_both = 0.625`

Thus the observed local plaintext sequence was not supported as a material causal necessity for R1 under the PT estimand.

### FI — final token placement is not required

Relocating nearly every already-produced complete token instance likewise did not reduce R1. About 99.6% of token slots changed token identity in both FI families, yet R1 remained typical or slightly higher than identity.

## Mechanistic synthesis

Taken together, the current evidence localizes the Naibbe/Voynich R1 resemblance to **how internally structured token types are generated and how often they occur**, rather than to their local or document-level sequencing.

A useful causal schematic is:

`plaintext composition / encoder states`

`        ↓`

`structured state-dependent emission`

`        ↓`

`complete-token internal forms + corpus frequencies   <-- R1-sensitive layer`

`        ↓`

`token placement across lines/manuscripts            <-- no detected extra R1 requirement`

This changes how R1 should be used in subsequent mechanism search. R1 should be treated primarily as a **token-construction / token-inventory constraint**. It currently has little evidence as a constraint on plaintext local order, token sequence, syntax, or document layout.

In practical inverse-search terms, a candidate mechanism should be asked first whether it naturally generates the observed family of internally structured token forms and their aggregate frequencies. Matching where those finished tokens occur is a separate constraint and should not be credited to R1 itself.

## What this does not establish

These results do not establish:

- historical use of Naibbe;
- Latin plaintext;
- absence of semantics;
- absence of genuine syntax or document structure in Voynich;
- that token placement is irrelevant to other Voynich constraints;
- decipherment.

The conclusion is specifically about what the replicated R1 statistic can causally/evidentially constrain in this experiment.

## Issue #72 endpoint

All three V2 responsibility classes requested by Issue #72 are now resolved:

- fixed-path direct-emission effects: resolved by Stage C1;
- total-pipeline plaintext-order effect: resolved by Stage D1/PT;
- final-surface allocation sufficiency: resolved by FI.

The resulting R1 role is narrower and more useful: **R1 is a replicated constraint on internally structured complete-token inventory, with strong sensitivity to state-dependent emission assignment but no detected requirement for exact local plaintext order or final token placement.**
