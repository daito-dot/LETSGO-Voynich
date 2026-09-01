# Issue #72 V2 Stage B1 — permanent raw aggregate archive addendum

The exact Stage B1 aggregate from Actions artifact `9784131519` is now permanently archived in-repository because Stage B2 needs the full rep0..rep4 66-edge residual-Z vectors, not only the human-readable summary table.

## Exact authority

- Stage B1 run: `33463625070`
- aggregate artifact: `9784131519`
- artifact ZIP SHA-256: `143731f7e430f3cea5c878890852ae24de4917ea9fa73eb3166330c1ff541fd5`
- exact raw `stage_b1_calibration.json` size: `44,780` bytes
- exact raw SHA-256: `b37d285b25d17623fa19910ff3f8f4586846bb8f19825c3dbdd6e8b19bb2e31d`

The raw aggregate contains, for every `rep0..rep4`, complete primary/secondary calibration objects including `q_full` and `z_full` across all 66 slot pairs.

## Repository transport

Permanent transport file:

`archive/stage_b1_calibration.json.gz.b64`

Prepared from the exact raw bytes using deterministic gzip (`mtime=0`) and base64:

- gzip bytes: `9,773` bytes
- gzip SHA-256: `135e2f0280cfdf7ad8286139545c1598a058959d90d44a346d2f524b827aa2d2`
- base64 bytes: `13,032` bytes
- base64 SHA-256: `39096f044618596859fac80bac58df9f6acd627a549f9f5b9b4919009f36f9a1`

Reconstruction:

```bash
base64 -d archive/stage_b1_calibration.json.gz.b64 | gzip -dc > /tmp/stage_b1_calibration.json
sha256sum /tmp/stage_b1_calibration.json
```

Expected raw SHA-256:

`b37d285b25d17623fa19910ff3f8f4586846bb8f19825c3dbdd6e8b19bb2e31d`

This addendum changes no Stage B1 scientific result. It only upgrades the already accepted Actions artifact into permanent repository authority for later 25-realization aggregation.
