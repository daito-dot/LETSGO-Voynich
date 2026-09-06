# Issue #92 / Issue #88 Phase 1 — held-out predictive-information budget

Date: 2026-09-06
Status: **COMPLETE — AUTHORITATIVE FIRST REVEAL ARCHIVED**

Authority:

- frozen plan: `PLAN.md`;
- implementation: `phase1_predictive_budget.py`;
- first-reveal provenance: `FIRST_REVEAL_PROVENANCE.md`;
- authoritative run: `34018276930`;
- artifact ID: `9984665954`;
- `phase1_results.json` SHA-256: `dba64d047b8843974e620c5a4e20f8729b5e37602248718f1e2a77aca91baafe`.

## Decision

> **`MATERIAL PREDICTIVE INFORMATION REMAINS`**

The Phase-0 local DECAY40 mechanism does not exhaust the tested cross-token predictability.

Two prospectively richer V2-based context classes each add reproducible held-out gain in all five physical-leaf folds:

1. longer history beyond the previous 40 tokens;
2. simple observable paragraph/line position after that longer-history model.

A separate matched byte n-gram control independently confirms that context crossing visible-space boundaries is predictive, although it does not prospectively establish more cross-token information than DECAY40 under the cross-model stability rule.

No S1, S2, H62 or R1 quantity participated in this result.

## 1. Predictive ladder

Mean outer held-out code lengths:

| model | mean bits/token | gain from previous rung |
|---|---:|---:|
| B0 frozen V2 | `9.708906` | — |
| B1 local DECAY40 | `9.596181` | `+0.112725` |
| B2 longer-history recency | `9.549254` | **`+0.046927`** |
| B3 + observable paragraph/line state | **`9.520325`** | **`+0.028929`** |

Cumulative B0→B3 reduction:

> **`0.188582 bit/token`**

This is about `1.94%` of the ~9.71-bit V2 code length. The result is therefore asymmetric: there is reproducible sequence information beyond local memory, but its average contribution is still modest compared with the information carried inside a token.

The correct interpretation is not “cross-token structure is negligible” and not “there are several hidden bits of syntax.” It is:

> **under the tested explicit model classes, at least ~0.19 bit/token of predictive structure can be extracted beyond the memoryless token grammar, and the tested budget is not yet saturated by the 40-token local mechanism.**

The number is model-class dependent, not an entropy bound.

## 2. B0/B1 regression

Phase 1 exactly reproduces the frozen Phase-0 baseline and local anchor:

- B0 V2: `9.7089061017 bits/token`;
- B1 DECAY40: `9.5961811202 bits/token`;
- local gain: `0.1127249815 bit/token`;
- positive gain in `5/5` folds.

B1 again selects `H=40`, `tau=32`, with `pi=.21,.21,.20,.21,.21` across folds.

This passed as a hard regression gate before richer-model interpretation.

## 3. Longer-history information survives

B2 uses the same edit-distance-1 recency mechanism as B1 but prospectively allows history windows `{40,80,160,320,ALL}` and scales `{16,32,64,128,256,INF}`.

Result:

- `Delta_long = B1 - B2 = 0.0469270813 bit/token`;
- positive in **5/5** outer folds;
- fold increments: `0.04054, 0.04223, 0.05771, 0.06126, 0.03290`.

Every outer-fold nested selector independently chooses exactly:

> `H=ALL`, `tau=128`, `pi=.30`.

Here `ALL` means all preceding surface tokens on the current physical leaf, never future tokens.

The result is strong evidence that the previous-40 horizon does not exhaust predictive edit-1-family information. But `H=ALL` and `pi=.30` are grid boundaries, so Phase 1 does **not** estimate a historical memory horizon or optimum strength.

Per the frozen stopping rule, the grid is not extended after reveal.

The boundary result creates a more important next question: does the gain really require ordered long history, or is the model exploiting the accumulating local vocabulary/token-family inventory of the leaf?

That distinction belongs to Phase 2 source attribution.

## 4. Observable document state adds information too

B3 tests only externally visible paragraph/line geometry on top of frozen B2:

- `ENTRY_BODY`: first line versus later lines;
- `LINE4`: SINGLE / FIRST / MIDDLE / FINAL line state.

The conditional emission component is shrunk toward global V2 by likelihood-selected `lambda`.

Result:

- `Delta_state = B2 - B3 = 0.0289294918 bit/token`;
- positive in **5/5** folds;
- fold increments: `0.03073, 0.02830, 0.02776, 0.02573, 0.03212`.

All five selectors choose `lambda=.50`.

State family:

- `ENTRY_BODY`: folds 0, 3;
- `LINE4`: folds 1, 2, 4.

Thus observable layout state carries reproducible predictive information after long recency, but the data do not yet establish one unique positional encoding.

This matters conceptually: not all predictive structure resides in token-to-token copying. At least some is tied to the document-production geometry visible on the page.

## 5. Independent visible-space boundary check with byte n-grams

B4 deliberately ignores the V2 slot grammar and edit-distance mechanism. It represents literal token surfaces as UTF-8 bytes plus a fixed `END_TOKEN` symbol and compares two versions of the same smoothed n-gram family:

- B4R `RESET`: context reset before every visible-space token;
- B4C `CONTINUOUS`: context crosses token boundaries and resets only at physical-leaf boundaries.

Primary matched result:

- B4R: `10.184336 bits/token`;
- B4C: `10.054691 bits/token`;
- `Delta_flex = 0.1296450893 bit/token`;
- positive in **5/5** folds.

The continuous selector chooses `k=2, alpha=.01` in all five folds. The reset selector chooses `k=3` in two folds and `k=2` in three; all choose `alpha=.01`.

This independently confirms:

> **information useful for predicting the next visible-space unit crosses the visible-space boundary.**

That does not prove the boundary is a natural-language word boundary. It shows the boundary is not an independence boundary.

Absolute B4 code lengths are worse than V2 and must not be compared directly to V2 as cross-token information. The matched RESET-vs-CONTINUOUS difference is the valid B4 quantity.

## 6. The flexible challenger does not beat local DECAY40 robustly

The prospectively defined cross-model diagnostic was:

`Delta_flex_over_local = Delta_flex - G_local`.

Result:

- mean `+0.016920 bit/token`;
- positive in only `3/5` folds;
- frozen `4/5` stability rule: **FAIL**.

Therefore Phase 1 does **not** claim that the byte model exposes more cross-token information than the simple local edit-1 model.

The material-residual classification instead comes independently from B2 and B3.

This also reinforces an important methodological point: different predictive model families capture overlapping structure, so their gains are not freely additive.

## 7. What Phase 1 changes

Before this phase, there was a serious possibility that the conspicuous cross-token recurrence statistics were generated by a very small local mechanism carrying only about `0.1 bit/token`, after which the sequence was nearly conditionally independent.

That possibility is weakened.

The new evidence says:

1. local edit-1 recency is real and predictive (`~0.113 bit/token`);
2. extending that same family beyond 40 tokens adds another `~0.047 bit/token` reproducibly;
3. observable paragraph/line state adds another `~0.029 bit/token` after long history;
4. an unrelated byte model independently detects `~0.130 bit/token` of cross-boundary predictive gain.

So the next-token information is **not confined to one tiny local recurrence event**.

At the same time, even B3 reduces V2 by only `~0.189 bit/token`. This remains far from the earlier abandoned intuition that cross-token memory should remove `2–3 bits/token`.

The current picture is therefore:

> **Voynich has real, distributed cross-token predictability, but the measured average information rate is still small relative to token-internal construction.**

## 8. What remains unresolved

The B2 `ALL` result is not yet evidence for a literal manuscript-wide or leaf-long memory mechanism.

Several explanations remain observationally entangled:

- genuine order-sensitive long recency;
- a prefix-local cache of token-family availability;
- gradual accumulation of leaf-specific vocabulary/topic inventory;
- document/register heterogeneity correlated with the prefix;
- repeated use of externally driven units that happen to share edit-1 neighbourhoods.

Likewise B3 says positional state predicts token surfaces, not why.

Those are now the main scientific ambiguities.

## 9. Next move: source attribution, not latent state

Phase 1 satisfies Issue #88's entry condition for Phase 2.

The next question is:

> **Which part of the `~0.19 bit/token` tested predictive gain requires sequence order, which part is explained by prefix/leaf token-family inventory, and which part is independently attributable to observable document state?**

The first Phase-2 controls should separate ordered recency from order-free causal prefix cache without using future tokens, and then decompose observable-state gain conditionally.

Rich latent-state work remains premature. If order-free inventory and visible document state explain most of the residual predictive gain, there may be little hidden state to discover. If a robust order-specific residual survives those controls, then a latent or external-state model becomes more strongly motivated.