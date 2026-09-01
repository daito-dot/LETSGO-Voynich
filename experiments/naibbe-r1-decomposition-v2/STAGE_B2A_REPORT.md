# Issue #72 V2 — Stage B2a extended positive-control support report

Status:

> **`UNCHANGED_NAIBBE_REP5_REP24_SURFACES_FROZEN`**

Stage B2a is target-blind. It freezes the exact twenty additional unchanged published-Naibbe realizations required by `STAGE_B2_POSITIVE_CONTROL_EXTENSION_PLAN.md` before any of their R1 quantities are calculated.

## 1. Population rule

The complete population is exactly:

`rep5, rep6, ..., rep24`

using the direct continuation of the historical Phase64B seed schedule:

`seed(manuscript_index, rep) = 6480000 + 100*manuscript_index + rep`.

No realization was dropped, replaced, rerolled, or selected from parser coverage or R1 behavior.

## 2. Target firewall

At completion of Stage B2a:

- no slot-pair Q was computed for rep5..rep24;
- no residual Z/E/W was computed;
- ZL3b/#58C and IT2a/#58D target residual vectors were not loaded;
- no target topology/sign agreement was computed;
- no R1 p-value was computed;
- no Issue #72 intervention surface was generated;
- no EL/ES/ET/EG/PT/FI R1 quantity was computed.

This remains a prospective positive-control extension.

## 3. Parser-support result

Coverage is descriptive only; there is no hard cutoff.

Across the twenty new unchanged realizations:

- minimum coverage: `0.8832444987047018` (`rep20`);
- maximum coverage: `0.8898070806456407` (`rep11`).

This is the same narrow high-support regime already observed for historical `rep0..rep4` (`0.885210–0.888162`). Nothing in B2a suggests that the extended positive-control population moved into a qualitatively different representation regime.

| rep | coverage | visible | parsed | pooled primary SHA-256 |
|---:|---:|---:|---:|---|
| 5 | 0.888154 | 33,698 | 29,929 | `c35c2d2ea150d35f1c41dd6eae7ca4acc59677f62458d468f657b047d0ea2ce3` |
| 6 | 0.886130 | 33,591 | 29,766 | `ab519bab773c3a0d22bfed68b83359791220e8a7eb1442fc2548c4c26581f077` |
| 7 | 0.886491 | 33,495 | 29,693 | `2e840787763241d664330a661d380dc9c62635f050ece9a41c4b979697eab081` |
| 8 | 0.885147 | 33,556 | 29,702 | `dc1f011b1b878e891f8c87db007564b1aa46d0d3d9a173bc4ab88f6d0f93d785` |
| 9 | 0.887203 | 33,680 | 29,881 | `61332ce8d1fd4d86a30539c5169ee3ba5cd0e60d016d3a48c13c891774dc4d03` |
| 10 | 0.885040 | 33,603 | 29,740 | `e592a1ddc78be6a14c3a63b434fcd1d4053039a0e761a82b0e25f1e4cc2ff1e5` |
| 11 | 0.889807 | 33,641 | 29,934 | `88916273ba63745c5a78d41bf1d44230a0b7a5280fbfc4684dcfff082b57f6ab` |
| 12 | 0.884291 | 33,567 | 29,683 | `0ceac77eb60f0153f344217c5335adf7749c42bd82e8c35ef10b4ec7e2efffb8` |
| 13 | 0.886108 | 33,523 | 29,705 | `edb1d4effa35f6bd74b70b6a7998b975cd9dedb4eb5984b33c4e960c6d23b3a4` |
| 14 | 0.887307 | 33,649 | 29,857 | `dcd9fe09af4269e443035052157c0c7499c9ab3b878c8fafc6ea7658ad241599` |
| 15 | 0.887431 | 33,695 | 29,902 | `14d39a81659f7d4d3e7a3f18cb4f170cab39f61598a8a96755fec1e74ee58150` |
| 16 | 0.887040 | 33,649 | 29,848 | `0d314a754dbcb6855a7ea40ec1b87a4650ada97b38fa9a9887201f3953e44063` |
| 17 | 0.883534 | 33,512 | 29,609 | `ac024646efb582f797d5a4a01cb28d11ba2e1d676640de050318eef27c02e431` |
| 18 | 0.887019 | 33,519 | 29,732 | `b9fee1a630e9223de6e8cb4eec273d389cc479aa54df9a1ca2917470faf2def3` |
| 19 | 0.885700 | 33,447 | 29,624 | `2b5b6ffd9f7421fc3f17a8958fa056de7862d712623a1f3cc7421289451ec600` |
| 20 | 0.883244 | 33,583 | 29,662 | `e1b2be4d2089683863999cc019eceb7e2e0b38e9437385171e1e6b5233f4217f` |
| 21 | 0.886092 | 33,448 | 29,638 | `d09116d218bc475e0ace48ba9fe94e5f3a3d10ccc7cf85c5ff04b61943df5742` |
| 22 | 0.888869 | 33,582 | 29,850 | `defbfff8d019c67834ee3f27e4d4192c6666297dbaf5317a08e2ecac497184ef` |
| 23 | 0.886668 | 33,618 | 29,808 | `d3ceffce6bed6c2877525c9731aa7f586d69dbbfe91677828ed9297819736a39` |
| 24 | 0.885163 | 33,639 | 29,776 | `4dea86009482ca9fad187233a6e5768ff1c80de00a92d08cd18a396883de2609` |

## 4. Scientific interpretation

B2a establishes only that the twenty predeclared additional unchanged-Naibbe executions are mechanically available and remain strongly compatible with the common 12-slot representation.

It does **not** establish that their R1 graphs match Voynich. That is the separately authorized B2b measurement.

The key methodological point is population closure:

> **All twenty identities were frozen before their R1 behavior was available.**

Therefore the expanded positive-control distribution cannot later be narrowed to remove inconvenient weak realizations.

## 5. Provenance

See `STAGE_B2A_PROVENANCE.md`.

Primary raw authority:

- run `33465227714`;
- artifact `9784609004`;
- raw `stage_b2a_support.json` SHA-256 `1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c`.

A permanent exact compressed/base64 copy is stored under `archive/`.

## 6. Next authorized step

Stage B2b may now score **only these exact rep5..rep24 surfaces**, using the same R1 coordinate system calibrated in Stage B1.

It must still not generate or score any Issue #72 intervention.

After B2b, `rep0..rep24` form the 25-realization T2 positive-control population used to calibrate the scale of unchanged-mechanism variation before the intervention randomization design is finalized.
