# Issue #194 Gate 0 — implementation freeze clarification

Date: 2026-09-08  
Status: **FROZEN BEFORE EXECUTABLE / BEFORE DECODE PAYLOAD INSPECTION**

One parser edge case is made explicit before the Gate-0 executable is committed:

- CT2 nomenclature examples can encode a plaintext space as `[ ];[CIPHER_TOKEN]`.
- Therefore, after removing the outer brackets, a non-empty plaintext field containing only whitespace is canonicalized to one ASCII space (`" "`) rather than to the empty string.
- All other plaintext and cipher-side fields follow the Stage-0 plan: surrounding horizontal whitespace is stripped; cipher alternatives split only on literal `|`.

This clarification changes no Gate threshold, classification, source URL, boundary channel, or score firewall. It only makes the already-listed plaintext-space boundary channel executable without ambiguity.
