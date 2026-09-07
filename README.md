# LETSGO-Voynich

Open research repository for testing falsifiable hypotheses about the Voynich Manuscript.

**日本語での参加も歓迎します。**

The manuscript is **not deciphered**. This repository separates reproducible surface structure, predictive mechanisms, historical mechanisms, content relations, and decipherment claims rather than treating them as interchangeable.

## Start here

If you are continuing the research, read these files in order:

1. [`RESUME.md`](RESUME.md) — deterministic restart point and exact next move;
2. [`research/STATUS.md`](research/STATUS.md) — current accepted scientific interpretation;
3. [`ROADMAP.md`](ROADMAP.md) — active decision gate and downstream forks;
4. [Issue #161](https://github.com/daito-dot/LETSGO-Voynich/issues/161) — current executable Currier-factorization gate;
5. [`research/PREDICTIVE_INFORMATION_PROGRAM.md`](research/PREDICTIVE_INFORMATION_PROGRAM.md) — governing Issue #88 program;
6. [`research/HYPOTHESIS_LEDGER.md`](research/HYPOTHESIS_LEDGER.md) — hypothesis history, including negative results;
7. [`research/RESEARCH_PROTOCOL.md`](research/RESEARCH_PROTOCOL.md) — normative evidential discipline.

Historical restart points and superseded navigation documents live under [`research/archive/`](research/archive/). Phase/Issue-specific frozen plans, first-reveal artifacts, hashes and provenance remain authoritative for their exact historical methods and numbers.

## Current structural picture

The strongest current evidence supports a compact, multiscale **surface-production** description:

- certain visible spaces behave as reproducible construction/production boundaries in both ZL3b and Takahashi/IT2a;
- token-internal topology is nearly reproduced by a target-blind second-order occupied-slot successor grammar;
- short edit-near recurrence/cache effects and slower causal-prefix/prior-paragraph inventory carry measurable cross-token predictive information;
- useful immediate raw context is localized to adjacent visible units inside the same source line and resets at line breaks;
- under fixed `k=2`, generic line-position/onset plus the immediately previous unit's terminal symbol exactly reproduces the previously flexible line-local expert at token-logp level;
- after that observable edge is added to corrected B3, Issue #134 finds **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**; both flexible challenger families select final `w=0` in all five outer folds;
- Issue #139 independently replicates the terminal→initial edge on Takahashi/IT2a;
- Issue #145 places ZL3b and IT2a in one frozen common Basic-EVA representation and finds the edge robust in both readings;
- Issue #148 transports the **literal** previous-terminal→next-initial conditional table bidirectionally across the two readings, retaining about 96–98% of target-native gain;
- Issue #151 shows **one fixed 0.5/0.5 reading-balanced common-EVA edge table suffices**; neither ZL3b nor IT2a retains a robust reading-specific residual;
- Issue #155 then shows that the stabilized literal table does **not** transport across Currier A/B in either direction under support matching;
- Issue #158 directly decomposes that difference and finds **`CURRIER GATE ADDS ROBUST EDGE INFORMATION IN BOTH A AND B`** independently in both readings.

The minimal live edge responsibility is therefore:

> **shared reading-independent terminal→initial architecture + explicit Currier-conditioned literal mapping.**

This does **not** establish natural-language word boundaries, plaintext, semantics, a cipher family, an author, hoax/artificial origin, historical direction, or a historical production algorithm.

## Current frontier

The active gate is **Issue #161 — global next-initial bias vs context-specific Currier edge interaction**.

Issue #158 proves that Currier A/B changes held-out edge prediction, but that does not yet tell us whether the A/B difference genuinely depends on the previous-terminal context. The next compression question is:

> Can Currier A/B be represented by one shared terminal→initial table plus a context-invariant Currier-specific bias over the next initial atom, or does a robust previous-terminal × next-initial interaction remain?

Issue #161 freezes a training-only outcome multiplier for all 32 common-EVA outcomes before target scoring. It compares:

- the regime-neutral pooled edge table;
- an outcome-only Currier gate with no Currier×previous-terminal interaction;
- the full Currier-specific edge table.

Primary residual:

`G_interaction = bits(EDGE_OUTCOME) - bits(EDGE_REGIME)`.

The first deliverable is score-free Gate0. No held-out `EDGE_OUTCOME` likelihood, `G_outcome`, `G_interaction` or classification may be inspected until authority, normalization, support and leakage are frozen.

A rich latent-state search remains **not licensed** by current residual evidence.

## Key current authorities

- Issue #134 residual closure: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.
- Issue #139 independent IT2a edge: run `34061721332`, artifact `9997679250`, result SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`.
- Issue #145 common-EVA edge: run `34062199123`, artifact `9997826217`, result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`.
- Issue #148 cross-reading literal transport: run `34073660425`, artifact `10001309613`, result SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`.
- Issue #151 reading-shared table consolidation: run `34074437422`, artifact `10001563139`, result SHA-256 `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`.
- Issue #155 common-EVA matched Currier transport: run `34075146845`, artifact `10001781210`, result SHA-256 `041d7abe8f677da012ae143df9f4f372e88afc2e2b3cc7b359a58a4d7395b737`.
- Issue #158 incremental Currier gate: run `34076400927`, artifact `10002205049`, result SHA-256 `eef6aee7cb202d73a7090c7aca0e9a0df404b46373589a8203da2b80ec1c3107`, PR #160 merge `1741bed875a582594dc797ef18e30dd2ef3351ce`.

For scientific claims, cite the exact phase/Issue artifact rather than only moving `main`.

## Repository layout

- `research/` — current scientific authority, program documents, ledgers and audits;
- `research/archive/` — superseded navigation/current-state snapshots retained for provenance;
- `experiments/` — frozen plans, code, reports, result JSON and first-reveal provenance;
- `data/` — source/transcription provenance and fetch/setup tooling;
- `.github/workflows/` — replay and first-reveal workflows;
- `hypotheses/` — hypothesis-specific material where retained.

## Evidence discipline

A useful hypothesis states the claim and scope, a falsifiable prediction, a falsification condition, the data-selection rule, the baseline/control, and an exact reproduction path where practical.

Target outcomes must not be used to choose the architecture, threshold, stratum, transformation or hyperparameter later presented as prospective evidence. Negative results stay in the repository because they constrain the search space.

Visible spaces may be used as empirically validated production boundaries under the tested representations; they must not be silently relabeled as natural-language words.

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

Active research under Issue #88. The current executable frontier is **Issue #161 Currier edge factorization**; see [`RESUME.md`](RESUME.md) and [`ROADMAP.md`](ROADMAP.md).
