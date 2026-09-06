# Issue #139 Gate0 — code authority

Date: 2026-09-07
Status: **FROZEN BEFORE ANY ISSUE #139 EDGE SCORE**

This file is part of the score-free replication contract. Gate0 must refuse to proceed if any of these repository blobs differ.

- Phase63B W1 / IT2a IVTFF parser: `experiments/phase63/phase63b_common.py`
  - Git blob SHA-1: `99cc6d49669c67432b4798b81c8250a17b3fbb38`
- SlotParser authority used by Issue #125: `experiments/issue26-music/issue26e_core.py`
  - Git blob SHA-1: `8bafba7f2bce4cf77c9001c729936c1ce619759b`
- archived independent-transcription authority: `experiments/occupancy-graph-independent-transcription/source-audit/issue66_source_audit.json`
  - Git blob SHA-1: `85c172c113927b91215463ee9297630580b57769`
  - file SHA-256: `bed86e92fcb854b614dfb474cd3bab9e6fc1e5746399fc14bced9f8e4448eddf`

The IT2a source itself remains frozen separately by the plan at SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5` and Git blob SHA-1 `4d6d3f2537b1f507a257529b49c94af7d6e03446`.

This authority fixes transport and parsing semantics only. It contains no POS2/EDGE2 probability, log likelihood, bits/token, edge gain, or scientific classification.
