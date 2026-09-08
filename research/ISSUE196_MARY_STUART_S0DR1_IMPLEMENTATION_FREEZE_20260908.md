# Issue #196 Mary Stuart S0-D-R1 — implementation freeze clarification

Date: 2026-09-08  
Status: **FROZEN BEFORE R1 EXECUTABLE**

Two mechanical repository edge cases are fixed before the recovery implementation:

1. A GitHub repository reported by the frozen GeorgeLasry public-repository endpoint with `size == 0` or a null/empty `default_branch` is archived as `EMPTY_REPOSITORY`, has no searchable file population, and does not make the channel fail. This is the only no-clone exception.
2. Every nonempty listed repository must clone successfully at its API-reported default branch. Any failure is a channel failure; no repository is silently skipped.

Text-content scanning is attempted only for files <=2 MB whose extension is either in the already-frozen S0-D text-scan set or the already-frozen data-like extension set. Non-UTF-8/binary files remain eligible as path-name candidates but are not decoded or searched internally.

Archive files are not unpacked during S0-D-R1. A source-role-relevant archive filename may be located as a candidate, but its contents require a later separately frozen structural source inspection.

These rules alter no search identifier, source boundary, positive-candidate rule, five-layer criterion, or final classification.
