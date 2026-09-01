# Issue #72 V2 Stage B2a — provenance

Stage B2a is the target-blind support freeze for the prospectively extended unchanged-Naibbe positive-control population `rep5..rep24`.

## Scientific workflow

- run: `33465227714`
- job: `99723583866`
- exact workflow/scientific head: `3da54653afff6bf4b7c3e414e1244f49e4393807`
- Stage B2 plan first-add: `5e34e7dd804c2679b4bb0cfa68ed7f2355f8e343`
- B2a script first-add: `cd97be52ea58c51186788b8ac18463e1573b420e`
- B2a workflow first-add: `3da54653afff6bf4b7c3e414e1244f49e4393807`
- parent main: `98a04953aabe9e228a17fa5808adf506a0833362`

Chronology gate passed before generation:

`B2 plan -> B2a support executable -> B2a workflow`

and `b2b_r1_calibration72_v2.py` did not yet exist.

## External authority

- CREMMA: `292525969ad98380b398e6606a9c2a36d51913ae`
- Naibbe: `f2675ec5dd275268bc64dd48ea64fc0e0e9827a2`
- encoder blob: `b566ad82e4b6ff0782ecdddebf77718dac44f292`
- codebook blob: `5cd34fb81d80faf3b4d57dbf1719c05ffde25302`
- decoder blob: `b56a1e6e615a7b2e31ad386efdf7e6f2ef2b9d7b`
- reused B0 support implementation blob: `ef3144591839395c18e1bdf308311bf99562bf9a`

## Actions artifact — primary raw authority

- artifact ID: `9784609004`
- artifact name: `issue72-v2-stageB2a-support-3da54653afff6bf4b7c3e414e1244f49e4393807`
- artifact ZIP SHA-256: `ea317e041adf084d66e27cb70953d431a0b4a3e7f88eba397107cd3740bfeffc`
- artifact size: `17,179` bytes

Exact files inside the artifact:

- `stage_b2a_support.json`: 91,795 bytes; SHA-256 `1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c`
- `stdout.txt`: 4,562 bytes; SHA-256 `362b4bb05d2b326210f34ce6fcd15547b60c3ea6e480ab9b3e44c3c63b8d9104`

## Permanent repository archive — repaired chunked transport

The first single-file base64 repository transport was discovered to be incomplete when Stage B2b run `33465741047`, job `99725103429`, attempted to reconstruct it. That run stopped before any Stage B2b R1 scoring.

See:

`STAGE_B2A_ARCHIVE_REPAIR_20260901.md`

The incomplete single-file transport is **not an authority**. The exact raw support JSON is permanently reconstructed from the ordered five-part archive:

- `archive/stage_b2a_support.json.gz.b64.part00`
- `archive/stage_b2a_support.json.gz.b64.part01`
- `archive/stage_b2a_support.json.gz.b64.part02`
- `archive/stage_b2a_support.json.gz.b64.part03`
- `archive/stage_b2a_support.json.gz.b64.part04`

Chunk SHA-256:

- part00: `6550601a713f73c697e509a68ff200dbd3463a0bd604d529e3e5e14ff9001807`
- part01: `ef10e5f044edfd3d12eb578aaa19a5db46b85f34aae0f2bcd884b8f141c3910c`
- part02: `cf35194b99cf1a025bc6bcb1d26f5cfd3f0f42e80906abdf61c73891b717ffc9`
- part03: `00bf9fb0ae056c45d01b2107db5ec1d20eb28eb00af5d229131a63d887b4082f`
- part04: `62dee3379b924d71b8135123ab5b00856c81b2510336c899b74947b057ca59ae`

Ordered concatenation produces:

- base64 text size: 20,124 bytes
- base64 SHA-256: `65f4e94d160c1e5538853532fc43054ff99682f5e1a8163ed4fc6e2e6b12e538`

Decoding produces deterministic `gzip -n -9` bytes:

- gzip size: 15,092 bytes
- gzip SHA-256: `2b18b9b45fa5ba9619c96f8bf83647b31017544dc634bb7c0b7181ed54e21a8a`

Decompression must produce the original primary raw authority:

- raw size: 91,795 bytes
- raw SHA-256: `1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c`

Reconstruction:

```bash
cat archive/stage_b2a_support.json.gz.b64.part00 \
    archive/stage_b2a_support.json.gz.b64.part01 \
    archive/stage_b2a_support.json.gz.b64.part02 \
    archive/stage_b2a_support.json.gz.b64.part03 \
    archive/stage_b2a_support.json.gz.b64.part04 \
  > /tmp/stage_b2a_support.json.gz.b64
base64 -d /tmp/stage_b2a_support.json.gz.b64 > /tmp/stage_b2a_support.json.gz
gzip -dc /tmp/stage_b2a_support.json.gz > /tmp/stage_b2a_support.json
sha256sum /tmp/stage_b2a_support.json
```

Expected raw SHA-256:

`1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c`

## Scientific firewall

The original B2a workflow and artifact freeze:

- `rep5_rep24_R1_scored=false`
- `issue72_intervention_surface_generated=false`
- `issue72_intervention_R1_scored=false`
- all `target_access` flags false.

The later archive repair changes only byte transport. Therefore Stage B2a still freezes population identity/support only. No complete-66 R1 result for `rep5..rep24`, and no EL/ES/ET/EG/PT/FI R1 result, was available before Stage B2b scoring authorization.
