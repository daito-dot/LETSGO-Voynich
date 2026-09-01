# Issue #72 V2 Stage C1 — target-blind preflight implementation incident (2026-09-01)

Status: **NO C1 TARGET REVEAL / NO C1 Q OR RESIDUAL SCORE**

Failed preflight:

- workflow run: `33469065031`
- job: `99734901522`
- exact head: `d29c8a697e4ad70d0c905cc1fbc6a84366a4cd27`
- scorer first-add: `1854db3dc0a3f55ac3974e7d35d18ebcd33e1bcd`

The run passed:

- plan → scoring amendment → target implementation contract → scorer chronology;
- exact permanent C0 gzip/raw/manifest verification;
- pinned Naibbe source authority;
- C1 compilation;
- C1 synthetic self-test with `target_loaded=false`.

It failed in the first real-data `--verify-only` reconstruction (`EL r0`) before slot-pair Q, residual-Z, target loading, or target correlation.

Failure:

```text
RuntimeError: C0 mask-line population does not match reconstructed lines
```

## Cause

C0 `common_support()` constructs `per_line_counts_and_mask` from `iter_positions()`. `iter_positions()` yields token positions. A reconstructed line with zero final tokens therefore has no token position and correctly has **no C0 mask row**.

The first C1 implementation's `line_lookup()` instead inserted every reconstructed line, including empty lines, and then required:

```python
len(mask_rows) == len(line_lookup)
```

This compared different universes: C0 token-bearing lines versus C1 all lines.

The frozen scientific support masks themselves are unaffected.

## Authorized recovery

Do not change:

- any C0 mask;
- any C0 randomization;
- any axis or assignment;
- any parser rule;
- any R1 statistic;
- any target vector;
- any reference-null namespace;
- any scientific threshold/interpretation.

Recovery is limited to matching C1 reconstruction to the already-frozen C0 mask domain:

> `line_lookup()` must omit reconstructed lines with `len(line) == 0`.

All non-empty reconstructed lines must still match C0 mask rows exactly, with exact visible lengths, mask bits, support counts, surface SHA identities and four-manuscript fold identities.

The original scorer file is retained unchanged for provenance. A recovery wrapper may replace only `line_lookup` before calling the frozen scorer entry point.

## Firewall

At failure:

- C1 Q computed: **false**;
- C1 residual-Z computed: **false**;
- ZL3b/IT2a target loaded: **false**;
- C1 target correlation computed: **false**;
- first-reveal workflow present: **false**.

Therefore this is a fully pretarget implementation repair.
