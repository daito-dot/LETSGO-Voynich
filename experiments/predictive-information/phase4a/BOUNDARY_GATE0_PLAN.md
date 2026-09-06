# Issue #112 Phase 4A — raw boundary Gate 0

Date: 2026-09-06
Status: **FROZEN BEFORE P1/P2 SCORING**
Parent: Issue #88

## Purpose

Phase 4 asks whether the visible-space-delimited unit used by the predictive-information program is a reproducible production unit, without assuming that it is a natural-language word.

This Gate 0 freezes only the representation and candidate-event support. It must not fit the boundary model or compute P1/P2.

## Source authority

Primary transcription: Zandbergen-Landini ZL3b, IVTFF `Eva- 2.0`, exact authority already used by the project:

- Git blob SHA-1 `2a4533ab9bdfa85db9bad602d590978953055df1`
- SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`
- 411,671 bytes

The CI mirror is pinned to `matthewdgreen/cipher_benchmark@315f0cad4de3d021bd4185765c037cf2a28d341c` and must reproduce the Git blob identity above.

## Why a new raw representation is required

Historical token analyses normalize the IVTFF line and use the 12-slot parser. Phase 4 is a construct-validity challenge to those token units, so it would be circular to let SlotParser admissibility determine candidate boundaries.

The Phase-4A event extractor therefore reads the raw IVTFF P-locus bodies directly. Historical parsing is permitted only to reproduce the already-frozen five physical-leaf folds.

## Frozen space authority

The IVTFF/EVA documentation distinguishes:

- `.` — certain word space;
- `,` — uncertain word space;
- `<->` / `<~>` — drawing interruption; IVTFF 2.0 treats drawing interruption as implying a word space.

The primary ZL3b first reveal uses **literal `.` only** for `REAL_SPACE`.

`,` and drawing-interruption markers are not silently deleted or converted to primary boundaries. A certain-space token containing either is unclean and is excluded as a complete local unit. This deliberately trades sample size for a less editorially ambiguous primary population.

A later sensitivity arm may prospectively freeze uncertain/inferred boundaries, but it cannot alter the primary result.

## Frozen Basic-EVA atomizer

Phase 4A operates on transcription-shape atoms, not semantic characters.

The common EVA sequences conventionally written without explicit connectivity notation are longest-matched as single atoms:

`cfh`, `ckh`, `cph`, `cth`, `ch`, `sh`.

Every remaining lowercase Basic-EVA letter is one atom. EVA `w` is not in the frozen Basic-EVA inventory.

Examples:

- `qokchody` -> `q o k ch o d y`
- `cthaiin` -> `cth a i i n`
- `shckhey` -> `sh ckh e y`

This is a fixed transcription convention only. It does not claim that these atoms are linguistic letters, plaintext symbols, or the historically intended units.

## Unclean-token rule

A certain-space token is excluded in full if it contains any of:

- IVTFF uncertain word-space comma;
- `?` illegibility;
- alternatives `[...]`;
- explicit ligature notation `{...}`;
- high-ASCII `@...;`;
- inline comment or drawing/intrusion markup `<...>`;
- uppercase connectivity notation;
- apostrophe/tick notation;
- non-Basic-EVA lowercase letters or other exceptional symbols.

No exceptional material is deleted followed by concatenation of the remaining atoms.

Only the documented leading paragraph marker `<%>` and trailing locus marker `<$>` may be removed at their structural edge positions. They never create candidate boundaries.

## Frozen folds

Reuse the original five physical-leaf folds from `phase62b_n0.parse_voynich()` plus `physical_leaf_folds()`.

This old parser is used **only** to recover the previously frozen leaf membership. Its normalized tokens, SlotParser output, or parser coverage cannot affect Phase-4A event eligibility.

Events on leaves outside those frozen folds are not part of the primary evaluation population and are counted separately.

## REAL_SPACE population

For every literal `.` inside a P-locus physical line, let `L` and `R` be the immediately adjacent certain-space tokens.

The event is eligible iff:

- both `L` and `R` are clean under the frozen atomizer;
- `len(L) >= 2` atoms;
- `len(R) >= 2` atoms.

Gate 0 records exact event counts by frozen fold and Currier A/B authority, plus a hash of event identities. No atom probability is computed.

## MID_TOKEN population

Every clean certain-space token with at least four atoms contributes exactly one deterministic pseudo-boundary:

`cut = floor(n_atoms / 2)`.

At least two atoms must remain on each side. The cut may not move after any score is observed.

Gate 0 records the atom-length distribution and event-identity hash.

## P2 support population

P2 compares the same concatenated atoms under:

- `OBSERVED = L | R`
- `SHIFT_LEFT = L[:-1] | (L[-1:] + R)`
- `SHIFT_RIGHT = (L + R[:1]) | R[1:]`

To keep at least two atoms on every side under all three candidates, Gate 0 freezes P2 eligibility to REAL_SPACE events with:

- `len(L) >= 3`
- `len(R) >= 3`.

There is no STOP/end-of-token probability in Phase 4A; the later P2 scorer will code every atom exactly once and differ only in the BOS-reset position.

## Currier authority

For diagnostics only, read `$L=A/B` from raw page headers. Preserve the Phase-3A score-free fallback for the sole missing raw `$L` case: `f57v -> B` from its unambiguous adjacent same-source comment.

Currier labels do not affect primary eligibility or the Gate decision.

## Gate rule

Proceed only if all three populations have nonzero support in every one of the five frozen physical-leaf folds:

1. REAL_SPACE;
2. MID_TOKEN;
3. P2 REAL_SPACE.

If any cell is zero, stop before scoring and freeze a deterministic support repair prospectively. Do not regroup folds based on results.

## Required archive

The Gate JSON must record:

- exact ZL3b identities;
- atomizer definition;
- exact five-fold leaf identity and hash;
- REAL_SPACE / MID_TOKEN / P2 counts by fold;
- Currier diagnostic counts;
- clean atom inventory;
- MID source-token length distribution;
- all exclusion reasons;
- event-identity hashes;
- explicit firewall booleans.

## Firewall

This Gate must not:

- compute P1/P2 or any likelihood/code-length result;
- fit the Phase-4A boundary model;
- use SlotParser for atomization or event eligibility;
- inspect R1, LOCAL40, PREV, S1/S2/H62 or Issue #84 target values for selection;
- tune atomization, pseudo-cut location, folds, model order or smoothing;
- infer that spaces are natural-language words;
- infer plaintext, semantics, cipher identity, hoax/artificial generation, historical mechanism or latent states.

## After a PASS

Merge this Gate 0 before adding the P1/P2 scorer. The scoring PR must consume this frozen representation and event authority without changing it.

Refs #88, #98, #109, #112.
