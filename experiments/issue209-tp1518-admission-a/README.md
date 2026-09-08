# Issue #209 — TP1518-WA0 Priority-5 admission Stage A

This branch runs one external-only audit of the pinned Trithemius Corpus machine-readable word-alphabet data before any Voynich target reveal.

Frozen source:

- `Trithemius-Corpus/Trithemius-Corpus`
- commit `0e38a37671a5e3b5decd11c19fe82de79883cae7`
- `site/static/cipher-data.json`

The audit counts emitted substitution columns, cell coverage, within-column duplicate words and emitted chunk/column order. It performs no OCR repair, Latin lexical repair, target lookup or Voynich scoring.

Gate classes and stop rule are controlled by Issue #209.
