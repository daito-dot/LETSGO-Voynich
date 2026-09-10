# Issue #172 roadmap addendum — post-#184 reversible-distribution control

Date: 2026-09-10  
Applies after: #184 / PR #220  
New issue: #221

## State change

Issue #184 S0 is complete with `S0_CAPACITY_16PLUS_EXACT`. The support-only question is closed: the frozen 12-slot language has exact reversible capacity far above the preregistered 16-bit audit threshold.

The earlier instruction **not to automatically proceed to S1** has been honored. No S1 target-derived probability fit or R2 score was computed during S0.

This addendum now licenses exactly one next control: **Issue #221 S1**, and only under the prospectively frozen `experiments/issue221-reversible-distribution-match/PLAN_S1.md`.

## Why this is licensed

S0 answered only support capacity. OGH-C already established that the observed compact memoryless token law is much narrower (~9.71 bits/token cross-entropy) than the abstract support capacity. Therefore the remaining mathematical upper-bound question is non-redundant:

> can exact reversible transport survive when output is forced to approximate that already-known V2 law rather than merely stay inside the legal support?

This is a control about compatibility of reversibility with a target-derived distribution. It is not a new historical candidate family.

## Priority / stopping rule

1. Freeze #221 plan — **this addendum + PLAN_S1 must merge before target execution**.
2. Run target-blind external-payload P0 and freeze its exact bytes/hash/environment.
3. Run one frozen S1 first reveal: global ZL3b V2 target law, deterministic CCDM, ZL3b primary + IT2a reading-transport arm, exact decoder closure, frozen R2 replay.
4. Archive result/provenance and close #221.
5. Stop this control lane. A positive S1 does not license #179 or a CCDM historical-mechanism phase; a failure does not license an in-phase repair.

## Other lanes remain unchanged

- historical replacement-candidate fishing remains closed by #213;
- #217 content lane remains `HOLD_FOR_NEW_EXTERNAL_LABEL_POPULATION`; no same-population feature/classifier tuning;
- #179 remains gated on genuinely new independent evidence;
- no cross-token R3-R8 repair is licensed by #221.

This addendum is the explicit roadmap revision required by the #184 preflight before S1 can begin.
