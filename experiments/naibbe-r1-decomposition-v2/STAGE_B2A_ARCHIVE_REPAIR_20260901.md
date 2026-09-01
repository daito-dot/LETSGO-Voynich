# Issue #72 V2 — Stage B2a archive transport repair, 2026-09-01

Status: **MECHANICAL TRANSPORT REPAIR; SCIENCE UNCHANGED**

## Incident

The first Stage B2b workflow attempt failed before any Stage B2b R1 scoring because the repository copy of the Stage B2a base64/gzip transport was incomplete.

Failed run:

- workflow run: `33465741047`
- prepare job: `99725103429`
- exact attempted scientific head: `fba2721dd0ec8a00e8f6d83852ee87481607cf04`

The chronology gate completed successfully. Failure occurred in the next step, `Reconstruct exact B1 and B2a raw authorities`, with:

```text
base64: invalid input
gzip: stdin: unexpected end of file
```

The compile step, source-firewall step, all score matrix jobs, and aggregate job were therefore not executed.

At this incident point:

- rep5..rep24 R1 had **not** been scored;
- EL/ES/ET/EG/PT/FI surfaces had **not** been generated or loaded in Stage B2b;
- no Issue #72 intervention R1 had been scored;
- no threshold, seed, parser rule, source population, null namespace, or scientific statistic was changed.

## Raw evidence was intact

The authoritative Stage B2a Actions artifact remained intact:

- Stage B2a run: `33465227714`
- job: `99723583866`
- artifact ID: `9784609004`
- artifact ZIP SHA-256: `ea317e041adf084d66e27cb70953d431a0b4a3e7f88eba397107cd3740bfeffc`
- exact raw `stage_b2a_support.json` size: `91,795` bytes
- exact raw SHA-256: `1076940701ea7621bbaccaafa08e4f3d0b34a06af5cfb364e56fcdbdf620d83c`

Therefore this was an archive-transport defect, not a scientific-data defect.

## Correct deterministic transport

Starting from the exact Actions raw JSON, deterministic shell transport is:

```bash
gzip -n -9 -c stage_b2a_support.json > stage_b2a_support.json.gz
base64 -w 0 stage_b2a_support.json.gz > stage_b2a_support.json.gz.b64
```

Expected identities:

- gzip size: `15,092` bytes
- gzip SHA-256: `2b18b9b45fa5ba9619c96f8bf83647b31017544dc634bb7c0b7181ed54e21a8a`
- base64 size: `20,124` bytes
- base64 SHA-256: `65f4e94d160c1e5538853532fc43054ff99682f5e1a8163ed4fc6e2e6b12e538`

The earlier single repository base64 file was shorter than the expected `20,124` bytes and is not an authority.

## Chunked permanent archive

To avoid another large-text transport truncation, the exact 20,124-byte base64 is stored as five ordered chunks:

| chunk | bytes | SHA-256 |
|---|---:|---|
| `stage_b2a_support.json.gz.b64.part00` | 5,000 | `6550601a713f73c697e509a68ff200dbd3463a0bd604d529e3e5e14ff9001807` |
| `stage_b2a_support.json.gz.b64.part01` | 5,000 | `ef10e5f044edfd3d12eb578aaa19a5db46b85f34aae0f2bcd884b8f141c3910c` |
| `stage_b2a_support.json.gz.b64.part02` | 5,000 | `cf35194b99cf1a025bc6bcb1d26f5cfd3f0f42e80906abdf61c73891b717ffc9` |
| `stage_b2a_support.json.gz.b64.part03` | 5,000 | `00bf9fb0ae056c45d01b2107db5ec1d20eb28eb00af5d229131a63d887b4082f` |
| `stage_b2a_support.json.gz.b64.part04` | 124 | `62dee3379b924d71b8135123ab5b00856c81b2510336c899b74947b057ca59ae` |

Chunk first-add commits:

- part00 `648016b1396aa8484d90b2d8a50668d57a0e0567`
- part01 `9d2b524a69aeeb107db142927671b3e9fdcdd322`
- part02 `9388765d8dd9786f1ab1b27a19e1debe4364f06b`
- part03 `f4295a9d7a6483cfc10306e88c01980c961c769d`
- part04 `66123cd297e39a2bd70c8536a1953ef4b99acb3a`

## Required reconstruction gate

Future B2b execution must verify, in order:

1. each individual chunk SHA-256 above;
2. concatenated base64 size `20,124` and SHA-256 `65f4e94d...`;
3. decoded gzip size `15,092` and SHA-256 `2b18b9b...`;
4. decompressed raw JSON size `91,795` and SHA-256 `10769407...`.

Only after all four layers pass may B2b R1 scoring begin.

## Chronology interpretation

The repair chunks were necessarily committed after the failed transport attempt. They are not part of the preregistered scientific design and need not predate the B2b scorer.

Scientific chronology remains:

`Stage B2 plan -> target-blind B2a population freeze -> B1 raw authority -> B2b scorer/aggregator -> target scoring`.

The chunk files are only a byte-preserving carrier for the already frozen B2a raw authority. Their post-failure creation does not authorize any change to the raw Stage B2a population or scientific method.
