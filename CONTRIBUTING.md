# Contributing to LETSGO-Voynich

This repository welcomes proposed decipherments, cipher systems, language identifications, generative explanations, structural analyses, control corpora, replications, and negative results.

## Core rule: make the claim falsifiable

A contribution should identify an observation that could count against the proposal. A system that can be changed after every mismatch is not yet a strong explanatory model.

For a proposed decipherment, please report:

- exact transcription and folios used
- symbol/token mapping rules
- all null characters, homophones, transpositions, anagrams, abbreviations, context rules, and exceptions
- which rules were fixed before examining the claimed reading
- what unseen material the system predicts
- what competing baseline it beats

## Claim ladder

Please distinguish these levels explicitly:

1. Observation — a reproducible pattern exists.
2. Structure — the pattern participates in a larger organization.
3. Mechanism — a constrained process can generate/predict it.
4. Content relation — the structure tracks independently grounded manuscript content.
5. Decipherment — an executable mapping predicts substantial unseen text with fixed interpretable output.

Evidence at one level does not automatically establish the next.

## Validation labels

Use the strongest label that is actually justified:

- exploratory
- model-selection / development
- internal held-out validation
- prospective validation
- external replication

If the evaluation material or target statistic was inspected before the model was frozen, say so.

## Controls

Where possible, preserve known structure in null models: token length, line boundaries, line position, folio composition, register/section, and other relevant constraints. A weak shuffle can make ordinary document structure look significant.

## Adversarial/deceptive cipher proposals

Deliberate deception is a legitimate hypothesis, but null results do not count as positive evidence for deception. Specify a bounded mechanism: e.g. fixed null rate, homophony budget, state transition, dummy morphology, or codebook rule. Complexity must be charged against simpler alternatives.

## Suggested PR contents

- `hypotheses/<name>.md` research note
- reproducible code under `experiments/` when needed
- compact result files rather than generated caches
- source/license information for any new corpus

English and Japanese are both welcome.
