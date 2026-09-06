# RESUME — deterministic restart point

Last consolidated: 2026-09-06

## Resume here — Issue #134 is active

Do not reconstruct the project from old chat when GitHub contains a newer state.

The latest completed scientific line is Issue #88 residual localization through Issue #130. PR #132 was merged after the first-reveal provenance was frozen. The scientific reveal is anchored to head `1604c2f36d106e918c55a24f7bea6b7e08622cff`; the post-reveal provenance commit did not alter the scorer or decision rule.

Repository navigation was consolidated in PR #133. The current executable child of Issue #88 is **Issue #134 — augmented observable core before latent-state work**.

### First sentence a future agent should be able to say

> We have reduced the previously flexible cross-token residual to a compact observable rule: **within a source line, the terminal raw symbol of one visible production unit helps predict the initial raw symbol of the next; the useful short context resets at line breaks.** The edge architecture exists in both Currier A and B, but the literal terminal→initial table is regime-dependent under the frozen transport tests.

The manuscript is not deciphered. Visible spaces are not assumed to be natural-language word boundaries.

## Read in this order

1. `README.md`
2. `research/STATUS.md`
3. `ROADMAP.md`
4. Issue #134
5. `research/PREDICTIVE_INFORMATION_PROGRAM.md`
6. `research/HYPOTHESIS_LEDGER.md`
7. `research/RESEARCH_PROTOCOL.md`
8. latest phase-specific plan/provenance under `experiments/predictive-information/`

For exact historical numbers or methods, open the relevant frozen plan, report and first-reveal provenance. Superseded navigation/current-state snapshots are in `research/archive/`.

## Authority hierarchy

1. phase/Issue-specific frozen plan + exact first-reveal artifact/provenance control historical method, hashes and frozen classification;
2. `research/STATUS.md` controls the current accepted high-level interpretation;
3. `research/PREDICTIVE_INFORMATION_PROGRAM.md` controls the Issue #88 program and latent-state licensing rule;
4. `research/HYPOTHESIS_LEDGER.md` controls current hypothesis status/history;
5. `research/RESEARCH_PROTOCOL.md` controls evidential discipline for new decision criteria;
6. `ROADMAP.md` controls current sequencing;
7. old chats, old RESUME/ROADMAP snapshots and archived addenda are non-authoritative where later repository evidence conflicts.

## Current accepted state

### 1. Token-internal construction is compact

Issue #75 + OGH-A/B/C close the token-internal R1 generation lane.

- target-blind second-order occupied-slot successor grammar: 298 counted conditional probabilities;
- median topology agreement `T≈0.948` on the ZL3b arm and `0.962` on the IT2a arm;
- memoryless V2 code length `9.7089061 bits/token`;
- approximate information split: shape `~7.0 bits/token`, values add `~2.7 bits/token`.

Do not open another occupancy-only R1 rung unless a later result invalidates this authority.

### 2. Certain visible spaces are production boundaries

Phase 4 independently supports exact visible cuts as statistical construction/production boundaries:

- ZL3b `D_RESET = +8.811905 bits/event`, 5/5;
- IT2a `D_RESET = +8.092615`, 5/5;
- exact observed cuts beat one-atom left/right shifts in both readings.

This does not establish linguistic words.

### 3. Corrected non-latent predictive ladder

After the source-order correction:

- B0 V2 `9.7089061 bits/token`;
- B1 local `9.5943670`;
- B2 longer causal history `9.5461692`;
- B3 + observable line/paragraph state `9.5172688`.

Most longer-history gain is causal-prefix / prior-paragraph inventory rather than detailed long ordered memory. A smaller actual-order component survives.

### 4. The Issue #118 residual exists but is small

The matched RESET/CONT byte-family test found:

- `G_context = +0.0178533 bit/token`, positive 5/5;
- `G_any = +0.0306054 bit/token`, positive 5/5.

The residual is only about 0.19% of B3 code length. It licenses localization, not semantic or rich latent-state interpretation.

### 5. L1–L3 localize the residual to an explicit same-line edge

Issue #121 same-order control:

- `G_edge = +0.0106322 bit/token`, positive 5/5.

Issue #123 line-reset scope:

- RESET2 → LINECONT2: `G_line = +0.0291614`, positive 5/5;
- LINECONT2 → LEAFCONT2: `G_beyond_line = -0.0185292`, positive 0/5.

Carrying the same short raw context across a line break is predictively harmful.

Issue #125 exact decomposition under fixed `k=2`:

- generic line-position/onset component `+0.00889185 bit/token`, positive 5/5;
- previous-terminal identity component `+0.02026956`, positive 5/5;
- EDGE2 and the formerly flexible LINECONT2 expert have maximum inner/outer token-logp difference `0.0`.

Thus the tested flexible line-local predictor does not hide an additional longer-context effect under this representation: it factorizes into observable line position plus immediate terminal→initial identity.

### 6. Currier transport separates shared architecture from regime-specific mapping

Issue #127 established:

- native explicit edge useful in Currier A and B;
- scalar edge strength compatible bidirectionally when the target identity table is supplied;
- literal source terminal→initial table transports only B→A under target-calibrated strength;
- exact source table + source strength transports neither direction.

Issue #130 removed the obvious support imbalance. For every one of five outcome-blind selections, A and B source tables were trained from exactly `8,728` visible edge events with identical selected counts inside each of 20 shared previous-terminal classes.

Frozen matched result:

- A→B: seed passes `0/5`, grand mean `+0.00693954 bit/token` — FAIL;
- B→A: seed passes `5/5`, grand mean `+0.02697082 bit/token` — PASS;
- classification: **`B→A ONLY`**.

The direction therefore cannot be explained merely by B having more source examples. Do not convert this into a historical A→B/B→A derivation claim or a statement that one Currier regime “contains” the other.

## Latest first-reveal authority

Issue #130 L4b:

- scientific head: `1604c2f36d106e918c55a24f7bea6b7e08622cff`;
- workflow run: `34029536188` — SUCCESS;
- artifact: `9988168421`;
- artifact ZIP digest: `sha256:90a6d658d72dda1e02ad96775822002e96c94858a99cbe15f9b08f95dd3a9707`;
- result JSON SHA-256: `d2ae55675fb7613b4f5000ab81558099f2821ff245acacdcb5a6697e06f7249e`;
- matched Gate JSON SHA-256: `a0f48878506369aa9dff60e06b60be13d41d36dd1ceef3a40c4fc63825db66f5`;
- provenance: `experiments/predictive-information/residual-gate/L4B_MATCHED_TRANSPORT_PROVENANCE.md`.

## Next scientific move — Issue #134

Issue #134 is the active executable gate. Its first deliverable is a **score-free design contract** for an augmented observable core residual test.

The core should incorporate, without target-outer leakage:

1. corrected B3;
2. generic line-position/onset support;
3. explicit immediately previous terminal → current initial edge;
4. a prospectively frozen Currier A/B table policy, because Issue #130 rejects a single universally transportable literal table under the tested setup;
5. a predeclared fallback for unknown/other Currier support.

Then compare that augmented non-latent core against a separately frozen flexible residual challenger on the original physical-leaf outer folds.

Decision:

- if robust residual disappears/fails the frozen stability rule, **do not license latent-state work**; consolidate the compact observable multiscale description;
- if a robust residual remains, localize remaining observable/support/representation effects before fitting or interpreting a latent state.

A later independent IT2a/Takahashi replication of the explicit terminal→initial edge is high-value, but should not be used to tune the ZL3b edge representation after seeing target outcomes.

## Do not

- reopen token-internal R1 model ladders without a new falsification reason;
- treat visible spaces as proven linguistic words;
- use residual signs to choose Currier/domain/hand strata after reveal;
- condition on writing hand as a causal explanation while hand and Currier remain inadequately crossed;
- use target outer folds to select edge tables, strengths, fallback or residual hyperparameters;
- infer plaintext, language, semantics, cipher identity, author, hoax/artificial origin or historical production mechanism from predictive fit;
- call a non-reversible surface generator a decipherment;
- append another “current resume” beneath this file. Replace this file and archive the superseded snapshot instead.