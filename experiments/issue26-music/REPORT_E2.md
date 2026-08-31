# Issue #26E2 — high-resolution and independent-transcription replication

Status: **STRONG GUIDONIAN SLOT REPLICATION**

All three frozen E2 gates pass:

- E2-A higher-resolution ZL replay: **PASS**
- E2-B independent IT2a architecture refit: **PASS**
- E2-C prospective fixed-map IT2a transfer: **PASS**

This is a structural replication of one specific Guidonian-like slot lattice. It is **not** a musical decipherment and does not yet authorize pitch/melody reconstruction.

## 1. Chronology firewall

`PLAN_E2.md` was committed before the E2 executable and before any E2 IT slot-lattice result was calculated.

The most important prospective commitment is E2-C. Issue26E had revealed, only as a post-hoc diagnostic, one max-parser slot10→vox map recurring in 4/5 ZL folds. E2 froze that mapping **before inspecting IT2a under the slot-lattice model**:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`

index tuple in state order `EMPTY,d,l,r,m,n` and vox order `ut,re,mi,fa,sol,la`:

`(0,3,4,1,2,5)`

E2-C did not optimize this six-state mapping on IT.

## 2. Frozen sources

ZL3b:

- mirror commit `315f0cad4de3d021bd4185765c037cf2a28d341c`
- exact Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`

IT2a / Takeshi Takahashi EvaT:

- canonical `voynich.nu` distribution
- exact accepted Phase63B SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`

The workflow downloaded the live canonical IT2a file and required an exact hash match before science. It passed.

The exact five Issue26E physical-leaf fold memberships were reused. No IT-specific fold rebalancing was permitted.

## 3. Replay integrity

Before accepting the 1,000-null extension, E2 reconstructed the first 100 null lattices using the exact original Issue26E labels and asserted the frozen Issue26E summaries.

For both min and max policies, all replay assertions passed exactly:

- parse coverage: pass
- mean Guidonian held-out accuracy: pass
- paired-null median: pass
- empirical p: pass
- fold-null-median win count: pass

Thus E2-A is an extension of the original test rather than a silently altered implementation.

## 4. E2-A — 1,000-null ZL replay

### Primary earliest-valid (`min`) parser

| quantity | E | E2-A 1,000-null |
|---|---:|---:|
| mean parse coverage | 0.769423 | **0.769423** |
| mean Guidonian accuracy | 0.850966 | **0.850966** |
| paired-null mean median | 0.841250 | **0.841215** |
| global advantage | +0.009717 | **+0.009752** |
| global empirical p | 0.009901 | **0.002997** |
| fold median wins | 5/5 | **5/5** |

The observed mean exceeds the 1,000-null 95th percentile `0.846623`.

Per-fold:

| fold | Guidonian A | null median | p_fold |
|---:|---:|---:|---:|
| 0 | 0.824605 | 0.813770 | 0.103896 |
| 1 | 0.855094 | 0.846778 | 0.169830 |
| 2 | 0.832306 | 0.821247 | 0.060939 |
| 3 | 0.863411 | 0.850009 | 0.046953 |
| 4 | 0.879417 | 0.872227 | 0.126873 |

The primary effect remains small and same-direction across all five folds.

### Latest-valid (`max`) sensitivity

- mean parse coverage: `0.769423`
- mean Guidonian A: **`0.843903`**
- paired-null median: `0.817965`
- paired-null q95: `0.827833`
- advantage: **`+0.025939`**
- global empirical p: **`0.000999`**
- fold median wins: **5/5**

Every max fold remains positive; fold p values are:

`0.032967 / 0.045954 / 0.019980 / 0.027972 / 0.025974`

**E2-A: PASS.**

The first positive result is therefore not an artifact of using only 100 matched null lattices.

## 5. E2-B — independent IT2a architecture replication

The complete Issue26E architecture was applied to the independently maintained IT2a/Takahashi EvaT transcription. Twenty morphology clusters and lattice mappings were learned from IT training leaves only.

IT has higher single-unit parse coverage than ZL under the same fresh Zattera parser:

`0.821315`.

### IT earliest-valid (`min`) refit

- mean Guidonian A: **`0.851215`**
- paired-null median: `0.841555`
- paired-null q95: `0.846768`
- advantage: **`+0.009660`**
- global p: **`0.009901`**
- fold median wins: **5/5**

Per-fold Guidonian / null-median / p:

- fold0: `0.836996 / 0.825010 / 0.079208`
- fold1: `0.843698 / 0.826721 / 0.019802`
- fold2: `0.853316 / 0.850526 / 0.366337`
- fold3: `0.861196 / 0.850153 / 0.148515`
- fold4: `0.860871 / 0.853244 / 0.188119`

Again, the primary min result is a small all-fold directional effect rather than five individually significant folds.

### IT latest-valid (`max`) refit

- mean Guidonian A: **`0.840472`**
- paired-null median: `0.815599`
- paired-null q95: `0.823784`
- advantage: **`+0.024873`**
- global p: **`0.009901`**
- fold median wins: **5/5**

Fold p values:

`0.029703 / 0.039604 / 0.019802 / 0.019802 / 0.069307`

The ZL pattern of a small min advantage and materially larger max advantage therefore transfers to an independent human transcription lineage without source-specific retuning.

**E2-B: PASS.**

## 6. E2-C — prospective fixed-map IT transfer

This is the strongest E2 test.

The six-state column mapping was frozen from the ZL post-E diagnostic before IT E2 evaluation:

`EMPTY→ut, d→fa, l→sol, r→re, m→mi, n→la`.

On IT only the 20 morphology-cluster→20 gamut-locus row assignment could fit from training leaves. The six state→vox mapping was not searched. Every degree-matched null lattice was constrained by the same fixed column mapping and could fit only its rows.

### Result

- mean IT parse coverage: `0.821315`
- fixed-map Guidonian A: **`0.833714`**
- paired-null median: `0.728345`
- paired-null q95: `0.757382`
- global advantage: **`+0.105369`**
- global p: **`0.009901`**
- fold median wins: **5/5**

Per-fold:

| fold | Guidonian A | null median | p_fold |
|---:|---:|---:|---:|
| 0 | 0.835597 | 0.744407 | 0.009901 |
| 1 | 0.802178 | 0.694870 | 0.009901 |
| 2 | 0.870536 | 0.784120 | 0.009901 |
| 3 | 0.848460 | 0.730211 | 0.009901 |
| 4 | 0.811799 | 0.726153 | 0.029703 |

The prospective fixed-map advantage is about **10.54 percentage points**, much larger than the original freely refitted min-policy effect. This cannot be attributed to choosing a favorable six-state→vox mapping on IT because that degree of freedom was removed before reveal.

**E2-C: PASS.**

## 7. Frozen classification

- E2-A high-resolution replay: pass
- E2-B independent IT architecture replication: pass
- E2-C prospective fixed-map IT transfer: pass

Frozen classification: **`STRONG GUIDONIAN SLOT REPLICATION`**.

## 8. What this now supports

The defensible statement is narrower than “Voynich is music” but materially stronger than Issue26E alone:

> In two independent EVA-family human transcription lineages, a six-state factor singled out by the independently published Zattera slot grammar and a sequence-blind twenty-class representation of the remaining token morphology generalize to the specific 20-locus×6-vox Guidonian admissibility lattice better than degree-matched non-Guidonian lattices under matched training freedom. The original ZL signal survives a tenfold null-resolution increase, and a six-state→vox correspondence frozen from ZL prospectively transfers to IT with a large held-out advantage.

This is a **replicated coding-structure result**.

It still does not establish:

- that slot10 states literally mean the named six voces;
- that the 20 morphology clusters are actual pitches or are in pitch order;
- that running text is a melody;
- rhythm, duration, mode, instrument or polyphony;
- semantic plaintext;
- that the manuscript author used the Guidonian hand rather than some non-musical formal system with the same lattice geometry.

## 9. Main remaining alternative explanation

The next serious null is no longer “random degree-matched lattice.” The Guidonian lattice has additional **ordered / overlapping / nested neighborhood geometry** generated by overlapping hexachords. Voynich token slots are themselves an ordered combinatorial grammar.

Therefore a non-musical ordered grammar could potentially produce the same advantage even though ordinary degree-preserving rewires do not.

The next test should ask:

> Does the Voynich result prefer the *specific Guidonian overlap geometry* over non-musical ordered/nested 20×6 lattices that preserve not only row/column degrees but comparable neighborhood overlap, interval/run structure and nesting?

That is the correct next falsification target before any melody or mutation-sequence analysis.

## 10. First-reveal provenance

- PR: `#32`
- scientific head: `6b313391bb0f10f5677758668ee1d4fe39b7e748`
- Actions run: `33356233986`
- job: `99378839395`
- artifact: `9745353368`
- artifact ZIP SHA-256: `23c882d49acdc0104b9e7f3d644ee7701d778c8e20fbd01b5b3ee0af6a8d6f05`
- raw JSON SHA-256: `d408699254041596c7a25f68238b7c50e31111a1bb612d87b56ad23725b6440d`
- plan SHA-256: `f64f4b9bbbff1bee89720c76d7d83d4626f41413d66bd5c37585db604d568b01`
- core SHA-256: `3e37c0223497f7008cb9d78ceeab18b34518c0c0b70860528a2017502fc1392d`
- E2 script SHA-256: `1f64a5e34582bf2d66ab656520c729168e8d4abcd7a8b28ead62f525d25af8df`
- IT2a SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
