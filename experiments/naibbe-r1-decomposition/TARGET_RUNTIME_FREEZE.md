# Issue #72 — target runtime freeze

Status: **FROZEN BEFORE TARGET SCORER EXECUTABLE AND BEFORE FIRST REVEAL**

For all Issue #72 target matrix jobs and the aggregate job:

- GitHub runner: `ubuntu-latest` with explicit `actions/setup-python` Python `3.13`;
- numpy `2.5.2`;
- scipy `1.18.1`;
- pandas `3.0.5`.

The external source identities remain those already frozen in PLAN_A/Stage A.

Rationale: Issue #68 deterministic transport reconstruction already demonstrated stable replay under these exact package versions. Freezing them before Issue #72 target scorer code prevents finite-null changes from package drift.

Target jobs must print/assert the actual package versions before scientific scoring.
