# Issue #72 V2 — FI authority audit (2026-09-01)

## Canonical scientific chain

The only FI allocation/scoring authority is the chain frozen before FI target access:

1. preregistration: `a053efd9803b6c0f74614986289c54a8add7d904` — `STAGE_C1_FI_PLAN.md`;
2. scorer/allocation implementation: `efad503afeb45500a8e520680ed7189bf9ee33f1` — `fi_r1_score72_v2.py`;
3. aggregation law: `285fb10db3f92df401f3f459d73827590af637a7` — `fi_aggregate72_v2.py`;
4. implementation freeze: `e773d37ee8bd94298788e7af3a67843109e3879d`;
5. successful target-blind boundary preflight: run `33496383052`, head `3ac22384ce5379d82883f9fd9ae7daa01677f27d`;
6. canonical first-reveal head: `442fa401dcd82fda7f6bb1c4720b908c50900c0b`, run `33496538872`.

The canonical allocation RNG is therefore exactly the implementation already frozen in `fi_r1_score72_v2.py`:

`random.Random(stable_seed("issue72v2:C1:<family>:allocation:<index>"))`

where `stable_seed` is the pre-existing `trace_audit72_v2.py` mapping:

`int.from_bytes(SHA256(namespace)[:8], "big") % (2**31 - 1)`.

The first-reveal workflow verifies the scorer-add commit exactly and checks that the scorer, aggregator, preregistration, and B0 authority are unchanged from the frozen implementation before scoring.

## Non-authoritative duplicate FI0 incident

After the canonical scorer/aggregator/freeze chain already existed, a second target-blind helper was added at commit:

`7da0369a03da3b9c11ba935818bd2e1ef68aa3fd`

with workflow commit:

`0b967f19461107edf5f4590bb80190dfbaf3a240`.

It generated target-blind run `33496401419` and repository commit `d024cb8f1a46647144920e6111f8f44551f1a5ef`.

That helper used a different deterministic namespace-to-seed mapping from the already-frozen canonical scorer. No Voynich target, Q, Z, R1, T, or FI p-value was accessed by that helper; the conflict is therefore a pretarget implementation duplication, not result-driven selection.

The duplicate helper was never read by `fi_r1_score72_v2.py`, `fi_aggregate72_v2.py`, or the canonical first-reveal workflow. The canonical first-reveal head contains the historical duplicate files in its tree only because the duplicate target-blind workflow completed immediately before launch. Its authorize job nevertheless pins the earlier scorer/aggregator commits, and every scored case regenerates allocation directly through that canonical scorer.

To prevent later agents from mistaking the duplicate metadata for scientific authority, the duplicate workflow, generator, and generated `stage-c1-fi0/` files were removed from the current branch in commits beginning `d31e0bd5e9d30f357954d5d7eccca00404891098` through `9d1c0c5b481cf3788ecf74ae01ff05e713e57bb1`.

Git history intentionally retains the incident for auditability.

## Authority rule

For FI interpretation:

- use only the exact 398 scored cases and aggregate produced by canonical run `33496538872` at scientific head `442fa401dcd82fda7f6bb1c4720b908c50900c0b`;
- never substitute, average with, or compare-select the duplicate FI0 allocation population;
- retain all 199 FI-G and all 199 FI-M canonical scorer cases;
- use the preregistered `T=min(R_ZL3b,R_IT2a)`, plus-one upper-tail p-values, and Holm correction exactly as frozen.
