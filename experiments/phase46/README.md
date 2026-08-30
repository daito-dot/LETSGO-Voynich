# Phase 46 — medieval plaintext temporal-shape control

## Question

Does the paragraph-reset / short-range temporal shape found in Voynich distinguish it from ordinary medieval prose or bounded cipher transforms?

## Control

Development control: Dante, *De vulgari eloquentia*, Liber I I.1–VIII.7, 48 genuine numbered source paragraphs, 2,405 words.

Because the control source did not supply comparable physical manuscript lineation for this purpose, words were deterministically wrapped using the empirical Voynich P-coded prose line-length distribution. A 200-wrap sensitivity analysis was also performed for raw Latin.

The first token of each synthetic line was excluded to match the Voynich convention used in the paragraph analyses.

## Key result

Short-range continuation is **not distinctive Voynich evidence**. Raw medieval Latin prose reproduced it and often showed a stronger previous-line advantage than Voynich. Bounded cipher transforms preserved or amplified this short-memory behavior.

The more discriminating feature was the large paragraph-boundary loss of edit1 token-family continuity:

- Voynich reset gap: about `+0.1443`
- raw/F1 Dante: about `+0.0216`
- F2 systematic cipher family maximum in this pilot: about `+0.0407`
- broad F3 nuisance/deceptive family maximum: about `+0.1077`

The F3 family here was deliberately broader than the later tightened admissible Phase44B encoder family. These values must not be described as the final Phase44B admissible cipher score.

## Interpretation

Phase46 corrected an earlier interpretation: generic short-memory drift cannot be credited as evidence for a special Voynich stateful generator/cipher.

The active target became the **large paragraph-boundary discontinuity in near-neighbor token-form families**.

This remained unusual relative to the one medieval Latin control and bounded transforms tested here, but one 2.4k-word Latin source cannot represent medieval natural language. Phase52 therefore explicitly revisits the document/genre confound with multiple manuscript types.
