# Research protocol

This document defines the methodological contract for the LETSGO-Voynich research program. It exists so that a new session can continue the work without silently changing what counts as evidence.

For research purpose and prioritization, `research/RESEARCH_OBJECTIVE.md` is normative. This protocol defines how evidence is tested; it does not make falsification itself the goal.

## 0. Research objective versus research method

The program seeks a constrained mathematical account of Voynich structure that can progressively approach explanatory reconstruction and, where possible, decipherment.

The working loop is:

1. identify reproducible structure;
2. find transformations or mechanisms that reproduce parts of it;
3. retain the parts that survive strong controls;
4. test whether those parts can coexist with meaningful information under constrained/reversible mappings;
5. when a sufficiently constrained reversible family exists, formulate and test the inverse problem on unseen Voynich material.

Falsifiable hypotheses, negative controls, held-out tests and model comparison are methods for keeping this search honest. They are not a target count to maximize.

A failed sufficient-model gate rejects sufficiency, not automatically every component of the model. A robust partial mechanism may remain useful as a transformation primitive, comparison tool, or component of a later model.

## 1. Claim ladder

Keep these levels separate:

1. **Observation** — a reproducible regularity exists.
2. **Structure** — the regularity belongs to a larger organized system.
3. **Mechanism** — a constrained process predicts or generates the structure.
4. **Content relation** — the structure predicts independently grounded manuscript content.
5. **Decipherment** — an executable mapping yields substantial fixed, interpretable prediction on unseen material.

Do not promote a claim merely because the lower-level result is statistically strong.

## 2. Falsifiability

Every serious hypothesis must say what would weaken or reject it. Preserve negative results in the ledger. Do not repeatedly modify a hypothesis after failures without recording the new degrees of freedom and treating the modified version as a new/nested model.

The aim is not to maximize rejections. State exactly what a failed test rejects: a complete model, a specific mechanism role, a parameterization, or a narrower prediction. Do not discard a partial mechanism merely because it is insufficient as a full explanation if its own prospective/held-out predictions remain supported.

Likewise, when a second mechanism reproduces the same statistic, downgrade the statistic's power to discriminate mechanisms; do not infer that the first mechanism has therefore lost all constructive value.

## 3. Validation vocabulary

Use explicit labels:

- training/development
- model selection
- exploratory analysis
- internal held-out validation
- prospective validation
- external replication

Do not use “independent validation” without saying independent in what sense.

If a target statistic, folio, document, label, visual pair, or control outcome was inspected before the rule/model was frozen, it is exposed for that purpose.

## 4. Null models

A null should preserve all structure that is not part of the hypothesis under test. Depending on the question this may include:

- whole-token identity/counts
- token length
- token-internal collapsed units
- line boundaries and line length
- first/middle/last line position
- slot occupancy/value constraints
- folio composition
- paragraph/item boundaries
- register/section
- Currier language / hand where available
- physical-page-order trends

Weak global shuffles are diagnostics, not automatically adequate inferential nulls.

## 5. State confounding

Local state is a default confound. Folio, register, section, paragraph/item, line position, scribe/hand, page order and document genre can create apparent semantic or cryptographic matches.

Where possible, semantic/content matching should compare correct vs wrong candidates within the same relevant state rather than compare a target to unrelated manuscript material.

## 6. Structural equivalence

Two glyphs/tokens/classes having similar contexts or compensating frequencies establishes structural equivalence only. It does not establish that they encode the same plaintext unit.

Promotion toward cipher equivalence requires either:

- prediction of independently grounded content, or
- successful transfer under a constrained encoder/mapping on material not used to construct the equivalence.

## 7. Cipher hypotheses

Systematic ciphers and deliberately deceptive/adversarial ciphers remain legitimate competitors.

A deceptive-cipher hypothesis must specify bounded nuisance capacity, for example:

- fixed/limited null rate
- homophony budget
- codebook size
- state-transition rule
- dummy morphology rule
- transposition budget
- context-conditioned mapping rule

Failure of a semantic test is not positive evidence for deception. The bounded cipher must predict held-out observations better than simpler alternatives after complexity charge.

When a cipher/surface transform is exactly reversible and reproduces supported Voynich structure, that construction should also be considered as a candidate inverse-problem family. Its value is not limited to serving as a null or competitor.

## 8. Generator hypotheses

Showing that a generator *can* reproduce one or two Voynich statistics is a mechanism demonstration, not evidence that it generated the manuscript.

A generator should be tested against a joint fingerprint. If mechanisms are added after observing failures, compare nested versions and charge incremental complexity using predictive code length / MDL or an equivalent predeclared framework.

Good code length alone is insufficient if the observed multivariate fingerprint lies outside the model's predictive distribution.

Failure of a generator as a sufficient manuscript-wide model does not erase a supported component mechanism. If a generator exposes a transformation principle that transfers to a reversible meaningful-text construction, retain that principle as an active transformation candidate and test whether it helps define a constrained inverse mapping.

## 9. External controls

Do not treat one document as representative of a language. Distinguish at least where possible:

- language
- genre/document function
- individual document
- chronology/script/scribe
- transcription convention
- abbreviation/expansion policy
- physical layout

Cross-script raw edit-distance statistics require special caution. Prefer matched token counts and length/alphabet/inventory-aware nulls and report representation choices.

## 10. Transcription

Transcription is an analysis layer, not manuscript ground truth. Important claims should eventually be checked against an independent transcription lineage or the manuscript images when feasible.

Always record preprocessing such as composite-unit collapse, uncertain-character handling, labels/body selection, and line-initial token exclusion.

## 11. Numerical and symbolic claims

Numerical, calendrical, astronomical or symbolic interpretations are late-stage hypotheses. First establish that the underlying recurrence/structure survives token-, boundary-, and state-preserving controls.

## 12. What counts as decipherment

A decipherment claim should provide:

- an executable fixed mapping or decoding procedure
- substantial prediction on unseen material
- interpretable output under rules fixed in advance
- explicit accounting of nulls, homophones, transpositions and exceptions
- strong alternative/null comparisons
- prospective validation or external replication
- documented errors and failure cases

A small number of readable phrases obtained after flexible mapping is not sufficient.

## 13. Reporting rule

For each experiment retain:

- question/hypothesis
- frozen versus explored choices
- input identity/provenance
- preprocessing
- exact metric
- null/control
- sample size/unit of analysis
- result and uncertainty
- limitations
- resulting hypothesis-status change
- highest-value next experiment, selected for expected progress toward the research objective; this may be a falsification/discrimination test, a constructive transformation test, an inverse/decoding test, or an external/content prediction test

Phase reports control exact numerical results. `research/STATUS.md` controls the current interpretation after later evidence.
