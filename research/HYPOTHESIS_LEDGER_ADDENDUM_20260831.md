# Hypothesis ledger addendum — Phase66 through Phase70

Date: 2026-08-31

This addendum records hypotheses introduced after the older `research/hypothesis-ledger.md` frontier. Phase-specific frozen plans/results remain the exact authority.

## P66-B2 — explicit pharmaceutical morphology/color predicts attached-label structure

Prediction before association:

- a frozen botanical morphology + normalized color representation should have a positive object-level relation to independently frozen generic attached-label structural distance if short labels directly encode these visible attributes in a surface-correlated way.

Falsification:

- preregistered page statistic fails effect/p gate on primary and replication.

Result:

- f102v2 primary T `0.00301060073648908`, p `0.4896875`;
- f100v replication T `-0.15277449822904368`, p `0.7352719907407408`.

Status: **FALSIFIED FOR TESTED REPRESENTATION — NO DETECTED ATTRIBUTE-LABEL RELATION**.

Does not falsify plant names, semantics, cipher/shorthand, or non-surface-correlated labels.

## P66-CONTROL — same morphology coding detects known image↔description correspondence

Prediction:

- in an ordinary historical botanical work where text actually describes depicted morphology, image-only leaf states and independently coded body-description states should correspond above random pairing.

Result:

- known-positive control strongly positive under the frozen coarse leaf-state framework.

Status: **SUPPORTED AS PIPELINE CALIBRATION**.

Implication:

- later Voynich nulls cannot be dismissed simply as a detector incapable of recovering any genuine morphology correspondence.

## P67-A — leaf morphology predicts immediately following body-paragraph surface

Prediction:

- after objective block→paragraph pairing and within-folio control, block distributions of leaf composition/arrangement/margin should predict paragraph character-ngram structure if the local body directly tracks those visible attributes at surface level.

Result:

- maxT `0.651104888344988`, exact p `0.19791666666666666`;
- observability-residualized p `0.53125`.

Status: **NOT SUPPORTED**.

## P67-B — root/subterranean morphology predicts body-paragraph surface

Reason for new hypothesis:

- many pharmaceutical fragments are root/storage dominant; root architecture was already a frozen external morphology character before Phase67.

Result:

- root RV about `0.612879`;
- exact p about `0.418403`;
- residualized p about `0.471354`.

Status: **NOT SUPPORTED**.

## P67-C — morphology signal appears after masking established formal channels

Prediction:

- if A1-like paragraph-entry/local-family structure masks content, removing entry line0 tokens and previous-10 edit1-compatible body tokens may reveal morphology↔remaining-text surface dependence.

Intervention:

- 685 cleaned tokens;
- 107 entry masked;
- 155 local-edit1 masked;
- 423 retained.

Result:

- maxT `0.5776971295416312`;
- exact p `0.6571180555555556`;
- retention-residualized p `0.9557291666666666`.

Status: **NOT SUPPORTED**.

## P68-A — morphology predicts formal-residual lexical/family selection

Prediction:

- even if character-level surface is formally constrained, different visible morphology may select different recurrent exact token identities or edit1 lexical neighborhoods among the 423 retained tokens.

Feasibility:

- 279 retained distinct token types;
- recurrent DF>=2 anchor vocabulary = 59;
- both text lanes nonzero 14/14 blocks.

Result:

- eight-way winner leaf arrangement × edit1-anchor family;
- maxT `0.5201980385567532`;
- exact p `0.9939236111111112`;
- retention-residualized p `0.8498263888888888`.

Status: **STRONGLY NOT SUPPORTED**.

Stop implication:

- do not continue tokenization/morphology/similarity redesign on the same 14 object-local image↔paragraph pairs. New content tests must change the scientific model.

## P69-C2-LH1 — meaningful plaintext can generate A1-like locality through context-adaptive homophones

Prediction:

- relative to a paired weighted-homophone control, preferring valid ciphertext homophones that are edit1 to the previous ten ciphertext tokens should increase S2 and reduce H62 D/C-short mismatch while preserving exact plaintext reversibility.

Historical status:

- homophonic substitution is historically grounded;
- the exact recent-ciphertext edit1 choice rule is **not** historically attested and is charged as a new mechanism.

Result:

- raw decode accuracy = 1.000 both arms;
- local opportunities on 54.41% of units;
- preregistered causal mechanism check passed all directions;
- LH1 S1 ratio `0.11334×`;
- LH1 S2 ratio `6.21358×`;
- LH1 S3 ratio `0.56827×`;
- H62 mean D `0.68873`;
- H62 mean C-short error `0.24909`;
- beats N0/C0 5/5 on both H62 diagnostics;
- better than A1-R1 on mean/median H62 D and D wins 3/5, but worse on C-short magnitude;
- full exposed gate fails because locality is far too strong and entry too weak.

Status: **SUPPORTED FOR LOCAL MECHANISM COMPATIBILITY; C2-LH1 LOCALITY-ONLY PARTIAL AS A FULL MODEL**.

Key promotion:

> A strong A1-like short-range recurrence profile is compatible with fully reversible meaningful plaintext. Therefore recurrence evidence alone does not identify a semantic-free generator.

Bounded failure:

> this exact adaptive cipher is not a complete Voynich model; it overproduces S2 and lacks the paragraph-entry system.

Post-result tuning of LH1 history length/edit distance/local strength is prohibited by the blinded routing freeze.

## P70-SC1 — frozen A1 formal surface is compatible with reversible meaningful plaintext

Status: **FROZEN / RUN PENDING**.

Question:

- use the already selected Phase61C fold-specific A1 entry strength/local probability as a surface-selection layer over the fixed uniquely reversible Naibbe homophone candidate sets for meaningful Latin plaintext;
- no parameter is fit to Phase69 outcomes;
- determine whether the resulting ciphertext enters the same broad held-out S1/S2/S3 + H62 regime.

This is an A1-semantic-compatibility construction, not an independent cipher challenger.

Falsification:

- exact reversibility fails;
- or SC1 does not causally improve paired semantic SC0 in the preregistered entry/local/H62 directions;
- or full broad regime gate fails.

Allowed positive claim only:

> the strongest currently supported formal layer can coexist constructively with recoverable meaningful plaintext.

Not allowed:

- historical cipher identification;
- Latin plaintext claim for Voynich;
- glyph meaning;
- decipherment.
