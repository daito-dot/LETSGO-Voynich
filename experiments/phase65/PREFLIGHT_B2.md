# Phase 65B2 — synthetic-only implementation gate

Status: **PASS**.

The implementation gate was executed before any Phase65B P25 visual/text association metric was computed.

- workflow run: `33347367075`
- job: `99353959487`
- head SHA: `3c5806fba58e57e1d9e433b1b66e8ab2946a5b2f`
- artifact: `9742452641`
- artifact ZIP SHA-256: `072f8ab224d162a05e0c0c21fcb6c0fc736d31277de7d2846d8f688806b28e64`
- tested executable SHA-256: `eeb80238582466607988b0fe2c8e1b1ce1336a24fab775a37eabd166a59b8b63`
- DINOv2 weights SHA-256: `b938bf1bc15cd2ec0feacfe3a1bb553fe8ea9ca46a7e1d8d00217f29aef60cd9`

The synthetic gate verified the frozen EVA parser examples, normalized Levenshtein distance, pair-count weighted Spearman statistic, exact row-restricted permutation enumeration, and the pinned DINOv2 ViT-S/14 forward path. The synthetic null contained 36 exact joint assignments and recovered the expected one-sided exact p-value `1/36` for the constructed perfect-association fixture. DINO output dimension was 384 and both test embeddings had unit norm.

No P25 labels, P25 DINO embeddings, P25 text distances, P25 correlations, or P25 permutation statistics were read or computed by this gate.

The subsequent scientific executable is frozen separately before first reveal and must be used unchanged for both the f102v2 primary test and, conditionally, the f100v replication.
