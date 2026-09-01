# Issue #68 — R1 first-reveal protocol

Status: **FROZEN BEFORE FIRST-REVEAL WORKFLOW AND BEFORE REAL R1 TARGET EXECUTION**

## Single authorized event

The first real Issue #68 R1 target execution is triggered only by:

> opening a same-repository pull request from `issue68-joint-constraint-target` to `main`.

The workflow event is `pull_request` with `types: [opened]` only.

It does **not** run on `synchronize`, `reopened`, `push`, or ordinary workflow updates.

The workflow must checkout exactly `github.event.pull_request.head.sha`, not the GitHub synthetic merge ref, and must propagate that SHA into the result as `github_sha`.

## Pre-reveal requirements

Before real target execution the workflow must verify:

1. exact target head checkout;
2. plan → preflight implementation → target implementation notes/order freeze → target scorer → this protocol → workflow chronology;
3. exact archived preflight SHA-256 `fdd2b1138542bf1b332b20f27a9869ac7a3501038e7d4ec9ccf40910e3b98771`;
4. preflight A1 disposition remains `FAIL_REPRESENTATION_COMPATIBILITY`;
5. preflight Naibbe disposition remains `AUTHORIZED_FOR_R1_REVEAL`;
6. preflight Naibbe R4 remains `FAIL`;
7. no permanent Issue #68 first-reveal result file already exists;
8. exact frozen CREMMA and Naibbe source identities;
9. target scorer compiles and synthetic self-test passes.

## Real execution boundary

Only after those checks may the workflow invoke:

`target68.py CREMMA_ROOT NAIBBE_ROOT`

The executable itself must verify the frozen primary surface SHA identities before pair-Q calculation.

A1 is not passed to the target executable and must not receive a real R1 pair/residual graph.

## Immediate output handling

The first reveal must emit one raw canonical JSON result artifact and a SHA-256 record.

Before any scientific interpretation or repository Source-of-Truth update:

1. preserve exact workflow run/job/head/artifact IDs;
2. preserve artifact ZIP digest;
3. preserve exact raw JSON SHA-256;
4. permanently archive the exact raw JSON in Git;
5. then, and only then, write the result report / hypothesis-ledger update.

No threshold, candidate view, seed, parser policy, null namespace, or target reading may change after the PR-open event.

## Failure semantics

A workflow/runtime error before a scientifically valid raw result exists may be repaired only mechanically and must be documented.

If a valid raw target result exists, it is the first reveal even if the result is unfavorable. No rerun may replace it as the scientific first reveal.
