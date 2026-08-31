# Phase 66C — illustrated-flora body-text calibration report

Status: **BODY-TEXT CALIBRATION COMPLETE; IMAGE↔BODY CONTROL PREREGISTERED SEPARATELY**

## Question

Would a genuinely meaningful illustrated botanical book necessarily produce the kind of short-label surface-form relation tested in Phase65B/66B, or can the depicted morphology instead be carried by the accompanying prose?

## Control source

Catharine Parr Traill (botanical descriptions) and Agnes FitzGibbon (paintings/lithographs), *Canadian Wild Flowers* (1868), cross-checked against the 1869 *North American Wild Flowers* reissue. The 1868 preface states that the descriptions were selected/adapted to the plants delineated in the plates.

The fixed control population contains 24 illustrated species from Canadian Plates I–VII. No entry was dropped for sparse or inconvenient prose.

## Frozen audit

Before the complete 24-entry audit, `PLAN_C.md` fixed a literal text-only rule.

The primary morphology categories were exactly the three Phase66A characters that survived the Voynich eligibility firewall:

- leaf composition
- leaf arrangement
- leaf margin

Extended audit categories were leaf shape, venation, stem architecture, root/subterranean form, reproductive architecture, and reproductive color.

A prose feature counted only when the species entry explicitly stated it. Illustration/species knowledge could not fill missing prose. Latin-binomial names were audited independently under a literal-string rule without importing Latin etymology.

## Result

Across the 24 fixed species:

| calibration quantity | result |
|---|---:|
| body prose explicitly states >=1 of the three primary morphology categories | **14/24 = 58.3%** |
| stricter direct mapping to at least one frozen Phase66 state | **13/24 = 54.2%** |
| body prose states >=1 extended morphology/color category | **24/24 = 100%** |
| literal Latin binomial explicitly states a primary morphology category | **0/24 = 0%** |
| body-minus-name primary availability difference | **+58.3 percentage points** |

Broad explicit primary coverage by character:

- leaf composition: 4/24
- leaf arrangement: 8/24
- leaf margin: 8/24

The exact per-entry evidence and stricter state-mappability flags are archived in `BODY_AUDIT_C.json`.

## Representative source behavior

This is not driven by one or two cherry-picked descriptions. Across the fixed population the prose includes, among other things:

- clustered/basal or whorled leaves;
- divided/leaflet-bearing leaves;
- lobed, toothed, waved or scalloped margins;
- lanceolate, ovate and sword-shaped leaf descriptions;
- many-nerved leaves;
- bulbs, corms, tubers, fibrous roots and running root-stalks;
- simple versus branching stems;
- racemes, spikes, panicles, solitary flowers and terminal heads;
- explicit flower/bract coloration.

The coverage is imperfect for any one narrow character, but morphology is pervasive when the whole botanical description is considered.

## Main calibration conclusion

The user's proposed distinction is supported by this control:

> In a known meaningful illustrated botanical work, depicted morphological information is frequently expressed in the **body description**, while the short plant-name string need not literally encode those morphological features at all.

This materially changes how the Phase65B/66B negatives should be read.

Phase65B and Phase66B are valid negative tests of their preregistered hypotheses, but they are **not generic detectors of image↔text semantics**. They primarily constrain a much narrower model in which similar/attribute-similar depicted plants induce similar **short attached label surface forms**.

A genuine image↔plant-name relation can exist without that condition, and a descriptive body text can carry morphology much more directly.

## Consequence for the Voynich program

Retain:

> Phase65B/66B found no prospective evidence that plant morphology/color is coupled to the surface structure of the short attached labels under the tested representations.

Do not promote this to:

> Plant morphology is not encoded anywhere in the associated Voynich text.

or:

> The labels/text lack semantic botanical content.

The appropriate next content test is therefore not another repair of short-label string similarity. It is a separately frozen **categorical encoding / morphology-description test**, preferably against text units that are long enough to plausibly contain descriptive features.

## Next control

`PLAN_D_IMAGE_BODY.md` was frozen after the body-availability result and before control image-side coding. It will test whether the same fixed Phase66 categorical states read from the historical illustrations agree with states explicitly recoverable from their paired prose more often than under description reassignment.

Because the same runtime has already read the body descriptions, that image↔body stage is explicitly labelled calibration rather than independent confirmation.
