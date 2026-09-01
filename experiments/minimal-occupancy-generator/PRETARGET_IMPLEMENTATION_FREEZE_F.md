# Issue #75 Phase F — pretarget implementation freeze

Date: 2026-09-02  
Status: **SCORER / AGGREGATE / CANDIDATE-SMOKE FROZEN BEFORE TARGET ACCESS**

## Frozen candidate authority

Phase F1:

- run `33551369264` — success;
- generation head `fa5be15c65dd9d75e6aadef2dc81c8c49919920f`;
- artifact ID `9817561974`;
- artifact digest `sha256:d776da6c8d9d2573e9fa33e1f839df0330b9a33beb768d069c7fe9a20c9b14be`;
- F1 authority SHA-256 `de7976ca1c3e047c7c6f6bb50facdab797449ba81496312526917673a98661f3`;
- permanent evidence commit `b4c34ccd0d80267ef56579438e77a11703956470`;
- 31/31 frozen candidate corpora;
- target access zero;
- Phase-F refitting zero;
- drops zero;
- rerolls zero.

Frozen endpoint occupancy SHAs:

- rep 0 `8a7b2a41bf95d865bf50714c43d582f2c51c4da905c00e8cc0a19d775580351e`;
- rep 30 `c9b3d4dde6946ab0462a4526a7b9acd995e648362940ad79a063203cb89bd324`.

## Frozen scorer

File:

`experiments/minimal-occupancy-generator/phase75f_score.py`

- commit `d706ac13d44e22ea8db2a725edb06c1f30ce7214`;
- Git blob SHA-1 `e26c56eedd7ac604699dababd08b90199a54b063`.

The scorer reconstructs the candidate from the frozen F0 parameter authority, requires exact F1 occupancy SHA equality, and only then permits the non-verify path to load the unchanged target references.

The `--verify-only` path stops before pair-Q, residual-Z, target loading, target correlation, sign agreement, and T.

Frozen null namespaces:

- `issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{r}:reference`;
- `issue75:phaseF:M6-KRS-GATED-2MIX-CHAIN:rep{r}:test`.

Null population remains:

- reference `1000`;
- test `1000`.

Complete residual-vector length remains `66`.

## Frozen target-blocked candidate smoke

File:

`experiments/minimal-occupancy-generator/phase75f_candidate_smoke.py`

- commit `6f797e90023d2fe040ddce58ca1416e41417270f`;
- Git blob SHA-1 `63809e374d721492b3ac580e90b75674a6675f3c`.

The smoke monkeypatches `load_target_references` to hard-fail if called, then executes the complete candidate-owned 1000-reference / 1000-test null on a frozen M6 candidate.

A successful smoke may compute candidate pair-Q and residual-Z, but must retain both target vector loads, target correlation, target sign agreement, and T as false.

## Frozen aggregate decision law

File:

`experiments/minimal-occupancy-generator/phase75f_aggregate.py`

- commit `806f3593918072291ead861e76ba30a514f8bb7f`;
- Git blob SHA-1 `a414766776c11ff6743cbafb120f9b881cb9b1b7`.

Frozen controls:

- Phase-A positive-control aggregate SHA `fc3788c01bfa908bcae528a7a2606d508d26f694bf5ae51bc6cb537232efb540`;
- Phase-D M4 aggregate SHA `c15ffb92030220596cacef9db9cb3bdb26c92607f675c24ff0fa607e16764489`;
- Phase-E M5 aggregate SHA `983aa0370d949690d7e117fbf2f1273f3a157975d51a06a5e149f4ea1861c0c5`;
- F1 candidate authority SHA `de7976ca1c3e047c7c6f6bb50facdab797449ba81496312526917673a98661f3`;
- Phase-A paired q95 tolerance `0.009768313008182594`.

Primary Phase-F classification is mechanically fixed to:

- `M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_SUFFICIENT` if `gap_M6 >= -0.009768313008182594`;
- otherwise `M6_KRS_GATED_TWO_LATENT_CHAIN_MODES_INSUFFICIENT_GLOBAL_THREE_MODE_FALLBACK_LICENSED`.

Paired M6-M5, M6-M4, q90, and q99 checks are diagnostic only.

## Pretarget requirement

Before any target score may run:

1. exact rep-0 F1 replay must pass under `--verify-only`;
2. exact rep-30 F1 replay must pass under `--verify-only`;
3. rep-0 candidate-owned null smoke must pass with the target loader hard-blocked;
4. all outputs and SHAs must be frozen as pretarget evidence;
5. a separate execution-freeze document must authorize exactly one complete 31-case first reveal.

Any failure before target access is a pretarget implementation failure, not a Phase-F scientific result.
