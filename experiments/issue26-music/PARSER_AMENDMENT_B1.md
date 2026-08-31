# Issue #26 experiment B — parser amendment B1

Status: **FROZEN BEFORE EXECUTABLE / SCIENTIFIC REVEAL**

`PLAN_B.md` already froze the population, representation and statistic. This amendment makes its phrase "remove editorial angle-bracket annotations and bracket-choice markup conservatively" executable before any scientific output exists.

For each `Lz` body string:

1. remove every `<!...>` and `<...>` annotation as a whole;
2. for a square-bracket alternative of the form `[left:right]`, retain `left` only; this follows the primary reading convention and does not inspect the historical target;
3. for square brackets without `:`, retain their alphabetic contents with brackets removed;
4. remove every brace-delimited `{...}` uncertain/editorial segment as a whole rather than concatenating across it;
5. replace all remaining characters other than ASCII letters, dot and whitespace with a separator;
6. split on dots and whitespace;
7. lowercase and retain non-empty ASCII-letter runs.

Editorial removal always inserts a separator, so no n-gram can be created across removed markup.

This parser rule is not varied in sensitivities.
