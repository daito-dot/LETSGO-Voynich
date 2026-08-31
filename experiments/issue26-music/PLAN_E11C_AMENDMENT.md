# E11C pre-executable amendment — unreadable-sign boundaries

Status: **FROZEN BEFORE E11C EXECUTABLE / SCIENTIFIC REVEAL**

The official STA1 file can retain `?` for unreadable/uncertain text. E11C must not delete such a marker and accidentally create a new adjacency.

Authoritative parsing rule:

- `<->` interruption markers break a character-LM run as already preregistered;
- a literal `?` likewise breaks a run and token adjacency;
- no 4-gram crosses either boundary;
- the `?` is not a cipher symbol and is not mapped to plaintext;
- all other E11C source, family, fold, solver, control, and decision rules remain unchanged.
