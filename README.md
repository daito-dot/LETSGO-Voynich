# LETSGO-Voynich

Open research repository for testing falsifiable hypotheses about the Voynich Manuscript.

**日本語での参加も歓迎します。**

The manuscript is **not deciphered**. This repository separates reproducible surface structure, predictive mechanisms, historical mechanisms, content relations, and decipherment claims rather than treating them as interchangeable.

## Start here

If you are continuing the research, read these files in order:

1. [`RESUME.md`](RESUME.md) — deterministic restart point and exact next move;
2. [`research/STATUS.md`](research/STATUS.md) — current accepted scientific interpretation;
3. [`ROADMAP.md`](ROADMAP.md) — active decision gate and downstream forks;
4. [Issue #151](https://github.com/daito-dot/LETSGO-Voynich/issues/151) — current executable shared-table consolidation gate;
5. [`research/PREDICTIVE_INFORMATION_PROGRAM.md`](research/PREDICTIVE_INFORMATION_PROGRAM.md) — governing Issue #88 program;
6. [`research/HYPOTHESIS_LEDGER.md`](research/HYPOTHESIS_LEDGER.md) — current hypothesis status, including negative results;
7. [`research/RESEARCH_PROTOCOL.md`](research/RESEARCH_PROTOCOL.md) — normative evidential discipline.

Historical restart points and superseded navigation documents live under [`research/archive/`](research/archive/). Phase/Issue-specific frozen plans, first-reveal artifacts, hashes and reports remain authoritative for their exact historical methods and numbers.

## Current structural picture

The strongest current evidence supports a compact, multiscale **surface-production** description:

- certain visible spaces behave as reproducible construction/production boundaries in both ZL3b and Takahashi/IT2a;
- token-internal topology is nearly reproduced by a target-blind second-order occupied-slot successor grammar;
- short edit-near recurrence/cache effects and slower causal-prefix/prior-paragraph inventory carry measurable cross-token predictive information;
- useful immediate raw context is localized to adjacent visible units **within the same source line** and resets at line breaks;
- under fixed `k=2`, generic line-position/onset plus the immediately previous unit's terminal symbol exactly reproduces the previously flexible line-local expert at token-logp level;
- after that observable edge is added to corrected B3, Issue #134 finds **`NO ROBUST RESIDUAL BEYOND AUGMENTED OBSERVABLE CORE`**: both flexible challenger families select final `w=0` in all five outer folds;
- Issue #139 independently replicates the terminal→initial edge on Takahashi/IT2a (`+0.1521119 bit/token`, positive 5/5);
- Issue #145 places ZL3b and IT2a in one frozen common Basic-EVA representation and finds the edge robust in both readings;
- Issue #148 then transports the **literal** previous-terminal→next-initial conditional table bidirectionally across those readings: ZL3b→IT2a `+0.1555482 bit/token`, IT2a→ZL3b `+0.1303902`, both positive 5/5, retaining about 96–98% of the target-native edge gain.

The earlier Currier A/B result remains different: under the frozen support-matched test in Issue #130, literal table transport was **B→A only**. The cross-reading result does not erase that regime asymmetry.

This does **not** establish natural-language word boundaries, plaintext, semantics, a cipher family, an author, hoax/artificial origin, historical direction, or a historical production algorithm.

## Current frontier

The active gate is **Issue #151 — shared common-EVA edge table vs reading-specific residual**.

Issue #148 shows that each reading's literal edge table predicts the other reading almost as well as the target-native table. The next question is therefore a model-simplification question:

> Can the two reading-native edge tables be collapsed to one frozen `0.5/0.5` reading-balanced common-EVA table, or does either reading retain reproducible held-out edge information that requires its own table?

The first #151 deliverable must be score-free. It freezes source/fold authority, the exact fractional-count consensus construction, target populations, support and decision classes before any shared-table held-out likelihood is inspected.

A rich latent-state search remains **not licensed** by the current residual evidence. If #151 permits one consolidated table, the next high-information test is whether the Currier A/B literal-table asymmetry survives the stabilized common representation.

See [`ROADMAP.md`](ROADMAP.md).

## Repository layout

- `research/` — current scientific authority, program documents, ledgers and audits;
- `research/archive/` — superseded navigation/current-state snapshots retained for provenance;
- `experiments/` — frozen plans, code, reports, result JSON and first-reveal provenance;
- `data/` — source/transcription provenance and fetch/setup tooling;
- `.github/workflows/` — replay and first-reveal workflows;
- `hypotheses/` — hypothesis-specific material where retained.

`research/README.md` documents which research files are current authority and which names are historical records.

## Evidence discipline

A useful hypothesis states:

1. the claim and scope;
2. a prediction;
3. a falsification condition;
4. the data-selection rule;
5. the baseline/control;
6. the exact reproduction path where practical.

Target outcomes must not be used to choose the architecture, threshold, stratum, transformation or hyperparameter later presented as prospective evidence. Negative results stay in the repository because they constrain the search space.

Visible spaces may be used as empirically validated production boundaries under the tested representations; they must not be silently relabeled as natural-language words.

## Key current authorities

- Issue #134 first reveal: run `34035108074`, artifact `9990011421`, result SHA-256 `6779c2ea135e63f0c9c5be3e6200e564c18225fb95bb344f5349f946d73b9698`.
- Issue #139 independent IT2a first reveal: run `34061721332`, artifact `9997679250`, result SHA-256 `ec07a86d1acc12169be4f5073882877f3c86f4c8932f2fed2629d09518c18a4d`.
- Issue #145 common-EVA dual-reading first reveal: run `34062199123`, artifact `9997826217`, result SHA-256 `663f4b4f9f48992036c2517109f5b8efde459cbdd35d034b567233edbd2efdf2`.
- Issue #148 literal-table transport first reveal: run `34073660425`, artifact `10001309613`, result SHA-256 `305e6e4e6eb59dcc969f1d4075eb5b64b06621c7a0cac8077c4cdedd76874923`, merged PR #150 at `b7e643a0d3075a9f09dbd9ec3a8f50149cb4a131`.

For scientific claims, cite the exact phase/Issue artifact rather than only moving `main`.

## Contribution scope

Contributions are welcome for natural-language, cipher, deliberately deceptive, formal/generative, scribal-production and mixed-mechanism hypotheses, as well as stronger controls and null models. A readable output is not sufficient for a decipherment claim if the mapping has uncontrolled substitutions, anagrams, nulls, homophones, exceptions or context-dependent degrees of freedom.

## Data policy

Current analyses use ZL3b / EVA-derived material and independently maintained readings where phase-specific source authority permits. Third-party transcription text is not automatically redistributed. [`data/README.md`](data/README.md) documents provenance, expected identity and local setup.

## License and reuse

- **Software and code** — MIT License; see [`LICENSE-CODE`](LICENSE-CODE).
- **Original research text, reports, documentation, figures, tables and project-generated result files** — CC BY 4.0; see [`LICENSE-CONTENT`](LICENSE-CONTENT).
- **Third-party transcriptions, manuscript images, corpora and quotations** — remain under their original rights and terms.

See [`LICENSE`](LICENSE) for repository-wide scope.

## Citation

Machine-readable metadata is in [`CITATION.cff`](CITATION.cff).

## Status

Active research under Issue #88. The current executable frontier is **Issue #151 shared common-EVA edge-table consolidation**; see [`RESUME.md`](RESUME.md) and [`ROADMAP.md`](ROADMAP.md).