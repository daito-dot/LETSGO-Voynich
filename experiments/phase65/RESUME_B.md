# Phase 65B GitHub-only resume checkpoint

Status: **CLOSED — M8-B1 NO DETECTED MORPHOLOGY RELATION.**

Purpose: deterministic checkpoint for reconstructing Phase65B from GitHub without chat history.

## Authority

- repository: `daito-dot/LETSGO-Voynich`
- experiment branch: `phase65b-image-label-science`
- normative design: `experiments/phase65/PLAN_B.md`
- source freeze: `experiments/phase65/SOURCE_MANIFEST_B.json`
- crop freeze: `experiments/phase65/CROP_MANIFEST_B.json`
- synthetic implementation audit: `experiments/phase65/PREFLIGHT_B2.md`
- frozen executable: `experiments/phase65/phase65b_science.py`
- final report: `experiments/phase65/REPORT_B.md`
- primary summary: `experiments/phase65/RESULT_PRIMARY_F102V2.json`
- replication summary: `experiments/phase65/RESULT_REPLICATION_F100V.json`

Always re-fetch current GitHub before continuing. Historical SHAs below are provenance, not instructions to reset current state.

## Frozen population

25 physical plant-fragment↔label loci were preregistered. `f102v2 L2.7 / f102v2.16` was excluded by the pre-result transcription-confidence firewall, leaving 24 objects.

- f102v2: L2=6, L3=5, total 11
- f100v: T=4, M=5, B=4, total 13

All 24 text-blind crops passed the frozen coverage/quality gate before any association reveal.

## Implementation freeze

Synthetic-only preflight passed before P25 association results were computed. The scientific executable was then frozen at SHA-256:

`9aa07355c5d8a69acc9ee0910cf2d83877d95482f53ca1a048ae8d6cd3c3a486`

Primary and replication used this same executable unchanged.

## Scientific results

### f102v2 primary

- T = `-0.06343525603959764`
- exact one-sided p = `0.6155787037037037`
- exact permutations = `86,400`
- L2 rho = `+0.15524376203803017`
- L3 rho = `-0.39145378315603935`
- frozen gate = FAIL

Provenance:

- head `c6b0c5f5362a4b6d92bbbee09324f68676057663`
- run `33348284648`
- artifact `9742817390`
- artifact digest `sha256:e90aad368dc81b3fb0093a2798c87cc1f5ed950069273e46d732269de1a0e4f3`

All predeclared sensitivities failed.

### f100v unchanged-code replication

- T = `-0.262995097127963`
- exact one-sided p = `0.8808159722222222`
- exact permutations = `69,120`
- T rho = `-0.5161002296110789`
- M rho = `-0.338501600193165`
- B rho = `+0.11595420713048968`
- frozen gate = FAIL

Provenance:

- scientific input head `3da1eed0f0401f5df0eccf846f2f8377f1c8e50e`
- run `33348802316`
- artifact `9743019225`
- artifact digest `sha256:54258ba8f2a5abe48215042967ae5b00ae1679b7e3dfbc083aa2e5d5572c8c10`

All predeclared sensitivities failed.

## Final classification

> **M8-B1 NO DETECTED MORPHOLOGY RELATION**

The frozen prediction that visually similar plant fragments have systematically more similar attached label forms was not supported. This conclusion is representation/population-specific and does not imply semantic absence.

Do not repair this result by tuning crops, DINO representation, textual distance, row definitions, transcription or thresholds after reveal. Any further image↔text test must be a new separately frozen hypothesis.

## Current frontier after Phase65B

Phase65B is finished. The next defensible content-relation direction is an **attribute-level cross-modal hypothesis**, not another post-hoc whole-image similarity search.

Before looking for any P25 association:

1. define interpretable visual attributes independently of attached label forms;
2. define a bounded textual feature family independently of Phase65B outcomes, preferably using manuscript-wide statistics or an external rationale;
3. freeze population, directions, multiplicity correction, holdout and falsification criteria;
4. run a synthetic/null preflight;
5. only then reveal the new association test.

This must receive a new phase/hypothesis identifier and must explicitly state that it is not a repair of M8-B1.

## Safe restart instruction

> Re-fetch current `daito-dot/LETSGO-Voynich`; read `experiments/phase65/REPORT_B.md`, `PLAN_B.md`, `RESULT_PRIMARY_F102V2.json`, `RESULT_REPLICATION_F100V.json`, `research/STATUS.md`, `research/hypothesis-ledger.md`, and `ROADMAP.md`. Treat current GitHub as descriptive authority. Phase65B is closed; do not retune it. Select and preregister the next independent content-relation frontier before computing a new image↔text association.
