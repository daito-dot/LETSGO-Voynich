# Issue #75 Phase C0 — recovered target-blind authority freeze

Date: 2026-09-01  
Status: **C0 COMPLETE / TARGET BLIND / 31-CASE AUTHORITY FROZEN**

## Scientific role

This file freezes the exact pre-target M3-KRS-CHAIN generated population. It contains no R1 target score and does not alter the preregistered model.

## Preregistration chronology recovery

The normative Phase-C plan text was committed prospectively inside `.github/workflows/issue75-phaseC-preregister-if-licensed.yml` at commit:

`837d9b904a6fa75e5e50554477a3277c527c4a94`

The M3 generator implementation was added in its immediate child commit:

`32d2f8c99a9c9cf608af8b393f597412556c6f5d`

The original preregistration run failed at the Phase-B license gate before writing `PLAN_C.md`. After the real Phase-B authority was recovered, the original historical preregistration job was rerun without changing its workflow definition, materializing the already-frozen plan text as `PLAN_C.md` at commit:

`615e60debc9ba9da024b91c86ae717b9ad03e460`

The recovered C0 workflow verified byte-for-byte equality between that `PLAN_C.md` and the plan text embedded in the pre-implementation commit.

It also verified that the earlier Phase-C first-reveal run `33506588721` stopped in authorization and that its `score` and `aggregate` jobs were skipped. Prior Phase-C target scores: `0`.

## Exact C0 authority

- workflow run: `33508138601` — success
- generation head: `1b3d1208e2a8d87649aa0489822f0ed6e6399dcd`
- permanent repository commit: `cf2c1905a6255db41b3a41aa6ab2002566095dd7`
- artifact ID: `9800460088`
- artifact name: `issue75-phaseC0-recovered-m3-authority-1b3d1208e2a8d87649aa0489822f0ed6e6399dcd`
- artifact digest: `sha256:27cb7c4081f654a2d6e51e3fca00b88b9483e5b050a373f0134b29ea6424d4cc`
- C0 authority SHA-256: `1ff4469f57a84093b8c5d6463bb276a8de6fc108eed666bf63c9c7dacbf622a6`
- stdout SHA-256: `0bd95c009b8b067ad241ad92e623b2650e7ace3360047c483332221745553e97`
- cases: `31/31`
- drops: `0`
- rerolls: `0`

Repository authority:

`experiments/minimal-occupancy-generator/stage-c0/generator_authority.json`

## Frozen M3 model

- family: `M3-KRS-CHAIN`
- exact training-only joint `(K,R,S)` descriptor distribution;
- conditional maximum-entropy unary slot terms plus nearest-neighbor occupied-pair terms;
- 11 free unary parameters;
- 10 free adjacent interaction parameters;
- 21 continuous parameters per cross-fit training split;
- explicit nonadjacent pair parameters: `0`;
- empirical complete-signature-specific parameters: `0`.

All five cross-fit fits satisfied the preregistered maximum moment error `<=1e-10`.

## Target firewall

C0 asserts for every case:

- pair Q not computed;
- residual Z not computed;
- target topology not loaded;
- target correlation not computed.

The authority-level target-access fields are all false.

## Next licensed action

Run exact target-blind replay preflight for reps `0` and `30`, then the rep0 candidate-owned null smoke. Only after both succeed may a Phase-C first reveal be authorized.
