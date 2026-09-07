# Issue #165 — section/domain source-attribution Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

No real-target section-conditioned probability, likelihood, `G_section`, `G_placebo`, or scientific classification was computed.

## Frozen chronology

- branch entry main: `72ff98da2eac4b830dd02eae7623577362c29150` (Issue #161 science merge);
- section/domain plan committed at `4652540f98d6aa6a103fbad3d66730b5f5c1d67e`, plan blob `d334092e6c7cd38f76deb48250fa09d8f9468064`;
- score-free scientific Gate implementation committed separately at `e1bc8c30917abc0d991a0cb7abe270c844d5841d`, Gate blob `adaca5dc387d58542044089aac5faaedc8880ccf`;
- initial workflow added afterward at `a6aee89a3b79ef6927e25940e0c24527b92bcddf`;
- initial Gate run `34078048402` stopped before accepting any section science because the plan/Gate had copied an incorrect Issue #107 artifact SHA. It emitted `gate_pass:false`, `scientific_section_metrics_computed:false`, and no `G_section`, `G_placebo`, or classification;
- the original Issue #107 artifact `9985775083` was re-downloaded. Its `phase3b_metadata_gate0.json` bytes hash to `8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717`, exactly matching current recomputation by the frozen #107 scanner;
- additive pre-Gate correction note committed at `25e958357974219518bdd5846487322ee0d84771`, blob `01a0c669de59ba43974566e171616682cc5c64f2`;
- authority-only wrapper committed at `c48d7a1b0f05852b0d76d0473ed640452084092f`, wrapper blob `8ad582bdea2351606e97e52c0ee733999c11820f`;
- the wrapper verifies the original Gate blob and correction-note blob, changes only the copied Issue #107 result SHA, then executes the original frozen Gate implementation;
- workflow rerouted to that wrapper at `f91842fc17b242d885ace6a2628fd3bec9a4901f`;
- corrected Gate run `34078255469` completed SUCCESS.

The scientific section rules, candidate levels, pure-leaf rules, support thresholds, deterministic placebo, model family, pass rule, and class set were not changed after any target section score because no such score existed.

## Authoritative score-free result

- workflow: `Issue165 section/domain source-attribution Gate0`
- run: `34078255469`
- exact Gate head: `f91842fc17b242d885ace6a2628fd3bec9a4901f`
- conclusion: `success`
- artifact ID: `10002824741`
- artifact ZIP digest: `sha256:ff5ab0d3ae33d098f3caf21d16f5420e775a79e7c12bf000ee89f725ce1a58b4`
- result JSON SHA-256: `3b6eededdfe197ed9152b9b0f756dffe34870eaf1a33b810d7e23f84d0d84f1a`

Gate disposition:

> **`PASS — PROCEED TO SEPARATELY COMMITTED SECTION/DOMAIN SCORER`**

## Reproduced authority

The Gate reproduces and pins:

- Issue #161 Gate result SHA-256 `32af814ddec529d5e255ae5bede00e93e989aad5b36a70f9abe34ffed839bd94`;
- Issue #161 Gate script blob `00e5bddc0484b9472bb4fce9dadb89dd52bf578f`;
- Issue #161 Gate provenance blob `67e91ba26a76898f679a5182828ab3e9f512d49a`;
- Issue #161 scientific scorer blob `d24149977770118505f2147c5aa2bb727631906f`;
- Issue #161 first-reveal provenance blob `73100548fef5dbc0d08a1951e3c0ca5b370cd6f4`;
- Issue #161 first-reveal result SHA-256 `11e179abcc53e5507d188b46f335c38198ee6a9d36f31fee406650610cafd031`;
- Issue #107 metadata scanner blob `110a6b848df71c4f51ec0d9dd3b262039d1fc66f`;
- corrected Issue #107 metadata result SHA-256 `8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`;
- Issue #165 plan blob `d334092e6c7cd38f76deb48250fa09d8f9468064`.

## Pure physical-leaf metadata authority

Candidate `$I` levels remain the complete prospectively frozen set:

`A, B, C, H, P, S, T, Z`.

The Gate classifies a physical leaf as pure only if all token-bearing mapped ZL3b loci resolve to one non-special metadata level.

- pure-I leaves: `92`;
- pure-I leaf-map SHA-256: `47ab536c6806eca5b037bc8cf81bae11069a153c92e4d17162c6381c92025eb1`;
- pure-H leaves: `98`;
- pure-H leaf-map SHA-256: `88e3071a7c8c05d8e0791f24a7a7edfbc19a0c9f59668cd980ad1054a9b7540f`.

Mixed or unresolved leaves remain excluded from section science.

## Frozen section eligibility

Thresholds:

- >=5 pure physical leaves in the Currier×section population;
- >=300 accepted common-EVA primary run-body targets in >=4/5 folds in ZL3b;
- same >=300 in >=4/5 folds in IT2a;
- >=2 eligible section levels required before a Currier regime is scientifically scorable.

### Currier A

Only `I=H` is eligible:

- pure leaves: `46`;
- ZL3b run-body targets by fold: `[802,469,851,660,516]`;
- IT2a: `[1065,611,1073,865,739]`.

Because A has only one eligible section level, **Currier A is `UNSCORABLE_BY_FROZEN_SUPPORT`** for section/domain attribution. No A section score is licensed.

### Currier B

Exactly two levels are eligible, so **Currier B is scorable**.

`I=B`:

- pure leaves: `9`;
- ZL3b targets `[774,709,857,855,292]` — threshold in 4/5 folds;
- IT2a `[951,897,1142,1097,367]` — threshold in 5/5 folds.

`I=S`:

- pure leaves: `12`;
- ZL3b `[1027,1013,1714,1555,923]` — 5/5;
- IT2a `[1344,1301,2151,1971,1167]` — 5/5.

Therefore the scientific target population is frozen to the union of pure `Currier B × I=B` and `Currier B × I=S` run-body primary targets, separately in each reading and outer fold.

## Scribe identifiability

Frozen Gate classification:

> **`SCRIBE_NOT_IDENTIFIABLE`**

No Currier×eligible-section cell contains two Davis-hand levels that independently meet the same >=300 in >=4/5 folds criterion in both readings. `licensed_cells=[]`.

No scribe predictive model is licensed by Issue #165.

## Deterministic section-label placebo

Only Currier B is scorable. For each outer fold, eligible training leaves are sorted by ascending physical leaf id and their actual section-label sequence is left-cyclically shifted by exactly one leaf.

The mapping changes labels on exactly 2 leaves in every fold; it is therefore non-degenerate without any searched permutation.

Frozen B placebo-map identities:

| fold | training leaves | changed leaves | map SHA-256 |
|---:|---:|---:|---|
| 0 | 17 | 2 | `f3907a8ae5d6aadd1d25da15bee8f3d44807aa84e379fc852cff86b723269836` |
| 1 | 17 | 2 | `582534ab378a04406cb61ebdca71f875e9f4e875505e89f072373878b4120797` |
| 2 | 16 | 2 | `1c7e39cecd4f3860de695b1c597c03ac58b0656430ce0cb0189e39f641820269` |
| 3 | 16 | 2 | `143abb7eb754d465bb11ff872d3ab02f44c70c73fb61d25d96fe571ade47c48c` |
| 4 | 18 | 2 | `0e47dda8c617f911fafd4dd603d08906bc59ef0d211e3e3fa8727d46049ee41e` |

Currier A has no placebo map because it is unscorable.

## Leakage and synthetic controls

- training-union ∩ held-out physical leaves is empty in all five folds;
- synthetic pure-I and pure-H rules pass;
- synthetic mixed/special exclusion passes;
- the frozen one-leaf-left placebo rotation passes;
- no real-target section likelihood is used by the synthetic test.

## Firewall

The Gate artifact records false for all section-science/tuning flags:

- real-target section probability or likelihood;
- `G_section`;
- `G_placebo`;
- scientific classification;
- held-out target outcome selection;
- mixed/unresolved scoring;
- scribe fitting;
- placebo search/repetition;
- Currier/fold/representation/#161 model changes;
- section×previous-terminal interaction;
- latent-state fitting;
- S1/S2/H62/R1 tuning.

## Consequence

The only allowed next sequence is:

1. merge this Gate0 authority;
2. branch from post-Gate main;
3. commit a scientific scorer separately, pinned to this exact result/wrapper/original Gate/provenance/plan;
4. score **Currier B only**, with target sections `I=B` and `I=S`;
5. compare the real section×outcome model against both the #161 Currier-only compact model and the frozen deterministic shifted-section placebo;
6. do not fit any scribe model.

Refs #84 #88 #107 #109 #161 #164 #165 #166.
