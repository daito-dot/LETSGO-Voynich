# Phase 51 — frozen finite-state DSL falsification

Phase 50 showed that a simple meaning-light finite-state morphology with weak local state could be tuned to reproduce two striking Voynich statistics: high edit-distance-1 family density and short-range locality.

Phase 51 froze that model family and tested dimensions not used to obtain the Phase50 match.

## Frozen family

- root families: 64
- local-state block length: 4
- state-use probability: 0.30
- prefix probability: 0.22
- suffix probability: 0.32
- variants per root: 2
- alphabet: `abcdefghiklmnoprstuy`
- roots: random length-3 strings, each with a one-final-character variant

Generated streams were laid into empirical Voynich folio/line/paragraph layout after generation. The generator was not informed of line or paragraph boundaries.

## Main pilot results

Across 20 independently generated corpora:

### Paragraph-boundary edit1 reset

- Voynich target: `0.1333132345`
- frozen DSL median: `0.0285473746`
- DSL range: `0.0215099795–0.0333334647`
- generated corpora >= Voynich: `0/20`

This target was recomputed using the Phase51 immediate-previous-line sharing metric and is therefore not numerically identical to the Phase47 fractional operation-decomposition headline.

### Line-position grammar

Mutual information between first/middle/last line position and token signature `(first unit, last unit, capped length)`:

- Voynich: `0.1435077526` bits
- frozen DSL median: `0.0241711464`
- DSL range: `0.0217489885–0.0261229049`
- generated corpora >= Voynich: `0/20`

### Period-4 residual

The DSL was also below the recomputed Voynich residual, but only one token-shuffle null was used per replicate in the completed run. This is diagnostic only and does not replace the stronger Phase42/43 periodicity tests.

## Interpretation

The Phase50 toy DSL is **falsified as a sufficient broad mechanism**. Its density/locality success was real but narrow.

At minimum, a stronger formal generator would require explicit line-position organization and a paragraph-level transition/reset capable of reorganizing active token families. Because these additions are motivated by observed failures, they incur complexity cost and cannot count as independent validation.
