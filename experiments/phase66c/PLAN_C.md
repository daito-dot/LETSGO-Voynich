# Phase 66C — illustrated-flora positive-control calibration

Status: **FROZEN BEFORE 24-ENTRY BODY-TEXT AUDIT**

Base main: `21ca553d0dc7f5e203465d08ae606b4c43305817`

## Motivation

Phase66B returned no detected relation between frozen depicted botanical attributes/color and short attached Voynich label structure. That negative result is only informative if the detector is calibrated against material where a botanical image and its prose are known to be semantically related.

This control asks a narrower question first: in a genuine illustrated botanical book, do prose descriptions explicitly state the same kinds of morphological characters that Phase66A measured from images?

## Control source

Catharine Parr Traill and Agnes FitzGibbon, *Canadian Wild Flowers* (1868), public-domain HTML transcription with illustrations at Project Gutenberg Canada.

The source explicitly presents botanical descriptions paired with illustrated plants. The 24-entry population is fixed prospectively as all individual species represented in Plates I–VII, splitting the two separately illustrated yellow lady's-slipper species in the shared entry.

## Frozen population (24 species)

1. Arum triphyllum
2. Orchis spectabilis
3. Castilleia coccinea
4. Rudbeckia fulgida
5. Pyrola elliptica
6. Moneses uniflora
7. Rubus odoratus
8. Veronica americana
9. Erythronium americanum
10. Trillium grandiflorum
11. Aquilegia canadensis
12. Dicentra canadensis
13. Trillium erectum
14. Geranium maculatum
15. Trientalis americana
16. Cypripedium parviflorum
17. Cypripedium pubescens
18. Iris versicolor
19. Vaccinium oxycoccus
20. Lilium philadelphicum
21. Campanula rotundifolia
22. Cypripedium spectabile
23. Rosa blanda
24. Pentstemon pubescens

No species may be removed because its description is inconvenient or sparse.

## Lane C0 — morphology availability in prose

Audit the body description for explicit statements corresponding to the same three Phase66A morphology characters that survived the Voynich image-side eligibility firewall:

- `leaf_composition`
- `leaf_arrangement`
- `leaf_margin`

Additionally record explicit mention coverage for:

- leaf shape
- venation
- stem branching/architecture
- root/subterranean form
- reproductive architecture
- flower/reproductive color

A character is `explicit=true` only when the species entry directly states a morphological property or uses an unambiguous botanical descriptor for it. Inference from species identity, genus knowledge, or the illustration is forbidden in this text-only audit.

For the two Cypripedium species sharing one prose entry, a statement counts for a species only when the text explicitly assigns it to that species or explicitly describes both species jointly. Species-specific statements must not be copied to the other species.

## Lane C1 — name-only comparison

For each of the same 24 species, repeat the audit using only the printed Latin binomial. The expected scientific point is not that Latin names contain zero information in principle, but whether the literal name string explicitly states the frozen morphology characters.

## Primary calibration quantities

Predeclared outputs:

1. `body_any_primary_morphology_rate`: fraction of 24 species for which body prose explicitly states at least one of leaf composition / arrangement / margin.
2. `body_primary_character_coverage`: number and fraction of species with an explicit statement for each of the three characters.
3. `body_any_extended_morphology_rate`: fraction with at least one explicit statement among the nine audited morphology/color categories.
4. `name_any_primary_morphology_rate`: same as (1) using only the Latin binomial.
5. paired difference `body_any_primary - name_any_primary` over the 24 matched species.

No p-value is required for the basic availability audit because this is a deterministic corpus-description quantity, not a sampled population inference. If an inferential matched test is later added, it must be preregistered before computation.

## Interpretation

If body prose frequently contains explicit morphology while names do not, then a semantically related illustrated flora can encode depicted attributes in **body text without producing short-name string similarity**. This would narrow the interpretation of Phase65B/66B negatives and motivate a new Voynich test aimed at categorical/semantic feature encoding rather than global string resemblance.

This control does not prove that Voynich labels are prose, names, or meaningful. It calibrates what the prior detector can and cannot be expected to detect.

## Contamination disclosure

Before this freeze, a few source excerpts were inspected while choosing the control source, including examples for Dicentra canadensis, Geranium maculatum, Iris versicolor, Lilium philadelphicum, and Cypripedium spp. Therefore this is not a blinded source-discovery exercise. The fixed 24-species population and all-entry audit prevent choosing only examples known to contain morphology after inspection.
