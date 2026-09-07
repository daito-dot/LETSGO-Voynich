# Issue #155 — common-EVA support-matched Currier Gate0 provenance

Date: 2026-09-07
Status: **PASS — SCORE-FREE AUTHORITY FROZEN**

No real-target Currier transport probability, likelihood, bits/token, `G_transport`, or scientific classification was computed by this Gate.

## Frozen chronology

- Issue #155 opened after Issue #151 closed as `ONE SHARED COMMON-EVA EDGE TABLE SUFFICES`;
- frozen plan commit `1b29f7a10103843053d6a33904dd81e96ecaa7be`, plan blob `1f30d7c62083dbff378612ce7bf177ee7d9fff80`;
- score-free Gate script commit `80f517914460cf1dcb36bbfaa9001093dbb1a999`, Gate blob `f5ab4fa31a92b3c303401da33611ffd5f77b402d`;
- first workflow/head commit `bd6d7d8b029039380bc93b467b8aa72390e6a4ed`;
- PR #156 opened only after plan, Gate script and workflow were committed;
- no Issue #155 scientific target scorer existed before the successful Gate run.

## First successful Gate authority

- workflow: `Issue155 common-EVA Currier Gate0`
- run: `34074918456`
- exact workflow head: `bd6d7d8b029039380bc93b467b8aa72390e6a4ed`
- conclusion: `success`
- artifact ID: `10001708204`
- artifact name: `issue155-common-eva-currier-gate0-bd6d7d8b029039380bc93b467b8aa72390e6a4ed`
- artifact ZIP digest: `sha256:a2b7decbc400b0a9d594daea5773585562cb333de207ec2e0a0f1eec1f133d31`
- result JSON SHA-256: `01f96038407975bc4d7a5944082a5bd2af9137f105edc33bd529cfccd33362f3`

Gate disposition:

> **`PASS — PROCEED TO SEPARATELY COMMITTED COMMON-EVA CURRIER SCORER`**

## Reproduced entry authority

The successful Gate reproduced:

- Issue #151 Gate result SHA-256 `bcc6c6bd5600ef9f74484807b51ef1db454613bae2bbd351d90f089c8693eea2`;
- Issue #151 Gate script blob `d5e3bd22501f8caebabc7c2728bc7f8d5cb59018`;
- Issue #151 Gate provenance blob `609ee5f208cfdb3739749d8d82e34d68e4803dd6`;
- Issue #151 first-reveal scorer blob `2dcd68c8fa68080552a8b90a81e118568b35f8ef`;
- Issue #151 first-reveal provenance blob `b599d7a3b4a2c749262231f711c6f14aa6a0cb0e`;
- declared Issue #151 first-reveal result SHA-256 `cb7d88b88a65df58c8d93d047b8fbfe4d2eda20d4c7314713c9d44e31a9b7355`;
- Phase 3A Currier authority script blob `015ee2cda0de53e14d82302aea7e639570db7242`;
- Phase 3A Currier Gate result SHA-256 `e970e83c8b6405fd224cef3c74f6c02ef430552fd1cd2b6aa969e89a475f258e`;
- physical-leaf fold SHA-256 `cf2df8edcf2b25c2f6388c4a9e2c1ee58a24ae05a9cf489ff9a43d2d28f0b64b`.

Frozen sources were reverified:

- ZL3b SHA-256 `bf5b6d4ac1e3a51b1847a9c388318d609020441ccd56984c901c32b09beccafc`, git blob `2a4533ab9bdfa85db9bad602d590978953055df1`;
- Takahashi/IT2a SHA-256 `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`, git blob `4d6d3f2537b1f507a257529b49c94af7d6e03446`.

## Currier physical-leaf authority

Phase 3A yields:

- `54` eligible `A_ONLY` physical leaves;
- `40` eligible `B_ONLY` physical leaves;
- A/B eligible sets are disjoint;
- mixed and unknown/other physical leaves remain excluded;
- Currier labels are derived only from the frozen ZL3b Phase 3A header/comment authority and reused unchanged for IT2a.

The target text of IT2a is never used to infer or alter Currier membership.

## Frozen matched-table construction

For each outer fold and Currier regime:

`C_R(c,y) = 0.5*C_ZL3b,R(c,y) + 0.5*C_IT2a,R(c,y)`.

For every previous-terminal context present in both Currier regimes:

`m(c) = min(M_A(c), M_B(c))`

`C_R^MATCH(c,y) = C_R(c,y) * m(c) / M_R(c)`.

Gate0 implements these counts with exact `Fraction` arithmetic. For every retained context and fold, the summed effective mass of `C_A^MATCH` and `C_B^MATCH` is exactly identical. The scale factor depends only on the context total; there is no outcome-selected subsampling.

The artifact archives the rational matched table entries and SHA-256 identities.

## Foldwise score-free support

| fold | retained contexts | matched effective mass | A cells | B cells | ZL3b-A supported/total | ZL3b-B supported/total | IT2a-A supported/total | IT2a-B supported/total |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 22 | 5,479 | 207 | 211 | 1,138/1,139 | 1,912/1,912 | 1,507/1,507 | 2,450/2,452 |
| 1 | 19 | 5,283 | 207 | 204 | 1,206/1,209 | 2,243/2,244 | 1,586/1,587 | 2,870/2,870 |
| 2 | 22 | 5,452 | 204 | 206 | 1,181/1,182 | 2,842/2,842 | 1,501/1,503 | 3,644/3,644 |
| 3 | 20 | 5,837 | 212 | 201 | 816/817 | 3,159/3,159 | 1,074/1,074 | 4,018/4,019 |
| 4 | 19 | 12,131/2 = 6,065.5 | 216 | 187 | 607/608 | 2,900/2,904 | 848/849 | 3,692/3,695 |

Minimum matched-context coverage among the 20 target cells is ZL3b-A fold 1:

`1206 / 1209 = 0.9975186104218362`.

Every target cell exceeds the preregistered minimum of 300 primary BODY targets and 300 matched-context-supported primary BODY targets. The smallest supported cell is ZL3b-A fold 4 with 607 supported BODY targets.

## Physical-leaf leakage firewall

For every fold and every reading/regime training set:

- training leaves ∩ held-out physical leaves = empty;
- union of ZL3b/IT2a × A/B training leaves ∩ held-out physical leaves = empty.

Thus a held-out manuscript leaf cannot enter the Currier source table through the other transcription lineage or opposite regime.

## Synthetic check

The target-free self-test verifies:

- exact 0.5/0.5 reading-balanced rational counts;
- exact context-by-context A/B mass matching;
- finite additive-smoothed probability for a seen synthetic atom;
- finite additive-smoothed END probability under `alpha=0.01`, `V=32`;
- no real target source loaded.

## Firewall

The artifact records all of the following as false:

- real-target transport probability computed;
- real-target transport likelihood computed;
- transport bits/token computed;
- `G_transport` computed;
- scientific classification computed;
- held-out current first atom used for context selection;
- target-selected atom mapping or support matching;
- reading weights tuned;
- context-match rule tuned;
- `k`, `alpha`, smoothing or fallback tuned;
- primary rho/mixture selected;
- hand/section/domain conditioning;
- latent-state fitting;
- S1/S2/H62/R1 tuning.

## Consequence

The support gate is clean and has substantial coverage. The next allowed sequence is:

1. merge this Gate authority;
2. create a fresh branch from the post-Gate main;
3. commit the Issue #155 scientific scorer separately and pin it to this exact Gate result/provenance;
4. only after the scorer blob is frozen, add the first target-scoring workflow.

No Issue #155 scientific Currier transport result has been revealed by this Gate.

Refs #88 #130 #151 #154 #155 #156.
