# Phase 52B — document/genre confound, matched-window and length-character null

Status: exploratory robustness extension. The target metrics were already exposed in Phase 52A, so this is not prospective validation.

## Question

How much of the high Voynich edit-distance-1 token-family density can be reproduced by selecting different medieval Latin manuscript documents, especially heavily abbreviated scholastic/medical material?

## Added source samples

All excerpts were fetched from `HTR-United/CREMMA-Medieval-LAT`, whose transcription is graphematic. Four additional source-native manuscript excerpts were sampled:

- Philadelphia College of Physicians 10a.135 — medical, *Tractatus de Sterilitate*
- Mazarine 915 — scholastic, Adam Wodeham *Ordinatio*
- BnF Latin 6395 — literary, Seneca *Medea*
- UBL Ms 758 — ecclesiastical, *In annuntiatione Mariae*

The snippets are source excerpts, not normalized editions. Unicode letter/mark sequences were treated as graphematic tokens; punctuation was removed and abbreviation glyphs retained.

## 141-token window results

Median raw edit-1 type-family coverage:

- Phi 10a.135 medical: 0.289
- Mazarine 915 scholastic: 0.589
- Latin 6395 literary: 0.179 (134-token excerpt)
- UBL 758 ecclesiastical: 0.257

Mazarine reaches 0.663 in one 141-token window. This exceeds the earlier five-document pilot maximum of ~0.457 and confirms that document/scribal selection is a stronger confound than the first pilot suggested.

## Length + character-frequency null

For each window, token lengths were held fixed and token characters were resampled iid from that window's empirical character multiset. This asks how much edit-1 density remains after the most immediate short-token/alphabet effect is removed.

Observed-minus-null excess among the new Latin windows:

- Phi medical: +0.022 to +0.071
- Mazarine scholastic: +0.019 to +0.162
- Latin 6395 literary: +0.054
- UBL ecclesiastical: +0.016 to +0.149

The Mazarine raw density is therefore partly expected from its very short graphematic/abbreviated tokens, although one window retains a substantial +0.162 excess.

Using the same null idea on 80 random 141-token Voynich prose windows (Voynich composite units retained):

- median observed edit-1 coverage: 0.756
- median null: 0.297
- median excess: **+0.446**
- mean excess: +0.436
- sampled excess range (approx. 2.5–97.5% order statistics): +0.153 to +0.674

Thus the highest Latin window seen here overlaps only the extreme low end of the Voynich excess distribution; its typical excess is far smaller.

## Graphematic sensitivity diagnostic

A deliberately crude NFKD/ASCII-letters-only transform was applied to the Latin excerpts. This is **not** abbreviation expansion or normalized Latin and must not be interpreted as such. It only tests whether combining marks/special graphemes alone create the density.

Median edit-1 coverage after this transform:

- Phi: 0.404
- Mazarine: 0.615
- Latin 6395: 0.230
- UBL: 0.353

Mazarine remains high, so its structure is not merely a Unicode combining-mark artifact.

## Interpretation

Phase 52 changes the control logic but does not erase the Voynich anomaly.

Supported:

1. Medieval Latin manuscript choice strongly changes raw near-neighbour density.
2. Highly abbreviated scholastic writing can move much closer to Voynich than ordinary continuous prose.
3. Raw edit-1 density must not be compared without length/alphabet/graphematic controls.
4. After a simple length+character-frequency null, the current Voynich excess remains much larger than the added Latin samples.

Not established:

- that genre itself, rather than document/scribe/script/abbreviation practice, causes the differences;
- that all medieval practical or list-like genres remain below Voynich;
- that the current iid character null is the final cross-script null.

## Decision

The document/genre confound is large enough to remain a standing control, but the current evidence does not support treating it as a sufficient explanation of the Voynich near-family network. This is enough to resume the nested-generator programme while continuing to add stronger genre-matched controls when available.

Next phase: minimal hierarchical generator comparison with explicit line-position and paragraph/item-state mechanisms, with added complexity charged and all Phase 51/52 targets treated as exposed development targets.
