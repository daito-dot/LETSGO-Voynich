# Issue #58A — 12-slot occupancy-graph specificity audit

Status: **PREREGISTERED — NO ISSUE #58 TARGET REVEAL YET**

Parent result: Issue #55B classified the previously selected slot3×slot5 relation as `DEPENDENCE REDUCES TO BINARY OCCUPANCY EXCLUSION`.

This revision is still pre-reveal. It replaces an initially proposed degree-preserving MCMC sensitivity with a direct held-out token-complexity conditioning analysis, avoiding an arbitrary Markov-chain mixing assumption.

## Scientific question

Issue #55 did not prospectively discover slot3×slot5: that pair was selected through the earlier E10 → #55 path. Issue #58 therefore does not retest that pair in isolation.

> In the complete binary occupancy graph of the frozen 12-slot parser, is the already-selected slot3×slot5 exclusion unusually strong and transferable across physical leaves, or is it one ordinary edge in a broader slot grammar?

This is a representation-level structural audit. It does not assign semantics, plaintext, music, cipher-table meaning, or historical identity to any slot.

## Frozen source and parser

Reuse without alteration:

- frozen ZL3b source Git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- existing `issue26e_core.SlotParser` 12-slot grammar;
- existing deterministic five `physical_leaf_folds`;
- primary parser policy `min`;
- `max` as a non-promoting parser-ambiguity sensitivity only.

For each successfully parsed token define occupancy vector `B in {0,1}^12`, where `B_s=1` iff slot `s` is nonEMPTY.

The complete tested edge set is all `C(12,2)=66` unordered slot pairs in lexicographic `(i,j)` order, `0 <= i < j <= 11`.

The historically selected edge is fixed as `(3,5)` before reveal.

## Population

Use exactly the physical-leaf numerical universe implied by the existing five folds. Every successfully parsed visible token contributes one 12-bit occupancy vector.

Record visible and parsed token counts, parse coverage, physical line counts, per-slot occupancy counts/rates, and per-fold counts.

No pair may be removed after outcome inspection because of rarity.

## Primary pair statistic — held-out symmetric predictive information gain

For each pair `(i,j)`, use the binary analogue of #55B with Jeffreys smoothing `alpha=0.5`.

For each held-out physical-leaf fold, estimate on the other four folds:

- `P(B_i)`, `P(B_j)`;
- `P(B_j | B_i)`, `P(B_i | B_j)`.

On the untouched fold compute base-2 cross-entropy improvements:

`G_j = CE[P(B_j)] - CE[P(B_j | B_i)]`

`G_i = CE[P(B_i)] - CE[P(B_i | B_j)]`

`Gsym(i,j) = (G_i + G_j)/2` bits/token.

Primary real statistic per edge is the equal-weight mean `Gsym` over the five held-out folds. Record all five fold gains and whether all five are positive.

## Direction diagnostics

For every edge also record descriptively:

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
3. uniformly permute that binary occupancy vector across token positions without replacement;
4. do not move states between lines, leaves, paragraphs, or folds.

Thus every null preserves exactly every line×slot occupancy count, every physical boundary, every fold assignment, and line-level register composition, while destroying cross-slot same-token pairing.

For reproducibility and computational tractability, each complete null population uses one deterministic root RNG seed:

`Issue58A:LineSlotOccupancyShuffle:v2:<null_index>`

Within a null, lines are processed in canonical `(leaf,page,paragraph,line_index)` order and slots in `0..11` order. The resulting sequence of independent within-line permutations is therefore fully deterministic without millions of separately hashed seeds.

Every null is rescored for all 66 edges with the identical five-fold procedure.

## Multiplicity correction — global maxT

For each null replicate calculate:

`M_null = max over all 66 edges of mean_Gsym_null(edge)`.

For each real edge `e`, define family-wise maxT adjusted upper-tail p:

`p_maxT(e) = (1 + # {null: M_null >= mean_Gsym_real(e)}) / 1001`.

This is the primary significance quantity. Unadjusted pairwise p-values may be recorded as diagnostics but cannot determine classification.

Because slot3×slot5 was selected before Issue #58 using the same manuscript, even its maxT value is interpreted as **current-representation extremeness**, not an independent prospective discovery p-value.

## Rank and selected-pair accounting

Rank all 66 real edges by descending mean held-out `Gsym`, tie-breaking lexicographically by `(i,j)`. Record fixed edge `(3,5)` rank.

Also rank exclusion diagnostics among edges with negative phi by descending `-phi`; descriptive only.

## Strong sensitivity — condition on occupancy outside the tested pair

The primary null preserves line×slot marginals but individual tokens can differ in overall occupancy complexity after shuffling. Rather than introduce an MCMC null with an arbitrary mixing schedule, use a direct held-out conditioning analysis.

For each pair `(i,j)` define:

`K_other = sum(B_s for s not in {i,j})`, taking values `0..10`.

On each training fold estimate with Jeffreys smoothing:

- baseline `P(B_j | K_other)` versus full `P(B_j | B_i, K_other)`;
- baseline `P(B_i | K_other)` versus full `P(B_i | B_j, K_other)`.

Score the held fold and average the two directional cross-entropy improvements to obtain `Gsym|K_other`.

This asks whether the pair carries predictive information after controlling directly for how many **other** slots the token occupies.

Compute this sensitivity for the real primary `min` population and for the same 1,000 primary null populations. Apply the same global maxT construction across 66 conditional edge statistics.

This sensitivity cannot promote a primary failure. If primary `(3,5)` is globally extreme but its conditional mean is non-positive, not all five conditional folds are positive, or conditional maxT `p > .01`, label the selected-edge interpretation **token-complexity-sensitive** and do not advance directly to a pair-specific transform model.

## `max` parser sensitivity

For parser policy `max`, compute the complete real 66-edge landscape, selected-edge rank, fold gains, direction diagnostics, and `K_other`-conditioned real statistics. Do not run a second multiplicity null family and do not allow `max` to promote the primary `min` classification.

## Parser co-occupancy admissibility audit

For every slot pair `(i,j)`, independently of observed frequencies, test whether at least one canonical token consisting of one allowed value from slot `i` followed by one allowed value from slot `j` has an exact parser output with those two intended slots nonEMPTY and all other ten EMPTY.

Record admitted/not-admitted for all 66 edges and a representative canonical token when admitted.

This distinguishes corpus-level exclusion from a hard impossibility encoded directly by the parser representation.

## Frozen classifications

### `SELECTED SLOT3xSLOT5 EDGE IS GLOBALLY EXTREME`

Primary `min` must satisfy all:

1. selected `(3,5)` rank by mean held-out `Gsym` <= 3 of 66;
2. selected `(3,5)` `p_maxT <= .01`;
3. all five selected-edge held-out gains positive;
4. pooled selected-edge phi < 0.

### `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`

Selected-edge extreme gate fails and at least five distinct edges have `p_maxT <= .01` with all five held-out gains positive.

### `SPARSE OCCUPANCY DEPENDENCE; SLOT3xSLOT5 NOT GLOBALLY EXTREME`

Selected-edge extreme gate fails and 1–4 edges meet `p_maxT <= .01` plus all-five-positive.

### `NO FAMILY-WISE OCCUPANCY EDGE SURVIVES`

Zero edges meet `p_maxT <= .01` plus all-five-positive.

`K_other` sensitivity and `max` parser policy cannot promote the primary classification.

## Interpretation rules

If selected edge is globally extreme and survives the `K_other` sensitivity, retain slot3×slot5 as a particularly strong representation-level incompatibility and permit a new plan-first test of whether it constrains a reversible surface-transform grammar.

If primary edge is extreme but `K_other`-sensitive, investigate the broader construction/complexity grammar instead of treating the pair as autonomous.

If a broad graph emerges, promote the object of study from slot3×slot5 to the complete occupancy grammar and characterize graph topology/conditional structure before attempting meaning.

If no family-wise edge survives, narrow #55 to a selected-pair observation under the earlier representation and do not build further decipherment claims on it.

## Stop rules

No post-reveal search over alternate slot subsets, occupancy definitions, folds, smoothing constants, thresholds, selected-edge neighborhoods, null families, or parser remappings. Any such change requires a new explicitly exploratory phase and cannot rescue #58A.
