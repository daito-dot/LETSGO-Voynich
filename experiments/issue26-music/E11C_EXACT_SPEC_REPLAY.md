# E11C exact-spec replay — 24-letter Latin correction

Status: **POST-REVEAL SPECIFICATION CORRECTION / SOLVER INADEQUATE**

## Why this replay was required

The first E11C scientific run revealed that the shared base executable retained a 25-letter plaintext alphabet even though the frozen E11/E11C specification normalized `j→i` and `v→u`, requiring 24 letters.

Commit `a643c273fe08da116a24f21954cf1d507e73c729` corrected only that specification mismatch in the pre-score compatibility runner. No Voynich-dependent parameter, objective, threshold, search rule, or representation was changed.

## Exact-spec first replay

- branch/head: `issue26-music-e11-leon-substitution` / `a643c273fe08da116a24f21954cf1d507e73c729`
- Actions run: `33382380148`
- job: `99457420733`
- artifact: `9754369814`
- raw JSON SHA-256: `6e0bee446000fcfd81ab20a383910256a2c6e19fbb1a72befa40aa93358940b7`
- artifact ZIP SHA-256: `0cd1ad7143e57fe64c6960791cb9a3b76a9cf5813db2f07de7bbba352169f8d2`

## Mandatory positive control

The exact-spec replay still fails the mandatory known-cipher positive control:

- true-key mean held-out CE: `2.8305081642674272 bits/char`;
- recovered-key mean held-out CE: `4.593013995872094`;
- mean occurrence-weighted key accuracy: `0.03398228251987704`;
- exact recovered-key recurrence: `2/5`;
- positive-control pass: **false**.

Therefore the frozen E11C classification remains:

**`SOLVER INADEQUATE`**

## Voynich numbers are non-interpretable under the gate

For audit only, the run emitted:

- Voynich mean held-out CE: `4.322080614768455`;
- pooled CE: `4.3051432788591155`;
- weighted mapping stability: `0.7343853927063229`;
- exact full-key recurrence: `1/5`;
- pooled top-five fraction: `0.6648483510536023`;
- one >=6 whole-token CREMMA hit (`distin`) in fold 2.

These numbers and fragments **must not be interpreted as evidence for or against the León/Visigothic substitution hypothesis**, because the same solver cannot recover the known synthetic cipher.

Do not promote or pursue `distin` or any other isolated output fragment from this run.

## Next permitted step

Solver calibration is moved to E11D on a separate branch. E11D is deliberately Voynich-blind: it may use only frozen medieval Latin and synthetic known-key ciphers. A later Voynich rerun is permitted only after the prospectively frozen E11D validation gate passes.
