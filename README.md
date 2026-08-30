# LETSGO-Voynich

Open research repository for testing hypotheses about the Voynich Manuscript.

**日本語での参加も歓迎します。**

This repository is not built around a claim that the manuscript has already been deciphered. The goal is to make proposed explanations testable, comparable, falsifiable, and reproducible.

> **Continuing the existing research? Start with [`RESUME.md`](RESUME.md).** It defines the reading order, source-of-truth hierarchy, current frontier, and rules that prevent exposed targets from being accidentally reused as prospective validation.

## What we are looking for

Contributions are welcome for:

- decipherment and cipher hypotheses
- candidate natural languages
- deliberately deceptive / adversarial encodings
- formal or generative models
- scribal-production hypotheses
- structural claims about tokens, lines, paragraphs, folios, sections, labels, diagrams, or illustrations
- negative results that eliminate plausible explanations
- better control corpora, null models, or evaluation methods

A useful hypothesis should state what evidence would make us reject or weaken it. A mechanism that can explain every possible outcome is not yet a strong decipherment hypothesis.

## Current competing explanation families

We currently keep several families open rather than assuming one answer:

1. meaningful natural-language text
2. encoded or deliberately obscured meaningful text
3. constrained formal / generative text
4. mixed mechanisms involving section, paragraph, line, scribal, or cipher state

The current research has found strong token-internal structure, line-position effects, document/section effects, local token-family organization, and paragraph-boundary effects. Some promising interpretations have failed stronger controls; those failures are retained rather than erased.

## How to propose a hypothesis

Open an Issue or submit a pull request. Please include, where applicable:

1. **Claim** — exactly what is proposed?
2. **Scope** — which folios, sections, labels, or transcription system?
3. **Prediction** — what should we observe if it is true?
4. **Falsification condition** — what result would weaken or reject it?
5. **Data selection rule** — was the evaluation material selected before or after seeing the result?
6. **Baseline / control** — what simpler explanation does it outperform?
7. **Reproduction** — code, data provenance, parameters, seeds, and commands where possible.

Readable output alone is not enough. If a proposed decipherment uses unconstrained substitutions, anagrams, null characters, homophones, exceptions, or context-dependent rules, please make those degrees of freedom explicit so they can be compared with simpler alternatives.

## Research records

- `RESUME.md` — deterministic restart/handoff entry point
- `RESEARCH_PROTOCOL.md` — methodological and evidence contract
- `research/STATUS.md` — current accepted state and research frontier
- `research/hypothesis-ledger.md` — hypotheses including negative results
- `research/CHECKPOINT_JA.md` — Japanese handoff/checkpoint
- `experiments/` — analysis archive and result files
- `data/README.md` — transcription provenance and setup

## Evidence labels

We distinguish:

- **Exploratory** — discovered after inspecting the target data.
- **Mechanism demonstration** — shows that a mechanism can reproduce a feature, not that the manuscript used it.
- **Held-out / prospective** — rules fixed before evaluating the held-out material.
- **External replication** — reproduced using genuinely independent data or transcription where applicable.

Negative results stay in the repository because they constrain the search space.

## Data policy

The current analyses use ZL3b / EVA-derived transcription material. Third-party transcription text is not automatically redistributed here. `data/README.md` documents provenance, expected file identity, and local setup. Contributions of external corpora should include their source and license.

## Language

Issues, discussions, research notes, and pull requests are welcome in English or Japanese.

## Status

Active research. The benchmark suite and historical experiment archive are currently being consolidated into this repository.
