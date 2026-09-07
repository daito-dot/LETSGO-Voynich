# LETSGO-Voynich

Open research repository for testing falsifiable hypotheses about the Voynich Manuscript.

**日本語での参加も歓迎します。**

The manuscript is **not deciphered**. This repository separates reproducible surface structure, predictive mechanisms, historical mechanisms, content relations, and decipherment claims rather than treating them as interchangeable.

## Start here

If you are continuing the research from current `main`, read these in order:

1. [`RESUME.md`](RESUME.md) — deterministic restart point and exact current frontier;
2. [`research/STATUS.md`](research/STATUS.md) — current accepted scientific interpretation;
3. [`ROADMAP.md`](ROADMAP.md) — current sequencing and next decision gate;
4. [`research/MECHANISM_DISCRIMINATION_FRONTIER_20260907.md`](research/MECHANISM_DISCRIMINATION_FRONTIER_20260907.md) — handoff for the present mechanism-search phase;
5. [Issue #172](https://github.com/daito-dot/LETSGO-Voynich/issues/172) — governing post-#88 mechanism-discrimination program;
6. [`experiments/joint-mechanism-discrimination/ISSUE176_RECOVERY_REVEAL_PROVENANCE.md`](experiments/joint-mechanism-discrimination/ISSUE176_RECOVERY_REVEAL_PROVENANCE.md) — frozen historical-anchor calibration result;
7. [`research/HYPOTHESIS_LEDGER.md`](research/HYPOTHESIS_LEDGER.md) — hypothesis history, including negative results;
8. [`research/RESEARCH_PROTOCOL.md`](research/RESEARCH_PROTOCOL.md) — normative evidential discipline.

Historical restart points and superseded navigation documents live in Git history and under [`research/archive/`](research/archive/) where retained. Phase/Issue-specific frozen plans, first-reveal artifacts, hashes and provenance remain authoritative for their exact historical methods and numbers.

## Current structural picture

The strongest accepted evidence supports a compact, multiscale **surface-production** description:

- certain visible spaces behave as reproducible construction/production boundaries in both ZL3b and Takahashi/IT2a;
- token-internal topology is nearly reproduced by a target-blind second-order occupied-slot successor grammar;
- short edit-near recurrence/cache effects and slower causal-prefix/prior-paragraph inventory carry measurable cross-token predictive information;
- useful immediate raw context is localized to adjacent visible units inside the same source line and resets at line breaks;
- under fixed `k=2`, generic line-position/onset plus the immediately previous unit's terminal symbol exactly reproduces the previously flexible line-local expert at token-logp level;
- the terminal→initial edge independently replicates across ZL3b/IT2a under common Basic-EVA;
- one fixed reading-balanced common-EVA base table suffices across those reading lineages;
- Currier A/B adds robust incremental next-initial information, but the remaining contrast factorizes to a context-invariant outcome bias rather than requiring a robust previous-terminal-specific interaction;
- after observable augmentation, no robust flexible residual remains that licenses a richer latent-state model.

This is a predictive surface contract. It does **not** establish natural-language word boundaries, plaintext, semantics, a cipher family, an author, a hoax/artificial origin, historical direction, or a historical production algorithm.

## Current program and frontier

Issue #88 is complete. The active program is **Issue #172 — joint mechanism discrimination under the frozen structural contract**.

Historical-anchor calibration is complete under that contract:

- **A1/A1-R1 — PARTIAL STRUCTURAL MODEL**: PASS R1/R3/R4/R10; FAIL R2/R5/R6/R7/R8; R9 N/A.
- **Naibbe C1-E0 — PARTIAL STRUCTURAL MODEL**: PASS R1/R2/R8/R10; FAIL R3/R4/R5/R6/R7/R9.
- no historical anchor is `JOINT-STRUCTURAL COMPETITIVE`;
- no decoder is promoted.

The strongest shared falsifier in this calibration is **R5/R6**: both anchors fail the accepted same-line previous-terminal → next-initial responsibility and instead preserve unwanted continuation across line breaks.

The current task is therefore **not** to repair A1, repair Naibbe, or combine their complementary passes. The next task is to use the frozen failure vector to eliminate architecture classes, then select and preregister a new independently motivated mechanism family before any new target scoring.

No new candidate family has yet been accepted or frozen. Specific ideas discussed outside the repository are not current scientific commitments unless they are added prospectively under the Issue #172 rules.

## Key current authorities

- Issue #88 predictive-information closeout: [`research/PREDICTIVE_INFORMATION_PROGRAM_CLOSEOUT_20260907.md`](research/PREDICTIVE_INFORMATION_PROGRAM_CLOSEOUT_20260907.md).
- Issue #172 governing program: [Issue #172](https://github.com/daito-dot/LETSGO-Voynich/issues/172).
- Historical-anchor recovery/calibration: [`ISSUE176_RECOVERY_REVEAL_PROVENANCE.md`](experiments/joint-mechanism-discrimination/ISSUE176_RECOVERY_REVEAL_PROVENANCE.md).
- Frozen recovery result SHA-256: `d6149607aa90530b02d440899d7abb23c28e44a51ff270205e919a3f00d17b35`.
- Calibration merge before this navigation refresh: `74d117e27e75e2594cebdf782ee506c77a1a762e` (PR #177).

For scientific claims, cite the exact phase/Issue artifact rather than only moving `main`.

## Repository layout

- `research/` — current scientific authority, program documents, ledgers and audits;
- `research/archive/` — superseded snapshots retained for provenance where applicable;
- `experiments/` — frozen plans, code, reports, result JSON and first-reveal provenance;
- `data/` — source/transcription provenance and fetch/setup tooling;
- `.github/workflows/` — replay and first-reveal workflows;
- `hypotheses/` — hypothesis-specific material where retained.

## Evidence discipline

A useful hypothesis states the claim and scope, a falsifiable prediction, a falsification condition, the data-selection rule, the baseline/control, and an exact reproduction path where practical.

Target outcomes must not be used to choose the architecture, threshold, stratum, transformation or hyperparameter later presented as prospective evidence. Negative results stay in the repository because they constrain the search space.

Visible spaces may be used as empirically validated production boundaries under the tested representations; they must not be silently relabeled as natural-language words.

For the current Issue #172 phase, architecture selection itself is part of the evidential firewall: a new candidate must have an independent mathematical, historical or procedural motivation before Voynich target scoring.

## Contribution scope

Contributions are welcome for natural-language, cipher, deliberately deceptive, formal/generative, scribal-production and mixed-mechanism hypotheses, as well as stronger controls and null models. A readable output is not sufficient for a decipherment claim if the mapping has uncontrolled substitutions, anagrams, nulls, homophones, exceptions or context-dependent degrees of freedom.

## Data policy

Current analyses use ZL3b / EVA-derived material and independently maintained readings where phase-specific source authority permits. Third-party transcription text is not automatically redistributed. [`data/README.md`](data/README.md) documents provenance, expected identity and local setup.

## License and reuse

- **Software and code** — MIT License; see [`LICENSE-CODE`](LICENSE-CODE).
- **Original research text, reports, documentation, figures, tables and project-generated result files** — CC BY 4.0; see [`LICENSE-CONTENT`](LICENSE-CONTENT).
- **Third-party transcriptions, manuscript images, corpora and quotations** — remain under their original rights and terms.

See [`LICENSE`](LICENSE) for repository-wide scope. Machine-readable citation metadata is in [`CITATION.cff`](CITATION.cff).

## Status

Active research under **Issue #172**. The current frontier is **architecture-class elimination and independently motivated new-candidate selection after the frozen historical-anchor calibration**. See [`RESUME.md`](RESUME.md) and [`research/MECHANISM_DISCRIMINATION_FRONTIER_20260907.md`](research/MECHANISM_DISCRIMINATION_FRONTIER_20260907.md).
