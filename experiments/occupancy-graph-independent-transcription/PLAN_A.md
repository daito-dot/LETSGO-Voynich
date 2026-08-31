# Issue #58D / #66 — preregistered independent-reading replication of the residual token-construction graph

Status: **PREREGISTERED — NO #58D PAIR, RESIDUAL, OR CROSS-READING TARGET SCORE REVEALED**

Parent: Issue #66 under umbrella Issue #58.

This plan must predate any executable that calculates an IT2a pairwise Q value, residual Z edge, residual energy, within-IT residual similarity, or ZL3b↔IT2a residual topology score.

## 1. Program object

Read `research/TOKEN_CONSTRUCTION_PROGRAM.md` first.

This lane studies the internal assembly of **one space-delimited Voynich token** under the established 12-slot representation.

It is not sentence-level grammar. Visible spaces are observed delimiters and are not assumed to be proven linguistic word boundaries.

#58C established under ZL3b that a broad token-internal residual interaction system remains after controlling line-local slot prevalence, with a shared core across Currier/section/line-position strata and measurable modulation.

#58D asks whether that result is **portable across an independent manuscript reading lineage** rather than being peculiar to the ZL3b reading/transcription.

## 2. Exact prior claim being replicated

Frozen #58C first reveal:

> `RESIDUAL GRAPH EXISTS WITH STRATUM MODULATION`

Frozen #58C first-reveal raw SHA-256:

`fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`

Integrated #58C main commit:

`c777b81c9ef424429105dbcfd60532bdb9158362`

The ZL3b first-reveal artifact is fixed external reference data. #58D may load it only after verifying that exact raw SHA-256. It must not reselect ZL edges, thresholds, groups or the ZL reference population after inspecting IT2a.

Known #58C aggregate facts are part of the replication target, not newly discovered #58D degrees of freedom:

- pooled `E_ALL = 3.2315507868`;
- `p_exist_ALL = 1/1001`;
- `W_ALL = 0.9447148364`;
- all seven target strata supported residual existence;
- four contrasts were `STABLE_RESIDUAL`: section B/H, B/S, H/S within Currier B, and line interior/final;
- three were `RELATED_RESIDUAL_BUT_MODULATED`: Currier A/B within Herbal, initial/interior, initial/final;
- no contrast was `DIFFERENT_RESIDUAL_OR_MIXTURE`.

Because #58C's finite 1,000-reference transform saturated many individual edges near the finite normal-score limits, #58D will not interpret tiny differences in individual Z magnitudes. Complete-graph correlation is retained for comparability, while full-graph sign agreement is added as a co-primary topology guard against overinterpreting saturated magnitudes.

## 3. Stage-A authorization already frozen without target scoring

Stage-A source/population audit completed before this plan and explicitly computed no pair/residual target metric.

Primary independent reading:

> **IT2a — Takeshi Takahashi reading in `EvaT`**

Exact source authority:

- URL: `https://www.voynich.nu/data/IT2a-n.txt`;
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`;
- Git-blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`;
- bytes: `342,104`;
- lines: `5,444`;
- header: `#=IVTFF EvaT 2.0 M 3`.

Stage-A disposition:

> `AUTHORIZED_FOR_TARGET_PLAN`

Observed support before any target score:

- clean W1 tokens: `34,411`;
- unchanged 12-slot parser accepted: `28,280`;
- coverage: `0.8218302287`;
- physical leaves shared with #58C: `99/99`;
- fold accepted tokens: `[4976, 5416, 6261, 6197, 5430]`;
- accepted group totals: AH `6295`, BH `2739`, BB `5551`, BS `8744`;
- accepted position totals: initial `3156`, interior `22105`, final `3006`.

Accepted group-by-fold support:

- AH: `[1632, 949, 1494, 1241, 979]`;
- BH: `[218, 859, 458, 580, 624]`;
- BB: `[1095, 1040, 1293, 1363, 760]`;
- BS: `[1462, 1433, 2389, 2166, 1294]`;
- initial: `[579, 591, 709, 679, 598]`;
- interior: `[3817, 4257, 4894, 4874, 4263]`;
- final: `[576, 567, 651, 643, 569]`.

Therefore all seven #58C contrasts remain in the #58D confirmatory family. BH fold0 is the smallest supported cell at 218 accepted tokens and is retained rather than repaired or rebalanced.

## 4. Independence claim and limitation

IT2a represents a Takeshi Takahashi reading lineage distinct from the ZL reading used by #58C.

However, IT2a and ZL3b both live inside an EVA/IVTFF representational ecosystem. A successful #58D result therefore supports:

> **replication across an independent manuscript reading lineage under a common EVA/IVTFF framework**

not complete alphabet/publication-pipeline independence.

GC2a/v101 is not part of the confirmatory target. No v101→EVA mapping may be introduced in #58D after inspection.

## 5. Frozen IT2a source parsing and 12-slot representation

### 5.1 Source-native W1 parsing

Use the pre-existing Phase63B W1 semantics:

- only P-coded IVTFF loci;
- source-native paragraph/page/physical-line boundaries;
- both `.` definite and `,` uncertain spaces are W1 boundaries;
- established IVTFF inline controls removed by the pre-existing parser;
- uncertain/unreadable tokens excluded rather than repaired;
- native EvaT letters retained exactly.

No new glyph mapping, normalization, spelling repair, token merge/split or line repair is allowed after target reveal.

### 5.2 Slot parser

Use the current frozen 12-slot grammar from:

`experiments/issue26-music/issue26e_core.py`

Primary ambiguity policy:

> `min`

Non-promoting sensitivity:

> `max`

Stage A established 9,492 accepted IT2a tokens with more than one legal parse and different `min`/`max` selected parses. This ambiguity is a known representation sensitivity and must not be hidden.

### 5.3 Token position

Token position is attached from the clean source line **before 12-slot rejection**, matching the #58B/#58C principle that position belongs to the observed source line rather than parser success:

- singleton: only clean token;
- initial: first of >=2 clean tokens;
- final: last of >=2 clean tokens;
- interior: all others.

Only successfully parsed token rows enter occupancy graphs, retaining their pre-parser position label.

## 6. Frozen physical-leaf folds and groups

Use the exact same 99 physical leaves and five leaf folds as #58C.

Groups:

- `ALL`;
- `AH` — Currier A within Herbal;
- `BH` — Currier B within Herbal;
- `BB` — section B within Currier B;
- `BS` — section S within Currier B;
- `initial`;
- `interior`;
- `final`.

Seven within-IT contrasts, unchanged from #58C:

1. `CURRIER_H_A_vs_B`: AH vs BH;
2. `SECTION_B_vs_H`: BB vs BH;
3. `SECTION_B_vs_S`: BB vs BS;
4. `SECTION_H_vs_S`: BH vs BS;
5. `POSITION_initial_vs_interior`;
6. `POSITION_initial_vs_final`;
7. `POSITION_interior_vs_final`.

No group or contrast may be dropped because its target effect is weak.

## 7. Base edge statistic

Retain all `C(12,2)=66` unordered slot pairs.

For each successfully parsed token, construct binary occupancy vector `B in {0,1}^12`.

For pair `(i,j)`, define:

`K_other = sum(B) - B_i - B_j`.

Use exactly the #58C base statistic:

1. form the `2 x 2` table of `(B_i,B_j)` within each observed `K_other=k`;
2. add Jeffreys `alpha=.5` to each cell of each observed table;
3. compute Mantel-Haenszel common odds ratio;
4. map to Yule Q: `Q=(OR_MH-1)/(OR_MH+1)`.

No individual edge may be excluded or promoted based on #58C strength or #58D outcome.

## 8. IT2a null and residual calibration

IT2a receives its **own** null calibration. ZL3b's edge-wise null distributions are never used to normalize IT2a.

### 8.1 Line-local null

For each IT2a physical line and each of 12 slots independently, relocate occupied states among the successfully parsed rows of that same line.

Preserve exactly:

- physical line identity;
- accepted row count per line;
- line × slot occupied count;
- page/Currier/section metadata attached to rows;
- frozen physical-leaf fold;
- pre-parser token-position label attached to each accepted row.

Destroy same-token cross-slot pairing.

### 8.2 Independent null split

Exactly 2,000 primary IT2a null populations:

Reference namespace, `N_ref=1000`:

`Issue58D:IT2a:ResidualGraph:Reference:LineSlotOccupancyShuffle:v1:<index>`

Test namespace, `N_test=1000`:

`Issue58D:IT2a:ResidualGraph:Test:LineSlotOccupancyShuffle:v1:<index>`

Reference nulls define residual calibration only. Test nulls supply confirmatory distributions only.

### 8.3 Residual transform

Use exactly #58C's reference empirical mid-rank normal score, separately for every:

`group × view × edge`.

Views are:

- FULL;
- five TRAIN excluding one physical-leaf fold;
- five HELD containing one physical-leaf fold.

For candidate q against sorted reference values `r_1...r_1000`:

`u(q) = [0.5 + #{r<q} + 0.5*#{r=q}] / 1001`

`Z(q) = Phi^{-1}(u(q))`.

No alternative z-score, clipping, edge weighting or post-reveal normalization is allowed.

## 9. Gate A — independent residual existence under IT2a

For residual vector `z`, define:

`E(z)=sqrt(mean_e z_e^2)` over all 66 edges.

Primary pooled IT2a existence:

- real `E_IT_ALL`;
- 1,000 independently transformed IT test-null energies;
- empirical upper-tail `p_exist_IT = [1 + #{E_null >= E_real}] / 1001`.

Physical-leaf reliability:

`W_IT_ALL = median_f corr(z_TRAIN(ALL,f), z_HELD(ALL,f))`, requiring >=4 valid folds.

Independent residual existence is **established** iff:

- `p_exist_IT <= .01`; and
- `W_IT_ALL >= .50`.

Stop rules:

- if `p_exist_IT > .01`, with this already adequate Stage-A population the global #58D result is `ZL3B RESIDUAL GRAPH DOES NOT REPLICATE INDEPENDENTLY`; topology may be emitted descriptively but cannot rescue the phase;
- if `p_exist_IT <= .01` but `W_IT_ALL < .50` or <4 valid folds, global result is `INDEPENDENT-TRANSCRIPTION REPLICATION INCONCLUSIVE`.

Only if Gate A passes may cross-reading topology promote.

## 10. IT2a stratum existence and within-IT geometry

After Gate A passes, reproduce #58C's exact seven-stratum residual-existence framework.

For each target group S compute `E_S` and `W_S`.

For each test null, take maximum residual energy across the seven groups. Family-wise p:

`p_E,maxT(S)`.

Group residual existence is supported iff:

- `p_E,maxT <= .01`;
- `W_S >= .50` with >=4 valid folds.

Then classify all seven within-IT contrasts using **the exact #58C gates without threshold changes**:

### `STABLE_RESIDUAL`

- both groups supported;
- Pearson `R_Z >= .70`;
- within-IT contrast maxT `p_R <= .01`;
- both directional held-out transfers satisfy the #58C rule `>= max(.60, target W-.15)`.

### `RELATED_RESIDUAL_BUT_MODULATED`

If stable fails:

- both groups supported;
- `R_Z >= .40`;
- `p_R <= .01`;
- both directional transfers `>= .30`.

### `DIFFERENT_RESIDUAL_OR_MIXTURE`

Both groups supported and any of:

- `R_Z < .40`;
- either directional transfer `<.30`.

Otherwise use the same #58C inconclusive classes.

The #58C register/section and line-position family classification rules are reused verbatim for IT2a.

## 11. Gate B — cross-reading complete-graph topology

The frozen ZL3b #58C residual vectors are loaded from the permanent first-reveal archive only after verifying raw SHA-256 `fba60daea6e30682065900a4cf15d53d2a2f536d933b588fae447fb43bb4728d`.

For each group S in:

`ALL, AH, BH, BB, BS, initial, interior, final`

compare the complete frozen ZL3b `z_full[S]` against the complete real IT2a `z_full[S]`.

### 11.1 Primary cross-reading correlation

`R_cross(S) = Pearson(z_ZL[S], z_IT[S])` over all 66 edges.

Pearson is retained because it is the #58C primary topology statistic and the same residual transform is used independently on each reading.

### 11.2 Co-primary saturation-robust sign agreement

`A_cross(S) = #{e: sign(z_ZL,e) == sign(z_IT,e) and neither is zero}` out of all 66 fixed edges.

Zero-valued residuals count as non-agreements rather than being dropped.

This is not an edge-selection test: every edge remains in the denominator.

### 11.3 Independent cross-reading nulls

For every one of the 1,000 IT2a test-null residual graphs, correlate/compare its group residual vector against the **fixed ZL3b real** residual vector for the same group.

Define family-wise maxima across all eight groups:

- `M_cross_R,null = max_S R_cross,null(S)`;
- `M_cross_A,null = max_S A_cross,null(S)`.

Then:

- `p_cross_R,maxT(S)` = empirical upper-tail p against `M_cross_R,null`;
- `p_cross_A,maxT(S)` = empirical upper-tail p against `M_cross_A,null`.

This tests whether IT2a agrees with the frozen ZL topology more than would an IT2a line-local null, while accounting for eight planned group comparisons.

Spearman and cosine may be emitted as non-promoting sensitivities only.

## 12. Frozen cross-reading topology classes

For each group S:

### `CROSS_READING_TOPOLOGY_REPLICATED`

iff all are true:

- `R_cross >= .70`;
- `p_cross_R,maxT <= .01`;
- `A_cross >= 50/66`;
- `p_cross_A,maxT <= .01`.

The 50/66 sign gate requires at least ~75% of the complete graph to agree in direction.

### `CROSS_READING_TOPOLOGY_RELATED_BUT_REPRESENTATION_MODULATED`

If full replication fails, use this iff:

- `R_cross >= .40`;
- `p_cross_R,maxT <= .05`;
- `A_cross >= 44/66`;
- `p_cross_A,maxT <= .05`.

The 44/66 gate requires at least two-thirds directional agreement.

### `CROSS_READING_TOPOLOGY_DIFFERENT`

Use this only if **both** practical and null evidence are poor:

- `R_cross < .30`;
- `A_cross <= 39/66`;
- `p_cross_R,maxT > .05`;
- `p_cross_A,maxT > .05`.

### otherwise

`CROSS_READING_TOPOLOGY_INCONCLUSIVE`.

This conservative failure rule prevents a middling or merely underpowered result from being mislabeled as true cross-reading difference.

## 13. Gate C — coarser shared-core/modulation geometry replication

#58C's four stable-reference contrasts were:

- section B/H within Currier B;
- section B/S within Currier B;
- section H/S within Currier B;
- interior/final.

Its three modulated-reference contrasts were:

- Currier A/B within Herbal;
- initial/interior;
- initial/final.

These sets are frozen now as a replication target; they are not selected from IT2a.

For IT2a define:

`G_core = median R_Z` over the four stable-reference contrasts.

`G_mod = median R_Z` over the three modulated-reference contrasts.

`Delta_geometry = G_core - G_mod`.

For every independently transformed IT test-null population compute the same seven within-null group correlations and matching `Delta_geometry_null`.

Secondary one-sided empirical p:

`p_Delta = [1 + #{Delta_null >= Delta_real}] / 1001`.

### broad geometry-core support

`GEOMETRY_CORE_SUPPORTED` iff:

1. all seven IT target strata have supported residual existence;
2. none of the seven within-IT contrasts is `DIFFERENT_RESIDUAL_OR_MIXTURE`;
3. at least 6/7 contrasts are either `STABLE_RESIDUAL` or `RELATED_RESIDUAL_BUT_MODULATED`.

### modulation-order replication

`MODULATION_ORDER_REPLICATED` iff:

- broad geometry core is supported;
- `Delta_geometry > 0`;
- `p_Delta <= .05`.

Failure of this secondary modulation-order test does not by itself negate a replicated token-construction core. An independent reading could make formerly modulated strata more uniform while still supporting the manuscript-level core.

## 14. Cross-reading group breadth

After Gate A passes, summarize the seven non-ALL cross-reading group topology classes.

`CROSS_READING_GROUP_CORE_BROAD` iff:

- at least 6/7 non-ALL groups are either `CROSS_READING_TOPOLOGY_REPLICATED` or `...RELATED_BUT_REPRESENTATION_MODULATED`;
- none is `CROSS_READING_TOPOLOGY_DIFFERENT`.

`CROSS_READING_GROUP_CORE_PARTIAL` iff:

- at least 4/7 are replicated/related;
- no more than one is different.

Otherwise group breadth is `CROSS_READING_GROUP_CORE_WEAK_OR_INCONCLUSIVE`.

## 15. Frozen overall #58D classification

Apply in this order.

### A. `ZL3B RESIDUAL GRAPH DOES NOT REPLICATE INDEPENDENTLY`

if either:

1. Gate A fails because `p_exist_IT > .01`; or
2. Gate A passes but pooled `ALL` topology is `CROSS_READING_TOPOLOGY_DIFFERENT`.

Stage A already established adequate source/population support, so these are substantive failures under the tested representation rather than source-availability failures.

### B. `INDEPENDENT-TRANSCRIPTION REPLICATION INCONCLUSIVE`

if:

- Gate A is reliability-inconclusive; or
- Gate A passes but pooled cross-reading topology is inconclusive; or
- required frozen ZL artifact verification fails; or
- required null/fold summaries are invalid; or
- broad within-IT geometry cannot be classified without a substantive difference gate firing.

### C. `INDEPENDENT TRANSCRIPTION REPLICATES RESIDUAL TOKEN-CONSTRUCTION CORE`

iff all are true:

1. Gate A independent IT residual existence passes;
2. pooled `ALL` cross-reading topology is `CROSS_READING_TOPOLOGY_REPLICATED`;
3. `CROSS_READING_GROUP_CORE_BROAD`;
4. `GEOMETRY_CORE_SUPPORTED`.

The secondary modulation-order test is reported separately and is not required for this core replication class.

### D. `RESIDUAL CONSTRUCTION REPLICATES, TOPOLOGY IS REPRESENTATION-MODULATED`

iff all are true and class C did not apply:

1. Gate A passes;
2. pooled `ALL` topology is either replicated or `...RELATED_BUT_REPRESENTATION_MODULATED`;
3. cross-reading group breadth is BROAD or PARTIAL;
4. `GEOMETRY_CORE_SUPPORTED`.

### E. otherwise

`INDEPENDENT-TRANSCRIPTION REPLICATION INCONCLUSIVE`.

No post-reveal edge subset, remapping or threshold change may promote an inconclusive/failing target.

## 16. `max` parser sensitivity — non-promoting

Because 9,492 IT2a tokens have different legal `min` and `max` parses, run a predeclared `max` sensitivity after primary classification.

It may report:

- real pooled/group residual energies under an independently generated max-policy reference calibration;
- physical-leaf residual reliability;
- within-IT seven-contrast residual geometry.

It cannot improve the frozen primary classification and need not receive a second 1,000-test-null confirmatory family.

If max qualitatively reverses the primary sign/topology pattern, report that prominently as representation sensitivity.

## 17. Preflight firewall

Before target reveal, a preflight may reproduce only:

- exact IT2a source hash/header;
- exact 34,411 clean-token source population;
- exact 28,280 accepted-token population under unchanged parser;
- exact 99 leaf universe and five folds;
- exact group/position totals and fold counts from Stage A;
- parser self-tests;
- exact ZL first-reveal archive SHA-256 and JSON structural keys **without reading any IT target pair/residual score**;
- deterministic null seed namespaces and line×slot marginal-preservation tests on synthetic/test data.

Preflight must not calculate any real IT2a pair Q value, residual graph, energy, cross-reading similarity or target p-value.

## 18. First-reveal authorization

The target executable must be committed only after this plan.

A push/preflight workflow must skip the target.

The first authorized target reveal should occur through an explicit later event (preferably opening the target PR or an equally auditable manual workflow event) after:

- plan-before-code ancestry is verified;
- source/population preflight passes;
- exact ZL archive verification passes;
- no target metric has been printed during preflight.

The first result must be archived permanently with:

- exact raw JSON;
- raw SHA-256;
- workflow run/job IDs;
- artifact ZIP digest;
- exact target head SHA;
- report and hypothesis-ledger update.

## 19. Interpretation boundary

Even the strongest positive #58D outcome would establish only that the residual token-construction core is reproducible across an independent manuscript reading lineage inside a common EVA/IVTFF framework.

It would not establish:

- that spaces are natural-language words;
- sentence syntax;
- semantic meanings for slots;
- a plaintext alphabet or cipher table;
- one historical production algorithm;
- semantic presence/absence;
- decipherment.

A successful result would justify the next methodological step: use only the cross-reading replicated token-construction constraints as prospective rejection criteria for reversible/generative/inverse model families, jointly with accepted recurrence and paragraph-entry constraints.