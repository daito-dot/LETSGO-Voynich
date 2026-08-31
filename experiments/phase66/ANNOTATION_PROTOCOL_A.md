# Phase 66A — frozen image-only annotation protocol

Status: **FROZEN BEFORE P25 ANNOTATION**

Companion files:

- `PLAN_A.md`
- `ANNOTATION_SCHEMA_A.json`

## Scientific firewall

This protocol is an image measurement procedure, not an interpretation exercise.

During annotation the annotator/model MUST NOT receive or retrieve:

- Voynich transcription;
- visible label glyphs if they can be excluded from the crop;
- label text identifiers that encode transcription content;
- Phase65B visual/text distances or outcomes;
- another P25 object for side-by-side comparison;
- candidate plant names;
- proposed glyph meanings.

The only scientific inputs are one frozen object crop and a neutral object ID.

## Exact instruction

The following instruction text is frozen verbatim for all scientific annotation passes:

---BEGIN FROZEN INSTRUCTION---
You are performing botanical descriptive character coding from a single historical plant drawing. This is measurement, not identification.

Use only directly visible geometry in the supplied crop. Do not identify the plant, infer a species, infer missing anatomy, use historical context, compare it with other drawings, judge overall similarity, or reason about any writing or label.

For every field, choose exactly one state permitted by ANNOTATION_SCHEMA_A.json. If the relevant structure is absent, cropped, ambiguous, too stylized to distinguish the permitted states, or the defining attachment/transition is not visibly resolved, output U. U is preferred to inference.

Important distinctions:
1. Code depicted form, not presumed real anatomy.
2. Do not infer leaf arrangement from overall symmetry; use visible attachment positions.
3. Do not infer compound leaves unless leaflet attachment supports it.
4. Do not treat drawing damage, pigment gaps, or line wobble as leaf-margin teeth.
5. Do not treat leaf petioles as stem branches.
6. Do not identify a flower solely from color.
7. For root/subterranean states and venation states ending in _like, the state means only that the drawing visibly resembles that geometry.
8. Evidence notes must be short and describe only visible geometric evidence. Never use taxon names, semantic interpretations, label/glyph references, or similarity claims.

Return only one JSON object conforming to ANNOTATION_SCHEMA_A.json. Do not add fields or alternative states.
---END FROZEN INSTRUCTION---

## Input construction

For each retained Phase65 object:

1. regenerate/verify the frozen crop using the Phase65 manifest and SHA256 provenance;
2. ensure the scientific image supplied to annotation contains the plant drawing region defined by the frozen crop and does not deliberately expand toward label text;
3. pass only `object_id` plus the image;
4. do not expose page transcription or text-side tables in the annotation context.

No crop boundary may be changed because a morphology state is difficult to classify. If the frozen crop does not show the required structure, use `U`.

## Pass policy

Scientific annotation uses three independent passes under identical inputs and the identical frozen instruction/schema.

- Passes: A1, A2, A3.
- No previous pass output is shown to a later pass.
- No conversational memory of earlier classifications may be supplied intentionally.
- Temperature/randomness controls, if exposed by the execution system, must be set to their lowest deterministic setting and recorded.
- Model/provider/version identifiers exposed by the runtime must be recorded verbatim.

For each field/object:

- 3/3 agreement -> retain state;
- 2/3 agreement -> retain modal state;
- no 2/3 agreement -> `U`.

This aggregation is automatic. There is no human adjudication.

## Failure/retry policy

A retry is permitted only for a technical failure:

- malformed/non-JSON output;
- missing required field;
- state outside frozen enum;
- image failed to load;
- provider/runtime error.

A scientifically valid but uncertain output (`U`) is never a retry reason.

Maximum technical retries: 2 per pass/object.

A retry receives the same image and same frozen instruction. It must not include coaching such as "look more closely at the root" or reveal why validation failed beyond machine-readable schema compliance.

If still technically invalid after 2 retries, that pass is `TECHNICAL_FAIL`; it cannot be manually repaired. If fewer than 2 valid passes remain for an object, the affected scientific fields are `U` for eligibility purposes unless the whole run is declared blocked before any text-side reveal.

## Evidence-note policy

Evidence notes are audit metadata only. They are never transformed into text features or used as scientific predictors.

Examples of allowed note content:

- "three leaves attach at one visible node"
- "blade edge shows repeated rounded projections"
- "several thin axes emerge from the basal region"

Forbidden:

- "looks like mint"
- "similar to object X"
- "probably medicinal"
- "label may name the root"

## Sealing rule

After A1/A2/A3 are complete:

1. archive every raw pass;
2. aggregate mechanically;
3. compute observability/state-count/stability diagnostics only;
4. publish the morphology table and eligibility report;
5. commit their hashes;
6. only then design/freeze the text-feature extraction and association statistic.

No Voynich label feature may be computed against morphology before step 5.

## Stop conditions

Phase66A is blocked rather than repaired if:

- crop provenance cannot be reproduced;
- annotation inputs cannot be kept label-blind;
- model identity/runtime cannot be recorded sufficiently for audit;
- a material protocol defect is discovered after P25 annotation starts.

If a material protocol defect is discovered after annotation starts, archive the run as invalid and start a newly versioned preregistration. Do not silently edit this protocol and continue.
