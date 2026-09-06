# Issue #112 Phase 4A — P1/P2 first-reveal plan

Date: 2026-09-06
Status: **FROZEN BEFORE P1/P2 SCORING**
Parent: Issue #88
Prerequisite: merged PR #113 score-free Gate 0

## Scientific question

Do visible certain spaces in ZL3b behave as reproducible production resets under a raw transcription-shape model, even if they are not natural-language word boundaries?

This phase tests only that construct-validity question. It does not search for a better tokenization or decipherment.

## Frozen event authority

The scoring executable must regenerate the merged Gate-0 populations from raw ZL3b and halt before model fitting if any identity differs.

Required identities:

- ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- fold identity SHA-256: `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`
- REAL_SPACE event hash: `45d456d106c96f3085774bfe3f2b8a4ed1c1a1bc70ae135215ea590d0039752c`
- MID_TOKEN event hash: `2e05e74a35d31391da976bb7a447694210a26e390397ecb738982cac4134b7af`
- P2 REAL_SPACE event hash: `ccd7efe6ce35b74fb41e227893d2bd972c2c4db60f9ae2c3830b38da6c45209b`
- counts: REAL `21,363`, MID `21,313`, P2 `18,696`.

Representation, certain-space authority, Basic-EVA atomization, exclusion rules, deterministic MID cut and P2 eligibility are exactly those merged in `BOUNDARY_GATE0_PLAN.md` and cannot change in this PR.

## Held-out design

Use the original five physical-leaf folds. For each outer fold `f`:

1. fit the raw-atom model only to clean certain-space token occurrences on the other four folds;
2. score only frozen events on fold `f`;
3. never use held-out scores to select an alphabet, order, smoothing parameter, event, threshold or stratum.

Each held-out event is scored exactly once by a model that did not see its physical leaf.

## Frozen raw-atom model

A single second-order conditional model:

`P(x_t | x_{t-2}, x_{t-1})`.

Training sequences are all clean certain-space tokens in the four training folds, regardless of token length. At the beginning of every token use context `(BOS, BOS)`. There is no STOP/end-token probability.

For each outer fold:

- target alphabet = atom types observed in its four-fold training population plus exactly one `OOV` target bucket;
- held-out atoms absent from the training alphabet map to `OOV` both as targets and when used as contexts;
- `BOS` is a context symbol only;
- smoothing is symmetric additive/Dirichlet `alpha = 0.5` over the training target alphabet plus OOV;
- no backoff, interpolation, order search, smoothing search or target-fold tuning is allowed.

For any mapped context `(u,v)` and target `x`:

`P(x|u,v) = (N(u,v,x)+0.5) / (N(u,v)+0.5*V)`

where `V` is the number of training atom types plus the OOV bucket. This also defines a uniform smoothed distribution for an unseen context.

## P1 — reset advantage contrast

For frozen event `... l[-2] l[-1] | r[0] r[1] ...`, score only the first two atoms to the right.

RESET:

- `r[0] | BOS,BOS`
- `r[1] | BOS,r[0]`

CARRY:

- `r[0] | l[-2],l[-1]`
- `r[1] | l[-1],r[0]`

Define event reset advantage:

`A = bits(CARRY) - bits(RESET)`.

Positive A favors a reset at the candidate cut.

Compute separately on frozen REAL_SPACE and MID_TOKEN events:

`D_RESET = mean(A_REAL) - mean(A_MID)`.

The pooled result is the mean over all held-out event scores, each produced by its own outer-fold model. Also report the five fold-specific contrasts.

Frozen P1 pass:

- pooled `D_RESET > 0`; and
- fold-specific `D_RESET > 0` in at least 4/5 folds.

No post-reveal minimum effect-size threshold may be added.

## P2 — exact observed cut versus ±1 atom

For each frozen P2 event with adjacent atom sequences L and R, code the same concatenated atoms under exactly three segmentations:

- `OBSERVED = L | R`
- `SHIFT_LEFT = L[:-1] | (L[-1:] + R)`
- `SHIFT_RIGHT = (L + R[:1]) | R[1:]`

Every segment is coded from `(BOS,BOS)` under the same outer-fold model. There is no STOP probability. Thus every candidate codes each atom in `L+R` exactly once and differs only in reset position.

Report paired event differences:

- `D_LEFT = bits(OBSERVED) - bits(SHIFT_LEFT)`
- `D_RIGHT = bits(OBSERVED) - bits(SHIFT_RIGHT)`.

Negative values favor the observed space.

A side passes iff:

- its pooled mean difference is `< 0`; and
- its fold-specific mean is `< 0` in at least 4/5 folds.

P2 passes only if both LEFT and RIGHT pass.

## Frozen classification

Apply exactly:

1. `SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY`
   - P1 passes and P2 passes both sides.
2. `SPACE MARKS A RESET BUT EXACT CUT IS WEAK`
   - P1 passes and P2 fails at least one side.
3. `SPACE POSITION IS LOCALLY PRIVILEGED WITHOUT RESET EVIDENCE`
   - P1 fails and P2 passes both sides.
4. `VISIBLE SPACE NOT SUPPORTED AS PRODUCTION BOUNDARY`
   - P1 fails and P2 fails at least one side.
5. `SUPPORT / REPRESENTATION INVALID`
   - merged Gate authority cannot be reproduced before fitting/scoring.

No post-reveal class may be added.

## Non-authoritative diagnostics

Report without changing the primary class:

- exact event counts and atom OOV rates by fold;
- Currier A/B P1/P2 summaries under the same unconditioned models;
- reset advantage by source/right-token atom length;
- no line-position diagnostic unless a separate score-free support rule is frozen before reveal. Phase 4A currently leaves line-position as `NOT_RUN` rather than inventing strata after scores exist.

## Interpretation firewall

A positive result can support visible spaces as reproducible production resets under this tested raw-glyph model. It cannot by itself establish that spaces are:

- natural-language words;
- semantic units;
- cipher groups;
- the historically intended segmentation.

It cannot identify plaintext, language, cipher family, author, hoax/artificial generation, historical mechanism or latent semantic state.

A negative result weakens the current one-production-episode-per-visible-unit interpretation and licenses a separately frozen alternative-segmentation program before latent-state work.

## First-reveal rule

The scientific executable and CI must be committed before any ZL3b P1/P2 result is inspected. The first successful CI artifact on that scientific head is authoritative. Later provenance/report commits may not alter the scorer; a rerun must reproduce the first-reveal JSON byte-for-byte.

Refs #88, #112, #113.
