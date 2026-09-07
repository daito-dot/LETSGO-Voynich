# Issue #165 — pre-Gate metadata authority correction

Date: 2026-09-07
Status: **AUTHORITY-ONLY CORRECTION BEFORE ANY SECTION SCIENTIFIC SCORE**

The frozen Issue #165 plan and first Gate0 implementation copied the Issue #107 metadata result SHA-256 as:

`8f48a01ef4457f38a4e273fe32ea73b9f90817af156be0111bb56a550f443870`

That string is a transcription error.

The original authoritative Issue #107 artifact (`9985775083`, run `34049262845`) was re-downloaded and its `phase3b_metadata_gate0.json` bytes hash to:

`8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717`

The current frozen Issue #107 scanner (`metadata_gate0_audit.py`, blob `110a6b848df71c4f51ec0d9dd3b262039d1fc66f`) independently recomputes the same canonical JSON SHA-256:

`8f48a62e74fa34f78691949a4b9404caaea39fd6ad8360a93600c653f7147717`.

Issue #165 Gate0 run `34078048402` stopped on this exact mismatch before pure-leaf eligibility, section-placebo science, any section-conditioned probability/likelihood, `G_section`, `G_placebo`, or scientific classification was accepted. Its output was `gate_pass:false` with `scientific_section_metrics_computed:false`.

This correction changes **only** the copied Issue #107 authority hash. It does not change:

- section candidate labels;
- pure-leaf rules;
- support thresholds;
- Currier/fold/common-EVA authority;
- scribe-identifiability rule;
- deterministic one-leaf-left placebo;
- section model family;
- scientific pass rule or class set.

The original Issue #165 plan blob remains frozen for scientific design. This note supersedes only its mistyped Issue #107 result SHA.

No target-driven repair is licensed by this correction.
