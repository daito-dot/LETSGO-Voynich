# Issue #72 V2 Stage C0 — recovery validation-order incident (2026-09-01)

Status: **C0 GENERATION COMPLETED / ARCHIVE NOT ACCEPTED / NO TARGET REVEAL**

Recovery workflow:

- run: `33467964705`
- job: `99731650108`
- exact recovery head: `297cb48243517d41f6266179c25367dc69198e5c`
- original failed run: `33467776608`
- recovery scope used: unreachable-j/k/w invariant-domain check only.

The recovery run successfully completed the full target-blind C0 generator, including all four axes × 31 preregistered assignments and the complete `stage_c0_support.json` construction.

The next workflow step, which validates the generated JSON before archive, failed at the assertion equivalent to:

```python
list(r['randomizations'][axis]) == [f'r{i}' for i in range(31)]
```

The C0 writer serializes canonical JSON with `sort_keys=True`. Therefore the parsed key insertion order is lexicographic (`r0,r1,r10,...,r2,...`) rather than numeric randomization order. The population itself is unchanged and complete; the validator incorrectly treated JSON object iteration order as scientific randomization order.

## Scientific status

This was a validation-only failure after target-blind support generation.

No Stage C R1 scorer existed. The C0 generator itself does not load ZL3b/IT2a residual targets or compute Q/residual-Z/target correlations. Because the validator failed before evidence upload/permanent commit, the ephemeral generated output is not promoted as authority and will be regenerated under the identical frozen generator.

## Authorized recovery 2

Do not change:

- Stage C plan;
- process paths rep0..rep4;
- axes;
- 31 assignment labels;
- deterministic hash randomization law;
- parser;
- trace renderer;
- common-support definition;
- scientific C0 generator output schema.

Change only validation of assignment membership:

```python
set(r['randomizations'][axis]) == {f'r{i}' for i in range(31)}
```

and separately require every stored row's numeric `randomization` field to cover `0..30` exactly.

This checks scientific identity without conflating it with canonical JSON key ordering.
