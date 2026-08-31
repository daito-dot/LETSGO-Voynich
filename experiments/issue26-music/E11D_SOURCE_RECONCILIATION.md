# Issue26E11D preflight — reconcile official STA running-text population

Status: **DESCRIPTIVE PARSER AUDIT ONLY — NO PLAINTEXT SCORING**

E11C was `SOLVER INADEQUATE`, so no Voynich inference was made. Its parser also saw 4,119 running-text source lines / 140,423 family events, while the corrected generic E11B source audit saw 4,130 lines / 140,589 events.

Before solver work or another scientific test, reconcile that population difference using only source syntax.

## Frozen diagnostic

Use the exact official ZL3b STA1 file:

- SHA-256 `8438ba1c45f47fe1d06b5262cbcdf60ce69158a0edbd4dd802612896f3217e2a`.

For every line matched by the generic E11B running-text locus regex (kind contains `P`):

1. test whether the E11C locus regex also matches;
2. list every generic-running-text line not matched by E11C, including line number, locus header, and code-event count after the corrected first-reading alternative rule;
3. classify the syntactic reason without inspecting any decoded/plaintext output;
4. also compare per-line first-reading code counts between generic and E11C-compatible parsing for lines matched by both;
5. no Latin model, substitution key, plaintext decoding, or statistical score may be run.

After diagnosis, freeze a corrected locus parser that includes all intended running-text lines. Do not change the `P` population criterion based on content.
