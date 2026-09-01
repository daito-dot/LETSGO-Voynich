# Issue #72 — complete-family R1 first-reveal protocol

Status: **FROZEN BEFORE FIRST-REVEAL WORKFLOW AND BEFORE ANY REAL COUNTERFACTUAL R1 SCORE**

## Single authorized scientific event

The only authorized first-reveal event is:

> opening a same-repository pull request from `issue72-naibbe-r1-decomposition` to `main`.

The workflow event is `pull_request` with `types: [opened]` only.

It must not run scientific target scoring on `push`, `synchronize`, `reopened`, or manual workflow dispatch.

All jobs must checkout the exact PR head SHA, never the synthetic merge ref.

## Frozen input family

The scientific family is exactly the target-authorized realization list permanently frozen in:

`experiments/naibbe-r1-decomposition/family-preflight/TARGET_AUTHORIZED_REALIZATIONS.txt`

with axis membership in:

`TARGET_AUTHORIZED_AXES.txt`

and exact canonical surface SHA-256/support records in:

`family-preflight/preflight.json`.

The first-reveal workflow may not add, remove, retry-select, or substitute a realization after target values exist.

## Pre-scoring gates

Before any matrix job computes a real pair-Q, the workflow must verify:

1. exact PR head checkout;
2. post-#68 parent main ancestry;
3. source-audit plan → source audit → target PLAN_A → family-support freeze → target implementation → runtime freeze → target scorer → aggregate scorer → this protocol → first-reveal workflow chronology;
4. permanent Stage-A audit exists and states no counterfactual R1 was scored;
5. permanent family-support preflight exists and states no counterfactual R1 was scored;
6. target-authorized axes/realizations exactly match the family-preflight JSON;
7. every authorized realization has frozen coverage >= 0.60;
8. no Issue #72 first-reveal result already exists;
9. target72.py and aggregate72.py compile and pass synthetic self-tests under the exact frozen runtime.

## Parallel scientific scoring

After the preparation gate passes, one matrix job is created for every and only every frozen authorized realization.

Each matrix job:

- checks out exact PR head;
- uses Python 3.13, numpy 2.5.2, scipy 1.18.1, pandas 3.0.5;
- checks out exact CREMMA and Naibbe authorities;
- calls `target72.py score RID ... OUTFILE`;
- writes scientific JSON directly to a dedicated file;
- validates RID/head/surface/family-preflight identity and 1,000-null array lengths;
- uploads JSON + SHA-256 + provenance as an immutable run artifact.

A matrix job may not assign final familywise p-values or axis/global classes.

## Complete-family aggregation

Only after all matrix jobs succeed, one aggregate job:

1. downloads every per-realization artifact;
2. requires the artifact RID set to equal the frozen authorized RID set exactly;
3. verifies every input JSON SHA and common exact first-reveal head;
4. runs `aggregate72.py` once;
5. applies the complete realization-family × both-reading maxT correction;
6. produces all per-realization full R1 passes, axis classes and the frozen global decomposition class;
7. packages aggregate JSON, all per-realization scientific JSONs, complete input SHA manifest and provenance into one final first-reveal artifact.

No scientific interpretation is written before this aggregate artifact exists.

## Failure semantics

If a job fails before producing a scientifically valid result artifact, only a mechanical/runtime/transport repair is allowed. It must be documented before retry and must not use partial target values to change candidate families, thresholds, seeds, support rules or algorithms.

If any scientifically valid counterfactual result is exposed before complete aggregation, it remains part of the first-reveal family and cannot be dropped or replaced.

If complete-family aggregation cannot be reconstructed without adaptive scientific changes, the outcome is `R1 DECOMPOSITION INCONCLUSIVE`.

## Permanent archival before interpretation

Before writing REPORT / hypothesis-ledger / Source-of-Truth updates, permanently preserve:

- scientific PR number;
- exact first-reveal head;
- workflow run ID and all scientific job IDs;
- every per-realization raw scientific JSON and SHA-256;
- every 1,000-test-null array contained in those JSONs;
- final aggregate JSON and SHA-256;
- aggregate artifact ZIP digest;
- exact ordered target-authorized realization list;
- input-realization SHA manifest;
- source/runtime identities.

## Immutable scientific boundary

After the PR-open event, do not change:

- intervention axis or realization set;
- intervention seed/permutation labels;
- support gate;
- parser policy;
- source/output view;
- null counts/namespaces;
- target readings;
- R1 gates;
- REL thresholds;
- axis/global classification logic.

Per-edge diagnostics are not allowed to promote or repair the primary result.
