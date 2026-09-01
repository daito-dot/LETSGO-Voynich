# Issue #72 V2 Stage C0 — pre-target implementation incident (2026-09-01)

Status: **NO TARGET REVEAL / NO SCIENTIFIC RANDOMIZATION RESULT**

Failed workflow:

- run: `33467776608`
- job: `99731102124`
- exact head: `6597ddd8316083949d15690e21208e2e0154bb0f`
- plan first-add: `79b498ef359b4cd69c3b8917e62eb11adbfb29d2`
- C0 implementation first-add: `7f07e26cb56ba3fbc219cbb20f25de5e824b7574`
- C0 workflow first-add: `6597ddd8316083949d15690e21208e2e0154bb0f`

The run passed:

- preregistration chronology;
- absence of a Stage C target scorer;
- exact Stage B2 raw authority SHA;
- exact CREMMA and Naibbe source commits/blobs;
- Python compilation.

It failed inside the target-blind Stage C0 support generator before a complete randomization support population was produced.

## Failure

The exception was:

```text
KeyError: 'unigram_alpha_j'
```

at the diagnostic invariant check named `unreachable_jkw_unchanged`.

The Stage C plan freezes the reachable effective alphabet used by Phase64B. Letters j/k/w are outside that reachable set. The pinned Naibbe mapping does not contain every synthetic `(state, table, j/k/w)` key. The first implementation nevertheless attempted direct dictionary indexing for all such nonexistent keys while checking that unreachable cells had not been altered.

This is an assertion-domain bug. It is not a codebook-randomization change.

## Scientific firewall

The failure occurred before:

- `stage_c0_support.json` completion;
- invariant validation;
- evidence artifact upload;
- permanent C0 archive;
- any Stage C R1 scorer existed;
- any slot-pair Q was computed;
- any residual-Z was computed;
- either ZL3b or IT2a target residual vector was loaded by C0;
- any intervention target correlation was computed;
- any PT/FI result was generated.

Therefore there is no Stage C target reveal to preserve from this run.

## Authorized recovery

The scientific randomization law, process-path population, parser, common-support definition, axes, 31 assignment labels, target firewall and all Stage C criteria remain unchanged.

Recovery is limited to the unreachable-cell invariant implementation:

> for j/k/w keys present in the pinned map, require exact value equality; for keys absent in the pinned map, require that the intervention map also leaves them absent.

This implements the already-preregistered semantic invariant "unreachable j/k/w cells remain unchanged" over the actual mapping domain.

The recovery must use a wrapper/patch that changes only this invariant check. It must retain the failed run above in provenance and must again complete C0 target-blind before any Stage C R1 implementation is added.
