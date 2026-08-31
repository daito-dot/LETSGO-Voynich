# Issue #58A — 12-slot occupancy-graph specificity audit

Status: **PREREGISTERED — NO ISSUE #58 TARGET REVEAL YET**

Parent result: Issue #55B classified the previously selected slot3×slot5 relation as `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`.

## Scientific question

Issue #55 did not prospectively discover slot3×slot5: that pair was selected through the earlier E10 → #55 path. Issue #58 therefore does not retest that pair in isolation.

The question is:

> In the complete binary occupancy graph of the frozen 12-slot parser, is the already-selected slot3×slot5 exclusion unusually strong and transferable across physical leaves, or is it one ordinary edge in a broader slot grammar?

This is a representation-level structural audit. It does not assign semantics, plaintext, music, cipher-table meaning, or historical identity to any slot.

## Frozen source and parser

Reuse without alteration:

- the same frozen ZL3b source blob used in #55: Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- the existing `issue26e_core.SlotParser` 12-slot grammar;
- the existing deterministic five `physical_leaf_folds`;
- primary parser policy `min`;
- `max` as a non-promoting parser-ambiguity sensitivity only.

For each successfully parsed token define occupancy vector `B in {0,1}^12`, where `B_s=1` iff slot `s` is nonEMPTY.

The complete tested edge set is all `C(12,2)=66` unordered slot pairs, in lexicographic `(i,j)` order with `0 <= i < j <= 11`.

The historically selected edge is fixed as `(3,5)` before reveal.

## Population

Use exactly the physical-leaf numerical universe implied by the existing five folds. Every successfully parsed visible token contributes one 12-bit occupancy vector.

Record:

- visible and parsed token counts;
- parse coverage;
- physical line counts;
- per-slot occupancy counts and rates;
- per-fold counts.

No pair may be removed after outcome inspection because of rarity. Low-information pairs remain in the complete landscape and are reported as such.

## Pair statistic — held-out symmetric predictive information gain

For each pair `(i,j)`, use the exact binary analogue of #55B with Jeffreys smoothing `alpha=0.5`.

On each held-out physical-leaf fold, estimate from the other four folds:

- `P(B_i)`, `P(B_j)`;
- `P(B_j | B_i)`, `P(B_i | B_j)`.

On the untouched fold compute base-2 cross-entropy improvements:

`G_j = CE[P(B_j)] - CE[P(B_j | B_i)]`

`G_i = CE[P(B_i)] - CE[P(B_i | B_j)]`

`Gsym(i,j) = (G_i + G_j)/2` bits/token.

Primary real statistic per edge is the equal-weight mean `Gsym` over the five held-out folds.

Also record all five fold gains and whether all five are positive.

## Direction diagnostics

Predictive information is unsigned with respect to co-occurrence versus exclusion. Therefore also record, descriptively for every edge:

- pooled 2×2 contingency table;
- phi coefficient;
- observed co-occupancy rate;
- independence-expected co-occupancy rate;
- co-occupancy ratio `observed / expected` when expected > 0.

Negative phi / ratio below 1 indicate exclusion. These diagnostics do not replace the predictive-information primary statistic.

## Primary null — within-line independent occupancy relocation

Generate exactly **1,000 deterministic null populations**.

For every physical line independently and for each of the 12 slots independently:

1. keep the number of parsed token positions in that line fixed;
2. keep that slot's exact line-local number of occupied positions fixed;
3. shuffle the slot occupancy vector across token positions without replacement;
4. do not move any occupancy state between lines, leaves, paragraphs, or folds.

Thus every null preserves exactly:

- line/token counts and all physical boundaries;
- for every line and slot, the occupancy count and occupancy rate;
- all fold membership and line-level register composition.

It destroys cross-slot same-token pairing while retaining each slot's line-local prevalence.

Frozen seed namespace:

`Issue58A:LineSlotOccupancyShuffle:v1:<null_index>:<page>:<paragraph>:<line_index>:<slot>`

Every null is rescored for all 66 edges with the identical five-fold procedure.

## Multiplicity correction — global maxT

For each null replicate calculate:

`M_null = max over all 66 edges of mean_Gsym_null(edge)`.

For each real edge `e`, define family-wise maxT adjusted upper-tail p:

`p_maxT(e) = (1 + # {null: M_null >= mean_Gsym_real(e)}) / 1001`.

This is the primary significance quantity. Unadjusted pairwise p-values may be recorded as diagnostics but cannot determine classification.

Because slot3×slot5 was selected before Issue #58 using the same manuscript, even its maxT value is interpreted as **current-representation extremeness**, not an independent prospective discovery p-value.

## Rank and selected-pair accounting

Rank all 66 real edges by:

1. descending mean held-out `Gsym`;
2. tie-break lexicographic `(i,j)`.

Record the fixed selected edge `(3,5)` rank.

Also rank exclusion diagnostics among edges with negative phi by descending `-phi`; this is descriptive only.

## Strong sensitivity — token-complexity-preserving line switches

The primary null preserves every line×slot marginal but can change the number of occupied slots within an individual token.

As a non-promoting sensitivity, generate **250 deterministic degree-preserving nulls** over each line's binary token×slot matrix using repeated valid 2×2 checkerboard switches. A valid switch converts either

`[[1,0],[0,1]] <-> [[0,1],[1,0]]`

for two token rows and two slot columns.

This preserves exactly within every line:

- each slot's occupancy count;
- each token's total occupied-slot count;
- line length.

For each line/null perform `max(100, 20 * number_of_ones)` deterministic attempted valid switches after deterministic initialization from the real matrix. Lines with no valid switch remain unchanged and are counted.

Frozen seed namespace:

`Issue58A:DegreePreservingSwitch:v1:<null_index>:<page>:<paragraph>:<line_index>`

Compute the same 66-edge landscape and maxT adjusted p-values. This sensitivity cannot promote a primary failure.

## Parser co-occupancy admissibility audit

For every slot pair `(i,j)`, independently of observed frequencies, test whether at least one canonical token consisting of one allowed value from slot `i` followed by one allowed value from slot `j` has an exact parser output with:

- those two intended slots nonEMPTY;
- all other ten slots EMPTY.

Record admitted / not-admitted for all 66 edges and representative canonical tokens.

This distinguishes corpus-level exclusion from a hard impossibility encoded directly by the parser representation.

## Frozen classifications

### `SELECTED SLOT3xSLOT5 EDGE IS GLOBALLY EXTREME`

Classify this only if primary `min` satisfies all:

1. selected `(3,5)` rank by mean held-out `Gsym` is <= 3 of 66;
2. selected `(3,5)` `p_maxT <= .01`;
3. all five selected-edge held-out gains are positive;
4. pooled selected-edge phi < 0 (the retained relation is exclusion, not positive co-occupancy).

### `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

Classify this if the selected-edge extreme gate above fails **and** at least five distinct edges have `p_maxT <= .01` with all five held-out gains positive.

### `SPARSE OCCUPANCY DEPENDENCE; SLOT3xSLOT5 NOT GLOBALLY EXTREME`

Classify this if the selected-edge extreme gate fails and 1–4 edges meet `p_maxT <= .01` plus all-five-positive.

### `NO FAMILY-WISE OCCUPANCY EDGE SURVIVES`

Classify this if zero edges meet `p_maxT <= .01` plus all-five-positive.

The degree-preserving sensitivity and `max` parser policy cannot promote the primary classification.

## Interpretation rules

If the selected edge is globally extreme:

- retain slot3×slot5 as a particularly strong representation-level incompatibility;
- do not infer a 25-state code;
- next work may test whether this edge constrains a reversible surface-transform grammar, but only under a new plan-first design.

If a broad graph emerges:

- promote the object of study from slot3×slot5 to the complete occupancy grammar;
- treat #55's edge as a selected example rather than a privileged code candidate;
- characterize graph topology/conditional structure before attempting meaning.

If no family-wise edge survives:

- narrow #55 to a selected-pair observation under the earlier representation and do not build further decipherment claims on it.

## Stop rules

No post-reveal search over:

- alternate slot subsets;
- alternate occupancy definitions;
- different fold construction;
- alternative smoothing constants;
- threshold or rank changes;
- selected-edge neighborhoods;
- null families;
- parser remappings.

Any such change requires a new explicitly exploratory phase and cannot rescue #58A.
