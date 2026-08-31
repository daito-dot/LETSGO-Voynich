# Content-relation program status — 2026-08-31

This file is a current-state addendum for the object/content program that advanced beyond the older `research/STATUS.md` narrative. Phase-specific frozen plans/results/reports remain authoritative for exact methods and numbers.

## Accepted high-level content state

The pharmaceutical image↔text program now has a calibrated positive control plus repeated Voynich nulls across several representational levels.

Retain:

> The tested pipeline can detect genuine image↔description morphology correspondence in an external botanical control, but no replicated/direct object-local relation has been detected between the sealed Voynich pharmaceutical morphology and its short attached label or immediately following body text under the tested surface, formal-residual, or lexical representations.

Do **not** convert these nulls into “the pictures are unrelated to the text” or “Voynichese has no semantics.” The tests address local surface/structural correspondence for visible morphology.

## Phase65A — localized anchors

- 25 physically localized pharmaceutical plant-fragment ↔ adjacent-label loci were frozen without using Voynichese similarity.
- 24 confidence-eligible units entered Phase65B/66 science.
- This removed the previous external-localization blocker.

## Phase65B — whole-image similarity vs label form

No replicated whole-crop visual-similarity ↔ attached-label-form relation was detected on f102v2/f100v.

This motivated morphology-first decomposition rather than further holistic image-distance tuning.

## Phase66A/B — explicit morphology/color vs short labels

Image side was frozen before label association using an externally grounded botanical morphology schema plus independently normalized color features.

Phase66B result:

- f102v2 primary: `T = 0.00301060073648908`, exact `p = 0.4896875`;
- f100v replication: `T = -0.15277449822904368`, exact `p = 0.7352719907407408`;
- classification: **M8-B2 NO DETECTED ATTRIBUTE-LABEL RELATION**.

Therefore the tested leaf morphology/color representation does not predict generic surface structure of the short attached labels.

## External botanical positive control

A separately constructed known-positive test used historical botanical plates and their body descriptions with the same coarse leaf-state vocabulary.

The control showed strong image↔description correspondence. This matters because it demonstrates that the morphology coding/comparison machinery is capable of recovering genuine correspondence when the description directly encodes the visible attributes.

The control does not identify Voynich plants and is not evidence for a specific plaintext.

## Phase67A — leaf morphology vs following body paragraph

Fourteen objectively delimited Quire 19 illustration-block → immediately following body-paragraph pairs were frozen before association.

After within-folio control:

- winner: leaf margin;
- maxT `0.651104888344988`;
- exact global `p = 0.19791666666666666`;
- coverage-residualized global `p = 0.53125`;
- classification: **NOT SUPPORTED**.

The predeclared n=1,2 sensitivity also failed (`p = 0.15625`).

## Phase67B — root/subterranean architecture vs body paragraph

Because many Quire 19 pharmaceutical fragments are root/storage dominant, Phase67B tested the already-frozen root/subterranean character rather than repairing Phase67A leaf states.

Result:

- RV `0.612879...`;
- exact `p = 0.418403...`;
- observability-residualized `p = 0.471354...`;
- classification: **NOT SUPPORTED**.

## Phase67C — morphology vs text after formal-channel masking

To test whether the strongest known formal layer was hiding content correspondence, paragraph tokens compatible with two already-established channels were masked before image↔text association:

1. paragraph line-0 entry-register tokens;
2. outside line 0, tokens exactly one edit away from one of the previous ten cleaned folio tokens.

Mask strength:

- cleaned tokens: 685;
- entry masked: 107;
- local edit1 masked: 155;
- retained innovations: 423 (61.75%).

Result:

- winner: leaf margin;
- maxT `0.5776971295416312`;
- exact `p = 0.6571180555555556`;
- retention-residualized global `p = 0.9557291666666666`;
- n=1,2 sensitivity `p = 0.7543402777777778`;
- classification: **NOT SUPPORTED**.

Thus removing tokens directly compatible with the strongest entry/local formal channels did not reveal a local morphology↔character-surface relation.

## Phase68A — morphology vs formal-residual lexical/family selection

Phase68 moved above character n-grams. It tested whether sealed morphology predicts:

1. exact recurrent retained-token identities;
2. exact-or-edit1 neighborhoods around recurrent retained-token anchors.

Text representation was feasible:

- retained tokens: 423;
- retained distinct types: 279;
- recurrent exact vocabulary (paragraph DF>=2): 59;
- both lexical lanes nonzero in 14/14 paragraphs.

Eight-way maxT result:

- winner: leaf arrangement × edit1-anchor family;
- maxT `0.5201980385567532`;
- exact global `p = 0.9939236111111112` (1,145/1,152 null assignments at least as large);
- retention-residualized global `p = 0.8498263888888888`;
- classification: **NOT SUPPORTED**.

This is a strong negative for further tokenization/morphology/similarity tweaking on the same 14 object-local pairs. That population is now considered exhausted for that style of post-hoc representation search.

## Phase69A — meaningful plaintext + adaptive homophonic surface

The program then changed scientific model rather than changing image/text features.

P69-C2-LH1 asked whether fully reversible meaningful Latin plaintext can acquire the A1-like short-range recurrence geometry when a valid homophone is selected to be edit1-close to recent ciphertext.

The exact edit1-context choice rule is an experimental modern mechanism, not historically attested.

Raw reversibility:

- 172,958 plaintext units across the frozen panel/realisations;
- LH0 decode accuracy = 1.000;
- LH1 decode accuracy = 1.000.

The local rule had an opportunity on 54.41% of plaintext units.

Paired LH0 control:

- S1 ratio `-0.05585×`;
- S2 ratio `-0.04196×`;
- S3 ratio `0.52639×`;
- mean H62 D `1.59850`;
- mean C-short error `0.98439`.

Adaptive LH1:

- S1 ratio **0.11334×**;
- S2 ratio **6.21358×**;
- S3 ratio **0.56827×**;
- mean H62 D **0.68873**;
- median H62 D **0.78332**;
- mean C-short error **0.24909**.

The preregistered local-mechanism check passed all three directions relative to LH0. LH1 beats N0 and C0 5/5 folds on both H62 diagnostics. It is even better than A1-R1 on mean/median H62 profile distance and wins D in 3/5 folds, although it is worse than A1-R1 on C-short magnitude.

Frozen classification:

> **C2-LH1 LOCALITY-ONLY PARTIAL**

Interpretation:

> A strong A1-like short-range recurrence profile is compatible with exactly recoverable meaningful plaintext under a context-dependent surface encoder. Therefore the recurrence evidence by itself does not imply semantic-free generation. This specific encoder is not a full Voynich model: it massively overproduces S2 and reproduces only ~0.11× of the paragraph-entry effect.

A blinded routing decision committed before the Phase69 result forbids tuning history length, edit distance, or local-selection strength after seeing this overshoot.

## Current frontier — Phase70

The next test is explicitly **not** another independent cipher challenger and not a Phase69 repair.

Phase70 asks a logical compatibility question:

> Can the already-frozen A1 entry/local surface parameters operate over a uniquely reversible meaningful-plaintext homophonic code while the ciphertext still enters the same broad held-out structural regime?

This construction is allowed to borrow frozen A1 training-side parameters because any positive result will be interpreted only as **semantic compatibility of the formal layer**, not as independent evidence for the historical cipher.

If it passes, structural A1 evidence and meaningful plaintext are demonstrably compatible. If it fails, the semantic constraints imposed by this fixed reversible codebook are too restrictive for the current A1 surface selector.
