# Issue #26 experiment B — representation amendment B2

Status: **FROZEN BEFORE EXECUTABLE / SCIENTIFIC REVEAL**

`PLAN_B.md` intended the unigram and bigram blocks to have equal weight in the concatenated cosine representation, but "normalize each block to sum to 1, then multiply each by 1/sqrt(2)" does not by itself guarantee equal L2 block norm.

Before any executable or scientific output exists, operationalize the intended equal-block weighting as follows:

1. compute within-sign relative frequencies separately for unigram and bigram blocks (L1 sum = 1 when non-empty);
2. L2-normalize each non-empty relative-frequency block to unit norm;
3. multiply each block by `1/sqrt(2)`;
4. concatenate the blocks.

The resulting full vector has unit L2 norm and exactly half of its squared norm in each block. Primary cosine similarity is therefore an equal-weight average of unigram-block cosine and bigram-block cosine.

Unigram-only and bigram-only sensitivities use their own unit-L2 block vectors.
