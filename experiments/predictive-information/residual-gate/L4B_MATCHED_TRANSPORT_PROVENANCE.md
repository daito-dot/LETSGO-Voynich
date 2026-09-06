# Issue #130 L4b support-matched transport — first-reveal provenance

Date: 2026-09-06
Parent: Issue #127 / Issue #130
Status: **AUTHORITATIVE FIRST REVEAL**

## Frozen scientific head

`1604c2f36d106e918c55a24f7bea6b7e08622cff`

No selected current-initial distribution, matched-table gain, target-inner rho, or A→B/B→A classification was inspected before PR #132 was opened at this head.

## Workflow authority

- workflow: `Issue130 support-matched edge transport first reveal`
- run: `34029536188`
- conclusion: **SUCCESS**
- artifact: `9988168421`
- artifact ZIP digest: `sha256:90a6d658d72dda1e02ad96775822002e96c94858a99cbe15f9b08f95dd3a9707`
- result JSON SHA-256: `d2ae55675fb7613b4f5000ab81558099f2821ff245acacdcb5a6697e06f7249e`

The scorer reproduced the merged support-matched Gate0 authority exactly:

- Gate JSON SHA-256 `a0f48878506369aa9dff60e06b60be13d41d36dd1ceef3a40c4fc63825db66f5`;
- parent Issue #127 Gate0 SHA-256 `31c96135ec8e265781fe295888e52d896d47122bfa9d2bbf6f7e36c001827bdb`;
- 20 shared previous-terminal contexts;
- exactly 8,728 selected visible source edge events in each Currier regime for every frozen seed;
- exact A/B selected-count equality separately within every retained previous-terminal class.

## Frozen classification

> **MATCHED_TABLE_TRANSPORT: B→A ONLY**

### A → B

All five outcome-blind matched-source seeds fail the frozen seed rule: each has positive mean gain but only `3/5` positive target folds.

Seed means:

- r0 `+0.00684520 bit/token` — 3/5, FAIL
- r1 `+0.00678375` — 3/5, FAIL
- r2 `+0.00681271` — 3/5, FAIL
- r3 `+0.00686835` — 3/5, FAIL
- r4 `+0.00738768` — 3/5, FAIL

Direction summary:

- seed passes `0/5`;
- grand mean across all 25 seed×fold gains `+0.00693954 bit/token`;
- overall **FAIL**.

### B → A

All five outcome-blind matched-source seeds pass the frozen seed rule: each has positive mean and `4/5` positive target folds.

Seed means:

- r0 `+0.02749523 bit/token` — 4/5, PASS
- r1 `+0.02747752` — 4/5, PASS
- r2 `+0.02760992` — 4/5, PASS
- r3 `+0.02737722` — 4/5, PASS
- r4 `+0.02489424` — 4/5, PASS

Direction summary:

- seed passes `5/5`;
- grand mean across all 25 seed×fold gains `+0.02697082 bit/token`;
- overall **PASS**.

Source-context fallback is negligible in both directions (`2/15,217` A→B targets and `1/6,634` B→A targets per seed).

## Interpretation

The directional terminal→initial conditional-table transport asymmetry survives prospectively matched source support. The original B→A-only result therefore cannot be explained by B having roughly twice as many source edge observations as A.

Supported statement:

> The same compact line-local terminal→initial edge architecture is useful in both Currier regimes, but the literal conditional mapping is not a single bidirectionally transportable table under the tested representation. B-trained mapping transfers robustly to A; A-trained mapping does not satisfy the frozen stability rule on B even after context-by-context support matching.

This materially strengthens a **regime-dependent observable mapping** interpretation. It does not establish that B historically derives from A, that B contains A, a writing-hand cause, semantics, plaintext, language, cipher family, author, hoax status, or historical production mechanism.

## Next program consequence

Issue #127/#130 complete the required Currier localization of the explicit edge. The next high-value step is to incorporate the line-position + terminal→initial observable edge into the non-latent predictive core and rerun a separately frozen residual-capacity gate. Only residual information surviving that stronger observable core should motivate a latent-state challenger.
