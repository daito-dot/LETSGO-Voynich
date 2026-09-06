# Issue #112 Phase 4A — raw boundary Gate 0 report

Date: 2026-09-06
Status: **PASS — scoring support is adequate**

## Question at this stage

Before asking whether a visible space behaves like a production reset, do we have a reproducible raw-transcription representation and enough prospectively defined events in every frozen held-out fold to run the test without post-hoc repair?

Answer: **yes**.

No P1/P2 likelihood or code-length result is present in this report.

## Representation frozen before scoring

The primary representation is intentionally conservative:

- source is exact ZL3b / IVTFF Eva-2 authority;
- REAL_SPACE uses literal `.` certain word spaces only;
- uncertain comma spaces and drawing-interruption/inferred spaces are excluded from the primary event population;
- common connected EVA forms `cfh`, `ckh`, `cph`, `cth`, `ch`, `sh` are longest-matched as one transcription-shape atom;
- remaining Basic-EVA lowercase characters are one atom each;
- alternative readings, uncertain readings, explicit ligature markup, high-ASCII symbols, inline comments/intrusions, uppercase connectivity and ticks make the complete local token unclean rather than being silently removed;
- only structural edge markers `<%>` and `<$>` may be stripped at their documented edge positions.

This representation is independent of the 12-slot parser. The old parser is used only to reproduce the already-frozen physical-leaf fold membership.

## Support

The raw audit processed all `4,119` P-loci represented in the frozen physical-leaf population.

Clean certain-space tokens: `28,052`.

Primary event counts:

- REAL_SPACE: `21,363`
- MID_TOKEN: `21,313`
- P2-eligible REAL_SPACE: `18,696`

Every population has substantial support in all five original folds:

| Fold | Clean tokens | REAL_SPACE | MID_TOKEN | P2 REAL_SPACE |
|---:|---:|---:|---:|---:|
| 0 | 4,932 | 3,685 | 3,682 | 3,240 |
| 1 | 5,440 | 4,171 | 4,224 | 3,675 |
| 2 | 6,174 | 4,717 | 4,616 | 4,176 |
| 3 | 6,039 | 4,623 | 4,591 | 4,016 |
| 4 | 5,467 | 4,167 | 4,200 | 3,589 |

Therefore no fold regrouping, support repair, threshold relaxation or alternative pseudo-boundary rule is licensed or needed.

## Diagnostic Currier support

Currier labels are diagnostic only and did not affect eligibility:

| Currier | Clean tokens | REAL_SPACE | MID_TOKEN | P2 REAL_SPACE |
|---|---:|---:|---:|---:|
| A | 8,478 | 5,898 | 5,721 | 4,942 |
| B | 19,107 | 15,141 | 15,276 | 13,491 |
| Unknown/other | 467 | 324 | 316 | 263 |

This confirms that a later secondary A/B diagnostic is not obviously support-starved, but the primary Phase-4A model remains unconditioned on Currier.

## Conservative exclusions

The main token-level exclusion counts include:

- uncertain comma space: `2,192`;
- inline/intrusion markup: `767`;
- alternative reading brackets: `645`;
- explicit ligature braces: `379`;
- illegible `?`: `184`;
- high-ASCII notation: `118`;
- apostrophe/tick: `90`;
- uppercase connectivity: `53`.

A clean token shorter than four atoms is retained for REAL_SPACE eligibility where possible but cannot supply the deterministic MID_TOKEN pseudo-boundary; `6,739` such cases were excluded from MID_TOKEN only.

For P2, `2,667` otherwise eligible real spaces lack the stricter >=3-atom support on both observed sides and are excluded prospectively.

## Gate classification

All frozen support predicates pass:

- REAL_SPACE nonzero in 5/5 folds;
- MID_TOKEN nonzero in 5/5 folds;
- P2 REAL_SPACE nonzero in 5/5 folds.

Classification:

> **PASS — PROCEED TO PHASE-4A P1/P2 FIRST REVEAL**

## What this does and does not mean

This Gate says only that the experiment is identifiable under the frozen representation with ample held-out support.

It does **not** show that spaces are production boundaries, words, semantic units, cipher groups or historically intended delimiters. The decisive next test is still blinded: train the fixed second-order raw-atom model on four folds, then test whether real spaces exhibit a greater reset advantage than deterministic internal cuts and whether the exact observed cut beats the two one-atom shifts.

If those tests fail under the frozen rules, the visible-space production-unit assumption must be weakened even though all earlier token-level predictive results remain numerically reproducible.

See `GATE0_PROVENANCE.md` for exact run/artifact/result hashes.

Refs #88, #112, #113.
