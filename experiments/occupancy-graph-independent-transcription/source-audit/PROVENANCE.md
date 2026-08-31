# Issue #58D / #66 Stage-A source-audit provenance

Status: **permanent archive of the source/population-only audit; no pair or residual target metric was computed**.

## Plan-before-code chronology

- post-#58C base main: `c777b81c9ef424429105dbcfd60532bdb9158362`
- branch: `issue66-independent-transcription-residual`
- `SOURCE_AUDIT_PLAN.md` first-add commit: `b45bf3ec94b5bf8165117c378b65c4348db0720d`
- pre-science correction of historical source authority: `7570fecd0d920f99f063c1bb6612621476f1db33`
- `source_audit58d.py` first-add commit: `532d2b6d6b5a278536b8234accd8ac11b6c9d88b`
- workflow/source-audit head: `142b301e753a275e0ebee20f5918e69bfc28a56a`

The correction commit fixed erroneous historical hash/alphabet text in the first draft by consulting the already committed Phase63B `SOURCE_AUDIT_B.md` and `SOURCE_MANIFEST_B.json`. It occurred before the Stage-A executable existed and before any #58D pair/residual target score was authorized or computed.

## Exact workflow

- workflow run: `33448114119`
- job: `99671663030`
- conclusion: `success`
- artifact ID: `9778760108`
- artifact name: `issue66-source-audit-142b301e753a275e0ebee20f5918e69bfc28a56a`
- artifact ZIP SHA-256: `6f91c7f872ab56e034fb0e4b27498ccdf0985b5c84279d44d4509978ff4189f5`
- exact raw `issue66_source_audit.json` SHA-256: `bed86e92fcb854b614dfb474cd3bab9e6fc1e5746399fc14bced9f8e4448eddf`
- raw JSON size: `8,059` bytes
- retrieval timestamp recorded inside result: `2026-08-31T22:51:27Z`

The downloaded artifact ZIP independently re-hashed to the GitHub-reported digest before the raw JSON was archived in this directory.

## Source identities observed

### IT2a / Takeshi Takahashi / EvaT

Current canonical file exactly matched the historical Phase63B byte authority:

- URL: `https://www.voynich.nu/data/IT2a-n.txt`
- SHA-256: `7f27a8b0feed8f6de0a99900df6bf912dd1d295c38e5f830bac8b41c3f536fb5`
- Git-blob SHA-1: `4d6d3f2537b1f507a257529b49c94af7d6e03446`
- bytes: `342,104`
- lines: `5,444`
- header: `#=IVTFF EvaT 2.0 M 3`

### GC2a / Glen Claston / v101

Current canonical file also exactly matched the historical Phase63B byte authority:

- URL: `https://www.voynich.nu/data/GC2a-n.txt`
- SHA-256: `b09570cb6c993bc2d87134d115e60a978650a8a6495483ddbb1f6005a586096f`
- Git-blob SHA-1: `8417a644fbd9c11cdaf85224f29cafee9ba1bdb0`
- bytes: `314,916`
- lines: `5,822`
- header: `#=IVTFF v101 2.0 M 6`

GC2a remains excluded from the exact 12-slot target unless a separately preregistered v101 compatibility layer is created; no such mapping was attempted here.

## Stage-A firewall

The executable and result explicitly exclude:

- pairwise occupancy contingency tables;
- any of the 66 Yule-Q target values;
- residual Z edges;
- residual graph energy;
- graph correlation/similarity;
- edge sign agreement/rank comparison;
- target empirical p-values.

The raw result records `scientific_pair_or_residual_metrics_computed: false`.

## Frozen disposition

IT2a Stage-A disposition:

> `AUTHORIZED_FOR_TARGET_PLAN`

This authorizes writing a separate preregistered target plan. It is **not** a scientific replication result.