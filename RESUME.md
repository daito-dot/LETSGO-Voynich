# RESUME — how to restart this research

This file is the entry point for a new researcher or a new AI/chat session continuing the project.

## Read in this order

1. `README.md`
2. `RESEARCH_PROTOCOL.md`
3. `research/STATUS.md`
4. `research/hypothesis-ledger.md`
5. `research/CHECKPOINT_JA.md` if Japanese context is useful
6. the report/README for the current active phase under `experiments/`
7. the scripts and result files for that phase before modifying the interpretation

Do not reconstruct the project from chat history if the repository contains a newer state.

## Authority hierarchy

When sources disagree:

1. **phase-specific report/result file** controls the exact method, sample, statistic, and numerical result for that experiment;
2. **`research/STATUS.md`** controls the current accepted interpretation after later evidence;
3. **`research/hypothesis-ledger.md`** controls hypothesis status/history and must preserve negative results;
4. **`research/CHECKPOINT_JA.md`** is a human-readable handoff, not numerical authority;
5. old chat summaries, comments, filenames, and memory are non-authoritative if contradicted by repository evidence.

Never silently replace an exact phase result with a later approximate summary.

## Current frontier

At the time this file was created, the active frontier is **Phase 52: document / genre confounding**.

Reason: medieval Latin controls show substantial document-to-document variation, and Voynich itself has substantial section variation. Before adding more mechanisms to a hierarchical formal generator, determine how much of the fingerprint can arise from practical/technical manuscript genre, document identity, scribal/transcription conventions, and section structure.

The next planned generator work becomes the following phase only after the genre/document confound is sufficiently characterized.

## Immediate Phase 52 work

Expand the medieval Latin panel, preferably within a common transcription framework, with multiple documents per relevant genre. Prioritize:

- medical
- recipe / pharmacological
- herbal if machine-readable material is available
- scholastic / commentary
- ecclesiastical
- literary/continuous prose baseline
- other strongly templated/list-like practical texts

Record source-native structural boundary type explicitly: prose paragraph, recipe/item, herb entry, chapter/section, list item, etc. Do not call all of them paragraphs.

Use matched token counts and, when controls lack manuscript lineation comparable to Voynich, deterministic/sensitivity line wrapping based on the empirical Voynich line-length distribution. Bootstrap at document/folio level rather than treating tokens as independent observations.

Primary comparison targets include:

- edit-distance-1 type-family density
- local previous-10 near-family excess under structure-aware nulls
- paragraph/item-boundary reset
- Phase47 operation decomposition: substitution/insertion/deletion
- Phase47 zone decomposition: initial/medial/final
- line-position mutual information
- relevant token-internal positional statistics where representation is comparable

Separate language, genre, individual-document, chronology/script, and transcription/abbreviation effects as far as the corpus allows.

## Frozen methodological constraints

- Phase52 targets already inspected are **exposed**. They may guide model development but cannot later be relabeled prospective validation.
- A new generator feature motivated by a known failure pays complexity cost.
- Search/tuning freedom belongs inside model selection or the null; it cannot be hidden in the final score.
- Local/folio/register state is a default confound.
- Semantic tests should compare correct vs wrong content within the same relevant state where possible.
- Structural equivalence is not semantic or cipher equivalence.
- Deliberate deception is allowed as a hypothesis only as a bounded mechanism; failed semantic tests are not positive evidence for deception.
- Numerical/symbolic interpretation comes late, after robust structural/content linkage.

## After Phase 52

Compare nested formal generators rather than jumping directly to a complex model:

- M0 — frozen Phase50 finite-state DSL
- M1 — M0 + explicit line-position process
- M2 — M0 + paragraph/item latent-state reset
- M3 — M0 + both mechanisms in a hierarchy

Conceptual architecture:

`document/global grammar -> paragraph/item state -> line state/position -> token family -> surface token`

Charge incremental description/model cost and compare held-out predictive code length / MDL plus multivariate fingerprint adequacy. The dimensions used to choose M1/M2/M3 are development targets, not independent validation.

## Before declaring decipherment

Require an executable mapping/generation rule, substantial prediction of unseen material, fixed interpretable output, strong structure-preserving nulls and competitors, prospective or external replication, and explicit accounting of failures/exceptions.

## Session behavior

When asked simply to “continue”, execute the current frontier rather than only describing the next step. Update durable repository records when the accepted interpretation changes. Stop only at a genuine decision point, external blocker, or result that requires choosing between materially different research branches.
