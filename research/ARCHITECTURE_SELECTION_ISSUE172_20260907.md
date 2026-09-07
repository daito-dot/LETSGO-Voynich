# Architecture-class elimination under Issue #172

Date: 2026-09-07
Parent: Issue #172
Related exploratory note: Issue #179
Authority base: `e59013ea1f1152f63c30382be5470ebdf09a1964`
Status: **SELECTION / EXTERNAL-PREFLIGHT ONLY — NO NEW VOYNICH TARGET SCORING LICENSED**

## Decision point

Issue #176 calibrated the historical anchors under the frozen post-#88 contract. Neither A1/A1-R1 nor Naibbe C1-E0 is jointly competitive. Their strongest shared falsifier is R5/R6: both fail to reproduce positive same-line previous-terminal -> next-initial gain and instead retain unwanted continuation across source-line breaks.

This document performs architecture-class elimination only. It does not repair either historical anchor, combine their complementary PASS sets, fit a new Voynich model, or score any new candidate against R1-R10.

## Independent evidence gathered before any new target score

### Historical cipher baseline

Historical cryptography is independently relevant because 15th-century European cipher keys included simple substitution, homophonic substitution, nomenclatures/code elements and nulls. Large comparative work on more than 1,600 historical keys finds that simple substitution dominated 15th-century nomenclature tables, with more complex homophonic/polyphonic mixtures becoming more common later.

Sources:
- Megyesi et al., *Keys with nomenclatures in early modern Europe*: https://www.tandfonline.com/doi/full/10.1080/01611194.2022.2113185
- DECODE historical-cipher database: https://ecp.ep.liu.se/index.php/histocrypt/article/view/397

This gives a genuine historical control family, but it does **not** independently motivate a line-reset state channel. A fixed symbolwise substitution can preserve source dependencies under relabeling; it does not by itself explain why useful adjacent context should be localized to one physical manuscript line.

### Scribal abbreviation / allography / line management

Medieval manuscript production independently supplies a different mechanism class: surface form can vary with scribal context and page layout.

- The Library of Congress overview notes that medieval abbreviation systems were widespread, rule-governed but flexible, and could vary by scribe and text: https://guides.loc.gov/manuscript-facsimiles/deciphering-scribal-abbreviations
- An early-15th-century Wycliffite Bible study documents superscript-letter abbreviations, commonly word-final but also medial: https://czasopisma.kul.pl/index.php/LingBaW/article/view/5665
- The University of Nottingham palaeography guide documents positional abbreviation functions such as `con-/com-` initially and `-us`, `-is`, final `e` at word endings: https://www.nottingham.ac.uk/manuscriptsandspecialcollections/researchguidance/medievaldocuments/letterformsandabbreviations.aspx
- IRHT Codicologia records line-management devices such as moving a word/word portion when space runs out and compressing final letters as justification techniques: https://codicologia.irht.cnrs.fr/theme/liste_theme/332

The external evidence is enough to motivate a **layout-aware, context-sensitive scribal rendering family** independently of Voynich target scoring. It is not evidence that this is the Voynich mechanism.

### Mathematical representation

Finite-state transducers are an established formalism for context-conditioned morphological/allomorphic realization. This supplies a bounded mathematical implementation family without requiring an unrestricted latent-state search.

Source:
- Maxwell, *Accounting for Allomorphy in Finite-state Transducers* (FSMNLP 2015): https://aclanthology.org/W15-4809/

Short-term cache models are also independently established as a way to model recent-use recurrence (Kuhn & De Mori 1990), but **they are not admitted into the selected scribal candidate merely to repair R8**. Adding a cache after seeing the #176 failure vector would create exactly the sort of target-shaped composite that Issue #172 forbids.

## Architecture-class elimination

| Class | Independent motivation | R5 line-local edge/reset | R8 slow inventory | Decision |
|---|---|---|---|---|
| fixed monoalphabetic / homophonic substitution or nomenclator | strong historical | source-inherited only; no endogenous physical-line reset | source-inherited only | **ELIMINATE as standalone joint explanation; retain external control value** |
| Alberti-style periodic/polyalphabetic boundary mechanism | historical, but later than the main manuscript window in its documented Alberti form | can carry explicit reset state | source-inherited | **CLOSED for nearby rescue**: Phase71 already froze and rejected the tested Alberti boundary mechanism; no interval/signal retuning |
| token-only finite-state/slot generator with no cross-token state | mathematical | **cannot express R5 by construction** | cannot express R8 | **ELIMINATE** |
| continuous finite-order Markov stream with no layout/boundary input | mathematical | can express adjacency but has no principled physical-line reset | limited ordered history only | **ELIMINATE** |
| Voynich-derived copy/variation/self-citation generator selected because it resembles observed recurrence | target-derived | potentially | potentially | **DEFER / NOT ADMISSIBLE as first new family without independent external motivation** |
| layout-aware context-sensitive scribal rendering / bounded allographic transducer | historical scribal + mathematical | **structurally natural**: local rendering state may reset at physical line scope | not supplied by renderer alone | **CARRY FORWARD TO EXTERNAL PREFLIGHT ONLY** |
| cache-augmented line renderer assembled now to cover R5+R8 | components individually motivated | yes | yes | **REJECT AS CURRENT COMPOSITE**: joint form is target-shaped after reveal |

## Selected family for preflight, not yet tournament entry

Working identifier: **LM-A0 — line-managed allographic surface family**.

Primary role if later admitted: `SURFACE GENERATOR ONLY`.

LM-A0 is deliberately incomplete. It claims only that a bounded scribal rendering process may choose among surface realizations using local writing context and physical line/layout state. It is not given a hidden plaintext, a dictionary, a Currier repair table, a paragraph cache, or a decoder inverse.

### Immutable architectural commitments for preflight

Before any Voynich score:

1. local rendering state is bounded and explicit;
2. local state may be reset only by a predeclared physical-layout event, never by a string-similarity decision;
3. image/layout annotation is performed without consulting Voynich token similarity or candidate score;
4. no empirical target vocabulary lookup table;
5. no candidate-specific Currier x previous-terminal repair table;
6. no paragraph cache or long-history module in LM-A0 merely to satisfy R8;
7. any later target plan must charge image geometry, line masks, illustration masks, reading order and other layout metadata under R10;
8. LM-A0 is not a decoder candidate and receives no R9 promotion path in this form.

Because LM-A0 does not independently specify an R8-generating source process, it is **not currently eligible for `JOINT-STRUCTURAL COMPETITIVE` scoring**. If external preflight supports the mechanism class, a later selection step must either provide an independently grounded source-side mechanism before target reveal or retain LM-A0 only as a partial-mechanism candidate.

## External preflight required before Voynich scoring

The next executable work is comparative and target-free:

1. identify one or more externally documented medieval manuscript samples with preserved lineation and visible abbreviations/allographs;
2. freeze annotation categories before measuring surface associations;
3. test whether physical line position / available line space / line interruption predicts abbreviation or allograph selection in those external samples;
4. record whether the effect is line-local, word-local, or only manuscript/scribe-global;
5. if no reproducible layout-conditioned effect can be established, LM-A0 is not promoted;
6. if an effect is established, freeze a minimal LM-A1 architecture from the **external** evidence before any Voynich target score.

The DECODE corpus should separately be considered as a historical-cipher control source for real ciphertext line/boundary behavior. It is not evidence for LM-A0 itself.

## Prospective Voynich prediction reserved by Issue #179

Only after external preflight and a separate preregistration may the Issue #179 image-interruption discriminator be run.

The key comparison remains fixed conceptually:

- ordinary same-line adjacency;
- same-height text interrupted by an illustration and plausibly continuing on the other side;
- movement from an illustration-shortened line to the next physical line;
- ordinary line break without an illustration;
- independently recognizable paragraph/item boundary.

Two predictions must remain distinct:

- **physical-interruption version**: a genuine pen/layout interruption should reduce carryover even when text resumes at the same height;
- **physical-line-scope version**: same-height continuation across an illustration should retain more carryover than a move to the next physical line.

Reading order and interruption class must be frozen from image geometry, not chosen from the text. If sample support, reading order or confounding is inadequate, the correct result is `INDETERMINATE`, not equivalence.

## Selection outcome

Current outcome:

> **No new joint candidate is licensed for Voynich scoring yet.**

> **LM-A0 is the only architecture family carried forward, and only to an external scribal/layout preflight.**

This is a positive narrowing decision. Static substitution/nomenclator remains historically relevant but lacks endogenous explanatory reach for the line-local reset; the tested Alberti rescue lane is already closed; token-only and boundary-blind Markov classes are structurally inadequate; and a line-renderer+cache composite is explicitly rejected as post-reveal assembly.

## Completion gate for this selection stage

- [ ] external manuscript sample(s) identified with source/provenance and usable line/layout evidence;
- [ ] score-free annotation schema frozen;
- [ ] external preflight run and archived;
- [ ] LM-A0 either rejected or promoted to a separately frozen LM-A1 architecture;
- [ ] if promoted, target access / complexity / trainable components / hard failure conditions frozen before Voynich scoring;
- [ ] only then open a separate target plan under #172;
- [ ] #179 remains exploratory until that target plan exists.

No new Voynich candidate score was inspected in producing this selection document.
