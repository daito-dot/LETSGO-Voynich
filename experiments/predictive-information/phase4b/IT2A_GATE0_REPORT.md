# Issue #115 Phase 4B — IT2a boundary Gate 0 report

Date: 2026-09-06
Status: **PASS — independent-reading support is adequate**

## Result

The independent Takahashi/IT2a reading is a valid target for the prospectively frozen Phase-4 boundary replication.

No IT2a boundary likelihood or P1/P2 score has been computed at this stage.

## Authority

The canonical IT2a source is still byte-for-byte identical to the authority previously frozen for independent-transcription work. It also covers the same 99 physical leaves and reproduces the original five-fold identity.

The Phase-4 representation was not modified after seeing the ZL3b result: literal certain `.` spaces, the same connected-composite raw-EVA atomizer, the same conservative exceptional-token exclusions, deterministic midpoint pseudo-boundary and the same P2 support rule.

## Population

IT2a supplies more scoreable Phase-4 events than ZL3b under the same conservative representation:

| Population | ZL3b | IT2a |
|---|---:|---:|
| clean tokens | 28,052 | 32,956 |
| REAL_SPACE | 21,363 | 27,436 |
| MID_TOKEN | 21,313 | 24,239 |
| P2 REAL_SPACE | 18,696 | 23,379 |

All three IT2a event populations have thousands of examples in every original leaf fold. No support repair, fold regrouping or rule relaxation is required.

## Source differences visible before scoring

The main conservative IT2a exclusions are modest:

- 71 token occurrences containing `?`;
- 697 certain-space segments containing inline/drawing markup;
- 2 uppercase-connectivity cases;
- 8,717 clean tokens shorter than four raw atoms, which remain usable for REAL_SPACE where supported but cannot supply MID_TOKEN events.

The clean atom inventory remains an EVA-family inventory. Rare atoms include `z=1`, `x=24`, `g=66`; this will be handled by the already-frozen training-alphabet + OOV rule rather than by deleting rare atoms.

## Gate classification

- exact source authority — PASS
- exact fold authority — PASS
- REAL_SPACE support 5/5 — PASS
- MID_TOKEN support 5/5 — PASS
- P2 support 5/5 — PASS
- score-free firewall — PASS

> **PASS — PROCEED TO IT2a P1/P2 FIRST REVEAL**

The next PR must regenerate the three event hashes before model fitting and then apply the identical Phase-4A model/metrics/classification once.

Refs #66, #88, #112, #115, #116.
