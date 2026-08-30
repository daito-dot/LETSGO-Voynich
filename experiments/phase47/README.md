# Phase 47 — paragraph-boundary edit decomposition

## Question

Is the large paragraph-boundary loss of near-neighbor token-family continuity concentrated in one edit type or token zone, or does it reflect a broad reconfiguration?

## Metric

For each current-line token type, measure whether a non-identical edit-distance-1 neighbor exists in the immediately preceding line. The first observed token of every line is excluded.

If a current token has multiple valid prior-line edit1 neighbors, its contribution is divided equally across all valid matches rather than selecting one post hoc. Operation and zone components therefore sum exactly to the original near-share/reset gap.

Direction: prior line -> current line.

Operations:

- substitution
- insertion
- deletion

Zones:

- initial
- medial
- final

## Voynich result

Total paragraph-boundary reset gap: `0.1442805889`.

By operation:

- substitution: `+0.0994329169` (68.9%)
- insertion: `+0.0202939041` (14.1%)
- deletion: `+0.0245537680` (17.0%)

By zone:

- initial: `+0.0617940536` (42.8%)
- medial: `+0.0425246568` (29.5%)
- final: `+0.0399618786` (27.7%)

Paired-folio bootstrap intervals were positive for all broad operation and zone components.

The only fine operation-zone cell without a clearly positive interval in this analysis was insertion-final.

## Control interpretation

The strongest high-gap nuisance-cipher configuration in the then-current broad Phase46/47 F3 control grid approached the scalar total gap mainly through **initial substitutions**. It did not reproduce the Voynich broad medial/deletion geometry.

Thus the current distinction is not merely that Voynich has a larger scalar boundary effect; the effect is distributed differently across token construction.

## Conclusion

The simplest boundary-specific prefix/suffix explanation is **not supported**.

The data support a broad change in the active repertoire of related token forms across paragraph boundaries. This remains compatible with multiple mechanisms:

1. paragraph-conditioned morphology/orthography in meaningful text
2. paragraph-conditioned cipher/key/alphabet state
3. a structured generator that reinitializes distributed token-construction state

Phase47 does not by itself distinguish those mechanisms.
