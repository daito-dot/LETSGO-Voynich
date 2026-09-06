# Issue #112 Phase 4A — P1/P2 first-reveal provenance

Date: 2026-09-06
Status: **AUTHORITATIVE FIRST REVEAL — COMPLETE**

## Scientific head

The first ZL3b P1/P2 target reveal was executed from PR #114 at the exact pre-result scientific head:

- commit: `aa03be358a102e032f187bdc22e6922aa44a4690`
- workflow: `Issue112 Phase4A P1-P2 first reveal`
- workflow run: `34024401543`
- conclusion: `success`
- artifact: `9986578674` (`issue112-phase4a-first-reveal`)
- artifact ZIP digest: `sha256:1f61c4c2f07dcb536ec18350740b52fd90c5cf43d1a248faa1060738f4eb9655`
- `phase4a_first_reveal.json` SHA-256: `62c74f7d104c46f0b2fdd29973b08bae5047f3da3f1b7441ad61dbe38ce69e3c`

No P1/P2 ZL3b result was inspected before this PR/head was created and its CI run started.

## Frozen authority reproduced before scoring

The executable halted before model fitting unless the merged Gate-0 authority reproduced exactly.

Reproduced:

- ZL3b Git blob: `2a4533ab9bdfa85db9bad602d590978953055df1`
- ZL3b SHA-256: `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- fold identity SHA-256: `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`
- REAL_SPACE event SHA-256: `45d456d106c96f3085774bfe3f2b8a4ed1c1a1bc70ae135215ea590d0039752c`
- MID_TOKEN event SHA-256: `2e05e74a35d31391da976bb7a447694210a26e390397ecb738982cac4134b7af`
- P2 event SHA-256: `ccd7efe6ce35b74fb41e227893d2bd972c2c4db60f9ae2c3830b38da6c45209b`
- counts: REAL `21,363`, MID `21,313`, P2 `18,696`.

Only after these checks did the five outer-fold models fit.

## Frozen classification

Authoritative classification:

> **SPACE IS A REPRODUCIBLE PRODUCTION BOUNDARY**

### P1 reset contrast

- pooled mean reset advantage at REAL_SPACE: `+2.7386509712 bits/event`
- pooled mean reset advantage at MID_TOKEN: `-6.0732544538 bits/event`
- pooled `D_RESET`: `+8.8119054250 bits/event`
- fold values: `+8.5561434879`, `+8.4585153024`, `+8.9749576101`, `+9.0476322316`, `+8.9490391234`
- positive folds: `5/5`
- frozen P1 gate: **PASS**.

The scored event contains exactly the first two atoms right of the candidate cut. Positive reset advantage means `(BOS,BOS)` reset contexts code those atoms better than carrying the two atoms from the left.

### P2 exact-cut challenge

Observed minus one-atom-left-shift code length:

- pooled: `-8.5018034591 bits/event`
- folds: `-8.4881126727`, `-8.5837221133`, `-8.3735373161`, `-8.7533846018`, `-8.2980131660`
- observed wins: `5/5` folds.

Observed minus one-atom-right-shift code length:

- pooled: `-5.4766018554 bits/event`
- folds: `-5.0612382263`, `-5.4605114894`, `-5.4825823881`, `-5.8315033000`, `-5.4639663991`
- observed wins: `5/5` folds.

Both frozen P2 sides: **PASS**.

## OOV diagnostic

The result is not driven by held-out alphabet failure. Training folds contained 30–31 atom types. P2 held-out atom OOV fractions by fold were approximately:

- fold0 `0.000126`
- fold1 `0.0000822`
- fold2 `0.0000246`
- fold3 `0`
- fold4 `0`.

P1 target OOV was likewise negligible.

## Currier diagnostic — non-authoritative

The same unconditioned models show the same direction in both major Currier regimes:

- Currier A: `D_RESET = +8.0129766703`; P2 left `-7.6717576096`; P2 right `-4.6167757601` bits/event.
- Currier B: `D_RESET = +9.1543329780`; P2 left `-8.8494330085`; P2 right `-5.8059322255` bits/event.

These are secondary diagnostics and do not change the primary frozen class.

## Claim boundary

The frozen label means that, under the predeclared raw-EVA second-order held-out test, literal certain spaces behave as reproducible morphotactic/context-reset boundaries and their exact observed location is strongly preferred to a one-atom shift in either direction.

It does **not** establish that visible-space units are natural-language words, semantic units, plaintext groups, a specific cipher unit or the historically intended conceptual unit. No language, plaintext, cipher family, author, hoax/artificial origin, historical mechanism or latent semantic state is identified.

Refs #88, #112, #113, #114.
