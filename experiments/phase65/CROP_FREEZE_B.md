# Phase 65B1 text-blind crop freeze

Status: **RECTANGLES FROZEN; awaiting GitHub Actions byte/hash materialization. No P25 association statistic has been computed.**

Normative authority: `PLAN_B.md`.

## What is frozen in this commit

`CROP_SPEC_B.json` fixes one integer `(x, y, width, height)` rectangle for every transcription-confidence-eligible V1-P25 object. The rectangles were selected on the exact Yale scans frozen by Phase65B0, using visible drawing/layout geometry only.

The crop objective is the largest practical axis-aligned region that stays inside one unambiguously attributable drawn plant object while stopping before associated label glyphs or a neighboring plant enters the rectangle. Because labels are physically adjacent to roots/stems, a crop need not contain the full drawn object; label exclusion takes precedence and the rectangle may retain only the clean morphology-bearing part of that object. This rule was fixed before any DINO embedding, string distance, correlation, retrieval score, or permutation statistic.

No unit is newly excluded by crop quality in the frozen rectangle set. The pre-existing confidence exclusion `L2.7 / f102v2.16` remains excluded before crop work.

Expected retained population after byte/hash verification:

- f100v: 13 = T 4 + M 5 + B 4
- f102v2: 11 = L2 6 + L3 5
- combined: 24/25

This clears the preregistered coverage firewall if source bytes and all crops verify.

## Mechanical materialization gate

`phase65b_crop_freeze.py` deliberately contains no text parser, DINO path, text-distance function, correlation, or permutation statistic. The workflow:

1. reads only the frozen Yale image identities from `SOURCE_MANIFEST_B.json`;
2. downloads and SHA-256 verifies the exact JPEG bytes;
3. applies the already-frozen rectangles;
4. writes PNGs and their SHA-256 hashes;
5. emits `CROP_MANIFEST_B.generated.json`;
6. checks the coverage firewall;
7. uploads all generated crops and manifest as an Actions artifact.

The generated manifest must be inspected and then promoted verbatim to `experiments/phase65/CROP_MANIFEST_B.json` before the synthetic-only implementation preflight. No scientific image↔label statistic is authorized by this commit.
