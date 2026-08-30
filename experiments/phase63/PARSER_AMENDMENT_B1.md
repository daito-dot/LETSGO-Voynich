# Phase63B parser amendment B1 — ZL Eva- apostrophe / zero

Status: **preflight-only correction committed before any Phase63B scientific metric is implemented or computed**.

The first parser preflight failed immediately when the strict Eva parser encountered notation present in the frozen ZL3b source. `SOURCE_MANIFEST_B.json`, which was produced before scientific implementation, had already exposed two plain nonalphabetic characters in ZL P-text after IVTFF structural stripping:

- apostrophe `'`
- digit `0`

Direct source inspection confirms these occur inside ZL Eva- tokens. The frozen IT2a/EvaT source inventory contains alphabetic characters only; this correction therefore does not alter IT tokenization or the GC/v101 parser.

Frozen correction:

- for **ZL Eva- only**, plain ASCII letters remain lowercase native units and `'` / `0` are additionally retained as one atomic native unit each;
- for **IT EvaT**, the parser remains alphabetic-only (plus any properly formed `@NNN;` unit if one were present);
- no punctuation is generalized into IT/EVA based on scientific results;
- scientific replication code has not yet been committed/run.

This is a syntax compatibility correction, not a metric/model change.