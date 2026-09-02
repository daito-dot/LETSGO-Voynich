# Issue #75 Phase B — first-reveal launch incident

Date: 2026-09-01  
Status: **PRETARGET WORKFLOW-TRANSPORT INCIDENT; NO TARGET CASE SCORED**

## Attempted launch

The first Phase-B first-reveal workflow was added at commit:

`693f627910f5775406da410ec4d7157a161021e4`

The Actions run listing briefly returned a queued run ID:

`33504454487`

but subsequent direct run retrieval returned `404`, the commit had zero check-runs, no scored-case artifact existed, and no `stage-b-first-reveal` or `REPORT_B.md` existed.

Therefore the attempted launch did not establish a durable Actions execution and did not score or reveal any M2 target case.

## Target firewall status

Before this launch attempt, both required target-blind execution authorities had already passed:

- exact replay preflight run `33503957561` — success;
- candidate-owned 1000-reference/1000-test smoke run `33504179109` — success with target loader deliberately unused.

The failed launch itself produced:

- no score job;
- no target-loaded JSON;
- no per-rep artifact;
- no aggregate;
- no classification.

No target-dependent scientific information was observed while diagnosing the launch failure.

## Licensed repair

Scientific files and authorities remain frozen exactly as before:

- `PLAN_B.md`;
- `phase75b_generator_support.py`;
- permanent Phase-B0 authority;
- `phase75b_score.py`;
- `phase75b_aggregate.py`;
- frozen Phase-A positive-control aggregate;
- `target68.py`;
- all seed/null namespaces and decision rules.

The workflow transport may be simplified to remove dynamic job-output matrix construction and use an explicit static rep matrix `0..30` while retaining the same exact 31-case scientific population.

The repaired workflow must still:

1. prove the same frozen chronology;
2. verify the successful target-blind preflight and smoke artifacts;
3. pin a single scientific workflow head;
4. score exactly reps `0..30` once each;
5. use no drops/rerolls;
6. aggregate with the unchanged frozen Phase-B law.

This is a pretarget launch/transport repair only. No M2 scientific commitment is changed.
