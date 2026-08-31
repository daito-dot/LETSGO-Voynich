# Phase 66A — morphology-first annotation preregistration

Status: **FROZEN DESIGN BEFORE ANY PHASE66 IMAGE ANNOTATION OR LABEL-FEATURE COMPUTATION**

Parent main: `61cb3905eb88a4cec77e8f6e62fe89bae9d9eda1`

## 1. Question

Phase65B found no detectable relation between whole-crop DINOv2 visual distance and generic label-form distance on either the primary or replication page.

Phase66 asks a different question:

> Do independently predefined botanical-morphology characters of the depicted plant fragments predict any predeclared structural feature of their physically attached Voynich labels?

This is not a retry of whole-image similarity. It decomposes the image into explicit botanical descriptive characters before any label-side association is inspected.

## 2. Non-negotiable separation

Before any Phase66 annotation:

- do not inspect the Voynich label strings while assigning image characters;
- do not inspect any image↔label score;
- do not add, delete, merge or redefine a morphology character because of label behavior;
- do not use free-form judgments such as "looks similar", "same kind", "probably related", "same plant" or "different species";
- do not identify a historical plant taxon as part of the primary annotation;
- do not use Phase65B DINO distances to guide morphology coding.

The annotation input is image-only. The annotation output is a fixed character/state table.

## 3. External descriptive framework

The schema is based on external botanical-description practice rather than traits invented from Voynich images.

Structural data model:

- DELTA (DEscription Language for TAxonomy): taxonomic descriptions encoded as explicit characters and states;
- TDWG SDD: structured descriptive data for taxa/specimens.

Terminology references:

- Flora of North America Categorical Glossary, especially the categories `arrangement`, `architecture`, `apex`, `base`, `margin`, `shape`, `venation`, and `structure`;
- Kew Plant Glossary as a secondary terminology cross-check.

These references define vocabulary. They do not imply that the Voynich drawings are taxonomically accurate or that a depicted organ can always be identified.

## 4. Observation principle

Code **what is visibly depicted**, not what the plant "must really be".

For every character, one of the permitted outputs must be used. `U` means unobservable/uncertain under the frozen rule and is a valid result, not a prompt to improvise.

No state may be inferred from another state. Example: if a leaf base is not visible, do not infer it from overall blade shape.

## 5. Primary morphology character set

Only characters expected to be visually observable in small pharmaceutical plant fragments are admitted to the primary lane.

### M01 organ visibility

Question: which major vegetative/reproductive structures are visibly represented?

Separate binary fields:

- `leaf_visible`: 0/1/U
- `stem_axis_visible`: 0/1/U
- `root_or_subterranean_visible`: 0/1/U
- `flower_or_inflorescence_visible`: 0/1/U
- `fruit_or_seed_body_visible`: 0/1/U

This is depiction-level coding only.

### M02 leaf composition

Applicable only when at least one leaf unit is sufficiently visible.

States:

- `simple`
- `compound_pinnate`
- `compound_palmate`
- `deeply_divided_uncertain_leaflet_status`
- `U`

Do not force a compound/simple decision when leaflet attachment is not visible.

### M03 leaf arrangement on visible axis

States:

- `alternate`
- `opposite`
- `whorled_3plus`
- `basal_or_rosette`
- `single_or_insufficient_nodes`
- `U`

A state is assigned only from visible attachment positions, not from apparent overall symmetry.

### M04 dominant leaf-blade shape

Primary coarse states, chosen to avoid fragile fine distinctions in stylized drawings:

- `linear_or_very_narrow`
- `lanceolate_or_elliptic_narrow`
- `elliptic_or_ovate_broad`
- `obovate_or_broader_distally`
- `orbicular_or_suborbicular`
- `cordate_or_sagittate_base_dominant`
- `lobed_or_divided_shape_dominant`
- `heteromorphic_no_single_dominant_state`
- `U`

This character records the dominant visible blade outline only.

### M05 leaf margin

States:

- `entire_or_nearly_entire`
- `serrate_or_dentate`
- `crenate_or_rounded_teeth`
- `lobed_or_incised`
- `spiny_or_aculeate_margin`
- `mixed`
- `U`

Do not score damage, pigment gaps or line wobble as teeth.

### M06 leaf apex

States:

- `acute_or_acuminate`
- `obtuse_or_rounded`
- `truncate_or_emarginate`
- `mucronate_apiculate_or_distinct_tip`
- `mixed`
- `U`

Only a clearly visible distal blade end qualifies.

### M07 leaf base

States:

- `attenuate_or_cuneate`
- `rounded_or_obtuse`
- `cordate`
- `sagittate_or_hastate`
- `truncate`
- `mixed`
- `U`

Only code where blade-to-petiole/axis transition is visibly interpretable.

### M08 primary venation depiction

Coarse depiction states:

- `single_midvein_laterals_not_evident`
- `pinnate_laterals_evident`
- `palmate_or_actinodromous_like`
- `parallel_or_subparallel`
- `reticulate_network_evident`
- `mixed`
- `U`

The suffix `-like` is deliberate: this is depiction coding, not anatomical identification.

### M09 stem/axis branching architecture

States:

- `unbranched_visible_axis`
- `one_or_more_lateral_branches`
- `repeated_forking_or_dichotomy_like`
- `tufted_multiple_axes_from_base`
- `mixed`
- `U`

Do not use leaf petioles as stem branches.

### M10 root/subterranean architecture

States:

- `single_primary_root_like`
- `branched_root_system`
- `fibrous_tufted_roots`
- `swollen_tuberous_or_storage_like`
- `bulb_corm_or_compact_storage_body_like`
- `rhizome_or_horizontal_axis_like`
- `mixed`
- `U`

The `-like` wording prevents botanical inference beyond the drawing.

### M11 reproductive structure architecture

Applicable only when a reproductive structure is clearly depicted.

States:

- `solitary_terminal_or_axillary_unit`
- `cluster_or_head_like`
- `spike_or_raceme_like`
- `umbel_like`
- `branched_panicle_like`
- `multiple_units_architecture_unclear`
- `U`

Do not infer flower identity solely from color.

### M12 visible radial symmetry of reproductive unit

States:

- `radial_or_actinomorphic_like`
- `bilateral_or_zygomorphic_like`
- `asymmetrical_or_irregular`
- `not_resolvable`
- `U`

This refers only to the visible drawn unit.

## 6. Secondary morphology lane

The following are recorded only if clearly visible and do not own the primary Phase66 claim:

- petiole visibly present/absent;
- leaflet count class;
- lobe count class;
- branch-order count class;
- visible flower/reproductive-unit count class;
- explicit spine/thorn/prickle depiction;
- visible tendril-like structure.

These are diagnostics, not a reservoir from which a significant primary result may be selected post hoc.

## 7. Color lane — separate from morphology

Color is not used to repair a morphology failure.

For each crop, record separately for visible organ regions:

- `green_present`
- `red_present`
- `blue_present`
- `yellow_or_ochre_present`
- `brown_present`
- `unpainted_or_parchment_dominant`

Values: 0/1/U.

Primary color analysis, if later authorized, must use deterministic pixel-space rules frozen in a separate Phase66 color preflight. Visual naming of subtle colors is not permitted as the scientific measurement.

## 8. Annotation engine and reproducibility

There is no human-rating or crowd-similarity step.

The annotation procedure will use a fixed image-only machine-vision instruction containing exactly the character/state definitions above. The model receives:

- the frozen Phase65 crop image;
- object ID only;
- no page transcription;
- no label string;
- no neighboring label crop;
- no Phase65B result;
- no other objects for pairwise comparison.

Output must be machine-readable JSON with one state per frozen field plus a short image-evidence note restricted to visible geometry.

Before annotation of the P25 population, the exact prompt/instruction text, model identity available to the execution environment, output schema and retry policy must be committed. If deterministic model version pinning is unavailable, this limitation must be recorded and a repeat-annotation stability audit is mandatory before any label-side reveal.

## 9. Unknown and disagreement policy

`U` is mandatory when the frozen visual criterion is not satisfied.

No manual override is allowed after label-side data are opened.

If repeated machine annotations disagree before label reveal:

- retain the modal state only if at least 2/3 exact agreement is achieved under identical frozen inputs;
- otherwise assign `U`;
- never adjudicate by looking at the label or at association results.

A repeat pass is for measurement stability only, not model selection.

## 10. Character eligibility firewall before text reveal

Before any label-side feature is computed, publish for each character:

- number observable vs `U`;
- state counts;
- page/row distribution;
- whether any state has fewer than 3 observations;
- repeat-annotation exact agreement if applicable.

A primary character is eligible only if:

1. at least 16/24 retained Phase65 units are non-`U`;
2. at least two states each contain >=4 units overall;
3. the character is represented on both f102v2 and f100v;
4. no single physical row contains >80% of all observations of a non-rare state;
5. repeat annotation exact agreement is >=0.80 if repeat audit is required.

Characters failing this firewall remain descriptively archived but cannot own a Phase66 primary claim.

## 11. Text-side firewall

No text feature may be selected by looking at morphology associations.

Before image↔text association, freeze a bounded text feature family derived without morphology access. Candidate families must be generic and auditable, for example:

- label length;
- first glyph unit;
- last glyph unit;
- presence of preregistered frequent unigram units;
- presence of preregistered frequent bigram units;
- boundary count for W1/W2;
- positional glyph-class counts.

Any vocabulary-dependent feature set must be selected from a corpus/population that is explicitly separated from the Phase66 outcome test or by a morphology-blind frequency rule frozen before association.

No Voynich-specific morpheme interpretation is allowed in the primary test.

## 12. Primary/replication chronology

Reuse the Phase65 page chronology unless a later power/eligibility audit proves it impossible before any association is computed:

- primary page: f102v2;
- replication page: f100v.

The exact association statistic, multiple-testing control, minimum effect size and permutation/null scheme must be frozen in `PLAN_B.md` after the image annotation table and text-feature family are separately frozen but **before the first image↔text association is computed**.

Phase66A itself does not compute an image↔text association.

## 13. What Phase66A may conclude

Allowed:

> A botanical-description character schema was externally grounded and frozen, then applied image-only with auditable observability/stability, producing a sealed morphology table suitable (or unsuitable) for a later prospective content-relation test.

Not allowed:

- plant identification;
- semantic decoding;
- glyph meaning;
- morphology↔label association;
- repair of Phase65B.

## 14. Sources used to freeze the design

- Dallwitz, M. J. / TDWG, DELTA — DEscription Language for TAxonomy: explicit character/state encoding for taxonomic descriptions.
- TDWG Structured Descriptive Data (SDD): structured descriptive data model for taxa/specimens.
- Flora of North America Categorical Glossary, Hunt Institute for Botanical Documentation: standardized categorical terminology including arrangement, architecture, apex, base, margin, shape, venation and structure.
- Beentje, H. J., *The Kew Plant Glossary*, 2nd ed., Royal Botanic Gardens, Kew, 2016: secondary terminology cross-check.

The source framework is external to Voynichese and was chosen before Phase66 image annotation.
