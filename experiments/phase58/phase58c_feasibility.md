# Phase 58C — localized paragraph-to-object linkage feasibility

## Decision

**BLOCKED / NOT IDENTIFIABLE FROM CURRENT AUTOMATIC SOURCES WITHOUT ADDING A NEW ANNOTATION LAYER.**

This is a methodological stop for this branch, not a project stop.

## Sources inspected

External visual resources were inspected after the Phase58B page-level tests:

- `geoffitect/voynich:data/visual/object_catalog.json`
- `geoffitect/voynich:data/visual/segmentation_data.json`
- `geoffitect/voynich:data/lexicon/figure_database.json`

The object catalogue provides image bounding boxes and coarse nearby-text-region counts, but its `lexicon_matches` are text-derived and therefore cannot serve as independent semantic ground truth. The segmentation file provides Vision-detected text-region boxes, but these are sparse image detections and are not mapped to ZL3b paragraph identifiers. The transcription gives paragraph/line order but not image coordinates.

## Why no automatic pairing is accepted

A rule such as 'assign each object to the nearest detected text region and then assign transcription paragraphs by top-to-bottom order' would introduce several unvalidated assumptions at once:

1. detected text regions are incomplete and do not correspond one-to-one to prose paragraphs;
2. image coordinate orientation/layout differs across illustration types;
3. many pages have text wrapping around illustrations rather than simple vertical blocks;
4. choosing the pairing that maximizes residual/content association would be circular semantic fishing.

Therefore Phase58C cannot currently produce a defensible prospective paragraph-to-object test.

## What would unblock it

Create an independent annotation table with at minimum:

`page_side, paragraph_id, image_bbox_or_polygon, linked_object_id, linkage_rule, annotator_confidence`

The annotator must not see residual coordinates or proposed decipherments. A second annotator or deterministic geometry rule should be used for an agreement audit.

## Consequence

Phase58B's page-level visual nulls stand. Localized semantics remains untested rather than failed.

Because Phase58D was frozen to occur only after a valid 58B/58C content relation, **do not launch a flexible cipher search now**. Move instead to mechanism discrimination: ask whether the structural/residual phenomena that survived Phases56–57 are reproduced by meaningful prose, bounded ciphers, or formal generators under the same analysis pipeline.
