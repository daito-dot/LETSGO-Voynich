# Phase 52 — document / genre confound test

## Question

Do apparent Voynich anomalies depend strongly on which comparison document is selected, even when the comparison language is held approximately fixed?

This phase was inserted before adding more machinery to the formal generator. Otherwise we risk modeling an ordinary property of medical, recipe, commentary, or other strongly structured manuscript genres as a Voynich-specific mechanism.

## Medieval Latin pilot

A first control panel uses manuscripts from the CREMMA Medii Aevi / CREMMA-Medieval-LAT project. This is useful because multiple medieval Latin manuscript types are represented under a common graphematic-transcription project.

Initial 141-token matched samples showed substantial document movement in edit-distance-1 type-family density and line-position effects. Example pilot values:

| manuscript | broad type | edit1 type-family density | line-position effect |
|---|---|---:|---:|
| Arras 861 | literary | 0.150 | 0.050 |
| CLM 13027 | medical | 0.214 | 0.087 |
| H318 | medical / recipes | 0.293 | 0.064 |
| UBL 758 | ecclesiastical | 0.371 | 0.154 |
| BIS 193 | scholastic | 0.457 | 0.046 |

These are pilot observations, not a balanced genre estimate. Manuscript, scribe/script, abbreviation practice, chronology and genre are still partly confounded.

## Voynich section variation

Voynich is also heterogeneous. In matched 141-token windows, preliminary section medians were approximately:

- Herbal A: 0.747
- Herbal B: 0.773
- Biological: 0.803
- Pharmaceutical: 0.733
- Recipes: 0.741

The current analysis indicates that section accounts for a substantial fraction of folio-level variation. Consequently, neither “Latin” nor “Voynich” should be treated as a single homogeneous distribution.

## Current interpretation

Document choice matters enough that a single Dante prose control cannot justify a claim about natural language or medieval Latin in general.

However, the current Latin pilot maximum remains below the Voynich section-level matched-window values. Therefore the hypothesis that Voynich's high near-neighbor density is *mainly* an artifact of selecting an unusually low-density Latin document is **preliminarily not supported**.

This is not closure. The Latin panel must be expanded and better balanced.

## Next tests

1. multiple manuscripts per relevant genre
2. medical, recipe/pharmacological, commentary/scholastic and other strongly templated material
3. token-length and alphabet/inventory-preserving controls
4. separation of manuscript/document, genre, chronology/script and language effects where data allow
5. exact paragraph-boundary decomposition on controls with genuine paragraph/item boundaries
6. diplomatic/graphematic versus normalized/expanded text only where a defensible transformation or aligned edition is available

The Phase52 targets are now exposed and must not later be described as prospective validation targets.
