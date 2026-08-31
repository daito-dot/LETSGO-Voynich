# Hypothesis ledger addendum — Issue #58

Date: 2026-09-01

This file records the selection-aware follow-up to Issue #55. Exact methods, thresholds, hashes and first-reveal provenance remain controlled by `experiments/occupancy-graph/PLAN_A.md`, `REPORT_A.md`, and `first-reveal/`.

## #58A — the selected slot3×slot5 exclusion is globally exceptional

Origin:

- #55B established an almost complete binary occupancy exclusion between slots 3 and 5.
- that pair was not prospectively unseen: it was selected through the earlier E10 → #55 path.
- #58A therefore scored all 66 unordered pairs under one frozen family-wise test instead of retesting `(3,5)` alone.

Prediction required for the selected-edge hypothesis:

1. `(3,5)` rank by mean held-out symmetric gain `<= 3/66`;
2. global maxT `p <= .01`;
3. all five held-out fold gains positive;
4. pooled phi negative.

Result:

- selected rank: `22/66` — **FAIL**;
- selected mean gain: `0.0442150445 bits/token`;
- selected global maxT p: `0.000999001` — pass;
- selected all-five-positive: pass;
- selected phi: `-0.20648429` — pass;
- selected `K_other`-conditional mean gain: `0.0263595018`;
- selected conditional maxT p: `0.55644356`;
- family-wise qualifying edges under the primary rule: `22/66`.

Status: **NOT SUPPORTED AS A UNIQUE / GLOBALLY EXTREME EDGE**.

The selected pair remains a real occupancy exclusion, but the hypothesis that it is one of the globally dominant relations is falsified by its rank.

## #58A — broad signed occupancy grammar

Frozen alternative classification rule:

- selected-edge extreme gate fails; and
- at least five distinct edges have global maxT `p <= .01` with all five held-out gains positive.

Result:

- selected-edge extreme gate fails because rank is `22`;
- `22` distinct edges qualify;
- the graph includes both positive and negative phi relations;
- strongest primary edge `(8,10)` has mean gain `0.76766689`, phi `+0.92377816`, and conditional maxT p `0.000999001`;
- `(8,11)` and `(10,11)` are strong negative relations;
- all `66/66` canonical two-slot co-occupancies are admitted by the parser.

Status: **SUPPORTED — `BROAD OCCUPANCY GRAMMAR; SLOT3xSLOT5 NOT UNIQUE`**.

Permitted interpretation:

- the current 12-slot representation exposes a broad signed token-construction grammar;
- slot3×slot5 is one valid exclusion edge within that graph;
- the leading structure is not reducible to a generic tendency for slots merely to avoid one another because strong positive co-construction edges also occur;
- simple parser impossibility does not explain the graph because every canonical pair is admissible.

Prohibited inference:

- semantic meanings for individual slots;
- a cipher table or plaintext mapping from edge sign/strength;
- music/Sloane revival;
- treating `(8,10)` or another observed high-scoring edge as a fresh prospective discovery target;
- manuscript-wide stability before stratified transfer is tested.

Disposition:

- move the target from selected-edge specificity to graph-level stability across externally defined register/Currier/section and token-position strata;
- perform that work only in a separately frozen #58B phase because #58A did not preregister exact stratification tests before reveal;
- defer reversible-transform interpretation until graph stability and, where possible, representation invariance are established.
